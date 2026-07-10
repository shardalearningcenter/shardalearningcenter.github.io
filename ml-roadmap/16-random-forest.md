---
layout: page
title: "Tutorial 16: Random Forest"
permalink: /ml-roadmap/16-random-forest/
---

> **Level:** Intermediate · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** Species Classification in Ecology

## Scenario

Ecologists need robust species classifiers that handle noisy field measurements. Random forests average many trees for better generalization.

## Learning Objectives

- Train `RandomForestClassifier`
- Tune `n_estimators`, `max_depth`, `max_features`
- Compare with single decision tree
- Use `OOB score` for free validation

## Prerequisites

- Tutorial 15
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_iris()` and `load_wine()`

## Hands-On Solution

Copy and run the complete script below:

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

X, y = load_wine(return_X_y=True)

models = {
    "Single Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest (100)": RandomForestClassifier(n_estimators=100, random_state=42),
    "Random Forest (500)": RandomForestClassifier(n_estimators=500, random_state=42, oob_score=True),
}

for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5)
    model.fit(X, y)
    oob = getattr(model, "oob_score_", None)
    oob_str = f"  OOB={oob:.3f}" if oob else ""
    print(f"{name:25s}  CV accuracy={scores.mean():.3f} (+/- {scores.std():.3f}){oob_str}")

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)
wine = load_wine()
for name, imp in sorted(zip(wine.feature_names, rf.feature_importances_), key=lambda x: -x[1])[:5]:
    print(f"  {name}: {imp:.4f}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Set `max_features='sqrt'`. Compare with default.
2. Plot feature importances as a bar chart.
3. Does doubling `n_estimators` from 100 to 500 help much?

## Key Takeaways

- Random forests reduce variance by averaging decorrelated trees
- OOB score approximates CV without a separate validation set
- Feature importances are more reliable than single-tree importances

## Navigation

← [Tutorial 15: Decision Trees for Interpretable Rules](15_decision_trees.md) | [Tutorial 17: Gradient Boosting for Churn Prediction](17_gradient_boosting.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
