---
title: Scripts
---
```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.neural_network import MLPClassifier

# Vectorize training set
counter = CountVectorizer(min_df=10, max_df=20)
counter.fit(X_train_text)
print("Vocabulary size:", len(counter.vocabulary_))

# Transform X_train to X_train_counts
X_train_counts = counter.transform(X_train_text)
print(X_train_counts.shape)

# TF-IDF fit and transform
count2tfidf = TfidfTransformer(use_idf=True).fit(X_train_counts)
X_train = count2tfidf.transform(X_train_counts).toarray()
print(X_train.shape)
```