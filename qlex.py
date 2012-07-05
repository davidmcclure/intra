# Query lexer.
# Follows Jay Conrod's tutorial:
# http://www.jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1

import sys
import re
import types
import intra as i


OP =        'OP'
TERM =      'TERM'

expressions = [
    (r'[ \n\t]+',               None),
    (r'\(',                     OP),
    (r'\)',                     OP),
    (r'AND',                    OP),
    (r'OR',                     OP),
    (r'NOT',                    OP),
    (r'LIKE',                   OP),
    (r'[A-Za-z][A-Za-z0-9]*',   TERM)
]

def p(characters):
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
