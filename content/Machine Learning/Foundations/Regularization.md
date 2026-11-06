---
title: Regularization
tags: [machine-learning, regularization, overfitting, model-evaluation, auto-captured]
draft: false
---
**Regularization** adds a preference for simpler models to training, so that a model fits the signal and not the noise. The usual form is a penalty added to the loss:

$$J(w)=\underbrace{\text{Loss}(w)}_{\text{fit the data}}+\lambda\,\underbrace{\Omega(w)}_{\text{penalty on complexity}}$$

The strength $\lambda \ge 0$ sets the trade-off. At $\lambda=0$ the model is unregularized; as $\lambda$ grows, weights are pushed toward zero.

## Why It Works
- **Overfitting** happens when a model has enough freedom to memorize noise: many features, few samples, or a flexible model. The symptom is low training error with high validation error.
- Large weights are the typical sign of a model contorting itself to fit noise (for example, a high-degree polynomial or two correlated features with huge opposite-sign weights).
- Penalizing weight size trades a little **bias** (the fit is deliberately a bit worse on training data) for a large drop in **variance** (predictions change less when the training sample changes). See [[Metrics and Model Evaluation]] for the bias-variance picture.
- Regularization is also what makes some problems solvable at all: with more features than samples, or perfectly separable classes, the unregularized solution is not unique or does not exist (see the logistic example below).

## L2 Regularization (Ridge, Weight Decay)
$$\Omega(w)=\lVert w\rVert_2^2=\sum_j w_j^2$$

- **Effect:** shrinks all weights smoothly toward zero, but rarely to exactly zero.
- **Correlated features:** splits weight among them instead of letting two features cancel each other with huge opposite weights, so it handles multicollinearity well.
- **Solution:** for linear regression there is a closed form, $w=(X^\top X+\lambda I)^{-1}X^\top y$. The added $\lambda I$ also makes $X^\top X$ invertible.
- **Gradient step:** each update multiplies the weights by $(1-\eta\lambda)$ before the usual gradient step, which is why it is called **weight decay**.

## L1 Regularization (Lasso)
$$\Omega(w)=\lVert w\rVert_1=\sum_j |w_j|$$

- **Effect:** drives some weights to **exactly zero**, which performs feature selection as a side effect and gives sparse, interpretable models.
- **Solution:** no closed form (the absolute value is not differentiable at 0), so it uses coordinate descent or proximal methods.
- **Caveat:** among a group of strongly correlated features, lasso tends to keep one arbitrarily and drop the others, and the choice can change from one sample to the next.

## Why L1 Gives Sparsity: the Geometry
Minimizing loss plus a penalty is equivalent to minimizing the loss while keeping $\Omega(w)$ below a budget. The penalty region is a **diamond** for L1 and a **circle** for L2. The best point is where the loss contours first touch the region.

![[l1-l2-regularization-geometry.png]]

The diamond has corners on the axes, and contours usually touch a corner first, where one weight is exactly zero. The circle has no corners, so the touching point has all weights non-zero. In higher dimensions the L1 region has many more corners and edges lying in coordinate subspaces, which is why many weights land at zero at once. For the underlying norms, see [[10. Vector Norms]].

## Coefficient Paths
Sweeping the penalty strength on synthetic data (120 samples, 8 features, only 3 truly informative) shows the difference directly.

![[lasso-ridge-coefficient-paths.png]]

Result at a moderate penalty (features standardized):

| Method | Noise features set to zero | Informative coefficients (true values about 98, 96, 86) |
|---|---|---|
| No penalty (OLS) | 0 of 5 (small non-zero noise weights) | 102, 85, 79 |
| Lasso, alpha = 10 | 5 of 5 | 92, 76, 70 |
| Ridge, alpha = 100 | 0 of 5 | 56, 47, 46 |

Lasso removes all five noise features and shrinks the real ones moderately. Ridge keeps every feature and shrinks all coefficients together. The penalty strengths are not comparable across methods: scikit-learn defines `alpha` differently for the two, and the plot's horizontal axes use different scalings.

