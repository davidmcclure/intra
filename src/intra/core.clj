(ns intra.core
  (:require [stemmers.porter :as porter]))

(defn add-token
  "Add a new token (with left-side character offset) to a list of tokens."
  [tokens new-token right-offset]
  (conj tokens {:token (porter/stem new-token)
                :left (- right-offset (count new-token))
                :right right-offset}))

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

(defn get-terms
  "Map unique terms to a vector of token instance offsets in the text."
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

(defn get-term-counts
  "Map unique terms to the number of times the type occurs in the text."
  [terms]
  (into {}
    (for [[term offsets] terms]
      [term (count offsets)])))

(defn get-term-weights
  "Map unique terms to weight between 0 and 1."
  [terms adjustor]
  (let [counts (vals (get-term-counts terms))
        min-count (reduce min counts)
        max-count (reduce max counts)]
    (into {}
      (for [[term offsets] terms]
        [term (adjustor (count offsets) min-count max-count)]))))
