---
title: GPT-2 and GPT-3
tags: [nlp, llm, pretraining, gpt, scaling, auto-captured]
draft: false
---
GPT-2 and GPT-3 kept the decoder-only Transformer recipe of [[GPT-1]] almost unchanged and changed **scale** and **how the model is used**. GPT-2 moved from fine-tuning to **zero-shot** use, and GPT-3 introduced **few-shot in-context learning** at 175 billion parameters.

## GPT-2: Language Models are Unsupervised Multitask Learners (2019)

**Idea.** A language model trained on a large, diverse corpus learns to perform many tasks without any task-specific training, because the task can be specified in the text itself (for example by appending "TL;DR:" to request a summary). The paper evaluates the models in a **zero-shot** setting, with no parameter or architecture changes for any task.

**Data: WebText.** Text scraped from web pages linked from Reddit posts that received **at least 3 karma**, used as a heuristic for human-curated quality. After cleaning, it contains slightly over 8 million documents totaling 40 GB of text, with all Wikipedia documents removed.

**Tokenization.** Byte-level byte-pair encoding. A byte-level base vocabulary needs only 256 symbols, and the final vocabulary is expanded to **50,257** tokens.

**Model sizes.**

| Parameters | Layers | $d_{model}$ |
| ---------- | ------ | ----------- |
| 117M | 12 | 768 |
| 345M | 24 | 1024 |
| 762M | 36 | 1280 |
| 1542M (the "1.5B" model) | 48 | 1600 |

**Changes from GPT-1.** The context grows from 512 to **1,024** tokens; layer normalization is moved to the input of each sublayer, with an additional layer normalization after the final self-attention block; residual weights are scaled at initialization by $1/\sqrt{N}$ for $N$ residual layers.

**Staged release.** OpenAI released the models in stages because of concerns about misuse: the 124M model in February 2019, then 355M, 774M in August 2019, and the full 1.5B model in November 2019. (The paper lists the smallest model as 117M; the released one is commonly named 124M.)

## GPT-3: Language Models are Few-Shot Learners (2020)

**Idea.** Scaling up an autoregressive language model to 175 billion parameters makes it a strong **in-context learner**: it performs a new task from instructions and examples in its prompt, with **no gradient updates**. The paper contrasts three settings with traditional fine-tuning:

| Setting | What the prompt contains |
| ------- | ------------------------ |
| Zero-shot | A natural-language task description only |
| One-shot | The description plus one demonstration |
| Few-shot | The description plus as many demonstrations as fit in the context window (typically 10 to 100) |

**Largest model.** 175 billion parameters, 96 layers, $d_{model}$ = 12,288, 96 attention heads of dimension 128, a context window of **2,048** tokens, and a feed-forward size of four times $d_{model}$. All models were trained for **300 billion tokens**. The paper trained eight sizes, from 125 million to 175 billion parameters, to study how performance scales with size.

**Architecture.** The same model as GPT-2 (modified initialization, pre-normalization, reversible tokenization), except that the layers alternate **dense and locally banded sparse attention** patterns, similar to the Sparse Transformer.

**Training data.** A weighted mix of filtered Common Crawl (60% of training samples), WebText2 (22%), two book corpora (8% each), and English Wikipedia (3%). Higher-quality sources are sampled more than once, and Common Crawl is sampled less than once.

## Progression

| | [[GPT-1]] | GPT-2 | GPT-3 |
| - | --------- | ----- | ----- |
| Parameters | About 117M (derived; not stated in the paper) | 1.5B (largest) | 175B |
| Context | 512 | 1,024 | 2,048 |
| Data | BooksCorpus (about 0.8B words) | WebText (40 GB, 8M documents) | About 300B training tokens |
| Adaptation | Fine-tune per task | Zero-shot | Few-shot (in-context) |

The architecture barely changed across the three; scale and the way the model is used did.

## What Came Next

GPT-3 followed instructions unreliably, which led to instruction tuning and reinforcement learning from human feedback ([[Reinforcement Learning from Human Feedback]]). Modern LLMs still start from self-supervised pre-training with next-token prediction, then add post-training stages. See [[Large Language Models]] and [[Evolution of Text Generation Models]].

*Sources: [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) (Radford et al., 2019) and [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) (Brown et al., 2020). Model sizes, dataset descriptions, and architecture changes were checked against the text of both papers; the staged-release dates come from [OpenAI's release pages](https://openai.com/index/gpt-2-6-month-follow-up/), and the 355M model's release month is reported inconsistently (April or May 2019). The closing paragraph is general knowledge, not from these papers.*

## Related Notes
- [[GPT-1]] - The pre-train and fine-tune recipe that GPT-2 and GPT-3 scale.
- [[BERT]] - The bidirectional encoder counterpart.
- [[Attention & Transformers]] - The architecture underneath.
- [[Large Language Models]] - Scale, training, and limitations of modern LLMs.
