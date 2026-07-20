---
layout: course
course_track: "AI / ML"
title: "Tutorial 10: Polynomial Features"
permalink: /courses/ml-roadmap/10-polynomial-features/
---

> **Level:** Intermediate · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** Vehicle Fuel Efficiency Modeling

## Scenario

MPG vs engine displacement shows a curved relationship. Linear regression on raw features underfits; polynomial features can capture the curve.

## Learning Objectives

- Generate polynomial features with `PolynomialFeatures`
- Understand feature explosion with high degree
- Combine with Pipeline and Ridge regularization
- Visualize fit improvement

## Prerequisites

- Tutorial 08
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

Synthetic non-linear regression data

## Hands-On Solution

Copy and run the complete script below:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

np.random.seed(42)
X = np.sort(5 * np.random.rand(80, 1), axis=0)
y = np.sin(X).ravel() + np.random.randn(80) * 0.3

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

for degree in [1, 3, 15]:
    pipe = Pipeline([
        ("poly", PolynomialFeatures(degree=degree)),
        ("scaler", StandardScaler()),
        ("model", Ridge(alpha=0.1 if degree > 5 else 1.0)),
    ])
    pipe.fit(X_train, y_train)
    r2 = r2_score(y_test, pipe.predict(X_test))
    print(f"Degree {degree:2d}  R² = {r2:.4f}  features = {pipe.named_steps['poly'].n_output_features_}")

# Plot degree-3 fit
pipe3 = Pipeline([
    ("poly", PolynomialFeatures(degree=3)),
    ("scaler", StandardScaler()),
    ("model", Ridge(alpha=1.0)),
])
pipe3.fit(X_train, y_train)
X_plot = np.linspace(0, 5, 100).reshape(-1, 1)
plt.scatter(X_test, y_test, alpha=0.6, label="Test")
plt.plot(X_plot, pipe3.predict(X_plot), "r-", label="Degree-3 fit")
plt.legend()
plt.savefig("polynomial_fit.png", dpi=120)
print("Saved polynomial_fit.png")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Plot train vs test R² for degrees 1–15. Where does overfitting start?
2. Increase Ridge `alpha` for degree 15. Can you recover generalization?
3. Use `interaction_only=True` in PolynomialFeatures. What changes?

## Key Takeaways

- PolynomialFeatures create non-linear terms from linear inputs
- High degree + no regularization → overfitting
- Always pair high-degree polynomials with regularization

## Navigation

← [Tutorial 09: ColumnTransformer for Mixed Data](09_column_transformer.md) | [Tutorial 11: Linear Regression for Housing Prices](11_linear_regression_housing.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
