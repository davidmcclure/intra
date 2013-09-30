
# vim: set expandtab tabstop=2 shiftwidth=2 softtabstop=2 cc=80;

# intra.Text: A text on which queries can be performed.
# :copyright: (c) 2013 by David McClure
# :license: BSD


import re


class Text:


    def __init__(self, text):

        '''
        Store the raw text string and initialize the token/types containers.

        Arguments:
            text [String]: The raw text string.
        '''

        self.text = text
        self.tokens = None
        self.types = None


    def tokenize(self):

        '''
        Tokenize the text. Store each token as a 2-tuple containing the token
        and its starting character offset in the original text. For each type,
        type, record the set of word offsets at which the type appears.
        '''

        self.tokens = []
        self.types = {}

        token = ''
        start = 0
        count = 0

        for i, c in enumerate(self.text):

            is_letter = re.match('[a-zA-Z]', character)

            if is_letter:
                if token == '': start = i
                word += c

            if token != '' and (not is_letter or i+1 == len(self.text)):

                # TODO: Lowercase/stem token.
                self.tokens.append((token, offset))
                self.types[token] = self.types.get(token, []).append(count)

                count += 1
                token = ''
