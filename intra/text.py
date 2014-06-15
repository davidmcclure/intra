

import intra.utils as utils
from nltk.stem import PorterStemmer
import requests
import re


class Text(object):

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
