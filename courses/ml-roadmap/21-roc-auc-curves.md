---
layout: course
course_track: "AI / ML"
title: "Tutorial 21: ROC / AUC Curves"
permalink: /courses/ml-roadmap/21-roc-auc-curves/
---

> **Level:** Intermediate · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** Medical Test Evaluation

## Scenario

A diagnostic test needs threshold selection. ROC curves show the tradeoff between true positive rate and false positive rate across all thresholds.

## Learning Objectives

- Compute ROC curve with `roc_curve`
- Calculate AUC with `roc_auc_score`
- Plot ROC curves comparing models
- Choose operating point for clinical use

## Prerequisites

- Tutorial 20
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_breast_cancer()`

## Hands-On Solution

Copy and run the complete script below:

```python
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, roc_auc_score

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
}

plt.figure(figsize=(7, 6))
for name, model in models.items():
    model.fit(X_train_s, y_train)
    y_prob = model.predict_proba(X_test_s)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)
    plt.plot(fpr, tpr, label=f"{name} (AUC={auc:.3f})")

plt.plot([0, 1], [0, 1], "k--", label="Random")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves — Breast Cancer Diagnosis")
plt.legend()
plt.savefig("roc_curves.png", dpi=120)
print("Saved roc_curves.png")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Find the threshold where TPR ≥ 0.95. What is the FPR?
2. Add a KNN model to the ROC plot.
3. Is AUC threshold-independent? When might it mislead?

## Key Takeaways

- ROC curves evaluate ranking quality across all thresholds
- AUC = 0.5 is random; AUC = 1.0 is perfect separation
- Use ROC for balanced problems; consider PR curves for heavy imbalance

## Navigation

← [Tutorial 20: Classification Metrics Deep Dive](20_classification_metrics.md) | [Tutorial 22: Learning Curves and Bias-Variance Diagnosis](22_learning_curves.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
