---
title: Image Basics Snippets
tags: [computer-vision, image-processing, numpy, code-snippets, auto-captured]
draft: false
---
Reading, slicing and modifying images with NumPy. Theory: [[Image Representation and Indexing]], [[Pixel-Level Operations]].

## Read and inspect

```python
import numpy as np
import mediapy as media           # or cv2.imread (BGR order!) / matplotlib.image.imread

img = media.read_image("photo.png")           # RGB, uint8
print(img.shape, img.dtype)                   # (H, W, 3) uint8
media.show_image(img)
```

## Slicing

```python
top_right = gray[0:200, -200:]                # rows 0-199, last 200 columns
window = gray[r-1:r+2, c-1:c+2]               # 3 x 3 window centred on row r, column c

masked = np.array(gray)                       # copy: a bare slice would modify gray itself
masked[20:140, 20:140] = 0                    # black square
masked[-200:, 0:200] = 0                      # black bottom-left corner
```

## Threshold

```python
# Loop version
out = np.zeros(gray.shape, dtype="uint8")
for i in range(gray.shape[0]):
    for j in range(gray.shape[1]):
        if gray[i, j] > 128:
            out[i, j] = 255

# Vectorized version
out = np.where(gray > 128, 255, 0).astype("uint8")
```

## Grayscale with luma weights

```python
gray = np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140]).astype("uint8")
```

## Colour mask

```python
mask = (rgb[..., 0] > 200) & (rgb[..., 1] > 100) & (rgb[..., 2] > 50)   # crude "orange"
out = rgb.copy()
out[mask] = [255, 0, 0]                       # paint selected pixels red
```

RGB boxes also catch yellows and near-whites. Thresholding the hue in HSV is more selective.

## Blend two images

```python
h = min(a.shape[0], b.shape[0])
w = min(a.shape[1], b.shape[1])
a, b = a[:h, :w], b[:h, :w]                   # crop to a common size
blend = (0.60 * a + 0.40 * b).astype("uint8") # float math, then back to uint8
```

## Mean (box) filter, loop version

```python
win = 15
half = win // 2
out = np.zeros(gray.shape, dtype="uint8")
for i in range(half, gray.shape[0] - half):
    for j in range(half, gray.shape[1] - half):
        window = gray[i-half:i+half+1, j-half:j+half+1]
        out[i, j] = window.sum() / (win * win)
```

This leaves an unfiltered black frame of width `half` around the image ([[Image Borders and Padding]]). Use an odd window size so the window has a centre pixel.

---
*Related:* [[Code Snippets MOC]], [[Computer Vision MOC]]
