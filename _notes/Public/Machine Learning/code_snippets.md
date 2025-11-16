---
title: Code Snippets
parent: Machine Learning
---
```python
# Train/Test split
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
# Calculate mean squared error (using for loops, todo: convert to matrices)
def mse(X, y, w, b):
    num_rows, num_features = X.shape
    mse = 0

    # Run the predictions for X (yi = wi * X + b)
    for i in range(num_rows):
        y_i = 0
        for j in range(num_features):
            y_i += X.iloc[i,j] * w[j] # Prediction for a single row
        y_i += b # Add bias

        # Calculate the cumulative squared loss
        mse += (y_i - y.iloc[i].item()) ** 2 

    # Return mean error
    return mse / num_rows
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

```python
# Stochastic Gradient Descent (SGD) implementation
def sgd(X, y, learning_rate=0.01, n_iterations=1000):
    m, n = X.shape
    theta = np.random.randn(n, 1)  # Initialize theta with random values
    y = y.values.reshape(-1, 1)    # Reshape y to be a column vector
    mse_history = []  # List to store MSE values over iterations

    for iteration in range(n_iterations):
        for i in range(m):
            random_index = np.random.randint(m)
            Xi = X[random_index:random_index+1]
            yi = y[random_index:random_index+1]
            gradients = 2 * Xi.T.dot(Xi.dot(theta) - yi)
            theta = theta - learning_rate * gradients

        # Store MSE for every iteration
        mse = np.mean((X.dot(theta) - y) ** 2)
        mse_history.append(mse)

        if iteration % 100 == 0 and iteration != 0:
            print(f"Iteration {iteration}: MSE = {mse}")

    return theta, mse_history
```

