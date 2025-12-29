---
title: Neural Networks
---
# Neural Networks

| Type           |
| -------------- |
| Neural Network |

# Multi-Layer Perceptron (MLP) Architecture
A single perceptron can only solve linearly separable problems (like the AND/OR gates). To solve non-linear problems (like XOR), we stack them into layers.

- **Input Layer:** Receives the raw feature vectors.    
- **Hidden Layers:** Intermediate layers that extract increasingly complex patterns and representations.
- **Output Layer:** Provides the final prediction (e.g., probabilities for classification).
- **Fully Connected:** In a standard MLP, every neuron in one layer is connected to every neuron in the next.

---
# Activation Functions
Activation functions introduce **non-linearity** into the network, allowing it to learn complex patterns. Without them, multiple layers would just collapse into a single linear transformation.
- **Sigmoid:** Maps input to a range between $(0, 1)$. Useful for binary classification.
- **ReLU (Rectified Linear Unit):** Outputs the input directly if positive, otherwise zero. It is the most common choice for hidden layers because it helps avoid the vanishing gradient problem.
- **Softmax:** Used in the output layer for multi-class classification to turn scores into probabilities that sum to $1$.
- **tanh**
- **Leaky ReLU**
- **Maxout**
- **ELU**

---

# Training: The Backpropagation Algorithm
The goal is to compute the partial derivative of the cost function $C$ with respect to any weight $w$ or bias $b$ in the network. This tells us the "gradient" or the direction we should move to decrease the error.
### 1. The Forward Pass
Before we can calculate errors, we must calculate the activations for each layer. For a given neuron $j$ in layer $l$:
1. Calculate the weighted input $z$:
$$z_j^l = \sum_k w_{jk}^l a_k^{l-1} + b_j^l$$

2. Apply the activation function $\sigma$ (e.g., Sigmoid or ReLU):
$$a_j^l = \sigma(z_j^l)$$

### 2. The Error at the Output Layer ($\delta^L$)
The error for the final layer $L$ is the starting point for the backward pass. It depends on how fast the cost changes relative to the output activation and how fast the activation changes relative to the weighted input:

$$\delta_j^L = \frac{\partial C}{\partial a_j^L} \sigma'(z_j^L)$$

### 3. Propagating the Error Backward ($\delta^l$)
We calculate the error of the current layer $l$ using the error of the next layer $l+1$. This is the "backpropagation" step:

$$\delta^l = ((w^{l+1})^T \delta^{l+1}) \odot \sigma'(z^l)$$

- $(w^{l+1})^T$: The transpose of the weights to move backward.    
- $\odot$: The Hadamard product (element-wise multiplication).

### 4. Calculating the Gradients
Once we have the error $\delta^l$ for a layer, the gradients for the weights and biases are:
- **Gradient for bias:** $\frac{\partial C}{\partial b_j^l} = \delta_j^l$ 
- **Gradient for weight:** $\frac{\partial C}{\partial w_{jk}^l} = a_k^{l-1} \delta_j^l$

### 5. The Weight Update (Gradient Descent)
Finally, we update the weights using the Learning Rate ($\eta$):

$$w_{new} = w_{old} - \eta \frac{\partial C}{\partial w}$$

---
# Key Concepts & Challenges
- **Universal Approximation Theorem:** A feedforward network with a single hidden layer and a finite number of neurons can approximate any continuous function.
- **Vanishing Gradient:** In very deep networks using Sigmoid, gradients can become so small that weights stop updating. ReLU is often used to mitigate this.
- **Overfitting:** Large networks can memorize training data. This is countered using techniques like **Dropout** (randomly disabling neurons) or **L2 Regularization**.