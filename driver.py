from  intra import *
f = open('./texts/test.txt')

string = ''
for line in f:
    string += line

t = Text(string)
q = Query(t)
s = Signal()
q.signals.append(s)

term1 = OrTerm(['david', 'kara'], True, 3)
s.terms.append(term1)

results = q.execute()
