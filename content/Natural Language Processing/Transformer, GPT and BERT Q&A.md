---
title: Transformer, GPT and BERT Q&A
tags: [nlp, transformers, bert, gpt, study-guide, auto-captured]
draft: false
---
Study guide in question-and-answer form, conceptual focus. Each answer starts with a short version, followed by details.

**Contents**
1. Attention Is All You Need (2017)
2. Improving Language Understanding by Generative Pre-Training, GPT-1 (2018)
3. BERT (2018)

The reinforcement learning papers are covered in [[RL Concepts and Papers Q&A]].
## 1. Attention Is All You Need (2017)

### Quick reference (base model)

| Item | Value |
|---|---|
| Layers per stack (N) | 6 encoder, 6 decoder |
| Model width (d_model) | 512 |
| Attention heads (h) | 8 |
| Per-head size (d_k = d_v) | 512 / 8 = 64 |
| Feed-forward inner size (d_ff) | 2048 |
| Dropout | 0.1 |
| Position information | fixed sinusoidal encoding |
| Vocabulary (English-German) | shared byte-pair vocabulary, about 37,000 tokens |
| Notation | n = source length, m = target length |

### 1.1 Encoder and decoder stacks

#### Are the encoder layer outputs concatenated?

> [!tip] Short answer
> No. Layers are stacked in sequence, not concatenated.

- The base encoder is N = 6 identical layers, each with its own weights.
- Each layer's `(n, 512)` output is the next layer's input; the width stays 512 throughout.
- The final layer's `(n, 512)` output is the encoder output, often called the **memory**.
- Every decoder layer reads that same final matrix in cross-attention, as K and V. The intermediate encoder layers are not read by the decoder.
- Concatenation happens only inside multi-head attention, where the 8 head outputs are joined into `(n, 512)` before W_O.

#### How does the decoder differ from the encoder?

> [!tip] Short answer
> It has a third sublayer (cross-attention), a masked self-attention, a shifted-right input, and an output head.

| | Encoder layer | Decoder layer |
|---|---|---|
| Sublayers | 1. self-attention, 2. feed-forward | 1. **masked** self-attention, 2. **cross-attention** over the encoder output, 3. feed-forward |
| Add & Norm | after each of the 2 sublayers | after each of the 3 sublayers |
| Input | source tokens + positional encoding | target tokens **shifted right by one** + positional encoding |
| Output | `(n, 512)` memory | `(m, 512)`, then linear + softmax over the vocabulary |

- In cross-attention, Q comes from the decoder state while K and V are projections of the encoder output `z`. The scores are `(m, n)` and there is no mask.
- With the causal mask and the right-shifted input, the prediction at position i depends only on positions before i.
- After the last decoder layer, a linear layer maps `(m, 512)` to `(m, vocab_size)` and softmax gives a next-token distribution per position.

> [!example] Example (translation)
> English "The cat sat" to French "Le chat s'est assis".
>
> - The encoder reads "The cat sat" once and produces the memory z, one 512-dimensional vector per source word.
> - The decoder starts from a start token and writes one French token at a time. To produce "chat" it first runs masked self-attention over what it has written so far ("Le"), then cross-attention, where its query asks "which source word am I translating now?" and attends mostly to "cat".
> - The softmax at that position then puts high probability on "chat". Each new token is appended and the process repeats.

#### How does decoder training differ from inference?

- **Training:** all m target positions are processed in parallel (teacher forcing); the mask prevents cheating.
- **Inference:** autoregressive. Predict a token, append it to the decoder input, repeat.

> [!question]+ Check yourself: why is the decoder input shifted right by one?
> So that the token at position i is predicted from positions before i. The input is [start, y1, ..., y(m-1)] and the targets are [y1, ..., y(m)]; together with the causal mask, position i never sees the token it must predict.

#### What are n and m, and what are the shapes?

> [!tip] Short answer
> n is the source length (encoder), m is the target length (decoder). They usually differ.

| Object                               | Shape                                                              |
| ------------------------------------ | ------------------------------------------------------------------ |
| Encoder output z                     | `(n, 512)`                                                         |
| Decoder state                        | `(m, 512)`                                                         |
| Encoder self-attention scores        | `(n, n)`                                                           |
| Decoder masked self-attention scores | `(m, m)`                                                           |
| Cross-attention scores               | `(m, n)` (rows are target positions, columns are source positions) |
| Final output                         | `(m, vocab_size)`                                                  |

> [!warning] Common mistake
> Cross-attention scores are `(m, n)`, not `(n, n)`: rows are target (query) positions and columns are source (key) positions. An `(n, n)` matrix appears only in encoder self-attention.

### 1.2 Attention: Q, K, V

#### What exactly are Q, K, and V?

> [!tip] Short answer
> Three learned linear projections of the same input: query = what a token looks for, key = how a token advertises itself, value = what it hands over when chosen.

```
Q = X · W_Q       K = X · W_K       V = X · W_V
Attention(Q, K, V) = softmax( Q Kᵀ / √d_k ) · V
```

| Piece | Role |
|---|---|
| Query | "What information do I need?" |
| Key | "What do I contain, for matching?" |
| Value | "What do I contribute if you pick me?" |
| Dot products Q·Kᵀ | score every query against every key |
| Softmax (per row) | turns scores into weights that sum to 1 |
| Multiply by V | each output is a weighted average of the value vectors |
| Division by √d_k | stops large dot products from saturating the softmax |

Library analogy: the query is your search request, the keys are the labels on the books, and the values are the books' contents.

> [!example] Example in English
> (conceptual illustration; roles and weights are what a trained model plausibly learns, not measured values)
>
> Sentence: "The animal didn't cross the street because it was too tired." To understand "it", the model must work out what it refers to.
>
> | Role | For the token "it" |
> |---|---|
> | Query | "I'm a pronoun; I need a noun I could refer to, one that could be tired" |
> | Key of "animal" | "I'm a living noun, a likely subject" |
> | Key of "street" | "I'm a place, an inanimate noun" |
> | Key of "tired" | "I'm an adjective describing a state" |
> | Value of "animal" | the content of its meaning: a living creature, the subject |
>
> - The query of "it" matches the key of "animal" best, since a living thing can be tired, and "street" much less. Illustrative attention weights for "it": animal 0.55, street 0.15, tired 0.10, it 0.10, other words 0.10.
> - The new representation of "it" is a weighted blend of the value vectors, mostly the meaning of "animal", so the reference is resolved.
> - "animal" is found because of what its **key** advertises (animate noun), but what "it" receives is its **value** (its meaning); these are two different jobs, which is why they are separate projections.
> - Context changes the match: in "...because it was too wide", "it" should match "street", since the query depends on the whole context.
> - Different heads look for different relations at once: pronoun to referent, adjective to the noun it describes, previous word.

> [!example] Worked example with numbers
> (tiny sizes: 3 tokens, d_model = 4, one head with d_k = d_v = 2; numbers are made up for illustration)
>
> ```
> X (3 tokens × 4)           W_Q (4×2)    W_K (4×2)    W_V (4×2)
> the  [1 0 1 0]            [1 0]        [1 0]        [1 0]
> cat  [0 1 0 1]            [0 1]        [0 1]        [0 1]
> sat  [1 1 0 0]            [1 0]        [0 0]        [1 1]
>                           [0 1]        [1 0]        [0 0]
>
> Q = X·W_Q       K = X·W_K       V = X·W_V       (each 3×2)
> the [2 0]       the [1 0]       the [2 1]
> cat [0 2]       cat [1 1]       cat [0 1]
> sat [1 1]       sat [1 1]       sat [1 1]
>
> scores = Q·Kᵀ   scaled (÷√2)    softmax per row        output = weights·V
> [2 2 2]         [1.41 1.41 1.41]  [0.33 0.33 0.33]      [1.00 1.00]
> [0 2 2]         [0.00 1.41 1.41]  [0.11 0.45 0.45]      [0.66 1.00]
> [1 2 2]         [0.71 1.41 1.41]  [0.20 0.40 0.40]      [0.80 1.00]
> ```
>
> Reading the row for "cat": its query `[0 2]` matches the keys of "cat" and "sat" (score 2) more than the key of "the" (score 0), so after softmax it puts about 45% of its attention on each of "cat" and "sat" and only 11% on "the". Its output `[0.66, 1.00]` is the weighted average of the three value vectors: 0.11·[2 1] + 0.45·[0 1] + 0.45·[1 1]. Each token ends up with a new 2-dimensional vector that mixes information from the tokens it attended to. With a causal mask the weights above the diagonal would be zero (for "cat": 0.2 on "the", 0.8 on "cat", 0 on "sat").

