---
title: Singular Value Decomposition
tags: [machine-learning, algorithms]
draft: false
---

| Type                                    |
| --------------------------------------- |
| Preprocessing, Dimensionality Reduction |

Please see "Singular Value Decomposition" section under [[2. Linear Algebra]] for SVD formulation.

## Interpretation of U, Σ, and V

For an $m \times n$ matrix $A$, $A = U\Sigma V^T$ splits the map $x \mapsto Ax$ into rotate, scale, rotate:

| Matrix             | Name                   | Meaning                                                                                                                                                      |
| ------------------ | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| $V$ ($n \times n$) | Right singular vectors | Orthonormal basis of the **input** space. Columns are eigenvectors of $A^TA$: the directions $A$ stretches independently. $V^T$ rotates $x$ into this basis. |
| $\Sigma$           | Singular values        | Scales each direction by $\sigma_i$ (the strength of that direction).                                                                                        |
| $U$ ($m \times m$) | Left singular vectors  | Orthonormal basis of the **output** space. Columns are eigenvectors of $AA^T$: where the stretched directions land.                                          |

The two bases are linked by $Av_i = \sigma_i u_i$: input direction $v_i$ maps to output direction $u_i$, stretched by $\sigma_i$.

**Dimensions: full vs. reduced SVD.** $\Sigma$ is $m \times n$, not square: the $\min(m, n)$ singular values sit on its diagonal and every other entry is zero. The shapes chain as $(m \times m)(m \times n)(n \times n) = m \times n$. For $m = 4$, $n = 2$:

$$\Sigma = \begin{bmatrix} \sigma_1 & 0 \\ 0 & \sigma_2 \\ 0 & 0 \\ 0 & 0 \end{bmatrix}$$

The zero rows multiply the last $m - r$ columns of $U$ (where $r$ is the rank), so those columns never contribute to $A$. The **reduced (thin) SVD** drops them: $U$ is $m \times k$, $\Sigma$ is $k \times k$, $V^T$ is $k \times n$, with $k = \min(m, n)$ or the rank. The product is still $m \times n$. In NumPy: `np.linalg.svd(A, full_matrices=False)`.

**Common uses:**
- Compression: keep the top $k$ columns of $U$ and $V$ and top $k$ values of $\Sigma$ for the best rank-$k$ approximation.
- [[Recommendation Systems]]: $U$ describes row entities (users), $V$ describes column entities (items), and each column pair is a latent factor.
- [[Word Vectors]]: rows of $U$ (scaled by $\Sigma$) act as word embeddings.

## Worked Example

Decompose $A = \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix}$ as $A = U\Sigma V^T$.

**Step 1: Find $V$ and $\Sigma$ from $A^TA$.**

$$\begin{aligned}
A^TA &= \begin{bmatrix} 25 & 20 \\ 20 & 25 \end{bmatrix} \\
\det(A^TA - \lambda I) &= (25-\lambda)^2 - 400 = 0 \\
\lambda_1 &= 45, \quad \lambda_2 = 5
\end{aligned}$$

The singular values are the square roots of the eigenvalues, sorted in descending order: $\sigma_1 = \sqrt{45} = 3\sqrt{5} \approx 6.71$ and $\sigma_2 = \sqrt{5} \approx 2.24$.

The unit eigenvectors of $A^TA$ give the columns of $V$:

$$v_1 = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}, \quad v_2 = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ -1 \end{bmatrix}$$

**Reminder: how to get $v_1$ and $v_2$.** For each eigenvalue, solve $(A^TA - \lambda I)v = 0$ (find the null space), then divide by the vector's length so it has unit norm.

$$\begin{aligned}
\lambda_1 = 45:\quad & \begin{bmatrix} -20 & 20 \\ 20 & -20 \end{bmatrix}v = 0 \;\Rightarrow\; -20v_a + 20v_b = 0 \;\Rightarrow\; v \propto \begin{bmatrix} 1 \\ 1 \end{bmatrix}, \quad \left\|\begin{bmatrix} 1 \\ 1 \end{bmatrix}\right\| = \sqrt{2} \\
\lambda_2 = 5:\quad & \begin{bmatrix} 20 & 20 \\ 20 & 20 \end{bmatrix}v = 0 \;\Rightarrow\; 20v_a + 20v_b = 0 \;\Rightarrow\; v \propto \begin{bmatrix} 1 \\ -1 \end{bmatrix}, \quad \left\|\begin{bmatrix} 1 \\ -1 \end{bmatrix}\right\| = \sqrt{2}
\end{aligned}$$

Because $A^TA$ is symmetric, $v_1 \perp v_2$ automatically. See [[2. Linear Algebra]] for eigenvectors.

**Step 2: Find $U$ from $Av_i = \sigma_i u_i$.**

$$\begin{aligned}
u_1 &= \frac{Av_1}{\sigma_1} = \frac{1}{3\sqrt{5}} \cdot \frac{1}{\sqrt{2}}\begin{bmatrix} 3 \\ 9 \end{bmatrix} = \frac{1}{\sqrt{10}}\begin{bmatrix} 1 \\ 3 \end{bmatrix} \\
u_2 &= \frac{Av_2}{\sigma_2} = \frac{1}{\sqrt{5}} \cdot \frac{1}{\sqrt{2}}\begin{bmatrix} 3 \\ -1 \end{bmatrix} = \frac{1}{\sqrt{10}}\begin{bmatrix} 3 \\ -1 \end{bmatrix}
\end{aligned}$$

**Step 3: Assemble.**

$$A = \underbrace{\frac{1}{\sqrt{10}}\begin{bmatrix} 1 & 3 \\ 3 & -1 \end{bmatrix}}_{U}\underbrace{\begin{bmatrix} 3\sqrt{5} & 0 \\ 0 & \sqrt{5} \end{bmatrix}}_{\Sigma}\underbrace{\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}}_{V^T}$$

**Step 4: Low-rank approximation (compression).** Keeping only the largest singular value gives the best rank-1 approximation of $A$:

$$A_1 = \sigma_1 u_1 v_1^T = \begin{bmatrix} 1.5 & 1.5 \\ 4.5 & 4.5 \end{bmatrix}$$

The error is $\|A - A_1\|_F = \sigma_2 = \sqrt{5}$, so the discarded singular values measure exactly how much information is lost. In general, keeping the top $k$ singular values stores $k(m + n + 1)$ numbers instead of $mn$, which is why SVD is used for compression and dimensionality reduction.

For NumPy code reproducing this example, see [[SVD Snippets]].

## Limitations

**Possible Limitations of SVD:**
- Computational cost scales quadratically
- Different learning regime than other DL models
- Bad for millions of words or documents (if used for [[Word Vectors]] in NLP - See section "Representing with a Co-occurrence Matrix")
- Hard to incorporate new words or documents (if used for [[Word Vectors]] in NLP - See section "Representing with a Co-occurrence Matrix")
