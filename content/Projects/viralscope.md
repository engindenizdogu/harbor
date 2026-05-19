---
title: viralscope
tags: [projects, portfolio, machine-learning]
draft: false
---
> A machine learning project that predicts YouTube video success using metadata and channel characteristics.

## Quick Facts
- **Context:** Term project for CS513 - Knowledge Discovery and Data Mining (Fall 2025)
- **Tech Stack:** Python, scikit-learn, Random Forest, SVM, MLP
- **Links:** [GitHub Repo](https://github.com/engindenizdogu/viralscope)

## Overview and Problem
The project processes over 85 million video records from the YouNiverse dataset to identify patterns that distinguish successful videos from others. The goal is to build a robust classification pipeline to predict video engagement accurately without data leakage.

## What I Built
- **Engineered** an end-to-end ML pipeline from raw data ingestion to trained models.
- **Implemented** random and data preparation sampling with engagement filtering.
- **Designed** a feature engineering process with a strict train/test split and scaling to prevent data leakage (labels created post-split).
- **Trained** multiple classification models including Random Forest, Decision Tree, Linear SVC, K-Nearest Neighbors, and Multi-Layer Perceptron.

## Key Results and Impact
- Optimized hyperparameters for 5 distinct models using GridSearchCV to maximize predictive performance.
- Processed a massive dataset of 85+ million records successfully.

---
*Related:* [[Projects MOC]]
