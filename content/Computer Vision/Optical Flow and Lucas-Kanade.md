---
title: Optical Flow and Lucas-Kanade
tags: [computer-vision, motion, optical-flow, tracking, auto-captured]
draft: false
---
**Optical flow** is the **apparent motion of brightness patterns** between two video frames. It is stored as a vector $(u, v)$ at each pixel, saying how far that pixel's pattern moved horizontally and vertically. Motion is a powerful visual cue, and sometimes the only one: a handful of moving dots is enough for a person to see a walking body.

Flow can come from **camera motion**, **object motion**, or **changes of lighting**. It is not always the same as true motion: a uniform sphere spinning in place has real motion but produces no flow, and a moving light over a still scene produces flow with nothing moving.

## The Three Assumptions

| Assumption | Meaning |
| ---------- | ------- |
| **Brightness constancy** | The projection of the same scene point looks the same in every frame |
| **Small motion** | Points do not move far between frames (about a pixel or less) |
| **Spatial coherence** | A pixel moves like its neighbours |

## The Brightness Constancy Equation

A point at $(x, y)$ in frame $t$ moves by $(u, v)$ and appears at $(x+u,\, y+v)$ in frame $t+1$ with the same brightness:

$$I(x + u,\; y + v,\; t + 1) = I(x, y, t)$$

For small motion, a first-order Taylor expansion of the left side gives

$$I(x,y,t) + I_x\,u + I_y\,v + I_t \approx I(x,y,t) \quad\Longrightarrow\quad I_x\,u + I_y\,v + I_t = 0$$

- $I_x, I_y$ are the spatial gradients ([[Image Gradients and the Sobel Operator]]).
- $I_t = I(x,y,t+1) - I(x,y,t)$ is the **temporal derivative**: the difference between the two frames.
- The unknowns are $u$ and $v$. In vector form, $\nabla I \cdot (u, v)^\top = -I_t$.

## The Aperture Problem

At one pixel this is **one equation with two unknowns**, so the motion cannot be recovered uniquely. If $(u, v)$ satisfies it, so does $(u + u',\, v + v')$ for any $(u', v')$ perpendicular to the gradient.

- The component of motion **along the gradient** (across the edge) is recoverable.
- The component **perpendicular to the gradient** (along the edge) is invisible.

Looking through a small window (an aperture) at a straight edge, you can only see motion perpendicular to it. The **barber pole illusion** is the classic demonstration: the stripes actually rotate around the pole, but you perceive them climbing upward because the motion across the stripes is the only part you can see.

**Example:** at a pixel with $I_x = 2$, $I_y = 0$, $I_t = -4$ (a vertical edge), the equation is $2u - 4 = 0$, so $u = 2$. Nothing at all is known about $v$.

## Lucas-Kanade: More Equations From a Window

Spatial coherence supplies extra equations. Assume all pixels in a window share the same $(u, v)$. A $5 \times 5$ window gives 25 equations in the same 2 unknowns:

$$\underbrace{\begin{pmatrix} I_x(p_1) & I_y(p_1) \\ \vdots & \vdots \\ I_x(p_{25}) & I_y(p_{25}) \end{pmatrix}}_{A\ (25 \times 2)} \underbrace{\begin{pmatrix} u \\ v \end{pmatrix}}_{d} = \underbrace{-\begin{pmatrix} I_t(p_1) \\ \vdots \\ I_t(p_{25}) \end{pmatrix}}_{b}$$

The system is overdetermined, so solve it by **least squares** ([[Least-Squares Line Fitting]]): $A^\top A\, d = A^\top b$, so $d = (A^\top A)^{-1} A^\top b$, with

$$A^\top A = \begin{pmatrix} \sum I_x I_x & \sum I_x I_y \\ \sum I_x I_y & \sum I_y I_y \end{pmatrix}, \qquad A^\top b = -\begin{pmatrix} \sum I_x I_t \\ \sum I_y I_t \end{pmatrix}$$

```mermaid
flowchart LR
    A["Two frames"] --> B["Ix, Iy, It"]
    B --> C["Window sums: A^T A and A^T b"]
    C --> D["Solve 2x2 system for (u, v)"]
    D --> E["Flow vector per pixel"]
```

### Why it works at corners and fails at flat regions

$A^\top A$ is the same matrix as the **structure tensor** of the [[Harris Corner Detector]]. Its eigenvalues decide whether the flow is well determined:

| Region | Eigenvalues of $A^\top A$ | Flow estimate |
| ------ | ------------------------- | ------------- |
| Flat | both small | None: the system is nearly singular |
| Edge | one large, one small | Only the component across the edge (the aperture problem again) |
| Corner | both large and similar | Reliable full $(u, v)$ |

Flow is well estimated exactly where "cornerness" is high, which is why corners are the standard **good features to track**.

## When Lucas-Kanade Fails

| Failure | Fix |
| ------- | --- |
| **Large motion** (more than about a pixel) breaks the Taylor expansion | **Coarse-to-fine** estimation on an image pyramid, with iterative refinement ([[Image Pyramids]]) |
| **A point does not move like its neighbours** (motion boundaries) | **Motion segmentation**: separate layers of coherent motion |
| **Brightness constancy fails** (lighting change, specular highlights) | **Feature matching** such as [[SIFT]], or tracking |

Smoothness is needed in both **space** (neighbours move alike) and **time** (small motion between frames).

## Uses

Video stabilization, object and action tracking, traffic and surveillance analysis, motion capture, autonomous driving, and the front end of visual SLAM and augmented reality.

*Sources: Lucas and Kanade, An Iterative Image Registration Technique with an Application to Stereo Vision, 1981; [Lucas-Kanade method (Wikipedia)](https://en.wikipedia.org/wiki/Lucas%E2%80%93Kanade_method); [Barber pole illusion (Wikipedia)](https://en.wikipedia.org/wiki/Barberpole_illusion).*

---
*Related:* [[Computer Vision MOC]], [[Harris Corner Detector]], [[Image Pyramids]], [[Least-Squares Line Fitting]], [[Feature Matching]]
