---
title: Stochastic Gradient Descent
---
```python
# Stochastic Gradient Descent (SGD) implementation for linear regression
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
	        # b = b - learning_rate * gradient_b where gradient_b = -2/n * np.sum(error)

        # Store MSE for every iteration
        mse = np.mean((X.dot(theta) - y) ** 2)
        mse_history.append(mse)

        if iteration % 100 == 0 and iteration != 0:
            print(f"Iteration {iteration}: MSE = {mse}")

    return theta, mse_history
```

