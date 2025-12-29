---
title: Support Vector Machines
---
# Support Vector Machines

| Type              |
| ----------------- |
| Linear Classifier |

**Support Vector Machines (SVM)** are powerful supervised machine learning models primarily used for classification, though they can also be adapted for regression. The core philosophy of SVM is to find the **optimal hyperplane** that separates data into different classes while maintaining the largest possible distance—called the **margin**—between the classes. This makes it a "Max-Margin Classifier," designed to be more robust to new, unseen data.

---

### Core Components
- **Hyperplane:** The decision boundary that separates classes. In a 2D space, this is a line; in 3D, it is a plane; and in higher dimensions, it is a hyperplane.
- **Support Vectors:** These are the data points closest to the hyperplane. They are the "critical points" that define the position and orientation of the boundary. If you move a support vector, the boundary moves; if you move other data points, the boundary stays the same.
- **Margin:** The perpendicular distance between the hyperplane and the support vectors. SVM aims to **maximize** this margin to reduce generalization error.
- **Hard vs. Soft Margin:**
	- **Hard Margin:** Requires every single data point to be correctly classified (only works for perfectly separable data).
    - **Soft Margin:** Uses **Slack Variables** ($\xi$) to allow some misclassifications or points within the margin, balancing the trade-off between a wide margin and low error. This is controlled by the **Regularization Parameter ($C$)**.

### The Kernel Trick
One of the most powerful features of SVM is its ability to handle **non-linear data**. When classes cannot be separated by a straight line, SVM uses a **Kernel Function** to map the data into a higher-dimensional space where a linear separation becomes possible.

- **Common Kernels:** Linear, Polynomial, and **Radial Basis Function (RBF/Gaussian)**.
- **Efficiency:** The "trick" is that SVM can compute the relationship between points in high-dimensional space without ever actually calculating their coordinates in that space, making it computationally efficient.

> **C-Parameter Intuition**
> 
> Think of C as a penalty for misclassification. A large C tells the model "errors are unacceptable," leading to a narrow margin but higher training accuracy (risk of overfitting). A small C tells the model "it's okay to miss a few points for the sake of a simpler, wider boundary" (better generalization).

> **Hinge Loss**
> 
> Unlike Logistic Regression, which uses all data points to calculate its loss, SVM uses Hinge Loss. This loss is zero for points that are correctly classified and outside the margin. This is why SVM is only defined by its support vectors—the rest of the points don't contribute to the loss once they are on the "safe" side of the street.
