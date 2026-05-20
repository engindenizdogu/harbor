---
title: CNNs
tags: [deep-learning]
draft: false
---
Convolutional Neural Networks are designed to process grid-like data, such as images. They use convolution operations in place of general matrix multiplication in at least one of their layers.

## The Forward Pass (1D / 2D Convolution)
During the forward pass, a filter (kernel) $W$ slides over the input $X$ to produce an output feature map $Y$.
For a simple 2D convolution (without padding or stride):
$$ Y_{i,j} = \sum_m \sum_n X_{i+m, j+n} W_{m,n} + b $$

## Backpropagation in CNNs

Backpropagation in a CNN requires computing three main gradients:
1. The gradient with respect to the filter weights (to update the filter).
2. The gradient with respect to the biases (to update the biases).
3. The gradient with respect to the input feature map (to pass the error down to the previous layer).

Let $\frac{\partial L}{\partial Y}$ be the gradient of the loss with respect to the output of the convolutional layer (this is passed backward from the subsequent layer).

### 1. Gradient with respect to the Filter Weights ($\frac{\partial L}{\partial W}$)
To update the filter weights, we need to know how the loss changes as each weight changes.
Because each weight in $W$ is multiplied by different parts of the input $X$ across the sliding window, the gradient is the **convolution of the input $X$ with the incoming gradient $\frac{\partial L}{\partial Y}$**.
$$ \frac{\partial L}{\partial W_{m,n}} = \sum_i \sum_j X_{i+m, j+n} \frac{\partial L}{\partial Y_{i,j}} $$
*In code, this is computed as a valid cross-correlation between the input $X$ and the upstream gradient $\frac{\partial L}{\partial Y}$.*

### 2. Gradient with respect to the Bias ($\frac{\partial L}{\partial b}$)
The bias $b$ is added to every element of the output feature map $Y$. Therefore, the gradient with respect to the bias is simply the **sum of all gradients** in $\frac{\partial L}{\partial Y}$:
$$ \frac{\partial L}{\partial b} = \sum_i \sum_j \frac{\partial L}{\partial Y_{i,j}} $$

### 3. Gradient with respect to the Input ($\frac{\partial L}{\partial X}$)
To propagate the error back to the previous layer, we need the gradient with respect to the input $X$.
Since each input pixel contributes to multiple output pixels (depending on the filter size), the gradient with respect to a single input pixel is the sum of the gradients from all output pixels it influenced, weighted by the filter weights.
Mathematically, this is equivalent to a **full convolution of the incoming gradient $\frac{\partial L}{\partial Y}$ (zero-padded) with the 180-degree rotated (flipped) filter $W$**.
$$ \frac{\partial L}{\partial X} = \text{Full Convolution} \left( \frac{\partial L}{\partial Y}, W_{\text{flipped}} \right) $$

## Backpropagation Through Pooling Layers

Pooling layers have no learnable parameters, but gradients still need to flow through them to reach earlier layers.

- **Max Pooling:** During the forward pass, max pooling selects the maximum value in a window. During backpropagation, the gradient from the next layer is routed **only to the index that had the maximum value** in the forward pass. All other elements in the pooling window receive a gradient of $0$.
- **Average Pooling:** During the forward pass, the average of the window is taken. During backpropagation, the incoming gradient is **distributed equally** among all elements in the pooling window (i.e., divided by the window size).

*For the mathematical prerequisites, see [[9. Vector Calculus]] and [[Neural Networks]] for the general backpropagation chain rule.*
