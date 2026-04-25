---
title: Batch Normalization
---
# Batch Normalization
Batch Normalization (BN) is a technique applied between the hidden layers of a neural network. The goal of Batch Normalization is to get stable gradients and thus faster convergence by normalizing inputs of the next hidden layer. It also acts as regularization which helps the network to generalize better.

Overall:
- Batch Normalization is a technique to speed up training and help make the model more stable.
- BN is just another network layer that gets inserted between a hidden layer and the next hidden layer. Its job is to take the outputs from the first hidden layer and normalize them before passing them on as the input of the next hidden layer.

Advantages:
1. Improves gradient flow through the network.
2. Allows use of saturating nonlinearities and higher learning rates.
3. Makes weights easier to initialize.
4. Act as a form of regularization and may reduce the need for dropout.
5. Results in faster convergence

**Original article:** [1502.03167](https://arxiv.org/pdf/1502.03167)

**Useful links:** 
- [Batch Norm Explained Visually - How it works, and why neural networks need it | Towards Data Science](https://towardsdatascience.com/batch-norm-explained-visually-how-it-works-and-why-neural-networks-need-it-b18919692739/)
- [Why Does Batch Norm Work? (C2W3L06)](https://www.youtube.com/watch?v=nUUqwaxLnWs&t=473s)

