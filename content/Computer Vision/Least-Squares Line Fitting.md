---
title: Least-Squares Line Fitting
tags: [computer-vision, model-fitting, least-squares, linear-algebra, auto-captured]
draft: false
---
**Line fitting** finds the line that best explains a cloud of 2D points. "Best" is defined by an error measure, and two common choices behave quite differently.

## Two Ways to Measure Error

| Method | Line model | What is minimized | Notes |
| ------ | ---------- | ----------------- | ----- |
| **Ordinary least squares (OLS)** | $y = mx + b$ | **Vertical** distances $\sum (y_i - m x_i - b)^2$ | Closed form. Cannot represent vertical lines. Assumes x is exact. |
| **Total least squares (TLS)** | $ax + by + c = 0$ with $a^2 + b^2 = 1$ | **Perpendicular** distances | Treats x and y symmetrically. Handles any orientation. |

For image points both coordinates are measured with noise and lines can be at any angle, so TLS is the natural choice.

## Total Least Squares via SVD

With a unit normal $\mathbf n = (a, b)$, the signed distance of a point $\mathbf p$ from the line is simply

$$d(\mathbf p) = a x + b y + c$$

so the squared error is $\sum d_i^2$. The solution has two parts:

1. The best line **passes through the centroid** $\bar{\mathbf p}$ of the points.
2. Center the data, $X = [\,\mathbf p_i - \bar{\mathbf p}\,]$ (an $n \times 2$ matrix), and take its **SVD**, $X = U \Sigma V^\top$. The first right singular vector (first row of $V^\top$) is the **direction** of greatest spread, the line's tangent. The **second** is the **normal** $\mathbf n$, direction of least spread.
3. Set $c = -\mathbf n \cdot \bar{\mathbf p}$.

```python
def fit_line(points):                      # points: n x 2
    mean = points.mean(axis=0)
    _, s, vt = np.linalg.svd(points - mean)
    a, b = vt[1]                           # normal = direction of least variance
    c = -(a * mean[0] + b * mean[1])
    return np.array([a, b, c])             # ax + by + c = 0, with a^2 + b^2 = 1
```

Two points give an exact line, so two is the **minimum sample** for a line. The singular values `s` are a quality measure: a tiny second value means the points are nearly collinear.

**Worked check:** points sampled without noise from $3x + y + 5 = 0$ recover exactly $(a, b, c) = (0.9487,\ 0.3162,\ 1.5811)$, which is $(3, 1, 5)$ divided by $\sqrt{10}$. A sign flip of all three numbers describes the same line.

## The Weakness: Outliers

Squared error punishes large residuals heavily, so a handful of points far from the line can drag the fit away from the true structure. A single arbitrarily bad point can move the result arbitrarily far (**breakdown point 0**).

![[ransac-vs-least-squares.png]]

*100 points on a noisy line plus 100 uniformly scattered outliers. The least-squares line (dashed) is pulled far off the true line by the outliers; RANSAC ignores them ([[RANSAC]]).*

Robust alternatives either downweight outliers (M-estimators, Huber loss), minimize a median of residuals, or search for a consensus set as in [[RANSAC]].

---
*Related:* [[Computer Vision MOC]], [[RANSAC]], [[RANSAC Snippets]]
