---
title: Least-Square Classification
tags: [machine-learning, algorithms]
draft: false
---
| Type              |
| ----------------- |
| Linear Classifier |

Very similar to linear regression. Same principles apply, just assign {-1, 1} to classes. Then compute the least squares optimization. The decision boundary will always be $f(x)=0$, so the prediction will have a $sign$ function.

$$
\begin{aligned}
f(x) = \begin{cases}
>0 & \text{decide } y_1 \\
<0 & \text{decide } y_2
\end{cases}
\end{aligned}
$$

**2 classes:**
![[Pasted image 20260425184917.png]]

**3 classes (example why it might perform badly):**
> For >2 classes, use one-hot-encoding.

![[Pasted image 20260425184927.png]]

**Cons:**
- Sensitive to outliers (squared error penalizes large mistakes heavily)
- Not ideal for classification (treats it as regression)
- Can give predictions outside [-1, +1] range
- Often outperformed by logistic regression or SVM

> Brain Teaser: You can also try to train two different linear models and try to interpret results.![[Pasted image 20260425184934.png]]

