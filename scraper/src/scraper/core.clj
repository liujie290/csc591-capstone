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
  [congress-num, {:keys [session bill]}]
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
  (->> (html/select html-res [:div#bill-summary])
       (map html/text)))

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
        html-res (html/html-resource (java.io.StringReader. result))]
    (-> bill-result
        (assoc-in [:bill :summary] (parse-summary html-res))
        (assoc-in [:bill :current-status] (parse-current-status html-res)))))


(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println "Hello, World!"))
