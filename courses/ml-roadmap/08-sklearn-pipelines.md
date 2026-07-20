---
layout: course
course_track: "AI / ML"
title: "Tutorial 08: scikit-learn Pipelines"
permalink: /courses/ml-roadmap/08-sklearn-pipelines/
---

> **Level:** Intermediate · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** Housing Price Prediction Workflow

## Scenario

A real estate analytics team needs a reproducible workflow that chains scaling, imputation, and regression — preventing data leakage and simplifying deployment.

## Learning Objectives

- Build a `Pipeline` with multiple steps
- Access intermediate steps with `named_steps`
- Use `make_pipeline` shorthand
- Serialize with `joblib`

## Prerequisites

- Tutorials 05–07
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`fetch_california_housing()` subset

## Hands-On Solution

Copy and run the complete script below:

```python
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
import joblib

X, y = fetch_california_housing(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", Ridge(alpha=1.0)),
])

pipe.fit(X_train, y_train)
rmse = mean_squared_error(y_test, pipe.predict(X_test), squared=False)
print(f"RMSE: ${rmse * 100_000:,.0f}")  # prices in $100k units

# Save entire pipeline
joblib.dump(pipe, "housing_pipeline.joblib")
loaded = joblib.load("housing_pipeline.joblib")
print(f"Loaded pipeline score: {loaded.score(X_test, y_test):.4f}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Add a second model step using `GridSearchCV` on `alpha` (preview for tutorial 23).
2. Inspect `pipe.named_steps['model'].coef_` after fitting.
3. Replace Ridge with `ElasticNet`. How does RMSE change?

## Key Takeaways

- Pipelines bundle preprocessing + model into one estimators
- One `fit()` call handles everything in order
- Serialize the whole pipeline for production deployment

## Navigation

← [Tutorial 07: Handling Missing Values](07_missing_value_imputation.md) | [Tutorial 09: ColumnTransformer for Mixed Data](09_column_transformer.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
