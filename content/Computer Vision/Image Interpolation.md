---
title: Image Interpolation
tags: [computer-vision, image-processing, interpolation, resampling, auto-captured]
draft: false
---
**Interpolation** estimates a value at a position where no sample exists, using the samples around it. Images are grids of samples, so any operation that moves pixels to non-integer positions, such as resizing, rotating or warping, needs it.

## Linear Interpolation (1D)

Between two known points $(x_0, y_0)$ and $(x_1, y_1)$, assume the value changes along a straight line:

$$y = (1 - t)\,y_0 + t\,y_1, \qquad t = \frac{x - x_0}{x_1 - x_0}, \quad t \in [0, 1]$$

The result is a **weighted average** of the two neighbours. At $t = 0.5$ it is the midpoint. Example: values 10 at $x = 2$ and 30 at $x = 6$ give $t = 0.25$ at $x = 3$, so $y = 0.75 \cdot 10 + 0.25 \cdot 30 = 15$.

## Bilinear Interpolation (2D)

Interpolate along x on the two surrounding rows, then along y between those two results. The output blends the **4 nearest pixels**. With fractional offsets $a$ (in x) and $b$ (in y) from the top-left neighbour $I_{00}$:

$$I(x, y) = (1-a)(1-b)\,I_{00} + a(1-b)\,I_{10} + (1-a)b\,I_{01} + ab\,I_{11}$$

```python
def bilinear(img, x, y):
    x0, y0 = int(np.floor(x)), int(np.floor(y))
    x1, y1 = min(x0 + 1, img.shape[1] - 1), min(y0 + 1, img.shape[0] - 1)
    a, b = x - x0, y - y0
    return ((1-a)*(1-b)*img[y0, x0] + a*(1-b)*img[y0, x1]
            + (1-a)*b*img[y1, x0] + a*b*img[y1, x1])
```

## Comparing the Methods

![[image-interpolation-comparison.png]]

*An 8 x 8 image enlarged 8x with three methods.*

| Method | Uses | Result | Cost |
| ------ | ---- | ------ | ---- |
| **Nearest neighbour** | The single closest pixel | Blocky, keeps exact original values | Cheapest |
| **Bilinear** | 4 neighbours | Smooth, slightly blurred | Low |
| **Bicubic** | 16 neighbours | Smoother and sharper than bilinear, can overshoot (ringing) | Higher |

Nearest neighbour is preferred when values must not be mixed, for example label maps where each number is a class.

## Resampling in Practice

- **Backward (inverse) mapping:** to resize or rotate, loop over the **output** pixels, compute the source position each one comes from, and interpolate there. Pushing source pixels forward instead leaves holes and overlaps.
- **Enlarging** (upsampling) needs interpolation to fill the new pixels. It cannot add real detail, only a smooth guess. The EXPAND step in [[Image Pyramids]] does exactly this.
- **Shrinking** (downsampling) is different: interpolation alone does not prevent **aliasing**, so low-pass filter first ([[Aliasing and Downsampling]]).
- Interpolation is itself a form of **convolution** with a small kernel: a triangle for linear, a cubic spline for bicubic ([[Cross-Correlation and Convolution]]). Doubling an image is the clearest case: insert zeros between the samples, then convolve with $[0.5, 1, 0.5]$ in each direction, which is bilinear interpolation.

*Source: [Foundations of Computer Vision, ch. 21: Downsampling and Upsampling Images](https://visionbook.mit.edu/upsamplig_downsampling_2.html).*

---
*Related:* [[Computer Vision MOC]], [[Image Warping]], [[Image Pyramids]], [[Aliasing and Downsampling]], [[Image Representation and Indexing]]
