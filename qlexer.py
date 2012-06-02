# Query lexer.
# Follows Jay Conrod's tutorial:
# http://www.jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1

import sys
import re


RESERVED = 'RESERVED'
TERM = 'TERM'

expressions = [
    (r'[ \n\t]+',               None),
    (r'\(',                     RESERVED),
    (r'\)',                     RESERVED),
    (r'AND',                    RESERVED),
    (r'OR',                     RESERVED),
    (r'NOT',                    RESERVED),
    (r'LIKE',                   RESERVED),
    (r'[A-Za-z][A-Za-z0-9]*',   TERM)
]

def intra_lex(characters):
    return lex(characters, expressions)


def lex(characters, expressions):
    '''Lex a character stream.
    :param str characters: Character stream.
    :param list expressions: Regexes and tags.
    :return list tokens: Tokens.'''
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for expr in expressions:
            pattern, tag = expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        pos = match.end(0)
    return tokens
