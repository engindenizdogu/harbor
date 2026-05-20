---
title: Fisher's Linear Discriminant
tags: [machine-learning, algorithms]
draft: false
---
| Type              |
| ----------------- |
| Linear Classifier |

Good Illustration: [An illustrative introduction to Fisher's Linear Discriminant - Thalles' blog](https://sthalles.github.io/fisher-linear-discriminant/)

Find an orientation along which the projected samples are well separated.
![[Pasted image 20260425184410.png]]

**Fisher's Linear Discriminant**
- We want class means to be as far as possible. The denominator is the total within-class scatter of the projected samples.

$$ \arg\max_{w} \frac{\vert m_{+} - m_{-} \vert ^2}{s_{+}^2 + s_{-}^2} $$

where $s_+^2$ or $s_-^2$ is (almost like variance),

$$ s_{+}^2 = \sum_{x \in C_{+}} (w^T x - m_{+})^2 $$

$$m_+ = \frac{1}{N_+} \sum_{x \in C_+} \mathbf{w}^T \mathbf{x} = \mathbf{w}^T \mathbf{m}_+$$

Define following matrices:

$$S_+ = \sum_{x \in C_+} (\mathbf{x} - \mathbf{m}_+)(\mathbf{x} - \mathbf{m}_+)^T$$

$$S_W = S_+ + S_-$$

> $S_+$ or $S_-$ takes the form
> 
> $$
\begin{aligned}
\begin{bmatrix} var(x_1) && cov(x_1,x_2) \\ cov(x_1,x_2) && var(x_2) \end{bmatrix}
\end{aligned}
$$

$$S_B = (m_+-m_-)(m_+-m_-)^T$$

Using these we obtain,

$$J(\mathbf{w}) = \frac{\vert m_+ - m_- \vert ^2}{s_+^2 + s_-^2} = \frac{\mathbf{w}^T S_B \mathbf{w}}{\mathbf{w}^T S_W \mathbf{w}}$$

$J$ is maximized when (take derivate with respect to w)

$$(w^TS_Bw)S_Ww = (w^TS_Ww)S_Bw$$

Notice:
- $w^TS_Ww$ and $w^TS_Bw$ are scalars, thus we get 

$$\alpha S_Ww = \beta S_Bw$$

- If we take $\lambda = \alpha / \beta$ we get $S_Bw=λS_Ww$ which the generalized eigenvalue problem:

$$S_W^{−1}S_Bw=λw$$

From the generalized eigenvalue equation, we derive that the optimal $w$ is:

$$w∝ S_W^{−1}(m_+−m_−)$$

> **Yes but how?!**
> 
> Notice $(m_+−m_−)^Tw$ in $S_Bw=(m_+−m_−)(m_+−m_−)^Tw$ is a scalar. That means the equation looks like $S_Bw=c.(m_+−m_−)$. This shows that $S_Bw$ is always proportional to $(m_+−m_−)$ regardless of what $w$ is! Plug this into the equation above to get the generalized eigenvalue equation.

To summarize, Fisher's Discriminant,
- Gives the linear function with the maximum ratio of between-class scatter to within-class scatter
- The problem, e.g. classification, has been reduced from a d-dimensional problem to a more manageable one-dimensional problem.
- Can be extended to multiclass classification
