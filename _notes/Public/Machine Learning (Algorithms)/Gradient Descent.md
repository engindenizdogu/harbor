---
title: Gradient Descent
---
# Gradient Descent

| Type         |
| ------------ |
| Optimization |

**Definition:** Gradient is the direction of the steepest ascent (by definitions). [Why the gradient is the direction of steepest ascent?](https://www.khanacademy.org/math/multivariable-calculus/multivariable-derivatives/gradient-and-directional-derivatives/v/why-the-gradient-is-the-direction-of-steepest-ascent)

> Some information on gradient descent can also be found on [[Linear Regression]].

**Weight update rule:**

$$ w:= w - \alpha * \bigtriangledown L(w) $$

**Why do we go in the opposite direction of the gradient?**
The gradient tells the direction of steepest _ascent_ of the loss. We go in the opposite direction because that is the direction that minimizes error.

> **IMPORTANT NOTE:**
> Only a handful of ML problems have closed-form solutions such as Linear Regression, Ridge Regression (Linear Regression with L2 Regularization), Linear Discriminant Analysis, some simple Bayesian models etc. Most problems do NOT have a closed form solution, hence we need to solve using iterative optimization algorithms like gradient descent. Examples to problems without closed form solutions: Logistic Regression, Neural Networks, Support Vector Machines etc.

> Also see: [The Misconception that Almost Stopped AI](https://www.youtube.com/watch?v=NrO20Jb-hy0)

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