---
title: Keyword Extraction & Topic Modelling
---
# Keyword Extraction & Topic Modelling Libraries
1. **Keyword Extraction**
	1. TF
	2. TF-IDF
	3. RAKE ([rake-keyword](https://github.com/u-prashant/RAKE), [python-rake](https://github.com/fabianvf/python-rake))
	4. YAKE ([yake](https://github.com/LIAAD/yake))
	5. KeyBERT ([KeyBERT](https://github.com/MaartenGr/KeyBERT))
	6. Spacy
	7. [Spark NLP](https://sparknlp.org/)
2. **Topic Modelling** - *Topic modelling requires a large collection of text documents to work, not very suitable for extracting topics from single sentences, paragraphs or tweets etc.*
	1. Latent Dirichlet Allocation (LDA)
	2. BERTopic
	3. Non-Negative Matrix Factorization (NMF)

> **Zero-shot classification** can also be an option, however it requires a list of predefined keywords or tags.

> **Alternative approach:** Using LLMs (could be local, LLMs could be better understanding context compared to the libraries above)

**List of approaches:**

| Method                         | Supervised/Unsupervised | Description                                                   | Notes                                                                           |
| ------------------------------ | ----------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| ==Keyword Extraction==         | ==Unsupervised==        | ==Extracts important words/phrases directly from text==       | ==Algorithms: RAKE, YAKE, KeyBERT, TF-IDF==                                     |
| ==Topic Modeling==             | ==Unsupervised==        | ==Discovers hidden themes across document **collections**==   | ==Algorithms: LDA, NMF, BERTopic==                                              |
| Zero-Shot Classification       | Unsupervised            | Classifies text into predefined categories without training   | Requires candidate labels but no training data                                  |
| ==Generative Tagging==         | ==Unsupervised==        | ==Uses LLMs to generate tags from scratch==                   | ==GPT, Claude, local LLMs; no predefined labels needed==                        |
| Semantic Similarity Matching   | Unsupervised            | Matches text to tags using embedding similarity               | Uses sentence transformers; requires tag vocabulary                             |
| ~~Rule-Based Tagging~~         | ~~Unsupervised~~        | ~~Uses predefined patterns and rules~~                        | ~~If text contains "python" or "javascript" → tag as "programming"~~            |
| Clustering                     | Unsupervised            | Groups similar documents, then manually labels clusters       | K-means, DBSCAN, Hierarchical clustering                                        |
| Graph-Based Methods            | Unsupervised            | Uses text as graph (words as nodes, co-occurrence as edges)   | TextRank, LexRank for keyword extraction                                        |
| Taxonomy Learning              | Unsupervised            | Automatically builds hierarchical tag structures              | Discovers parent-child relationships between tags                               |
| Co-occurrence Analysis         | Unsupervised            | Finds words/phrases that frequently appear together           | Useful for discovering tag relationships                                        |
| Prompt Engineering             | Unsupervised            | Carefully crafted prompts to guide LLM tagging                | No training but requires prompt iteration                                       |
| Lexicon-Based Methods          | Unsupervised            | Uses predefined dictionaries/wordlists for categories         | If text contains "goal", "score", "team" → sports                               |
| Named Entity Recognition (NER) | Supervised/Unsupervised | Identifies specific entities (people, places, organizations)  | Can use pre-trained models (unsupervised) or custom-trained                     |
| Supervised Text Classification | Supervised              | Traditional ML trained on labeled examples                    | Requires 1000+ labeled examples; methods: Naive Bayes, SVM, Logistic Regression |
| Fine-tuned Transformers        | Supervised              | Neural models (BERT, RoBERTa) trained on your specific data   | Best accuracy but requires significant labeled data (5000+)                     |
| Multi-label Classification     | Supervised              | Assigns multiple tags per document simultaneously             | Binary Relevance, Classifier Chains, Label Powerset                             |
| Transfer Learning              | Supervised              | Uses pre-trained model, fine-tunes on small dataset           | Requires only 100-500 labeled examples                                          |
| Attention-Based Tagging        | Supervised              | Neural network learns which parts of text matter for each tag | Modern approach; part of transformer models                                     |
| Few-Shot Learning              | Semi-supervised         | Learns from just a few examples per category                  | Needs 5-50 examples per tag; uses models like SetFit                            |
| Active Learning                | Semi-supervised         | Iteratively asks human to label most informative examples     | Reduces labeling effort by 50-80%                                               |
| Weak Supervision               | Semi-supervised         | Uses noisy/programmatic labels instead of manual labels       | Tools: Snorkel; combines heuristics and patterns                                |
| Contrastive Learning           | Semi-supervised         | Learns by comparing similar vs dissimilar examples            | Good when you have unlabeled data + some labels                                 |
| Ensemble Methods               | Either                  | Combines multiple tagging approaches                          | Vote/average results from different methods for better accuracy                 |
