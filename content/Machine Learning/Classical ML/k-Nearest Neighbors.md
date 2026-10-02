---
title: k-Nearest Neighbors
tags: [machine-learning, algorithms]
draft: false
---
| Type           |
| -------------- |
| Classification |

**The Elbow Curve for parameter selection:**
![[Pasted image 20260425184429.png|497]]

**Properties of a distance function:**
1. $d(x,y) > 0$ (when $x \neq y$)
2. $d(x,y) = d(y,x)$
3. $d(x,z) \leq d(x,y) + d(y,z)$ (triangle inequality)

**Distance Function Examples:**
- Euclidian Distance
- Minkowski Distance
- Manhattan Distance
