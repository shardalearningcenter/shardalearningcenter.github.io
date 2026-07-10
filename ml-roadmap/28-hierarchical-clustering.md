---
layout: page
title: "Tutorial 28: Hierarchical Clustering"
permalink: /ml-roadmap/28-hierarchical-clustering/
---

> **Level:** Intermediate · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** Country Development Grouping

## Scenario

The UN wants to group countries by development indicators. Hierarchical clustering builds a dendrogram showing nested group structure.

## Learning Objectives

- Use `AgglomerativeClustering`
- Visualize dendrograms with scipy
- Compare linkage methods (ward, complete, average)
- Cut dendrogram at desired k

## Prerequisites

- Tutorial 27
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_iris()` for demonstration

## Hands-On Solution

Copy and run the complete script below:

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score

iris = load_iris()
X = StandardScaler().fit_transform(iris.data)

# Dendrogram (subsample for readability)
idx = np.random.RandomState(42).choice(len(X), 50, replace=False)
Z = linkage(X[idx], method="ward")

plt.figure(figsize=(10, 5))
dendrogram(Z, truncate_mode="level", p=4)
plt.title("Hierarchical Clustering Dendrogram (Ward)")
plt.savefig("dendrogram.png", dpi=120)

for method in ["ward", "complete", "average"]:
    agg = AgglomerativeClustering(n_clusters=3, linkage=method)
    labels = agg.fit_predict(X)
    ari = adjusted_rand_score(iris.target, labels)
    print(f"linkage={method:10s}  ARI={ari:.3f}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Cut the dendrogram at 4 clusters. How does ARI change?
2. Compare hierarchical vs K-Means on iris (use ARI).
3. When is hierarchical clustering preferred over K-Means?

## Key Takeaways

- Hierarchical clustering needs no preset k (but you still choose a cut)
- Ward linkage minimizes within-cluster variance
- Dendrograms provide rich visual structure but scale poorly to large n

## Navigation

← [Tutorial 27: K-Means Customer Segmentation](27_kmeans_clustering.md) | [Tutorial 29: Voting and Stacking Ensembles](29_ensemble_voting_stacking.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
