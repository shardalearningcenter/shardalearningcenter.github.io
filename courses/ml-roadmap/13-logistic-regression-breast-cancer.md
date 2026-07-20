---
layout: course
course_track: "AI / ML"
title: "Tutorial 13: Logistic Regression — Breast Cancer"
permalink: /courses/ml-roadmap/13-logistic-regression-breast-cancer/
---

> **Level:** Intermediate · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** Tumor Malignancy Diagnosis

## Scenario

Pathologists need a second opinion system that classifies tumors as malignant or benign from cell measurements.

## Learning Objectives

- Train `LogisticRegression` for binary classification
- Interpret coefficients as log-odds
- Use `predict_proba` for risk scores
- Set classification threshold

## Prerequisites

- Tutorial 05
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_breast_cancer()` — 30 features, binary target

## Hands-On Solution

Copy and run the complete script below:

```python
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_s, y_train)

y_prob = clf.predict_proba(X_test_s)[:, 1]
y_pred = clf.predict(X_test_s)

print(classification_report(y_test, y_pred, target_names=data.target_names))
print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")

# Custom threshold: flag if malignant probability > 0.3
y_pred_sensitive = (y_prob > 0.3).astype(int)
print("\nLower threshold (0.3) — higher recall for malignant:")
print(classification_report(y_test, y_pred_sensitive, target_names=data.target_names))
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Find the top 5 features by absolute coefficient magnitude.
2. Try `class_weight='balanced'`. How do precision/recall shift?
3. Plot predicted probability distribution for malignant vs benign.

## Key Takeaways

- Logistic regression outputs calibrated probabilities
- Threshold tuning trades precision vs recall
- Scaling is important for stable coefficient interpretation

## Navigation

← [Tutorial 12: Ridge and Lasso Regularization](12_ridge_lasso_regression.md) | [Tutorial 14: K-Nearest Neighbors Classification](14_knn_classification.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
