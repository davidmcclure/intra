from  intra import *
import matplotlib.pyplot as plt
import requests as r
import re

text = None

def load(url, html=False):
    global text
    res = r.get(url)
    stream = res.text
    if html:
        p = re.compile(r'<.*?>')
        stream = p.sub('', stream)
    text = Text(stream)
    print 'loaded'

def paste(stream):
    global text
    text = Text(stream)

def qand(query, width=1000):
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

def qor(query, width=1000):
    global text
    terms = query.split(' ')
    q = Query(text)
    s = Signal()
    q.signals.append(s)
    t = OrTerm(terms, True, width)
    s.terms.append(t)
    q.execute()
    plt.clf()
    plt.plot(q.signals[0].signal)

def qlike(query, width=1000):
    global text
    terms = query.split(' ')
    q = Query(text)
    s = Signal()
    q.signals.append(s)
    for term in terms:
        t = LikeTerm(term, True, width)
        s.terms.append(t)
    q.execute()
    plt.clf()
    plt.plot(q.signals[0].signal)
    for term in s.terms:
        print term.terms

def onClick(event):
    global text
    print '-------------------'
    print text.wordsnippet(int(event.xdata), 1000).format(u'')
    print '-------------------'
    return

fig = plt.figure()
fig.canvas.mpl_connect('button_press_event', onClick)
