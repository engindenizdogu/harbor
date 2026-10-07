---
title: Harris Corner Detector
tags: [computer-vision, feature-detection, corners, auto-captured]
draft: false
---
A **corner** is a point where the image changes strongly in **every** direction. Corners are good landmarks: they can be located precisely and found again in another view of the same scene, which makes them the first step of image matching, tracking and 3D reconstruction. The **Harris detector** (Harris and Stephens, 1988) finds them from image gradients.

## Intuition: Shift a Small Window

Slide a small window by $(u, v)$ and measure how much its contents change:

| Region | What happens when the window shifts | Verdict |
| ------ | ------------------------------------ | ------- |
| **Flat** | No change in any direction | Not distinctive |
| **Edge** | No change along the edge, large change across it | Ambiguous along the edge |
| **Corner** | Large change in every direction | Distinctive |

## The Structure Tensor

For small shifts the change is described by the **structure tensor** (second-moment matrix), built from the image derivatives $I_x, I_y$ ([[Image Gradients and the Sobel Operator]]) and summed over a window with weights $w$:

$$M = \sum_{(x, y) \in \text{window}} w(x, y) \begin{pmatrix} I_x^2 & I_x I_y \\ I_x I_y & I_y^2 \end{pmatrix}$$

The products $I_x^2$, $I_y^2$, $I_x I_y$ are **products of first derivatives**, not second derivatives. The eigenvalues $\lambda_1 \ge \lambda_2$ of $M$ tell the regions apart:

| $\lambda_1$ | $\lambda_2$ | Region |
| ----------- | ----------- | ------ |
| small | small | Flat |
| large | small | Edge |
| large | large | **Corner** |

## The Response Function

Computing eigenvalues per pixel is costly, so Harris uses a score that needs only the determinant and trace:

$$R = \det(M) - k\,\operatorname{trace}(M)^2 = \lambda_1 \lambda_2 - k\,(\lambda_1 + \lambda_2)^2$$

with $\det(M) = I_{xx} I_{yy} - I_{xy}^2$ built from the window sums, and $k \approx 0.04$ to $0.06$.

- $R$ **large and positive:** corner.
- $R$ **negative:** edge (one eigenvalue dominates).
- $|R|$ **small:** flat region.

## Algorithm

```mermaid
flowchart LR
    A[Gray image] --> B["Gradients Ix, Iy (Sobel)"]
    B --> C["Products Ix², Iy², IxIy"]
    C --> D["Sum over a window to get M"]
    D --> E["Response R = det M - k trace² M"]
    E --> F[Threshold]
    F --> G["Non-maximum suppression (3x3)"]
    G --> H[Corner list]
```

1. Compute $I_x$ and $I_y$ (optionally after Gaussian smoothing).
2. Form $I_x^2$, $I_y^2$ and $I_x I_y$ at every pixel.
3. Sum each over a window (for example $5 \times 5$) to get the entries of $M$.
4. Compute $R$ at every pixel.
5. **Threshold** $R$, then apply **non-maximum suppression** so each corner is one pixel instead of a blob ([[Non-Maximum Suppression]]).

![[harris-corner-pipeline.png]]

*Harris on a photograph with a $5 \times 5$ box window and a threshold of 10% of the maximum response. 241 corners survive 3 x 3 suppression. The edge of the image also attracts corners, which is a border artifact ([[Image Borders and Padding]]).*

## Parameters

| Parameter | Effect |
| --------- | ------ |
| Window size and weights | Larger windows give smoother, more robust responses with slightly worse localization. A **Gaussian** window is smoother and more rotation-invariant than a box window. |
| $k$ | Larger $k$ penalizes edges more and keeps fewer, stronger corners. |
| Threshold | Controls how many corners are kept. It is best set **relative to the maximum** of $R$, since the absolute scale depends on image contrast and can be around $10^{13}$. |
| Pre-smoothing $\sigma$ | Suppresses noise-induced corners. |

How the threshold sets the corner count (same photograph as above, 800 x 531, thresholds as a fraction of the maximum $R$):

| Threshold | Corners after 3 x 3 NMS |
| --------- | ----------------------- |
| 1% | about 2000 |
| 5% | about 570 |
| 10% | **241** |
| 20% | about 67 |

A common target is 100 to 300 corners per image.

## Properties and Limits

- **Rotation invariant:** the eigenvalues of $M$ do not change when the image rotates.
- **Robust to additive brightness change**, since derivatives ignore a constant offset. Scaling contrast changes $R$ (it scales with the fourth power of the gain), which is why the threshold is relative.
- **Not scale invariant:** a corner at one scale looks like a curved edge at a coarser one. Multi-scale detectors search over a scale space ([[Image Pyramids]]), and later detectors such as [[SIFT]] build on this idea ([[Scale Space and Difference of Gaussians]]).
- **Computation:** a naive per-pixel loop with a $k \times k$ window costs $O(HWk^2)$, and the box sums are a classic use of [[Integral Images]].

*Sources: [Harris corner detector (Wikipedia)](https://en.wikipedia.org/wiki/Harris_corner_detector); Harris and Stephens, A Combined Corner and Edge Detector, 1988. The threshold sweep is my own measurement on the example photograph.*

---
*Related:* [[Computer Vision MOC]], [[Image Gradients and the Sobel Operator]], [[Non-Maximum Suppression]], [[Corner Detection Snippets]]