#### Why three projections instead of the raw embedding, or only two?

> [!tip] Short answer
> Each projection solves a different problem; removing any one costs expressiveness.

- **Using K as V** forces one vector to be both the matching key and the content handed over, so "what makes me relevant" can't be separated from "what information I carry". A token might be matched because it is a verb while passing along information about its subject.
- **Using Q as K** makes the score symmetric: `x_i · W_Q W_Qᵀ · x_jᵀ` equals the score for `(j, i)`. Attention could not be directional (a verb looking for its subject is a different role from the subject looking for its verb), and each token would tend to match itself most strongly because `q_i · q_i` is a squared norm.
- Separate `W_Q` and `W_K` give a general **asymmetric** bilinear form, so what a token searches for can differ from what it advertises.
- This is a design choice that works best in practice, not a mathematical necessity. Variants such as multi-query attention share K and V across heads to save memory.

#### Where do Q, K, V come from in each attention block?

| Attention type | Q from | K and V from | Mask |
|---|---|---|---|
| Encoder self-attention | previous encoder layer | previous encoder layer | none |
| Decoder self-attention | decoder | decoder | causal |
| Encoder-decoder (cross) | decoder | encoder output z | none |

#### Are Q, K, V initialized the same, since the diagram splits into three?

> [!tip] Short answer
> The input is the same, but the three weight matrices are separate and independently initialized.

- The same X goes through three different matrices W_Q, W_K, W_V, each randomly initialized (commonly Xavier-style; the paper does not specify). So Q, K, V differ from the first forward pass.
- Training shapes each matrix toward its role because they feed different parts of the computation: Q and K feed the scores, V feeds the output. The roles emerge from usage.
- Each head has its own independently initialized projections. This breaks symmetry so heads can specialize instead of learning identical things.

#### What are the "Linear" boxes in Figure 2, and why does the paper write Q·W^Q instead of X·W?

> [!tip] Short answer
> The bottom Linear boxes are W_Q, W_K, W_V (one set per head); the top Linear is W_O. The paper's Q, K, V on the left of the multiplication are the block's inputs.

- **Bottom three Linear boxes:** `W_Q`, `W_K`, `W_V`, drawn stacked because there is one set per head (h = 8).
- **Linear after Concat:** a different matrix, `W_O`. The concatenated heads (8 × 64 = 512) are mixed and projected back to d_model.
- **Scaled dot-product block** (MatMul, Scale, optional Mask, SoftMax, MatMul): no learned weights.
- **Paper's formula:** `head_i = Attention(Q·W_i^Q, K·W_i^K, V·W_i^V)`. Here Q, K, V on the right are the **inputs to the block** (the three arrows at the bottom of the figure); the projected versions are `Q·W_i^Q` and so on.
- The block is reused with different inputs: in encoder and decoder self-attention all three inputs are the same X, so `Q·W^Q` is just `X·W^Q`. In cross-attention, the query input is the decoder state and the key and value inputs are the encoder output.
- The letters Q, K, V are **overloaded**: raw block inputs on the left of the multiplication, projected matrices going into scaled dot-product attention.
- So in the encoder, K, Q, V are the *outputs* of the projections, not the block's inputs; the block's three inputs are all X.
- For the first layer X is token embeddings plus positional encoding; for later layers it is the previous layer's output.

> [!warning] Common mistake
> In the encoder, K, Q, and V are the *outputs* of the projections, not the block's inputs; the block's three inputs are all the same X. The Q, K, V on the right of the paper's `Q·W^Q` are the block inputs, and the same letters are reused for the projected matrices.

#### What are the dimensions of Q, K, V and of each attention step?

> [!tip] Short answer
> Per head, Q, K, V are `(n, 64)`; scores are `(n, n)`; the head output is `(n, 64)`; 8 heads concatenate to `(n, 512)`.

| Step (self-attention, one head) | Operation | Shape |
|---|---|---|
| Input | X | `(n, 512)` |
| Weights | W_Q, W_K, W_V (each) | `(512, 64)` |
| Projections | Q, K, V | `(n, 64)` each |
| 1. MatMul | Q · Kᵀ | `(n, 64)·(64, n)` = `(n, n)` |
| 2. Scale | divide by √64 = 8 | `(n, n)` |
| 3. Mask (optional) | add -∞ above the diagonal | `(n, n)` |
| 4. Softmax | along each row | `(n, n)`, rows sum to 1 |
| 5. MatMul | weights · V | `(n, n)·(n, 64)` = `(n, 64)` |
| Concat 8 heads | | `(n, 512)` |
| Output projection | W_O is `(512, 512)` | `(n, 512)` |

- Entry (i, j) of the weight matrix is how much token i attends to token j. Output row i is a weighted average of the value vectors.
- The `(n, n)` matrix is why attention cost grows quadratically with sequence length.
- Splitting 512 across 8 heads keeps the cost close to one full-width head but gives 8 attention patterns.
- **Cross-attention:** Q is `(m, 64)`, K and V are `(n, 64)`. Then `Q·Kᵀ` is `(m, n)`, the weights are `(m, n)`, and weights · V is `(m, n)·(n, 64)` = `(m, 64)`. After concat and W_O the output is `(m, 512)`, matching the decoder residual. An `(n, n)` score matrix appears only in encoder self-attention.
- Q and K must share d_k for the dot product; the paper also sets d_v equal.

> [!question]+ Check yourself: what are the shapes of Q, K, V, the score matrix, and a head's output?
> Per head (n tokens, d_k = d_v = 64): Q, K, V are `(n, 64)`; scores `Q·Kᵀ` are `(n, n)`; the head output is `(n, 64)`; the 8 heads concatenate to `(n, 512)` and W_O keeps it `(n, 512)`.

#### Why scale by √d_k?

If query and key components have unit variance, their dot product has variance d_k, so a large d_k pushes the softmax toward one-hot, where gradients vanish. Dividing by √d_k restores unit variance.

#### What is the mask, and where is it used?

> [!tip] Short answer
> The causal mask stops a position from seeing future tokens. It is used only in decoder self-attention.

- **Why needed:** the decoder generates one token at a time, so predicting token i may use only tokens before i. In training, the full target is available and all positions run in parallel, so without a mask position i could look at token i+1 and cheat.
- **How:** add -∞ to the score entries above the diagonal. Since exp(-∞) = 0, softmax gives future tokens zero weight and each row still sums to 1.

```
scores            mask              after softmax
[a b c d]         [ 0 -∞ -∞ -∞]     [1.0  0   0   0 ]
[e f g h]    +    [ 0  0 -∞ -∞]  →  [.4  .6   0   0 ]
[i j k l]         [ 0  0  0 -∞]     [.2  .3  .5   0 ]
[m n o p]         [ 0  0  0  0]     [.1  .2  .3  .4 ]
```

Row 1 sees only itself; the last row sees all tokens (a lower-triangular pattern).

> [!example] Example
> Training on "I love natural language". The decoder input is the target shifted right (start, I, love, natural) and the targets are (I, love, natural, language).
>
> | Position holding | Can attend to | Must predict |
> |---|---|---|
> | start | start | I |
> | I | start, I | love |
> | love | start, I, love | natural |
> | natural | start, I, love, natural | language |
>
> Without the mask, the position holding "love" could look at the next input token "natural" and simply copy it. With the mask it must predict "natural" from "start I love" alone, which is the same situation it faces when generating.

