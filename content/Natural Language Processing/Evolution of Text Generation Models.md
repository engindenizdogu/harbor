---
title: Evolution of Text Generation Models
tags: [nlp, language-models, history, auto-captured]
draft: false
---

A timeline of how text generation approaches evolved, from hand-written rules to large pre-trained Transformers. Dates are those of the original works; items after the Transformer link to the notes that cover them.

## Early approaches
1. **Rule-based and template systems (1950s-1980s):** hand-written grammars and templates (e.g., ELIZA, 1966). Predictable but brittle.
2. **N-gram language models (1980s-2000s):** predict the next word from the previous n-1 words using counts; smoothing (e.g., Kneser-Ney) handles sparsity. See [[Language Modeling & N-grams]].

## Neural era
3. **Neural language models (2003):** learned embeddings plus a feed-forward network generalize across similar words.
4. **RNNs (2010):** a hidden state carries context, but vanishing gradients limit memory. See [[RNNs & LSTMs]].
5. **LSTMs and GRUs:** gating preserves information over longer spans.
6. **Seq2seq encoder-decoder (2014):** maps input to output (translation, summarization) but through a fixed-vector bottleneck.
7. **Attention (2014-2015):** the decoder looks back at all encoder states, removing the bottleneck.
8. **Transformer (2017):** self-attention replaces recurrence, enabling parallel training and long-range dependencies. See [[Attention & Transformers]].

## Pretraining and scale
9. **Pretrain then fine-tune (2018-2019):** GPT (decoder-only, autoregressive), BERT (encoder-only, masked, not a generator), T5/BART (encoder-decoder, text-to-text). See [[GPT-1]] and [[BERT]].
10. **Scaling era (2020-2022):** GPT-3 showed few-shot in-context learning; scaling laws (Kaplan, Chinchilla) guided size-versus-data tradeoffs. Decoder-only became dominant. See [[GPT-2 and GPT-3]] and [[Large Language Models]].
11. **Alignment (2022):** instruction tuning and RLHF make models follow intent. See [[Reinforcement Learning from Human Feedback]].

## Recent directions
12. **Open and efficient models (2022-2024):** open-weight models, mixture-of-experts, grouped-query attention, FlashAttention (2022), the [[KV Cache]].
13. **Reasoning models (2024-present):** RL-trained long chains of thought and more inference-time compute.
14. **Alternatives and hybrids:** state-space models (Mamba), diffusion language models, multimodal architectures.

*Sources: [Attention Is All You Need](https://arxiv.org/abs/1706.03762) (2017), [BERT](https://arxiv.org/abs/1810.04805) (2018), [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) (2020), and [FlashAttention](https://arxiv.org/abs/2205.14135) (2022). The dates for the Transformer, GPT-1, BERT, GPT-2, GPT-3, and FlashAttention were checked against the papers or their arXiv listings. The earlier items (ELIZA, n-gram smoothing, neural language models, RNN language models, seq2seq, attention) and the later ones (grouped-query attention, Mamba, reasoning models) are dated from general knowledge and were not re-checked here.*

## Related Notes
- [[Language Modeling & N-grams]] - The statistical starting point.
- [[RNNs & LSTMs]] - The recurrent era.
- [[Attention & Transformers]] - The architecture that changed the field.
- [[GPT-1]], [[BERT]], [[GPT-2 and GPT-3]] - The pre-training era.
- [[Large Language Models]] - Scale and alignment.
