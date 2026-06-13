---
title: Activation Functions
tags:
  - machine-learning
  - deep-learning
  - neural-networks
  - fundamentals
draft: false
---

**Activation functions** are mathematical transformations applied to the output of each neuron in a neural network. Without them, a neural network — no matter how many layers deep — would reduce to a single linear transformation, making it no more expressive than logistic regression. Activation functions introduce **non-linearity**, which is what allows networks to learn complex patterns, approximate arbitrary functions, and stack meaningful layers.

## Why Non-Linearity Matters

A neuron computes a weighted sum of its inputs plus a bias:

$$z = \mathbf{w}^T \mathbf{x} + b$$

Without activation, stacking $L$ layers just composes linear functions — which is still linear:

$$\mathbf{W}_L (\mathbf{W}_{L-1} \cdots (\mathbf{W}_1 \mathbf{x})) = \mathbf{W}_\text{eff} \mathbf{x}$$

Applying a non-linear activation $\sigma$ after each layer breaks this collapse, allowing the network to express any continuous function (given sufficient width/depth — Universal Approximation Theorem).

---

## Properties of a Good Activation Function

| Property | Why it matters |
|---|---|
| **Non-linearity** | Required to model complex data |
| **Differentiability** | Needed for gradient-based optimization (backprop) |
| **Monotonicity** | Helps ensure a convex loss surface per layer |
| **Bounded output (sometimes)** | Useful in output layers to produce probabilities |
| **Non-saturating** | Avoids vanishing gradients in deep networks |
| **Computationally cheap** | Applied millions of times during training |

---

## 1. Sigmoid

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

Maps any real input to the range $(0, 1)$. Historically the default choice.

**Derivative:**
$$\sigma'(z) = \sigma(z)(1 - \sigma(z))$$

The maximum derivative value is $0.25$ (at $z=0$).

**Intuition:** Think of it as a smooth, differentiable version of a step function. A neuron "fires" with probability approaching 1 for very large positive inputs, and nearly 0 for very large negative inputs.

**Pros:**
- Output interpretable as a probability
- Smooth, everywhere differentiable
- Well understood theoretically

**Cons:**
- **Vanishing gradient:** Saturates at both tails ($\sigma' \to 0$), causing gradients to vanish in deep networks
- **Non-zero centered:** Outputs are always positive $(0, 1)$, leading to inefficient zig-zagging gradient updates
- Computationally expensive (exponential)

**Use cases:** Binary classification output layer. Rarely used in hidden layers of modern deep networks.

---

## 2. Hyperbolic Tangent (tanh)

$$\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}} = 2\sigma(2z) - 1$$

Maps input to $(-1, 1)$. A rescaled and shifted version of sigmoid.

**Derivative:**
$$\tanh'(z) = 1 - \tanh^2(z)$$

Maximum value is $1$ at $z = 0$.

**Intuition:** Like sigmoid but zero-centered. Negative inputs produce negative outputs, which allows gradients to be both positive and negative — fixing sigmoid's zig-zagging issue.

**Pros:**
- **Zero-centered outputs** → faster convergence than sigmoid
- Stronger gradients than sigmoid (max derivative = 1 vs. 0.25)
- Smooth and differentiable

**Cons:**
- Still **saturates** at extremes — vanishing gradient persists
- Computationally expensive

**Use cases:** Hidden layers in shallow networks, RNN/LSTM gates (where bounded outputs are desirable).

---

## 3. ReLU (Rectified Linear Unit)

$$\text{ReLU}(z) = \max(0, z)$$

The dominant activation function in modern deep learning. Simple, yet remarkably effective.

**Derivative:**
$$\text{ReLU}'(z) = \begin{cases} 1 & z > 0 \\ 0 & z \leq 0 \end{cases}$$

**Intuition:** A neuron is either "on" (passes the signal through unchanged) or "off" (completely blocked). This sparsity — most neurons being inactive at any given input — gives networks a kind of efficient, distributed representation.

**Pros:**
- **No vanishing gradient** for positive activations (gradient = 1)
- Extremely cheap to compute (just a comparison and clamp)
- Induces sparse activation → efficient representations
- Enables training of very deep networks (breakthrough in 2010s)

**Cons:**
- **Dying ReLU problem:** Neurons with $z \leq 0$ have gradient = 0, so they never update. With a bad initialization or high learning rate, many neurons can permanently "die"
- **Not zero-centered** (outputs are $\geq 0$)
- Unbounded output can lead to exploding activations without careful weight initialization

**Use cases:** Default choice for hidden layers in CNNs and deep feedforward networks. Still widely used.

---

## 4. Leaky ReLU

$$\text{LeakyReLU}(z) = \begin{cases} z & z > 0 \\ \alpha z & z \leq 0 \end{cases}$$

