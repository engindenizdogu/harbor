---
title: Canny Edge Detector
tags: [computer-vision, edge-detection, gradients, auto-captured]
draft: false
---
The **Canny edge detector** (John Canny, 1986) turns an image into a map of **thin, connected, single-pixel-wide edges**. Thresholding the gradient magnitude alone ([[Image Gradients and the Sobel Operator]]) gives thick bands and ragged fragments. Canny adds three ideas to fix this: smooth first, thin the edges, and use two thresholds.

## The Pipeline

```mermaid
flowchart LR
    A[Gray image] --> B["1. Gaussian smoothing"]
    B --> C["2. Gradient magnitude and direction"]
    C --> D["3. Non-maximum suppression across the edge"]
    D --> E["4. Double threshold + hysteresis"]
    E --> F[Edge map]
```

1. **Smooth** with a Gaussian of scale $\sigma$ to suppress noise, since derivatives amplify it ([[Gaussian Filtering and Convolution]]). Larger $\sigma$ keeps only broad edges, smaller $\sigma$ keeps fine detail and noise.
2. **Compute the gradient** at each pixel, for example with Sobel: magnitude $\lVert\nabla I\rVert$ and direction $\theta = \operatorname{atan2}(G_y, G_x)$, which points **across** the edge. Steps 1 and 2 together are the derivative of a Gaussian.
3. **Non-maximum suppression (NMS).** A thick edge band has high gradient over several pixels. Keep a pixel only if its magnitude is the **largest along the gradient direction**, comparing it with the two neighbours on either side of the edge (the direction is rounded to 0, 45, 90 or 135 degrees). Everything else is set to zero, leaving a one-pixel-wide ridge.
4. **Hysteresis thresholding** with two thresholds $T_{high} > T_{low}$:
   - magnitude $\ge T_{high}$: **strong** edge pixel, always kept;
   - $T_{low} \le$ magnitude $< T_{high}$: **weak** pixel, kept **only if connected** (through other weak pixels) to a strong one;
   - magnitude $< T_{low}$: discarded.

## Why Two Thresholds?

| Single threshold | Problem |
| ---------------- | ------- |
| **High** | Only the clearest edges survive, and real edges break into fragments wherever the contrast dips |
| **Low** | Edges stay connected, but noise and texture produce many false edges |

Hysteresis gets the best of both: strong pixels act as **seeds** that vouch for the weak pixels along the same contour, while isolated weak pixels (noise) are dropped, since nothing strong vouches for them. A common rule of thumb is $T_{high} : T_{low}$ between 2:1 and 3:1.

**Example** with $T_{low} = 30$ and $T_{high} = 50$, along one contour whose gradient magnitudes are $20,\ 55,\ 40,\ 60,\ 25,\ 10$:

- $55$ and $60$ are strong, so they are kept.
- $40$ is weak but sits between two strong pixels, so it is kept.
- $25$ and $20$ are below $T_{low}$, and $10$ too: discarded.

## NMS Here vs. in Harris

The suppression direction differs from [[Harris Corner Detector]]. Canny's NMS is **one-dimensional, across the edge**, because an edge is a curve and we want to keep its ridge. Harris NMS is applied in **all directions**, because a corner is a single point ([[Non-Maximum Suppression]]).

## Parameters

| Parameter | Effect |
| --------- | ------ |
| $\sigma$ | Scale of the edges found, and noise suppression |
| $T_{high}$ | How strong an edge must be to start a contour |
| $T_{low}$ | How far a contour may continue through weaker pixels |

*Sources: Canny, A Computational Approach to Edge Detection, IEEE TPAMI, 1986; [Canny edge detector (Wikipedia)](https://en.wikipedia.org/wiki/Canny_edge_detector).*

---
*Related:* [[Computer Vision MOC]], [[Image Gradients and the Sobel Operator]], [[Non-Maximum Suppression]], [[Gaussian Filtering and Convolution]], [[Harris Corner Detector]]
