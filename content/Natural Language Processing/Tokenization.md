---
title: Tokenization
tags: [nlp, machine-learning, text, auto-captured]
draft: false
---
#### Tokenization Strategies
- **Character Tokenization:** The simplest tokenization scheme is to feed each character individually to the model.
	- Ignores any structure in the text and treats the whole string as a stream of characters.
	- Helps deal with misspellings and rare words.
	- But the main drawback is that linguistic structures such as words need to be learned from the data. This requires significant compute, memory, and data.
- **Word Tokenization:** Split into words and map each word to an integer.
	- One simple way to do it splitting sentences by whitespace.
	- Given that words can include declinations, conjugations, or misspellings, the size of the vocabulary can easily grow into the millions! Which results in models with lots of parameters (expensive to train).
	- A common approach is to limit the vocabulary and discard rare words by considering, say, the 100,000 most common words in the corpus. Assign rare or unknown words to `<UNK>` tokens.
- **Subword Tokenization:** combine the best aspects of character and word tokenization.
	- Idea: We want to split rare words into smaller units to allow the model to deal with complex words and misspellings.
	- We want to keep frequent words as unique entities so that we can keep the length of our inputs to a manageable size.
	- Advantage when it comes to unknown words: Instead of mapping a new word like "unhappily" to a single `<UNK>` token because it wasn't in the training set, the model can decompose it into `un-`, `happi`, and `-ly`. This means the model can still assign a meaningful probability to the sequence because it knows the meaning and behavior of those individual sub-units. This effectively creates a **fixed-size vocabulary** that can still represent an **infinite number of words**.

### Byte Pair Encoding (BPE)

BPE (Sennrich et al., 2016, adapted from a data-compression algorithm) builds a subword vocabulary by repeatedly **merging the most frequent adjacent pair** of symbols.

**Training**
1. Split every word into characters and add an end-of-word marker `_`. Keep the word counts.
2. Count every adjacent symbol pair, weighted by word frequency.
3. Merge the most frequent pair into one new symbol and record the merge rule. Ties can be broken arbitrarily.
4. Repeat until the vocabulary reaches the target size (base characters plus the number of merges).

**Worked example.** Corpus: `low` x5, `lower` x2, `newest` x6, `widest` x3. The merges, in order:

| Step | Merge | Pair count |
| ---- | ----- | ---------- |
| 1 | `e` + `s` | 9 |
| 2 | `es` + `t` | 9 |
| 3 | `est` + `_` | 9 |
| 4 | `l` + `o` | 7 |
| 5 | `lo` + `w` | 7 |
| 6 | `n` + `e` | 6 |
| 7 | `ne` + `w` | 6 |
| 8 | `new` + `est_` | 6 |

(Steps 1 to 3 tie on count 9, and ties here were broken by first occurrence.)

**Encoding a new word.** Split it into characters and apply the learned merges **in the order they were learned**. The unseen word `lowest` becomes `low` + `est_`, and `newer` becomes `new` + `e` + `r` + `_`, so a word never seen in training is still represented by known pieces.

```python
from collections import Counter

def pair_counts(words):                       # words: {tuple_of_symbols: count}
    pairs = Counter()
    for symbols, count in words.items():
        for a, b in zip(symbols, symbols[1:]):
            pairs[(a, b)] += count
    return pairs

def merge_pair(words, pair):
    merged = {}
    for symbols, count in words.items():
        out, i = [], 0
        while i < len(symbols):
            if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == pair:
                out.append(symbols[i] + symbols[i + 1]); i += 2
            else:
                out.append(symbols[i]); i += 1
        merged[tuple(out)] = count
    return merged

corpus = {"low": 5, "lower": 2, "newest": 6, "widest": 3}
words = {tuple(w) + ("_",): c for w, c in corpus.items()}
for _ in range(8):                            # 8 merges
    best = pair_counts(words).most_common(1)[0][0]
    words = merge_pair(words, best)
```

**Notes**
- **Byte-level BPE** starts from the 256 possible bytes instead of characters, so every string can be encoded and no `<unk>` token is needed. GPT-2 uses it, with a vocabulary of 50,257 (256 byte tokens, 50,000 merges and one end-of-text token).
- **Vocabulary size** is a hyperparameter. The original GPT used 40,478 (478 base tokens plus 40,000 merges), and modern models use roughly 30,000 to over 100,000.
- **Pre-tokenization** (splitting on whitespace or punctuation first) stops merges from crossing word boundaries.
- The pieces are driven by **frequency**, so they are not always meaningful morphemes.

### Other Subword Methods

| Method | How the vocabulary is built | Used by |
| ------ | --------------------------- | ------- |
| **BPE** | Merge the most frequent pair | GPT family, Llama |
| **WordPiece** | Merge the pair with the best score $\dfrac{\text{freq}(ab)}{\text{freq}(a)\,\text{freq}(b)}$, favouring pairs that occur together more than chance | BERT ([[BERT]]) |
| **Unigram** | Start with a large vocabulary and **prune** the tokens whose removal hurts the likelihood least. Probabilistic, so it can sample different tokenizations | T5 |
| **SentencePiece** | A library that applies BPE or Unigram to the raw character stream, treating the space as a symbol (`▁`), so it works for languages written without spaces | T5, many multilingual models |

### Resources

- [Hugging Face Tokenizer Summary](https://huggingface.co/docs/transformers/tokenizer_summary) — A comprehensive summary explaining standard subword tokenization algorithms (BPE, WordPiece, and Unigram). Source for the vocabulary sizes and the WordPiece and Unigram descriptions above.
- [Neural Machine Translation of Rare Words with Subword Units (Sennrich et al., 2016)](https://arxiv.org/abs/1508.07909) — The paper that introduced BPE for neural models.

Related: [[Natural Language Processing MOC]], [[Word2Vec]], [[Large Language Models]]

