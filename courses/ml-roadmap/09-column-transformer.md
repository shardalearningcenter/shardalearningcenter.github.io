---
layout: course
course_track: "AI / ML"
title: "Tutorial 09: Column Transformer"
permalink: /courses/ml-roadmap/09-column-transformer/
---

> **Level:** Intermediate · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** Adult Income Prediction

## Scenario

Census data mixes numeric features (age, hours-per-week) with categorical ones (occupation, marital-status). Each type needs different preprocessing in parallel.

## Learning Objectives

- Build a `ColumnTransformer` with multiple branches
- Apply different transformers per column group
- Feed output into a classifier Pipeline
- Inspect transformed feature names

## Prerequisites

- Tutorials 06–08
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`fetch_openml('adult', version=2)` — income >50K prediction

## Hands-On Solution

Copy and run the complete script below:

```python
import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

adult = fetch_openml("adult", version=2, as_frame=True, parser="auto")
X = adult.data
y = (adult.target == ">50K").astype(int)

num_cols = ["age", "hours-per-week"]
cat_cols = ["workclass", "education", "occupation"]

preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]), num_cols),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ]), cat_cols),
])

pipe = Pipeline([
    ("prep", preprocessor),
    ("clf", LogisticRegression(max_iter=1000)),
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
pipe.fit(X_train, y_train)
print(classification_report(y_test, pipe.predict(X_test), target_names=["<=50K", ">50K"]))
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Add `marital-status` to categorical columns.
2. Use `remainder='drop'` vs `remainder='passthrough'` and compare shapes.
3. Time the pipeline fit. Which step is slowest?

## Key Takeaways

- ColumnTransformer applies different preprocessing to different columns
- Nested Pipelines keep each branch clean and composable
- Essential pattern for real-world tabular data

## Navigation

← [Tutorial 08: Building scikit-learn Pipelines](08_sklearn_pipelines.md) | [Tutorial 10: Polynomial Features for Non-Linear Patterns](10_polynomial_features.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
