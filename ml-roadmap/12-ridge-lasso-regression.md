---
layout: page
title: "Tutorial 12: Ridge & Lasso Regression"
permalink: /ml-roadmap/12-ridge-lasso-regression/
---

> **Level:** Intermediate · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** High-Dimensional Gene Expression

## Scenario

With more features than samples (or highly correlated features), ordinary least squares overfits. L1/L2 regularization controls complexity.

## Learning Objectives

- Compare OLS, Ridge (L2), and Lasso (L1)
- Understand `alpha` as regularization strength
- Use Lasso for automatic feature selection
- Plot coefficient paths vs alpha

## Prerequisites

- Tutorial 11
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

Diabetes dataset with polynomial feature expansion

## Hands-On Solution

Copy and run the complete script below:

```python
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

base_steps = [
    ("poly", PolynomialFeatures(degree=2, include_bias=False)),
    ("scaler", StandardScaler()),
]

models = {
    "OLS": LinearRegression(),
    "Ridge": Ridge(alpha=1.0),
    "Lasso": Lasso(alpha=0.1, max_iter=10000),
}

for name, model in models.items():
    pipe = Pipeline(base_steps + [("model", model)])
    pipe.fit(X_train, y_train)
    train_r2 = pipe.score(X_train, y_train)
    test_r2 = pipe.score(X_test, y_test)
    n_nonzero = np.sum(pipe.named_steps["model"].coef_ != 0) if name == "Lasso" else "all"
    print(f"{name:6s}  train R²={train_r2:.4f}  test R²={test_r2:.4f}  features={n_nonzero}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Sweep `alpha` from 0.001 to 100 for Ridge. Plot test R².
2. How many Lasso coefficients are exactly zero at alpha=1.0?
3. When would you choose Lasso over Ridge?

## Key Takeaways

- Ridge shrinks coefficients but keeps all features
- Lasso drives some coefficients to zero (feature selection)
- Regularization trades bias for lower variance

## Navigation

← [Tutorial 11: Linear Regression for Housing Prices](11_linear_regression_housing.md) | [Tutorial 13: Logistic Regression for Binary Classification](13_logistic_regression_breast_cancer.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
