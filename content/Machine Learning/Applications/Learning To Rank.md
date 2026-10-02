---
title: Learning To Rank
tags:
  - machine-learning
  - learning-to-rank
  - recommendation-systems
  - search
draft: false
---
Learning to Rank (LTR) is a class of supervised machine learning algorithms designed to sort a list of items based on their relevance to a specific query. While classical machine learning models (like classification or regression) predict single values from a feature vector, LTR models evaluate a set of feature vectors to output an optimal ordering.

## Core Concepts

In LTR, the system receives an n-dimensional feature vector containing information about a query and a document. The goal is to learn a function that outputs a relevance score, allowing documents to be ranked such that highly relevant documents appear at the top of the search results.

Feature vectors in LTR generally incorporate:
1. **Document-only features:** e.g., document length, number of links.
2. **Query-only features:** e.g., query length, term frequency of the query.
3. **Query-document combination features:** e.g., TF-IDF, BM25, number of matching words.

### Training Data Collection

LTR relies on "ground truth" training data to teach the model what an ideal set of ranked results looks like:
- **Offline LTR:** Relies on manual annotation by human experts rating query-document pairs. It provides high-quality data but is time-consuming and expensive.
- **Online LTR:** Implicitly collects user interaction signals, such as clicks, views, or time spent on a page. While easier to scale, the data can be noisy and harder to interpret.

## Ranking Approaches

Most LTR algorithms use stochastic gradient descent to optimize ranking. Depending on how the algorithm compares items during training, there are three primary approaches:

### Pointwise Ranking

- **Mechanism:** Predicts an independent score for each document feature vector.
- **Problem Formulation:** Casts ranking as a regression or classification problem.
- **Drawbacks:** It optimizes scores independently and ignores relative document order. This means a model might achieve a lower overall loss but still display irrelevant results at the top, negatively impacting user experience. It also suffers from severe class imbalance since most documents are irrelevant to any given query.

### Pairwise Ranking

- **Mechanism:** Compares documents in pairs. The model predicts the probability that document A should be ranked higher than document B.
- **Loss Function:** Uses pairwise loss (e.g., cross-entropy on the softmax of the difference between document scores). 
- **Algorithms:** RankNet is a foundational algorithm that minimizes the number of rank inversions.
- **Drawbacks:** Optimizing for the fewest number of inversions is not always ideal. Users care most about the absolute top results. A ranking with fewer overall inversions might push a highly relevant result out of the #1 spot, which hurts user-centric metrics like nDCG.

### Listwise Ranking

- **Mechanism:** Takes entire lists of documents as input and directly optimizes ranking metrics (like nDCG or precision).
- **Algorithms:** 
  - **LambdaRank:** An extension of RankNet where the gradient "lambdas" are multiplied by the change in nDCG that would result from swapping two documents. This effectively forces the model to prioritize getting the top results right.
  - **LambdaMART:** Combines LambdaRank with gradient boosted trees. It is highly effective and widely used in practice.
  - **SoftRank:** Creates a differentiable approximation of nDCG ("SoftNDCG") so it can be optimized directly via gradient descent.

## Industry Applications

LTR is primarily used in scenarios requiring sophisticated relevancy sorting:
- **Search Engines:** Ordering web pages so the most relevant appear first.
- **[[Recommendation Systems]]:** Choosing which products or media to recommend to a user.
- **Enterprise Search:** Tools like Lucidworks Fusion leverage Apache Solr's LTR capabilities to replace manual boost/block rules with automated, machine-learned relevancy based on user behavior signals.

## References

- *Source: [Introduction to Ranking Algorithms | Towards Data Science](https://towardsdatascience.com/introduction-to-ranking-algorithms-4e4639d65b8/)*
- *Source: [The ABCs of Learning to Rank | Lucidworks](https://lucidworks.com/blog/abcs-learning-to-rank)*
