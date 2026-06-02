---
title: Building Embedding Models From Scratch
tags:
  - nlp
  - code-snippet
  - deep-learning
  - embeddings
draft: false
---

If you've ever wondered how modern AI systems mathematically "understand" text, the secret lies in embeddings. At their core, embeddings are dense, continuous vector representations of discrete data—like words, phrases, or even entire documents. While we often rely on pre-trained models from OpenAI or HuggingFace in production setups, building one from scratch is one of the most effective ways to truly grasp what happens under the hood.

In this guide, we'll explore three foundational architectures you can build to generate embeddings, progressing from classical methods to modern deep learning techniques.

### The Classic Approach: Word2Vec
Word2Vec is arguably the model that popularized dense vector embeddings. Rather than relying on massive, complex LLMs, Word2Vec uses a remarkably shallow neural network to learn word associations from a large corpus of text. 

It typically comes in two flavors:
- **Continuous Bag of Words (CBOW):** This approach looks at a window of surrounding context words and tries to predict the target word in the middle.
- **Skip-Gram:** This takes the opposite approach by using a single target word to predict the surrounding context words. Skip-gram tends to perform slightly better, especially for infrequent words.

In both cases, the goal is simple. We want to maximize the mathematical similarity (the dot product) between a word and its true context words, while actively minimizing the similarity against a set of random, "fake" context words—a technique known as Negative Sampling.

### The Compression Trick: Autoencoder Bottlenecks
Moving beyond shallow networks, we can use [[Autoencoders]] to force a neural network to learn a compressed representation of our data. 

An autoencoder is designed to reconstruct its own input. However, its architecture intentionally includes a low-dimensional hidden layer in the middle—a "bottleneck." By passing the input through an encoder network, compressing it into this bottleneck, and then forcing a decoder network to reconstruct the original data, the model must learn to preserve the most essential meaning (the latent features).

Once the model is trained, we simply throw away the decoder. That bottleneck layer? Those are our embeddings.

### The Modern RAG Workhorse: Siamese Networks
If you are building an application that uses Retrieval-Augmented Generation (RAG) or semantic search, you'll likely encounter Dual Encoders, also known as Siamese Networks.

Instead of predicting a context word or reconstructing an input, a Siamese Network uses two identical twin networks that share the exact same weights. You pass two distinct items—for example, a "search query" and a "document"—through the network to generate two separate embedding vectors. 

During training, the network is penalized using Contrastive Loss if matching query-document pairs end up with dissimilar vectors. Over time, the model learns a beautiful semantic space where related concepts live close to one another, which you can easily measure using cosine similarity.

---

### Hands-On: A PyTorch Skip-Gram from Scratch

Concepts are great, but seeing the code provides a much better intuition. Here is a minimal implementation of the Skip-Gram architecture using PyTorch. Notice how we rely on `nn.Embedding` as simple lookup tables for our word vectors.

```python
import torch
import torch.nn as nn

class SkipGramModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super(SkipGramModel, self).__init__()
        # Lookup table for the target word vectors
        self.target_embeddings = nn.Embedding(vocab_size, embedding_dim)
        # Lookup table for the context word vectors
        self.context_embeddings = nn.Embedding(vocab_size, embedding_dim)

    def forward(self, target_idx, context_idx):
        # 1. Fetch embeddings for our given word indices
        u = self.target_embeddings(target_idx) # Shape: [batch_size, embedding_dim]
        v = self.context_embeddings(context_idx) # Shape: [batch_size, embedding_dim]
        
        # 2. Compute the dot product between target and context vectors
        # A higher score means the network predicts a higher probability of them co-occurring.
        score = torch.sum(u * v, dim=1)
        return score

# -- Example usage in a training loop --
vocab_size = 10000
embedding_dim = 128
model = SkipGramModel(vocab_size, embedding_dim)

# Dummy inputs simulating a batch of 4 word pairs (target word, context word)
target_words = torch.tensor([10, 42, 54, 98])
context_words = torch.tensor([15, 6, 88, 12])

# Forward pass to get similarity scores
scores = model(target_words, context_words)

# To train this, you would pass these scores to a loss function like BCEWithLogitsLoss 
# along with positive (1) and negative (0) sampled labels.
print("Similarity scores:", scores)
```

### Where to Go from Here

- **[The Illustrated Word2vec (Jay Alammar)](http://jalammar.github.io/illustrated-word2vec/):** An incredibly visual explanation of how Word2Vec and its embeddings are mathematically constructed and trained.
- **[PyTorch Official NLP Tutorial - Word Embeddings](https://pytorch.org/tutorials/beginner/nlp/word_embeddings_tutorial.html):** A step-by-step programmatic tutorial on building CBOW and N-Gram models from scratch.
- **[Andrej Karpathy's "Makemore" Series (YouTube)](https://www.youtube.com/watch?v=PaCmpygFfXo):** A foundational video series leading you through building an autoregressive character-level language model from absolute scratch, including the embedding lookups.
- **[Sentence-Transformers Documentation (sbert.net)](https://www.sbert.net/):** Your next stop after mastering word-level embeddings. Learn how Siamese networks are used to create dense vector representations for entire sentences.