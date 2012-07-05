from  intra import *
import matplotlib.pyplot as plt
import requests as r

def load(url):
    global text
    res = r.get(url)
    text = Text(res.text)
    print res.text[:1000]

def q(query, width=1000):
    global text
    terms = query.split(' ')
    q = Query(text)
    s = Signal()
    q.signals.append(s)
    for term in terms:
        t = StaticTerm(term, True, width)
        s.terms.append(t)
    q.execute()
    plt.clf()
    plt.plot(q.signals[0].signal)
