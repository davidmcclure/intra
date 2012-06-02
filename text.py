# Intra.

import math as m
import const as c
import numpy as n
from stemming.porter2 import stem
from operator import itemgetter


def group(iterator, count):
    '''Yield n-tuples on an iterator.
    :param iter iterator: An iterable object.
    :param int count: Length of yielded tuples.
    :yield tuple: The chunked tuples.'''
    itr = iter(iterator)
    while True:
        yield tuple([itr.next() for i in range(count)])

def halflife_to_lifetime(halflife):
    '''Convert a halflife to a mean decay lifetime.
    :param int halflife: Halflife.
    :return float: Mean decay lifetime.'''
    return float(halflife) / m.log(2)

def decay(start, mean, threshold):
    '''Generate exponential decay values.
    :param float start: The starting value.
    :param float mean: The decay mean lifetime.
    :param float threshold: The decimal part of the
    \ start value after which to stop the computation.
    :return list values: The list of values.'''
    values = []
    end = start * threshold
    val = start
    itr = 0
    while val > end:
        val = start * m.exp(-itr / mean)
        values.append(val)
        itr += 1
    return values

def entoken(stream):
    '''Yield a stream of tokens.
    :param str stream: A string of text.
    :yield tuple: (word, char offset)'''
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

def clean(word):
    '''Normalize a word.
    :param str word: The word text.
    :return str: The cleaned word.'''
    for p in c.punct: word = word.replace(p, '')
    for b in c.breaks: word = word.replace(b, '')
    return word.lower()


class Text(object):

    def __init__(self, text):
        '''Tokenize text.
        :param str text: The text stream.
        :return None'''
        self.text = text
        self.words = []
        for word in entoken(text):
            self.words.append(word)

    def snippet(self, offset, radius):
        '''Get a text snippet.
        :param int offset: The center character offset.
        :param int radius: The character radius.
        :return str: The snippet.'''
        return self.text[offset-radius:offset+radius]

    def offsets(self, word):
        '''Get list of stemmed token offsets.
        :param str word: The word.
        :return list offsets: [offset1, offset2, ...]'''
        word = stem(word)
        offsets = []
        for i,w in enumerate(self.words):
            if word == w[0]:
                offsets.append(i)
        return offsets

    def radii(self, word):
        '''Get list of radii between all instances of token.
        :param str word: The word.
        :return list radii: [radius2, radius2, ...]'''
        radii = []
        offsets = self.offsets(word)
        for i,j in group(offsets, 2):
            radii.append(j-i)
        return radii

    def decay(self, word, halflife, threshold, snippet_radius):
        '''Single word exponential decay search.
        :param str word: The word.
        :param float halflife: The decay halflife as word radius.
        :param float threshold: The decimal part of the decay
        \ start value after which to stop the computation.
        :param int snippet_radius: The highlighting radius.
        :return list results: [(snippet, offset %)]'''
        # Compute out the decay series.
        lifetime = halflife_to_lifetime(halflife)
        series = decay(1., lifetime, threshold)
        radius = len(series)
        # Get occurrences, shell out the sum matrix.
        offsets = self.offsets(word)
        wordcount = len(self.words)
        sums = n.zeros(wordcount)
        # Compute forward offsets.
        for o in offsets:
            end = o+radius
            if end > wordcount: end = wordcount
            for pos,val in zip(range(o,end), series):
                sums[pos] += val
        # Compute negative offsets.
        for o in offsets:
            rseries = series
            start = o-radius+1
            if start < 0:
                rseries = series[start:]
                start = 1
            for pos,val in zip(range(start,o), reversed(rseries)):
                sums[pos] += val
        # Find local maximums.
        results = []
        text_len = float(len(self.text))
        i = 1
        for pos,word in zip(sums[1:-1], self.words[1:-1]):
            if pos > sums[i-1] and pos > sums[i+1]:
                snippet = self.snippet(word[1], snippet_radius)
                ratio = word[1]/text_len
                results.append((snippet, pos, ratio))
            i += 1
        return sorted(results, key=itemgetter(1), reverse=True)
