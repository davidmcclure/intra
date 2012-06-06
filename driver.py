from  intra import *
f = open('./texts/wp.txt')

string = ''
for line in f:
    string += line

t = Text(string)
q = Query(t)
s = Signal(t)
q.signals.append(s)

term1 = StaticTerm('andrew', True, 500)
term2 = StaticTerm('sky', True, 500)
s.terms.append(term1)
s.terms.append(term2)

results = q.execute(10, 2000)
