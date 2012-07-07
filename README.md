# Intra

Intra is a prototype application that experiments with a new approach to searching inside of long texts. Instead of trying to imitate the structure of (inter-)document-based approaches by chopping long texts into short segments and then returning subsets of the segments, Intra models relevancy by converting search queries into two-dimensional "signals" - each word in the text is mapped onto an integer on the X axis, and Intra computes a y-axis value for each word position.

This approach has three advantages:

  1. First, it makes it possible for the user to immediately intuit the structure of the query result. Instead of having to make substantive (and usually opaque) decisions behind the scenes about what portions of the text get returned and in what order, the signal data can be presented almost completely unmodified, allowing the user to bore down into the source text by interacting directly with the signal graph.

  2. Related to #1, the signal graph automatically conveys "positional" information about the distribution of query relevance across the duration of the text. Instead of getting back a vertical stack of intermixed snippets that come from different parts of the text, the signal graph immediately conveys information about not only about what parts of the text are relevant but also how those parts are relatively positioned in the text. This is especially useful in cases where the user already has knowledge of the text (eg, literary analysis) and is trying to confirm, deny, or discover thematic movements or other kinds of _change_ over the course of the text.

  3. Finally, Intra's approach to modeling relevancy makes it extremely simple to extrapolate upwards into compound or boolean queries (AND, OR, NOT, LIKE) without having to use complex clustering alrogithms (and again, without having to make concealed decisions for the user). Each signal can be treated as a "layer" of relevance information across the text interval, and the signals can be arithmetically summed as one-dimensional matrices to create synthetic signals that represent complex search queries. In essence, this brings the level of sophistication and control that we expect from inter-document searches (Google, Solr, etc.) to _intra_-document searches, which until now have been limited to literal character string matching (control-f).

## The query model

Intra models relevancy in an extremely simple way that tries to capture basic intuitions about how how meaning dissipates around a term match. Whenever a term match is found in the text, a gaussian curve that is "emitted" in both directions away from the offset position of the match. The intuition is that terms can be imagined to have a "meaning energy" that is strongest at their actual position of the text, which then tapers off gradually within the immediate context of the surronding phrase, sentence, paragraph, or section and then falls of sharpy beyond that. 

When a query is executed, Intra starts by creating a one-dimensional array with a length equal to the wordcount of the text filled with zeros - one zero per word. For each term match in the text, Intra will sum onto the array the values of a gaussian curve centered on the offset position of the term match.

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

## Does it work?

Anecdotally, it appears to. For example, with the example query above on _Leaves of Grass_, Intra appears to do a good job of finding particularly "self-y" passages. Clicking near the high peak around word 60,000 in the graph above gives this passage:

```text
-------------------
de,)
  The sea whisper'd me.




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

Likewise, Intra seems to be able to clearly resolve thematically important locations in texts. Working with _War and Peace_:

```python
load('http://www.gutenberg.lib.md.us/2/6/0/2600/2600.txt')
```

The query **qand('andrew sky')** cleanly picks out a series of oft-discussed passages in which Andrei ("andrew" in the query, to conform with the Garnett translation) gazes up into the Russian sky at key moments of spiritual growth:

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



## Todo

  * A real query parser, which would eliminate the need for different query functions and make it possible to combine different boolean operators. For example, queries like:

    * "natasha AND (pierre OR andrei) NOT anatole"
    * "natasha AND LIKE (joy OR love OR happy OR smile)"
    * "andrei AND sky AND battle)"

  * A hosted web application that would let users register texts by pasting URLs or raw content, and then execute queries and browse the signals/texts by way of an in-browser JavaScript application.