where $\alpha$ is a small constant, typically $0.01$.

**Derivative:**
$$\text{LeakyReLU}'(z) = \begin{cases} 1 & z > 0 \\ \alpha & z \leq 0 \end{cases}$$

**Intuition:** Gives dying neurons a small "leak" of gradient — they can still update and potentially recover.

**Pros:**
- Fixes the dying ReLU problem
- Retains most of ReLU's computational efficiency
- Gradient is always non-zero

**Cons:**
- $\alpha$ is a hyperparameter that must be tuned or set manually
- The small negative slope may not always help

**Use cases:** Anywhere ReLU is used but dying neurons are a concern. Common in GANs (discriminator networks).

---

## 5. Parametric ReLU (PReLU)

$$\text{PReLU}(z) = \begin{cases} z & z > 0 \\ a \cdot z & z \leq 0 \end{cases}$$

Like Leaky ReLU, but $a$ is **learned** as a parameter during backpropagation rather than hand-set.

**Pros:**
- Can adapt $a$ to the data, potentially outperforming Leaky ReLU
- Adds minimal parameters (one per channel or per neuron)

**Cons:**
- Risk of overfitting on small datasets
- Slightly more complex training

---

## 6. ELU (Exponential Linear Unit)

$$\text{ELU}(z) = \begin{cases} z & z > 0 \\ \alpha(e^z - 1) & z \leq 0 \end{cases}$$

where $\alpha > 0$ (commonly $1.0$).

**Derivative:**
$$\text{ELU}'(z) = \begin{cases} 1 & z > 0 \\ \text{ELU}(z) + \alpha & z \leq 0 \end{cases}$$

**Intuition:** Smoothly saturates negative inputs to $-\alpha$ (instead of zero) and has a smooth derivative everywhere — combining the best of ReLU and tanh.

**Pros:**
- **Mean activations closer to zero** → reduces bias shift and speeds up learning
- Smooth at $z = 0$, unlike ReLU
- More robust to noisy inputs for negative values

**Cons:**
- Slower to compute due to exponential
- Saturates for very negative inputs (vanishing gradient for $z \ll 0$)

**Use cases:** Deep networks where training instability or dying neurons are concerns. A practical upgrade over ReLU/Leaky ReLU in many architectures.

---

## 7. SELU (Scaled ELU)

$$\text{SELU}(z) = \lambda \begin{cases} z & z > 0 \\ \alpha(e^z - 1) & z \leq 0 \end{cases}$$

with $\lambda \approx 1.0507$ and $\alpha \approx 1.6733$ (derived mathematically).

**Key property:** SELU is **self-normalizing** — when used with LeCun normal weight initialization and a specific architecture, activations converge to zero mean and unit variance across layers, making batch normalization unnecessary.

**Pros:**
- Self-normalizing behavior → stable training in deep networks without BatchNorm
- Outperforms ReLU in some fully connected architectures

**Cons:**
- Only works correctly with specific weight initialization (LeCun normal)
- Primarily designed for fully connected layers, less studied for CNNs

---

## 8. GELU (Gaussian Error Linear Unit)

$$\text{GELU}(z) = z \cdot \Phi(z) = z \cdot \frac{1}{2}\left[1 + \text{erf}\left(\frac{z}{\sqrt{2}}\right)\right]$$

where $\Phi$ is the standard normal CDF. Often approximated as:

$$\text{GELU}(z) \approx 0.5z\left(1 + \tanh\left(\sqrt{\frac{2}{\pi}}(z + 0.044715z^3)\right)\right)$$

**Intuition:** Weights the input by the probability that it is positive under a standard normal distribution. It is a smooth, probabilistic gate — high inputs pass through nearly unchanged; very negative inputs are suppressed; near-zero inputs get a soft, uncertain treatment.

**Pros:**
- Smooth, non-monotonic around zero → richer gradient signal
- Empirically strong performance in large models
- Default in BERT, GPT-2, GPT-3, and most modern Transformers

**Cons:**
- More expensive to compute than ReLU
- Less interpretable intuitively

**Use cases:** The dominant activation in **Transformer architectures** and large language models.

---

## 9. Swish

$$\text{Swish}(z) = z \cdot \sigma(\beta z) = \frac{z}{1 + e^{-\beta z}}$$

where $\beta$ can be a fixed constant (e.g., $1$) or a learnable parameter. When $\beta = 1$ and $z > 0$, Swish ≈ $z$; when $\beta \to \infty$, Swish $\to$ ReLU.

**Discovered** by Google Brain via neural architecture search (2017).

**Pros:**
- Smooth and non-monotonic
- Outperforms ReLU on deep networks in various benchmarks
- Unbounded above (like ReLU), bounded below

