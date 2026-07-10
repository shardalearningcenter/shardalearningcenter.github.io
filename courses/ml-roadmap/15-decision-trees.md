---
layout: course
course_track: "AI / ML"
title: "Tutorial 15: Decision Trees"
permalink: /courses/ml-roadmap/15-decision-trees/
---

> **Level:** Intermediate · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** Loan Default Risk Assessment

## Scenario

Regulators require explainable credit decisions. Decision trees provide human-readable if-then rules.

## Learning Objectives

- Train `DecisionTreeClassifier`
- Control overfitting with `max_depth` and `min_samples_leaf`
- Visualize the tree structure
- Extract feature importances

## Prerequisites

- Tutorial 04
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_breast_cancer()` as stand-in for credit risk binary classification

## Hands-On Solution

Copy and run the complete script below:

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score

X, y = load_breast_cancer(return_X_y=True)
feature_names = load_breast_cancer().feature_names

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

for depth in [3, None]:
    tree = DecisionTreeClassifier(max_depth=depth, random_state=42)
    tree.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, tree.predict(X_train))
    test_acc = accuracy_score(y_test, tree.predict(X_test))
    label = depth if depth else "unlimited"
    print(f"max_depth={label:10s}  train={train_acc:.3f}  test={test_acc:.3f}")

# Interpretable tree
tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)
print("\nTree rules (depth=3):")
print(export_text(tree, feature_names=list(feature_names)))

importances = sorted(zip(feature_names, tree.feature_importances_), key=lambda x: -x[1])
print("\nTop 5 features:")
for name, imp in importances[:5]:
    print(f"  {name}: {imp:.4f}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Plot the tree with `sklearn.tree.plot_tree`. Save as PNG.
2. Try `min_samples_leaf=20`. Compare test accuracy.
3. Why does unlimited depth achieve 100% training accuracy?

## Key Takeaways

- Trees are interpretable but prone to overfitting
- Pruning via max_depth/min_samples_leaf is essential
- Feature importances show which splits matter most

## Navigation

← [Tutorial 14: K-Nearest Neighbors Classification](14_knn_classification.md) | [Tutorial 16: Random Forest Ensemble](16_random_forest.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
