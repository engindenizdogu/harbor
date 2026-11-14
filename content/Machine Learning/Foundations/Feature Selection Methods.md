---
title: Feature Selection Methods
tags: [machine-learning, feature-selection, statistics, preprocessing, auto-captured]
draft: false
---
**Feature selection** keeps the useful input variables and drops the rest. It reduces overfitting, speeds up training, cuts storage and measurement cost, and makes models easier to interpret. It differs from dimensionality reduction (such as PCA), which builds new features instead of keeping a subset of the originals.

## Why Not Use All Features?
A natural question is why not hand every feature to the model and let it decide. Four reasons:
- **Overfitting:** with more features than samples ($p > n$), a model can fit the training data perfectly by also fitting the noise. Training scores look excellent while test scores collapse.
- **Occam's razor:** simpler models with fewer inputs are easier to explain and trust.
- **Garbage in, garbage out:** non-informative features distract the learning process and degrade the output.
- **Cost:** every extra feature adds training time, memory, and often a real-world cost to measure or collect it.

## Three Families
| Family | How it works | Strengths | Weaknesses | Examples |
|---|---|---|---|---|
| **Filter** | Score each feature with a statistic, independent of any model | fast, scalable, model-independent | ignores interactions between features | variance, correlation, chi-square, mutual information |
| **Wrapper** | Search subsets by training a model on each candidate | captures interactions, often the most accurate | expensive; overfits unless cross-validated | forward selection, backward elimination, RFE |
| **Embedded** | Selection happens during training | efficient, built into model fitting | tied to one model and its tuning | Lasso (L1), decision trees, random forest importance |

Filter methods scale to large data, but most score features one at a time, so they miss interactions between features. Wrapper methods are covered in their own section below; for ranking features by how much a trained model relies on them, see [[Feature Importance Methods]].

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

## Wrapper Methods
Wrappers search over feature subsets by training a model on each candidate. All of them are **greedy** (a decision is never reconsidered), **costly** (many model fits), and must run **inside cross-validation** to avoid leakage.

| Method | Start | Step | Stops when |
|---|---|---|---|
| **Forward selection** | no features | add the feature that most improves the criterion (CV score, AIC, p-value) | no addition helps, or $k$ features reached |
| **Backward elimination** | all features | remove the weakest feature by a statistical criterion (highest p-value, best AIC/BIC/CV score) | all remaining features are significant, or no removal helps |
| **Recursive feature elimination (RFE)** | all features | remove the feature(s) with the smallest model importance ($\lvert\text{coef}\rvert$ or `feature_importances_`) | a preset number of features remains (RFECV picks it by CV) |

**RFE vs. backward elimination.** Both shrink the set one step at a time, and on a linear model they behave almost the same. The difference is the removal rule: backward elimination uses a statistical test, while RFE uses whatever importance the model exposes, so it works with linear models, SVMs and trees. RFE also returns a full ranking and can drop several features per step (`step` parameter). Because it ranks by coefficient size, **standardize features before RFE**.

**Classic backward example:** fit OLS, drop the feature with p = 0.82, refit, and repeat until every p < 0.05. Selecting by p-value makes the final model's p-values look better than they really are, so validate on held-out data.

**Forward vs. backward.** Backward elimination sees all features together from the start, so it handles features that matter only in combination better than forward selection. It needs more samples than features, though.

## Embedded Methods
The model selects features as a side effect of training.

| Method | How it selects | Strengths | Weaknesses |
|---|---|---|---|
| **Lasso (L1)** | the penalty $\lambda\sum_j \lvert w_j\rvert$ drives some weights to exactly zero | automatic, fast, good for high-dimensional sparse data (text, genomics) | drops one of a group of correlated features arbitrarily; result depends on $\lambda$ |
| **Decision tree** | features that split the data well earn high impurity-reduction scores | nonlinear, no scaling needed | single trees overfit; biased toward features with many levels |
| **Random forest** | averages tree importances over many trees | more robust to noise than one tree | higher cost on large data; less interpretable |

**Penalty strength sets the feature count.** On the diabetes regression dataset (10 standardized features), Lasso keeps:

| `alpha` | 0.01 | 0.1 | 1 | 5 | 10 | 20 |
|---|---|---|---|---|---|---|
| Non-zero coefficients | 10 | 9 | 7 | 5 | 4 | 3 |

Tune `alpha` by cross-validation (`LassoCV`) rather than picking it by hand. See [[Regularization]] for why L1 produces exact zeros.

**Common snippet pitfall.** `SelectFromModel(LogisticRegression(penalty="l1"))` raises an error in current scikit-learn, because the default `lbfgs` solver supports only L2. Pass `solver="liblinear"` or `solver="saga"`. With `max_features=k`, also set `threshold=-np.inf` to get exactly the top $k$ by importance.

## scikit-learn Patterns
Tested on the breast cancer dataset with a stratified 70/30 split:

