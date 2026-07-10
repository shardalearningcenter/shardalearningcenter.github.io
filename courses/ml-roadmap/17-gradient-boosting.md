---
layout: course
course_track: "AI / ML"
title: "Tutorial 17: Gradient Boosting"
permalink: /courses/ml-roadmap/17-gradient-boosting/
---

> **Level:** Advanced · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** Telecom Customer Churn

## Scenario

A telecom company wants to identify customers likely to cancel service. Gradient boosting sequentially corrects errors for high accuracy.

## Learning Objectives

- Train `GradientBoostingClassifier`
- Understand learning rate and n_estimators
- Plot staged predictions and feature importance
- Compare with RandomForest

## Prerequisites

- Tutorial 16
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

Synthetic churn dataset

## Hands-On Solution

Copy and run the complete script below:

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import classification_report

np.random.seed(42)
n = 1000
df = pd.DataFrame({
    "tenure_months": np.random.randint(1, 72, n),
    "monthly_charges": np.random.uniform(20, 120, n),
    "total_charges": np.random.uniform(100, 8000, n),
    "support_calls": np.random.poisson(2, n),
    "contract_type": np.random.choice([0, 1, 2], n),  # 0=monthly, 1=1yr, 2=2yr
})
df["churned"] = (
    (df["tenure_months"] < 12).astype(int) * 0.4
    + (df["monthly_charges"] > 80).astype(int) * 0.3
    + (df["contract_type"] == 0).astype(int) * 0.3
    + np.random.randn(n) * 0.1 > 0.3
).astype(int)

X = df.drop("churned", axis=1)
y = df["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
gbc.fit(X_train, y_train)
print("Gradient Boosting:")
print(classification_report(y_test, gbc.predict(X_test)))

for name, imp in sorted(zip(X.columns, gbc.feature_importances_), key=lambda x: -x[1]):
    print(f"  {name}: {imp:.4f}")

rf = RandomForestClassifier(n_estimators=100, random_state=42)
for name, model in [("GBC", gbc), ("RF", rf)]:
    scores = cross_val_score(model, X, y, cv=5, scoring="f1")
    print(f"{name} CV F1: {scores.mean():.3f}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Try `learning_rate=0.01` with `n_estimators=500`. Compare with default.
2. Use `staged_predict` to plot accuracy vs number of trees.
3. Add interaction feature `tenure_months * monthly_charges`.

## Key Takeaways

- Boosting builds trees sequentially to correct residuals
- Lower learning rate + more trees often generalizes better
- GBC often wins on tabular data but trains slower than RF

## Navigation

← [Tutorial 16: Random Forest Ensemble](16_random_forest.md) | [Tutorial 18: Support Vector Machines](18_svm_classification.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
