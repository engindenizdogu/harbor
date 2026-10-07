---
title: Image Noise
tags: [computer-vision, image-processing, noise, auto-captured]
draft: false
---
**Image noise** is random variation in pixel values that does not come from the scene. Different noise processes call for different filters, so recognising the type is the first step in removing it.

## Common Noise Models

| Type | Model | Typical cause | Looks like | Good filter |
| ---- | ----- | ------------- | ---------- | ----------- |
| **Gaussian** (additive) | $I' = I + n,\; n \sim \mathcal N(0, \sigma^2)$ | Sensor and electronics noise | Fine grain over every pixel | Gaussian blur, averaging |
| **Salt-and-pepper** (impulse) | Each pixel set to 0 or 255 with some probability, others untouched | Dead or stuck pixels, transmission errors | Isolated black and white dots | **Median filter** |
| **Poisson** (shot) | Variance grows with the signal | Photon counting in low light | Grainier in dark regions | Variance-stabilizing transforms, then Gaussian-style denoising |
| **Speckle** (multiplicative) | $I' = I\,(1 + n)$ | Ultrasound, radar | Granular texture scaled by intensity | Specialised speckle filters |

Gaussian noise corrupts **every** pixel by a small amount, so averaging cancels it. Salt-and-pepper corrupts a **fraction** of pixels by a huge amount, so averaging smears the outliers and the median ignores them ([[Median Filter]]).

## Simulating Salt-and-Pepper Noise

A common recipe corrupts an image with two independent masks, each at rate $p$ (for example $p = 0.05\,i$ for noise level $i$):

```python
img[np.random.random(img.shape) < p] = 0          # pepper: black pixels
img[np.random.random(img.shape) > 1 - p] = 255    # salt: white pixels
```

A full generation loop is in [[Template Matching Snippets]]. Because the masks are independent, the fraction of corrupted pixels is about $1 - (1-p)^2$, so the "40%" label is about 64% corrupted. See [[Median Filter]] for the full conversion table and [[Template Matching]] for how SAD and NCC cope.

## Noise Is Not a Brightness or Contrast Change

An affine intensity change $I' = aI + b$ is a **global, deterministic** transformation. Noise is **random and local**. That is why NCC's invariance to $a$ and $b$ does not explain why it tolerates salt-and-pepper noise better than SAD; its advantage there is that it compares the pattern across the window.

*Source: [Image noise (Wikipedia)](https://en.wikipedia.org/wiki/Image_noise).*

---
*Related:* [[Computer Vision MOC]], [[Median Filter]], [[Gaussian Filtering and Convolution]], [[Template Matching]]
