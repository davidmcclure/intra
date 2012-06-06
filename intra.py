# Intra.

import math as m
import numpy as np
from stemming.porter2 import stem
from operator import itemgetter
import re


scrub = [
    '\n',
    '\r',
    '(',
    ')',
    ':',
    ';',
    ',',
    '!',
    '.',
    '?',
    '/',
    '"',
    '*',
    "'"]

def group(iterator, count):
    '''Yield n-tuples on an iterator.
    :param iter iterator: An iterable object.
    :param int count: Length of yielded tuples.
    :yield tuple: The chunked tuples.'''
    itr = iter(iterator)
    while True:
        yield tuple([itr.next() for i in range(count)])

def decay(height, fwhm, threshold):
    '''Generate exponential decay values.
    :param float height: The starting value.
    :param float fwhm: Full width at half maximum.
    :param float threshold: The decimal part of the
    \ start value after which to half the series.
    :return list values: The list of values.'''
    c = fwhm / 2*m.sqrt(2*m.log(2))
    values = []
    end = height * threshold
    val = height
    i = 0
    while abs(val) > abs(end):
        val = height * m.exp(-(i**2)/(2*c**2))
        values.append(val)
        i += 1
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
        elif word and char == ' ':
            yield (stem(clean(word)), offset)
            offset = None
            word = ''

def clean(word):
    '''Normalize a word.
    :param str word: The word text.
    :return str: The cleaned word.'''
    for s in scrub: word = word.replace(s, '')
    return word.lower()

def maxes(signal):
    '''Find indices of local maxima on a signal.
    :param list signal: The signal.
    :yield list maxes: The maxima positions.'''
    maxes = []
    i = 1
    for s in signal[1:-1]:
        if s > signal[i-1] and s > signal[i+1]:
            maxes.append(i)
        i += 1
    return maxes


class Text:

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

class Query:

    def __init__(self, text):
        '''Set text, shell signals list.
        :param Text text: A text.
        :return None'''
        self.text = text
        self.signals = []

    def execute(self, count, radius):
        '''Run query.
        :param int count: The number of results.
        :param int radius: The snippet character radius.
        :return list results: The result snippets.'''
        # Find local maxima.
        maxes = []
        for s in self.signals:
            maxes += s.maxima()
        maxes = sorted(maxes,key=itemgetter(1),reverse=True)
        # Build results.
        results = []
        for m in maxes[:count]:
            offset = self.text.words[m[0]][1]
            snippet = self.text.snippet(offset, radius)
            results.append(snippet)
        return results



class Signal:

    def __init__(self, text):
        '''Set text, shell terms lists and signal.
        :param Text text: A text.
        :return None'''
        self.text = text
        self.signal = np.zeros(len(text.words))
        self.terms = []

    def scale(self):
        '''Scale terms based on frequency.
        :return None'''
        # Build counts and max.
        max = 0
        for term in self.terms:
            term.count(self.text)
            if term.term_count > max:
                max = term.term_count
        # Scale the term values.
        for term in self.terms:
            val = float(max)/term.term_count
            term.value = term.value * val

    def generate(self):
        '''Generate signal values.
        :return None'''
        self.scale()
        for term in self.terms:
            offsets = term.offsets(self.text)
            series = decay(term.value, term.fwhm, 0.1)
            length = len(self.signal)
            radius = len(series)
            # Right decay.
            for o1,o2 in offsets:
                b2 = o2+radius
                if b2 > length: b2 = length
                for p,v in zip(range(o2,b2), series):
                    self.signal[p] += v
            # Left decay.
            for o1,o2 in offsets:
                rseries = series
                b1 = o1-radius+1
                if b1 < 0:
                    rseries = series[:b1]
                    b1 = 1
                rseries = reversed(rseries)
                for p,v in zip(range(b1,o1), rseries):
                    self.signal[p] += v

    def maxima(self):
        '''Find local maxima.
        :return list maxima: The maxima.'''
        self.generate()
        maxima = []
        i = 1
        for s in self.signal[1:-1]:
            if s > self.signal[i-1] and s > self.signal[i+1]:
                maxima.append((i, self.signal[i]))
            i += 1
        return maxima


class Term:

    def __init__(self, term, sign, fwhm):
        '''Set parameters, parse term.
        :param str term: The term.
        :param bool sign: True/positive, False/negative.
        :param int fwhm: Full width at half maximum.
        :return None'''
        self.term_count = 0
        self.value = 1 if sign else -1
        self.fwhm = float(fwhm)
        self.parse(term)

    # abstractmethod
    def parse(self, term):
        '''Prepare the term input for matching.
        :param str term: The term.
        :return None'''
        pass

    # abstractmethod
    def match(self, sample):
        '''Evaluate a text sample against the term.
        :param list sample: A list of tokens.
        :return bool: True if the term matches.'''
        pass

    # abstractmethod
    def walk(self, text):
        '''Yield text samples for matching.
        :param Text text: A text.
        :yield list: A list of tokens.'''
        pass

    # abstractmethod
    def offsets(self, text):
        '''Return list of offset start and end
        \ positions of all term matches in the text.
        :param Text text: A text.
        :return list: [[pos1,pos2], [pos1,pos2], ..].'''
        pass

    def count(self, text):
        '''Build term count.
        :param Text text: A text.
        :return None'''
        for token in self.walk(text.words):
            if self.match(token):
                self.term_count += 1


class StaticTerm(Term):

    def parse(self, term):
        '''Set term.
        :param str term: The term.
        :return None'''
        self.term = stem(term)

    def match(self, sample):
        '''Evaluate for a single term match.
        :param list sample: List with 1 token ~ [token].
        :return bool: True if the term matches.'''
        return sample[0][0] == self.term

    def walk(self, text):
        '''Step through each word in the text.
        :param Text text: A text.
        :yield list: [token].'''
        for word in text:
            yield [word]

    def offsets(self, text):
        '''Return list of offset start and end
        \ positions of all term matches in the text.
        :param Text text: A text.
        :return list: [[pos1,pos2], [pos1,pos2], ..].'''
        offsets = []
        for i,token in enumerate(self.walk(text.words)):
            if self.match(token):
                offsets.append([i,i])
        return offsets
