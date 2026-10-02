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
  - **Variants:** **Binary Cross-Entropy** for two classes, and **Categorical Cross-Entropy** for multi-class problems. See [[#3. Cross-Entropy in Depth]] below.
- **Hinge Loss:** 
  - **What it is:** Designed for "maximum margin" classification, primarily used with [[Support Vector Machines]] (SVMs).
  - **Pros/Cons:** Penalizes predictions that fall on the wrong side of the decision boundary or within the margin.
- **Kullback-Leibler (KL) Divergence:** 
  - **What it is:** Measures how one probability distribution differs from a reference probability distribution. Often used in specific neural network architectures.

## 3. Cross-Entropy in Depth

### The Intuition
Cross-entropy compares two probability distributions: the **true distribution** $p$ (the labels) and the **predicted distribution** $q$ (the model's output). It measures how many "nats" (or bits, with $\log_2$) of surprise the model experiences when the true outcome occurs.

$$H(p, q) = -\sum_{x} p(x)\,\log q(x)$$

- A confident, correct prediction gives a loss near **0**.
- A confident, wrong prediction gives a very large loss, since $-\log q \to \infty$ as $q \to 0$.
- It is tied to KL divergence: $H(p, q) = H(p) + D_{KL}(p \,\|\, q)$. Because the label entropy $H(p)$ is constant, minimizing cross-entropy is the same as minimizing KL divergence, which equals maximum likelihood estimation.

| Predicted probability of the true class | Loss $-\ln q$ | Reading |
|---|---|---|
| 0.99 | 0.010 | Confident and right |
| 0.90 | 0.105 | Good |
| 0.50 | 0.693 | Coin flip |
| 0.10 | 2.303 | Bad |
| 0.01 | 4.605 | Confident and wrong |

### Binary Cross-Entropy (BCE / Log Loss)
Used when there are **two classes** and the model outputs a single probability $\hat{y} = P(y=1)$, usually through a **sigmoid** $\sigma(z) = \frac{1}{1+e^{-z}}$.

$$L = -\big[\,y\,\ln(\hat{y}) + (1-y)\,\ln(1-\hat{y})\,\big]$$

Since $y$ is either 0 or 1, only one term is ever active:

$$L = \begin{cases} -\ln(\hat{y}) & \text{if } y = 1 \\ -\ln(1-\hat{y}) & \text{if } y = 0 \end{cases}$$

Averaged over a batch of $N$ samples:

$$J = -\frac{1}{N}\sum_{i=1}^{N}\big[\,y_i\ln(\hat{y}_i) + (1-y_i)\ln(1-\hat{y}_i)\,\big]$$

**Worked example (spam detection).** Three emails, label 1 = spam:

| Email | True $y$ | Predicted $\hat{y}$ | Loss |
|---|---|---|---|
| A | 1 | 0.9 | $-\ln 0.9 = 0.105$ |
| B | 0 | 0.2 | $-\ln 0.8 = 0.223$ |
| C | 1 | 0.6 | $-\ln 0.6 = 0.511$ |

Batch loss: $\frac{0.105 + 0.223 + 0.511}{3} \approx 0.280$. Email C is the least certain, so it contributes the most.

**Where it is used:** [[Logistic Regression]], binary classifiers (fraud, churn, disease present or absent), GAN discriminators, and **multi-label** classification, where each label gets its own sigmoid and its own BCE term (a movie can be both "comedy" and "romance").

### Categorical Cross-Entropy (Multi-Class)
Used when there are $C$ **mutually exclusive classes**. The model outputs raw scores (**logits**) $z$, which a **softmax** turns into a probability distribution:

$$\hat{y}_c = \text{softmax}(z)_c = \frac{e^{z_c}}{\sum_{j=1}^{C} e^{z_j}}$$

The label is a **one-hot** vector $y$ (1 for the true class, 0 elsewhere), so the sum collapses to a single term:

$$L = -\sum_{c=1}^{C} y_c \ln(\hat{y}_c) = -\ln(\hat{y}_{\text{true}})$$

Averaged over a batch:

$$J = -\frac{1}{N}\sum_{i=1}^{N}\sum_{c=1}^{C} y_{i,c}\ln(\hat{y}_{i,c})$$

**Worked example (image classification).** Classes: cat, dog, bird. The true class is **dog**, so $y = [0, 1, 0]$. The network outputs logits $z = [1.0,\ 2.0,\ 0.1]$.

1. Exponentiate: $[e^{1.0}, e^{2.0}, e^{0.1}] = [2.718,\ 7.389,\ 1.105]$, sum $= 11.212$
2. Softmax: $\hat{y} = [0.242,\ 0.659,\ 0.099]$
3. Loss: $L = -\ln(0.659) \approx 0.417$

Had the model instead predicted $[0.7,\ 0.2,\ 0.1]$ (confident in cat), the loss would be $-\ln(0.2) \approx 1.609$, nearly 4 times larger.

**Gradient:** softmax combined with cross-entropy has a very clean gradient with respect to the logits, $\frac{\partial L}{\partial z_c} = \hat{y}_c - y_c$. For the example above that is $[0.242,\ -0.341,\ 0.099]$: push the dog logit up and the others down. This is a big reason the pair is so common, and why gradients stay healthy even when predictions are badly wrong.

### Choosing the Right Variant

| Task | Output layer | Loss | Label format |
|---|---|---|---|
| Binary (spam or not) | 1 unit, sigmoid | Binary cross-entropy | 0 or 1 |
| Multi-class, one label per sample | $C$ units, softmax | Categorical cross-entropy | One-hot, e.g. `[0, 1, 0]` |
| Multi-class, integer labels | $C$ units, softmax | Sparse categorical cross-entropy | Class index, e.g. `1` |
| Multi-label (several can be true) | $C$ units, sigmoid each | Binary cross-entropy per class | Multi-hot, e.g. `[1, 0, 1]` |

*Sparse* categorical cross-entropy computes the same value as the one-hot version; it only saves memory by storing the class index.

### In Practice
- **Use logits, not probabilities, with the fused loss.** In PyTorch, `nn.CrossEntropyLoss` expects raw logits and applies log-softmax internally; `nn.BCEWithLogitsLoss` does the same for sigmoid. This is more numerically stable than computing softmax or sigmoid first and then taking the log.
- **Avoid $\log(0)$.** Libraries clip probabilities to a small epsilon, such as $10^{-7}$, when you pass in probabilities directly.
- **Class imbalance:** pass per-class weights (`weight=` or `pos_weight=` in PyTorch), or use focal loss, which down-weights easy examples.
- **Label smoothing:** replace the hard one-hot target with something like $[0.05,\ 0.9,\ 0.05]$ to reduce overconfidence.

```python
import torch, torch.nn as nn

# Multi-class: logits for (cat, dog, bird), true class = dog (index 1)
logits = torch.tensor([[1.0, 2.0, 0.1]])
target = torch.tensor([1])
print(nn.CrossEntropyLoss()(logits, target))   # tensor(0.4170)

# Binary: one logit per sample, target is 0.0 or 1.0
logit = torch.tensor([2.1972])                 # sigmoid -> 0.9
print(nn.BCEWithLogitsLoss()(logit, torch.tensor([1.0])))  # tensor(0.1054)
```

### References for Cross-Entropy
- Goodfellow, Bengio and Courville, [Deep Learning, Chapter 6: Deep Feedforward Networks](https://www.deeplearningbook.org/contents/mlp.html): cross-entropy as negative log-likelihood, and softmax output units.
- Wikipedia, [Cross-entropy](https://en.wikipedia.org/wiki/Cross-entropy): the identity $H(p,q) = H(p) + D_{KL}(p\|q)$, the link to maximum likelihood, and the logistic regression loss.
- Stanford CS231n, [Linear classification: Softmax classifier](https://cs231n.github.io/linear-classify/): softmax and cross-entropy walkthrough with numeric examples.
- PyTorch, [CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html): expects unnormalized logits; supports `weight` and `label_smoothing`.
- PyTorch, [BCEWithLogitsLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html): sigmoid and BCE fused for numerical stability; supports `pos_weight`.

---
*Source: Synthesized from [BuiltIn](https://builtin.com/machine-learning/common-loss-functions), [DataCamp](https://www.datacamp.com), and [IBM](https://www.ibm.com) technical documentation.*
