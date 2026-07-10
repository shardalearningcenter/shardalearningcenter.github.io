---
layout: page
title: "Tutorial 23: Grid Search CV"
permalink: /ml-roadmap/23-grid-search-cv/
---

> **Level:** Advanced · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** Optimizing SVM for Image Classification

## Scenario

Default hyperparameters rarely optimal. GridSearchCV exhaustively searches parameter combinations with cross-validation.

## Learning Objectives

- Define a parameter grid
- Run `GridSearchCV` with Pipeline
- Inspect `best_params_` and `cv_results_`
- Evaluate best model on held-out test set

## Prerequisites

- Tutorial 18
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_digits()`

## Hands-On Solution

Copy and run the complete script below:

```python
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline

X, y = load_digits(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC()),
])

param_grid = {
    "svm__C": [0.1, 1, 10],
    "svm__gamma": ["scale", 0.01, 0.001],
    "svm__kernel": ["rbf", "linear"],
}

search = GridSearchCV(pipe, param_grid, cv=3, scoring="accuracy", n_jobs=-1, verbose=1)
search.fit(X_train, y_train)

print(f"Best params: {search.best_params_}")
print(f"Best CV score: {search.best_score_:.4f}")
print(f"Test score: {search.score(X_test, y_test):.4f}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Expand the grid. How does search time grow?
2. Plot `C` vs mean CV score for RBF kernel using `cv_results_`.
3. Use `refit=True` (default) and confirm best estimator is refit on full train set.

## Key Takeaways

- GridSearchCV automates CV + refit on best params
- Prefix pipeline params with step name (e.g., `svm__C`)
- Grid size grows exponentially — use RandomizedSearchCV for large spaces

## Navigation

← [Tutorial 22: Learning Curves and Bias-Variance Diagnosis](22_learning_curves.md) | [Tutorial 24: RandomizedSearchCV for Efficient Tuning](24_randomized_search.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
