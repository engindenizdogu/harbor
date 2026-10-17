---
title: Natural Language Processing MOC
tags: [nlp, moc]
draft: false
---
Map of Contents. Learning path from classical text processing to Transformers and LLMs. Neural network basics live in [[Machine Learning MOC]]; agent systems built on LLMs live in [[Agents MOC]].

## Foundations
- [[Glossary (NLP)]] - Key NLP terms and definitions.
- [[What is NLP?]] - NLP is a field of linguistics and machine learning focused on understanding human language.
- [[Language Modeling & N-grams]] - Predicting the next word; statistical language models.
- [[Tokenization]] - Character, word, and subword tokenization schemes.

## Representations
- [[Word Vectors]] - Knowledge-based vs. distributional word representations.
- [[Word2Vec]] - CBOW and Skip-gram, negative sampling, subsampling, analogies, and limitations.
- [[Building Embedding Models From Scratch]] - Word2Vec, autoencoder bottleneck, and Siamese networks, with a PyTorch Skip-Gram snippet.
- [[Keyword Extraction & Topic Modelling]] - TF, TF-IDF, RAKE, and topic models.

## Neural Sequence Models
- [[RNNs & CNNs for Text Classification]] - Improvements over n-grams and remaining limitations.
- [[RNNs & LSTMs]] - RNN/LSTM architecture, parameter counting, text generation, and Seq2Seq machine translation.
- [[Attention & Transformers]] - Self-attention, multi-head attention, the Transformer encoder/decoder, the paper-to-code walkthrough, and BERT pre-training.
- [[Transformer Snippets]] - PyTorch building blocks of the original Transformer (attention, masks, positional encoding, training recipe).
- [[GPT-1]] - Generative pre-training of a Transformer decoder, then fine-tuning with task-specific input transformations.
- [[BERT]] - Bidirectional encoder pre-training with masked language modeling and next sentence prediction.
- [[Transformer, GPT and BERT Q&A]] - Question-and-answer study guide with worked examples for the three papers.

## Large Language Models
- [[Large Language Models]] - Characteristics, scale, and training of LLMs.
- [[GPT-2 and GPT-3]] - Zero-shot and few-shot in-context learning, and how scale changed the GPT recipe.
- [[Evolution of Text Generation Models]] - Timeline from rule-based systems to large pre-trained Transformers.
- [[KV Cache]] - Storing Key and Value vectors of previous tokens to speed up generation.
- [[LM Benchmarks]] - Coding, reasoning, and general benchmarks for language models.

---
## To Research / Inbox
