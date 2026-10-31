---
title: Image Stitching Snippets
tags: [computer-vision, image-stitching, homography, code-snippets, auto-captured]
draft: false
---
Everything needed to stitch two images, using OpenCV only to read files and to compute AKAZE features. Theory: [[Image Stitching]], [[Homographies and Perspective Warping]], [[AKAZE and Binary Descriptors]], [[RANSAC]]. Points are `(x, y)` = `(column, row)`; image arrays are indexed `[y, x]`.

## Keypoints and descriptors

```python
import cv2, numpy as np

def get_akaze(img):
    kps, desc = cv2.AKAZE_create().detectAndCompute(img, None)   # desc: N x 61 uint8 (488 bits)
    return np.array([k.pt for k in kps]), desc                    # (N, 2) locations

def expand_binary(desc):
    return np.unpackbits(desc, axis=1).astype(np.float32)         # N x 488, one 0/1 per bit
    # squared L2 distance between these rows == Hamming distance between the packed descriptors
```

In the OpenCV 5.0 alpha build, `AKAZE_create` was not exposed in the main module (it lives in the extra modules); 4.x has it.

## Matching with the ratio test

```python
def compute_distance(d1, d2):
    # squared Euclidean distances (N, M) via |a|^2 + |b|^2 - 2 a.b
    return (d1**2).sum(1)[:, None] + (d2**2).sum(1)[None, :] - 2 * d1 @ d2.T

def find_matches(d1, d2, ratio):
    dist = compute_distance(d1, d2)
    nn = np.argsort(dist, axis=1)[:, :2]                 # nearest and second nearest in image 2
    rows = np.arange(len(d1))
    best, second = dist[rows, nn[:, 0]], dist[rows, nn[:, 1]]
    keep = best / (second + 1e-8) < ratio                 # on squared distances: compare with SIFT's 0.8 via sqrt
    return np.column_stack([np.where(keep)[0], nn[keep, 0]])   # (K, 2) index pairs
```

For 15,000 x 11,000 keypoints the distance matrix is large; compute it once and reuse it while trying thresholds. Float matrix products may emit spurious overflow warnings on some builds, so check results.

## Homography fit and RANSAC

```python
def homography_transform(X, H):                          # X: (N, 2)
    Y = np.hstack([X, np.ones((len(X), 1))]) @ H.T
    return Y[:, :2] / Y[:, 2:3]

def fit_homography(XY):                                  # XY: (N, 4) rows [x, y, x', y']
    A = np.zeros((2 * len(XY), 9))
    for i, (x, y, xp, yp) in enumerate(XY):
        p = np.array([x, y, 1.0])
        A[2*i]   = np.concatenate([np.zeros(3), -p, yp * p])
        A[2*i+1] = np.concatenate([p, np.zeros(3), -xp * p])
    H = np.linalg.svd(A)[2][-1].reshape(3, 3)             # smallest singular vector
    if H[2, 2] == 0:
        raise ValueError("H[2,2] is zero")
    return H / H[2, 2]

def ransac_homography(XY, eps=1.0, n_iters=1000, seed=0):
    rng = np.random.default_rng(seed)
    best_count, best_inliers = -1, None
    for _ in range(n_iters):
        sample = XY[rng.choice(len(XY), 4, replace=False)]        # without replacement
        H = fit_homography(sample)
        err = np.linalg.norm(homography_transform(XY[:, :2], H) - XY[:, 2:], axis=1)
        inliers = err < eps
        if inliers.sum() > best_count:
            best_count, best_inliers = inliers.sum(), inliers
    return fit_homography(XY[best_inliers]), best_count        # refit on all inliers

# kps1, kps2: (N, 2) locations; matches: (K, 2) index pairs
XY = np.hstack([kps1[matches[:, 0]], kps2[matches[:, 1]]])
H, n_inliers = ransac_homography(XY, eps=5, n_iters=5000)       # H maps image 1 -> image 2
```

## Canvas size

```python
def find_canvas_size(img1, img2, H):
    h1, w1 = img1.shape[:2]; h2, w2 = img2.shape[:2]
    corners2 = np.array([[0, 0], [w2-1, 0], [w2-1, h2-1], [0, h2-1]], float)
    c = homography_transform(corners2, np.linalg.inv(H))       # image 2's corners in image 1's frame
    xs = np.append(c[:, 0], [0, w1-1]); ys = np.append(c[:, 1], [0, h1-1])
    xmin, xmax = int(np.floor(xs.min())), int(np.ceil(xs.max()))
    ymin, ymax = int(np.floor(ys.min())), int(np.ceil(ys.max()))
    return ymax - ymin + 1, xmax - xmin + 1, -xmin, -ymin       # height, width, offset_x, offset_y
```

## Warp and combine (vectorized)

```python
def warp_and_combine(img1, img2, H):
    h1, w1 = img1.shape[:2]; h2, w2 = img2.shape[:2]
    ch, cw, ox, oy = find_canvas_size(img1, img2, H)
    ys, xs = np.mgrid[0:ch, 0:cw]
    px, py = xs - ox, ys - oy                                    # canvas pixel in image 1's frame
    q = homography_transform(np.column_stack([px.ravel(), py.ravel()]).astype(float), H)
    sx, sy = q[:, 0], q[:, 1]                                    # same pixel in image 2's frame

    ok = (sx >= 0) & (sx <= w2 - 1) & (sy >= 0) & (sy <= h2 - 1)
    c0 = np.clip(np.floor(sx).astype(int), 0, w2 - 1); r0 = np.clip(np.floor(sy).astype(int), 0, h2 - 1)
    c1 = np.minimum(c0 + 1, w2 - 1);                    r1 = np.minimum(r0 + 1, h2 - 1)
    dc, dr = (sx - c0)[:, None], (sy - r0)[:, None]
    val = ((1-dr)*(1-dc)*img2[r0, c0] + (1-dr)*dc*img2[r0, c1]
           + dr*(1-dc)*img2[r1, c0] + dr*dc*img2[r1, c1])        # bilinear, all 3 channels at once

    V = np.zeros((ch * cw, 3), np.uint8)
    V[ok] = np.round(val[ok]).astype(np.uint8)                   # round, do not truncate
    inside1 = ((px >= 0) & (px < w1) & (py >= 0) & (py < h1)).ravel()
    V[inside1] = img1[py.ravel()[inside1].astype(int), px.ravel()[inside1].astype(int)]  # image 1 wins
    return V.reshape(ch, cw, 3)
```

On a 1000 x 750 pair this produced a 1481 x 1579 canvas in 0.4 s. On quarter-size copies it matched a per-pixel Python loop exactly (maximum difference 0 grey levels) and was about 30 times faster.

## Draw matches

```python
def draw_matches(img1, img2, kps1, kps2, matches):
    out = np.vstack([img1, img2]).copy()                       # image 2 below image 1
    for i, j in matches:
        x1, y1 = kps1[i]; x2, y2 = kps2[j]
        cv2.line(out, (int(x1), int(y1)), (int(x2), int(y2 + img1.shape[0])), (255, 0, 0), 1)
    return out
```

Debugging tip: build the two inputs as overlapping crops of one image (for example `I[100:400, 100:400]` and `I[150:450, 75:375]`). The true transform is then a pure translation, so the top-left 2 x 2 block of `H` must be close to the identity and `H[2, :2]` close to zero.

---
*Related:* [[Code Snippets MOC]], [[Computer Vision MOC]], [[Image Warping Snippets]]
