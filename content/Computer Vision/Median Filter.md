---
title: Median Filter
tags: [computer-vision, image-processing, filtering, noise, auto-captured]
draft: false
---
The **median filter** replaces each pixel with the **median** of its k x k neighbourhood. Unlike the Gaussian in [[Gaussian Filtering and Convolution]], it is a **non-linear** filter: it sorts the window instead of taking a weighted sum.

## Why It Suits Salt-and-Pepper Noise

Salt-and-pepper corruption sets pixels to extreme values (0 or 255). The median ignores outliers, whereas a Gaussian averages them in and smears them into their neighbours.

Worked example on a 3 x 3 window whose values are 10, 12, 255, 11, 0, 13, 12, 9, 11:

| Filter | Computation | Output |
| ------ | ----------- | ------ |
| Mean (box blur) | $333 / 9$ | **37**, dragged far from the true level of about 11 by the 255 and the 0 |
| Median | sorted: 0, 9, 10, 11, 11, 12, 12, 13, 255 | **11** |

Denoising *before* matching is therefore a natural fix for the failures in [[Template Matching]]. SAD would plausibly hold up much longer after a median filter, but this is a hypothesis that was not tested.

## Limits

- **It cannot fully recover the image.** It does not know which pixels are corrupted, so it also changes clean pixels, and the original values are lost. It is not invertible.
- **It loses fine detail.** Thin lines, sharp corners and small features get rounded or removed, because the median treats them like outliers.
- **It breaks down at high noise density.** The median is robust only while **fewer than half** of the window's pixels are corrupted. Past that, the median itself is a 0 or 255 and the output stays noisy. A bigger window helps but blurs more.

## When Does the Median Keep the Maximum?

In a $3 \times 3$ window the median is the **5th smallest of 9 values**. It equals the window's maximum only if the maximum value occupies **at least 5 of the 9 pixels**, meaning more than half of the window. Examples: a window inside a flat bright region, or a window on a straight edge where at least 5 pixels belong to the bright side. A lone bright pixel (a single outlier or a thin line) is never preserved, which is exactly why thin features are removed.

## Check the Noise Labels

In a common simulation recipe (used in the worked example in [[Template Matching]]), noise is added with two **independent** masks, one for salt and one for pepper, each at rate $p = 0.05\,i$. A pixel is hit if either mask selects it, so the corrupted fraction is about

$$1 - (1 - p)^2$$

which is roughly double the label for small $p$:

| Noise label | Rate per mask $p$ | Approx. total corrupted |
| ------------------- | ----------------- | ----------------------- |
| 10% (i = 2) | 0.10 | 19% |
| 20% (i = 4) | 0.20 | 36% |
| 30% (i = 6) | 0.30 | 51% |
| 40% (i = 8) | 0.40 | 64% |
| 50% (i = 10) | 0.50 | 75% |
| 60% (i = 12) | 0.60 | 84% |
| 70% (i = 14) | 0.70 | 91% |
| 80% (i = 16) | 0.80 | 96% |

At the "40%" label about 64% of pixels are corrupted, already **past the median's 50% limit**. Pixels that were already 0 or 255 are unchanged by the masks, so the visible damage is slightly lower than the table, especially on a mostly white background (reasoning, not measured).

This also reframes the experiment: SAD failed at a label of 40% (about 64% corrupted) and NCC at 60% (about 84% corrupted).

## Checklist

- Median removes outliers well but loses detail, changes clean pixels too, and fails above 50% corruption in the window.
- A 3 x 3 median keeps the window maximum only when that value fills at least 5 of the 9 pixels.
- The noise labels are per mask, so the real corrupted fraction is about double.

---
*Related:* [[Computer Vision MOC]], [[Image Noise]], [[Template Matching]], [[Gaussian Filtering and Convolution]]
