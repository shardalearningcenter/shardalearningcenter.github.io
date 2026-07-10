---
layout: page
title: "Tutorial 20: Classification Metrics"
permalink: /ml-roadmap/20-classification-metrics/
---

> **Level:** Intermediate · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** Credit Card Fraud Detection

## Scenario

Fraud is rare (0.1% of transactions). Accuracy is misleading — you need precision, recall, and F1 tuned to business costs.

## Learning Objectives

- Compute precision, recall, F1, support
- Use `classification_report` and `confusion_matrix`
- Understand why accuracy fails on imbalanced data
- Choose metrics aligned with business goals

## Prerequisites

- Tutorial 13
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

Imbalanced synthetic fraud dataset

## Hands-On Solution

Copy and run the complete script below:

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix,
)

X, y = make_classification(
    n_samples=5000, n_features=20, weights=[0.99, 0.01],
    random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
print(f"F1:        {f1_score(y_test, y_pred):.4f}")
print(f"\n{classification_report(y_test, y_pred, target_names=['legit', 'fraud'])}")
print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred))

# Dummy classifier that always predicts legit
y_dummy = np.zeros_like(y_test)
print(f"\nDummy accuracy: {accuracy_score(y_test, y_dummy):.4f}  (misleading!)")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Use `class_weight='balanced'` in LogisticRegression. How do metrics change?
2. Calculate the business cost: FP costs $5, FN costs $500. Find optimal threshold.
3. When would you optimize for precision vs recall in fraud detection?

## Key Takeaways

- Accuracy is wrong metric for imbalanced classification
- Precision = of predicted positives, how many are correct
- Recall = of actual positives, how many did we catch

## Navigation

← [Tutorial 19: Naive Bayes for Text Classification](19_naive_bayes_text.md) | [Tutorial 21: ROC Curves and AUC](21_roc_auc_curves.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
