---
layout: page
title: "Tutorial 01: Iris Flower Classification"
permalink: /ml-roadmap/01-iris-flower-classification/
---

> **Level:** Beginner · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** Botanical Garden Species ID

## Scenario

A botanical garden receives unknown iris samples and needs an automated system to classify them into Setosa, Versicolor, or Virginica based on sepal and petal measurements.

## Learning Objectives

- Load a dataset with `sklearn.datasets`
- Understand features (X) and target (y)
- Fit your first classifier with `fit()` and `predict()`
- Compute accuracy with `score()`

## Prerequisites

- Python basics, NumPy arrays
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_iris()` — 150 samples, 4 features, 3 classes

## Hands-On Solution

Copy and run the complete script below:

```python
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load data
iris = load_iris()
X, y = iris.data, iris.target
feature_names = iris.feature_names
target_names = iris.target_names

print("Features:", feature_names)
print("Classes:", target_names)
print("Shape:", X.shape)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train KNN classifier
clf = KNeighborsClassifier(n_neighbors=5)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred, target_names=target_names))

# Predict a new sample
new_flower = np.array([[5.1, 3.5, 1.4, 0.2]])
predicted = clf.predict(new_flower)
print(f"New sample predicted as: {target_names[predicted[0]]}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Try `n_neighbors=1` vs `n_neighbors=15`. How does accuracy change?
2. Use only the first two features (sepal length, sepal width). Compare accuracy.
3. Print `clf.predict_proba()` for the test set and inspect class probabilities.

## Key Takeaways

- scikit-learn estimators follow `fit(X, y)` → `predict(X)` API
- Always hold out test data you never train on
- KNN is a simple baseline that works well on small, clean datasets

## Navigation

[Tutorial 02: Wine Quality Exploratory Analysis](02_wine_quality_eda.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
