---
title: Natural Language Processing Coursework CS584
tags:
  - projects
  - nlp
  - python
draft: false
---
> A portfolio of assignments covering the modern NLP stack, from classical text classification to causal language model internals and LLM agents.

## Quick Facts
- **Context:** CS584 Natural Language Processing Coursework (Spring 2026)
- **Tech Stack:** Python, PyTorch, HuggingFace Transformers, scikit-learn, OpenAI API, Optuna
- **Links:** None available

## Overview and Problem
This repository contains four major projects exploring the evolution of NLP. The work transitions from TF-IDF baselines to dense word embeddings, and culminates in implementing from-scratch decoding algorithms and multi-turn LLM agents.

## What I Built
- **Developed** baseline sentiment classifiers using TF-IDF with scikit-learn and PyTorch MLPs, optimized via Optuna.
- **Implemented** nearest-neighbor search, word analogy tasks, and CNN-based sentiment classifiers using pre-trained GloVe and Cohere embeddings.
- **Engineered** greedy decoding and beam search algorithms from scratch for the Llama-3.2-1B model.
- **Designed** a multi-turn LLM-powered conversational agent from scratch with persistent memory, branching capabilities, and custom tool-use (regex-based calculator interception).

## Key Results and Impact
- Replicated WEAT bias statistics to quantify gendered associations in GloVe embeddings.
- Boosted sentiment classification validation accuracy from ~60% (TF-IDF) to ~91.6% using Cohere embeddings and 1D Convolutions.
- Successfully visualized the divergence between greedy and beam-search paths during causal language model generation.
- Demonstrated reliable tool invocation by prompting the custom agent to intercept and compute arithmetic expressions before generating final responses.

---
*Related:* [[Projects MOC]]
