---
layout: course
course_track: "AI / ML"
title: "Tutorial 03: Train/Test Baseline"
permalink: /courses/ml-roadmap/03-train-test-baseline/
---

> **Level:** Beginner · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** Diabetes Progression Prediction

## Scenario

A clinic wants to predict diabetes disease progression one year after baseline measurements. You must establish a simple baseline before trying complex models.

## Learning Objectives

- Split data with `train_test_split`
- Build a DummyRegressor baseline
- Compare baseline vs LinearRegression
- Use R² and MAE metrics

## Prerequisites

- Tutorials 01–02
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_diabetes()` — 442 patients, 10 features, continuous target

## Hands-On Solution

Copy and run the complete script below:

```python
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

diabetes = load_diabetes()
X, y = diabetes.data, diabetes.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Baseline: always predict the mean
baseline = DummyRegressor(strategy="mean")
baseline.fit(X_train, y_train)
y_pred_base = baseline.predict(X_test)

# Linear model
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("=== Baseline (mean) ===")
print(f"MAE:  {mean_absolute_error(y_test, y_pred_base):.2f}")
print(f"R²:   {r2_score(y_test, y_pred_base):.4f}")

print("\n=== Linear Regression ===")
print(f"MAE:  {mean_absolute_error(y_test, y_pred):.2f}")
print(f"R²:   {r2_score(y_test, y_pred):.4f}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Try `DummyRegressor(strategy='median')` as another baseline.
2. Change `test_size` to 0.1 and 0.4. How do metrics fluctuate?
3. Print the learned coefficients and identify the most influential feature.

## Key Takeaways

- Always beat a dumb baseline before celebrating your model
- R² near 0 means the model explains little variance
- Train/test split gives an unbiased estimate of generalization

## Navigation

← [Tutorial 02: Wine Quality Exploratory Analysis](02_wine_quality_eda.md) | [Tutorial 04: Cross-Validation for Reliable Evaluation](04_cross_validation.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
