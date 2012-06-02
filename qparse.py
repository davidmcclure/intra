# Query parser.
# Follows Jay Conrod's tutorial:
# http://www.jayconrod.com/posts/39/a-simple-interpreter-from-scratch-in-python-part-3

from qlex import *
from qcomb import *
from qast import *


def parse(tokens):
    return parser()(tokens, 0)

def parser():
    return Phrase()
