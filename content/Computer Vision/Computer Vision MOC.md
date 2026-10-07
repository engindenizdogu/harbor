---
title: Computer Vision MOC
tags: [computer-vision, moc]
draft: false
---
Map of Contents. Classical image analysis built from first principles: pixels and filtering, gradients and corners, matching patches, changing resolution, and fitting models robustly. Learned visual models (CNNs and beyond) live in [[Machine Learning MOC]], and image generation lives in [[Generative AI MOC]].

## Fundamentals
- [[Image Representation and Indexing]] - Arrays, channels, data types, (x, y) vs. (row, column), slicing, and views vs. copies.
- [[Pixel-Level Operations]] - Grayscale, thresholding, colour masks, blending, and the uint8 overflow trap.
- [[Image Noise]] - Gaussian, salt-and-pepper, Poisson, and speckle noise, and which filter fits each.

## Filtering and Gradients
- [[Cross-Correlation and Convolution]] - Flipped vs. unflipped kernels, border modes, and the FFT.
- [[Image Borders and Padding]] - Zero, replicate, and reflect padding, and the false edges zero padding creates.
- [[Gaussian Filtering and Convolution]] - Gaussian kernels, box filters, normalization, and zero-mean kernels.
- [[Median Filter]] - A non-linear filter for salt-and-pepper noise, its limits, and how independent masks make the real corruption exceed the label.
- [[Image Gradients and the Sobel Operator]] - Gradient magnitude and direction, which kernel finds which edge, and smoothing first.

## Feature Detection
- [[Harris Corner Detector]] - Structure tensor, the response function, thresholds, and border artifacts.
- [[Non-Maximum Suppression]] - Keeping one detection per object, on score maps, corner maps, and bounding boxes.

## Local Features
- [[Scale Space and Difference of Gaussians]] - Scale space, blob detection, DoG as an approximate normalized Laplacian, and octaves.
- [[SIFT]] - Scale- and rotation-invariant keypoints: DoG extrema, localization, orientation, and the 128-D descriptor.
- [[Feature Matching]] - Nearest-neighbour descriptor matching, the ratio test, and RANSAC verification.

## Matching
- [[Template Matching]] - SAD, SSD, NCC and ZNCC, the intensity model, when to use which, a salt-and-pepper noise experiment, complexity, and limits.
- [[Multi-Scale Template Matching]] - Finding the same object at several sizes by shrinking the image, and detecting multiple instances.
- [[Integral Images]] - Constant-time rectangle sums for fast window statistics.

## Geometric Transformations
- [[Image Warping]] - Homogeneous coordinates, translation, rotation, scaling, shear, affine maps, and forward vs. inverse warping.
- [[Homographies and Perspective Warping]] - Perspective transforms, the DLT estimate from 4 point pairs, rectification, and when a homography is exact.
- [[Cylindrical Warping]] - Projecting onto a cylinder for panoramas, the mapping formulas, and choosing the focal length.

## Resolution and Scale
- [[Aliasing and Downsampling]] - Why a low-pass filter must come before subsampling.
- [[Image Interpolation]] - Linear, bilinear, and bicubic interpolation, and inverse mapping for resizing.
- [[Image Pyramids]] - Gaussian and Laplacian pyramids, REDUCE and EXPAND, and uses from search to blending.

## Model Fitting
- [[Least-Squares Line Fitting]] - OLS vs. total least squares, the SVD solution, and sensitivity to outliers.
- [[RANSAC]] - Robust fitting by random sampling: threshold, number of trials, and multiple models.

## Code and Projects
- [[Image Basics Snippets]] - Indexing, thresholding, colour masks, blending, and box filtering.
- [[Corner Detection Snippets]] - Sobel, Harris, 3 x 3 NMS, and corner overlays.
- [[Image Warping Snippets]] - Transform matrices, inverse warping, affine and homography estimation, and a cylindrical warp.
- [[SIFT and Matching Snippets]] - OpenCV SIFT, ratio-test matching, RANSAC verification, and from-scratch DoG and matching code.
- [[Template Matching Snippets]] - SAD and NCC matchers, Gaussian filtering, the multi-scale search, NMS, integral images, and noise generation.
- [[RANSAC Snippets]] - Synthetic lines, SVD line fit, and a RANSAC loop.
- [[Computer Vision Coursework CS558]] - Coursework results using these techniques.

## Related Domains
- [[Machine Learning MOC]] - Neural networks and learning methods.
- [[Generative AI MOC]] - Image generation, VAEs, and GANs.
- [[Code Snippets MOC]] - Reusable code across domains.

---
## To Research / Inbox
*(Drop new concepts or terms you want to research here as unlinked wiki-links)*

Next topics: the Canny edge detector, Hough transform, homography estimation, Fourier transform basics.
