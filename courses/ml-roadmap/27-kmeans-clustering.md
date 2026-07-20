---
layout: course
course_track: "AI / ML"
title: "Tutorial 27: K-Means Clustering"
permalink: /courses/ml-roadmap/27-kmeans-clustering/
---

> **Level:** Intermediate · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** Retail Customer Segments

## Scenario

A retailer wants to group customers by purchase behavior for targeted marketing — without labeled segments.

## Learning Objectives

- Apply `KMeans` clustering
- Choose k with elbow method and silhouette score
- Interpret cluster centroids
- Scale features before clustering

## Prerequisites

- Tutorial 05
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

Synthetic customer purchase data

## Hands-On Solution

Copy and run the complete script below:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

np.random.seed(42)
n = 300
cluster1 = np.random.randn(n // 3, 2) * 0.5 + [2, 8]
cluster2 = np.random.randn(n // 3, 2) * 0.5 + [8, 8]
cluster3 = np.random.randn(n - 2 * (n // 3), 2) * 0.5 + [5, 2]
X = np.vstack([cluster1, cluster2, cluster3])

X_scaled = StandardScaler().fit_transform(X)

inertias, silhouettes = [], []
K_range = range(2, 8)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(X_scaled, labels))

print("Silhouette scores:", dict(zip(K_range, [f"{s:.3f}" for s in silhouettes])))

km = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = km.fit_predict(X_scaled)

plt.figure(figsize=(7, 5))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap="viridis", alpha=0.7)
plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
            marker="X", s=200, c="red", label="Centroids")
plt.legend()
plt.savefig("kmeans_segments.png", dpi=120)
print("Saved kmeans_segments.png")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Plot the elbow curve (k vs inertia).
2. Try `n_init=1` vs `n_init=10`. Why does sklearn warn?
3. Apply KMeans to `load_iris()` without labels. Compare clusters to true species.

## Key Takeaways

- K-Means partitions data into k spherical clusters
- Always scale features — clustering is distance-based
- Silhouette score helps choose k when ground truth is unknown

## Navigation

← [Tutorial 26: PCA for Dimensionality Reduction](26_pca_dimensionality_reduction.md) | [Tutorial 28: Hierarchical Clustering](28_hierarchical_clustering.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
