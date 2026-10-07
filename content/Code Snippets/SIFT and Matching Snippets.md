---
title: SIFT and Matching Snippets
tags: [computer-vision, feature-detection, feature-matching, sift, code-snippets, auto-captured]
draft: false
---
Detecting SIFT keypoints with OpenCV, matching descriptors with the ratio test, verifying with RANSAC, and a from-scratch ratio-test matcher and DoG detector. Theory: [[SIFT]], [[Feature Matching]], [[Scale Space and Difference of Gaussians]].

## Detect and describe (OpenCV)

```python
import cv2

gray = cv2.imread("photo.jpg", cv2.IMREAD_GRAYSCALE)
sift = cv2.SIFT_create()                        # included in OpenCV 4.4 and later
keypoints, desc = sift.detectAndCompute(gray, None)   # desc: N x 128, float32

kp = keypoints[0]
print(kp.pt, kp.size, kp.angle)                 # position (x, y), scale (diameter), orientation in degrees

vis = cv2.drawKeypoints(gray, keypoints, None,
                        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)   # circles show scale and angle
```

## Ratio test and RANSAC (OpenCV)

```python
kp1, d1 = sift.detectAndCompute(img1, None)
kp2, d2 = sift.detectAndCompute(img2, None)

knn = cv2.BFMatcher(cv2.NORM_L2).knnMatch(d1, d2, k=2)       # two nearest neighbours per descriptor
good = [m for m, n in knn if m.distance < 0.8 * n.distance]  # ratio test

src = np.float32([kp1[m.queryIdx].pt for m in good])
dst = np.float32([kp2[m.trainIdx].pt for m in good])
H, mask = cv2.findHomography(src, dst, cv2.RANSAC, 3.0)      # 3 pixel inlier threshold
inliers = [m for m, ok in zip(good, mask.ravel()) if ok]

vis = cv2.drawMatches(img1, kp1, img2, kp2, inliers, None)
```

On an 800 x 531 photograph and a copy rotated by 30 degrees and scaled to 0.7, this gave 2754 and 1745 keypoints, 1007 ratio-test matches and 954 RANSAC inliers.

## Ratio test from scratch (NumPy)

```python
def match_ratio(d1, d2, ratio=0.8):
    # Pairwise Euclidean distances via |a - b|^2 = |a|^2 - 2ab + |b|^2
    dist = np.sqrt(np.maximum((d1**2).sum(1)[:, None] - 2 * d1 @ d2.T + (d2**2).sum(1)[None, :], 0))
    order = np.argsort(dist, axis=1)[:, :2]               # nearest and second nearest in B
    rows = np.arange(len(d1))
    first, second = dist[rows, order[:, 0]], dist[rows, order[:, 1]]
    keep = first < ratio * second
    return np.column_stack([rows[keep], order[keep, 0]])  # (index in A, index in B)

def mutual_check(d1, d2):
    dist = np.sqrt(np.maximum((d1**2).sum(1)[:, None] - 2 * d1 @ d2.T + (d2**2).sum(1)[None, :], 0))
    a2b, b2a = dist.argmin(1), dist.argmin(0)
    return [(i, j) for i, j in enumerate(a2b) if b2a[j] == i]
```

`match_ratio` returned exactly the same 1007 pairs as OpenCV's brute-force matcher in the test above. The distance matrix is $N_1 \times N_2$, which is fine for a few thousand keypoints; for more, use an approximate index such as FLANN.

## DoG extrema from scratch (one octave)

```python
from scipy import ndimage as ndi

def dog_extrema(img, sigma0=1.6, s=3, thresh=0.03):
    # img: float in [0, 1]. Returns (level, y, x) of 3 x 3 x 3 extrema, plus the sigma list.
    k = 2 ** (1 / s)
    sig = [sigma0 * k**i for i in range(s + 3)]          # s + 3 blurred images per octave
    L = np.stack([ndi.gaussian_filter(img, sg) for sg in sig])
    D = L[1:] - L[:-1]                                   # s + 2 difference-of-Gaussian images
    is_ext = ((D == ndi.maximum_filter(D, size=3)) |
              (D == ndi.minimum_filter(D, size=3))) & (np.abs(D) > thresh)
    is_ext[0] = is_ext[-1] = False                       # need a level above and below
    return np.argwhere(is_ext), sig
```

This is only the first stage of SIFT: it has no input doubling, no further octaves, no sub-pixel refinement and no edge rejection. It shows how the DoG stack and the 26-neighbour test work.

---
*Related:* [[Code Snippets MOC]], [[Computer Vision MOC]], [[RANSAC Snippets]]
