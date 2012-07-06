# Intra

Intra is a prototype application that experiments with a new approach to searching inside of long texts. Instead of trying to imitate the structure of document-based approaches by chopping long texts into short segments and then returning subsets of the segments, Intra models relevancy by converting search queries into two-dimensional "signals" - each word in the text is mapped onto an integer on the X axis, and Intra computes a y-axis value for each word position.

This approach has two advantages. First, it makes it possible for the user to immediately intuit the structure of the query result across the linear duration of the text - positional information about the relevancy of the query is completely baked into the presentation of the results. Instead of having to make substantive decisisions for the user about what gets returned and in what order, the signal data can be presented unmodified and unadorned, allowing the user to bore in on the actual source text by interacting with the signal graph.

Second, Intra's approach to modeling relevancy makes it simple to go beyond single-term searches and model compound and boolean queries (AND, OR, NOT, LIKE) just by arithmetically summing an arbitrary number of signals.

## The query model

Intra models relevancy as a gaussian curve that "emits" in both directions away from a term match. When a query is executed, Intra starts with a one-dimensional array with a length equal to the wordcount of the text, filled with zeros (one zero per word). For each term match in the text, Intra will compute out a gaussian curve with a height of 1 centered on the offset position of the matching token.

For example, using this text:

```text
word word match1 match1 word word word word match1 match2 word word
```

The signal curve for the query **qand('match1', 2)** with a decay halflife of 2 words looks like this:

![qand1](http://dclure.org/wp-content/uploads/2012/07/qand-1.png)

Since a curve is summed onto the array for each term match, term clustering is automatically modeled in the final signal - the curve is higher around offsets 3 and 4 than it is at 8 because the decay curves for the two side-by-side occurrences of "match1" add on top of one another to produce a higher signal value.

For more than one query term, logical "AND" is modeled by just computing the curves for each of the terms and then summing them to form a composite signal. For example, **qand('match1 match2', 2)** gives this signal:

![qand2](http://dclure.org/wp-content/uploads/2012/07/qand-2.png)

Here, though, you can see that the phrase "match1 match2" produced a higher spike than "match1 match1." This is because Intra scales the center values for the decay curves based on the relative frequency of the terms in the query, the intuition beight that infrequent terms should be "higher energy" than frequent terms.

Logical "OR" queries, meanwhile, do not scale the center values and just test each token to see if it matches any of the query terms. **qor('match1 match2', 2)** gives:

![qor1](http://dclure.org/wp-content/uploads/2012/07/qor-1.png)

As an early experiment, Intra can also do synonym queries, which are based on Wordnet synsets accessed by way of nltk. Synonyms are generated and AND-ed together. For example, the query **qlike('joy', 2)** resolves to **qand('rejoice, joyousness, joyfulness, joy, deilght, gladden, pleasure')**.

So, using this text:

```text
word word gladden joy word word word word rejoice word word word
```

qlike('joy', 2) gives:

![qlike1](http://dclure.org/wp-content/uploads/2012/07/qlike-1.png)

## Usage

In its current form, Intra requires Python 2.6, ipython, pylab, matplotlib, nltk, stemming, and numpy.

Run iPython with Pylab:

```bash
ipython -pylab
```

Import the driver module:

```python
from driver import *
```

Then, register a text. Webpages can be loaded remotely, or text can be pasted directly into the terminal.

```python
# either:
paste('Some text.')
# or remote content (here, Leaves of Grass):
load('http://www.gutenberg.lib.md.us/1/3/2/1322/1322.txt')
```

Then, queries can be executed with qand, qor, and qlike:

```python
qand('i me mine self')
```

![whitman](http://dclure.org/wp-content/uploads/2012/07/whitman.png)

Once the signal renders in the matplotlib window, click anywhere on the graph and Intra will print a short snippet of text centered around the token offset that corresponds to the x-axis position of the click. Zoom and pan with the default matplotlib controls.

## Todo

  * A real query parser, which would eliminate the need for different query functions. Eg, queries like "natasha AND (pierre OR andrei) NOT anatole"

  * A hosted web application that would let users register texts by pasting URLs or raw content, and then execute queries and browse the signals/texts by way of an in-browser JavaScript application.
