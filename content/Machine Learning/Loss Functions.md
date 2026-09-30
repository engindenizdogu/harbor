---
title: Loss Functions
tags:
  - machine-learning
  - model-evaluation
draft: false
---
In machine learning, **loss functions** (or cost functions) are mathematical formulas used to measure the difference between a model's predicted output and the actual target values. The model uses this error metric during training to update its weights and improve its accuracy. 

The choice of loss function depends primarily on the type of task: **Regression** or **Classification**.

## 1. Regression Loss Functions
Used when the goal is to predict a continuous numerical value (e.g., price, temperature).

- **Mean Squared Error (MSE / L2 Loss):** 
  - **What it is:** The average of the squared differences between predicted and actual values.
  - **Pros/Cons:** It penalizes larger errors more heavily because of the squaring. It is very common but highly sensitive to outliers.
- **Mean Absolute Error (MAE / L1 Loss):** 
  - **What it is:** The average of the absolute differences between predicted and actual values.
  - **Pros/Cons:** Generally more robust to outliers than MSE.
- **Huber Loss:** 
  - **What it is:** A combination of MSE and MAE. It acts like MSE when errors are small and like MAE when errors are large.
  - **Pros/Cons:** Less sensitive to outliers than MSE while remaining differentiable at zero.

## 2. Classification Loss Functions
Used when the goal is to categorize data points into discrete classes (e.g., spam vs. not spam).

- **Cross-Entropy Loss (Log Loss):** 
  - **What it is:** The most common loss function for classification models that output probability values between 0 and 1.
  - **Variants:** **Binary Cross-Entropy** for two classes, and **Categorical Cross-Entropy** for multi-class problems.
- **Hinge Loss:** 
  - **What it is:** Designed for "maximum margin" classification, primarily used with [[Support Vector Machines]] (SVMs).
  - **Pros/Cons:** Penalizes predictions that fall on the wrong side of the decision boundary or within the margin.
- **Kullback-Leibler (KL) Divergence:** 
  - **What it is:** Measures how one probability distribution differs from a reference probability distribution. Often used in specific neural network architectures.

---
*Source: Synthesized from [BuiltIn](https://builtin.com/machine-learning/common-loss-functions), [DataCamp](https://www.datacamp.com), and [IBM](https://www.ibm.com) technical documentation.*
