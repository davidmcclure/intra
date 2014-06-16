

from nltk.stem import PorterStemmer
from sklearn.neighbors import KernelDensity
from scipy import stats

import numpy
import re
import intra.utils as utils
import requests


class Text(object):


    @classmethod
    def from_file(cls, path):

        """
        Create a text from a filepath.

        :param cls: The Text class.
        :param path: The filepath.
        """

        return cls(open(path, 'r').read())


    @classmethod
    def from_url(cls, url):

        """
        Create a text from a URL.

        :param cls: The Text class.
        :param path: The URL.
        """

        return cls(requests.get(url).text)


    def __init__(self, text):

        """
        Store and tokenize the text.

        :param text: The text as a raw string.
        """

        self.text = text
        self.tokenize()


    def tokenize(self):

        """
        Tokenize the text. Store left and right character offsets for each
        token, and build a token -> offsets map.
        """

        self.tokens = []
        self.offsets = {}

        # Strip tags and downcase.
        text = utils.strip_tags(self.text).lower()

        pattern = re.compile('[a-z]+')
        porter = PorterStemmer()

        # Walk words in the text.
        for i, match in enumerate(re.finditer(pattern, text)):

            stemmed = porter.stem(match.group(0))

            # Token:
            self.tokens.append({
                'token':    stemmed,
                'left':     match.start(),
                'right':    match.end()
            })

            # Token -> offset:
            if stemmed in self.offsets: self.offsets[stemmed].append(i)
            else: self.offsets[stemmed] = [i]


    def get_bare_tokens(self):

        """
        Get a list of the raw, unadorned tokens in the text.
        """

        return [token['token'] for token in self.tokens]


    def get_query_offsets(self, query):

        """
        Given a query text, compute an ordered list of offsets in this text
        where words in the query text appear.

        :param query: A query text.
        """

        offsets = []
        for token in query.get_bare_tokens():
            offsets += self.offsets[token]

        return sorted(offsets)


    def kde_scipy(self, query, resolution=1000):

        """
        Scipy kernel density estimation.

        :param query: A query text.
        :param resolution: The number of points to evaluate.
        """

        offsets = self.get_query_offsets(query)

        # Generate evenly-spaced sampling points.
        samples = numpy.linspace(0, len(self.tokens), resolution)

        # Estimate the density.
        kde = stats.gaussian_kde(offsets)
        return kde.evaluate(samples)