| Attention | Masked? |
|---|---|
| Encoder self-attention | No (bidirectional) |
| Decoder self-attention | Yes (causal) |
| Cross-attention | No (decoder may see the whole source) |

Implementations also use a padding mask, setting scores for padding tokens to -∞. GPT-style models are decoder-only with the causal mask (autoregressive); BERT drops the mask (bidirectional).

### 1.3 Add & Norm

#### What is the Add & Norm step?

> [!tip] Short answer
> `output = LayerNorm(x + Dropout(Sublayer(x)))`, with shapes staying `(n, 512)`.

- **Add (residual connection):** the sublayer only learns a *correction* to its input. Gradients have a direct path through the addition, and the original embedding and positional signal remain available in higher layers.
- **Why d_model = 512 everywhere:** addition requires matching shapes, so every sublayer and the embeddings produce 512-dimensional outputs.
- **Dropout (p = 0.1)** is applied to the sublayer output before it is added.
- Each encoder layer has two Add & Norm steps: after attention and after the feed-forward network.
- It is **layer** norm, not batch norm, and it is applied to the sum `x + Sublayer(x)`. Normalizing only the sublayer output would leave the skip path un-normalized.

> [!warning] Common mistake
> Layer norm normalizes across the 512 features of each token (not across the batch), and it is applied to `x + Sublayer(x)`, not to the sublayer output alone.

#### What does layer normalization do and help with?

> [!tip] Short answer
> It normalizes each token's 512 features, keeping activations stable so deep stacks train faster and more reliably.

```
μ = mean(x_token),  σ² = variance(x_token)
y = γ · (x − μ) / √(σ² + ε) + β          γ, β learned (512 values each)
```

- Keeps activation scale stable across depth (each residual add increases magnitude and variance).
- Keeps gradients well behaved, allowing larger learning rates and less sensitivity to initialization.
- Keeps inputs to attention and softmax in a healthy range.
- Independent of batch size and sequence length, so it suits variable-length text and one-token-at-a-time inference.
- Learned γ and β preserve expressiveness.

> [!example] Example (layer norm)
> A token vector `[2, 4, 6]` has mean 4 and variance 2.67, so it becomes `[-1.22, 0, 1.22]` (before γ and β). The vector `[20, 40, 60]`, ten times larger, gives exactly the same result, which is how layer norm keeps the scale stable across layers.
>
> **Example (residual):** if the input is `x = [1.0, 2.0]` and the sublayer outputs `[0.1, -0.2]`, the sum is `[1.1, 1.8]`: the original is kept and the sublayer applies a small edit. Without the skip connection the sublayer would have to reproduce `[1.0, 2.0]` itself.

| | Layer norm | Batch norm |
|---|---|---|
| Normalizes | each token across its features | each feature across the batch |
| Depends on batch size | No | Yes |

- The original paper normalizes after adding (**post-LN**); many later models normalize before the sublayer (**pre-LN**), which trains more stably at large depth.
- The original "internal covariate shift" explanation for normalization has been questioned (for batch norm, by Santurkar et al., 2018); the safer summary is that normalization stabilizes activations and smooths optimization.

### 1.4 Position-wise feed-forward network

#### What is the FFN, and does it output `(n, 2048)`?

> [!tip] Short answer
> No. 2048 is the hidden size inside the FFN; its output is `(n, 512)`.

```
FFN(x) = max(0, x·W1 + b1) · W2 + b2
```

| Parameter | Shape |
|---|---|
| W1 | `(512, 2048)` |
| b1 | `(2048,)` |
| W2 | `(2048, 512)` |
| b2 | `(512,)` |

| Step | Shape |
|---|---|
| Input (after Add & Norm) | `(n, 512)` |
| After first linear (expand) | `(n, 2048)` |
| After ReLU | `(n, 2048)` |
| After second linear (compress) | `(n, 512)` |

> [!warning] Common mistake
> 2048 is the hidden size *inside* the FFN. The FFN's output is `(n, 512)`, which the next Add & Norm requires.

- Each bias is one vector broadcast across all n tokens.
- **Position-wise** means the same two layers are applied independently to each token's vector; there is no mixing between tokens (that happens only in attention). It is equivalent to two convolutions with kernel size 1.
- Each layer has its own FFN weights. About 2.1M weights per layer versus about 1M for attention, so the FFN holds most of the model's parameters.

#### Why two fully connected layers instead of one?

- Two linear layers with no nonlinearity between them collapse into one. The ReLU between them is what adds expressiveness.
- The first layer **expands** (512 to 2048), giving the ReLU a richer space; the second **compresses** back to 512 so the result can be added to the residual.
- A single 512-to-512 layer plus ReLU would be much weaker.
- Attention outputs are mostly linear mixes of value vectors, so the FFN provides the main per-token nonlinear processing.
- Interpretively, each hidden unit acts like a feature detector, and later work suggests these layers behave like key-value memories storing much of a model's knowledge.

> [!example] Example (illustrative)
> In "The animal didn't cross the street because it was too tired", attention has just blended information about "animal" into the vector for "it". The FFN then processes that one vector on its own. Some of its 2048 hidden units might respond to "animate, singular subject" and others to "being tired", and the second layer writes the resulting features back into the 512-dimensional vector. No other token is involved in this step.

### 1.5 Embeddings and the output layer

#### What is weight tying?

> [!tip] Short answer
> One embedding matrix E is shared by the encoder input embedding, the decoder input embedding, and the pre-softmax output layer.

| Place | Use of E (shape `(vocab, 512)`) |
|---|---|
| Encoder input | row lookup |
| Decoder input | row lookup |
| Final layer | `logits = h · Eᵀ` |

- The input to the final linear layer is the decoder output `(m, 512)`; the result is `(m, vocab_size)` logits, then softmax.
- The logit for a token is the dot product between the decoder output and that token's embedding.
- Saves parameters (about 19M for a ~37k vocabulary).
- **Sharing between encoder and decoder works** because both sides use one vocabulary (a shared byte-pair vocabulary of about 37,000 tokens for English-German). With separate vocabularies, the encoder and decoder embeddings would be separate matrices, and the output projection could still be tied to the decoder embedding.
- Positional encoding is not a weight matrix and is added to each side independently.

> [!example] Example (illustrative)
> To predict the word after "The cat sat on the", the decoder produces a 512-dimensional vector h. Because the output layer is the embedding table transposed, each candidate's logit is the dot product of h with that word's embedding. "mat" and "floor" have embeddings close to h and get high logits, while "banana" gets a low one. The same vector that represents "mat" as an input is what scores it as an output.

#### Where does the √d_model scaling apply?

On the **input side only**: `x = E[token] · √512 + PE`. Embedding values start small (roughly 1/√d_model per element) while sinusoidal encodings range over [-1, 1], so without scaling the positional encodings would swamp the token meaning. The output projection has no such scaling.

> [!warning] Common mistake
> The √d_model scaling applies to the input embeddings only, not to the output projection `h · Eᵀ`.

#### Are the embeddings trained with the rest of the model?

- Yes. The table is randomly initialized and learned end to end with the translation loss, not taken from pretrained vectors such as Word2Vec or GloVe.
- With weight tying it receives gradient from both the input lookup and the output softmax.
- **Not trained:** the sinusoidal positional encoding (fixed) and the tokenizer (the BPE vocabulary is built beforehand).
- BERT and GPT also learn their embeddings from scratch during pre-training.

### 1.6 Positional encoding

```
PE(pos, 2i)   = sin( pos / 10000^(2i / d_model) )
PE(pos, 2i+1) = cos( pos / 10000^(2i / d_model) )
```

#### What is the difference between `pos` and `i`, and how is `i` chosen?

> [!tip] Short answer
> `pos` is the token's position (the row); `i` indexes the sin/cos dimension pair (the column pair). `i` is a loop index, not a learned or chosen value.

| | Meaning | Range |
|---|---|---|
| `pos` | token position in the sequence | 0, 1, 2, ... |
| `i` | index of the dimension pair | 0 to d_model/2 - 1 (0 to 255) |

