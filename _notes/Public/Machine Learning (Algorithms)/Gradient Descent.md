---
title: Gradient Descent
---
# Gradient Descent

| Type         |
| ------------ |
| Optimization |

> Some information on gradient descent can be found on [[Linear Regression]].

**Weight update rule:**

$$ w:= w - \alpha * \bigtriangledown L(w) $$

**Why do we go in the opposite direction of the gradient?**
The gradient tells the direction of steepest _ascent_ of the loss. We go in the opposite direction because that is the direction that minimizes error.

> **Negative gradients:** When taking the gradient, some components being negative just means that increasing those specific parameters would actually decrease the loss - so the gradient descent update (with the negative sign) will increase them to reduce loss overall.