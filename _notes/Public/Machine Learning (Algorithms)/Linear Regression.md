---
title: Linear Regression
---
# Linear Regression

| Type       |
| ---------- |
| Regression |

**Prediction:**

$$fw(x) = y = w^Tx + \beta = w_1x + w_0$$

**Loss:**

$$L(x,y,w) = (fw(x) − y)^2$$

**Why use squared loss?**
- Makes the function convex
- Prevents errors from cancelling out
- Penalizes large errors
- Easily differentiable

**Closed Form Solution (Normal Equation)**
L2 Loss (squared loss): 

$$L2 = {1 \over N} {\sum(w^⊤x − y)^2}$$

we have (solve for ${\vartheta L(w) \over \vartheta(w)}=0$),

$$ {\vartheta L(w) \over \vartheta(w)} = X^TXw-y^TX = 0$$

Solution:

$$w^∗ =(X^TX)^−1X^Ty$$

## Gradient Descent
Update weights using ($\alpha$ is the learning rate):

$$ w:= w - \alpha * \bigtriangledown L(w) $$

where the loss function $L(w)$ is defined as (matrix form):

$$ L(w) = {2\over N} * X^T(Xw-y)$$

or (component-wise):

$$ L(w) = {2\over N} * \sum_i^n (x_i*w_i - y_i)x_i$$

> **Note: $\bigtriangledown L(w)$ = ${\vartheta L(w) \over \vartheta(w)}$** 

**Gradient Descent Options:**
- **(Batch) Gradient Descent** (calculate for all of the training set X at once)
	- Can be very slow
	- Datasets may not fit in memory
	- Doesn’t allow online (on-the-fly) model updates
	- Guaranteed to converge to the global minimum for convex error surfaces and to a local minimum for non-convex surfaces
- **Stochastic Gradient Descent** (shuffle X and evaluate one row at a time, check for stopping condition)
	- Allow for online update with new examples
	- With a high variance that cause the objective function to fluctuate heavily
- **Mini Batch Gradient Descent** (use mini batches instead of evaluating one row at a time, check for stopping condition)
	- Reduces the variance of the parameter/model updates, which can lead to more stable convergence
	- Can make use of highly optimized matrix optimizations
* Adaptive learning rates (see AdaGrad algorithm)

> **Note:** Closed form solution can be very slow with datasets that have many rows

## L1/L2 Regularization (LASSO/Ridge Regression)
- L2:
	- sum-of-squares error + $\alpha w^Tw$
	- Can calculate the closed form solution 
	- Can use it with gradient descent
	- Do not generally regularize the bias term
	- Handles multicollinearity well

- L1:
	- sum-of-squares error + $\alpha \vert w \vert$
	- Non-zero coefficients indicate important features
	- Must use iterative methods (no closed form solution)

Use L1 when:
- You have many features and suspect most are irrelevant
- You want interpretable models with feature selection
- You need to identify the most important predictors

Use L2 when:
- Most features are potentially useful
- You want stable coefficient estimates
- Computational efficiency is important
- Features are highly correlated