- For slot `d` in 0..511: `i = d // 2`; the even slot uses sine and the odd slot uses cosine.
- Small `i` oscillates fast across positions; large `i` oscillates slowly (like the second hand versus the hour hand of a clock).
- The whole table is a **fixed function** of `pos` and `d_model`, computed once.

> [!warning] Common mistake
> `i` is not learned or chosen: it is a loop index, and slot d belongs to pair `i = d // 2` (sine for even slots, cosine for odd). Sinusoidal positional encoding has no trainable weights.

```python
import numpy as np

def positional_encoding(seq_len, d_model):
    pe = np.zeros((seq_len, d_model))
    for pos in range(seq_len):
        for i in range(d_model // 2):
            angle = pos / 10000 ** (2 * i / d_model)
            pe[pos, 2 * i]     = np.sin(angle)
            pe[pos, 2 * i + 1] = np.cos(angle)
    return pe
```

> [!example] Example
> "dog bites man" and "man bites dog" contain the same three words, and attention on its own treats the input as an unordered set, so the two sentences would look identical. Adding a different position vector to each token makes "dog" in first place differ from "dog" in third place.
>
> With d_model = 4 there are two pairs (i = 0 with divisor 1, i = 1 with divisor 100):
>
> | pos | slot 0: sin(pos) | slot 1: cos(pos) | slot 2: sin(pos/100) | slot 3: cos(pos/100) |
> |---|---|---|---|---|
> | 0 | 0.000 | 1.000 | 0.000 | 1.000 |
> | 1 | 0.841 | 0.540 | 0.010 | 1.000 |
> | 2 | 0.909 | -0.416 | 0.020 | 1.000 |
>
> The first pair changes quickly with position and the second barely moves, like a minute hand and an hour hand together.

#### What is its dimension and how is it combined with the embeddings?

Same as the token embeddings: `d_model` per token, `(seq_len, d_model)` per sequence. It is **added** element-wise (not concatenated) to the embedding-layer output, once at the encoder input and once at the decoder input, then dropout is applied. The embeddings are first scaled by √d_model.

#### Why divide by 10000?

- The base 10000 sets the **slowest frequency**. The divisor sweeps from 1 (fastest pair, wavelength 2π) toward 10000 (slowest pair, wavelength about 2π·10000 ≈ 63,000): a geometric progression of wavelengths.
- A large base keeps the slow dimensions from wrapping around within realistic sequence lengths, so positions get unique codes; the spread gives multi-scale resolution.
- It is a hand-picked heuristic with no derivation in the paper; later long-context models raise the base.

#### Why not just add the raw position index?

- Unbounded magnitude swamps the token's meaning.
- Normalizing by length makes the same offset mean different values in different sequences.
- A single scalar is a weak, entangled signal compared with a bounded 512-dimensional code, and it extrapolates poorly.
- Sinusoids make relative offsets easy: `PE(p) · PE(q)` depends only on `p − q`.
- A one-hot position needs a fixed maximum length and has no notion of closeness; it is essentially the learned positional embedding, which the paper found to perform nearly identically.

#### Does the encoding depend on the sequence length?

No. It depends only on `pos` and `d_model`, so position 5 gets the same vector in a 10-token and a 100-token sentence, and it can be evaluated at any position. Caveat: distinct codes don't guarantee the model generalizes to positions longer than those seen in training. Extrapolation turned out weak, which motivated RoPE and ALiBi.

> [!info] Paper detail
> Section 3.5 says the authors also tried learned positional embeddings and found nearly identical results; they chose sinusoids because they might let the model extrapolate to longer sequences than seen in training.

#### Why use both sine and cosine?

- Sine alone is ambiguous (each value occurs twice per cycle). The pair (sin θ, cos θ) is a point on the unit circle and fixes the phase uniquely.
- Shifting a position by k is a **rotation** whose matrix depends only on k, so `PE(pos+k)` is a linear function of `PE(pos)`.
- The dot product of two encodings is a sum of `cos(offset · frequency)` terms, so it depends only on the relative offset, which attention can use directly.

### 1.7 Using the Transformer beyond translation

#### Can it be used for sequence modeling in general, and do you disable the decoder?

> [!tip] Short answer
> Yes. You keep one half of the architecture and drop the other.

| Variant | Keeps | Mask | Cross-attention | Example use |
|---|---|---|---|---|
| Encoder-decoder (original) | both | decoder self-attention only | yes | translation, summarization (T5) |
| Decoder-only | decoder | causal | removed | language modeling (GPT) |
| Encoder-only | encoder | none | n/a | understanding, embeddings (BERT) |

- **Decoder-only:** drop the encoder and the cross-attention sublayer, so each layer is masked self-attention plus FFN. Training feeds tokens t1..tn and predicts t2..t(n+1) at every position in parallel.
- **Encoder-only:** keep the encoder with no mask, plus a small task head (classifier on [CLS], per-token head, or masked-token head).

> [!example] Example
> *Decoder-only:* the prompt "The capital of France is" gives a next-token distribution (illustratively " Paris" 0.92, " a" 0.02, and so on); " Paris" is appended and the model continues. *Encoder-only:* for "The movie was wonderful", the encoder reads all tokens at once and a classifier on the [CLS] vector outputs "positive"; a per-token head on "Washington signed the bill" tags "Washington" as a person.
- The paper tests generalization on English constituency parsing (Section 6.3); the same ideas apply to images, audio, time series, proteins, and code.
- **Strengths:** parallel training across positions; any two tokens interact in one attention step (O(1) path) versus O(n) steps in an RNN.
- **Limitations:** attention cost is O(n²) in sequence length; order must be injected; generation is sequential at inference.

#### What is the inference pipeline for a decoder-only model?

```
tokens so far → embeddings + positional encoding
  → N × [ masked self-attention → Add & Norm → FFN → Add & Norm ]
  → linear + softmax over the vocabulary
  → take the LAST row → pick a token (argmax or sampling) → append → repeat
```

- Only the last position's row predicts the new token; the other rows are needed only in training.
- Choosing a token (argmax, temperature, top-k, top-p) is not part of the network.
- The network is the same as in training; training predicts all positions at once, generation makes one forward pass per token.
- A **KV cache** stores past tokens' keys and values so each step computes only the new token's row.

> [!example] Example
> After generating " Paris", only the new token's query, key, and value are computed; the keys and values for "The capital of France is" are reused from the cache.

#### How can it be parallelized if the layer stack is sequential?

> [!tip] Short answer
> Depth is sequential (6 steps); positions are not.

| Axis | Sequential? | Size |
|---|---|---|
| Layers (1 → 2 → ... → 6) | Yes | N = 6, fixed |
| Positions (tokens 1..n) | No, all at once | n, via matrix operations |

- An RNN needs n sequential steps because `h_t` depends on `h_(t-1)`. The paper's Table 1: self-attention has O(1) sequential operations and O(1) maximum path length; recurrent layers have O(n) for both.
- More parallelism: the 8 independent heads, the batch, and teacher forcing in the decoder.
- It remains sequential at inference (one forward pass per new token, made cheap by the KV cache).

> [!example] Example
> For a 6-word sentence an RNN needs 6 sequential steps, one per word. A 6-layer Transformer also takes 6 sequential steps, one per layer, but each layer handles all 6 words at once. For a 600-word document the RNN needs 600 sequential steps while the Transformer still needs 6 (each over a larger matrix).

> [!question]+ Check yourself: which parts of the Transformer are sequential and which are parallel?
> Depth is sequential: the 6 layers run one after another. Positions are parallel: within a layer, all tokens are processed at once through matrix operations. Autoregressive generation at inference is sequential (one forward pass per new token, made cheap by the KV cache).

---

## 2. Improving Language Understanding by Generative Pre-Training (GPT-1, 2018)

### Quick reference

| Item | GPT-1 | Original Transformer (base) |
|---|---|---|
| Structure | decoder only, masked self-attention | encoder + decoder |
| Layers | 12 | 6 + 6 |
| Hidden size | 768 | 512 |
| Heads | 12 (64 each) | 8 (64 each) |
| FFN inner size | 3072 | 2048 |
| Activation | GELU | ReLU |
| Position information | learned embeddings | fixed sinusoids |
| Context | 512 tokens | n/a |
| Vocabulary | BPE, 40,000 merges | BPE, about 37,000 |
| Parameters | about 117M (not stated in the paper; worked out below) | |

