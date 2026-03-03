---
title: Evaluation
---
```python
# Calculate mean squared error without library methods
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