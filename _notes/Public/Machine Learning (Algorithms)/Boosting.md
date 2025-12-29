---
title: Boosting
---
# Boosting

| Type               |
| ------------------ |
| Ensemble Technique |

Boosting is an ensemble technique that combines multiple "weak learners" (models that are only slightly better than random guessing) into a single "strong learner." Unlike [[Bagging]] (which trains models in parallel), Boosting trains models **sequentially**. Each new model attempts to correct the errors made by the previous models by focusing more on the misclassified data points.
### AdaBoost (Adaptive Boosting)
- **Weighted Data:** Each training instance is assigned a weight.
- **Iterative Correction:** After a model is trained, the weights of incorrectly classified instances are increased, while the weights of correctly classified instances are decreased.
- **Final Prediction:** The final output is a weighted sum of all the weak learners' predictions.
### Gradient Boosting
- **Residuals:** Instead of adjusting weights, Gradient Boosting trains the next model on the **residual errors** (the difference between predicted and actual values) of the previous model.
- **Gradient Descent:** It optimizes a loss function by adding models that point in the negative gradient direction.
