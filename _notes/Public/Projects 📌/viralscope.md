---
title: viralscope
---
# viralscope
###### Term project for CS513 - Knowledge Discovery and Data Mining (Fall 2025)

**GitHub Link:** [engindenizdogu/viralscope: Viral video predictor for Youtube videos](https://github.com/engindenizdogu/viralscope)

**viralscope** is a machine learning project that predicts YouTube video success using metadata and channel characteristics. The project processes 85+ million video records from the YouNiverse dataset to identify patterns that distinguish successful videos from others.

**Key Features:**
- End-to-end ML pipeline from raw data to trained models
- Random and data preparation sampling with engagement filtering
- Feature engineering with train/test split and scaling
- Multiple classification models with hyperparameter tuning
- Designed to prevent data leakage - labels created only after train/test split

**Models with GridSearchCV:**
1. **Random Forest Classifier**
2. **Decision Tree Classifier**
3. **Linear SVC**
4. **K-Nearest Neighbors**
5. **Multi-Layer Perceptron**

