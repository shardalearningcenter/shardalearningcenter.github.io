---
layout: course
course_track: "AI / ML"
title: "Tutorial 26: PCA Dimensionality Reduction"
permalink: /courses/ml-roadmap/26-pca-dimensionality-reduction/
---

> **Level:** Intermediate · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** Visualizing Handwritten Digits

## Scenario

64-pixel digit images are hard to visualize. PCA projects them to 2D while preserving maximum variance for exploratory analysis.

## Learning Objectives

- Apply `PCA` for dimensionality reduction
- Interpret `explained_variance_ratio_`
- Visualize 2D projections colored by class
- Use PCA as preprocessing before classification

## Prerequisites

- Tutorial 05
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_digits()`

## Hands-On Solution

Copy and run the complete script below:

```python
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier

digits = load_digits()
X, y = digits.data, digits.target

# 2D visualization
pca2 = PCA(n_components=2)
X_2d = pca2.fit_transform(StandardScaler().fit_transform(X))

plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_2d[:, 0], X_2d[:, 1], c=y, cmap="tab10", alpha=0.6, s=15)
plt.colorbar(scatter, label="Digit")
plt.xlabel(f"PC1 ({pca2.explained_variance_ratio_[0]:.1%})")
plt.ylabel(f"PC2 ({pca2.explained_variance_ratio_[1]:.1%})")
plt.title("Digits in 2D PCA Space")
plt.savefig("digits_pca.png", dpi=120)

# Classification with reduced dimensions
for n in [2, 10, 30, 64]:
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("pca", PCA(n_components=n)),
        ("knn", KNeighborsClassifier(n_neighbors=5)),
    ])
    scores = cross_val_score(pipe, X, y, cv=5)
    print(f"n_components={n:2d}  CV accuracy={scores.mean():.3f}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. How many components explain 95% of variance? Use `np.cumsum`.
2. Reconstruct a digit from 10 PCA components. Plot original vs reconstructed.
3. Compare PCA preprocessing vs raw features for KNN.

## Key Takeaways

- PCA finds orthogonal directions of maximum variance
- Useful for visualization, noise reduction, and speeding up training
- Always scale before PCA

## Navigation

← [Tutorial 25: Feature Selection Techniques](25_feature_selection.md) | [Tutorial 27: K-Means Customer Segmentation](27_kmeans_clustering.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
