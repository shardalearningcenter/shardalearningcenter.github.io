---
layout: page
title: "Tutorial 05: Feature Scaling"
permalink: /ml-roadmap/05-feature-scaling/
---

> **Level:** Beginner · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** Credit Approval Risk Scoring

## Scenario

A bank's credit model uses features on vastly different scales (income in thousands, age in years, account balance in millions). Distance-based and gradient-based models need scaling.

## Learning Objectives

- Apply `StandardScaler` and `MinMaxScaler`
- See impact on KNN and LogisticRegression
- Understand fit on train, transform on test
- Avoid data leakage when scaling

## Prerequisites

- Tutorial 04
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_breast_cancer()` — features with different magnitudes

## Hands-On Solution

Copy and run the complete script below:

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

knn = KNeighborsClassifier(n_neighbors=5)

# Without scaling
knn.fit(X_train, y_train)
acc_raw = accuracy_score(y_test, knn.predict(X_test))

# With StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
knn.fit(X_train_scaled, y_train)
acc_scaled = accuracy_score(y_test, knn.predict(X_test_scaled))

print(f"KNN without scaling: {acc_raw:.2%}")
print(f"KNN with StandardScaler: {acc_scaled:.2%}")

# Show scale difference
print(f"\nFeature 0 range (raw): [{X_train[:, 0].min():.1f}, {X_train[:, 0].max():.1f}]")
print(f"Feature 0 range (scaled): [{X_train_scaled[:, 0].min():.2f}, {X_train_scaled[:, 0].max():.2f}]")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Repeat with `MinMaxScaler`. Compare results.
2. Does LogisticRegression benefit from scaling? Test and explain.
3. What happens if you `fit_transform` on the full dataset before splitting?

## Key Takeaways

- Scale features when using KNN, SVM, neural nets, or regularized linear models
- Fit scaler on training data only, then transform test data
- Tree-based models are generally scale-invariant

## Navigation

← [Tutorial 04: Cross-Validation for Reliable Evaluation](04_cross_validation.md) | [Tutorial 06: Encoding Categorical Variables](06_categorical_encoding.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
