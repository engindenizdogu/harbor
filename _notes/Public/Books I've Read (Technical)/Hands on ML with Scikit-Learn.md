---
title: Hands on ML with Scikit-Learn, Keras & Tensorflow
---
# Hands on ML with Scikit-Learn
###### Aurélien Geron, 2nd Edition

Find code examples at: [ageron/handson-ml3: A series of Jupyter notebooks that walk you through the fundamentals of ML and DL in Python](https://github.com/ageron/handson-ml3/tree/main)

# ML Methods
1. **Supervised Learning**
   - k-Nearest Neighbors
   - Linear Regression
   - Logistic Regression
   - Support Vector Machines (SVMs)
   - Decision Trees and Random Forests
2. **Unsupervised Learning**
   - **Clustering**
     - k-Means
     - Hierarchical Cluster Analysis (HCA)
     - Expectation Maximization
   - **Visualization and dimensionality reduction**
     - Principal Component Analysis (PCA)
     - Kernel PCA
     - Locally-Linear Embedding (LLE)
     - t-distributed Stochastic Neighbor Embedding (t-SNE)
   - **Association rule learning**
     - Apriori
     - Eclat
3. **Semi-Supervised Learning**

# Batch Learning vs Online (Incremental) Learning
One important parameter of **online learning** systems is how fast they should adapt to changing data: this is called the learning rate. If you set a high learning rate, then your system will rapidly adapt to new data, but it will also tend to quickly forget the old data.
# Generalization
Two main approaches to generalization:
1. **instance-based learning:** the system learns the examples by heart, then generalizes to new cases using a similarity measure
2. **model-based learning**

# Overfitting
Overfitting happens when the model is too complex relative to the amount and noisiness of the training data. The possible solutions are:
- To simplify the model by selecting one with fewer parameters (e.g., a linear model rather than a high-degree polynomial model), by reducing the number of attributes in the training data or by constraining the model
- To gather more training data
- To reduce the noise in the training data (e.g., fix data errors and remove outliers)

# Underfitting
When the model is too simple.
- Selecting a more powerful model, with more parameters
- Feeding better features to the learning algorithm (feature engineering)
- Reducing the constraints on the model (e.g., reducing the regularization hyper parameter)

# Cross-validation
Commonly used when the dataset is small and splitting it into three subsets (training, validation, test) yields a model that is too simple.
[Course: The Data Science Course: Complete Data Science Bootcamp 2025 (Udemy)](https://www.udemy.com/course/the-data-science-course-complete-data-science-bootcamp/learn/lecture/10784420#search)
###### Chapter Questions
1. How would you define Machine Learning?
2. Can you name four types of problems where it shines?
3. What is a labeled training set? 
4. What are the two most common supervised tasks?
5. Can you name four common unsupervised tasks?
6. What type of Machine Learning algorithm would you use to allow a robot to walk in various unknown terrains?
7. What type of algorithm would you use to segment your customers into multiple groups?
8. Would you frame the problem of spam detection as a supervised learning problem or an unsupervised learning problem?
9. What is an online learning system?
10. What is out-of-core learning?
11. What type of learning algorithm relies on a similarity measure to make predictions? 
12. What is the difference between a model parameter and a learning algorithm’s hyperparameter?
13. What do model-based learning algorithms search for? What is the most common strategy they use to succeed? How do they make predictions?
14. Can you name four of the main challenges in Machine Learning?
15. If your model performs great on the training data but generalizes poorly to new instances, what is happening? Can you name three possible solutions?
16. What is a test set and why would you want to use it? 
17. What is the purpose of a validation set?
18. What can go wrong if you tune hyperparameters using the test set?
19. What is cross-validation and why would you prefer it to a validation set?

> Appendix B - ML Workflow Checklist

###### Question
- scikit-learn: What's the difference between fit(), transform() ve fit_transform() functions?

###### Exercises
1. Try a Support Vector Machine regressor (sklearn.svm.SVR), with various hyper parameters such as kernel="linear" (with various values for the C hyperpara meter) or kernel="rbf" (with various values for the C and gamma hyperparameters). Don’t worry about what these hyperparameters mean for now. How does the best SVR predictor perform?
2. Try replacing GridSearchCV with RandomizedSearchCV.
3. Try adding a transformer in the preparation pipeline to select only the most important attributes.
4. Try creating a single pipeline that does the full data preparation plus the final prediction. 
5. Automatically explore some preparation options using GridSearchCV.

# Metrics: Accuracy, Precision, Recall & F1 Score
**Accuracy** is generally not the preferred performance measure for classifiers, especially when you are dealing with skewed datasets (i.e., when some classes are much more frequent than others) - Example; MNIST dataset, classifying "not-5's". You would be right 90% of the time even with a dumb classifier.

> About precision and recall:
> Now your 5-detector does not look as shiny as it did when you looked at its accuracy. When it claims an image represents a 5, it is correct only 72.9% of the time (precision). More over, it only detects 75.6% of the 5s (recall).

The **F1 score** favors classifiers that have similar precision and recall. This is not always what you want: in some contexts you mostly care about precision, and in other contexts you really care about recall. For example, if you trained a classifier to detect videos that are safe for kids, you would probably prefer a classifier that rejects many good videos (low recall) but keeps only safe ones (high precision), rather than a classifier that has a much higher recall but lets a few really bad videos show up in your product (in such cases, you may even want to add a human pipeline to check the classifier's video selection). On the other hand, suppose you train a classifier to detect shoplifters on surveillance images: it is probably fine if your classifier has only 30% precision as long as it has 99% recall (sure, the security guards will get a few false alerts, but almost all shoplifters will get caught). Unfortunately, you can't have it both ways: increasing precision reduces recall, and vice versa. This is called the precision/recall tradeoff.
# Precision/Recall Tradeoff

```python
y_scores = cross_val_predict(sgd_clf, X_train, y_train_5, cv=3, method='decision_function')
```

**decision_function** is a method used when increasing the threshold!

It is fairly easy to create a classifier with virtually any precision you want: just set a high enough threshold, and you’re done. Hmm, not so fast. A high-precision classifier is not very useful if its recall is too low!

> Precision/Recall Tradeoff
>
> If someone says “let’s reach 99% precision” you should ask, “at what recall?”

## ROC Curve vs. PR Curve

Since the ROC curve is so similar to the precision/recall (or PR) curve, you may wonder how to decide which one to use. *As a rule of thumb, you should prefer the PR curve whenever the positive class is rare or when you care more about the false positives than the false negatives, and the ROC curve otherwise.* For example, looking at the previous ROC curve (and the ROC AUC score), you may think that the classifier is really good. But this is mostly because there are few positives (5s) compared to the negatives (non-5s). In contrast, the PR curve makes it clear that the classifier has room for improvement (the curve could be closer to the top right corner).
# Linear Regression
## Gradient Descent
> When using Gradient Descent, you should ensure that all features have a similar scale (e.g., using Scikit-Learn’s StandardScaler class), or else it will take much longer to converge.

## Batch Gradient Descent vs. Stochastic Gradient Descent

The main problem with Batch Gradient Descent is the fact that it uses the whole training set to compute the gradients at every step, which makes it very slow when the training set is large. At the opposite extreme, Stochastic Gradient Descent just picks a random instance in the training set at every step and computes the gradients based only on that single instance.

## The Bias/Variance Tradeoff

An important theoretical result of statistics and Machine Learning is the fact that a model's generalization error can be expressed as the sum of three very different errors:

**Bias:** This part of the generalization error is due to wrong assumptions, such as assuming that the data is linear when it is actually quadratic. A high-bias model is most likely to underfit the training data.

**Variance:** This part is due to the model's excessive sensitivity to small variations in the training data. A model with many degrees of freedom (such as a high-degree polynomial model) is likely to have high variance, and thus to overfit the training data. This notion of bias is not to be confused with the bias term of linear models.

**Irreducible error:** This part is due to the noisiness of the data itself. The only way to reduce this part of the error is to clean up the data (e.g., fix the data sources, such as broken sensors, or detect and remove outliers). Increasing a model's complexity will typically increase its variance and reduce its bias. Conversely, reducing a model's complexity increases its bias and reduces its variance. This is why it is called a tradeoff.

> Increasing a model’s complexity will typically increase its variance and reduce its bias. Conversely, reducing a model’s complexity increases its bias and reduces its variance. This is why it is called a tradeoff.
