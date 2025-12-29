---
title: Principal Component Analysis (PCA)
---
# Principal Component Analysis (PCA)

| Type                                    |
| --------------------------------------- |
| Preprocessing, Dimensionality Reduction |

**Goals of PCA:**
- Visualize data in a lower-dimensional space
- Understand the sources of variability in the data
- Understand correlations between different coordinates of the data points
- Noise may be reduced

> PCA rotates the data (centered at the origin) in such a way that the maximum variability is visible (i.e., aligned with the axes.)

For a given data set and parameter k, to goal of PCA is to compute the k-dimensional subspace that minimizes the average squared distance between the points and the subspace. Principle components corresponds to the k eigenvectors of the covariance matrix that have the largest eigenvalues.

**How to calculate PCA?**
1. Calculate the eigenvalues and unit eigenvectors of the covariance matrix and order the eigenvectors in descending order with respect to the corresponding eigenvalues.
	1. Covariance matrix: $Cov(X) = {1\over n-1}X^TX$
2. The unit vectors $u_1,...,u_n$ of the covariance matrix represent the principle components of the data. The corresponding eigenvalues give the variance of the principle components.
3. Pick top k principle components and construct $[u_1,...,u_k]$
4. Each observation $x \epsilon R^n$ will be represented as $Q^T_kx$ in the lower dimensional space $R^k$.

> In practice, do not forget to apply **z-score normalization** to the dataset before computing PCA. This is to ensure every feature has the same scale and does not mess up eigenvalue calculations. In other words, think of two features: a car's age and total miles driven. If we do not normalize, "total mileage" could be "represented" more while calculating eigenvalues.