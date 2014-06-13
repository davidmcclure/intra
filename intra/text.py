

import intra.utils as utils
from nltk.stem import PorterStemmer
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
        porter = PorterStemmer()

        # Match continuous letters.
        pattern = re.compile('[a-z]+')
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