## Elastic Net
$$\Omega(w)=\alpha\,\lVert w\rVert_1+(1-\alpha)\,\lVert w\rVert_2^2$$

A blend of both. It keeps lasso's sparsity but, thanks to the L2 part, handles groups of correlated features more stably (it tends to keep or drop them together). A good default when there are many correlated features and sparsity is still wanted. In scikit-learn the mix is controlled by `l1_ratio`.

## L1 vs. L2 at a Glance

| | L1 (Lasso) | L2 (Ridge) |
|---|---|---|
| Penalty | $\sum \lvert w_j\rvert$ | $\sum w_j^2$ |
| Weights | exactly zero for some | small but non-zero |
| Feature selection | built in | none |
| Correlated features | picks one, unstable | shares weight, stable |
| Closed form (linear regression) | no | yes |
| Use when | many features, most irrelevant, want interpretability | most features useful, correlated features, stability matters |

## Bayesian View
Regularization is maximum a posteriori (MAP) estimation with a prior on the weights:
- **L2** corresponds to a **Gaussian** prior: weights are believed to be small and symmetric around zero.
- **L1** corresponds to a **Laplace** prior: sharply peaked at zero, so many weights are believed to be exactly zero.

A larger $\lambda$ means a tighter prior (a stronger belief that weights are small).

## Practical Rules
1. **Scale the features first.** The penalty treats all weights alike, so a feature measured in large units gets a small weight and is barely penalized. Standardize before fitting (see [[Scaling Techniques]]).
2. **Do not penalize the intercept.** The bias term only shifts predictions and does not add complexity.
3. **Choose $\lambda$ by cross-validation**, searching on a log scale (for example 0.001 to 1000), and judge on validation data, never training data. Pick the smallest model within one standard error of the best score if you want a simpler one.
4. **Regularize the model, not the metric.** The penalty applies during training; the evaluation metric stays the same (see [[Metrics and Model Evaluation]]).

## Regularization in Logistic Regression
[[Logistic Regression]] supports both penalties. In scikit-learn, `LogisticRegression` applies **L2 by default**, and the strength is set by `C`, which is the **inverse** of $\lambda$: small `C` means strong regularization, large `C` means weak.

Example: study hours (1 to 10) against pass/fail, where the classes are perfectly separable (fail for 1 to 4 hours, pass for 5 to 10):

| `C` | Coefficient on hours | Intercept |
|---|---|---|
| 0.1 | 0.46 | -1.97 |
| 1 (default) | 1.18 | -5.31 |
| 100 | 5.65 | -25.43 |
| 1,000,000 | 11.12 | -49.92 |

As the penalty vanishes the coefficient keeps growing. For separable data the unregularized maximum-likelihood solution does not exist: a steeper sigmoid always fits slightly better, so the weights diverge. A little L2 keeps the solution finite and the probabilities sensible. For L1, use `penalty="l1"` with a solver that supports it (`liblinear` or `saga`).

## Beyond Weight Penalties
Other techniques also limit effective model complexity and are all regularization in the broad sense:
- **Early stopping:** stop training when validation loss stops improving. In gradient-based training this acts much like an L2 penalty, since weights have had less time to grow.
- **Dropout:** randomly disable neurons during training so the network cannot rely on any single unit (see [[Neural Networks]]).
- **Data augmentation:** more varied training examples reduce overfitting without touching the loss.
- **Smaller or simpler models:** fewer features, shallower trees, lower polynomial degree. See [[Polynomial Regression]] and [[Decision Trees]].
- **Weight decay vs. L2 in adaptive optimizers:** for plain SGD the two are equivalent. With Adam they are not, because the L2 gradient is rescaled by the adaptive step size. The decoupled version (AdamW) applies decay directly to the weights and is the standard choice for training transformers.

## Related Notes
- [[Linear Regression]]: the penalized forms and when to use each.
- [[Logistic Regression]]: regularization and the `C` parameter.
- [[Feature Selection Methods]]: statistical filters, the alternative to L1 for dropping features.
- [[Loss Functions]]: the loss term that the penalty is added to.
- [[10. Vector Norms]]: the L1 and L2 norms behind the penalties.