**Cons:**
- Slightly more expensive than ReLU
- Marginal gains over GELU in practice

**Use cases:** EfficientNet and other modern CNNs; a strong drop-in replacement for ReLU.

---

## 10. Softmax

$$\text{Softmax}(\mathbf{z})_i = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}$$

Softmax is a **vector-to-vector** function (unlike the others which operate element-wise). It converts a vector of raw scores (logits) into a probability distribution over $K$ classes.

**Key properties:**
- All outputs are in $(0, 1)$
- Outputs sum to exactly $1$
- Amplifies the largest logit relative to others (controlled by temperature)

**Numerical stability:** The naive formula can overflow for large $z_i$. In practice, subtract the max logit first:

$$\text{Softmax}(z_i) = \frac{e^{z_i - \max(\mathbf{z})}}{\sum_j e^{z_j - \max(\mathbf{z})}}$$

**Temperature scaling:** Dividing logits by temperature $T$ before softmax:
- $T \to 0$: approaches argmax (one-hot)
- $T \to \infty$: uniform distribution
- $T > 1$: softer / more uncertain outputs (used in knowledge distillation)

**Use cases:** Final layer for **multi-class classification**. Also used in attention mechanisms (Scaled Dot-Product Attention in Transformers uses softmax to normalize attention weights).

---

## Summary Comparison

| Function | Range | Zero-centered | Saturates | Vanishing Grad | Dying Neurons | Modern Use |
|---|---|---|---|---|---|---|
| Sigmoid | $(0, 1)$ | No | Yes (both) | Severe | No | Output (binary) |
| tanh | $(-1, 1)$ | Yes | Yes (both) | Moderate | No | RNN gates |
| ReLU | $[0, \infty)$ | No | No | No (positive) | Yes | CNNs, MLP |
| Leaky ReLU | $(-\infty, \infty)$ | No | No | No | No | GANs |
| ELU | $(-\alpha, \infty)$ | Near-zero | Negative only | Mild | No | Deep MLP |
| SELU | $(-\lambda\alpha, \infty)$ | Self-normalizing | Negative only | Mild | No | Deep MLP (no BN) |
| GELU | $\approx(-0.17, \infty)$ | Near-zero | No | No | No | Transformers, LLMs |
| Swish | $\approx(-0.28, \infty)$ | Near-zero | No | No | No | EfficientNet |
| Softmax | $(0, 1)^K$, sums to 1 | N/A | N/A | N/A | No | Multi-class output |

---

## The Vanishing Gradient Problem

When gradients are backpropagated through many layers, they are multiplied by the derivative of the activation at each step. If those derivatives are consistently $< 1$ (as with sigmoid's max of $0.25$), the gradient shrinks exponentially with depth:

$$\frac{\partial \mathcal{L}}{\partial w^{(1)}} = \frac{\partial \mathcal{L}}{\partial a^{(L)}} \cdot \prod_{l=2}^{L} \sigma'(z^{(l)})$$

After $L = 10$ layers with sigmoid, the gradient is multiplied by at most $0.25^{10} \approx 10^{-6}$ — effectively zero. The network cannot learn.

**Solutions:** ReLU and its variants, skip connections ([[Residual Networks]]), layer normalization, careful weight initialization.

---

## Choosing the Right Activation

- **Hidden layers (default):** ReLU → try GELU/Swish if performance matters
- **Hidden layers (Transformers/LLMs):** GELU (essentially universal)
- **Hidden layers (RNNs/LSTMs):** tanh (for cell state), sigmoid (for gates)
- **Output layer — binary classification:** Sigmoid
- **Output layer — multi-class classification:** Softmax
- **Output layer — regression:** Linear (no activation) or ReLU (non-negative outputs)
- **Dying ReLU observed:** Switch to Leaky ReLU, ELU, or PReLU

---

## Related Concepts

- [[Loss Functions]] — activation functions define what a network can represent; loss functions define what it optimizes
- [[Backpropagation]] — the mechanism by which activation derivatives flow to update weights
- [[Batch Normalization]] — often used alongside activations to stabilize training; can reduce the importance of activation choice
- [[Neural Network Architectures]]

---

*Source: Synthesized from [Deep Learning (Goodfellow et al.)](https://www.deeplearningbook.org/), [CS231n Stanford](https://cs231n.github.io/neural-networks-1/), [Hendrycks & Gimpel (2016) — GELU paper](https://arxiv.org/abs/1606.08415), [Ramachandran et al. (2017) — Swish paper](https://arxiv.org/abs/1710.05941), and [Clevert et al. (2015) — ELU paper](https://arxiv.org/abs/1511.07289).*
