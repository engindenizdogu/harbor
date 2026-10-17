---
title: BERT
tags: [nlp, transformers, pretraining, bert, language-models, auto-captured]
draft: false
---
BERT (Bidirectional Encoder Representations from Transformers) pre-trains a deep, bidirectional Transformer **encoder** on unlabeled text, then fine-tunes the whole model on each downstream task with just one added output layer. Every layer conditions on left and right context at once, which earlier pre-trained models did not do.

## Why Bidirectional

A word's meaning often depends on the context after it as well as before it. In "The bank approved my loan", a left-to-right model has seen only "The" when it builds the representation of "bank". The BERT paper argues that one-directional restrictions are sub-optimal for sentence-level tasks and harmful for token-level tasks such as question answering, where context from both directions is crucial.

| Model | Directionality |
| ----- | -------------- |
| OpenAI GPT | Left-to-right only: each token attends only to earlier tokens |
| ELMo | Two independently trained LSTMs (left-to-right and right-to-left) whose outputs are concatenated, so only **shallowly** bidirectional |
| BERT | Jointly conditions on both sides in **all layers** (deeply bidirectional) |

## Architecture

BERT is a multi-layer bidirectional Transformer **encoder**, almost identical to the original implementation described in [[Attention & Transformers]]. There is no decoder and no cross-attention, and the self-attention is unmasked.

| Model | Layers $L$ | Hidden size $H$ | Heads $A$ | Parameters |
| ----- | ---------- | --------------- | --------- | ---------- |
| BERT-BASE | 12 | 768 | 12 | 110M |
| BERT-LARGE | 24 | 1024 | 16 | 340M |

The feed-forward size is $4H$ (3072 and 4096). BERT-BASE was sized to match OpenAI GPT ([[GPT-1]]) for a fair comparison; the critical difference is that BERT's self-attention is bidirectional while GPT's is restricted to the left.

**Why only an encoder?** A decoder's causal mask exists so text can be generated one token at a time, and its cross-attention exists to read a separate source sequence. BERT needs neither. Its training task (masked language modeling) needs both sides of the context, and its outputs are one vector per input token that a small head turns into a label, tag, or answer span. The cost is that BERT cannot generate text naturally.

## Input Representation

One token sequence can hold a single sentence or a sentence pair:

```
[CLS] my dog is cute [SEP] he likes play ##ing [SEP]
```

- **WordPiece** tokenization with a 30,000-token vocabulary (rare words split into pieces, as in "play ##ing"). See [[Tokenization]].
- **`[CLS]`** is the first token of every sequence. Its final hidden state is the aggregate representation used for classification and for next sentence prediction.
- **`[SEP]`** separates the two sentences and ends each one.
- **`[MASK]`** replaces tokens selected for masked language modeling (pre-training only).
- A token's input is the **sum of three embeddings**: the token embedding, a **segment** embedding (sentence A or B), and a **position** embedding.

The appendix says the last 10% of pre-training steps use sequences of length 512 "to learn the positional embeddings", so BERT's position embeddings are learned parameters (maximum length 512), not the fixed sinusoids of the original Transformer. The paper does not state this explicitly in the main text; it is inferred from the appendix.

## Pre-Training Task 1: Masked Language Modeling

A standard language model can only be trained left-to-right or right-to-left, because with both-sided context in a multi-layer model each word could indirectly "see itself" and the prediction becomes trivial. BERT instead hides tokens and predicts them from both sides (a Cloze task).

1. Select **15%** of all WordPiece tokens in each sequence at random.
2. Replace each selected token as follows:

| Replacement | Probability | Example (the 4th token of "my dog is hairy" is chosen) |
| ----------- | ----------- | ------------------------------------------------------ |
| `[MASK]` token | 80% | my dog is [MASK] |
| Random word | 10% | my dog is apple |
| Unchanged | 10% | my dog is hairy |

3. The final hidden vector at each selected position goes through a softmax over the vocabulary and is trained with **cross-entropy** against the original token.
4. The loss is computed **only at the selected positions**. The other 85% of tokens are visible context with no prediction target.

**The mismatch.** `[MASK]` appears in pre-training but never at fine-tuning time. Using random or unchanged tokens for 20% of the selected positions means the model cannot tell which tokens it must predict or which were replaced, so it must keep a good contextual representation of every input token. Random replacement affects only 10% of 15% = 1.5% of tokens, which does not seem to harm language understanding.

