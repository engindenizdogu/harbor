---
title: Feature Matching
tags: [computer-vision, feature-matching, descriptors, auto-captured]
draft: false
---
**Feature matching** pairs keypoints in one image with the keypoints in another that show the same physical point. Each keypoint carries a **descriptor**, a vector summarizing its neighbourhood ([[SIFT]] produces 128 numbers), and matching is a nearest-neighbour search in descriptor space.

```mermaid
flowchart LR
    A[Image A and B] --> B["Detect keypoints and compute descriptors"]
    B --> C["For each descriptor in A, find nearest in B"]
    C --> D["Filter: ratio test, mutual check"]
    D --> E["Geometric verification (RANSAC)"]
    E --> F[Clean set of correspondences]
```

## Distance Between Descriptors

| Descriptor | Typical distance |
| ---------- | ---------------- |
| Real-valued vectors (SIFT) | Euclidean ($L_2$) distance |
| Binary descriptors (such as ORB) | Hamming distance (number of differing bits) |

## Choosing Which Matches to Trust

Taking every keypoint's nearest neighbour gives many **wrong** matches, because a keypoint with no true counterpart (hidden, outside the view, or filtered out) still has *some* nearest neighbour.

| Strategy | Rule | Weakness |
| -------- | ---- | -------- |
| **Nearest neighbour only** | Accept the closest descriptor | Accepts all unmatched points too |
| **Distance threshold** | Accept if the distance is below $t$ | Some descriptors are distinctive and others generic, so no single $t$ fits |
| **Ratio test** | Accept if $d_1 / d_2 < 0.8$ ($d_1$ nearest, $d_2$ second nearest) | Rejects some correct matches |
| **Mutual (cross) check** | Keep $a \leftrightarrow b$ only if each is the other's nearest | Fewer matches |

### The ratio test

A correct match should be **much closer** than any other candidate. A wrong match has no good counterpart, so its nearest and second-nearest are about equally far and the ratio is near 1. Lowe measured, for SIFT, that rejecting matches with a ratio above 0.8 **removes 90% of the false matches while losing fewer than 5% of the correct ones**.

An experiment on a photograph and a copy of it rotated 30 degrees and scaled to 0.7, where the true mapping is known, shows the effect. A match counts as correct when its position agrees with the known transform to within 3 pixels:

| Method | Matches | Correct |
| ------ | ------- | ------- |
| Nearest neighbour only | 2754 | 994 (36%) |
| **Ratio test, 0.8** | 1007 | **954 (95%)** |
| After RANSAC (homography, 3 px) | 954 | 954 (inliers) |

The ratio test turns a mostly wrong match set into a mostly right one, and RANSAC removes the last mistakes.

### Choosing the threshold: an experiment

The same pair of photographs matched with AKAZE descriptors at several ratio thresholds, then verified with RANSAC (3 px threshold, 3000 trials). Two sample pairs:

| Ratio (on Hamming distance) | Pair A: matches | Pair A: RANSAC inliers | Pair B: matches | Pair B: RANSAC inliers |
| --------------------------- | --------------- | ---------------------- | --------------- | ---------------------- |
| 0.6 | 114 | 99 (87%) | 1901 | 1461 (77%) |
| 0.7 | 202 | 151 (75%) | 2483 | 1837 (74%) |
| 0.8 | 368 | 205 (56%) | 3229 | 2232 (69%) |
| 0.9 | 1023 | 279 (27%) | 5198 | 2459 (47%) |
| 0.95 | 1850 | 189 (10%) | 8335 | 2453 (29%) |

- **Lower ratio:** fewer matches but a much higher fraction are correct.
- **Higher ratio:** more matches, so more *correct* ones at first, but the inlier fraction collapses.
- The count of inliers **stops growing** (and for pair A even falls) once the threshold is loose, because extra matches are almost all wrong.
- The drop for pair A at 0.95 also reflects too few RANSAC trials: with about 10% inliers and 4 points per trial, 99% confidence needs roughly 40,000 trials, not 3000 ([[RANSAC]]).

For a geometric fit, fewer but cleaner matches are usually better than many dirty ones, as long as enough remain to fit the model.

## Binary Descriptors

Binary descriptors are compared by Hamming distance, which equals the squared Euclidean distance on the bits. The ratio test is then taken on squared distances, so its thresholds are not comparable with SIFT's 0.8: see [[AKAZE and Binary Descriptors]].

## Geometric Verification

Even good matches contain mistakes, so a final check asks that the matches **agree on a geometric model**: a homography for a plane or a rotating camera ([[Homographies and Perspective Warping]]), or a fundamental matrix for a general scene. [[RANSAC]] fits the model to random minimal samples of matches and keeps the largest consensus. Lowe's own system clustered matches by pose with a Hough transform and then verified the result by least squares.

## Fast Search

Exact nearest-neighbour search in 128 dimensions is no faster than checking every candidate, since tree indexes lose their advantage above roughly 10 dimensions. Approximate methods return the true neighbour with high probability, such as Lowe's **Best-Bin-First** variant of k-d trees. Libraries provide this as FLANN-style search, and for a few thousand keypoints a brute-force distance matrix is fine ([[SIFT and Matching Snippets]]).

## Related Matching Ideas

This is the keypoint counterpart of [[Template Matching]]: instead of sliding a patch over every position, compare compact descriptors of a few distinctive points, which is faster and tolerates scale and rotation.

*Sources: Lowe, [Distinctive Image Features from Scale-Invariant Keypoints, IJCV 2004](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf), for the 0.8 ratio, the 90% and 5% figures, Best-Bin-First and the Hough clustering; the Hamming remark and mutual check are from my own knowledge. The results table comes from my own run of OpenCV's SIFT on an example photograph.*

---
*Related:* [[Computer Vision MOC]], [[SIFT]], [[AKAZE and Binary Descriptors]], [[Image Stitching]], [[RANSAC]], [[Homographies and Perspective Warping]], [[SIFT and Matching Snippets]]
