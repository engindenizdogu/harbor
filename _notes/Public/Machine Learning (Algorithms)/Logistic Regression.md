---
title: Logistic Regression
---
# Logistic Regression

| Type              |
| ----------------- |
| Linear Classifier |

Usually performs better than these linear classifiers:
- [[Least-Square Classification]]
- [[Fisher's Linear Discriminant]]
- [[Rosenblatt's Perceptron]]
- [[Support Vector Machines]]

---

**Logistic Regression (LR)** is a fundamental classification algorithm used in machine learning to predict discrete outcomes. Unlike generative models that model feature distributions, Logistic Regression is a **discriminative model** that directly learns the probability of a label $y$ given the features $x$, denoted as $P(y=k\vert x)$. It utilizes specific activation functions: **Sigmoid** for binary cases and **Softmax** for multi-class cases to map real-valued inputs into normalized probability scores.

---

### Classification Mechanisms
- **Binary Logistic Regression ($K=2$):** 
    - Uses the **Sigmoid function** $\sigma(w^Tx) = \frac{1}{1+e^{-w^Tx}}$ to estimate the probability of the positive class ($y=1$).
    - The output ranges between 0 and 1.
    - **Decision Boundary:** By selecting a threshold of 0.5, the decision boundary simplifies to $w^{\top}x = 0$, which is linear with respect to $x$.
- **Multi-class Logistic Regression ($K>2$):**
    - Uses the **Softmax function** to ensure the sum of probabilities across all $K$ classes equals 1.
    - Calculation involves two steps: computing the inner product $f_k = w_k^{\top}x$ for each class, then applying the softmax to get normalized probabilities.

### Optimization and Loss Functions
- **Cross-Entropy Loss:** The model is optimized by maximizing the likelihood (or minimizing the negative log-likelihood) of the correct class. This is equivalent to minimizing the cross-entropy between the true distribution (one-hot encoded labels) and the predicted distribution.
- **Gradient Descent:** A first-order optimization algorithm that iteratively updates model parameters $w$ by moving in the direction of the negative gradient.
    - **Batch Gradient Descent:** Calculates the gradient using the entire training dataset.
    - **Stochastic Gradient Descent (SGD):** Updates parameters based on a single randomly chosen training example, providing an online update solution but with higher variance.
    - **Mini-batch Gradient Descent:** A trade-off that calculates the gradient on a small random subset of data, offering more stable convergence and better computational efficiency via matrix optimization.

---

### Regularization
- **Purpose:** A technique used to prevent **overfitting** by penalizing large model coefficients.
- **L2 Regularization:** Adds an L2 norm penalty term ($\lambda \sum \vert \vert w \vert \vert^2$) to the loss function.
- **Hyperparameter $\lambda$:** Controls the strength of regularization; the optimal value is typically chosen using a validation set.

> **The Intuition of Cross-Entropy**
> 
> In information theory, cross-entropy measures the "distance" between two probability distributions18. In Logistic Regression, we want our predicted probability distribution to be as close as possible to the "ground truth" (where the correct class has a probability of 1 and all others 0).

> **Why use Mini-batches?**
> 
> While SGD is fast, its path to the minimum is "noisy" due to high variance. Mini-batching strikes a balance: it's faster than Batch GD because you don't wait for the whole dataset, but smoother than SGD because the average gradient of a batch is a more reliable estimate than a single point.