### 2.1 Relation to the Transformer

> [!tip] Short answer
> GPT-1 takes the Transformer decoder without cross-attention, pre-trains it on unlabeled text, then fine-tunes it per task.

- Each block: masked multi-head self-attention, Add & Norm, FFN, Add & Norm, with the causal mask.
- Earlier pre-training work (ULMFiT and others) used LSTMs. The paper argues the Transformer gives a more structured memory for long-term dependencies and more robust transfer; its parallel training also makes large-scale pre-training practical.
- **Timeline:** Transformer (June 2017), GPT-1 (June 2018), BERT (October 2018), which took the **encoder** with bidirectional attention instead.

### 2.2 Framework: two stages

> [!tip] Short answer
> A semi-supervised procedure: learn a high-capacity language model on unlabeled text, then adapt it to each labeled task with a small added output layer.

```
Stage 1 (Section 3.1): unsupervised pre-training  → maximize L1 (Eq. 1) with the model of Eq. 2
Stage 2 (Section 3.2): supervised fine-tuning     → maximize L3 = L2 + λ·L1 (Eq. 3-5)
```

### 2.3 Equation 1: the pre-training objective

```
L1(U) = Σᵢ log P( uᵢ | uᵢ₋ₖ, …, uᵢ₋₁ ; Θ )
```

| Symbol | Meaning |
|---|---|
| U | the unlabeled corpus as a token sequence |
| uᵢ | the actual token at position i (the label) |
| uᵢ₋ₖ … uᵢ₋₁ | the k previous tokens (context window) |
| Θ | all network parameters |
| P(·; Θ) | probability the network assigns (via its softmax) |
| Σᵢ | sum over every position: each token is a training example |

- Maximizing L1 is **maximum likelihood**: choose Θ so the observed text is as probable as possible. It is "unsupervised" because the labels are the next tokens already in the text.
- **Why the log:** it turns a product of probabilities into a sum, is numerically stable, easy to differentiate, and does not change the maximizer (log is monotonic).
- **Chain rule and k:** exactly, `P(u₁…uₙ) = Πᵢ P(uᵢ | u₁…uᵢ₋₁)`. Eq. 1 truncates each conditional to the last k tokens because the network has a bounded context (512). In the Transformer this is not a sliding loop: a 512-token sequence goes in once and the causal mask makes every position predict its next token in parallel.
- **Cross-entropy and perplexity:** maximizing L1 equals minimizing the negative log-likelihood, i.e. the cross-entropy between the one-hot true next token and the softmax output. Perplexity is exp of the average negative log-likelihood per token (lower is better); the paper reports 18.4 on BooksCorpus.
- **Worked example (k = 3, "the cat sat on the mat"):** L1 sums log P(cat | the), log P(sat | the cat), log P(on | the cat sat), log P(the | cat sat on), log P(mat | sat on the).
- A probability of 1 gives log 1 = 0 (the best value); every term is ≤ 0. Probability 1 on every token is not reachable on real text because many contexts have several valid continuations.

#### Isn't this just counting occurrences?

> [!tip] Short answer
> Counting is the exact solution only for lookup-table (n-gram) models. A neural model has no closed form and is trained by gradient ascent.

- n-gram: `P(cat | the) = count("the cat") / count("the")`.
- Neural: P is the output of a network with parameters Θ. Run the forward pass, evaluate the log-probability of each true next token, backpropagate, and nudge Θ so those tokens become more probable. The gradient on the logits is the one-hot true token minus the softmax probabilities.
- Unlike counting, the network generalizes to contexts never seen verbatim (embeddings and shared parameters), handles long contexts where counts would be hopelessly sparse (almost every 512-token context occurs once), and reuses the same Θ at every position.

> [!question]+ Check yourself: why is log(1) = 0 the best value of a term in L1?
> Probabilities are at most 1, so every log-probability is at most 0. A term of 0 means the model gave the true next token probability 1; more negative values mean the model was less confident or wrong.

### 2.4 Equation 2: the model

```
h₀   = U·W_e + W_p
h_l  = transformer_block(h_{l-1})        for l = 1 … n   (n = 12 layers here)
P(u) = softmax( h_n · W_eᵀ )
```

| Line | What it does | Shapes |
|---|---|---|
| h₀ | embedding lookup plus **learned** position embeddings (added) | U `(k, vocab)` one-hot, W_e `(vocab, 768)`, W_p `(k, 768)`, h₀ `(k, 768)` |
| h_l | 12 blocks, each with its own weights; masked self-attention, Add & Norm, FFN (768 to 3072 to 768), Add & Norm; no cross-attention | `(k, 768)` throughout |
| P(u) | multiply by the transposed embedding matrix (**tied weights**), softmax per row | `(k, vocab)` |

- The n in Eq. 2 is the layer count, not the corpus length of Eq. 1.

> [!warning] Common mistake
> Eq. 1 and Eq. 2 both use the letter n: in Eq. 2 it is the number of layers (12), and in Eq. 1 it is the length of the corpus.
- W_e is used twice: embedding lookup at the input and, transposed, as the output projection. The logit for a token is the dot product of the final hidden state with that token's embedding. W_p is separate and used only at the input.
- The linear step has no learned bias in Eq. 2.

> [!example] Example
> The context "the cat" becomes token ids, say [5, 41]. Then h₀ is a `(2, 768)` matrix whose rows are `W_e[5] + W_p[0]` and `W_e[41] + W_p[1]` (each a 768-dimensional vector). The 12 blocks refine these rows, and each row of the final h_n is multiplied by W_eᵀ to score every vocabulary word as the next token.
- **GPT-1's FFN:** `GELU(x·W₁ + b₁)·W₂ + b₂` with W₁ `(768, 3072)`, W₂ `(3072, 768)`. GELU(x) = x·Φ(x) (Φ is the standard normal CDF) is a smooth curve that lets small negative values through, whereas ReLU cuts negatives to zero. It became the default in BERT and GPT-style models.

#### How do Eq. 1 and Eq. 2 connect?

> [!tip] Short answer
> Eq. 2 is the model (how P is computed); Eq. 1 is the objective (how good those probabilities are on real text).

1. Feed the context as U and run Eq. 2.
2. softmax(h_n · W_eᵀ) is a distribution over the whole vocabulary.
3. P(uᵢ | …) is the single entry at the index of the **true** token, so `L1 = Σᵢ log softmax(h_n · W_eᵀ)[uᵢ]`.
4. Example: context "the cat", true token "sat", P(sat) = 0.12 contributes log 0.12 ≈ -2.1. Training changes Θ so this probability rises.

- Θ = {W_e, W_p, all attention and FFN weights, LayerNorm parameters}; the gradient of L1 flows back through the softmax, the 12 blocks, and the embeddings.
- One forward pass over 512 tokens gives 512 distributions and 512 terms of L1 at once.
- Perspective: Eq. 1 is the loss (its negative is the loss), Eq. 2 is the architecture.

### 2.5 Architecture disclosure

#### Is GPT-1's architecture disclosed?

Yes, in Section 4.1 ("Model specifications"): the details are in the quick-reference table. Working out the parameter count:

```
token embeddings   40,000 × 768        ≈ 30.7M   (tied with the output layer)
position embeds    512 × 768           ≈  0.4M
per layer          attention 4 × 768²  ≈ 2.4M
                   FFN 2 × 768 × 3072  ≈ 4.7M     → ≈ 7.1M per layer
12 layers                              ≈ 85M
total                                  ≈ 117M
```

Disclosure shrinks across the line: GPT-2 and GPT-3 architectures were described (GPT-3: 175B parameters, 96 layers, d_model 12,288, weights not released); later models' architectures are not disclosed.

### 2.6 Equations 3-5: supervised fine-tuning

