# Intra

Intra experiments with a new way of searching inside of documents - think of it as a souped-up version of Control+F. Instead of chopping texts into short segments and returning ordered subsets of the segments, Intra models relevancy by converting search queries into two-dimensional "signals" - each word in the text is mapped onto an integer on the X axis, and Intra computes a Y-axis value for each word position. In the final presentation of the result, the user can bore down to specific textual passages by zooming in and out and clicking anywhere on the signal graph, which focuses the text to the position that corresponds to the x-axis offset of the click.

For example, searching for `I me mine self` in _Leaves of Grass_ gives results like this:

![whitman](http://dclure.org/wp-content/uploads/2012/07/whitman.png)

This approach has couple of advantages:

  1. First, the concept of a "document" is of limited usefulness when the object of analysis _is itself a document_ (or a comparatively small set of documents - e.g., the collected works of Shakespeare). The problem is that it's impossible to pick a single segment length that's optimal for all queries - relevance doesn't distribute in evenly-sized chunks inside of texts, meaning that there's no single "unit" to return as a result. Trying to pick one will always favor one type of result over another - if you treat a text as a series of sentences, the search results won't represent high-level patterns in meaning distribution at the level of chapters or sections (e.g., war vs. peace in _War and Peace_). But if you index large sub-documents, you iron over important fluctuations at the sentence / phrase level.

  Really, when searching inside of a text, the "document space" is the _set of all continuous series of words, of all lengths_. The most meaningful result for a given query could be a single word, a phrase, a sentence, a paragraph, a chapter, or any combination thereof. By representing relevance as a signal curve instead of a set of sub-documents, Intra can represent meaning-units of any size.

  2. Related, the signal curve captures "positional" information about the distribution of relevance across the length of the text. Instead of getting back a vertical stack of mixed snippets that come from different parts of the text, the signal graph conveys information about not only about what parts of the text are relevant but also how those parts are positioned relative to one another in the text. This is especially useful in cases where the user already has knowledge of the text (e.g., literary analysis) and is trying to confirm, deny, or discover thematic movements or other kinds of _change_ over the course of the text.

  3. Last, Intra's approach to modeling relevancy makes it easy to model compound, "fuzzy" queries on the contents of individual documents. Each signal can be treated as a "layer" of relevance information across the text interval, and the signals can be arithmetically summed as one-dimensional matrices to create synthetic signals that represent complex search queries. This brings the level of sophistication and control that we expect from inter-document searches (Solr, ElasticSearch, etc.) to intra-document searches, which until now have been mostly limited to literal character string matching (Control-F) or stacked-snippets results (like the Google Books search interface, which is the best I've found).

  This also makes it possible to expand the concept of a "query" in interesting ways - in Intra, the query can be any string of text of any size, and the result is effectively a fuzzy substring match between the query and the target document - where the document "sounds like" the query. By using passages or even entire texts as the query, it's possible to automatically search for sections of semantic overlap between texts, to "cross" texts and authors with one another. Where does _Leaves of Grass_ sound like _Hamlet_? Where does Shapespeare sound like the Bible? Where does Hemingway sound like Dostoevsky?

## The query model

Intra models relevancy in an extremely simple way that tries to capture basic intuitions about how how meaning dissipates around a term match. Whenever a term match is found in the text, a gaussian curve that is "emitted" in both directions away from the offset position of the match. The intuition is that terms can be imagined to have a "meaning energy" that is strongest at their actual position in the text. The energy tapers off gradually within the immediate context of the surronding phrase, sentence, paragraph, or section, and then falls of sharpy beyond that. 

