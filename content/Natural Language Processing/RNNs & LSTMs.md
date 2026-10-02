---
title: RNNs & LSTMs
tags: [deep-learning, rnn, lstm, nlp, sequence-modeling, text-generation, machine-translation]
draft: false
---
Recurrent Neural Networks (RNNs) and Long Short-Term Memory networks (LSTMs) are the core architectures for modeling **sequential data** — text, speech, and time series. Unlike fully-connected or convolutional networks, they process input step-by-step and maintain hidden state across time steps.

## Why Not FC or ConvNets for Sequences?

- **FC Nets / ConvNets** process a paragraph as a whole, require fixed-size input and produce fixed-size output — they cannot naturally handle variable-length sequences.
- **RNNs** handle variable-length sequences, share weights across time steps, and maintain state.

---

## Text Preprocessing Pipeline

Before feeding text into an RNN, raw text is transformed:

**Tokenization → Encoding → Alignment**

1. **Tokenization** (word-level): split text into tokens, build a frequency-sorted vocabulary.
2. **Encoding**: map tokens to integer indices. Infrequent words/tokens are dropped:
   - *Computational cost*: a bigger vocabulary → higher-dimensional one-hot vectors.
   - *Low information value*: typos and rare named entities contribute noise.
3. **One-Hot Encoding** (char-level) or **Embeddings** (word-level): word-level requires embeddings because the vocabulary is too large for one-hot.
4. **Alignment**: pad/truncate sequences to the same length.

---

## Simple RNN

The recurrence relation at each time step:

$$h_t = \tanh(A \cdot [h_{t-1},\, x_t] + b)$$

- $h_t$: hidden state at step $t$
- $x_t$: **embedding vector** at step $t$ (not the one-hot vector — the output of the embedding layer)
- $A$: shared weight matrix
- `tanh` keeps values bounded in $(-1, 1)$, preventing exploding activations.

### Parameter Count

$$\text{Params} = \dim(h) \times (\dim(h) + \dim(x)) + \dim(h)$$

> **Important:** $\dim(x)$ is the embedding dimension (e.g., 32), **not** the vocabulary size.

### `return_sequences`

| `return_sequences` | Output shape | Effect on Dense layer |
|---|---|---|
| `False` (default) | Last $h_T$ only | Dense sees a single vector |
| `True` | All $h_1, \ldots, h_T$ | Dense applied at each step — only the Dense layer's param count changes |

```python
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Embedding(input_dim=vocab_size, output_dim=32),
    keras.layers.SimpleRNN(64, return_sequences=False),
    keras.layers.Dense(10, activation='softmax')
])
model.summary()
```

### Shortcomings

- **Vanishing gradient / long-term dependency problem**: gradients decay over long sequences, so early tokens are effectively forgotten.

### Chaos and Stability
In the language of dynamical systems, the training of RNNs is a balance between **stability** and **chaos**:
*   **Vanishing Gradients:** Represent a "stable" but "damped" system. The influence of the initial state $h_0$ decays exponentially.
*   **Exploding Gradients:** Represent a **chaotic** system. Small changes in the initial state or parameters lead to massive, unpredictable changes in the output (the **Butterfly Effect**).
*   **Edge of Chaos:** Researchers have found that RNNs perform best when initialized at the "edge of chaos"—a regime where the system is sensitive enough to remember the past but stable enough to not let noise explode.

> [!TIP]
> For more on the math behind this, see [[7. Chaos Theory]].

---

## LSTM (Long Short-Term Memory)

LSTM introduces a **cell state** $C_t$ (the "conveyor belt") and three **gates** to selectively retain or discard information.

### Gates

| Gate | Formula | Role |
|---|---|---|
| Forget gate | $f_t = \sigma(W_f \cdot [h_{t-1}, x_t])$ | How much of $C_{t-1}$ to keep (0 = forget, 1 = keep) |
| Input gate | $i_t = \sigma(W_i \cdot [h_{t-1}, x_t])$ | How much of the new candidate to write |
| Candidate | $\tilde{C}_t = \tanh(W_C \cdot [h_{t-1}, x_t])$ | The actual candidate content to add |
| Cell update | $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$ | Updated cell state |
| Output gate | $o_t = \sigma(W_o \cdot [h_{t-1}, x_t])$ | How much of cell state to expose as $h_t$ |
| Hidden state | $h_t = o_t \odot \tanh(C_t)$ | Output hidden state |

### Parameter Count

$$\text{Params} = 4 \times \dim(h) \times (\dim(h) + \dim(x))$$

There are **4 weight matrices**: $W_f, W_i, W_C, W_o$ — hence 4× an equivalent SimpleRNN.

