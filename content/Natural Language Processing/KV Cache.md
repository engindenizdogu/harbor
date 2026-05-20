---
title: KV Cache
tags:
  - nlp
  - llms
  - optimization
  - transformers
draft: false
---
**KV (Key-Value) caching** is a critical performance optimization technique used in Large Language Models (LLMs) to speed up text generation (inference).

## The Core Problem: Redundant Computation
LLMs are **autoregressive**, meaning they generate text one token at a time. To generate each new token, the model technically needs to "look back" at all the previous tokens in the sequence to maintain context and coherence. 

Without caching, a naive implementation would re-process the entire history of the sequence for every single new token generated. As the conversation or document gets longer, this creates a massive computational bottleneck, as the amount of work required scales quadratically ($O(n^2)$) with the sequence length.

## How KV Caching Solves It
draft: false
*   **Value (V):** Represents the actual content or meaning the token provides.

When generating a new token, the **Key** and **Value** vectors for all previous tokens remain exactly the same as they were in the previous step. They never change. 

**KV caching works by:**
1.  **Storing** the Key and Value vectors for all previously processed tokens in GPU memory.
2.  **Retrieving** those cached vectors when generating the next token, instead of recomputing them from scratch.
3.  **Computing** only the Query, Key, and Value for the *new* token, then appending them to the existing cache.

This turns what was previously a redundant, quadratic process into a much faster, linear operation, as the model only performs "new" work for the current token being generated.

## The Trade-off: Compute vs. Memory
While KV caching significantly reduces computation time and latency, it comes with a cost: **increased memory usage.**

*   **Memory Footprint:** The cache must be stored in fast, high-bandwidth memory (usually VRAM on a GPU) to be effective. As the sequence length grows, the memory required to store the KV cache grows linearly.
*   **Bottleneck:** In modern LLM serving, the KV cache often becomes a primary memory bottleneck. If the cache grows too large, it may exceed available GPU memory, forcing engineers to use techniques like **quantization** (reducing the precision of the cached data), **paging** (similar to virtual memory in OS, e.g., PagedAttention), or **offloading** (moving parts of the cache to slower CPU or system memory).

## Summary Table

| Feature         | Without KV Cache                        | With KV Cache                     |
| :-------------- | :-------------------------------------- | :-------------------------------- |
| **Computation** | Recomputes all previous tokens          | Only computes the new token       |
| **Complexity**  | Quadratic ($O(n^2)$)                    | Linear ($O(n)$)                   |
| **Speed**       | Slow (becomes slower as sequence grows) | Fast (consistent per-token speed) |
| **Memory**      | Low (no storage of past states)         | High (stores past K, V tensors)   |

## Related Concepts
- [[Transformer Architecture]]
- [[Attention Mechanism]]
- [[Autoregressive Models]]
