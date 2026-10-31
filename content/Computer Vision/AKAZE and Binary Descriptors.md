---
title: AKAZE and Binary Descriptors
tags: [computer-vision, feature-detection, feature-description, akaze, descriptors, auto-captured]
draft: false
---
Real-valued descriptors such as [[SIFT]]'s 128 floating-point numbers are accurate but heavy to compute and compare. **Binary descriptors** describe a keypoint with a short string of **bits**, so comparing two of them is a cheap bit-count. **AKAZE** is a widely used detector and binary descriptor, available in OpenCV.

## AKAZE

AKAZE (Accelerated-KAZE; Alcantarilla, Nuevo and Bartoli, 2013) differs from SIFT in two main ways:

| | SIFT | AKAZE |
| --- | --- | --- |
| Scale space | **Gaussian** blur, which smooths noise and object boundaries equally ([[Scale Space and Difference of Gaussians]]) | **Nonlinear diffusion**, which smooths flat regions but preserves edges |
| Speed trick | Difference-of-Gaussian approximation | **Fast Explicit Diffusion (FED)** to build the nonlinear scale space quickly |
| Detector | Extrema of the difference of Gaussians | Extrema of the Hessian determinant across scales |
| Descriptor | 128 real numbers (gradient histograms) | **Binary** M-LDB (Modified Local Difference Binary) string |
| Descriptor size | 512 bytes as 32-bit floats | 61 bytes (the full-length 486-bit descriptor, padded to whole bytes) |

Because the scale space follows edges, keypoints and descriptors respect object boundaries better than a Gaussian blur, which smears them. The detector returns each keypoint's location, angle and the scale (octave) at which it was found.

## How a Binary Descriptor Works

A binary descriptor is built from many **simple comparisons** around the keypoint, for example "is the average intensity of region A larger than region B?" Each comparison gives one bit, and M-LDB also compares gradients, using the scale-space information for robustness. Concatenating the bits gives the descriptor.

The ideas behind the family (BRIEF, ORB, BRISK, FREAK, LDB) are the same: **fast to compute, tiny to store, and fast to compare**. They trade some distinctiveness against SIFT for large speed gains.

## Matching With Hamming Distance

Two binary descriptors are compared with the **Hamming distance**, the number of bit positions where they differ. In hardware this is an XOR followed by a population count.

If the packed bytes are expanded into one 0 or 1 per bit, the **squared Euclidean distance equals the Hamming distance**, because $(a_i - b_i)^2$ is 1 exactly when the bits differ:

$$\lVert \mathbf a - \mathbf b \rVert_2^2 = \sum_i (a_i - b_i)^2 = d_{Hamming}(\mathbf a, \mathbf b), \qquad a_i, b_i \in \{0, 1\}$$

```python
bits = np.unpackbits(desc, axis=1).astype(np.float32)    # N x 488: one column per bit
# squared L2 between rows of `bits` == Hamming distance between the packed descriptors
```

I confirmed on real descriptors that the two quantities agree exactly (for example 182 and 153 differing bits for two sample pairs). This lets a standard distance-matrix routine ([[Feature Matching]]) handle binary descriptors unchanged.

## The Ratio Test Needs Different Thresholds

The ratio test ([[Feature Matching]]) compares the nearest and second-nearest distance. For SIFT the ratio is taken on **Euclidean** distances, with 0.8 as Lowe's value. A routine that works on squared distances, such as the Hamming computation above, computes the ratio of **squared** distances, which is the square of the Euclidean ratio:

| Ratio on Hamming (squared L2) | Equivalent Euclidean ratio |
| ----------------------------- | -------------------------- |
| 0.6 | 0.77 |
| 0.7 | 0.84 |
| 0.8 | 0.89 |
| 0.9 | 0.95 |

So a value of 0.9 on Hamming distances is much stricter than it sounds. Binary descriptors also have **smaller distance gaps**, with few bits separating a good match from the second best, so the useful range is higher and must be tuned per image pair. An experiment on two sample pairs shows the trade-off: fewer, cleaner matches at low ratios, more but dirtier matches at high ones, with the count of RANSAC inliers peaking at about 0.9 and not improving beyond ([[Feature Matching]]).

*Sources: [AKAZE reference implementation](https://github.com/pablofdezalc/akaze) (nonlinear scale space, FED, M-LDB, 486-bit full-length descriptor) and [OpenCV's AKAZE documentation](https://docs.opencv.org/3.4/d8/d30/classcv_1_1AKAZE.html); Alcantarilla, Nuevo and Bartoli, Fast Explicit Diffusion for Accelerated Features in Nonlinear Scale Spaces, BMVC 2013. The Hessian-determinant detector, SIFT descriptor size and the BRIEF/ORB family remarks are from my own knowledge. The squared-L2 equals Hamming check and the ratio table were computed in my own runs.*

---
*Related:* [[Computer Vision MOC]], [[SIFT]], [[Feature Matching]], [[Image Stitching]]
