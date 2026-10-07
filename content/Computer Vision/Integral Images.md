---
title: Integral Images
tags: [computer-vision, image-processing, algorithms, template-matching, auto-captured]
draft: false
---
An **integral image** (also called a **summed-area table**) stores, at each pixel, the sum of all pixels above and to the left of it. After one pass to build it, the sum over **any rectangle** costs exactly **four lookups**, no matter how large the rectangle is.

## Definition

For an image $i$, the integral image is

$$I(x, y) = \sum_{x' \le x,\; y' \le y} i(x', y')$$

It can be built in a single pass with the recurrence $I(x,y) = i(x,y) + I(x-1,y) + I(x,y-1) - I(x-1,y-1)$, or with two cumulative sums.

Worked example, a 4 x 4 image of the numbers 1 to 16 (padded with a zero row and column):

| | | | | |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 3 | 6 | 10 |
| 0 | 6 | 14 | 24 | 36 |
| 0 | 15 | 33 | 54 | 78 |
| 0 | 28 | 60 | 96 | 136 |

The bottom-right value 136 is the sum of all 16 pixels.

## Rectangle Sum in Four Lookups

For a rectangle with corners $A$ (top-left), $B$ (top-right), $C$ (bottom-left) and $D$ (bottom-right) in the padded table:

$$\sum_{\text{rect}} i = I(D) - I(B) - I(C) + I(A)$$

The sum is the big block ending at $D$, minus the strips above and to the left, plus the corner $A$ that was subtracted twice. The cost is independent of the rectangle size.

```python
def integral(img):
    ii = np.zeros((img.shape[0] + 1, img.shape[1] + 1))   # zero row and column in front
    ii[1:, 1:] = img.cumsum(0).cumsum(1)
    return ii

def rect_sum(ii, x, y, w, h):                             # top-left (x, y), size w x h
    return ii[y+h, x+w] - ii[y, x+w] - ii[y+h, x] + ii[y, x]
```

## Why It Matters for Template Matching

In [[Template Matching]] each window needs its **mean** and its **sum of squares** (for the NCC normalization). Those depend only on rectangle sums, so two integral images, one of $f$ and one of $f^2$, give every window's mean and norm in constant time per window. The remaining cross term $\sum W \cdot T$ is a correlation and is sped up with an FFT instead.

Other well-known uses:

- **Viola-Jones face detection** evaluates thousands of rectangular (Haar-like) features per window in constant time each.
- **SURF** uses it to approximate Gaussian derivative filters with box filters.
- **Box blur** of any radius at constant cost per pixel.

*Sources: [Summed-area table (Wikipedia)](https://en.wikipedia.org/wiki/Summed-area_table). The 4 x 4 example and code were checked against a direct sum.*

---
*Related:* [[Computer Vision MOC]], [[Template Matching]], [[Cross-Correlation and Convolution]]
