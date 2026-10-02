---
title: Autoencoders
tags: [deep-learning, autoencoders, dimensionality-reduction, supervised-learning, unsupervised-learning, mnist]
draft: false
---
An autoencoder is a neural network trained to reconstruct its input. It compresses the input into a **bottleneck** (low-dimensional latent space) and then reconstructs the original signal from that compressed representation. They are primarily used for **unsupervised dimensionality reduction**.

## Architecture

An autoencoder has two components:

- **Encoder**: Maps the high-dimensional input to a low-dimensional latent representation.
- **Decoder**: Reconstructs the original input from the latent representation.

The bottleneck layer is the key — its dimensionality determines the compression factor.

### Typical Dense Autoencoder (MNIST 784 → 2)

```
Input (784)
  → Dense(500, tanh)
  → Dense(300, tanh)
  → Dense(100, tanh)
  → Bottleneck / Code (2, tanh)
  → Dense(100, tanh)
  → Dense(300, tanh)
  → Dense(500, tanh)
  → Output (784, sigmoid)
```

- `tanh` is preferred over `relu` in this architecture: `relu` can cause exploding loss or noisy/random-looking reconstructions.
- The final decoder layer uses `sigmoid` because the input data is normalized to [0, 1].
- Loss: `binary_crossentropy` (appropriate for pixel-level reconstruction of normalized images).

---

## Unsupervised Autoencoder

Trained only on the reconstruction objective. The latent features learned this way are **not discriminative** — a downstream classifier trained on 2D features achieves only ~55-70% accuracy on MNIST (vs. ~97% on the raw data). Features do not form clear clusters or clean class boundaries in 2D space.

---

## Supervised Autoencoder (SAE)

Extends the standard autoencoder by adding a **classification branch** directly off the bottleneck layer. This forces the encoder to learn a latent space that is simultaneously useful for reconstruction *and* classification — making the features discriminative.

### Architecture

The encoder and decoder remain the same. A classifier head is attached to the bottleneck:

```
Bottleneck (2)
  → Dense(64, tanh)
  → Dense(128, tanh)
  → Dense(10, softmax)
```

The model has **two outputs**: the reconstruction and the class prediction.

### Multi-Output Training

The SAE is compiled with two loss functions and configurable weights:

```
Loss = w1 * binary_crossentropy(reconstruction) + w2 * categorical_crossentropy(classification)
```

A lower weight on the classification loss (e.g., `w2 = 0.1`) reduces overfitting from the classifier branch without compromising reconstruction quality.

### Discriminativeness

A classifier trained on the 2D latent features from the SAE achieves **>90% test accuracy** on MNIST — validating that the supervised constraint produces far more discriminative representations.

---

## Overfitting and Regularization

The classification branch is more prone to overfitting than the reconstruction branch. Remedies:

- Add **Dropout** layers (e.g., `Dropout(0.5)`) in the classifier head.
- Reduce the classification **loss weight** relative to the reconstruction loss.
- Reduce the number of training **epochs**.

---

## Key Hyperparameters

| Parameter | Typical Value | Notes |
|---|---|---|
| Bottleneck size | 2 | For visualization; larger = more capacity |
| Activation (encoder/decoder) | `tanh` | Avoids dead neurons, smoother gradients |
| Activation (output) | `sigmoid` | For [0,1] normalized inputs |
| Reconstruction loss | `binary_crossentropy` | Pixel-wise |
| Classification loss | `categorical_crossentropy` | One-hot labels |
| Optimizer | RMSprop | `lr=0.002`, `momentum=0.01` |
| Batch size | 128 | |

---

## Parameter Counting (Dense Autoencoder)

Example architecture: **784 → 100 → 20 → 100 → 784**

| Layer | Weights | Biases | Total |
|---|---|---|---|
| 784 → 100 | 78,400 | 100 | 78,500 |
| 100 → 20 | 2,000 | 20 | 2,020 |
| 20 → 100 | 2,000 | 100 | 2,100 |
| 100 → 784 | 78,400 | 784 | 79,184 |
| **Total** | | | **161,804** |