```
P(y | x₁…x_m) = softmax( h_l^m · W_y )         (Eq. 3)
L2(C)         = Σ_{(x,y)} log P(y | x₁…x_m)    (Eq. 4)
L3(C)         = L2(C) + λ · L1(C),  λ = 0.5    (Eq. 5)
```

| Symbol | Meaning | Shape |
|---|---|---|
| C | labeled dataset of (input tokens x₁…x_m, label y) | |
| h_l^m | final block's activation at the **last token** | `(768,)` |
| W_y | new, randomly initialized output matrix | `(768, num_classes)` |

- **Why the last token:** causal masking means it is the only position that has seen the whole input (the "extract" token in Figure 1).
- **Auxiliary loss λ·L1:** keeps the language-modeling loss during fine-tuning; it improves generalization and speeds convergence.
- **New parameters:** only W_y and the embeddings of the delimiter, start, and end tokens. Everything else is reused.

| | Eq. 1 (pre-training) | Eq. 4 (fine-tuning) |
|---|---|---|
| Data | unlabeled text | labeled examples |
| Terms | one per token position | one per example |
| Output | distribution over vocabulary | distribution over classes |
| Output matrix | W_e (tied, pre-trained) | W_y (new) |
| Parameters trained | all, from scratch | all, from pre-trained values, plus W_y |

#### Worked example: sentiment

```
"⟨s⟩ great movie ⟨e⟩" → 12 blocks → h_l^m (768) → · W_y (768×2) → softmax
P(positive) = 0.7, true label positive → L2 term = log 0.7 ≈ -0.36
L3 = L2 + 0.5 · (language-modeling log-likelihood of the same text)
```

Fine-tuning settings: learning rate 6.25e-5, batch size 32, about 3 epochs.

#### Are the pre-trained weights frozen, and is W_e still used?

> [!tip] Short answer
> Not frozen: all weights are updated from their pre-trained values. W_e is still used at the input; only the output projection W_eᵀ is replaced by W_y.

| Parameters | Initialization | During fine-tuning |
|---|---|---|
| Embeddings (W_e, W_p) and 12 blocks | pre-trained | updated (small learning rate) |
| W_y | random | trained from scratch |
| Delimiter, start, end embeddings | random | trained from scratch |

Freezing the network and training only W_y would be the feature-based approach, not GPT-1.

> [!warning] Common mistake
> Fine-tuning does not freeze the pre-trained weights, and W_e is still used at the input. Only the output projection `W_eᵀ` is replaced by the new W_y for prediction; the new parameters are W_y and the special-token embeddings.

#### How does the auxiliary LM loss work (the two heads in Figure 1)?

```
tokens → embeddings + positions → 12 masked blocks → h_l
head A (language model): h_l · W_eᵀ at EVERY position → L1
head B (task classifier): h_l at the LAST token · W_y → L2
L3 = L2 + 0.5 · L1, backpropagated once into the shared body
```

- Pre-training has only head A. At test time only head B is needed.
- The LM target is the task's input text; the label is not a text token, so it enters only through L2.
- This is multi-task learning: a supervised main objective plus an unsupervised auxiliary one.

### 2.7 Task-specific input transformations (Section 3.3)

> [!tip] Short answer
> Structured inputs are flattened into one token sequence, so the architecture never changes.

- **Why needed:** the model was pre-trained on contiguous text, but tasks have structured inputs (sentence pairs, document-question-answer triplets).
- **Rejected alternative:** task-specific architectures on top of transferred representations reintroduce heavy customization and new parameters that get no benefit from transfer.
- **Traversal-style approach:** convert each input into one ordered token sequence wrapped in randomly initialized start and end tokens, with a delimiter `$` between parts.

| Task | Input sequence(s) | Head |
|---|---|---|
| Classification (SST-2, CoLA) | `⟨s⟩ text ⟨e⟩` directly | linear + softmax over classes |
| Entailment (SNLI, MultiNLI, QNLI, RTE, SciTail) | `⟨s⟩ premise $ hypothesis ⟨e⟩` | linear + softmax over entailment, contradiction, neutral |
| Similarity (MRPC, QQP, STS-B) | both orderings (A $ B and B $ A), processed independently; final representations **added element-wise** | linear |
| QA and commonsense (RACE, Story Cloze) | for each candidate a_k: `[z; q; $; a_k]` (context, question, delimiter, answer), scored independently | softmax **across candidates** |

- **Similarity uses both orders:** similarity is symmetric but a causal model's representation depends on order; summing removes the arbitrary choice.
- **QA scores candidates independently** with one shared head, so the number of new parameters does not depend on the number of candidates.
- **Versus BERT:** GPT-1 uses only a delimiter in one flat sequence, with no segment embeddings, and reads the last token. BERT uses [CLS] and [SEP] plus segment embeddings and reads the [CLS] vector.

> [!example] Examples (illustrative inputs)
> | Task | Input sequence | Outcome |
> |---|---|---|
> | Classification | `⟨s⟩ A delightful, moving film ⟨e⟩` | positive |
> | Entailment | `⟨s⟩ A man is playing a guitar $ A person is making music ⟨e⟩` | entailment |
> | Similarity | `⟨s⟩ The film was great $ The movie was excellent ⟨e⟩` and the reversed order; the two final vectors are added | similar |
> | QA, candidate 1 | `⟨s⟩ Tom hiked all day and was exhausted. $ Why did Tom go to bed early? $ He was exhausted ⟨e⟩` | score 1 |
> | QA, candidate 2 | the same context and question with `He had a meeting` | score 2 |
>
> For QA, the two scores go through a softmax across candidates and the higher one is the answer.

#### Do the delimiter, start, and end tokens add new vocabulary?

Yes, three new special tokens, each with a new randomly initialized 768-dimensional row appended to the embedding table (and, with weight tying, to the output projection). They never appear in pre-training, so their embeddings are learned only from fine-tuning data, which is why the formats are kept simple. They occupy normal positions in the 512-token context.

### 2.8 Why pre-training helps, and results

#### How does unsupervised pre-training help a classification task?

> [!tip] Short answer
> The head W_y can only read out what is already in the 768-dimensional vector; pre-training puts useful language knowledge there.

- To predict next tokens on long text the model must learn word meanings, syntax, negation, and tone, none of which needs labels.
- **Sentiment example, few labeled reviews:** a word like "mesmerizing" may never appear in the labeled set, but pre-training places it near "captivating"; a negation like "wasn't terrible" was seen many times. The final-token vector already encodes a rough positive-tone direction, and fine-tuning only learns to read it out. A model trained from scratch would have to learn language from the small labeled set.
- **Grammaticality example:** on CoLA, GPT-1 scored 45.4 versus 35.0 for the previous best, attributed to the linguistic bias learned in pre-training (language modeling gives high probability to well-formed text).

| Stage | Contribution |
|---|---|
| Pre-training (Eq. 1) | general language knowledge in the weights |
| Supervised loss (Eq. 4) | maps that knowledge to the task's labels |
| Auxiliary LM loss (Eq. 5) | keeps the representation language-aware while specializing |

#### Key hyperparameters and results

| Item | Value |
|---|---|
| Pre-training data | BooksCorpus, over 7,000 unpublished books (long contiguous text) |
| Pre-training | Adam, max learning rate 2.5e-4 (warmup over 2,000 updates, cosine decay), 100 epochs, batch 64 of 512-token sequences, N(0, 0.02) initialization, dropout 0.1 |
| Fine-tuning | learning rate 6.25e-5, batch size 32, about 3 epochs, λ = 0.5 |
| Results | state of the art on 9 of 12 tasks |
| Gains | Story Cloze +8.9%, RACE +5.7%, MultiNLI +1.5%, GLUE +5.5% (72.8 versus 68.9) |
| Weaker | RTE 56.0% versus 61.7% for a multi-task BiLSTM |

> [!question]+ Check yourself: why does GPT-1 read the last token for classification?
> Because of the causal mask, only the last token has attended to the entire input, so its activation acts as the summary of the sequence.

