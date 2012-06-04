from  intra import *
f = open('./texts/cp.txt')

string = ''
for line in f:
    string += line

t = Text(string)
s = Signal(t)

axe = StaticTerm('axe', True)
god = StaticTerm('god', False)
s.terms.append(axe)
s.terms.append(god)

s.scale()
