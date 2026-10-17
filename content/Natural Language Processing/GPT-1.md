---
title: GPT-1
tags: [nlp, transformers, pretraining, gpt, language-models, auto-captured]
draft: false
---
GPT-1 ("Improving Language Understanding by Generative Pre-Training") showed that a Transformer **decoder** pre-trained as a language model on unlabeled text can be fine-tuned, with minimal changes, to many language understanding tasks. It is a semi-supervised, two-stage recipe: unsupervised pre-training, then supervised fine-tuning.

## Framework

| Stage | Data | Objective |
| ----- | ---- | --------- |
| 1. Unsupervised pre-training | Large unlabeled corpus | Next-token prediction (language modeling) |
| 2. Supervised fine-tuning | Small labeled dataset per task | Task loss plus an auxiliary language-modeling loss |

The Transformer is used because it gives a more structured memory for long-range dependencies than LSTMs, and its parallel training makes large-scale pre-training practical. Earlier pre-training approaches (LSTM-based) were limited to shorter-range prediction.

## Stage 1: Pre-Training (Equations 1 and 2)

**Objective.** For an unlabeled token corpus $U = \{u_1, \ldots, u_n\}$ and context window $k$, maximize the language-modeling likelihood:

$$L_1(U) = \sum_i \log P(u_i \mid u_{i-k}, \ldots, u_{i-1}; \Theta)$$

Each token is a training example, so every position gives a learning signal. This is maximum-likelihood training: pick the parameters $\Theta$ that make the observed text as probable as possible. It is "unsupervised" because the labels are the next tokens already in the text. Maximizing $L_1$ is the same as minimizing the cross-entropy between the true next token and the model's softmax output; perplexity is the exponential of the average negative log-likelihood per token (the paper reports 18.4 on its corpus).

**Model.** A multi-layer Transformer decoder:

$$\begin{aligned} h_0 &= U W_e + W_p \\ h_l &= \text{transformer\_block}(h_{l-1}), \quad l = 1, \ldots, n \\ P(u) &= \text{softmax}(h_n W_e^\top) \end{aligned}$$

- $W_e$ is the token embedding matrix and $W_p$ the **learned** position embedding matrix.
- The output layer reuses $W_e^\top$ (tied weights), so a token's score is the dot product of the final hidden state with that token's embedding.
- Each block is masked multi-head self-attention, then a position-wise feed-forward network, each with a residual connection and layer norm. Compared with the original Transformer decoder, the cross-attention sublayer is removed.

**Why this is not counting.** Counting gives the exact maximum-likelihood solution only for a lookup-table model such as an n-gram model. Here $P$ is the output of a neural network, so $L_1$ is maximized by gradient ascent, and the network generalizes to contexts never seen verbatim.

## Stage 2: Fine-Tuning (Equations 3 to 5)

For a labeled dataset $C$ of inputs $x^1, \ldots, x^m$ with label $y$, the final block's activation at the **last token**, $h_l^m$, feeds a new linear layer $W_y$:

$$\begin{aligned} P(y \mid x^1, \ldots, x^m) &= \text{softmax}(h_l^m W_y) \\ L_2(C) &= \sum_{(x, y)} \log P(y \mid x^1, \ldots, x^m) \\ L_3(C) &= L_2(C) + \lambda \, L_1(C) \end{aligned}$$

- The last token is used because the causal mask means only it has attended to the whole input.
- The auxiliary language-modeling loss $\lambda L_1$ (with $\lambda = 0.5$) improves generalization of the supervised model and accelerates convergence.
- The **only new parameters** are $W_y$ and the embeddings of the start, end, and delimiter tokens. All pre-trained weights are reused and **updated** (they are not frozen).
- One forward pass serves two heads: the language-model head (tied $W_e^\top$, at every position) and the task head ($W_y$, at the last token).

## Task-Specific Input Transformations

Pre-training saw contiguous text, so structured inputs are flattened into one token sequence (a "traversal-style" approach) with randomly initialized start and end tokens and a delimiter `$`. This avoids task-specific architectures that add new parameters receiving no transfer.

| Task | Input sequence | Head |
| ---- | -------------- | ---- |
| Classification | start, text, end | linear + softmax over classes |
| Entailment | start, premise, `$`, hypothesis, end | linear + softmax over classes |
| Similarity (no inherent order) | both orderings of the two sentences, processed independently, final vectors added element-wise | linear |
| Question answering, commonsense | for each candidate answer: start, context, question, `$`, answer, end | score each candidate independently, softmax across candidates |

## Model and Training Details

| Item | Value |
| ---- | ----- |
| Architecture | 12-layer decoder-only Transformer, masked self-attention |
| Hidden size, heads, FFN size | 768, 12, 3072 |
| Activation | GELU |
| Position information | Learned embeddings (not sinusoidal) |
| Context length | 512 tokens |
| Tokenization | Byte-pair encoding, 40,000 merges |
| Pre-training data | BooksCorpus, over 7,000 unpublished books (long contiguous text lets the model learn long-range dependencies) |
| Pre-training | Adam, max learning rate 2.5e-4, 100 epochs, batch 64 of 512-token sequences, dropout 0.1 |
| Fine-tuning | Learning rate 6.25e-5, batch 32, about 3 epochs |

The paper does not state a parameter total; working it out from these specifications gives about 117M.

## Results

State of the art on 9 of the 12 tasks studied, with absolute gains of 8.9% on Story Cloze, 5.7% on RACE, 1.5% on MultiNLI, and 5.5% on GLUE (overall GLUE score 72.8 versus the previous best of 68.9). On CoLA, which tests grammatical acceptability, it scored 45.4 against 35.0, which the authors attribute to linguistic knowledge acquired in pre-training. One weaker result: 56.0% on RTE versus 61.7% for a multi-task BiLSTM.

## Why Pre-Training Helps

The classification head is a single small matrix, so it can only read out information already present in the final vector. Next-token prediction on long text forces the model to learn word meanings, syntax, negation, and tone without labels, so fine-tuning mostly has to learn how to read those features out for the target task.

## Compared with BERT

GPT-1 came a few months before [[BERT]]. Both pre-train and then fine-tune all weights. GPT-1 reads the **last token** of a flat sequence with a delimiter and keeps the language-modeling loss during fine-tuning; BERT reads the `[CLS]` vector (or each token), uses segment embeddings, and has no auxiliary loss. BERT-BASE was sized to match GPT-1 for comparison.

*Source: Radford et al., 2018, [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf). Architecture, equations, hyperparameters, and results were checked against Sections 1 to 4 of the paper. The parameter total and the counting comparison are derived or general knowledge, not stated in the paper.*

## Related Notes
- [[Attention & Transformers]] - The Transformer decoder that GPT-1 builds on.
- [[BERT]] - The bidirectional encoder counterpart.
- [[Large Language Models]] - Later models that scaled this decoder-only recipe.
- [[Language Modeling & N-grams]] - Count-based language models that the neural approach replaces.
