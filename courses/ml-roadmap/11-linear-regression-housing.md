---
layout: course
course_track: "AI / ML"
title: "Tutorial 11: Linear Regression — Housing"
permalink: /courses/ml-roadmap/11-linear-regression-housing/
---

> **Level:** Intermediate · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** California Real Estate Valuation

## Scenario

A property tech startup needs to estimate home values from location, age, and neighborhood demographics.

## Learning Objectives

- Train `LinearRegression` on real housing data
- Interpret coefficients as feature importance
- Evaluate with RMSE and MAE
- Visualize predictions vs actuals

## Prerequisites

- Tutorial 08
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`fetch_california_housing()` — 20,640 samples, 8 features

## Hands-On Solution

Copy and run the complete script below:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error

housing = fetch_california_housing()
X, y = housing.data, housing.target
feature_names = housing.feature_names

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LinearRegression()),
])
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)

rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)
print(f"RMSE: ${rmse * 100_000:,.0f}")
print(f"MAE:  ${mae * 100_000:,.0f}")

coefs = pipe.named_steps["model"].coef_
for name, coef in sorted(zip(feature_names, coefs), key=lambda x: -abs(x[1])):
    print(f"  {name:15s} {coef:+.4f}")

plt.scatter(y_test, y_pred, alpha=0.3, s=10)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
plt.xlabel("Actual ($100k)")
plt.ylabel("Predicted ($100k)")
plt.savefig("housing_predictions.png", dpi=120)
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Remove the `MedInc` feature. How much does RMSE increase?
2. Add polynomial features for `AveRooms`. Does it help?
3. Identify the worst-predicted neighborhoods (largest residuals).

## Key Takeaways

- Linear regression is interpretable via coefficients
- Median income is typically the strongest housing price predictor
- Residual plots reveal systematic errors (non-linearity)

## Navigation

← [Tutorial 10: Polynomial Features for Non-Linear Patterns](10_polynomial_features.md) | [Tutorial 12: Ridge and Lasso Regularization](12_ridge_lasso_regression.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
