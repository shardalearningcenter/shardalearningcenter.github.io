---
layout: course
course_track: "AI / ML"
title: "Tutorial 22: Learning Curves"
permalink: /courses/ml-roadmap/22-learning-curves/
---

> **Level:** Advanced · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** Predicting Customer Lifetime Value

## Scenario

Your model plateaus early. Learning curves reveal whether you need more data, a simpler model, or a more complex one.

## Learning Objectives

- Plot learning curves with `learning_curve`
- Diagnose high bias vs high variance
- Compare simple vs complex models
- Decide if more data will help

## Prerequisites

- Tutorial 16
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`fetch_california_housing()`

## Hands-On Solution

Copy and run the complete script below:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import learning_curve
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = fetch_california_housing(return_X_y=True)

def plot_learning_curve(estimator, title, filename):
    train_sizes, train_scores, val_scores = learning_curve(
        estimator, X, y, cv=5, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 8), scoring="neg_mean_squared_error"
    )
    train_rmse = np.sqrt(-train_scores.mean(axis=1))
    val_rmse = np.sqrt(-val_scores.mean(axis=1))

    plt.figure(figsize=(7, 5))
    plt.plot(train_sizes, train_rmse, "o-", label="Training")
    plt.plot(train_sizes, val_rmse, "o-", label="Validation")
    plt.xlabel("Training samples")
    plt.ylabel("RMSE")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=120)
    print(f"Saved {filename}")

plot_learning_curve(
    Pipeline([("s", StandardScaler()), ("m", LinearRegression())]),
    "Linear Regression Learning Curve", "lc_linear.png"
)
plot_learning_curve(
    DecisionTreeRegressor(max_depth=None),
    "Deep Tree Learning Curve (overfitting)", "lc_tree.png"
)
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. For the deep tree: does validation RMSE improve with more data?
2. Plot learning curves for Ridge with alpha=100 vs alpha=0.01.
3. Write a diagnosis: which model has high bias? High variance?

## Key Takeaways

- Large gap between train and validation = high variance (overfitting)
- Both curves high and close = high bias (underfitting)
- Parallel curves that don't converge = more data may help

## Navigation

← [Tutorial 21: ROC Curves and AUC](21_roc_auc_curves.md) | [Tutorial 23: Hyperparameter Tuning with GridSearchCV](23_grid_search_cv.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
