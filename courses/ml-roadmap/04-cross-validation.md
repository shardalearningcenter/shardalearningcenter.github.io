---
layout: course
course_track: "AI / ML"
title: "Tutorial 04: Cross Validation"
permalink: /courses/ml-roadmap/04-cross-validation/
---

> **Level:** Beginner · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** Breast Cancer Screening Reliability

## Scenario

A hospital needs confidence intervals on model performance, not just a single train/test score that might be lucky or unlucky.

## Learning Objectives

- Use `cross_val_score` for k-fold CV
- Understand stratified folds for classification
- Compare models with consistent evaluation
- Report mean and std of scores

## Prerequisites

- Tutorial 03
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_breast_cancer()` — 569 samples, 30 features, malignant vs benign

## Hands-On Solution

Copy and run the complete script below:

```python
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

data = load_breast_cancer()
X, y = data.data, data.target

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

models = {
    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000)),
    ]),
    "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
}

for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
    print(f"{name:22s}  {scores.mean():.3f} (+/- {scores.std():.3f})")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Run CV with `n_splits=10`. How does std change?
2. Use `scoring='f1'` instead of accuracy. Does ranking change?
3. Add KNeighborsClassifier to the comparison.

## Key Takeaways

- Single splits can mislead — CV gives robust estimates
- StratifiedKFold preserves class ratios in each fold
- Pipelines ensure preprocessing is fit only on training folds

## Navigation

← [Tutorial 03: Train-Test Split and Baseline Models](03_train_test_baseline.md) | [Tutorial 05: Feature Scaling with StandardScaler](05_feature_scaling.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
