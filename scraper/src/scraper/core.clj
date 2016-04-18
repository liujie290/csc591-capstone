(ns scraper.core
  (:require [clj-http.client :as client]
            [clojure.data.csv :as csv]
            [net.cgrand.enlive-html :as html]
            [miner.ftp :as ftp]
            [clojure.data.json :as json]
            [semantic-csv.core :as sc :refer :all]
            [clojure.java.io :as io]
            [clojure.string :as str])
  (:gen-class))

(defn fetch-house-info
  "Fetchs house info csv"
  [^Integer congress-num]
  (ftp/with-ftp [client "ftp://anonymous:pwd@voteview.com/dtaord"]
    (let [house-desc (str "h" congress-num "desc.csv")
          stream (ftp/client-get-stream client house-desc)]
      (->> (csv/read-csv
            (io/reader stream))
           mappify
           doall))))

(def search-url "https://www.congress.gov/search")

(defn query-congress
  "build http query for congress"
  [congress-num bill]
  {:q 
   (json/write-str
    {:source "legislation"
     :search bill
     :congress (str congress-num)})
  })

(defn build-bill-result
  "builds a bill result"
  [[result congress-man]]
  {:bill {:name (:content result)
          :url (get-in result [:attrs :href])}
   :congress-man {:name (:content congress-man)
                  :url (get-in congress-man [:attrs :href])}})

(defn get-bill-results
  "Crawls gov site to get text of bill"
  [congress-num, bill]
  (let [query (query-congress congress-num bill)
        result (:body (client/get search-url {:query-params query}))
        html-res (html/html-resource (java.io.StringReader. result))]
    (->> (html/select html-res #{[:#main :> :ol html/first-child :a]})
         (partition 2)
         (map build-bill-result))))

(defn pairs-reg
  [str]
  (re-seq #"^\s*\[(\w+)\] => (.*)$" str))

(defn parse-summary
  [html-res]
  (->> (html/select html-res #{[:#main :> :div.generated-html-container]})
       (map html/text)
       (map #(str/replace % #"[\t\n]" ""))
       (map #(str/replace % #"\s+" " "))
       (map #(str/replace % #"[^0-9a-zA-Z\s]+" ""))))

(defn parse-summary-text
  [html-res]
  (print html-res)
  (->> (html/select html-res #{[:#billTextContainer]})
       (map html/text)
       (map #(str/replace % #"[\t\n]" ""))
       (map #(str/replace % #"\s+" " "))
       (map #(str/replace % #"[^0-9a-zA-Z\s]+" ""))))

(defn follow-text-link
  [html-res]
  (->> (html/select html-res
                    #{[:#content :> :div.tabs_container.bill-only
                       :> :ul :> [:li (html/nth-of-type 2)] :> :h2 :> :a]})
       (map #(get-in % [:attrs :href]))
       (map #(client/get %))
       (map :body)
       (map #(html/html-resource (java.io.StringReader. %)))
       first))

(defn follow-summary-text-link
  [html-res]
  (->> (html/select html-res
                    #{[:#main :> [:div (html/nth-of-type 3)] :> :ul :> [:li (html/nth-of-type 3)] :> :a]})
       (print)
       (map #(get-in % [:attrs :href]))
       (map #(client/get %))
       (map :body)
       (map #(html/html-resource (java.io.StringReader. %)))
       first))

(defn tail
  [[head & tail]]
  tail)

(defn keyvalue
  [[key value]]
  {(keyword key) value})

(defn parse-status-details
  [[status details]]
  (let [parsed-details (->> (first (:content details))
                            (str/split-lines)
                            (map pairs-reg)
                            (filter (comp not nil?))
                            (map #(tail (first %)))
                            (map keyvalue)
                            (into {}))]
    (-> {}
        (assoc :status status)
        (assoc :details parsed-details))))

(defn parse-current-status
  [html-res]
  (->> (html/select html-res #{[:ol.bill_progress :li.selected]})
       (map #(get-in % [:content]))
       (map parse-status-details)))

(defn get-bill-details
  [bill-result]
  (let [result (:body (client/get (get-in bill-result [:bill :url])))
        html-res (html/html-resource (java.io.StringReader. result))
        html-summary (follow-text-link html-res)]
    (-> bill-result
        (assoc-in [:bill :summary] (parse-summary html-summary) )
        (assoc-in [:bill :current-status] (parse-current-status html-res)))))

(defn get-bill
  [congress-num bill]
  (let [bill-results (get-bill-results congress-num bill)]
    (get-bill-details (first bill-results))))

(def ignore-words ["QUORUM" "JOURNAL" "ADJOURN"])

(defn in? 
  "true if coll contains elm"
  [coll elm]  
  (some #(= elm %) coll))

(defn map-to-bills
  [congress-info]
  (->> congress-info
       (map :bill)
       (filter #((comp not in?) ignore-words %))
       (filter #((comp not =) "" %))
       (set)
       (into [])))

(defn save-bill-to-path
  [path congress-num bill-name]
  (if-not (nil? bill-name)
    (let [bill (get-bill congress-num bill-name)]
      (println bill-name)
      (spit (str path "/" bill-name ".json") bill))))

(defn load-data
  [congress-num path]
  (let [congress-info (fetch-house-info congress-num)
        bills (map-to-bills congress-info)
        full-path (str path "/" congress-num "/.")]
    (io/make-parents full-path)
    (loop [[bill & tail] bills]
      (save-bill-to-path full-path congress-num bill)
      (if-not (nil? bill)
        (recur tail))
      )))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (let [[congress-num path] args]
    (load-data congress-num path)))
