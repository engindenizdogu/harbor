---
title: Part-of-Speech Tagging
tags: [nlp, pos-tagging, sequence-labeling, hmm, auto-captured]
draft: false
---
**Part-of-speech (POS) tagging** labels every word in a sentence with its grammatical category: noun, verb, adjective, preposition and so on. It is one of the oldest NLP tasks and a classic example of **sequence labeling**, where each input token gets one output label.

Example with Penn Treebank tags:

| The | quick | brown | fox | jumps | over | the | lazy | dog |
| --- | ----- | ----- | --- | ----- | ---- | --- | ---- | --- |
| DT | JJ | JJ | NN | VBZ | IN | DT | JJ | NN |

## Tag Sets

| Tag set | Size | Notes |
| ------- | ---- | ----- |
| **Universal Dependencies (UPOS)** | 17 coarse tags | Shared across languages |
| **Penn Treebank** | about 45 tags | English only, with fine distinctions such as `VBZ` (verb, 3rd person singular present) vs. `VBD` (past tense) |

The 17 universal tags are, by class:

| Class | Tags |
| ----- | ---- |
| Open class | ADJ, ADV, INTJ, NOUN, PROPN, VERB |
| Closed class | ADP, AUX, CCONJ, DET, NUM, PART, PRON, SCONJ |
| Other | PUNCT, SYM, X |

Open classes accept new words all the time (new nouns and verbs appear constantly). Closed classes are small fixed sets of function words.

## Why It Is Hard: Ambiguity

The same word can have different tags depending on context:

- "Time **flies** like an arrow": *flies* is a verb. "Fruit **flies** like a banana": *flies* is a noun.
- "I **book** a flight" (verb) vs. "I read a **book**" (noun).

A tagger must therefore use the **surrounding words**, not just a dictionary lookup.

**Baselines and accuracy.** Tagging each word with its most frequent tag in the training data already reaches roughly **90%** on English (the figure depends strongly on how unknown words are handled), while modern taggers reach about **97%**, near the level of agreement between human annotators.

## Methods

| Era | Method | Idea |
| --- | ------ | ---- |
| Early | **Rule-based** | Hand-written rules narrow each word's possible tags |
| Statistical | **Hidden Markov model (HMM)** | Probabilistic model of tag sequences, decoded with Viterbi |
| Feature-based | **MEMM, CRF** | Discriminative models using word suffix, capitalization and neighbouring words as features |
| Neural | **BiLSTM, fine-tuned Transformer** | Contextual representations from the whole sentence ([[RNNs & LSTMs]], [[BERT]]) |

### The HMM tagger

An HMM picks the tag sequence $t_1 \dots t_n$ that maximizes the product of **transition** and **emission** probabilities:

$$\hat{t}_{1:n} = \arg\max_{t_{1:n}} \prod_{i=1}^{n} \underbrace{P(w_i \mid t_i)}_{\text{emission}}\ \underbrace{P(t_i \mid t_{i-1})}_{\text{transition}}$$

- **Transition:** how likely a tag is after the previous tag (a determiner is usually followed by a noun or adjective).
- **Emission:** how likely a tag is to produce the word ("book" is likely as a noun, less so as a verb).

There are exponentially many tag sequences, so the **Viterbi algorithm** finds the best one with dynamic programming in $O(n\,T^2)$ time for $T$ tags. It keeps, for every position and tag, the best score of any path ending there, and backtracks at the end. The transition term is the same bigram idea as in [[Language Modeling & N-grams]].

## Where It Is Used

- **Features for other tasks:** syntactic parsing, named entity recognition and information extraction.
- **Lemmatization:** the lemma of "saw" depends on the tag (noun "saw" stays *saw*, verb "saw" becomes *see*).
- **Keyword extraction:** candidate phrases are often noun phrases found from tag patterns ([[Keyword Extraction & Topic Modelling]]).

## In Code

```python
import spacy
nlp = spacy.load("en_core_web_sm")
for token in nlp("The quick brown fox jumps over the lazy dog"):
    print(token.text, token.pos_, token.tag_)      # universal tag, Penn Treebank tag
```

```python
import nltk
nltk.pos_tag(nltk.word_tokenize("The quick brown fox jumps over the lazy dog"))   # Penn Treebank tags
```

*Sources: [Universal Dependencies, UPOS tag set](https://universaldependencies.org/u/pos/) (the 17 tags; the class grouping is the same page). The accuracy figures come from university NLP lecture slides, for example [Cornell CS 6741](https://www.cs.cornell.edu/courses/cs6741/2015fa/lectures/02-pos.pdf) and [CMSC 470](https://home.cs.colorado.edu/~jbg/teaching/CMSC_470/10a_hmm.pdf); I could not open Jurafsky and Martin's textbook chapter to confirm its exact numbers. The Penn Treebank tag count and the HMM and Viterbi description are standard background from my own knowledge.*

---
*Related:* [[Natural Language Processing MOC]], [[What is NLP?]], [[Language Modeling & N-grams]], [[BERT]]
