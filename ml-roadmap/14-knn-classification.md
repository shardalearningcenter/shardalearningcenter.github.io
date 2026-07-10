---
layout: page
title: "Tutorial 14: KNN Classification"
permalink: /ml-roadmap/14-knn-classification/
---

> **Level:** Intermediate · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** Handwritten Digit Recognition

## Scenario

A postal service wants to read zip codes from envelopes. KNN classifies digits by finding similar training examples.

## Learning Objectives

- Train KNN on high-dimensional image data
- Tune `n_neighbors` and distance metrics
- Understand curse of dimensionality
- Measure latency vs accuracy tradeoff

## Prerequisites

- Tutorial 05
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_digits()` — 8×8 grayscale digit images

## Hands-On Solution

Copy and run the complete script below:

```python
import time
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix

digits = load_digits()
X, y = digits.data, digits.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

for k in [1, 3, 5, 11]:
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsClassifier(n_neighbors=k)),
    ])
    start = time.time()
    pipe.fit(X_train, y_train)
    acc = accuracy_score(y_test, pipe.predict(X_test))
    elapsed = time.time() - start
    print(f"k={k:2d}  accuracy={acc:.4f}  fit+predict={elapsed:.3f}s")

# Best model confusion matrix
best = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=3)),
])
best.fit(X_train, y_train)
print("\nConfusion matrix (k=3):")
print(confusion_matrix(y_test, best.predict(X_test)))
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Try `metric='manhattan'` vs default Euclidean.
2. Which digit pair is most often confused? Inspect confusion matrix.
3. Reduce to 2D with PCA (preview tutorial 26) and visualize decision boundaries.

## Key Takeaways

- KNN is non-parametric — no explicit training phase
- Prediction is slow on large datasets (searches all neighbors)
- Scaling is critical when features have different ranges

## Navigation

← [Tutorial 13: Logistic Regression for Binary Classification](13_logistic_regression_breast_cancer.md) | [Tutorial 15: Decision Trees for Interpretable Rules](15_decision_trees.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
