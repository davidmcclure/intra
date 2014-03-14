(ns intra.core
  (:require [stemmers.porter :as porter]))

(defn add-token
  "Add a new token (with left-side character offset) to a list of tokens."
  [tokens new-token right-offset]
  (conj tokens {:token (porter/stem new-token)
                :offset (- right-offset (count new-token))}))

(defn get-tokens
  "Tokenize a string, storing the original character offset for each token."
  [text]
  (let [text (clojure.string/lower-case text)
        char-count (count text)]
    (loop [offset 0
           token ""
           tokens []]
      (if (< offset char-count)
        (let [character (get text offset)
              offset (inc offset)]
          (if (re-matches #"[a-z]" (str character))
            (if (and (= offset char-count) (not= token ""))
              (recur offset "" (add-token tokens (str token character) offset))
              (recur offset (str token character) tokens))
            (if (not= token "")
              (recur offset "" (add-token tokens token (dec offset)))
              (recur offset "" tokens))))
        tokens))))

(defn get-types
  "Map unique types to a vector of token instance offsets in the text."
  [tokens]
  (let [word-count (count tokens)]
    (loop [offset 0
           types {}]
      (if (< offset word-count)
        (let [token (get-in tokens [offset :token])]
          (if (contains? types token)
            (recur (inc offset) (update-in types [token] #(conj % offset)))
            (recur (inc offset) (assoc types token [offset]))))
        types))))

(defn get-heights
  "For each type, compute a starting height for decay curves."
  [types scale]
  (let [min-count (reduce min (vals types))
        max-count (reduce max (vals types))]
    (reduce (fn [heights [k v]] (assoc heights k (scale v))) {} types)))
