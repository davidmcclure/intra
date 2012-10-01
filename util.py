from nltk.stem.porter import PorterStemmer


def entoken(text):

    '''Yield stemmed tokens with character offets.

    :param string text: The text.

    :yield tuple: Tuples of (token, offset).'''

    porter = PorterStemmer()

    offset = None
    length = len(text)
    token = ''

    # Walk characters.
    for i,char in enumerate(text):

        if char != ' ':
            token += char
            if offset is None: offset = i

        if token and (char == ' ' or i+1 == length):
            yield (porter.stem_word(token), offset)
            offset = None
            token = ''

