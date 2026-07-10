---
layout: course
course_track: "AI / ML"
title: "Tutorial 02: Wine Quality EDA"
permalink: /courses/ml-roadmap/02-wine-quality-eda/
---

> **Level:** Beginner · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** Winery Quality Assessment

## Scenario

A winery wants to understand which chemical properties (alcohol, acidity, sulphates) correlate with wine quality before building a predictive model.

## Learning Objectives

- Load and inspect the Wine dataset
- Compute summary statistics with NumPy/pandas
- Visualize feature distributions
- Identify class imbalance across cultivars

## Prerequisites

- Tutorial 01
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_wine()` — 178 samples, 13 chemical features, 3 cultivar classes

## Hands-On Solution

Copy and run the complete script below:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine

wine = load_wine()
X, y = wine.data, wine.target

print("Feature names:", wine.feature_names)
print("Target names:", wine.target_names)
print(f"Samples per class: {np.bincount(y)}")

# Summary statistics
for i, name in enumerate(wine.feature_names):
    col = X[:, i]
    print(f"{name:20s} mean={col.mean():.2f}  std={col.std():.2f}")

# Visualize alcohol vs flavanoids colored by cultivar
plt.figure(figsize=(8, 5))
for cls in range(3):
  mask = y == cls
  plt.scatter(X[mask, 0], X[mask, 6], label=wine.target_names[cls], alpha=0.7)
plt.xlabel("Alcohol")
plt.ylabel("Flavanoids")
plt.legend()
plt.title("Wine Cultivars: Alcohol vs Flavanoids")
plt.tight_layout()
plt.savefig("wine_eda.png", dpi=120)
print("Saved wine_eda.png")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Create a histogram of the `proline` feature for each cultivar.
2. Which two features have the highest correlation? Use `np.corrcoef`.
3. Count how many samples belong to each class and discuss imbalance.

## Key Takeaways

- EDA before modeling prevents surprises later
- Feature scales differ widely — scaling will matter for distance-based models
- Visualization reveals separability between classes

## Navigation

← [Tutorial 01: Iris Flower Classification](01_iris_flower_classification.md) | [Tutorial 03: Train-Test Split and Baseline Models](03_train_test_baseline.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
