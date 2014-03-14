(defproject intra "0.1.0-SNAPSHOT"
  :description "Fuzzy searching inside of long documents."
  :url "https://github.com/davidmcclure/Intra"
  :license {:name "Apache 2.0"
            :url "http://www.apache.org/licenses/LICENSE-2.0.txt"}
  :dependencies [[org.clojure/clojure "1.5.1"]
                 [stemmers "0.2.1"]]
  :main ^:skip-aot intra.core
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}})
