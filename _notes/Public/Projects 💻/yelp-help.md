---
title: yelp-help
---
# yelp-help

###### Term project for CS559 - Machine Learning: Fundamentals and Applications (Fall 2025)

**GitHub Link:** [engindenizdogu/yelp-help](https://github.com/engindenizdogu/yelp-help)

**TLDR:** A machine learning pipeline that predicts restaurant success by analyzing Yelp business data, customer reviews, and operational features using multiple classification models to identify what makes restaurants thrive.

**Project Summary:** This project develops a machine learning pipeline to predict restaurant success using the Yelp Academic Dataset, leveraging real-world business data to identify the key factors that separate thriving establishments from struggling ones. The end-to-end pipeline processes millions of reviews, tips, and business records from Yelp's JSON data, engineering features from nested attributes like parking availability, ambience, operating hours, and customer engagement metrics to create a comprehensive feature set. Through systematic data cleaning, feature engineering, and exploratory analysis, the project defines restaurant "success" as achieving both high ratings (≥4 stars) and above-median review counts, then trains and compares seven different machine learning models—including Logistic Regression, Random Forest, SVM, and Neural Networks—using grid search cross-validation to optimize performance. The modular architecture, controlled through a configurable pipeline script, allows each stage (metadata analysis, preprocessing, cleaning, visualization, and model training) to be executed independently or sequentially, making it both a practical tool for predicting restaurant outcomes and an educational framework for understanding how data science techniques can extract actionable insights from complex, real-world datasets.
