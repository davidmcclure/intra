# Query lexer.
# Follows Jay Conrod's tutorial:
# http://www.jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1

import sys
import re


LPAREN =    'LPAREN'
RPAREN =    'RPAREN'
OP =        'OP'
TERM =      'TERM'

expressions = [
    (r'[ \n\t]+',               None),
    (r'\(',                     LPAREN),
    (r'\)',                     RPAREN),
    (r'AND',                    OP),
    (r'OR',                     OP),
    (r'NOT',                    OP),
    (r'LIKE',                   OP),
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

def parse(tokens, g=[]):
    '''Parse a list of tokens.
    :param list tokens: List of tokens.
    :return list tokens: Tokens.'''
    if not tokens: return g
    token = tokens.pop(0)
    if token[1] == RPAREN:
        return g
    elif token[1] == TERM or token[1] == OP:
        g.append(token)
    elif token[1] == LPAREN:
        sg = []
        g.append(parse(tokens, sg))
    return parse(tokens, g)





    # token = tokens.pop(0)
    # if token[1] == LPAREN:
    #     while tokens[0][1] != RPAREN:
    #         g.append(parse(tokens))
    #     tokens.pop(0)
    # else:
    #     g.append(token)
    # return parse(tokens, g)
