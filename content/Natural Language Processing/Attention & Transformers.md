---
title: Attention & Transformers
tags: [deep-learning, nlp, attention, transformer, bert, seq2seq, self-attention]
draft: false
---
Attention mechanisms solve a core limitation of the encoder-decoder RNN: the entire input sequence is compressed into a fixed-size context vector, which the decoder then uses for all output steps. With attention, the decoder can **selectively focus on different parts of the encoder's output** at each decoding step.

## The Development Arc

The lecture frames the evolution as **4 explicit stages**, each building on the last:

| Stage | Architecture                   | Key idea                                                                   |
| ----- | ------------------------------ | -------------------------------------------------------------------------- |
| 1     | RNN with Attention             | Decoder attends over *all encoder states* instead of just the last one     |
| 2     | RNN with Self-Attention        | Each encoder hidden state attends over *other states in the same sequence* |
| 3     | Attention without RNN          | Cross-attention between encoder and decoder, but no recurrence             |
| 4     | **Self-Attention without RNN** | Every layer is pure self-attention — this is the **Transformer**           |

Each step addresses the limitations of the previous:
- **RNN alone**: sequential computation, can't parallelize, long-term forgetting.
- **RNN + Attention**: decoder learns where to look, but the RNN itself is still sequential.
- **RNN + Self-Attention**: richer encoder representations, but still sequential.
- **Transformer**: fully parallel, no recurrence, attention does everything.

---

## Attention in Seq2Seq (RNN + Attention)

In a standard Seq2Seq model, the decoder only looks at its **current hidden state**. With attention, it additionally consults **all encoder hidden states**, weighted by relevance.

### Complexity

| Model | Parameters per step |
|---|---|
| Without attention | $O(m + t)$ |
| With attention | $O(m \cdot t)$ |

> $m$ = input length, $t$ = output length. Each decoder step computes weights over all $m$ encoder states.

**Key rule:** Do NOT re-use attention weights $\alpha$ computed in a previous decoder step.

### Query, Key, Value Abstraction

| Component | "What it means" | Source |
|---|---|---|
| **Query** | "What am I looking for?" | Decoder hidden state |
| **Key** | "What do I have to offer?" | Each encoder hidden state |
| **Value** | "The actual content I return" | Each encoder hidden state |

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right) V$$

---

## Self-Attention

Self-attention applies the attention mechanism to a **single sequence** — the query, key, and value all come from the same sequence.

**What it enables:**
- Each token can attend to every other token in the same sequence.
- The model builds richer, context-aware representations.
- Less likely to forget earlier parts of the sequence.

**Example:** In *"The FBI is chasing a criminal on the run"*, when encoding "run", self-attention allows the model to attend to "FBI", "chasing", and "criminal".

### Attention vs. Self-Attention

| | Attention (Seq2Seq) | Self-Attention |
|---|---|---|
| Needs decoder? | Yes (two sequences) | No (one sequence) |
| Use case | Machine translation | Any sequence task |
| Scope | Cross-sequence | Within-sequence |

---

## Single-Head Self-Attention

Three learned parameter matrices: $W_Q$, $W_K$, $W_V$.

$$\text{Attn}(Q, K, V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right) V$$

where $Q = X W_Q$, $K = X W_K$, $V = X W_V$.

---

## Multi-Head Self-Attention

Run **$h$ independent single-head self-attention layers in parallel**, each with its own $W_Q^i, W_K^i, W_V^i$. Concatenate all outputs.

- **Total parameter matrices:** $3h$ (Q, K, V per head).
- **Output shape:** if each head outputs a $d \times 1$ vector → multi-head output is $hd \times 1$.
- Different heads can specialize in different types of relationships (syntax, coreference, proximity, etc.).

```python
# Keras MultiHeadAttention layer
mha = keras.layers.MultiHeadAttention(num_heads=8, key_dim=64)
output = mha(query=x, key=x, value=x)  # self-attention: all three are the same x
```

---

## Self-Attention Without RNN (The Bridge to Transformers)

This is the conceptual leap that makes the Transformer feel *inevitable*.

The question to ask: **"If self-attention already lets each token attend to all others in the sequence, why do we need the RNN at all?"**

- The RNN's job was to accumulate context across time steps.
- Self-attention does this *directly* — in a single operation, every token can look at every other token.
- The RNN is now **redundant** as a context aggregator.

**Removing the RNN gives you:**
- Full **parallelism** — no sequential dependency between steps.
- No **vanishing gradient** through time — attention weights are direct connections.
- Unlimited **effective context window** — every token attends to every other token equally.

