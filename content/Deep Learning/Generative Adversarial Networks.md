---
title: Generative Adversarial Networks
tags: [deep-learning, generative-models, gans, image-generation, adversarial-training]
draft: false
---
A GAN is a **generative model** composed of two neural networks trained in **adversarial competition**:

- **Generator (G):** Takes a random latent vector $z$ as input and produces a fake image.
- **Discriminator (D):** Takes an image (real or fake) and outputs a probability $\in [0, 1]$ of it being real.

The two networks are trained simultaneously until the discriminator can no longer distinguish real from fake — meaning the generator's output is indistinguishable from real data.

---

## Architecture Overview

| Network | Input | Output |
|---|---|---|
| Generator | Random vector $z \sim \mathcal{N}(0, I)$ | Fake image |
| Discriminator | Image (real or fake) | Probability of being real (0 = fake, 1 = real) |

---

## Training Procedure

Training alternates between two steps:

**Step 1 — Update the Discriminator:**
- Feed **real images** with target = 1.
- Feed **fake images** (from G) with target = 0.
- Train D as a binary classifier.
- G's weights are **frozen**.

**Step 2 — Update the Generator:**
- Pass random vectors $z$ through G → D.
- Set target = **1** (we want D to think the fakes are real).
- Only G's weights are updated; D is **frozen**.

Repeat until equilibrium (ideally).

```python
import tensorflow as tf
from tensorflow import keras

# --- Generator ---
def build_generator(latent_dim=100):
    model = keras.Sequential([
        keras.layers.Dense(7 * 7 * 256, use_bias=False, input_shape=(latent_dim,)),
        keras.layers.BatchNormalization(),
        keras.layers.LeakyReLU(),
        keras.layers.Reshape((7, 7, 256)),
        keras.layers.Conv2DTranspose(128, (5, 5), strides=(1, 1), padding='same', use_bias=False),
        keras.layers.BatchNormalization(),
        keras.layers.LeakyReLU(),
        keras.layers.Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same', use_bias=False),
        keras.layers.BatchNormalization(),
        keras.layers.LeakyReLU(),
        keras.layers.Conv2DTranspose(1, (5, 5), strides=(2, 2), padding='same',
                                     use_bias=False, activation='tanh'),  # output 28x28x1
    ])
    return model

# --- Discriminator ---
def build_discriminator():
    model = keras.Sequential([
        keras.layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same', input_shape=(28, 28, 1)),
        keras.layers.LeakyReLU(),
        keras.layers.Dropout(0.3),
        keras.layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same'),
        keras.layers.LeakyReLU(),
        keras.layers.Dropout(0.3),
        keras.layers.Flatten(),
        keras.layers.Dense(1),  # logit output
    ])
    return model

cross_entropy = keras.losses.BinaryCrossentropy(from_logits=True)

def discriminator_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    return real_loss + fake_loss

def generator_loss(fake_output):
    # Generator wants D to output 1 (real) for its fakes
    return cross_entropy(tf.ones_like(fake_output), fake_output)
```

---

## Training Instability

GANs are notoriously difficult to train. Two opposing failure modes:

| Problem | Description | Effect |
|---|---|---|
| D too **strong** | Discriminator perfectly detects all fakes | Generator gradient → 0, learning stops |
| D too **weak** | Discriminator is random | Generator gets no useful signal |

### Solutions

1. **Add decaying noise** to both real and fake images when training D.
2. **Perturb the labels** (label smoothing):
   - Real: $1 \to \text{Uniform}(0.7, 1.2)$
   - Fake: $0 \to \text{Uniform}(0.0, 0.3)$

---

## VAE vs. GAN

| | VAE | GAN |
|---|---|---|
| Training objective | Explicit: GenLoss + KL Loss | Adversarial: no pixel-level comparison |
| Architecture | Single encoder-decoder network | Two competing networks |
| Output quality | Slightly **blurry** (pixel-wise reconstruction loss averages) | **Sharper**, more realistic |
| Generator sees real images? | Yes (input-output pairs) | No — only receives feedback through D |
| Latent space | Structured, continuous (Gaussian prior) | Unstructured random vector |

---

## Related Notes
- [[Autoencoders]] - The encoder-decoder architecture; VAE extends this with a probabilistic latent space.
- [[Variational Autoencoders]] - The VAE alternative to GANs for image generation.
- [[Image Generation MOC]] - Overview of generative image models.
