---
title: Image Borders and Padding
tags: [computer-vision, image-processing, filtering, padding, auto-captured]
draft: false
---
A filter with a $k \times k$ kernel needs $\tfrac{k-1}{2}$ pixels on every side of the pixel it is computing. Near the image border those pixels do not exist, so the algorithm must **decide what to put there**. That choice is small for smoothing but can produce fake edges and fake corners.

## Common Policies

| Policy | What the missing pixels are | Effect |
| ------ | --------------------------- | ------ |
| **Zero padding** | 0 (black) | Simple. Borders darken in blurs, and the jump from image to black looks like a strong edge. |
| **Replicate (edge)** | Copy of the nearest border pixel | No invented edge. Slightly biases the border towards its edge pixel. |
| **Reflect (mirror)** | Mirror image across the border | Keeps local texture and gradients continuous. |
| **Wrap (periodic)** | Pixels from the opposite side | Consistent with FFT-based filtering, rarely sensible for photos. |
| **Valid (crop)** | Nothing: skip positions that do not fit | Output is smaller, $(H-h+1) \times (W-w+1)$. |
| **Skip and leave unfiltered** | Loop only over interior pixels | Same size output, but a frame of untouched (often black) pixels remains. |

Output sizes for "valid", "same" and "full" are in [[Cross-Correlation and Convolution]].

## Zero Padding Creates False Edges

A derivative filter measures change. With zero padding, the pixel next to the border sees "bright image, then black", which is a large artificial step.

![[border-padding-artifacts.png]]

*Sobel gradient magnitude on a photograph. Zero padding raises the mean gradient in the outermost column to about 350, against about 100 with replicate padding and about 85 across the interior. From the second column on, the two policies agree.*

Consequences:

- **Edge detectors** ([[Image Gradients and the Sobel Operator]]) report a bright frame around the image.
- **Corner detectors** ([[Harris Corner Detector]]) report spurious corners along the border, since the artificial edge meets the real image edges.
- **Blurs** darken the border, because the kernel averages in zeros ([[Gaussian Filtering and Convolution]]).
- **Template matching** is unaffected as long as the search stays inside the image, since it uses valid positions ([[Template Matching]]).

## What to Do

- Prefer **replicate** or **reflect** for gradients and corner detection.
- If zero padding is required, **discard results within a margin** of the border equal to the kernel radius (plus the window radius for compound operators such as Harris).
- When an implementation skips the border, remember the unfiltered frame has width $\tfrac{k-1}{2}$: a 15 x 15 mean filter leaves a 7-pixel black frame.
- Zero padding is harmless when the image already fades to black, or when every object of interest is far from the edge.

*Gradient figures computed on a sample photograph with a 3 x 3 Sobel kernel under both padding modes.*

---
*Related:* [[Computer Vision MOC]], [[Cross-Correlation and Convolution]], [[Gaussian Filtering and Convolution]], [[Harris Corner Detector]]
