---
title: Algorithms
parent: Machine Learning
---
# Regression
## Linear Regression
**Prediction:**
$$fw(x) = y = w^Tx + \beta = w_1x + w_0$$
**Loss:**
$$L(x,y,w) = (fw(x) − y)^2$$
**Why use squared loss?**
- Prevents errors from cancelling out
- Penalizes large errors
- Easily differentiable

**Closed Form Solution (Normal Equation)**
L2 Loss (squared loss): 
$$L2 = {1 \over N} {\sum(w^⊤x − y)^2}$$
we have (solve for ${\vartheta L(w) \over \vartheta(w)}=0$),
$$ {\vartheta L(w) \over \vartheta(w)} = X^TXw-y^TX $$
Solution:
$$w^∗ =(X^TX)^−1X^Ty$$
## Linear Regression with Gradient Descent
Update weights using ($\alpha$ is the learning rate):

$$ w:= w - \alpha * \bigtriangledown L(w) $$

where the loss function $L(w)$ is defined as (matrix form):

$$ L(w) = {2\over N} * X^T(Xw-y)$$

or (component-wise):

$$ L(w) = {2\over N} * \sum_i^n (x_i*w_i - y_i)x_i$$

> **Note: $\bigtriangledown L(w)$ = ${\vartheta L(w) \over \vartheta(w)}$** 


**Gradient Descent Options:**
- Gradient Descent (calculate for all of the training set X at once)
	- Can be very slow
	- Datasets may not fit in memory
	- Doesn’t allow online (on-the-fly) model updates
	- Guaranteed to converge to the global minimum for convex error surfaces and to a local minimum for non-convex surfaces
- Stochastic Gradient Descent (shuffle X and evaluate one row at a time, check for stopping condition)
	- Allow for online update with new examples
	- With a high variance that cause the objective function to fluctuate heavily
- (Batch) Gradient Descent (use mini batches instead of evaluating one row at a time, check for stopping condition)
	- Reduces the variance of the parameter updates, which can lead to more stable convergence
	- Can make use of highly optimized matrix optimizations
* Adaptive learning rates (see *AdaGrad* algorithm)

> **Note:** Closed form solution can be very slow with datasets that have many rows

#### L1/L2 Regularization (LASSO/Ridge Regression)
- L2:
	- sum-of-squares error + $\alpha w^Tw$
	- Can calculate the closed form solution 
	- Can use it with gradient descent
	- Do not generally regularize the bias term
	- Handles multicollinearity well

- L1:
	- sum-of-squares error + $\alpha \vert w \vert$
	- Non-zero coefficients indicate important features
	- Must use iterative methods (no closed form solution)

Use L1 when:
- You have many features and suspect most are irrelevant
- You want interpretable models with feature selection
- You need to identify the most important predictors

Use L2 when:
- Most features are potentially useful
- You want stable coefficient estimates
- Computational efficiency is important
- Features are highly correlated

## Polynomial Regression


# Classification
## Linear Classification Algorithms

> $w$ is the normal vector to the hyperplane which separates points into the positive class or negative class.
### Least-Square Classification
Very similar to linear regression. Same principles apply, just assign {-1, 1} to classes. Then compute the least squares optimization. The decision boundary will always be $f(x)=0$, so the prediction will have a $sign$ function.
$$f(x) = \begin{cases}
>0 & \text{decide } y_1 \\
<0 & \text{decide } y_2
\end{cases}$$

**2 classes:**
![](../../../assets/images/least_squares_class.png)

**3 classes (example why it might perform badly):**
> For >2 classes, use one-hot-encoding.

![](../../../assets/images/least_squares_3class.png)
**Cons:**
- Sensitive to outliers (squared error penalizes large mistakes heavily)
- Not ideal for classification (treats it as regression)
- Can give predictions outside [-1, +1] range
- Often outperformed by logistic regression or SVM

