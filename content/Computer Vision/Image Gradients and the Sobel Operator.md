---
title: Image Gradients and the Sobel Operator
tags: [computer-vision, image-processing, edge-detection, gradients, auto-captured]
draft: false
---
An **edge** is a place where intensity changes sharply. The **image gradient** measures that change: at each pixel it is a vector pointing toward the steepest increase in brightness. Edges, corners ([[Harris Corner Detector]]) and most feature detectors are built on gradients.

## The Gradient

$$\nabla I = \begin{pmatrix} \partial I / \partial x \\ \partial I / \partial y \end{pmatrix} = \begin{pmatrix} G_x \\ G_y \end{pmatrix}, \qquad
\lVert \nabla I \rVert = \sqrt{G_x^2 + G_y^2}, \qquad
\theta = \operatorname{atan2}(G_y, G_x)$$

- **Magnitude** says how strong the edge is.
- **Direction** $\theta$ points across the edge, perpendicular to it.
- A cheaper approximation of the magnitude is $|G_x| + |G_y|$.

On discrete images derivatives are **finite differences**, which are computed by correlating the image with a small kernel ([[Cross-Correlation and Convolution]]).

## Sobel Kernels

$$S_x = \begin{pmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{pmatrix}, \qquad
S_y = \begin{pmatrix} 1 & 2 & 1 \\ 0 & 0 & 0 \\ -1 & -2 & -1 \end{pmatrix}$$

![[sobel-gradients-example.png]]

*Absolute Sobel responses on a photograph. The two responses highlight different edge orientations, and the magnitude combines them.*

**Which kernel finds which edge?** $S_x$ subtracts the pixels on its left from those on its right, so it responds to intensity change **along x**: it fires on **vertical edges**. $S_y$ differences up against down, so it fires on **horizontal edges**. A quick test: a kernel whose columns are antisymmetric, `-1 0 1` across, is a horizontal derivative, hence a vertical-edge detector. The sign of the response depends on correlation vs. convolution and on whether $y$ points down, which is why the **absolute value** is displayed and the magnitude is unaffected.

### Why it works well

- Each kernel is **separable**: $S_x = \begin{pmatrix}1\\2\\1\end{pmatrix} \begin{pmatrix}-1 & 0 & 1\end{pmatrix}$. It differentiates along one axis and **smooths** along the other with weights $[1, 2, 1]$.
- Smoothing makes it less noise-sensitive than a bare difference `[-1, 1]`.
- Divide by 8 to get a true derivative estimate in intensity units per pixel.
- Flat regions give zero response, because each kernel's weights **sum to zero** ([[Gaussian Filtering and Convolution]]).

## Smooth First, Then Differentiate

Derivatives amplify noise: a single noisy pixel creates a large local difference. Pre-blurring with a Gaussian suppresses it, at the cost of fine edges. The scale $\sigma$ sets which structures survive:

| Smoothing | Result |
| --------- | ------ |
| None or small $\sigma$ | Many thin, noisy edges, including texture |
| Moderate $\sigma$ | Clean edges of the main structures |
| Large $\sigma$ | Only the broad outlines, with blurred locations |

Because convolution is associative, Gaussian smoothing followed by a derivative equals one filter, the **derivative of a Gaussian**. Border handling matters too: zero padding produces a false bright frame ([[Image Borders and Padding]]).

## From Gradients to Edge Maps

Thresholding the magnitude gives thick edge bands. Thin, connected edges need extra steps, as in the Canny detector: smoothing, gradient, **non-maximum suppression** across the edge direction ([[Non-Maximum Suppression]]), and hysteresis thresholding.

*Source: [Sobel operator (Wikipedia)](https://en.wikipedia.org/wiki/Sobel_operator).*

---
*Related:* [[Computer Vision MOC]], [[Harris Corner Detector]], [[Cross-Correlation and Convolution]], [[Corner Detection Snippets]]
