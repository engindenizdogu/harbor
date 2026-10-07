---
title: Corner Detection Snippets
tags: [computer-vision, edge-detection, corners, image-processing, code-snippets, auto-captured]
draft: false
---
Sobel gradients, Harris response, 3 x 3 non-maximum suppression and corner overlays, written with plain NumPy loops for clarity. Theory: [[Image Gradients and the Sobel Operator]], [[Harris Corner Detector]], [[Non-Maximum Suppression]]. `filter_image` and `pad_input_wrt_filter` are in [[Template Matching Snippets]].

## Sobel operator

```python
def sobel_operator(image):
    Mx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])     # responds to vertical edges
    My = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])     # responds to horizontal edges
    Gx = filter_image(image, Mx)
    Gy = filter_image(image, My)
    return Gx, Gy, np.sqrt(Gx**2 + Gy**2)                   # magnitude

Gx, Gy, mag = sobel_operator(gray)
# display np.abs(Gx), np.abs(Gy), mag with cmap='gray'
```

Smooth first for less noise: `sobel_operator(filter_image(gray, generate_gaussian(2.0)))`.

## Harris response

```python
def harris_detector(image, window_size=5, alpha=0.04):
    response = np.zeros(image.shape)
    Ix, Iy, _ = sobel_operator(image)

    pad = lambda a: pad_input_wrt_filter(a, window_size, window_size)
    Ixx, Iyy, Ixy = pad(Ix * Ix), pad(Iy * Iy), pad(Ix * Iy)   # products of first derivatives

    window = np.ones((window_size, window_size))                # equal weights (box)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            m1 = np.sum(Ixx[y:y+window_size, x:x+window_size] * window)
            m2 = np.sum(Iyy[y:y+window_size, x:x+window_size] * window)
            m3 = np.sum(Ixy[y:y+window_size, x:x+window_size] * window)
            M = np.array([[m1, m3], [m3, m2]])                  # structure tensor
            response[y, x] = np.linalg.det(M) - alpha * np.trace(M) ** 2
    return response
```

The per-pixel loop is slow on large images. The same result comes from box-filtering the three product images once and computing `m1 * m2 - m3**2 - alpha * (m1 + m2)**2` on whole arrays.

## 3 x 3 non-maximum suppression with a relative threshold

```python
def nms(response, frac=0.1):
    threshold = frac * response.max()               # relative: the absolute scale varies with the image
    out = np.zeros_like(response)
    padded = pad_input_wrt_filter(response, 3, 3)   # zero-padding
    for y in range(response.shape[0]):
        for x in range(response.shape[1]):
            v = response[y, x]
            if v > threshold and v >= padded[y:y+3, x:x+3].max():   # centre is the neighbourhood max
                out[y, x] = v
    return out
```

On a photograph of 800 x 531 pixels, `frac = 0.01` gave about 2000 corners and `frac = 0.1` gave 241. Using `>=` keeps ties, so a flat plateau of equal responses can yield several adjacent corners.

## Corner overlay

```python
ys, xs = np.where(nms_result > 0)
binary = np.zeros(nms_result.shape, np.uint8)
overlay = np.stack([gray] * 3, axis=-1)             # gray image as RGB

for y, x in zip(ys, xs):                            # enlarge each corner to a 5 x 5 square
    y0, y1 = max(0, y - 2), min(gray.shape[0], y + 3)
    x0, x1 = max(0, x - 2), min(gray.shape[1], x + 3)
    binary[y0:y1, x0:x1] = 255
    overlay[y0:y1, x0:x1] = [255, 0, 0]
```

With zero padding, expect extra "corners" along the image border; drop detections within a few pixels of the edge or switch to replicate padding ([[Image Borders and Padding]]).

---
*Related:* [[Code Snippets MOC]], [[Computer Vision MOC]]
