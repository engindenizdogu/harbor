---
title: Preprocessing
---
```python
# Train/Test split (manual)
def train_test_split(X, y, split_size=0.2):
    # Generate shuffled indices
    num_data_points = X.shape[0]
    shuffled_indices = np.random.permutation(num_data_points)

    # Split indices into test and train
    test_set_size = int(num_data_points * split_size)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]

    # Use the indices to split the data
    X_train = X.iloc[train_indices]
    X_test = X.iloc[test_indices]
    y_train = y.iloc[train_indices]
    y_test = y.iloc[test_indices]

    return X_train, X_test, y_train, y_test
```

```python
# Z-score standardization
def standardize(X_train, X_test):
    # Calculate the mean and standard deviation of the training set
    mean = np.mean(X_train, axis=0)
    std = np.std(X_train, axis=0)

    # To prevent division by zero, set std=1 where std is zero
    std[std == 0] = 1

    # Standardize the training set
    X_train_scaled = (X_train - mean) / std

    # Use the training set's mean and std to standardize the test set
    X_test_scaled = (X_test - mean) / std

    return X_train_scaled, X_test_scaled
```