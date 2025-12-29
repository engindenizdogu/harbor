---
title: k-Nearest Neighbors
---
# k-Nearest Neighbors

| Type           |
| -------------- |
| Classification |

**The Elbow Curve for parameter selection:**
![](/assets/img/elbow_curve.png)

**Properties of a distance function:**
1. $d(x,y) > 0$ (when $x \neq y$)
2. $d(x,y) = d(y,x)$
3. $d(x,z) \leq d(x,y) + d(y,z)$ (triangle inequality)

**Distance Function Examples:**
- Euclidian Distance
- Minkowski Distance
- Manhattan Distance