> [!info] Paper detail
> The 12 tasks span four categories: natural language inference (SNLI, MultiNLI, QNLI, SciTail, RTE), question answering and commonsense (RACE, Story Cloze), similarity (MRPC, QQP, STS-B), and classification (SST-2, CoLA). The paper also analyzes zero-shot behaviors of the pre-trained model on four settings.

---

## 3. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (2018)

### Quick reference

| | BERT-BASE | BERT-LARGE |
|---|---|---|
| Layers (L) | 12 | 24 |
| Hidden size (H) | 768 | 1024 |
| Heads (A) | 12 | 16 |
| Parameters | 110M | 340M |
| FFN size | 4H = 3072 | 4H = 4096 |
| Vocabulary | WordPiece, 30,000 | |
| Max sequence | 512 | |

### 3.1 Motivation and framing

#### Why do we want bidirectional representations?

> [!tip] Short answer
> A word's meaning often depends on context to its right as well as its left, and a left-to-right model cannot use it.

- Example: in "The bank approved my loan", a left-to-right model has seen only "The" when it builds the representation of "bank".
- The paper argues one-directional restrictions are sub-optimal for sentence-level tasks and very harmful when fine-tuning on token-level tasks such as question answering, where context from both directions is crucial.
- Entailment also needs words in both sentences to relate in both directions.

> [!example] Example
> In "Washington signed the bill" versus "Washington is rainy today", the right-hand words decide whether "Washington" is a person or a place. A shallow model like ELMo computes a left-to-right and a right-to-left representation separately and concatenates them. BERT lets every layer mix information from both sides, so the representation of "Washington" can use "signed the bill" at every level.

#### What limitation of existing models does BERT address, and how does it differ from ELMo?

| Model | Directionality |
|---|---|
| GPT | left-to-right only; each token attends only to previous tokens |
| ELMo | two independently trained LSTMs (left-to-right and right-to-left), concatenated; **shallowly** bidirectional |
| BERT | jointly conditions on left and right context in **all layers**; deeply bidirectional |

#### What are the two strategies for applying pre-trained representations?

| Strategy | Example | How it works |
|---|---|---|
| Feature-based | ELMo | task-specific architectures that take the pre-trained representations as extra features |
| Fine-tuning | OpenAI GPT, **BERT** | minimal task-specific parameters; all pre-trained parameters are fine-tuned |

### 3.2 Architecture

#### Does BERT use the encoder, the decoder, or both?

> [!tip] Short answer
> Only the encoder: a multi-layer bidirectional Transformer encoder, almost identical to the original implementation (tensor2tensor).

- No decoder and no cross-attention.
- Self-attention is **unmasked**, so every token attends to all tokens in both directions.

> [!warning] Common mistake
> BERT has no decoder and no cross-attention, and it cannot generate text naturally. "Encoder" here means bidirectional, unmasked self-attention.
- The paper's footnote: the bidirectional version is usually called a Transformer encoder, and the left-context-only version a Transformer decoder because it can generate text.

#### Why does BERT use only an encoder?

> [!tip] Short answer
> BERT's goal is deep bidirectional *understanding* of text, not generation. That is exactly what an encoder provides, and a decoder would add nothing the task needs.

- **The decoder's job is generation.** A decoder's masked self-attention lets each position see only earlier tokens, so that text can be produced one token at a time. BERT wants the opposite: every token should see both sides.
- **The training task needs both sides.** Masked language modeling predicts hidden tokens from the words on both sides, which an unmasked (encoder) self-attention stack does directly. A causal mask would block the right-hand context and bring back the left-to-right limitation the paper is trying to remove.
- **There is no separate output sequence to generate.** The decoder's cross-attention exists to read a source sequence while writing a different target sequence. BERT's outputs are one vector per input token (and [CLS]), and a small head (a classifier, a tag predictor, or a span scorer) turns them into the answer.
- **Fine-tuning stays simple.** One stack plus one output layer is easy to fine-tune for many tasks, which is the paper's central point.

**What it gives up:** BERT cannot generate text naturally, since there is no autoregressive decoder. That is the trade-off behind the later split in practice: encoders for understanding, retrieval, and classification; decoders for generation.

#### Why was BERT-BASE chosen to match GPT's size?

