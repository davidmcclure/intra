
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
        self.tokens = []


    def tokenize(self):

        '''
        Populate the `tokens` attribute with a list of tuples, one for each
        word in the text, each containing the word and the original character
        offset of the word in the text.
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
