---
title: Image Warping Snippets
tags: [computer-vision, image-processing, geometry, code-snippets, auto-captured]
draft: false
---
Transformation matrices, inverse warping with bilinear sampling, affine and homography estimation, and a cylindrical warp, in plain NumPy. Theory: [[Image Warping]], [[Homographies and Perspective Warping]], [[Cylindrical Warping]]. Images are float or uint8 arrays of shape `(H, W, C)`.

## Transformation matrices

```python
def translation(tx, ty):
    return np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1.]])

def rotation(theta):                         # radians; y axis points down in images
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.]])

def scaling(sx, sy):
    return np.diag([sx, sy, 1.])             # sx == sy: uniform

def shear(h):
    return np.array([[1, h, 0], [0, 1, 0], [0, 0, 1.]])

def about_point(M, cx, cy):                  # apply M about (cx, cy) instead of the origin
    return translation(cx, cy) @ M @ translation(-cx, -cy)

# Matrices apply right to left: scale first, then rotate, then translate
M = translation(40, 25) @ about_point(rotation(np.deg2rad(30)), 100, 100) @ scaling(0.8, 0.8)
```

## Inverse warping with bilinear sampling

```python
def sample_bilinear(img, sx, sy, fill=255):
    # sx, sy: float source positions (flat arrays); positions outside the image get `fill`
    h, w = img.shape[:2]
    x0, y0 = np.floor(sx).astype(int), np.floor(sy).astype(int)
    a, b = (sx - x0)[:, None], (sy - y0)[:, None]
    inside = (sx >= 0) & (sx <= w - 1) & (sy >= 0) & (sy <= h - 1)
    x0c, x1 = np.clip(x0, 0, w - 1), np.clip(x0 + 1, 0, w - 1)
    y0c, y1 = np.clip(y0, 0, h - 1), np.clip(y0 + 1, 0, h - 1)
    out = ((1-a)*(1-b)*img[y0c, x0c] + a*(1-b)*img[y0c, x1]
           + (1-a)*b*img[y1, x0c] + a*b*img[y1, x1])
    out[~inside] = fill
    return out

def warp(img, M, out_shape, fill=255):
    # For each OUTPUT pixel find its source with M^-1 (a homography needs the divide by w)
    H, W = out_shape
    ys, xs = np.mgrid[0:H, 0:W]
    pts = np.stack([xs.ravel(), ys.ravel(), np.ones(H * W)])
    q = np.linalg.inv(M) @ pts
    out = sample_bilinear(img.astype(float), q[0] / q[2], q[1] / q[2], fill)
    return out.reshape(H, W, -1).astype(np.uint8)
```

Output size for a transformed image: map the four corners with `M`, take the min and max of x and y, and prepend a translation by `(-min_x, -min_y)` so nothing lands at negative coordinates.

## Estimate an affine transform from 3 or more point pairs

```python
def estimate_affine(src_pts, dst_pts):
    # Solves [x y 1] * P = [u v] in the least-squares sense; 3 non-collinear pairs are exact
    A = np.hstack([np.asarray(src_pts, float), np.ones((len(src_pts), 1))])
    P, *_ = np.linalg.lstsq(A, np.asarray(dst_pts, float), rcond=None)
    return np.vstack([P.T, [0, 0, 1]])                  # 3 x 3
```

## Estimate a homography (DLT)

```python
def estimate_homography(src_pts, dst_pts):
    # 4 pairs are exact; more pairs give a least-squares fit. Normalise coordinates first for noisy data.
    A = []
    for (x, y), (u, v) in zip(src_pts, dst_pts):
        A.append([x, y, 1, 0, 0, 0, -u*x, -u*y, -u])
        A.append([0, 0, 0, x, y, 1, -v*x, -v*y, -v])
    _, _, vt = np.linalg.svd(np.array(A, float))
    H = vt[-1].reshape(3, 3)                            # smallest singular vector
    return H / H[2, 2]
```

With wrong matches in the pairs, wrap the 4-point solve in [[RANSAC Snippets]]-style sampling. To rectify, map the four detected corners to the corners of a rectangle and call `warp` with the resulting matrix.

## Cylindrical warp

```python
def cylindrical_warp(img, f):
    # f: focal length in pixels; coordinates measured from the image centre
    h, w = img.shape[:2]
    ys, xs = np.mgrid[0:h, 0:w]
    xp, yp = xs - w / 2, ys - h / 2                     # cylinder coordinates (x', y')
    sx = f * np.tan(xp / f) + w / 2                     # source position (inverse mapping)
    sy = yp / np.cos(xp / f) + h / 2
    out = sample_bilinear(img.astype(float), sx.ravel(), sy.ravel())
    return out.reshape(h, w, -1).astype(np.uint8)
```

Forward formulas, for reference: `x' = f * arctan(x / f)` and `y' = f * y / sqrt(x**2 + f**2)`. Estimate `f` from the field of view with `f = (W / 2) / tan(FOV / 2)`.

---
*Related:* [[Code Snippets MOC]], [[Computer Vision MOC]], [[Image Interpolation]]
