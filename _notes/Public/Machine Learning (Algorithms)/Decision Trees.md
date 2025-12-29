---
title: Decision Trees
---
# Decision Trees

| Type                       |
| -------------------------- |
| Classification, Regression |

Decision Trees are non-parametric supervised learning methods used for classification and regression. They use a tree-like graph of decisions to predict the value of a target variable.

**Decision Tree Algorithms**
- CART
- C4.5
- C5.0
### Key Components
- **Nodes:** Represent a test on an attribute (feature).
- **Branches:** Represent the outcome of the test.
- **Leaves:** Represent the final class label or value.
### Building the Tree (Recursive Partitioning)
The goal is to partition data into subsets that are as "pure" as possible.
- **Information Gain:** Measures the reduction in **Entropy** (disorder) after a split. Higher gain is better.
- **Gini Impurity:** A measure of how often a randomly chosen element would be incorrectly labeled. Used frequently in the CART algorithm.
- **Splitting Criteria:** At each node, the algorithm selects the feature and split point that maximizes purity in the resulting child nodes.
### Overfitting and Pruning
Decision trees can easily overfit by becoming too deep and capturing noise.
- **Pre-pruning:** Stop growing the tree early (e.g., limit depth or minimum samples per leaf).
- **Post-pruning:** Grow the full tree and then remove nodes that provide little predictive power.

| **Feature**    | **Decision Trees**          | **Boosting**                       |
| -------------- | --------------------------- | ---------------------------------- |
| **Model Type** | Single base learner         | Ensemble of learners               |
| **Training**   | Fast, recursive             | Sequential, slower                 |
| **Complexity** | Easy to interpret           | High predictive power, "black box" |
| **Variance**   | High (prone to overfitting) | Reduced via iterative refinement   |
