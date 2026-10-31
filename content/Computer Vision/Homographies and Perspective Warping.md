---
title: Homographies and Perspective Warping
tags: [computer-vision, geometry, homography, transformations, auto-captured]
draft: false
---
A **homography** (projective transformation) is the most general 2D mapping that keeps straight lines straight. It describes how a **flat surface** looks when photographed from different viewpoints, and also how two images of any scene relate when the camera only **rotates** about its centre. It extends the affine family from [[Image Warping]] by adding perspective foreshortening: parallel lines can converge, and far things look smaller.

## Definition

A homography is a $3 \times 3$ matrix $H$ acting on homogeneous coordinates ([[Homogeneous Coordinates]]):

$$\begin{pmatrix} x' \\ y' \\ w' \end{pmatrix} = \begin{pmatrix} h_{11} & h_{12} & h_{13} \\ h_{21} & h_{22} & h_{23} \\ h_{31} & h_{32} & h_{33} \end{pmatrix} \begin{pmatrix} x \\ y \\ 1 \end{pmatrix}$$

so the output position is $(u, v) = (x'/w',\ y'/w')$:

$$u = \frac{h_{11} x + h_{12} y + h_{13}}{h_{31} x + h_{32} y + h_{33}}, \qquad v = \frac{h_{21} x + h_{22} y + h_{23}}{h_{31} x + h_{32} y + h_{33}}$$

- The **division by $w'$** is what makes it perspective. It is not a linear map of $(x, y)$.
- $H$ is only defined **up to scale** (multiplying all entries by a constant gives the same mapping), so it has **8 degrees of freedom**, and one entry, usually $h_{33}$, is fixed to 1.
- If $h_{31} = h_{32} = 0$, the denominator is constant and $H$ reduces to an **affine** map.
- **Preserves:** straight lines, and incidence (points on a line stay on a line). **Does not preserve:** parallelism, lengths, angles or length ratios.

## Estimating a Homography

Each correspondence $(x, y) \leftrightarrow (u, v)$ gives **two** linear equations in the entries of $H$. With 8 unknowns, **4 point pairs** (no three collinear) determine $H$ exactly. This is the **Direct Linear Transform (DLT)**.

Rearranging $u = \frac{h_{11}x + h_{12}y + h_{13}}{h_{31}x + h_{32}y + h_{33}}$ and the matching equation for $v$ gives, for each pair, two rows of a matrix $A$:

$$\begin{pmatrix} x & y & 1 & 0 & 0 & 0 & -ux & -uy & -u \\ 0 & 0 & 0 & x & y & 1 & -vx & -vy & -v \end{pmatrix} \mathbf h = \mathbf 0$$

where $\mathbf h$ is the 9 entries of $H$ stacked. Stack all pairs into one matrix $A$ and solve $A\mathbf h = \mathbf 0$ with $\lVert \mathbf h \rVert = 1$: $\mathbf h$ is the **right singular vector with the smallest singular value** of $A$ (the SVD), equivalently the eigenvector of $A^\top A$ with the smallest eigenvalue, the same device as in [[Least-Squares Line Fitting]]. Then reshape and divide by $h_{33}$.

- **More than 4 pairs** are solved in the least-squares sense.
- **Normalize the coordinates** (centre them, scale to about unit size) before building $A$ for numerical stability.
- **Outliers:** real correspondences from feature matching contain wrong pairs, so the 4-point solve is wrapped in [[RANSAC]]. This is how panoramas are stitched.

## Fitting in Practice

- **Know the direction.** $H$ maps the first point set to the second. If you need the reverse, use $H^{-1}$ (`np.linalg.inv`; the transpose is the inverse only for rotation matrices).
- **Build $A$ carefully.** Each correspondence gives two rows. With $\mathbf p = (x, y, 1)^\top$ they can be written $\big(\mathbf 0^\top,\ -\mathbf p^\top,\ y'\,\mathbf p^\top\big)$ and $\big(\mathbf p^\top,\ \mathbf 0^\top,\ -x'\,\mathbf p^\top\big)$, which is the same system as above with the rows arranged differently.
- **Normalize by $h_{33}$ only after checking it is not zero.** A zero there means something went wrong, or the mapping sends the origin to infinity.
- **Do not fit from a minimal set of neighbouring points.** Points that are very close together, combined with rounded coordinates, make the solution unstable. Spread the 4 points far apart, or use many points.
- **Check one point by hand.** Map a single source point and compare it with its target before trusting the matrix.
- **Measure the error as the mean distance** between each mapped point and its target:

