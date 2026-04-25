---
title: Preprocessing
---
```python
# Train/Test split with numpy (shuffle indices)
shuffled_indices = np.random.permutation(x_train.shape[0])
x_tr = x_train[shuffled_indices[:40000]]
y_tr = y_train_vec[shuffled_indices[:40000]]
x_val = x_train[shuffled_indices[40000:]]
y_val = y_train_vec[shuffled_indices[40000:]]

print('Shape of x_tr: ' + str(x_tr.shape))
print('Shape of y_tr: ' + str(y_tr.shape))
print('Shape of x_val: ' + str(x_val.shape))
print('Shape of y_val: ' + str(y_val.shape))
```

```python
# Train/Test split with ratio
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
# one-hot-encoding implementation
def to_one_hot(y, num_class=10):
	y_encoded = np.zeros((y.shape[0], num_class))
	for i in range(y.shape[0]):
		# numpy.org/doc/stable/user/basics.indexing.html#integer-array-indexing
		y_encoded[i, y[i]] = 1 # or y_encoded[i, y[i][0]] = 1

	return y_encoded
```

```python
# Z-score standardization
def standardize(X_train, X_test):
    # Calculate the mean and standard deviation of the training set
    mean = np.mean(X_train, axis=0)
    std = np.std(X_train, axis=0)

    # To prevent division by zero, set std=1 where std is zero
    std[std == 0] = 1 # note: could add an epsilon term

    # Standardize the training set
    X_train_scaled = (X_train - mean) / std

    # Use the training set's mean and std to standardize the test set
    X_test_scaled = (X_test - mean) / std

    return X_train_scaled, X_test_scaled
```