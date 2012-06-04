from  intra import *
f = open('./texts/test.txt')

string = ''
for line in f:
    string += line

t = Text(string)
s = Signal(t)

plus1 = StaticTerm('word', True, 2)
plus2 = StaticTerm('david', False, 2)
s.terms.append(plus1)
s.terms.append(plus2)

s.generate()
