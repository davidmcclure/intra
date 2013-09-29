
# vim: set expandtab tabstop=2 shiftwidth=2 softtabstop=2 cc=80;

# intra.Text: A text on which queries can be performed.
# :copyright: (c) 2013 by David McClure
# :license: BSD


import re


class Text:


    def __init__(self, text):

        '''
        Store the raw text string and initialize the tokens list.

        :type text: string
        :param text: The raw text string.
        '''

        self.text = text
        self.tokens = None
        self.types = None


    def tokenize(self):

        '''
        Tokenize the text. For each token, store the starting character offset
        in the original text. For each type, store the set of token offsets at
        which the type appears.
        '''

        word = ''

        for i, character in enumerate(self.text):

            is_letter = re.match('[a-zA-Z]', character)

            if is_letter:
                if len(word) == 0: offset = i
                word += character

            if word and (not is_letter or i+1 == len(self.text)):
                self.tokens.append((word, offset))
                word = ''