The only thing lost is the notion of **position** — RNNs inherently encode order by processing left to right. Transformers solve this with **positional encodings** added to the input embeddings, injecting order information back in explicitly.

> **In short:** Self-attention without RNN = Transformer encoder. The Transformer isn't magic — it's what you get when you ask "what if we only use self-attention?"

---

## The Transformer

The Transformer is a **Seq2Seq model built entirely from attention and dense layers** — no recurrence.

### Why Remove the RNN?

- RNNs are **sequential**: $h_3$ cannot be computed before $h_2$ — no parallelism.
- RNNs still suffer from **long-term forgetting** even with attention.
- Attention-only computation is **fully parallelizable**.

### Transformer Encoder

- Stack of **6 identical blocks**.
- Each block: **Multi-Head Self-Attention (8 heads) + Dense Layer** (+ residual connections & layer norm).
- Input shape: $512 \times m$ → Output shape: $512 \times m$ (**shape-preserving** so blocks can be stacked).

### Transformer Decoder

- Stack of **6 identical blocks**.
- Each block has **3 sublayers**:
  1. **Masked Multi-Head Self-Attention** — attends to the decoder's own previous outputs (masked to prevent attending to future tokens).
  2. **Multi-Head Attention** — Keys & Values come from encoder output; Queries come from sublayer 1.
  3. **Dense Layer**.
- Input: $512 \times t$ (decoder) + $512 \times m$ (encoder output) → Output: $512 \times t$.

### Transformer as Machine Translation

1. Encoder processes the full source sentence.
2. Decoder generates the target sentence **one token at a time**.
3. Decoding starts with a `[START]` token, stops at `[STOP]`.
4. Both special tokens are part of the vocabulary and learned during training.

```python
# Minimal Transformer encoder block in Keras
class TransformerEncoderBlock(keras.layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, **kwargs):
        super().__init__(**kwargs)
        self.attn = keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim // num_heads)
        self.ffn = keras.Sequential([
            keras.layers.Dense(ff_dim, activation='relu'),
            keras.layers.Dense(embed_dim),
        ])
        self.norm1 = keras.layers.LayerNormalization()
        self.norm2 = keras.layers.LayerNormalization()

    def call(self, x, training=False):
        attn_out = self.attn(x, x)
        x = self.norm1(x + attn_out)
        ffn_out = self.ffn(x)
        return self.norm2(x + ffn_out)
```

---

## BERT (Bidirectional Encoder Representations from Transformers)

BERT is a method for **pre-training** the Transformer encoder on unlabeled text, producing powerful general-purpose representations that can be fine-tuned for downstream tasks.

- Trained on **English Wikipedia** (~2.5 billion words) + BookCorpus.
- Does **not** require manually labeled data.
- Fully **bidirectional** — attends to left and right context simultaneously.

### Pre-Training Tasks

**Task 1 — Masked Language Modeling (MLM)**
- 15% of tokens are randomly replaced with `[MASK]`.
- The model predicts the original masked words using a **Softmax classifier**.
- Loss: **Cross-Entropy**.

**Task 2 — Next Sentence Prediction (NSP)**
- Input: `[CLS] Sentence A [SEP] Sentence B`.
- Target: `True` (consecutive) or `False` (random pairing).
- 50% real pairs, 50% random pairs.
- A **binary classifier** is applied to the `[CLS]` token output.
- Loss: **Binary Cross-Entropy**.

**Combined Training:**
$$\mathcal{L} = \mathcal{L}_{\text{NSP}} + \mathcal{L}_{\text{MLM}_1} + \mathcal{L}_{\text{MLM}_2} + \ldots$$

Both tasks are trained **simultaneously** in a single gradient descent step.

```python
# Fine-tuning BERT with HuggingFace + Keras
from transformers import TFBertModel, BertTokenizer
import tensorflow as tf

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert = TFBertModel.from_pretrained('bert-base-uncased')

inputs = tokenizer("Hello, my dog is cute", return_tensors="tf")
outputs = bert(**inputs)

# CLS token representation for classification
cls_embedding = outputs.last_hidden_state[:, 0, :]  # shape: (batch, 768)
logits = tf.keras.layers.Dense(2)(cls_embedding)
```

---

## Related Notes
- [[RNNs & LSTMs]] - The sequential architectures that Transformers replace.
- [[Autoencoders]] - Another encoder-decoder architecture (for reconstruction, not generation).
- [[Large Language Models]] - GPT-style models built on the Transformer decoder.
- [[4. RNNs & CNNs for Text Classification]] - NLP grounding for sequence models.
