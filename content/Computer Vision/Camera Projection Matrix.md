---
title: Camera Projection Matrix
tags: [computer-vision, camera-geometry, calibration, linear-algebra, auto-captured]
draft: false
---
The **camera projection matrix** $P$ packs the whole imaging process into one $3 \times 4$ matrix that maps a 3D world point to a pixel. It builds directly on the [[Pinhole Camera and Perspective Projection]] and uses [[Homogeneous Coordinates]] so that the perspective division becomes a single matrix product.

## The Chain From World to Pixel

```mermaid
flowchart LR
    W["World point X (4x1)"] -->|"[R | t]  extrinsics"| C["Camera coordinates"]
    C -->|"canonical projection [I | 0]"| N["Normalized image point"]
    N -->|"K  intrinsics"| P["Pixel (u, v)"]
```

- **Extrinsic parameters** place the camera in the world: a **rotation** $R$ and a **translation** $t$ (6 numbers).
- **Intrinsic parameters** describe the camera itself: **focal length(s)**, **principal point**, pixel scaling (and optionally skew).

## Normalized Camera Coordinates

In the **normalized camera coordinate system** the camera center is the origin, the principal axis is the $z$ axis, and $f = 1$. Projection is then

$$\begin{pmatrix} u \\ v \\ 1 \end{pmatrix} \simeq \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \end{pmatrix} \begin{pmatrix} X \\ Y \\ Z \\ 1 \end{pmatrix} = \begin{pmatrix} X \\ Y \\ Z \end{pmatrix}, \qquad u = \frac{X}{Z},\; v = \frac{Y}{Z}$$

where $\simeq$ means "equal up to scale": divide by the third coordinate to read off $(u, v)$. These coordinates depend only on the **direction** of the ray, so any two cameras at the same pose see the same normalized point.

## Intrinsics: the Calibration Matrix $K$

Two things turn normalized coordinates into pixels:

- The **focal length** scales by $f$ (or $f_x, f_y$ for non-square pixels).
- The **principal point** $(p_x, p_y)$, where the optical axis meets the image plane, is the origin in camera coordinates, but pixel coordinates put the origin in the image corner, so we shift by $(p_x, p_y)$.

$$K = \begin{pmatrix} f & 0 & p_x \\ 0 & f & p_y \\ 0 & 0 & 1 \end{pmatrix}, \qquad u_{pix} = f\,\frac{X}{Z} + p_x, \quad v_{pix} = f\,\frac{Y}{Z} + p_y$$

## Extrinsics: Rotation and Translation

If $\tilde C$ is the camera center in world coordinates and $\tilde X$ a world point, the point in the camera frame is

$$\tilde X_{cam} = R\,(\tilde X - \tilde C) = R\tilde X + t, \qquad t = -R\tilde C$$

First translate so the camera sits at the origin, then rotate. In homogeneous form this is the $4 \times 4$ matrix $\begin{pmatrix} R & t \\ 0 & 1 \end{pmatrix}$.

## The Full Matrix

$$x \simeq K\,[\,R \mid t\,]\,X, \qquad P = K\,[\,R \mid -R\tilde C\,] \quad (3 \times 4)$$

- $P$ is defined **up to scale**, which leaves **11 degrees of freedom**: 5 intrinsic ($f_x, f_y$, skew, $p_x, p_y$) and 6 extrinsic.
- To project: compute $PX$, then **divide by the third coordinate**.

### The camera center is the null space of $P$

In homogeneous world coordinates the camera center is $C = (\tilde C, 1)^\top$, and

$$P\,C = K\,(R\tilde C - R\tilde C) = 0.$$

Its projection is $(0,0,0)$, which is undefined: the camera center is the one point that has no image.

## Worked Example

Intrinsics: $f = 100$, principal point $(50, 50)$. The camera is unrotated ($R = I$) and sits at $\tilde C = (1, 0, 0)$. The world point is $\tilde X = (3, 2, 10)$.

1. **World to camera:** $R(\tilde X - \tilde C) = (2,\, 2,\, 10)$.
2. **Normalize:** $(u, v) = (2/10,\, 2/10) = (0.2,\, 0.2)$. No focal length yet.
3. **Apply $K$:** $u_{pix} = 100 \cdot 0.2 + 50 = 70$, $v_{pix} = 100 \cdot 0.2 + 50 = 70$.

The pixel is $(70, 70)$.

## Going Backward: Pixel to Ray

Applying $K^{-1}$ to a pixel gives a normalized point $(u, v, 1)$, which is the **direction of the viewing ray** in camera coordinates. For pixel $(60, 70)$ with the same $K$: $(0.1,\, 0.2,\, 1)$. Every point $Z\cdot(0.1,\, 0.2,\, 1)$ along that ray projects to the same pixel, so **depth cannot be recovered from one image**. It needs a known depth or a second view where two rays intersect.

## Calibration

**Camera calibration** estimates the transformation from world to image coordinates, that is $P$, or $K$, $R$ and $t$. The standard approach photographs an object with known 3D points and measures their pixel positions. Each correspondence gives two linear equations in the entries of $P$, so with 11 degrees of freedom **at least 6 correspondences** are needed. Solving them by homogeneous least squares is the same method as the [[Homographies and Perspective Warping]] estimate.

*Sources: [Camera resectioning (Wikipedia)](https://en.wikipedia.org/wiki/Camera_resectioning); Hartley and Zisserman, Multiple View Geometry in Computer Vision. The 6-correspondence count follows from the degrees of freedom above (standard result, my own derivation).*

---
*Related:* [[Computer Vision MOC]], [[Pinhole Camera and Perspective Projection]], [[Homogeneous Coordinates]], [[Image Warping]], [[Least-Squares Line Fitting]]
