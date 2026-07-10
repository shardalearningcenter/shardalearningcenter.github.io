---
layout: page
title: "Tutorial 29: Ensemble Voting & Stacking"
permalink: /ml-roadmap/29-ensemble-voting-stacking/
---

> **Level:** Advanced · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** MNIST Digit Recognition Ensemble

## Scenario

No single model is best. Voting and stacking combine diverse classifiers for higher accuracy on digit recognition.

## Learning Objectives

- Build `VotingClassifier` (hard and soft voting)
- Build `StackingClassifier` with meta-learner
- Compare ensemble vs individual models
- Understand diversity requirement

## Prerequisites

- Tutorials 14–18
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`load_digits()`

## Hands-On Solution

Copy and run the complete script below:

```python
from sklearn.datasets import load_digits
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import (
    RandomForestClassifier, VotingClassifier, StackingClassifier,
)
from sklearn.neighbors import KNeighborsClassifier

X, y = load_digits(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def make_pipe(clf):
    return Pipeline([("scaler", StandardScaler()), ("clf", clf)])

estimators = [
    ("knn", make_pipe(KNeighborsClassifier(5))),
    ("svm", make_pipe(SVC(probability=True))),
    ("rf", make_pipe(RandomForestClassifier(100, random_state=42))),
]

voting_hard = VotingClassifier(estimators=estimators, voting="hard")
voting_soft = VotingClassifier(estimators=estimators, voting="soft")
stacking = StackingClassifier(
    estimators=estimators,
    final_estimator=LogisticRegression(max_iter=1000),
    cv=3,
)

for name, model in [("KNN", estimators[0][1]), ("SVM", estimators[1][1]),
                     ("RF", estimators[2][1]), ("Voting (hard)", voting_hard),
                     ("Voting (soft)", voting_soft), ("Stacking", stacking)]:
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    print(f"{name:16s}  test accuracy = {acc:.4f}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Remove the best individual model from the ensemble. What happens?
2. Try stacking with `final_estimator=RandomForestClassifier(n_estimators=50)`.
3. Use `cross_val_score` on stacking. Is it higher than individuals?

## Key Takeaways

- Ensembles work when base models make different errors
- Soft voting uses predicted probabilities; hard voting uses class labels
- Stacking learns how to combine base model outputs

## Navigation

← [Tutorial 28: Hierarchical Clustering](28_hierarchical_clustering.md) | [Tutorial 30: Capstone — Titanic Survival Prediction](30_capstone_titanic_survival.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