$$\text{error} = \frac{1}{N} \sum_i \big\lVert H\mathbf p_i - \mathbf p'_i \big\rVert_2$$

### Example: nine synthetic point sets

Correspondences between a letter shape and transformed copies of it, with integer pixel coordinates (except the last set, which has real-valued coordinates):

| Case | What the fitted $H$ shows | Mean error (px) |
| ---- | ------------------------- | --------------- |
| 1, 2, 3 | Scaling (non-uniform in 1 and 2, uniform in 3) | 0.25, 0.24, 0.47 |
| 4 | Swap of $x$ and $y$: $H = \begin{pmatrix} 0 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix}$ | 0.00 |
| 5 | Rotation by 180 degrees with a shift: $H = \begin{pmatrix} -1 & 0 & 76 \\ 0 & -1 & 101 \\ 0 & 0 & 1 \end{pmatrix}$ | 0.00 |
| 6, 7, 8 | General affine maps mixing scale, rotation or reflection, and shift | 0.46, 0.39, 0.39 |
| 9 | Strong perspective ($h_{32} \approx -0.8$), real-valued coordinates | 0.006 |

![[homography-fit-example.png]]

*Fits for cases 3 and 9. When the fit is right, the mapped points (green) lie on the target points (orange).*

Why the errors are not zero: coordinates rounded to integers carry up to half a pixel of error in each coordinate, and the expected distance from such rounding alone is about **0.38 px**. The fits with errors of 0.24 to 0.47 px are therefore as good as the data allow. Exact integer mappings (a swap, a 180-degree rotation) fit with zero error, and real-valued data fit to 0.006 px.

## Using a Homography: Rectification

![[homography-rectification.png]]

*Left: a flat square. Middle: the same square seen from an oblique view, with its four corners marked. Right: the view undone with a homography estimated from just those 4 point pairs. The result is blurrier because the pixels were resampled twice, and the original detail is gone.*

Typical uses:

| Use | How |
| --- | --- |
| **Document or whiteboard rectification** | Mark the 4 corners of the page and map them to a rectangle |
| **Panoramas** | Warp every photo into the frame of a reference image with a homography estimated from feature matches |
| **Augmented reality** | Map a flat marker or poster onto its detected quadrilateral |
| **Plane-based tracking and calibration** | Track a planar target between frames |

Warping an image with $H$ follows the same inverse-mapping recipe as any other warp: apply $H^{-1}$ to each output pixel and interpolate ([[Image Warping]], [[Image Interpolation]]).

## When a Homography Is Exact

A homography relates two views of an image exactly in two cases:

1. The scene is a **plane** (a wall, a floor, a page, a distant ground).
2. The camera **only rotates** around its optical centre, with no translation. Then any scene, however deep, gives images related by a homography, which is why hand-held panoramas work when you stand still and turn.

If the camera also moves through a 3D scene with depth, a single homography fits only parts of it. A **fundamental matrix** is the general relation then.

Code: [[Image Warping Snippets]].

*Sources: [Foundations of Computer Vision, ch. 41: Homographies](https://visionbook.mit.edu/homography.html), which covers 8 degrees of freedom, the DLT, planar scenes, pure rotation, panoramas and RANSAC; [Homography (computer vision), Wikipedia](https://en.wikipedia.org/wiki/Homography_(computer_vision)); Hartley and Zisserman, Multiple View Geometry in Computer Vision, DLT algorithm. The recovered matrix in the figure matched the true one to about $10^{-10}$ in my test.*

---
*Related:* [[Computer Vision MOC]], [[Image Warping]], [[Cylindrical Warping]], [[RANSAC]], [[Image Stitching]], [[Image Warping Snippets]]