![gaussian](http://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Normal_Distribution_PDF.svg/1000px-Normal_Distribution_PDF.svg.png)

When a query is executed, Intra starts by creating a one-dimensional array with a length equal to the wordcount of the text filled with zeros - one zero per word. For each term match in the text, Intra will sum onto the array the values of a gaussian curve centered on the offset position of the term match.

For example, using this text:

```text
word word match1 match1 word word word word match1 match2 word word
```

The signal curve for the query **qand('match1', 2)** with a decay halflife of 2 words looks like this:

![qand1](http://dclure.org/wp-content/uploads/2012/07/qand-1.png)

Since a decay curve is summed onto the array for each term match, term clustering is automatically modeled in the final signal - the curve is higher around offsets 3 and 4 than it is at 8 because the decay curves for the two side-by-side occurrences of "match1" add on top of one another to produce a higher aggregate signal value.

For more than one query term, logical "AND" is modeled by just computing the curves for each of the terms and then summing them to form a composite signal. For example, **qand('match1 match2', 2)** gives this signal:

![qand2](http://dclure.org/wp-content/uploads/2012/07/qand-2.png)

Here, though, you can see that the phrase "match1 match2" produced a higher spike than "match1 match1." This is because Intra scales the center values for the decay curves based on the relative frequency of the terms in the query, the intuition being that infrequent terms should be "higher energy" than frequent terms.

Logical "OR" queries, meanwhile, do not scale the center values and just test each token to see if it matches any of the query terms. **qor('match1 match2', 2)** gives:

![qor1](http://dclure.org/wp-content/uploads/2012/07/qor-1.png)

As an early experiment, Intra can also do synonym queries, which are based on [Wordnet][wordnet] synsets accessed by way of [NLTK][nltk]. Synonyms are generated and AND-ed together. For example, the query **qlike('joy', 2)** resolves to **qand('rejoice, joyousness, joyfulness, joy, deilght, gladden, pleasure')**.

So, using this text:

```text
word word gladden joy word word word word rejoice word word word
```

qlike('joy', 2) gives:

![qlike1](http://dclure.org/wp-content/uploads/2012/07/qlike-1.png)

## Usage

Intra requires Python 2.6, [IPython][ipython], [PyLab][pylab], [matplotlib][matplotlib], [NLTK][nltk], [Stemming][stemming], and [NumPy][numpy]. (The pieces can be assembled using [virtualenv][virtualenv].)

Run iPython with PyLab:

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

## In practice

For example, with the example query above on _Leaves of Grass_, Intra does a good job of finding particularly "self-y" passages. Clicking near the high peak around word 60,000 in the graph above centers exactly on the start of "As I Ebb'd with the Ocean of Life":

```text
-------------------
As I Ebb'd with the Ocean of Life

       1
  As I ebb'd with the ocean of life,
  As I wended the shores I know,
  As I walk'd where the ripples continually wash you Paumanok,
  Where they rustle up hoarse and sibilant,
  Where the fierce old mother endlessly cries for her castaways,
  I musing late in the autumn day, gazing off southward,
  Held by this electric self out of the pride of which I utter poems,
  Was seiz'd by the spirit that trails in the lines underfoot,
  The rim, the sediment that stands for all the water and all the land
      of the globe.

  Fascinated, my eyes reverting from the south, dropt, to follow those
      slender windrows,
  Chaff, straw, splinters of wood, weeds, and the sea-gluten,
  Scum, scales from shining rocks, leaves of salt-lettuce, left by the tide,
  Miles walking, the sound of breaking waves the other side of me,
  Paumanok there and then as I thought the old thought of likenesses,
  These you presented to me you fish-shaped island,
  As I wended the shores I know,
  As I walk'd with that electric self seeking types.

       2
  As I wend to the shores I know not,
  As I list to the dirge, the voices of men and women wreck'd,
  As I inhale the impalpable breezes that set in upon me,
  As the ocean so mysterious rolls toward me closer and closer,
  I too but signify at the utmost a little wash'd-up drift,
  A few sands and dead leaves to gather,
  Gather, and merge myself as part of the sands and drift.

  O baffled, balk'd, bent to the very earth,
  Oppress'd with myself that I have dared to open my mouth,
  Aware now that amid all that blab whose echoes recoil upon me I have
      not once had the least idea who or what I am,
  But that before all my arrogant poems the real Me stands yet
      untouch'd, untold, altogether unreach'd,
  Withdrawn far, mocking me with mock-congratulatory signs and bows,
  With peals of distant ironical laughter a
-------------------
```

The second-highest peak, near word 20,000, is also distinctly me-mine-I-ish:

```text
 The soldier camp'd or upon the march is mine,
  On the night ere the pending battle many seek me, and I do not fail them,
  On that solemn night (it may be their last) those that know me seek me.
  My face rubs to the hunter's face when he lies down alone in his blanket,
  The driver thinking of me does not mind the jolt of his wagon,
  The young mother and old mother comprehend me,
  The girl and the wife rest the needle a moment and forget where they are,
  They and all would resume what I have told them.

       48
  I have said that the soul is not more than the body,
  And I have said that the body is not more than the soul,
  And nothing, not God, is greater to one than one's self is,
  And whoever walks a furlong without sympathy walks to his own
      funeral drest in his shroud,
  And I or you pocketless of a dime may purchase the pick of the earth,
  And to glance with an eye or show a bean in its pod confounds the
      learning of all times,
  And there is no trade or employment but the young man following it
      may become a hero,
  And there is no object so soft but it makes a hub for the wheel'd universe,
  And I say to any man or woman, Let your soul stand cool and composed
      before a million universes.
```

Or, working with _War and Peace_:

```python
load('http://www.gutenberg.lib.md.us/2/6/0/2600/2600.txt')
```

The query **qand('andrew sky')** cleanly picks out a series of much-discussed passages in which Andrei ("andrew" in the query, to conform with the Garnett translation) gazes up into the Russian sky at key moments of spiritual growth:

![andrei](http://dclure.org/wp-content/uploads/2012/07/wp.png)

The two side-by-side high peaks at around word 125,000 give these two paragraphs, which constitute the first (and most significant) occurences of the theme when Andrei is injured at Austerliz:

```text
"What's this? Am I falling? My legs are giving way," thought he, and
fell on his back. He opened his eyes, hoping to see how the struggle of
the Frenchmen with the gunners ended, whether the red-haired gunner had
been killed or not and whether the cannon had been captured or saved.
But he saw nothing. Above him there was now nothing but the sky--the
lofty sky, not clear yet still immeasurably lofty, with gray clouds
gliding slowly across it. "How quiet, peaceful, and solemn; not at all
as I ran," thought Prince Andrew--"not as we ran, shouting and fighting,
not at all as the gunner and the Frenchman with frightened and angry
faces struggled for the mop: how differently do those clouds glide
across that lofty infinite sky! How was it I did not see that lofty sky
before? And how happy I am to have found it at last! Yes! All is vanity,
all falsehood, except that infinite sky. There is nothing, nothing, but
that. But even it does not exist, there is nothing but quiet and peace.
Thank God!..."
```

And:

```text
Prince Andrew understood that this was said of him and that it was
Napoleon who said it. He heard the speaker addressed as Sire. But he
heard the words as he might have heard the buzzing of a fly. Not only
did they not interest him, but he took no notice of them and at once
forgot them. His head was burning, he felt himself bleeding to death,
and he saw above him the remote, lofty, and everlasting sky. He knew it
was Napoleon--his hero--but at that moment Napoleon seemed to him such a
small, insignificant creature compared with what was passing now between
himself and that lofty infinite sky with the clouds flying over it. At
that moment it meant nothing to him who might be standing over him, or
what was said of him; he was only glad that people were standing near
him and only wished that they would help him and bring him back to
life, which seemed to him so beautiful now that he had today learned to
understand it so differently. He collected all his strength, to stir and
utter a sound. He feebly moved his leg and uttered a weak, sickly groan
which aroused his own pity.
```

Meanwhile, the third-highest peak, near word 175,000, is another key occurrence of the trope that directly references the Austerliz scene:

```text
"Yes, if it only were so!" said Prince Andrew. "However, it is time to
get on," he added, and, stepping off the raft, he looked up at the sky
to which Pierre had pointed, and for the first time since Austerlitz saw
that high, everlasting sky he had seen while lying on that battlefield;
and something that had long been slumbering, something that was best
within him, suddenly awoke, joyful and youthful, in his soul. It
vanished as soon as he returned to the customary conditions of his
life, but he knew that this feeling which he did not know how to develop
existed within him. His meeting with Pierre formed an epoch in Prince
Andrew's life. Though outwardly he continued to live in the same old
way, inwardly he began a new life.
```

Generally, it seems that Intra is good at doing "concept" or "theme" searches that layer up a cluster of terms. When I write papers, this is the level of abstraction that I tend to think at.

## Todo

  * A real query parser, which would eliminate the need for different query functions and make it possible to combine different boolean operators. For example, queries like:

    * "natasha AND (pierre OR andrei) NOT anatole"
    * "natasha AND LIKE (joy OR love OR happy OR smile)"
    * "hamlet AND LIKE (divine OR holy OR god)"

  * A hosted, no-registration web application (structurally, like Voyant) that would let users create texts by pasting in a URL or a raw text stream. Users could then execute queries and browse the result signals / texts using an in-browser JavaScript application, perhaps using [Richshaw][rickshaw] for plotting.

[ipython]: http://ipython.org/
[pylab]: http://www.scipy.org/PyLab
[matplotlib]: http://matplotlib.sourceforge.net/
[rickshaw]: http://code.shutterstock.com/rickshaw/examples/
[nltk]: http://nltk.org/
[stemming]: http://pypi.python.org/pypi/stemming/1.0
[numpy]: http://numpy.scipy.org/
[wordnet]: http://wordnet.princeton.edu/
[virtualenv]: http://pypi.python.org/pypi/virtualenv/