For a fair comparison (110M versus GPT's size). The critical difference is that BERT uses bidirectional self-attention while GPT lets each token attend only to context on its left.

### 3.3 Input representation

#### What special tokens does BERT use and why?

> [!tip] Short answer
> [CLS] for a sequence-level summary, [SEP] to separate sentences, [MASK] to mark prediction positions.

| Token | Where | Purpose |
|---|---|---|
| [CLS] | first token of every sequence | its final hidden state is the aggregate sequence representation, used for classification and for next sentence prediction |
| [SEP] | between and after the sentences | separates the two sentences of a pair (for example question and answer) |
| [MASK] | replaces selected tokens in masked LM | marks the positions to predict; appears **only in pre-training**, which causes the mismatch discussed below |

They exist so that one token sequence can unambiguously represent either one sentence or a pair, and so the model has a fixed place to read a sequence-level summary.

> [!example] Example (Figure 2)
> `[CLS] my dog is cute [SEP] he likes play ##ing [SEP]`. [CLS] is read for the sequence-level prediction, the two [SEP] tokens end sentence A and sentence B, and during masked-LM pre-training some words in this sequence would be replaced by [MASK].

#### What are the three embeddings, and are the position embeddings learned?

Each token's input is the **sum** of three embeddings (Figure 2):

| Embedding | Contribution |
|---|---|
| Token | WordPiece token identity |
| Segment | learned embedding saying whether the token belongs to sentence A or B |
| Position | position in the sequence (E0, E1, E2, ...) |

- The appendix says the last 10% of pre-training steps use sequences of length 512 "to learn the positional embeddings", so BERT's position embeddings are **learned parameters** (maximum length 512), not the fixed sinusoids of the original Transformer. GPT-1 also learns its positions.
- The paper does not state this explicitly in Section 3; this is inferred from the appendix.

> [!example] Example (Figure 2)
> For `[CLS] my dog is cute [SEP] he likes play ##ing [SEP]`, the tokens are numbered 0 to 10. The first six tokens (through the first [SEP]) get the segment embedding E_A and the last five get E_B. The input for "play" (position 8) is `E_play + E_B + E_8`.

#### What tokenization does BERT use, and how are sentences packed?

- **WordPiece** with a 30,000-token vocabulary; rare words split into pieces, as in "play ##ing".
- **Single sentence:** `[CLS] sentence A [SEP]`. **Pair:** `[CLS] sentence A [SEP] sentence B [SEP]`, with segment embeddings marking A and B.
- A "sentence" is an arbitrary span of contiguous text and a "sequence" is the whole input (up to 512 tokens). One architecture handles both single-text and text-pair tasks.

### 3.4 Pre-training: masked language model

#### How does BERT become bidirectional, and why not train a normal LM with both-sided context?

> [!tip] Short answer
> Standard LMs can only be trained one-directionally, because both-sided conditioning lets each word indirectly "see itself". BERT masks tokens and predicts them instead.

- In a multi-layer model with both-sided context, the target word could trivially be predicted through the other layers.
- BERT masks a percentage of the input tokens at random and predicts only those masked tokens from the surrounding context (a masked LM, also called a Cloze task).
- The representation then fuses left and right context.
- Trade-offs: it cannot generate text naturally; it learns from only about 15% of tokens per sequence.

#### How does masking work in detail?

1. **Select** 15% of all WordPiece tokens in each sequence at random (after tokenization, no special handling of partial word pieces).
2. **Replace** each selected token:

| Replacement | Probability |
|---|---|
| [MASK] token | 80% |
| random token | 10% |
| left unchanged | 10% |

3. **Predict:** the final hidden vector T_i at a selected position goes to a softmax over the vocabulary, trained with cross-entropy against the original token.
4. **Loss:** only selected positions contribute.

> [!example] Example (from the paper's appendix)
> The sentence is "my dog is hairy" and the 4th token, "hairy", is chosen.
>
> | Outcome | Input to BERT | Target at that position |
> |---|---|---|
> | 80%: [MASK] | my dog is [MASK] | hairy |
> | 10%: random word | my dog is apple | hairy |
> | 10%: unchanged | my dog is hairy | hairy |
>
> In every case the model must output "hairy" at that position, and the loss is computed only there.

> [!warning] Common mistake
> Only 15% of tokens are selected, and only 80% of those become [MASK]; the random and unchanged cases are still predicted. The loss is computed only at the selected positions.

#### What mismatch does masking create, and how is it reduced?

> [!tip] Short answer
> [MASK] appears in pre-training but never in fine-tuning. Replacing only 80% of selected tokens with [MASK] reduces the gap.

- For the 20% of selected positions that get a random or unchanged token, the model cannot tell which tokens it must predict, so it has to keep a good contextual representation of **every** input token.
- The paper compares variations of this recipe in Appendix C.2.

> [!question]+ Check yourself: why not always replace the selected tokens with [MASK]?
> Because [MASK] never appears at fine-tuning time, creating a mismatch. With some random or unchanged tokens the model cannot tell which positions it must predict, so it keeps a good contextual representation of every token.

The paper's own reasoning: the encoder does not know which words it will be asked to predict or which have been replaced by random words, so it is forced to keep a distributional contextual representation of every input token. Keeping the word unchanged biases the representation toward the actual observed word. Random replacement affects only 10% of 15% = 1.5% of all tokens, so it does not seem to harm language understanding.

#### How does BERT's masked LM differ from a denoising auto-encoder?

A denoising auto-encoder reconstructs the entire input; BERT predicts only the masked words.

### 3.5 Pre-training: next sentence prediction

#### What is NSP and how are its examples generated?

> [!tip] Short answer
> A binary task: is sentence B the actual next sentence after A? It targets tasks that depend on relationships between two sentences.

- QA and natural language inference depend on sentence relationships, which language modeling does not capture directly.
- For each example, 50% of the time B is the true next sentence (label IsNext) and 50% of the time a random corpus sentence (label NotNext).

> [!example] Example (illustrative)
> With A = "The man went to the store.", the pair B = "He bought a gallon of milk." is labeled IsNext, while B = "Penguins are flightless birds." (a random sentence from elsewhere in the corpus) is labeled NotNext. The [CLS] vector predicts the label.
- The [CLS] vector C is used for the prediction; the final model reaches 97 to 98% accuracy on NSP. The paper reports in Section 5.1 that it benefits QA and NLI.
- Unlike earlier work that transferred only sentence embeddings, BERT transfers all parameters.
- The training loss is the sum of the mean masked-LM likelihood and the mean NSP likelihood.

> [!info] Paper detail
> Section 5.1 reports that NSP benefits QA and NLI. RoBERTa (Liu et al., 2019) later found that removing the NSP loss matches or slightly improves downstream performance.

#### Why is C not a meaningful sentence representation without fine-tuning?

Because it was trained only for the NSP task (the paper's footnote).

#### What loss functions does BERT use?

> [!tip] Short answer
> Cross-entropy (negative log-likelihood) throughout. The paper states it in words and short formulas but does not number its equations the way GPT-1 does.

| Stage | Loss | Where the paper says it |
|---|---|---|
| Masked LM | cross-entropy between the softmax over the vocabulary at each masked position and the original token | Section 3.1: the final hidden vector T_i "will be used to predict the original token with cross entropy loss" |
| Next sentence prediction | binary classification (IsNext or NotNext) from the [CLS] vector, with a likelihood loss | Section 3.1 and Appendix A.2 |
| Total pre-training loss | **sum of the mean masked-LM likelihood and the mean NSP likelihood** | Appendix A.2 |
| Fine-tuning, classification (GLUE) | `log(softmax(C·Wᵀ))`, a standard classification loss, where C is the [CLS] vector and W is the new `(K, H)` label matrix | Section 4.1 |
| Fine-tuning, question answering | **sum of the log-likelihoods of the correct start and end positions**, each from a softmax over the passage tokens (start probability from the dot product of a start vector S with T_i) | Section 4.2 |

```
L_pretrain = L_MLM + L_NSP
L_MLM = - mean over the masked positions of  log P( original token | context )
L_NSP = - log P( IsNext or NotNext | [CLS] vector )
```

- The MLM loss is computed only at the selected 15% of positions.
- The paper does not describe a separate loss for tagging tasks; it says token representations are fed into an output layer.

### 3.6 Data and fine-tuning

#### What data is BERT pre-trained on, and why a document-level corpus?

- **Data:** BooksCorpus (800M words) and English Wikipedia (2,500M words; only text passages, ignoring lists, tables, and headers).
- **Why document-level:** it is critical to extract long contiguous sequences; a shuffled sentence-level corpus such as the Billion Word Benchmark would not provide them.
- **Procedure:** batches of 256 sequences of up to 512 tokens, 1,000,000 steps (about 40 epochs over the 3.3 billion words), sequence length 128 for 90% of the steps and 512 for the last 10%, GELU, dropout 0.1, Adam with learning rate 1e-4.

#### How is BERT fine-tuned for different tasks?

> [!tip] Short answer
> Plug in the task's inputs and outputs and fine-tune all parameters end to end.

| Task type | Input (A and B) | Output used |
|---|---|---|
| Paraphrase, entailment | sentence pair, or hypothesis-premise pair | [CLS] representation to an output layer |
| Question answering | question-passage pair | token representations to an output layer |
| Classification (sentiment) | text with an empty second part | [CLS] representation |
| Sequence tagging | text with an empty second part | token representations |

Each downstream task gets its own fine-tuned model, all initialized from the same pre-trained parameters.

> [!example] Examples (illustrative inputs)
> | Task | Input | Which output is used |
> |---|---|---|
> | Sentiment | `[CLS] The movie was wonderful [SEP]` | [CLS] vector to a classifier: positive |
> | Entailment | `[CLS] A man is playing a guitar [SEP] A person is making music [SEP]` | [CLS] vector: entailment |
> | Question answering | `[CLS] Who wrote Hamlet? [SEP] Hamlet is a play by William Shakespeare. [SEP]` | passage token vectors score a start and end, giving the span "William Shakespeare" |
> | Named entity tagging | `[CLS] Washington signed the bill [SEP]` | each token vector: PERSON, O, O, O |

#### Why does a concatenated pair with self-attention include bidirectional cross attention?

In every layer each token of sentence A can attend to every token of B and the reverse. Earlier approaches encode the two texts independently and then apply cross attention in a separate stage; BERT unifies the two stages with self-attention over the concatenated pair.

#### How expensive is fine-tuning compared with pre-training?

| | Cost |
|---|---|
| Fine-tuning | at most 1 hour on a single Cloud TPU, or a few hours on a GPU |
| Pre-training BERT-BASE | 4 days on 4 Cloud TPUs (16 chips) |
| Pre-training BERT-LARGE | 4 days on 16 Cloud TPUs (64 chips) |

> [!question]+ Check yourself: how does BERT handle a sentence pair differently from GPT-1?
> BERT uses [CLS] and [SEP] tokens plus segment embeddings marking A and B, and reads the [CLS] vector. GPT-1 uses only a delimiter token inside one flat sequence, with no segment embeddings, and reads the last token.

---

*Sources: [Attention Is All You Need](https://arxiv.org/abs/1706.03762) (Vaswani et al., 2017), [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) (Radford et al., 2018), and [BERT](https://arxiv.org/abs/1810.04805) (Devlin et al., 2018). Architecture details, equations, hyperparameters, and results were checked against the papers. Remarks that go beyond the papers are general knowledge, for example the KV cache, pre-layer-norm, multi-query attention, RoPE and ALiBi, and the key-value-memory view of feed-forward layers; the worked examples with illustrative numbers are not from the papers.*

## Related Notes
- [[Attention & Transformers]] - The architecture and the original paper.
- [[GPT-1]] - The GPT-1 paper in note form.
- [[BERT]] - The BERT paper in note form.
- [[RL Concepts and Papers Q&A]] - The companion guide for the reinforcement learning papers.
