---
title: SVD Snippets
tags: [code-snippets, machine-learning, linear-algebra]
draft: false
---
NumPy snippets for the [[Singular Value Decomposition]] worked example: decomposition, reconstruction, low-rank approximation, and full vs. reduced shapes.

## Decompose and reconstruct

```python
import numpy as np

A = np.array([[3., 0.], [4., 5.]])

U, s, Vt = np.linalg.svd(A)      # s is a 1D array of singular values (descending), Vt is V transposed
print(s)                         # [6.708 2.236] = [3*sqrt(5), sqrt(5)]

# Rebuild A = U @ Sigma @ V^T
print(np.allclose(U @ np.diag(s) @ Vt, A))   # True
```

NumPy may flip the sign of a singular-vector pair (here `U[:, 0]` and `Vt[0]` come out negative compared with the hand calculation). The product is unchanged, because the signs cancel.

## Rank-1 approximation

```python
# Keep only the largest singular value: A1 = sigma_1 * u_1 * v_1^T
A1 = s[0] * np.outer(U[:, 0], Vt[0])
print(A1)                                    # [[1.5 1.5], [4.5 4.5]]

# Frobenius error equals the dropped singular value
print(np.linalg.norm(A - A1), s[1])          # 2.236  2.236
```

General rank-$k$ version:

```python
def low_rank(A, k):
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    return U[:, :k] @ np.diag(s[:k]) @ Vt[:k]
```

## Full vs. reduced shapes

```python
B = np.arange(8.).reshape(4, 2)              # m = 4, n = 2

U, s, Vt = np.linalg.svd(B)                  # full
print(U.shape, s.shape, Vt.shape)            # (4, 4) (2,) (2, 2)

Ur, sr, Vtr = np.linalg.svd(B, full_matrices=False)   # reduced (thin)
print(Ur.shape, sr.shape, Vtr.shape)         # (4, 2) (2,) (2, 2)

# Full SVD needs a rectangular Sigma (m x n) padded with zero rows
S = np.zeros(B.shape)
S[:len(s), :len(s)] = np.diag(s)
print(np.allclose(U @ S @ Vt, B))            # True
```
