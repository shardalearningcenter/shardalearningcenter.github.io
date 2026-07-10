---
layout: page
title: "Tutorial 07: Missing Value Imputation"
permalink: /ml-roadmap/07-missing-value-imputation/
---

> **Level:** Beginner · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** Health Survey Data Cleaning

## Scenario

Patient survey responses have missing BMI and blood pressure readings. You must impute sensibly without leaking test-set statistics.

## Learning Objectives

- Detect missing values with pandas
- Use `SimpleImputer` for mean/median/mode strategies
- Use `KNNImputer` for multivariate imputation
- Impute inside a Pipeline

## Prerequisites

- Tutorial 06
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

Modified diabetes dataset with injected missing values

## Hands-On Solution

Copy and run the complete script below:

```python
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error

X, y = load_diabetes(return_X_y=True)
rng = np.random.RandomState(42)
mask = rng.random(X.shape) < 0.1
X_missing = X.copy()
X_missing[mask] = np.nan

X_train, X_test, y_train, y_test = train_test_split(
    X_missing, y, test_size=0.2, random_state=42
)

for strategy in ["mean", "median"]:
    pipe = Pipeline([
        ("imputer", SimpleImputer(strategy=strategy)),
        ("model", LinearRegression()),
    ])
    pipe.fit(X_train, y_train)
    mae = mean_absolute_error(y_test, pipe.predict(X_test))
    print(f"SimpleImputer({strategy:6s}) MAE: {mae:.2f}")

pipe_knn = Pipeline([
    ("imputer", KNNImputer(n_neighbors=5)),
    ("model", LinearRegression()),
])
pipe_knn.fit(X_train, y_train)
mae_knn = mean_absolute_error(y_test, pipe_knn.predict(X_test))
print(f"KNNImputer         MAE: {mae_knn:.2f}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Count missing values per column before imputation.
2. Try `SimpleImputer(strategy='constant', fill_value=0)`.
3. Why must imputation happen inside CV folds, not before splitting?

## Key Takeaways

- Never impute using statistics from the full dataset before splitting
- Mean imputation is simple; KNN imputation uses feature relationships
- Imputers are transformers — they belong in Pipelines

## Navigation

← [Tutorial 06: Encoding Categorical Variables](06_categorical_encoding.md) | [Tutorial 08: Building scikit-learn Pipelines](08_sklearn_pipelines.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
