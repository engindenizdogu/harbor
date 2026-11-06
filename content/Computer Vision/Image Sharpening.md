---
title: Image Sharpening
tags: [computer-vision, image-processing, filtering, sharpening, auto-captured]
draft: false
---
**Sharpening** makes edges and fine detail more pronounced. It does **not** remove noise, and it usually amplifies it. The standard method is **unsharp masking**, named after a darkroom technique that subtracted a blurred ("unsharp") copy of the photograph.

## The Idea: Add Back the Details

Blurring removes fine detail, so the difference between an image and its blurred copy **is** the detail. Add some of that detail back:

$$\text{detail} = I - G_\sigma * I, \qquad I_{sharp} = I + \alpha\,(I - G_\sigma * I)$$

- $G_\sigma * I$ is a Gaussian-blurred copy ([[Gaussian Filtering and Convolution]]).
- $\alpha$ controls the **strength**: $\alpha = 0$ leaves the image unchanged, larger values exaggerate edges.
- $\sigma$ controls the **size of the detail** that is boosted: a small $\sigma$ sharpens fine texture, a large $\sigma$ boosts broad edges and local contrast.

Rearranging gives two equivalent views:

$$I_{sharp} = (1 + \alpha)\,I - \alpha\,(G_\sigma * I)$$

so it is a "double-weight identity minus a blur", and because convolution is linear it collapses into **one kernel**, $(1+\alpha)\,\delta - \alpha\,G_\sigma$, where $\delta$ is the identity (impulse) kernel ([[Linear Shift-Invariant Filters]]).

**Example** with a $3 \times 3$ box blur and $\alpha = 1$: the center weight is $2 - \tfrac{1}{9} = \tfrac{17}{9}$ and the eight others are $-\tfrac{1}{9}$:

$$\frac{1}{9}\begin{pmatrix} -1 & -1 & -1 \\ -1 & 17 & -1 \\ -1 & -1 & -1 \end{pmatrix}$$

The weights sum to 1, so flat regions keep their brightness. Only places where a pixel differs from its neighbourhood change.

## Why It Works

In a flat region the blur equals the image, so the detail is zero and nothing changes. Across an edge the detail is positive on the bright side and negative on the dark side, which makes the bright side brighter and the dark side darker. The edge looks steeper, so it appears sharper.

The detail image $I - G_\sigma * I$ is a **band-pass** response. It is the negative of a difference of Gaussians (one level blurred by $\sigma$, the other not blurred at all), and a difference of Gaussians approximates the Laplacian ([[Scale Space and Difference of Gaussians]]), so the detail behaves like a negative Laplacian: it responds only to local change.

## Pitfalls

| Issue | Why |
| ----- | --- |
| **Noise is amplified** | Noise lives in the fine detail that is being boosted. Blur lightly first, or keep $\alpha$ small ([[Image Noise]]). |
| **Halos** | Large $\alpha$ overshoots on both sides of a strong edge, creating bright and dark bands. |
| **Clipping and overflow** | The result can leave $[0, 255]$. Compute in float and clip before converting back ([[Data Types in Image Processing]]). |
| **Confusion with denoising** | Sharpening makes noise worse. Removing noise needs smoothing or a [[Median Filter]]. |

```python
import numpy as np
from scipy.ndimage import gaussian_filter

def sharpen(img, sigma=1.5, alpha=1.0):
    f = img.astype(np.float32)
    detail = f - gaussian_filter(f, sigma)
    return np.clip(f + alpha * detail, 0, 255).astype(np.uint8)
```

*Sources: [Unsharp masking (Wikipedia)](https://en.wikipedia.org/wiki/Unsharp_masking). The 3 x 3 kernel is derived from the formula above.*

---
*Related:* [[Computer Vision MOC]], [[Gaussian Filtering and Convolution]], [[Linear Shift-Invariant Filters]], [[Cross-Correlation and Convolution]], [[Scale Space and Difference of Gaussians]]
