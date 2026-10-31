---
title: Probability Calibration
tags: [machine-learning, model-evaluation, calibration, classification, auto-captured]
draft: false
---
A model is **calibrated** if its predicted probabilities match observed frequencies: among all cases where it says 0.7, about 70% should truly be positive. Ranking quality (AUC, see [[ROC and AUC Curves]]) and calibration are different properties. A model can rank perfectly yet output probabilities that are far too confident or too timid.

## Why It Matters
- **Decisions with costs:** the rule "predict positive when $p > C_{FP}/(C_{FP}+C_{FN})$" is only correct for calibrated probabilities.
- **Risk communication:** "a 30% chance" must mean 30%, for example in medicine or credit scoring.
- **Combining models or thresholds:** downstream systems that multiply or compare probabilities inherit any distortion.
- **Ranking-only uses** (top-$k$ lists) do not need calibration.

## Measuring It
**Reliability diagram:** group predictions into bins by predicted probability and plot the observed fraction of positives against the mean prediction in each bin. A calibrated model follows the diagonal; points above it mean the model under-predicts, points below mean it over-predicts. Bins with few examples are noisy, so show counts or use quantile bins.

| Metric | Definition | Notes |
| :-- | :-- | :-- |
| **Brier score** | $\frac{1}{n}\sum (p_i - y_i)^2$ | Mean squared error of the probabilities; lower is better; mixes calibration with ranking |
| **Log loss** | $-\frac{1}{n}\sum [y_i\ln p_i + (1-y_i)\ln(1-p_i)]$ | Punishes confident mistakes very heavily |
| **Expected calibration error (ECE)** | Weighted average gap between confidence and accuracy over bins | Depends on the number of bins |

## Which Models Tend to Be Miscalibrated
- **Naive Bayes** pushes probabilities toward 0 and 1 because its independence assumption double-counts correlated evidence.
- **Random forests, boosted trees, and SVMs** often distort probabilities away from the extremes.
- **Logistic regression** is usually reasonably calibrated when its assumptions roughly hold.
- **Modern deep networks** are often overconfident (Guo et al., 2017, [On Calibration of Modern Neural Networks](https://arxiv.org/abs/1706.04599)).

These are tendencies, not guarantees; always check on your own data.

## Fixing It: Post-Hoc Calibration
Train the classifier, then learn a mapping from its scores to probabilities **on held-out data** (or with cross-validation), never on the training data the model already fit.

| Method | Idea | When it fits |
| :-- | :-- | :-- |
| **Platt scaling** | Fit a logistic curve $p=1/(1+e^{As+B})$ to the scores | Small datasets, distortion shaped like a sigmoid |
| **Isotonic regression** | Fit a monotone step function | More data (it can overfit small sets), arbitrary monotone distortion |
| **Temperature scaling** | Divide the logits by one learned $T$ before the softmax | Neural networks; changes confidence, not the predicted class |

Both Platt and isotonic mappings are monotone, so they leave the ranking essentially unchanged: AUC stays the same while probabilities improve.

## Experiment
*Simulated data (10,000 training and 10,000 test examples, 12 features with some redundant ones, run with scikit-learn).* Gaussian naive Bayes was calibrated with 5-fold cross-validation.

![[reliability-diagram-calibration.png]]
*Reliability diagram on the test set. The dashed diagonal is perfect calibration.*

| Model | AUC | Brier score |
| :-- | :-- | :-- |
| Naive Bayes (raw) | 0.901 | 0.1429 |
| Naive Bayes + Platt (sigmoid) | 0.901 | 0.1406 |
| Naive Bayes + isotonic | 0.901 | 0.1251 |
| Logistic regression | 0.882 | 0.1234 |

- **Ranking is unchanged:** all three naive Bayes variants have the same AUC.
- **Probabilities improve:** isotonic calibration moves the curve close to the diagonal and cuts the Brier score from 0.1429 to 0.1251; Platt helps only slightly here.
- **Better ranking is not better probabilities:** naive Bayes has the higher AUC, yet logistic regression has the lower Brier score, and after isotonic calibration the two are similar.
- **Noise caveat:** logistic regression's curve is erratic in the top bins because few examples fall there.

```python
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import brier_score_loss

calibrated = CalibratedClassifierCV(GaussianNB(), method="isotonic", cv=5).fit(X_train, y_train)
p = calibrated.predict_proba(X_test)[:, 1]
frac_pos, mean_pred = calibration_curve(y_test, p, n_bins=10)   # reliability diagram
brier_score_loss(y_test, p)
```
*Source: [scikit-learn probability calibration guide](https://scikit-learn.org/stable/modules/calibration.html).*

## Related Idea for Forecasts
Interval forecasts have a calibration analogue called **coverage**: a 95% prediction interval should contain the true value about 95% of the time. See [[Autoregressive Models]] and [[Statistical Inference Basics]].