```python
model = keras.Sequential([
    keras.layers.Embedding(input_dim=vocab_size, output_dim=64),
    keras.layers.LSTM(128, return_sequences=True),
    keras.layers.LSTM(64),
    keras.layers.Dense(1, activation='sigmoid')
])
```

---

## Stacked RNNs / LSTMs

Multiple RNN/LSTM layers stacked on top of each other. The first layer must have `return_sequences=True` to pass a full sequence to the next layer. May improve performance when the dataset is large.

```python
model = keras.Sequential([
    keras.layers.Embedding(vocab_size, 64),
    keras.layers.LSTM(128, return_sequences=True),  # passes full sequence
    keras.layers.LSTM(64),                           # final layer
    keras.layers.Dense(num_classes, activation='softmax')
])
```

---

## Bidirectional RNN

A Bidirectional RNN runs **two independent RNNs** over the sequence — one forward, one backward — and **concatenates** their hidden states: $[h_t, h'_t]$.

- **Use when:** the full input sequence is available (e.g., text classification, encoding).
- **Cannot use as decoder:** the backward pass requires future tokens, which don't exist yet during autoregressive generation.

```python
model = keras.Sequential([
    keras.layers.Embedding(vocab_size, 64),
    keras.layers.Bidirectional(keras.layers.LSTM(64)),
    keras.layers.Dense(1, activation='sigmoid')
])
```

---

## Pretrained Embeddings

The embedding layer is responsible for most trainable parameters. When labeled data is scarce, **freeze a pretrained embedding** (e.g., GloVe, Word2Vec) to reduce trainable parameters and leverage large-corpus knowledge.

---

## Best Practices Summary

1. **Always use LSTM** instead of SimpleRNN.
2. **Use Bi-RNN** instead of unidirectional RNN whenever possible.
3. **Stack RNN layers** for larger datasets.
4. **Pretrain the embedding layer** when labeled data is small.

---

## Text Generation (Char-Level)

1. Slice text into overlapping segments; each segment is input, the next character is the label.
2. Formulated as **multi-class classification** (one class per character).
3. Choosing the next character:
   - *Greedy*: always pick the highest-probability character — too deterministic.
   - *Multinomial sampling*: sample from the distribution — too random.
   - *Temperature-scaled sampling* (best): adjust the sharpness of the distribution.

```python
import numpy as np

def sample_with_temperature(predictions, temperature=1.0):
    predictions = np.asarray(predictions).astype("float64")
    predictions = predictions ** (1.0 / temperature)
    predictions = predictions / np.sum(predictions)
    return np.random.choice(len(predictions), p=predictions)
```

- **temperature < 1**: more deterministic (sharper distribution).
- **temperature > 1**: more random (flatter distribution).
- **temperature = 1**: standard multinomial sampling.

---

## Machine Translation: Seq2Seq

Architecture: **LSTM Encoder** → final states $(h, c)$ → **LSTM Decoder**

- Two separate tokenizers/dictionaries (source and target languages have different vocabularies).
- Loss: Cross-Entropy.

### Improvements

| Technique | Why it helps |
|---|---|
| Bi-LSTM Encoder | Longer memory — doesn't forget early tokens in long sentences |
| Word-level tokenization | Shorter sequences → less forgetting; BUT requires more data |
| Multi-task learning | Additional supervision signal |
| Attention | Decoder can focus on relevant encoder states |

> **Why can't the Bi-LSTM be the decoder?** Causality. Decoding is autoregressive — you generate one token at a time. The backward LSTM requires seeing future tokens, which don't exist yet.

```python
# Encoder
encoder_inputs = keras.Input(shape=(None,))
enc_emb = keras.layers.Embedding(src_vocab_size, 256)(encoder_inputs)
encoder_lstm = keras.layers.Bidirectional(keras.layers.LSTM(256, return_state=True))
enc_out, fh, fb, bh, bb = encoder_lstm(enc_emb)
state_h = keras.layers.Concatenate()([fh, bh])
state_c = keras.layers.Concatenate()([fb, bb])

# Decoder
decoder_inputs = keras.Input(shape=(None,))
dec_emb = keras.layers.Embedding(tgt_vocab_size, 256)(decoder_inputs)
decoder_lstm = keras.layers.LSTM(512, return_sequences=True, return_state=True)
dec_out, _, _ = decoder_lstm(dec_emb, initial_state=[state_h, state_c])
decoder_outputs = keras.layers.Dense(tgt_vocab_size, activation='softmax')(dec_out)

model = keras.Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
```

---

## Related Notes
- [[Attention & Transformers]] - Mechanism that allows decoders to focus on relevant encoder states.
- [[4. RNNs & CNNs for Text Classification]] - NLP perspective on RNN architectures.
- [[5. Tokenization]] - Text preprocessing details.
- [[3. Word Vectors]] - Embedding representations used as RNN input.
