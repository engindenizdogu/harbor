---
title: Clustering Evaluation Metrics
tags: [machine-learning, model-evaluation, metrics, clustering, auto-captured]
draft: false
---
Clustering is unsupervised, so there is no single "accuracy". Metrics fall into two families:

| Family | Needs true labels? | Question answered | Examples |
| ------ | ------------------ | ----------------- | -------- |
| **External** | Yes | How well do the clusters match a known grouping? | Purity, Rand Index, Adjusted Rand Index, NMI |
| **Internal** | No | Are the clusters compact and well separated? | Inertia, Silhouette, Davies-Bouldin |

Cluster IDs are arbitrary (cluster 0 vs. cluster 2 means nothing), so a good external metric must be **invariant to relabeling**. Plain accuracy is not, which is why these metrics exist. Classification metrics live in [[Metrics and Model Evaluation]].

All external metrics start from the **contingency table**, rows = clusters, columns = true classes. Running [[k-Means]] ($k=3$) on Iris gives:

| Cluster | setosa | versicolor | virginica | Cluster size |
| ------- | -----: | ---------: | --------: | -----------: |
| 0       | 0      | 48         | 14        | 62           |
| 1       | 50     | 0          | 0         | 50           |
| 2       | 0      | 2          | 36        | 38           |

## Purity
Assign each cluster to its majority class and count how many points are then "correct":

$$\text{Purity} = \frac{1}{n} \sum_{j} \max_{c} \, n_{jc}$$

Iris: $(48 + 50 + 36) / 150 = 0.89$.

- Range 0 to 1, higher is better; easy to interpret.
- **Flaw:** purity rewards more clusters. With one cluster per point, purity is 1. Only compare runs with the same $k$.

## Rand Index (RI)
Look at every **pair** of points ($\binom{n}{2}$ pairs) and check whether the clustering and the ground truth agree about the pair:

- $a$ = pairs in the **same** cluster and the **same** class
- $b$ = pairs in **different** clusters and **different** classes

$$\text{RI} = \frac{a + b}{\binom{n}{2}}$$

It is the accuracy of the question "do these two points belong together?". Range 0 to 1, with 1 a perfect match. Iris: $\text{RI} \approx 0.88$.

**Flaw:** random clusterings do not score 0, and the baseline rises with the number of clusters. That makes RI hard to read on its own.

## Adjusted Rand Index (ARI)
ARI corrects RI for chance by subtracting its expected value under random labeling:

$$\text{ARI} = \frac{\text{RI} - \mathbb{E}[\text{RI}]}{\max(\text{RI}) - \mathbb{E}[\text{RI}]}$$

Computed directly from the contingency table with $n_{jc}$ (cell counts), $a_j$ (row sums), $b_c$ (column sums):

$$\text{ARI} = \frac{\sum_{jc} \binom{n_{jc}}{2} - \left[\sum_j \binom{a_j}{2} \sum_c \binom{b_c}{2}\right] / \binom{n}{2}}{\frac{1}{2}\left[\sum_j \binom{a_j}{2} + \sum_c \binom{b_c}{2}\right] - \left[\sum_j \binom{a_j}{2} \sum_c \binom{b_c}{2}\right] / \binom{n}{2}}$$

| ARI | Meaning |
| --- | ------- |
| 1   | Identical partitions (up to relabeling) |
| ~0  | Random labeling |
| < 0 | Worse than random |

Iris: $\text{ARI} \approx 0.73$. This is the metric to report by default when ground truth exists, since it is chance-corrected and does not depend on $k$ the way purity does.

## Normalized Mutual Information (NMI)
Measures how much knowing the cluster reduces uncertainty about the class, using entropy:

$$\text{NMI} = \frac{I(C; K)}{\text{mean}\big(H(C),\, H(K)\big)}$$

Range 0 to 1. Like ARI it ignores labels, but it is information-theoretic rather than pair-counting. Iris: $\text{NMI} \approx 0.76$.

## Internal Metrics (no ground truth)
- **Inertia (within-cluster sum of squares):** the quantity [[k-Means]] minimizes. Always decreases as $k$ grows, so use it with the elbow method rather than as a score.
- **Silhouette score:** for each point, $s = \dfrac{b - a}{\max(a, b)}$, where $a$ is the mean distance to its own cluster and $b$ the mean distance to the nearest other cluster. Range -1 to 1; near 1 means well-matched to its cluster, near 0 means on a boundary, negative means probably misassigned. The mean over all points can be compared across values of $k$. Iris ($k=3$): about 0.55.
- **Davies-Bouldin index:** average similarity between each cluster and its most similar neighbor; *lower* is better.

## Which to Use
| Situation | Metric |
| --------- | ------ |
| Ground truth available, quick sanity check | Purity |
| Ground truth available, comparing methods or different $k$ | ARI (and NMI) |
| No ground truth, choosing $k$ | Silhouette, elbow on inertia |

## Code
```python
from sklearn.metrics import (adjusted_rand_score, rand_score,
                             normalized_mutual_info_score, silhouette_score)
import pandas as pd

contingency = pd.crosstab(cluster_labels, y)
purity = contingency.max(axis=1).sum() / contingency.values.sum()

ri  = rand_score(y, cluster_labels)
ari = adjusted_rand_score(y, cluster_labels)
nmi = normalized_mutual_info_score(y, cluster_labels)
sil = silhouette_score(X, cluster_labels)        # internal: needs only the data
```

*Source: [scikit-learn, Clustering performance evaluation](https://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation). Original ARI: Hubert & Arabie (1985).*
