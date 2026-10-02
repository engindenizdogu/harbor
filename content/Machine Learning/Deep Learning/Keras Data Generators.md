---
title: Keras Data Generators
tags: [deep-learning, keras, data-science]
draft: false
---

## Overview of On-the-Fly Generation

When training deep learning models on large datasets (such as high-resolution image sets or extensive video segments), loading all samples into the system's memory (RAM) is often impossible. In these scenarios, data must be loaded and preprocessed dynamically, or **on-the-fly**, during training.

Keras addresses this challenge through the `keras.utils.Sequence` class. By subclassing `Sequence`, you can build custom data generators that read mini-batches of data from disk, preprocess them, and feed them directly to the model during training.

## The Keras Sequence Interface

To implement a custom data generator, you subclass `keras.utils.Sequence` and implement the following core methods:

1. `__init__(self, ...)`: Configures the dataset references (such as lists of file IDs and labels), batch sizes, spatial dimensions, channels, and shuffling options.
2. `__len__(self)`: Denotes the number of batches per epoch. It is calculated by dividing the total number of samples by the batch size.
3. `__getitem__(self, index)`: Retrieves a specific batch at the given `index`. This method performs the actual loading and preprocessing of the data batch.
4. `on_epoch_end(self)`: Executed at the end of each epoch. It is typically used to reshuffle data indices to ensure the network receives samples in a different order each epoch, preventing overfitting.

## Custom DataGenerator Implementation

Here is the standard implementation template for a custom Keras data generator:

```python
import numpy as np
import keras

class DataGenerator(keras.utils.Sequence):
    def __init__(self, list_IDs, labels, batch_size=32, dim=(32, 32), 
                 n_channels=1, n_classes=10, shuffle=True):
        """
        Initialization settings for the data generator.
        """
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.list_IDs = list_IDs
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        """
        Returns the number of batches per epoch.
        """
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        """
        Generates one batch of data.
        """
        # Generate indexes of the batch
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]

        # Find list of temporary IDs to load
        list_IDs_temp = [self.list_IDs[k] for k in indexes]

        # Generate data
        X, y = self.__data_generation(list_IDs_temp)

        return X, y

    def on_epoch_end(self):
        """
        Updates indexes after each epoch.
        """
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def __data_generation(self, list_IDs_temp):
        """
        Generates data containing batch_size samples.
        """
        # Pre-allocate memory for batch X and target labels y
        X = np.empty((self.batch_size, *self.dim, self.n_channels))
        y = np.empty((self.batch_size), dtype=int)

        # Load data and preprocess on-the-fly
        for i, ID in enumerate(list_IDs_temp):
            # Store sample loaded from disk (e.g., NumPy binary format)
            X[i,] = np.load('data/' + ID + '.npy')

            # Store class label
            y[i] = self.labels[ID]

        return X, keras.utils.to_categorical(y, num_classes=self.n_classes)
```

## Model Training Pipeline

Once the generator class is defined, it can be instantiated for the training and validation partitions.

```python
from my_classes import DataGenerator

# Set configuration parameters
params = {
    'dim': (32, 32),
    'batch_size': 64,
    'n_classes': 6,
    'n_channels': 1,
    'shuffle': True
}

# Define partitions and labels dictionary
partition = {
    'train': ['id-1', 'id-2', 'id-3', 'id-4'], 
    'validation': ['id-5', 'id-6']
}
labels = {
    'id-1': 0, 'id-2': 1, 'id-3': 2, 'id-4': 1, 
    'id-5': 1, 'id-6': 0
}

# Instantiate generators
training_generator = DataGenerator(partition['train'], labels, **params)
validation_generator = DataGenerator(partition['validation'], labels, **params)

# Compile and train model
model.compile(optimizer='adam', loss='categorical_crossentropy')

# Feed generators directly to fit
model.fit(
    training_generator,
    validation_data=validation_generator,
    use_multiprocessing=True,
    workers=6
)
```

## Key Advantages of `keras.utils.Sequence`

* **Multiprocessing Safety**: Unlike regular Python generator objects (which use `yield` and are not thread-safe), `keras.utils.Sequence` is index-based (`__getitem__`). This allows Keras to query indices out-of-order, running multiple worker processes safely in parallel without risking duplicate data loading or synchronization locks.
* **Guaranteed Single Ingestion**: Using `Sequence` guarantees that the model goes through all samples exactly once per epoch, preventing bias caused by random-sampling-with-replacement generators.

## Modern Keras Updates

In Keras 3 and modern TensorFlow (2.x+):
* **Deprecation of `fit_generator`**: The method `model.fit_generator()` is deprecated. You should pass `keras.utils.Sequence` objects directly into `model.fit()`.
* **Alternatives**: For more advanced pipelines, `tf.data.Dataset` API offers alternative ways to build high-performance input pipelines using methods like `.map()`, `.batch()`, and `.prefetch()`. However, `keras.utils.Sequence` remains the simplest way to implement custom Python-based logic.

## References and Attribution
* Source: [A detailed example of how to use data generators with Keras](https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly) by Afshine Amidi and Shervine Amidi.
* Code Repository: [afshinea/keras-data-generator](https://github.com/afshinea/keras-data-generator)
