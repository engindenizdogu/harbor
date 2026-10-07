---
title: Cross-Correlation and Convolution
tags: [computer-vision, image-processing, filtering, convolution, auto-captured]
draft: false
---
Both operations slide a small array (the **kernel** or **template**) over an image and compute a weighted sum at each position. They differ in one detail: **convolution flips the kernel first, correlation does not.**

## Definitions (2D, discrete)

$$\begin{aligned}
\text{Cross-correlation:}\quad (f \star h)[y, x] &= \sum_{k, l} f[y + l,\, x + k]\; h[l, k] \\
\text{Convolution:}\quad (f * h)[y, x] &= \sum_{k, l} f[y - l,\, x - k]\; h[l, k]
\end{aligned}$$

Convolution is the same as correlation with the kernel rotated by 180 degrees.

| | Cross-correlation | Convolution |
| --- | --- | --- |
| Kernel flipped | No | Yes |
| Commutative, associative | No | **Yes** |
| Natural use | **Matching** a pattern ("how similar is this window to the template?") | **Filtering** and building up filters (blur then derivative equals one combined filter) |
| Symmetric kernel (e.g. Gaussian) | Same result | Same result |

## Where Each Shows Up

- **Template matching** is correlation. SAD, SSD and NCC are variations on comparing a window with the template at the same orientation ([[Template Matching]]). The NCC numerator is a correlation of the zero-mean patches.
- A direct filtering loop that multiplies the window and the kernel without flipping (see [[Template Matching Snippets]]) technically computes **correlation**. The Gaussian is symmetric, so the result equals true convolution ([[Gaussian Filtering and Convolution]]).
- **Convolutional neural networks** compute cross-correlation too, even though the layers are called "convolutions". The kernel is learned, so flipping it would change nothing.

## Border Handling and Output Size

For an $H \times W$ image and an $h \times w$ kernel:

| Mode | Output size | Notes |
| ---- | ----------- | ----- |
| **valid** | $(H-h+1) \times (W-w+1)$ | Only positions where the kernel fully fits. This is the template-matching score map. |
| **same** | $H \times W$ | Pad by $(h-1)/2$ and $(w-1)/2$. With zero-padding, borders get darker. |
| **full** | $(H+h-1) \times (W+w-1)$ | Every position with any overlap. |

## Cost and the FFT

Direct computation costs $O(HWhw)$. The **convolution theorem** says convolution in the image domain is a pointwise product in the frequency domain, so large kernels or templates are faster through the **FFT**: transform both, multiply, transform back, at about $O(HW \log HW)$ regardless of kernel size. For separable kernels such as the Gaussian, two 1D passes are cheaper still. Fast window statistics come from [[Integral Images]].

*Source: [Cross-correlation (Wikipedia)](https://en.wikipedia.org/wiki/Cross-correlation).*

---
*Related:* [[Computer Vision MOC]], [[Template Matching]], [[Gaussian Filtering and Convolution]], [[Integral Images]]
