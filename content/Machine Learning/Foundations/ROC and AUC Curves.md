---
title: ROC and AUC Curves
tags: [machine-learning, model-evaluation, metrics, classification, auto-captured]
draft: false
---
A classifier usually outputs a **score** (a probability or a margin), and a **threshold** turns it into a yes or no. The **ROC curve** shows how the model behaves at every possible threshold at once, and the **AUC** summarizes it as one number. The confusion matrix, precision, recall, and F1 for a single threshold are in [[Metrics and Model Evaluation]]; whether the scores themselves can be trusted as probabilities is the subject of [[Probability Calibration]].

## Building the Curve
Two rates come from the confusion matrix at a given threshold:

$$\text{TPR} = \frac{TP}{TP + FN} \;(\text{recall, sensitivity}) \qquad \text{FPR} = \frac{FP}{FP + TN} \;(1 - \text{specificity})$$

Sweep the threshold from high to low. At a very high threshold nothing is predicted positive, so $(\text{FPR},\text{TPR})=(0,0)$; at a very low one everything is, giving $(1,1)$. Plotting the pairs between them traces the ROC curve (receiver operating characteristic). A lower threshold catches more positives and also raises more false alarms.

### Worked example
Ten examples, five positive and five negative. Scores: positives 0.95, 0.85, 0.70, 0.55, 0.40; negatives 0.80, 0.60, 0.45, 0.30, 0.20.

| Threshold | TPR | FPR |
| :-- | :-- | :-- |
| above 0.95 | 0.0 | 0.0 |
| 0.95 | 0.2 | 0.0 |
| 0.85 | 0.4 | 0.0 |
| 0.80 | 0.4 | 0.2 |
| 0.70 | 0.6 | 0.2 |
| 0.60 | 0.6 | 0.4 |
| 0.55 | 0.8 | 0.4 |
| 0.45 | 0.8 | 0.6 |
| 0.40 | 1.0 | 0.6 |
| 0.30 | 1.0 | 0.8 |
| 0.20 | 1.0 | 1.0 |

At a threshold of 0.5 the model predicts 4 true positives and 2 false positives, so $\text{TPR}=0.8$ and $\text{FPR}=0.4$: one point on the curve.

## AUC
**AUC** (area under the ROC curve) has a direct meaning: the probability that a randomly chosen positive gets a higher score than a randomly chosen negative, counting ties as half. In the example, 19 of the 25 positive-negative pairs are ordered correctly, so $\text{AUC}=19/25=0.76$ (this matches the library value).

| AUC | Reading |
| :-- | :-- |
| 0.5 | No better than chance (the diagonal) |
| 0.7 to 0.8 | Often called acceptable (a loose rule of thumb that varies by field) |
| above 0.9 | Strong ranking |
| 1.0 | Every positive scores above every negative |
| below 0.5 | Worse than chance; the scores are inverted |

Properties worth remembering:
- **Threshold-free:** it judges the ranking, not one operating point.
- **Depends only on ranking:** multiplying the scores or applying any monotone transformation leaves AUC unchanged, so it says nothing about whether probabilities are calibrated.
- **Not tied to prevalence:** FPR and TPR are each computed within one class, so AUC is stable when the class mix changes. This is both a strength and the weakness described next.

## ROC vs. Precision-Recall
When positives are rare, ROC can look flattering because the huge pool of negatives keeps the FPR small even when false positives swamp the true ones. A precision-recall (PR) curve plots precision against recall and shows the problem directly. Summary metric: **average precision** (AP), the area under the PR curve; its chance level is the prevalence, not 0.5.

![[roc-vs-pr-imbalanced.png]]
*Same logistic regression on a simulated dataset with 2% positives (8,000 test examples, 160 positives). Left: ROC AUC is 0.80. Right: average precision is 0.55 against a chance level of 0.02.*

The numbers from this run show the effect:

| Operating point | FPR | Precision | Counts |
| :-- | :-- | :-- | :-- |
| Recall at least 0.5 | 0.002 | 0.86 | 80 true positives, 13 false positives |
| Recall at least 0.8 | 0.47 | 0.034 | 128 true positives, 3,685 false positives |

An AUC of 0.80 sounds good, yet pushing recall to 0.8 means about 29 false alarms for every real positive. As a rule of thumb, prefer the PR curve when the positive class is rare or when false positives matter more than false negatives, and ROC otherwise.

## Choosing a Threshold
The curve does not choose the operating point; you do.

| Method | Idea |
| :-- | :-- |
| **Youden's J** | Maximize $J=\text{TPR}-\text{FPR}$, the point farthest above the diagonal. In the worked example several thresholds tie at $J=0.4$ |
| **Cost-based** | If the scores are calibrated probabilities and a false positive costs $C_{FP}$ and a false negative $C_{FN}$, predict positive when $p > C_{FP}/(C_{FP}+C_{FN})$ |
| **Fixed target** | Take the highest-precision point that still reaches a required recall (or the reverse) |

The cost rule only works when the scores are real probabilities, which is why [[Probability Calibration]] matters.

## Beyond Two Classes and Single Numbers
- **Multiclass:** compute ROC one class against the rest (one-vs-rest), or one pair at a time (one-vs-one), then average. **Macro** averaging weights classes equally; **micro** pools all decisions, so large classes dominate.
- **Uncertainty:** an AUC from a test set is an estimate. Bootstrap the test set for a confidence interval, or use the DeLong test to compare two models scored on the same examples.
- **Related scores:** the **Gini coefficient** is $2\,\text{AUC}-1$. The **KS statistic** is the maximum gap between the score distributions of the two classes, which equals the maximum of $\text{TPR}-\text{FPR}$ (Youden's J).

## Link to Hypothesis Testing
A threshold is a decision rule, so the ideas from [[Statistical Inference Basics]] apply: FPR is the type I error rate (the significance level $\alpha$) and TPR is statistical power. The ROC curve is the power-versus-$\alpha$ trade-off of the detector. The same reasoning covers any alerting system: its detection rate and false-alert rate are a single point on a ROC curve.

```python
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score

fpr, tpr, thresholds = roc_curve(y_true, scores)
auc = roc_auc_score(y_true, scores)
ap  = average_precision_score(y_true, scores)
best = thresholds[(tpr - fpr).argmax()]          # Youden's J
# multiclass: roc_auc_score(y, proba, multi_class="ovr", average="macro")
```
*Source: [scikit-learn model evaluation guide](https://scikit-learn.org/stable/modules/model_evaluation.html). The worked example and the 2% prevalence experiment were run with scikit-learn.*
