---
title: Feature Selection Methods
tags: [machine-learning, feature-selection, statistics, preprocessing, auto-captured]
draft: false
---
**Feature selection** keeps the useful input variables and drops the rest. It reduces overfitting, speeds up training, cuts storage and measurement cost, and makes models easier to interpret. It differs from dimensionality reduction (such as PCA), which builds new features instead of keeping a subset of the originals.

## Three Families
| Family | How it works | Cost | Examples |
|---|---|---|---|
| **Filter** | Score each feature with a statistic, independent of any model | cheapest | variance, correlation, chi-square, mutual information |
| **Wrapper** | Train a model on candidate subsets and keep the best | most expensive | recursive feature elimination, forward/backward selection |
| **Embedded** | Selection happens during training | moderate | L1 regularization, tree feature importances (see [[Regularization]]) |

This note covers the statistical **filter** methods. They scale to large data, but most score features one at a time, so they miss interactions between features.

## Summary
| Method | Question it asks | Feature type | Target type |
|---|---|---|---|
| **Variance** | Does the feature vary at all? | numeric | none (unsupervised) |
| **Correlation** | Is it linearly related to the target, or to another feature? | numeric | numeric or binary |
| **Chi-square** | Are the feature and the class independent? | non-negative or categorical | categorical |
| **Mutual information** | How much does the feature reduce uncertainty about the target? | any | any |

## Variance Method
Drop features whose variance is below a threshold. A constant feature has variance 0 and cannot separate anything.
- **Unsupervised:** it ignores the target, which makes it a cheap first cleanup for constant columns and near-constant flags (for example a column that is 99.9% zeros).
- **Scale matters:** variance depends on units, so a feature measured in thousands always outscores one measured in fractions. Compare variances only after min-max scaling (see [[Scaling Techniques]]), or on binary features, where the variance is $p(1-p)$.
- **Tool:** `sklearn.feature_selection.VarianceThreshold`.

## Correlation
- **Feature vs. target:** keep features with a high absolute correlation (Pearson for linear, Spearman for monotonic relations). See [[Correlation Coefficients]].
- **Feature vs. feature:** if two features correlate above about 0.9, they carry the same information. Drop one to reduce multicollinearity.
- **Limit:** it detects only linear or monotonic relations. A feature with $r\approx 0$ can still be strongly related to the target (see the figure below).

## Chi-Square Test
Tests whether a feature and a categorical target are independent, using the contingency table of counts:

$$\chi^2=\sum \frac{(O-E)^2}{E}$$

$O$ is the observed count in a cell and $E$ the count expected if feature and class were independent. A large $\chi^2$ (small p-value) means dependence, so the feature is kept.
- **Requirements:** non-negative features (counts, frequencies, or min-max scaled values) and a categorical target. Numeric features are often binned first.
- **Typical use:** text classification, ranking words by how strongly they depend on the class.
- **Limit:** unreliable when expected cell counts are very small (below about 5).
- **Tool:** `sklearn.feature_selection.chi2`.

## Mutual Information
$$I(X;Y)=\sum_{x,y}p(x,y)\log\frac{p(x,y)}{p(x)\,p(y)}$$

It measures how far the joint distribution is from independence. It is zero if and only if $X$ and $Y$ are independent, and it grows with **any** kind of dependence, including nonlinear.
- **Flexible:** works for numeric and categorical features, for classification and regression targets.
- **Limit:** for continuous features it is estimated (nearest-neighbor methods), so it is noisier and slower than correlation. It does not give the direction of a relation.
- **Tools:** `mutual_info_classif`, `mutual_info_regression`.

## Correlation vs. Mutual Information
![[correlation-vs-mutual-information.png]]

Correlation catches the linear case and misses the quadratic one entirely ($r=0.06$ although $y$ is almost determined by $x$). Mutual information is high for both and near zero for pure noise. Use it when nonlinear relations are plausible. The MI values here are in nats, from scikit-learn's estimator on 400 synthetic points.

## Example: Breast Cancer Dataset
569 samples, 30 numeric features, benign vs. malignant, computed with scikit-learn:

- **Variance:** raw variances range from 0.00001 (`smoothness error`) to 324,167 (`worst area`), purely a scale artifact. After min-max scaling the smallest variance is about 0.006, so no feature is constant.
- **Correlation with the target:** the top feature is `worst concave points` at $\lvert r\rvert=0.79$. Among features, `mean radius` and `mean perimeter` correlate at 0.998, so one of them is redundant.
- **Chi-square (after scaling):** the top feature is `mean concave points` ($\chi^2\approx 52$).
- **Mutual information:** the top three are `worst perimeter`, `worst area` and `worst radius` (about 0.45 to 0.47). The lowest are near zero: `mean fractal dimension` (0.01) and `texture error` (0.001).

The methods agree on which features are strong but rank them differently, so compare rankings instead of trusting one score.

## Choosing and Using
1. **Start with variance**, then drop highly correlated feature pairs.
2. **Pick the score by data type:** correlation for linear relations, mutual information when relations may be nonlinear, chi-square for categorical features and target.
3. **Select inside cross-validation.** Choosing features on the full dataset before splitting leaks test information and inflates scores. Put the selector in a `Pipeline`.
4. **Choose the number of features** (`SelectKBest(k=...)` or `SelectPercentile`) by validation performance, not by a fixed cutoff.
5. **Know the blind spot.** A feature that looks useless alone can matter in combination, such as an XOR pattern where neither input predicts the target alone. Wrapper and embedded methods can catch these.

## Related Notes
- [[Correlation Coefficients]]: Pearson, Spearman and Kendall in detail.
- [[Regularization]]: L1 as an embedded selection method.
- [[Exploratory Data Analysis]]: inspecting features before selecting.
- [[Principal Component Analysis (PCA)]]: reducing dimensionality by building new features instead.
