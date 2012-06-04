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


class Signal:

    def __init__(self, text):
        '''Set text, shell terms lists and signal.
        :return None'''
        self.text = text
        self.signal = np.zeros(len(text.words))
        self.terms = []

    def generate(self):
        '''Generate signal values.
        :return None'''
        self.scale()

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


class Term:

    def __init__(self, term, sign):
        '''Set term, shell value and count.
        :param str term: The term.
        :param bool sign: True/positive, False/negative.
        :return None'''
        self.term_count = 0
        self.value = 1 if sign else -1
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
        '''Step through each word in the text.
        :param Text text: A text.
        :return list: [[pos1,pos2], [pos1,pos2], ..].'''
        offsets = []
        for i,token in enumerate(self.walk(text.words)):
            if self.match(token):
                offsets.append([i,i])
        return offsets