**Cost.** Because only about 15% of positions give a prediction per sequence, masked LM may need more pre-training steps than a left-to-right model, which predicts at every position.

## Pre-Training Task 2: Next Sentence Prediction

Tasks such as question answering and natural language inference depend on the relationship between two sentences, which language modeling does not directly capture. For each example, 50% of the time sentence B really follows A (label `IsNext`) and 50% of the time it is a random sentence from the corpus (`NotNext`). The `[CLS]` vector predicts the label; the final model reaches 97 to 98% accuracy on this task. Unlike earlier work that transferred only sentence embeddings, BERT transfers all parameters. The `[CLS]` vector is not a meaningful sentence representation without fine-tuning, since it was trained only for this task.

**Total pre-training loss** is the sum of the mean masked-LM likelihood and the mean NSP likelihood:

```
L_pretrain = L_MLM + L_NSP
```

## Pre-Training Data and Scale

- **Data:** BooksCorpus (800M words) and English Wikipedia (2,500M words, text passages only). A **document-level** corpus is critical, because a shuffled sentence-level corpus would not provide long contiguous sequences.
- **Procedure:** batches of 256 sequences of up to 512 tokens, 1,000,000 steps (about 40 epochs over the 3.3 billion words), Adam with learning rate 1e-4, dropout 0.1, GELU activation. Sequence length 128 for 90% of the steps, then 512 for the final 10%, because attention cost grows with the square of the length.
- **Compute:** about 4 days on 4 Cloud TPUs (16 chips) for BERT-BASE and on 16 Cloud TPUs (64 chips) for BERT-LARGE.

## Fine-Tuning

Plug the task's inputs and outputs into BERT and fine-tune **all** parameters end to end. Fine-tuning is relatively cheap: the paper's results can be replicated in at most about an hour on a single Cloud TPU, or a few hours on a GPU. Each task gets its own fine-tuned model, all initialized from the same pre-trained weights.

| Task type | Input | Output used | Loss |
| --------- | ----- | ----------- | ---- |
| Classification (sentiment) | `[CLS] text [SEP]` | `[CLS]` vector | standard classification loss, $\log \text{softmax}(C W^\top)$ |
| Sentence-pair (entailment, paraphrase) | `[CLS] A [SEP] B [SEP]` | `[CLS]` vector | same |
| Question answering | `[CLS] question [SEP] passage [SEP]` | each passage token's vector, scored against a start vector and an end vector | sum of log-likelihoods of the correct start and end positions |
| Sequence tagging (NER) | `[CLS] text [SEP]` | each token's vector | per-token classification |

Encoding a concatenated pair with self-attention effectively includes bidirectional cross attention between the two sentences, which unifies the two stages (encode separately, then cross-attend) used by earlier approaches.

## Results

New state of the art on eleven NLP tasks at release: GLUE score 80.5% (7.7 points absolute improvement), MultiNLI accuracy 86.7% (4.6), SQuAD v1.1 test F1 93.2 (1.5), and SQuAD v2.0 test F1 83.1 (5.1).

## BERT vs. GPT-Style Pre-Training

| | BERT | GPT-style |
| - | ---- | --------- |
| Architecture | Encoder | Decoder |
| Attention | Bidirectional | Causal mask |
| Objective | Masked LM (plus NSP) | Next-token prediction |
| Predictions per sequence | About 15% of positions | Every position |
| Train/use match | Mismatch (`[MASK]`) | Match |
| Generates text | Not naturally | Natively |
| Typical uses | Classification, tagging, QA, embeddings, ranking | Generation, dialogue, in-context learning |

Decoder-style models became the basis of modern [[Large Language Models]] because every token is a training signal, generation is the training task, and one prompted model can serve many tasks. Encoders remain common for embeddings, retrieval, and cheap high-volume classification.

*Source: [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805) (Devlin et al., 2018). The architecture, objectives, data, and results were checked against Sections 1 to 4 and Appendix A of the paper. The comparison with GPT-style models is general knowledge, not from the paper.*

## Related Notes
- [[Attention & Transformers]] - The Transformer encoder that BERT stacks.
- [[GPT-1]] - The left-to-right pre-train and fine-tune counterpart.
- [[Tokenization]] - WordPiece and other subword schemes.
- [[Large Language Models]] - Decoder-style models built on the same architecture.
