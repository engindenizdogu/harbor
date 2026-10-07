---
title: Machine Learning MOC
tags: [machine-learning, moc, dashboard]
draft: false
---
Welcome to the Machine Learning Map of Contents. This dashboard organizes notes logically to provide structured learning paths and rapid discovery.

## Foundations
Core vocabulary, problem types, and evaluation, located in the `Foundations/` directory.
- [[Glossary]] - Foundational machine learning definitions (Bias, Variance, etc.).
- [[Machine Learning Domains]] - Breakdown of ML problem types (Classification, Regression, Unsupervised).
- [[Metrics and Model Evaluation]] - Guide on evaluating models, bias/variance tradeoff, and regularization.
- [[Clustering Evaluation Metrics]] - Purity, Rand Index, Adjusted Rand Index, NMI, and silhouette for judging clusters.
- [[Loss Functions]] - How models measure error (MSE, Cross-Entropy).
- [[Exploratory Data Analysis]] - The crucial first step of inspecting and understanding your data.
- [[Scaling Techniques]] - Methods for normalization and when to use them.

## Math for Machine Learning
Mathematical foundations, located in the `Math/` directory.
- [[0. Glossary (ML Math)]]
- [[1. Probability]]
- [[2. Linear Algebra]]
- [[3. Calculus]]
- [[4. Bayesian Decision Theory]]
- [[5. Determinants]]
- [[6. Fourier Transform]]
- [[7. Chaos Theory]]
- [[8. Law of Large Numbers]]
- [[9. Vector Calculus]]
- [[10. Vector Norms]]

## Classical ML
Deep dives into specific algorithms, located in the `Classical ML/` directory.

### Linear & Parametric Models
- [[Linear Classifiers]] - Hyperplanes and decision boundaries.
- [[Linear Regression]]
- [[Logistic Regression]]
- [[Polynomial Regression]]
- [[Least-Square Classification]]
- [[Fisher's Linear Discriminant]]
- [[Rosenblatt's Perceptron]]
- [[Gradient Descent]]

### Tree-Based & Ensemble Methods
- [[Decision Trees]] - Gini splits, pruning, and a worked Iris example with tree visualization.
- [[Random Forest]]
- [[Bagging]]
- [[Boosting]]

### Support Vector Machines & Non-Parametric
- [[Support Vector Machines]]
- [[k-Nearest Neighbors]]

### Bayesian Methods
- [[Bayesian Decision Methods]]
- [[Bayesian Networks]]

### Unsupervised Learning (Clustering & PCA)
- [[k-Means]] - Centroid-based clustering, with a worked Iris example and evaluation.
- [[Hierarchical Clustering]]
- [[Locally Adaptive Clustering (LAC)]]
- [[Mixtures of Gaussians]]
- [[Principal Component Analysis (PCA)]]
- [[Singular Value Decomposition]]
- [[Self-organizing Map]]

## Deep Learning
Neural network fundamentals and architectures, located in the `Deep Learning/` directory. Sequence models and Transformers live under [[Natural Language Processing MOC]]; VAEs and GANs under [[Generative AI MOC]].
- [[Neural Networks]] - MLP architecture, backpropagation, and training challenges.
- [[Activation Functions]] - Non-linearities and when to use them.
- [[Batch Normalization]] - Stable gradients and faster convergence.
- [[Convolutional Neural Networks]] - Forward pass, backpropagation through convolutional and pooling layers.
- [[Autoencoders]] - Bottleneck architectures, reconstruction loss, and latent spaces.
- [[Keras vs. PyTorch vs. TensorFlow]] - Framework comparison.
- [[Keras Data Generators]] - Memory-efficient on-the-fly data generation with `keras.utils.Sequence`.

## Reinforcement Learning
Detailed domain dashboard: [[Reinforcement Learning MOC]]
- [[Reinforcement Learning]] - The agent-environment interaction loop.
- [[Markov Decision Processes]] - Mathematical framework (States, Actions, Transitions).
- [[Q-Learning]] - Off-policy value-based learning.
- [[Deep Reinforcement Learning]] - Scaling RL with Neural Networks.
- [[Dynamic Programming]] - The foundational framework for solving MDPs.

## Applications
Located in the `Applications/` directory.
- [[Recommendation Systems]]
- [[Learning To Rank]]
- [[Anti-Bot Machine Learning]] - How ML is used to detect and mitigate automated agents.

## Related Domains
- [[Natural Language Processing MOC]] - Language modeling, embeddings, Transformers, and LLMs.
- [[Computer Vision MOC]] - Template matching, filtering, and resolution changes.
- [[Generative AI MOC]] - Image generation, VAEs, and GANs.
- [[Agents MOC]] - Agent memory, benchmarks, and conversational agents.

---
## To Research / Inbox
*(Drop new concepts or terms you want to research here as unlinked wiki-links, e.g., `[[Transformers]]`)*
