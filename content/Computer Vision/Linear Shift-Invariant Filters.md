---
title: Linear Shift-Invariant Filters
tags: [computer-vision, image-processing, filtering, linear-algebra, auto-captured]
draft: false
---
Most basic image filters share two properties, **linearity** and **shift invariance**. Together they make a filter a **convolution**, and they explain why filters can be combined, reordered and made faster in so many useful ways.

## The Two Properties

| Property | Meaning |
| -------- | ------- |
| **Linearity** | $f(a I_1 + b I_2) = a\,f(I_1) + b\,f(I_2)$. This needs both **additivity** (filter of a sum is the sum of filters) and **homogeneity** (scaling the input scales the output) |
| **Shift invariance** | Shifting the input shifts the output by the same amount: the filter does the same thing at every position |

A filter with both is called **linear shift-invariant (LSI)**. The key theorem: **every LSI filter is a convolution with some kernel**, namely its response to a single bright pixel (the **impulse response**). So "LSI" and "convolution" describe the same class ([[Cross-Correlation and Convolution]]). Cross-correlation is the same operation with the kernel unflipped, so it is LSI as well.

## Which Filters Are Linear?

| Linear (LSI) | Not linear |
| ------------ | ---------- |
| Box blur, Gaussian blur ([[Gaussian Filtering and Convolution]]) | **Median filter** ([[Median Filter]]), and any max or min filter |
| Derivative filters, Sobel ([[Image Gradients and the Sobel Operator]]) | Gradient **magnitude** (it takes a square root) |
| Sharpening ([[Image Sharpening]]) | Thresholding, clipping, non-maximum suppression |

**Why the median is not linear.** Take two windows $A = (0, 0, 1)$ and $B = (0, 1, 0)$. Both have median $0$, so $\operatorname{med}(A) + \operatorname{med}(B) = 0$. But $A + B = (0, 1, 1)$ has median $1$. Additivity fails.

## Useful Consequences

Convolution is **commutative**, **associative** and **distributive** over addition, so for LSI filters the **order does not matter** and cascades can be merged:

- **Separability.** A 2D kernel that is an outer product of two 1D kernels, $K = \mathbf{u}\mathbf{v}^\top$, can be applied as two 1D passes. For an $N \times N$ image and $M \times M$ kernel the cost drops from $O(N^2 M^2)$ to $O(N^2 M)$. The Gaussian and Sobel kernels are separable.
- **Derivative of a Gaussian.** Smoothing then differentiating is one filter, $\partial_x(G_\sigma * I) = (\partial_x G_\sigma) * I$, which is the basis of the [[Canny Edge Detector]].
- **Cascaded Gaussians.** Blurring with $\sigma_1$ and then $\sigma_2$ equals one blur with $\sigma = \sqrt{\sigma_1^2 + \sigma_2^2}$, so scale space can be built by repeated small blurs ([[Scale Space and Difference of Gaussians]]).
- **Sharpening as one kernel.** $I + \alpha(I - G * I)$ collapses to $(1+\alpha)\delta - \alpha G$.
- **Linear filters pass through sums.** Filtering the sum of a signal and noise is filtering each separately, which is how the effect of a blur on noise can be analysed.

Note that only convolution is **commutative**. Cross-correlation is not, which matters when combining flipped kernels.

*Sources: Szeliski, [Computer Vision: Algorithms and Applications](https://szeliski.org/Book/), chapter on image processing (linear filtering); [Linear time-invariant system (Wikipedia)](https://en.wikipedia.org/wiki/Linear_time-invariant_system) for the same idea in 1D signals.*

---
*Related:* [[Computer Vision MOC]], [[Cross-Correlation and Convolution]], [[Gaussian Filtering and Convolution]], [[Median Filter]], [[Image Sharpening]]
