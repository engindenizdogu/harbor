---
title: Bayesian Decision Methods
---
# Bayesian Decision Methods

| Type                            |
| ------------------------------- |
| Generative Classification Model |

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

