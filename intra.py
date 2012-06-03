# Intra.

import math as m
import numpy as n
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


class Query:

    def __init__(self):
        '''Shell signals list.
        :return None'''
        self.signals = []


class Signal:

    def __init__(self):
        '''Shell terms lists.
        :return None'''
        self.positive = []
        self.negative = []


class Term:

    # abstractmethod
    def match(self, sample):
        '''Evaluate a text sample against the term.
        :param list sample: A list of tokens.
        :return bool: True if the term matches.'''
        pass


class StaticTerm(Term):

    def __init__(self, term):
        '''Set term.
        :param str term: The term.
        :return None'''
        self.term = stem(term)

    def match(self, sample):
        '''Evaluate for a single term match.
        :param list sample: List with 1 token ~ [token].
        :return bool: True if the term matches.'''
        return sample[0] == self.term