| Goal | Code | Result |
|---|---|---|
| Drop near-constant features | `VarianceThreshold(threshold=0.01)` on min-max scaled data | kept 29 of 30 |
| Top-k by score | `SelectKBest(mutual_info_classif, k=10)`; `SelectKBest(chi2, k=10)` needs non-negative input | `scores_`, `pvalues_` give per-feature scores |
| Top percent | `SelectPercentile(f_classif, percentile=25)` | kept 8 |
| RFE | `Pipeline([StandardScaler(), RFE(LogisticRegression(), n_features_to_select=8, step=2)])` | `support_`, `ranking_` (1 = kept) |
| RFE with CV | `RFECV(LogisticRegression(), cv=5, scoring="roc_auc")` | chose 7 features |
| Forward/backward | `SequentialFeatureSelector(est, direction="forward", n_features_to_select=5, cv=5)` | forward picked `area error`, `worst texture`, `worst perimeter`, `worst smoothness`, `worst concave points` |
| Embedded (L1) | `SelectFromModel(LogisticRegression(penalty="l1", solver="liblinear", C=0.1))` | kept 7 |
| Embedded (trees) | `SelectFromModel(RandomForestClassifier(), threshold="median")` | kept 15 |

Regression targets use `f_regression` or `mutual_info_regression`. Sequential selection fits many models and is slow on large feature sets.

**Leakage-safe evaluation:**
```python
pipe = Pipeline([("scale", StandardScaler()),
                 ("select", SelectKBest(f_classif, k=10)),
                 ("clf", LogisticRegression())])
cross_val_score(pipe, X, y, cv=5, scoring="roc_auc")
```
This gave AUC 0.987, versus 0.995 with all 30 features and no selection. Selection did not improve accuracy here; its payoff is speed, interpretability, and robustness on noisy high-dimensional data.

## Evaluating a Selection
A selected subset is only as good as what it does to the final model. Compare models with and without selection on:

| Criterion | What to measure |
|---|---|
| **Predictive performance** | accuracy, F1, RMSE on cross-validation or a hold-out set |
| **Cost** | training and inference time, memory |
| **Simplicity** | number of features kept |
| **Generalization** | gap between training and validation scores; a smaller gap means less overfitting |
| **Stability** | whether the same features are chosen across data splits or bootstrap samples |

Stability is the criterion most often skipped. Measure it by running the selector on bootstrap samples and computing the average pairwise **Jaccard similarity** $\lvert A\cap B\rvert / \lvert A\cup B\rvert$ of the selected sets.

![[feature-selection-stability.png]]

Breast cancer dataset, top 10 of 30 features on 20 bootstrap samples. Univariate filters were the most stable (0.93 and 0.89), random forest next (0.83), L1 lower (0.73) and RFE the least stable (0.57). The data has many near-duplicate features (radius, perimeter and area), and model-based methods swap between them from sample to sample. Low stability does not mean low accuracy: the swapped features carry the same information. It does mean the individual feature names should not be over-interpreted.

## Feature Selection at Big Data Scale
- **Filters parallelize easily**, since each feature is scored independently, so they are the usual first step on very wide data.
- **Wrappers become expensive** because each step retrains a model on the full dataset. Prefer embedded methods or RFE with a large `step`.
- **Spark MLlib** provides `VarianceThresholdSelector`, `UnivariateFeatureSelector` (F-test or chi-square depending on whether features and label are continuous or categorical, keeping top-$k$, a percentile, or by false-positive/discovery rate), and `ChiSqSelector`. L1 selection uses `LogisticRegression` or `LinearRegression` with `elasticNetParam=1.0`, and tree models expose `featureImportances`. See [[Apache Spark]].

## Applications
- **Bioinformatics:** pick a few genes or proteins out of thousands for disease or cancer-subtype classification.
- **Finance:** select the key indicators for credit scoring and risk models.
- **Text classification:** keep the most informative words or n-grams for spam detection or sentiment analysis.
- **Sensors and IoT:** choose the most informative signals for predictive maintenance or health monitoring with wearables.
- **Marketing:** find the variables that drive churn or campaign response.

## Choosing and Using
1. **Start with variance**, then drop highly correlated feature pairs.
2. **Pick the score by data type:** correlation for linear relations, mutual information when relations may be nonlinear, chi-square for categorical features and target.
3. **Select inside cross-validation.** Choosing features on the full dataset before splitting leaks test information and inflates scores. Put the selector in a `Pipeline`.
4. **Choose the number of features** (`SelectKBest(k=...)` or `SelectPercentile`) by validation performance, not by a fixed cutoff.
5. **Match the family to the budget.** Filters for very wide data or a quick first pass, embedded methods when the model is already chosen, wrappers when accuracy matters most and the feature count is modest.
6. **Know the blind spot.** A feature that looks useless alone can matter in combination, such as an XOR pattern where neither input predicts the target alone. Wrapper and embedded methods can catch these.

## Related Notes
- [[Correlation Coefficients]]: Pearson, Spearman and Kendall in detail.
- [[Regularization]]: L1 as an embedded selection method.
- [[Feature Importance Methods]]: coefficients, impurity, permutation importance and SHAP.
- [[Exploratory Data Analysis]]: inspecting features before selecting.
- [[Principal Component Analysis (PCA)]]: reducing dimensionality by building new features instead.