> Brain Teaser: You can also try to train two different linear models and try to interpret results.
> ![](../../../assets/images/lsc_teaser.png)
### Linear Discriminant Analysis / Fisher’s Linear Discriminant
Good Illustration: [An illustrative introduction to Fisher's Linear Discriminant - Thalles' blog](https://sthalles.github.io/fisher-linear-discriminant/)

Find an orientation along which the projected samples are well separated.
![](../../../assets/images/fishers_linear_disc.png)

**Fisher's Linear Discriminant**
- We want class means to be as far as possible. The denominator is the total within-class scatter of the projected samples.
$$ \arg\max_{w} \frac{\vert m_{+} - m_{-} \vert ^2}{s_{+}^2 + s_{-}^2} $$
where $s_+^2$ or $s_-^2$ is (almost like variance),
$$ s_{+}^2 = \sum_{x \in C_{+}} (w^T x - m_{+})^2 $$
$$m_+ = \frac{1}{N_+} \sum_{x \in C_+} \mathbf{w}^T \mathbf{x} = \mathbf{w}^T \mathbf{m}_+$$
Define following matrices:
$$S_+ = \sum_{x \in C_+} (\mathbf{x} - \mathbf{m}_+)(\mathbf{x} - \mathbf{m}_+)^T$$
$$S_W = S_+ + S_-$$

> [!NOTE] Note!
> $S_+$ or $S_-$ takes the form
> $$\begin{bmatrix} var(x_1) && cov(x_1,x_2) \\ cov(x_1,x_2) && var(x_2) \end{bmatrix}$$

$$S_B = (m_+-m_-)(m_+-m_-)^T$$
Using these we obtain,
$$J(\mathbf{w}) = \frac{\vert m_+ - m_- \vert ^2}{s_+^2 + s_-^2} = \frac{\mathbf{w}^T S_B \mathbf{w}}{\mathbf{w}^T S_W \mathbf{w}}$$
$J$ is maximized when (take derivate with respect to w) $$(w^TS_Bw)S_Ww = (w^TS_Ww)S_Bw$$
Notice:
- $w^TS_W​w$ and $w^TS_Bw$ are scalars, thus we get $$\alpha S_Ww = \beta S_Bw$$
- If we take $\lambda = \alpha / \beta$ we get $S_B​w=λS_W​w$ which the generalized eigenvalue problem:
$$S_W^{−1}​S_B​w=λw$$

From the generalized eigenvalue equation, we derive that the optimal $w$ is:
$$w∝ S_W^{−1}(m_+−m_−)$$

> [!NOTE] Yes but how?!
> Notice $(m_+​−m_−​)^Tw$ in $S_B​w=(m_+​−m_−​)(m_+​−m_−​)^Tw$ is a scalar. That means the equation looks like $S_B​w=c.(m_+​−m_−​)$. This shows that $S_B​w$ is always proportional to $(m_+−m_−)$ regardless of what $w$ is! Plug this into the equation above to get the generalized eigenvalue equation.

To summarize, Fisher's Discriminant,
- Gives the linear function with the maximum ratio of between-class scatter to within-class scatter
- The problem, e.g. classification, has been reduced from a d-dimensional problem to a more manageable one-dimensional problem.
- Can be extended to multiclass classification
### Support Vector Machines
### Rosenblatts’ Perceptron (not very popular right now?)
### Logistic Regression *(usually performs better than the algorithms above)*
### Where can linear classifiers fail?
![](../../../assets/images/linear_classfiers_example.png)
## k-NN for Estimation and Prediction
You can use k-NN for estimating missing values or prediction

# Other
## Bayesian Decision Methods
Given observation x, the decision is based on posterior probability:
- Decide $y_1$, if $P(y_1 \vert x) > P(y_2 \vert x)$
- Decide $y_2$, if $P(y_2 \vert x) > P(y_1 \vert x)$

Note that, $P(y_1 \vert x) = {P(x \vert y_1).P(y_1) \over P(x)}$ and $P(y_2 \vert x) = {P(x \vert y_2).P(y_2) \over P(x)}$ so the probability $P(x)$ does not matter in our decision (same for both).

Probability of error:
$$P(error \vert x) = \begin{cases}
P(y_1 \vert x), & \text{if decide } y_2 \text{ but } y_1 \text{ is true} \\
P(y_2 \vert x), & \text{if decide } y_1 \text{ but } y_2 \text{ is true}
\end{cases}$$

Goal is to minimize error (based on single instance):
$$P(error \vert x) = min[P(y_1 \vert x), P(y_2 \vert x)]$$

Minimizing average error:
$$P(error) = \int_{-\infty}^{\infty} P(error, x)\,dx = \int_{-\infty}^{\infty} P(error \vert x)p(x)\,dx$$

**Generalizing for more classes:**
- Feature vector $x = (x1,x2,...,x_d)$ ∈ $R^d$: allow use of more than one feature
- $y1,y2,...,y_c$: finite set of c states of nature, i.e., categories (can be more than two)
- $\alpha_1,\alpha_2,...,\alpha_a$: a finite set of possible actions
- $λ(α_i \vert y_i)$: loss function, describes the loss incurred for taking action $\alpha_i$ when state of nature is $y_i$
- $P(y_i)$: prior probability that state of nature is $y_i$
- $p(x \vert yi)$: state conditional probability for $x$

The ***expected loss***, or ***conditional risk***, of taking action  $\alpha_i$ is:
$$R(\alpha_i\vert x) = \sum_{j=1}^{c} \lambda(\alpha_i\vert y_j)P(y_j \vert x)$$

Choose $\alpha(x)$ that minimizes overall risk:

$$R = \int R(\alpha(x) \vert x)p(x)\,dx$$
$$R(\alpha_i \vert x) = \sum_{j=1}^{c} \lambda(\alpha_i \vert y_j)P(y_j \vert x)$$
$$\alpha^*=argmin_{\alpha_i}R(\alpha_i \vert x)$$

## Principal Component Analysis (PCA)



