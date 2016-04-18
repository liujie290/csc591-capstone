(defproject scraper "0.1.0-SNAPSHOT"
  :description "Collects data and stores data from congress.gov"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [[org.clojure/clojure "1.8.0"]
                 [clj-http "3.0.1"]
                 [enlive "1.1.6"]
                 [semantic-csv "0.1.0"]
                 [org.clojure/data.json "0.2.6"]
                 [com.velisco/clj-ftp "0.3.5"]
                 [org.clojure/data.csv "0.1.3"]]
  :main ^:skip-aot scraper.core
  :target-path "target/%s"
  :profiles {:dev {:dependencies [[midje "1.8.3"]]
                   :plugins [[lein-midje "3.2"]] }
             :uberjar {:aot :all}})