---

## Convolutional Autoencoder

For image data, replacing dense layers with convolutional layers yields better spatial feature extraction.

- **Encoder**: `Conv2D` + `MaxPooling2D` (downsampling)
- **Decoder**: `Conv2D` + `UpSampling2D` (upsampling)

```python
from tensorflow import keras

# Encoder
inputs = keras.Input(shape=(28, 28, 1))
x = keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
x = keras.layers.MaxPooling2D((2, 2), padding='same')(x)  # 14x14x32
x = keras.layers.Conv2D(16, (3, 3), activation='relu', padding='same')(x)
encoded = keras.layers.MaxPooling2D((2, 2), padding='same')(x)  # 7x7x16 (bottleneck)

# Decoder
x = keras.layers.Conv2D(16, (3, 3), activation='relu', padding='same')(encoded)
x = keras.layers.UpSampling2D((2, 2))(x)  # 14x14x16
x = keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
x = keras.layers.UpSampling2D((2, 2))(x)  # 28x28x32
decoded = keras.layers.Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)  # 28x28x1

autoencoder = keras.Model(inputs, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
```

---

## Denoising Autoencoder

A denoising autoencoder is trained to **reconstruct clean images from corrupted inputs**, forcing the network to learn more robust and generalizable features.

- **Input**: noisy version of images
- **Target**: original clean images
- Loss: same reconstruction loss (MSE or binary cross-entropy)

```python
import numpy as np

# Add Gaussian noise to training images
noise_factor = 0.4
x_train_noisy = x_train + noise_factor * np.random.randn(*x_train.shape)
x_train_noisy = np.clip(x_train_noisy, 0.0, 1.0)

# Same architecture as standard AE; only the input changes
autoencoder.fit(
    x_train_noisy, x_train,  # noisy input → clean target
    epochs=50,
    batch_size=256,
    validation_data=(x_test_noisy, x_test)
)
```

---

## Dimensionality Reduction Strategy

Autoencoders can reduce high-dimensional data to a compact bottleneck representation. A common pipeline for visualization:

1. **Autoencoder**: 784-dim → 20-dim (fast, nonlinear reduction)
2. **t-SNE**: 20-dim → 2-dim (better visualization than 784 → 2 directly)

**Why not AE directly to 2-dim?** The resulting 2D visualization is poor — too much information is lost in one step.

**Why not t-SNE directly from 784-dim?** Accurate results but extremely slow at high dimensions.

```python
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# 1. Extract 20-dim bottleneck codes
encoder_model = keras.Model(inputs, encoded)
codes = encoder_model.predict(x_test)          # shape: (n, 20)

# 2. Reduce to 2-dim with t-SNE
tsne = TSNE(n_components=2, random_state=42)
codes_2d = tsne.fit_transform(codes)           # shape: (n, 2)

# 3. Visualize
plt.scatter(codes_2d[:, 0], codes_2d[:, 1], c=y_test, cmap='tab10', s=5)
plt.colorbar()
plt.title('AE + t-SNE Latent Space')
plt.show()
```

---

## Related Notes
- [[Neural Networks]] - Foundational building blocks used in the encoder/decoder.
- [[Batch Normalization]] - An alternative regularization technique usable in AE layers.
- [[Keras vs. PyTorch vs. TensorFlow]] - Framework used for implementation.
- [[Variational Autoencoders]] - Probabilistic extension of AE; adds structured, continuous latent space and generative capability.
- [[Generative Adversarial Networks]] - Alternative generative model; no reconstruction loss, produces sharper images.
- [[Autoencoder Snippets]] - Reusable code for building and training AEs in Keras.
- [[ML Preprocessing Snippets]] - One-hot encoding and train/val/test splitting patterns.
