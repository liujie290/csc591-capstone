(ns scraper.core-test
  (:use midje.sweet)
  (:require [clojure.test :refer :all]
            [scraper.core :refer :all]))

(fact "`fetch-house-info` retrieves and returns csv of a house number"
      (fetch-house-info 113) =not=> nil?
      (fetch-house-info 113) => (contains []))

(def row  {:bill "H R 3572", :date "2014-12-02", :description "To revise the boundaries of certain John H. Chafee Coastal Barrier Resources System units in North Carolina", :naytotal "7", :number "536", :question "On Motion to Suspend the Rules and Pass, as Amended", :result "Passed", :session "2nd", :yeatotal "410"})

(fact "`get-bill-results' crawls gov site for bill text"
      (get-bill-results row) =not=> nil?)
