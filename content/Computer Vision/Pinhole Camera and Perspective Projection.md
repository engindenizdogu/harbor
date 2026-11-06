---
title: Pinhole Camera and Perspective Projection
tags: [computer-vision, camera-geometry, projection, perspective, auto-captured]
draft: false
---
The **pinhole camera** is the simplest model of how a 3D scene becomes a 2D image, and it is the basis of nearly all geometric computer vision. Every other camera model (lenses, calibration matrices) is a refinement of it.

## Why a Pinhole?

Putting a bare piece of film in front of an object does not give an image: every film point receives light from **every point of the object**, so the result is a blur. A **barrier with a tiny hole** blocks most rays and keeps only the **pencil of rays through a single point**. Each film point then sees light from essentially one direction, and a sharp, inverted image forms on the **image plane**.

That single point has many names: **aperture, center of projection, optical center, focal point, camera center**. The principle is the ancient **camera obscura**, used by artists and even by turning a darkened room into a giant camera.

## Deriving the Projection

Use the **canonical coordinate system**:

- The camera center is the **origin**.
- The **$z$ axis** is the optical axis, perpendicular to the image plane. Depth is measured along it.
- The $x$ and $y$ axes are parallel to the image plane (horizontal and vertical in the image).
- The image plane is the plane $z = f$, where $f$ is the **focal length**.

A scene point $P = (x, y, z)$ projects to where the ray from $P$ through the origin crosses the image plane. Every point on that ray is a multiple $\lambda P$, and the image plane needs the third coordinate to be $f$, so $\lambda z = f$ and $\lambda = f/z$. Therefore

$$(x, y, z) \;\longmapsto\; \left( f\,\frac{x}{z},\; f\,\frac{y}{z} \right)$$

The same result follows from similar triangles in a side view:

```
 y
 |                         . P = (y, z)
 |            . P' = (y', f)
 C------------|------------------> z
 0            f            z        so   y'/f = y/z
```

Notes on the formula:

- **Division by $z$** is perspective: doubling the distance halves the image coordinates.
- **All points on the same visual ray** project to the same pixel, since the factors cancel in $x/z$. A single image therefore loses depth.
- The **camera center itself has no projection**, and points with $z = 0$ project to infinity.
- A real image plane sits behind the center and the image is flipped. We pretend the plane is **in front** at $z = +f$ so the image stays upright. The math is identical.
- The map is **not linear** in $(x, y, z)$. [[Homogeneous Coordinates]] turn it into a matrix product followed by one division: see [[Camera Projection Matrix]].

**Example:** with $f = 100$, the point $(2, 4, 20)$ lands at $(10, 20)$, and $(2, 4, 40)$ at $(5, 10)$.

## What Projection Preserves

| Preserved | Not preserved |
| --------- | ------------- |
| Straight lines stay straight | Lengths and ratios of lengths |
| | Angles |
| | **Parallelism** |

## Vanishing Points

**Parallel lines in the scene converge to a single point in the image**, the **vanishing point**. To construct it, draw the ray from the camera center parallel to the scene lines: where that ray meets the image plane is the vanishing point. Every line with the same direction shares it. Converging lines are a powerful depth cue in paintings and photographs.

The exception: parallel lines that are also **parallel to the image plane** never converge. They stay parallel in the image.

## Planes, Vanishing Lines and the Horizon

- **Fronto-parallel plane** (parallel to the image plane): every point is at the same depth $z$, so the pattern is simply **scaled by $f/z$**. Angles and ratios of lengths and areas are preserved.
- **Tilted plane:** the pattern is distorted by a **2D homography** ([[Homographies and Perspective Warping]]).
- **Vanishing line:** each family of parallel planes has one. Construct it by joining the vanishing points of two different line directions that lie in the plane.
- **Horizon:** the vanishing line of the **ground plane**. It passes through all points at the **height of the camera**. A scene point imaged above the horizon is higher than the camera, and one below it is lower, so the horizon reveals the relative heights of objects.

## Projection of 3D Shapes

A **sphere** projects to an **ellipse** in general (the cone of rays touching the sphere cuts the image plane in an ellipse), and to a circle only when it is centered on the optical axis. The stretching is visible near the edges of wide-angle photographs.

*Sources: [Pinhole camera model (Wikipedia)](https://en.wikipedia.org/wiki/Pinhole_camera_model); [Vanishing point (Wikipedia)](https://en.wikipedia.org/wiki/Vanishing_point); Szeliski, [Computer Vision: Algorithms and Applications](https://szeliski.org/Book/), chapter on image formation.*

---
*Related:* [[Computer Vision MOC]], [[Camera Projection Matrix]], [[Homogeneous Coordinates]], [[Homographies and Perspective Warping]], [[Cylindrical Warping]]
