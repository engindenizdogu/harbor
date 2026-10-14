---
title: Transformer Snippets
tags: [nlp, deep-learning, transformer, code-snippets, auto-captured]
draft: false
---
PyTorch building blocks of the original Transformer, in the order they are assembled. They follow the structure of *The Annotated Transformer* (see the walkthrough in [[Attention & Transformers]]); shapes are `(batch, seq, d_model)` unless noted.

## Scaled Dot-Product Attention

```python
import math, torch, torch.nn as nn

def attention(query, key, value, mask=None, dropout=None):
    d_k = query.size(-1)
    scores = query @ key.transpose(-2, -1) / math.sqrt(d_k)   # (..., q_len, k_len)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)           # blocked positions get ~0 weight
    p_attn = scores.softmax(dim=-1)
    if dropout is not None:
        p_attn = dropout(p_attn)
    return p_attn @ value, p_attn
```

The $\sqrt{d_k}$ scaling keeps the dot products from growing with the key width, which would push the softmax into regions with tiny gradients.

## Multi-Head Attention

```python
import copy

def clones(module, n):
    return nn.ModuleList([copy.deepcopy(module) for _ in range(n)])

class MultiHeadedAttention(nn.Module):
    def __init__(self, h, d_model, dropout=0.1):
        super().__init__()
        assert d_model % h == 0
        self.d_k, self.h = d_model // h, h
        self.linears = clones(nn.Linear(d_model, d_model), 4)  # W_Q, W_K, W_V, W_O
        self.dropout = nn.Dropout(dropout)

    def forward(self, query, key, value, mask=None):
        if mask is not None:
            mask = mask.unsqueeze(1)                           # same mask for every head
        b = query.size(0)
        # 1) project, then split d_model into h heads of size d_k
        q, k, v = [
            lin(x).view(b, -1, self.h, self.d_k).transpose(1, 2)
            for lin, x in zip(self.linears, (query, key, value))
        ]
        # 2) attend in all heads at once
        x, _ = attention(q, k, v, mask=mask, dropout=self.dropout)
        # 3) concatenate heads and apply the output projection
        x = x.transpose(1, 2).contiguous().view(b, -1, self.h * self.d_k)
        return self.linears[-1](x)
```

All heads share one matrix multiply per projection: the single `d_model x d_model` weight is just the $h$ per-head matrices stacked.

## Masks

```python
def subsequent_mask(size):
    "True where a position may attend: itself and everything before it."
    return torch.tril(torch.ones(1, size, size, dtype=torch.bool))

def padding_mask(src, pad_idx=0):
    return (src != pad_idx).unsqueeze(-2)                      # (batch, 1, src_len)
```

The decoder combines both: a target position may attend only to earlier, non-padding positions.

## Residual Connection with Layer Norm

```python
class SublayerConnection(nn.Module):
    "x + Dropout(Sublayer(LayerNorm(x))): normalization applied before the sublayer."
    def __init__(self, size, dropout):
        super().__init__()
        self.norm = nn.LayerNorm(size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, sublayer):
        return x + self.dropout(sublayer(self.norm(x)))
```

The paper writes $\text{LayerNorm}(x + \text{Sublayer}(x))$ (post-norm). Normalizing first (pre-norm) is the common variant in code because it trains more stably in deep stacks.

## Position-wise Feed-Forward and Embeddings

```python
class PositionwiseFeedForward(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.w_1, self.w_2 = nn.Linear(d_model, d_ff), nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        return self.w_2(self.dropout(self.w_1(x).relu()))

class Embeddings(nn.Module):
    def __init__(self, d_model, vocab):
        super().__init__()
        self.lut, self.d_model = nn.Embedding(vocab, d_model), d_model

    def forward(self, x):
        return self.lut(x) * math.sqrt(self.d_model)           # scale to match the positional encoding
```

## Sinusoidal Positional Encoding

```python
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout, max_len=5000):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        pe = torch.zeros(max_len, d_model)
        pos = torch.arange(max_len).unsqueeze(1)
        div = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe[:, 0::2], pe[:, 1::2] = torch.sin(pos * div), torch.cos(pos * div)
        self.register_buffer("pe", pe.unsqueeze(0))            # fixed, not trained

    def forward(self, x):
        return self.dropout(x + self.pe[:, : x.size(1)])
```

## Training Recipe: Warmup Schedule and Label Smoothing

```python
from torch.optim.lr_scheduler import LambdaLR

def rate(step, d_model=512, factor=1.0, warmup=4000):
    step = max(step, 1)                                         # avoid 0 ** -0.5
    return factor * d_model ** -0.5 * min(step ** -0.5, step * warmup ** -1.5)

model = nn.Linear(1, 1)                                         # stand-in for the Transformer
optimizer = torch.optim.Adam(model.parameters(), lr=1.0, betas=(0.9, 0.98), eps=1e-9)
scheduler = LambdaLR(optimizer, lr_lambda=rate)                 # call scheduler.step() after each optimizer step
```

The learning rate rises linearly for `warmup` steps, then decays with the inverse square root of the step. The optimizer's base `lr` is 1.0 so the schedule alone sets the rate.

```python
class LabelSmoothing(nn.Module):
    "KL divergence against a smoothed target: (1 - eps) on the true token, eps spread over the rest."
    def __init__(self, vocab_size, padding_idx, smoothing=0.1):
        super().__init__()
        self.criterion = nn.KLDivLoss(reduction="sum")
        self.vocab_size, self.padding_idx, self.smoothing = vocab_size, padding_idx, smoothing

    def forward(self, log_probs, target):                       # log_probs: (n_tokens, vocab)
        true_dist = torch.full_like(log_probs, self.smoothing / (self.vocab_size - 2))
        true_dist.scatter_(1, target.unsqueeze(1), 1.0 - self.smoothing)
        true_dist[:, self.padding_idx] = 0                      # never predict padding
        true_dist[target == self.padding_idx] = 0               # ignore padded targets
        return self.criterion(log_probs, true_dist.detach())
```

Smoothing with $\epsilon = 0.1$ raises perplexity (the model is deliberately less certain) but improves accuracy and BLEU.

## Greedy Decoding

```python
@torch.no_grad()
def greedy_decode(model, src, src_mask, max_len, start_symbol):
    memory = model.encode(src, src_mask)
    ys = torch.full((1, 1), start_symbol, dtype=src.dtype, device=src.device)
    for _ in range(max_len - 1):
        out = model.decode(memory, src_mask, ys, subsequent_mask(ys.size(1)).to(src.device))
        next_word = model.generator(out[:, -1]).argmax(dim=-1)  # most likely next token
        ys = torch.cat([ys, next_word.view(1, 1)], dim=1)
    return ys
```

Greedy decoding keeps only the single best token at each step; beam search keeps several candidates and usually scores higher.

---
*Source: written in the style of [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/) (Harvard NLP) for [Attention Is All You Need](https://arxiv.org/abs/1706.03762). Related:* [[Attention & Transformers]] | [[Code Snippets MOC]]
