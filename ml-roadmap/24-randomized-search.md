---
layout: page
title: "Tutorial 24: Randomized Search"
permalink: /ml-roadmap/24-randomized-search/
---

> **Level:** Advanced · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** Tuning Random Forest at Scale

## Scenario

Random forests have many hyperparameters. Exhaustive grid search is too slow — sample random combinations instead.

## Learning Objectives

- Use `RandomizedSearchCV` with distributions
- Compare wall-clock time vs GridSearchCV
- Use `scipy.stats` for continuous distributions
- Analyze `cv_results_` DataFrame

## Prerequisites

- Tutorial 23
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_wine()`

## Hands-On Solution

Copy and run the complete script below:

```python
import time
import pandas as pd
from scipy.stats import randint, uniform
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier

X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

param_dist = {
    "n_estimators": randint(50, 500),
    "max_depth": randint(2, 20),
    "min_samples_split": randint(2, 20),
    "max_features": uniform(0.1, 0.9),
}

start = time.time()
search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_dist, n_iter=30, cv=5, scoring="accuracy",
    random_state=42, n_jobs=-1,
)
search.fit(X_train, y_train)
elapsed = time.time() - start

print(f"Search time: {elapsed:.1f}s")
print(f"Best params: {search.best_params_}")
print(f"Test accuracy: {search.score(X_test, y_test):.4f}")

results = pd.DataFrame(search.cv_results_)
print(results[["param_n_estimators", "param_max_depth", "mean_test_score"]].head())
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Increase `n_iter` to 100. Does test accuracy improve?
2. Plot `n_estimators` vs `mean_test_score` as scatter plot.
3. When is RandomizedSearchCV preferred over GridSearchCV?

## Key Takeaways

- Random search often finds good params faster than exhaustive grid
- Use distributions for continuous params, lists for discrete
- Always set `random_state` for reproducibility

## Navigation

← [Tutorial 23: Hyperparameter Tuning with GridSearchCV](23_grid_search_cv.md) | [Tutorial 25: Feature Selection Techniques](25_feature_selection.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
