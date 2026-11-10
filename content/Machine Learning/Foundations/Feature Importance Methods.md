---
title: Feature Importance Methods
tags: [machine-learning, feature-importance, interpretability, explainability, auto-captured]
draft: false
---
**Feature importance** measures how much a trained model relies on each input feature. It is used to explain models, debug them, and guide [[Feature Selection Methods|feature selection]]. Different methods answer slightly different questions, so they often disagree.

## Comparison
| Method | What it measures | Model | Data used | Main weakness |
|---|---|---|---|---|
| **Coefficient magnitude** | size of $\lvert\beta\rvert$ | linear / logistic | training | linear effects only; needs standardized features |
| **Impurity (tree) importance** | total impurity reduction from splits on the feature | trees, forests, boosting | training | biased toward high-cardinality features |
| **Permutation importance** | score drop when the feature is shuffled | any | held-out | weak with correlated features |
| **SHAP values** | each feature's contribution to each prediction | any (fast for trees) | any | slow for non-tree models; credit split among correlated features |

## Coefficient Magnitude
Rank features by $\lvert\beta_j\rvert$ in linear or logistic regression.
- **Standardize first:** a coefficient's size depends on the feature's units.
- **Sign gives direction.** In logistic regression $e^{\beta_j}$ is the odds ratio for a one-unit (one-standard-deviation, after scaling) increase.
- **L1 regularization** pushes weak coefficients to exactly zero, which turns this into embedded selection (see [[Regularization]]).
- **Limits:** captures linear effects only, and coefficients become unstable when features are correlated.

## Impurity-Based (Tree) Importance
For each feature, sum the impurity reduction (Gini, entropy, or variance) over all splits that use it, weighted by the number of samples reaching the split, average over trees, and normalize to sum to 1. In scikit-learn this is `feature_importances_`.
- **Pros:** free after training; captures nonlinearity and interactions.
- **Cons:** biased toward continuous or high-cardinality features (a random ID column can score high); computed on training data, so it rewards overfitting; splits importance among correlated features.
- Boosting libraries (XGBoost, LightGBM) offer variants: **gain** (impurity reduction), **split count** (how often a feature is used), and **cover** (samples affected).

## Permutation Importance
Shuffle one feature's column in held-out data and measure how much the score drops. A large drop means the model depends on that feature.
- **Pros:** model-agnostic, uses unseen data, no cardinality bias.
- **Cons:** with correlated features, a partner feature compensates and shuffling creates unrealistic rows; costs one scoring pass per feature per repeat. Values near zero or negative mean the feature is noise to the model.
- **Tool:** `sklearn.inspection.permutation_importance(model, X_test, y_test, n_repeats=10)`.

## SHAP Values
**SHAP** (SHapley Additive exPlanations) applies Shapley values from cooperative game theory. A feature's contribution to one prediction is its average marginal effect over all subsets of the other features, and the contributions plus a baseline sum exactly to the prediction:

$$f(x)=\phi_0+\sum_{j=1}^{p}\phi_j$$

- **Local and global:** each prediction gets its own explanation; global importance is mean $\lvert\phi_j\rvert$, and beeswarm plots show direction and spread.
- **Algorithms:** TreeSHAP is exact and fast for tree models; KernelSHAP is model-agnostic but slow.
- **Caveats:** explains the model, not causality; correlated features split credit; results depend on how "missing" features are simulated.
- **Tool:** the separate [`shap`](https://shap.readthedocs.io/) package (not part of scikit-learn).

## Example: Breast Cancer Dataset
A random forest on 569 samples and 30 features, with a held-out test set:

| Rank | Impurity importance | Permutation importance (ROC-AUC drop) |
|---|---|---|
| 1 | `worst perimeter` 0.14 | `worst concave points` 0.007 |
| 2 | `worst concave points` 0.13 | `worst radius` 0.005 |
| 3 | `worst radius` 0.12 | `worst area` 0.004 |

The permutation values are tiny because radius, perimeter and area are near-duplicates of each other: shuffling one barely hurts the model, since the others carry the same information. This is the correlated-feature weakness in action.

## Practical Rules
1. **Cross-check methods.** High impurity importance with near-zero permutation importance suggests overfitting or cardinality bias.
2. **Handle correlated features first** (drop or group them) before reading importances.
3. **Use held-out data** for permutation importance and SHAP.
4. **Importance is not causation.** It describes what the model uses, not what drives the outcome.

## Related Notes
- [[Feature Selection Methods]]: filter, wrapper and embedded selection.
- [[Regularization]]: L1 coefficients as embedded selection.
- [[Random Forest]]: the ensemble behind impurity importance.

*Source: [scikit-learn: Permutation feature importance](https://scikit-learn.org/stable/modules/permutation_importance.html); [Lundberg and Lee, A Unified Approach to Interpreting Model Predictions (2017)](https://arxiv.org/abs/1705.07874)*
