---
layout: page
title: "Tutorial 25: Feature Selection"
permalink: /ml-roadmap/25-feature-selection/
---

> **Level:** Advanced · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** Gene Microarray Analysis

## Scenario

20,000 genes, 60 patients. Most genes are noise. Feature selection reduces overfitting and improves interpretability.

## Learning Objectives

- Use `SelectKBest` with statistical tests
- Use `RFE` (Recursive Feature Elimination)
- Use model-based selection with Lasso
- Compare model performance with fewer features

## Prerequisites

- Tutorial 12
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

High-dimensional synthetic classification

## Hands-On Solution

Copy and run the complete script below:

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

X, y = make_classification(
    n_samples=200, n_features=100, n_informative=10,
    n_redundant=20, random_state=42
)

full_model = LogisticRegression(max_iter=1000)
full_scores = cross_val_score(full_model, X, y, cv=5)
print(f"All 100 features:  CV accuracy = {full_scores.mean():.3f}")

# SelectKBest
pipe_kbest = Pipeline([
    ("select", SelectKBest(f_classif, k=15)),
    ("clf", LogisticRegression(max_iter=1000)),
])
kbest_scores = cross_val_score(pipe_kbest, X, y, cv=5)
print(f"SelectKBest (k=15): CV accuracy = {kbest_scores.mean():.3f}")

# RFE
pipe_rfe = Pipeline([
    ("rfe", RFE(LogisticRegression(max_iter=1000), n_features_to_select=15)),
    ("clf", LogisticRegression(max_iter=1000)),
])
rfe_scores = cross_val_score(pipe_rfe, X, y, cv=5)
print(f"RFE (15 features):  CV accuracy = {rfe_scores.mean():.3f}")

pipe_kbest.fit(X, y)
mask = pipe_kbest.named_steps["select"].get_support()
print(f"Selected features: {np.where(mask)[0][:10]}...")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Sweep k from 5 to 50 in SelectKBest. Plot CV accuracy vs k.
2. Use `SelectFromModel` with RandomForest feature importances.
3. Why must feature selection happen inside CV, not before?

## Key Takeaways

- Feature selection reduces dimensionality and overfitting risk
- SelectKBest is fast; RFE is slower but considers feature interactions
- Always wrap selection in Pipeline to prevent leakage

## Navigation

← [Tutorial 24: RandomizedSearchCV for Efficient Tuning](24_randomized_search.md) | [Tutorial 26: PCA for Dimensionality Reduction](26_pca_dimensionality_reduction.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
