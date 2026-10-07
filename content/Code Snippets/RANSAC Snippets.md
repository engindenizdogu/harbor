---
title: RANSAC Snippets
tags: [computer-vision, model-fitting, ransac, code-snippets, auto-captured]
draft: false
---
Synthetic data, a total-least-squares line fit and a minimal RANSAC loop. Theory: [[Least-Squares Line Fitting]], [[RANSAC]].

## Generate a noisy line and outliers

```python
def make_line(a, b, c, nr, sigma=0):
    """nr points on ax + by + c = 0 inside a 100-unit span, plus Gaussian noise of std sigma."""
    intercept = np.array([-c / a, 0]) if abs(b) < 1e-8 else np.array([0, -c / b])
    tang = np.array([-b, a]) / np.hypot(a, b)                 # from normal to tangent
    rng = np.random.default_rng()
    points = intercept + rng.uniform(0, 100, nr)[:, None] * tang
    if sigma > 0:
        points = points + rng.standard_normal((nr, 2)) * sigma
    return points

def make_outliers(minx, maxx, miny, maxy, nr):
    rng = np.random.default_rng()
    return np.column_stack([rng.uniform(minx, maxx, nr), rng.uniform(miny, maxy, nr)])

inliers = make_line(3.0, 1.0, 5.0, nr=100, sigma=1.5)
lo, hi = inliers.min(), inliers.max()                         # square box avoids degenerate cases
outliers = make_outliers(lo, hi, lo, hi, nr=100)
data = np.vstack([inliers, outliers])
```

## Least-squares fit and point-to-line error

```python
def fit_line(points):
    mean = points.mean(axis=0)
    _, _, vt = np.linalg.svd(points - mean)       # SVD of the centred points
    a, b = vt[1]                                  # unit normal = direction of least variance
    return np.array([a, b, -(a * mean[0] + b * mean[1])])

def line_errors(line, points):
    # signed perpendicular distance, valid because (a, b) has unit length
    return points @ line[:2] + line[2]
```

## RANSAC

```python
def pick_pair(data, rng):
    return data[rng.choice(len(data), size=2, replace=False)]   # minimal sample for a line

def ransac(data, num_trials, threshold=1.0):
    rng = np.random.default_rng()
    best_line, best_count = None, -1
    for _ in range(num_trials):
        line = fit_line(pick_pair(data, rng))
        count = np.sum(np.abs(line_errors(line, data)) < threshold)
        if count > best_count:
            best_line, best_count = line, count
    return best_line, best_count

line, count = ransac(data, num_trials=100, threshold=3.0)       # about 2 sigma
refit = fit_line(data[np.abs(line_errors(line, data)) < 3.0])   # least squares on the inliers
```

## How many trials?

```python
import math

def num_trials(inlier_ratio, sample_size=2, confidence=0.99):
    return math.ceil(math.log(1 - confidence) / math.log(1 - inlier_ratio ** sample_size))

num_trials(0.5)   # 17
num_trials(0.1)   # 459
```

Things to try: sweep `threshold` against `sigma` (a threshold of 0.33 sigma keeps only about 26% of the true inliers), raise the outlier count, or fit several lines by removing each line's inliers and repeating.

---
*Related:* [[Code Snippets MOC]], [[Computer Vision MOC]]
