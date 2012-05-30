# Intra.

import const as c
from stemming.porter2 import stem


def clean(word):
    '''Normalize a word.
    :param word: The word text.'''
    for p in c.punct: word = word.replace(p, '')
    for b in c.breaks: word = word.replace(b, ' ')
    return word.lower()

def entoken(stream):
    '''Yield a stream of tokens.
    :param stream: A string of text.'''
    offset = None
    word = ''
    for i, char in enumerate(stream):
        if char != ' ':
            word += char
            if offset is None: offset = i
        elif char == ' ' or i == len(stream):
            yield (stem(clean(word)), offset)
            offset = None
            word = ''


class Text(object):

    def __init__(self, text):
        '''Tokenize text.
        :param text: The text stream.'''
        self.text = text
        self.words = []
        for word in entoken(text):
            self.words.append(word)

    def snippet(self, offset, radius):
        '''Get a text snippet.
        :param offset: The center character offset.
        :param radius: The character radius.'''
        return self.text[offset-radius:offset+radius]

    def search(self, word, radius):
        '''Direct word search.
        :param word: The word.
        :param radius: The highlighting radius.'''
        word = stem(word)
        hits = []
        for w in self.words:
            if word == w[0]:
                hits.append(self.snippet(w[1], radius))
        return hits

    def dbscan(self, word, radius, eps, min_pts):
        '''DBSCAN implementation.
        http://en.wikipedia.org/wiki/DBSCAN
        :param word: The word.
        :param radius: The highlighting radius.
        :param eps: Clustering word-radius distance.
        :param min_pts: Minimum points for cluster.'''
        # Get all results, forming a list of 3-tuples
        # with form (word, char offset, token offset).
        word = stem(word)
        hits = []
        for i, w in enumerate(self.words):
            if word == w[0]:
                hits.append((w[0], w[1], i))
        # Cluster the results.
        cluster = []
        clusters = []
        cluster.append(hits[0])
        for h in hits[1:]:
            if len(cluster) == 0:
                cluster.append(h)
            elif h[2] - cluster[-1][2] < eps:
                cluster.append(h)
            else:
                if len(cluster) >= min_pts:
                    clusters.append(cluster)
                cluster = []
        # Get snippets and bounds for the clusters.
        results = []
        text_len = float(len(self.text))
        for cluster in clusters:
            snippets = []
            # Form snippets.
            for c in cluster:
                snippet = self.snippet(c[1], radius)
                snippets.append(snippet)
            # Get bounds.
            b1 = cluster[0][1]/text_len
            b2 = cluster[-1][1]/text_len
            results.append((snippets, (b1,b2)))
        return results
