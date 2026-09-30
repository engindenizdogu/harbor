---
title: Autoencoder Snippets
tags: [code-snippets, deep-learning, autoencoders, keras, mnist, dimensionality-reduction]
draft: false
---
Reusable **Keras** code for building and training standard and supervised autoencoders. Examples use the MNIST dataset (784-dimensional inputs, 10 classes).

See [[Autoencoders]] for the conceptual background.

---

## Data Preparation

### Load and Normalize MNIST

```python
from keras.datasets import mnist
import numpy as np

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(60000, 28*28).astype('float32') / 255.
x_test  = x_test.reshape(10000, 28*28).astype('float32') / 255.
```

### One-Hot Encode Labels

```python
def to_one_hot(y, num_class=10):
    results = np.zeros((len(y), num_class))
    for i, label in enumerate(y):
        results[i, label] = 1.
    return results

y_train_vec = to_one_hot(y_train)
y_test_vec  = to_one_hot(y_test)
```

### Train / Validation Split

```python
rand_indices  = np.random.permutation(60000)
train_indices = rand_indices[0:10000]
valid_indices = rand_indices[10000:20000]

x_tr  = x_train[train_indices, :]
y_tr  = y_train_vec[train_indices, :]
x_val = x_train[valid_indices, :]
y_val = y_train_vec[valid_indices, :]
```

---

## Unsupervised Autoencoder

### Build Model

```python
from keras.layers import Input, Dense
from keras import models

input_img  = Input(shape=(784,), name='input_img')
enc_dense_1 = Dense(500, activation='tanh')(input_img)
enc_dense_2 = Dense(300, activation='tanh')(enc_dense_1)
enc_dense_3 = Dense(100, activation='tanh')(enc_dense_2)
bottleneck  = Dense(2,   activation='tanh')(enc_dense_3)   # 2D bottleneck

dec_dense_1 = Dense(100, activation='tanh')(bottleneck)
dec_dense_2 = Dense(300, activation='tanh')(dec_dense_1)
dec_dense_3 = Dense(500, activation='tanh')(dec_dense_2)
dec_dense_4 = Dense(784, activation='sigmoid')(dec_dense_3)  # sigmoid for [0,1] output

ae = models.Model(input_img, dec_dense_4)
ae.summary()
```

### Compile and Train

```python
from tensorflow.keras import optimizers

ae.compile(
    loss='binary_crossentropy',
    optimizer=optimizers.RMSprop(learning_rate=0.002, momentum=0.01)
)

history = ae.fit(
    x_tr, x_tr,
    batch_size=128,
    epochs=200,
    validation_data=(x_val, x_val)
)
```

### Extract Encoder for Feature Visualization

```python
ae_encoder   = models.Model(input_img, bottleneck)
encoded_test = ae_encoder.predict(x_test)  # shape: (10000, 2)
```

---

## Supervised Autoencoder (SAE)

### Build Model (with classifier branch off bottleneck)

```python
from keras.layers import Input, Dense, Dropout
from keras import models

input_img   = Input(shape=(784,), name='input_img')
enc_dense_1 = Dense(500, activation='tanh')(input_img)
enc_dense_2 = Dense(300, activation='tanh')(enc_dense_1)
enc_dense_3 = Dense(100, activation='tanh')(enc_dense_2)
bottleneck  = Dense(2,   activation='tanh')(enc_dense_3)

# Decoder branch
dec_dense_1 = Dense(100, activation='tanh')(bottleneck)
dec_dense_2 = Dense(300, activation='tanh')(dec_dense_1)
dec_dense_3 = Dense(500, activation='tanh')(dec_dense_2)
dec_dense_4 = Dense(784, activation='sigmoid')(dec_dense_3)

# Classifier branch (with Dropout to reduce overfitting)
cls_1     = Dense(64,  activation='tanh')(bottleneck)
dropout_1 = Dropout(0.5)(cls_1)
cls_2     = Dense(128, activation='tanh')(dropout_1)
dropout_2 = Dropout(0.5)(cls_2)
cls_out   = Dense(10, activation='softmax')(dropout_2)

sae = models.Model(input_img, [dec_dense_4, cls_out])
sae.summary()
```

### Compile with Multiple Losses

```python
sae.compile(
    loss=['binary_crossentropy', 'categorical_crossentropy'],
    loss_weights=[1, 0.1],   # low classification weight reduces overfitting
    optimizer=optimizers.RMSprop(learning_rate=0.002, momentum=0.01)
)
```

### Train with Multiple Targets

```python
history = sae.fit(
    x_tr, [x_tr, y_tr],
    batch_size=128,
    epochs=30,
    validation_data=(x_val, [x_val, y_val])
)
```

### Extract SAE Encoder and Evaluate Features

```python
sae_encoder = models.Model(input_img, bottleneck)
f_tr  = sae_encoder.predict(x_tr)
f_val = sae_encoder.predict(x_val)
f_te  = sae_encoder.predict(x_test)

# Build a small classifier on top of the 2D features
input_feat = Input(shape=(2,))
h1  = Dense(128, activation='relu')(input_feat)
h2  = Dense(128, activation='relu')(h1)
out = Dense(10, activation='softmax')(h2)

clf = models.Model(input_feat, out)
clf.compile(
    loss='categorical_crossentropy',
    optimizer=optimizers.RMSprop(learning_rate=1e-4),
    metrics=['acc']
)
clf.fit(f_tr, y_tr, batch_size=32, epochs=30, validation_data=(f_val, y_val))
```

---

## Visualization

### Visualize Reconstructions

```python
import matplotlib.pyplot as plt
import numpy as np

ae_output = ae.predict(x_test).reshape((10000, 28, 28))

fig, axes = plt.subplots(nrows=5, ncols=4, figsize=(4, 4))
for ax, i in zip(axes.flat, np.arange(20)):
    ax.imshow(ae_output[i], cmap='gray')
    ax.axis('off')
plt.tight_layout()
plt.show()
```

### Visualize 2D Latent Space (Color-Coded by Class)

```python
colors      = np.array(['r', 'g', 'b', 'm', 'c', 'k', 'y', 'purple', 'darkred', 'navy'])
colors_test = colors[y_test]

fig = plt.figure(figsize=(6, 6))
plt.scatter(encoded_test[:, 0], encoded_test[:, 1], s=10, c=colors_test, edgecolors=colors_test)
plt.axis('off')
plt.tight_layout()
plt.show()
```

### Plot Training / Validation Loss

```python
loss     = history.history['loss']
val_loss = history.history['val_loss']
epochs   = range(len(loss))

plt.plot(epochs, loss,     'bo', label='Training Loss')
plt.plot(epochs, val_loss, 'r',  label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()
```
