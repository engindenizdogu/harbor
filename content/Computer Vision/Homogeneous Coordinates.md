---
title: Homogeneous Coordinates
tags: [computer-vision, geometry, homogeneous-coordinates, linear-algebra, auto-captured]
draft: false
---
**Homogeneous coordinates** describe an $n$-dimensional point with $n + 1$ numbers. A 2D point $(x, y)$ becomes the 3-vector $(x, y, 1)^\top$, and a 3D point $(X, Y, Z)$ becomes the 4-vector $(X, Y, Z, 1)^\top$. The extra number is not a physical dimension. It is a bookkeeping device that lets translation and perspective projection be written as **matrix multiplications**, and it appears throughout geometry in computer vision.

## Definition

A homogeneous vector $(x, y, w)^\top$ with $w \ne 0$ represents the ordinary point

$$\left(\frac{x}{w},\ \frac{y}{w}\right)$$

Any non-zero scalar multiple of a homogeneous vector is the **same point**:

$$(x, y, 1)^\top \equiv (\lambda x, \lambda y, \lambda)^\top \quad \text{for any } \lambda \ne 0$$

So $(2, 1, 1)$, $(4, 2, 2)$ and $(1, 0.5, 0.5)$ all stand for the 2D point $(2, 1)$. Only the **ratios** of the entries matter.

| Direction | Rule |
| --------- | ---- |
| Ordinary to homogeneous | Append a 1: $(x, y) \to (x, y, 1)$ |
| Homogeneous to ordinary | **Divide by the last entry**, then drop it: $(x, y, w) \to (x/w,\ y/w)$ |

![[homogeneous-coordinates-rays.png]]

*In 2D, each homogeneous vector is a direction from the origin in 3D. Every point along one ray (the crosses and dots) is the same 2D point, and the plane $w = 1$ picks out its position.*

## Why Use Them

### 1. Translation becomes a matrix

A plain $2 \times 2$ matrix can rotate, scale or shear a 2D point but cannot translate it, because every output is a weighted sum of $x$ and $y$ with no constant term. With the extra 1 the constant has somewhere to act:

$$\begin{pmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} x \\ y \\ 1 \end{pmatrix} = \begin{pmatrix} x + t_x \\ y + t_y \\ 1 \end{pmatrix}$$

Rotation, scaling, shear and translation are then all matrices, and a chain of transformations is **one matrix product** ([[Image Warping]]). In 3D the same idea gives a $4 \times 4$ rigid motion
$\begin{pmatrix} R & \mathbf t \\ \mathbf 0^\top & 1 \end{pmatrix}$.

### 2. Perspective becomes linear

Perspective projection divides by depth, which is not a linear operation. In homogeneous coordinates the division is **deferred**: the matrix multiplication stays linear, and you divide by the last entry at the end. That is how a homography ([[Homographies and Perspective Warping]]) or a camera projection maps points while keeping the algebra to a single matrix product.

### 3. Points at infinity

A vector whose last entry is zero, $(x, y, 0)^\top$, cannot be divided by $w$. It represents a **point at infinity**: a pure **direction**. This lets parallel lines "meet" at a finite homogeneous point (a vanishing point), and it keeps formulas valid in cases that would otherwise need special handling.

## Lines and Intersections

In 2D, a line $ax + by + c = 0$ is the 3-vector $\mathbf l = (a, b, c)^\top$. A point $\mathbf p$ lies on it exactly when

$$\mathbf l^\top \mathbf p = 0$$

Points and lines are **dual**, so two simple formulas use the **cross product**:

| Task | Formula |
| ---- | ------- |
| Line through two points | $\mathbf l = \mathbf p_1 \times \mathbf p_2$ |
| Intersection of two lines | $\mathbf p = \mathbf l_1 \times \mathbf l_2$ |

Worked examples (checked numerically):

- The line through $(1, 1)$ and $(3, 2)$: $(1, 1, 1) \times (3, 2, 1) = (-1, 2, -1)$, which is the line $-x + 2y - 1 = 0$. Both points satisfy it.
- The lines $y = x$, written $(1, -1, 0)$, and $x + y = 4$, written $(1, 1, -4)$: their cross product is $(4, 4, 2)$, which is the point $(2, 2)$ after dividing by the last entry.
- The **parallel** lines $x + y = 1$ and $x + y = 3$, written $(1, 1, -1)$ and $(1, 1, -3)$: their cross product is $(-2, 2, 0)$. The last entry is zero, so the intersection is a point at infinity in the direction $(-1, 1)$, which is the direction of the lines.

## Common Uses

| Where | What the extra coordinate does |
| ----- | ------------------------------ |
| 2D transformations | Affine maps and homographies as $3 \times 3$ matrices ([[Image Warping]]) |
| Camera model | A 3D point $(X, Y, Z, 1)$ maps to an image point through a $3 \times 4$ projection matrix |
| Line fitting and geometry | Lines as 3-vectors, intersections as cross products |
| Estimation | Equations of the form $A\mathbf h = \mathbf 0$ solved with SVD, because the unknown matrix is only defined up to scale ([[Homographies and Perspective Warping]]) |

## Practical Tips

- **Normalize before comparing.** Two homogeneous vectors are equal as points when they are proportional, so divide by the last entry before computing distances or plotting.
- **Check for $w \approx 0$.** A tiny last entry means the point is very far away or at infinity, and the division becomes unstable.
- **Matrices are defined up to scale too.** A homography has 9 entries but 8 degrees of freedom, since multiplying every entry by the same constant gives the same mapping.
- **Stay consistent with $(x, y)$ order.** Homogeneous formulas take $x$ before $y$, while an image array is indexed `[y, x]` ([[Image Representation and Indexing]]).

*Source: [Foundations of Computer Vision, ch. 38: Representing Images and Geometry](https://visionbook.mit.edu/homogeneous_coordinates.html) (definition, scale equivalence, division by the last entry, and the transformation hierarchy). The line and point-at-infinity relations are standard projective geometry from my own knowledge, and the numerical examples were checked in code.*

---
*Related:* [[Computer Vision MOC]], [[Image Warping]], [[Homographies and Perspective Warping]], [[Image Warping Snippets]]
