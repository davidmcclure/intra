

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

        pass # TODO

    def get_bare_tokens(self):
        """
        Get a 1-dimensional array of the raw, stemmed tokens.
        """

        pass # TODO
