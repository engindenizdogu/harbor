---
title: Variational Autoencoders
tags: [deep-learning, generative-models, vae, autoencoders, dimensionality-reduction, kl-divergence]
draft: false
---
A Variational Autoencoder (VAE) extends the standard autoencoder into a **probabilistic generative model**. Instead of encoding to a fixed code vector, the encoder outputs a **distribution** (mean $\mu$ and log-variance $\log \sigma^2$). A code vector $z$ is then **randomly sampled** from this distribution and passed to the decoder.

## Sampling Pipeline

$$\text{Input Image} \to \text{Encoder} \to (\mu,\, \log \sigma^2) \to \text{Sample } z \to \text{Decoder} \to \text{Output Image}$$

### Reparameterization Trick

Backpropagation cannot flow through a stochastic sampling operation. The reparameterization trick makes sampling differentiable:

$$\sigma = e^{0.5 \cdot n} \quad \text{(where } n = \log \sigma^2 \text{)}$$
$$v = \sigma \cdot \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, 1)$$
$$z = \mu + v$$

This separates the **stochasticity** ($\varepsilon$) from the **learnable parameters** ($\mu$, $\log \sigma^2$), allowing gradients to flow.

---

## Loss Function

$$\mathcal{L} = \underbrace{\mathcal{L}_{\text{Gen}}}_{\text{reconstruction}} + \lambda \cdot \underbrace{\mathcal{L}_{\text{KL}}}_{\text{regularization}}$$

- **Generation Loss** $\mathcal{L}_{\text{Gen}}$: L2 distance or cross-entropy between input and reconstruction.
- **KL Loss** $\mathcal{L}_{\text{KL}}$: Kullback-Leibler divergence between the learned distribution and $\mathcal{N}(0, I)$.

### Why is KL Loss Necessary?

Without KL regularization, the encoder learns to set $\sigma \to 0$ — collapsing the VAE into a standard (deterministic) autoencoder:

- Minimizing generation loss → encourage $z$ close to $\mu$ → encourage small $\sigma$.
- **VAE with $\sigma = 0$ is exactly a standard AE.**

The KL term counteracts this by:
1. **Encouraging large variance** $\sigma$ (avoids vanishing variance).
2. **Pulling the mean $\mu$ toward the origin** (avoids isolated clusters in latent space).

---

## KL Divergence

A measure of distance between two probability distributions:

$$D_{\text{KL}}(P \| Q) = \sum_x P(x) \log \frac{P(x)}{Q(x)}$$

For a Gaussian with parameters $(\mu, \sigma)$ vs. $\mathcal{N}(0, 1)$:

$$D_{\text{KL}} = -\frac{1}{2} \sum_j \left(1 + \log \sigma_j^2 - \mu_j^2 - \sigma_j^2\right)$$

---

## Generative Capabilities

Because the latent space is structured and continuous, you can:

- **Interpolate** between two images by averaging their $\mu$ vectors.
- **Perform semantic arithmetic**: e.g., add a "smile vector" to alter an image's expression.

---

## Keras Implementation

```python
import tensorflow as tf
from tensorflow import keras
import numpy as np

latent_dim = 20

# --- Encoder ---
encoder_inputs = keras.Input(shape=(784,))
x = keras.layers.Dense(256, activation='relu')(encoder_inputs)
z_mean = keras.layers.Dense(latent_dim)(x)
z_log_var = keras.layers.Dense(latent_dim)(x)

# Reparameterization
def sampling(args):
    z_mean, z_log_var = args
    epsilon = tf.random.normal(shape=tf.shape(z_mean))
    return z_mean + tf.exp(0.5 * z_log_var) * epsilon

z = keras.layers.Lambda(sampling)([z_mean, z_log_var])
encoder = keras.Model(encoder_inputs, [z_mean, z_log_var, z], name='encoder')

# --- Decoder ---
decoder_inputs = keras.Input(shape=(latent_dim,))
x = keras.layers.Dense(256, activation='relu')(decoder_inputs)
decoder_outputs = keras.layers.Dense(784, activation='sigmoid')(x)
decoder = keras.Model(decoder_inputs, decoder_outputs, name='decoder')

# --- VAE Model with custom loss ---
class VAE(keras.Model):
    def __init__(self, encoder, decoder, **kwargs):
        super().__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder

    def call(self, x):
        z_mean, z_log_var, z = self.encoder(x)
        reconstruction = self.decoder(z)
        # KL divergence loss
        kl_loss = -0.5 * tf.reduce_mean(
            1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var)
        )
        self.add_loss(kl_loss)
        return reconstruction

vae = VAE(encoder, decoder)
vae.compile(optimizer='adam', loss='binary_crossentropy')
```

---

## VAE vs. Standard Autoencoder

| | Standard AE | VAE |
|---|---|---|
| Encoding | Fixed code vector | Distribution $(\mu, \sigma)$ |
| Latent space | Potentially discontinuous | Continuous, structured |
| Generative? | No (no principled sampling) | Yes |
| Loss | Reconstruction only | Reconstruction + KL |

---

## Related Notes
- [[Autoencoders]] - Standard and convolutional autoencoders; the foundation VAE builds on.
- [[Generative Adversarial Networks]] - Alternative generative approach; produces sharper images but lacks structured latent space.
- [[Image Generation MOC]] - Overview of image generation models.
