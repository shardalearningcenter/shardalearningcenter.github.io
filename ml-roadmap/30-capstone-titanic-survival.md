---
layout: page
title: "Tutorial 30: Capstone — Titanic Survival"
permalink: /ml-roadmap/30-capstone-titanic-survival/
---

> **Level:** Advanced · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** End-to-End ML Project

## Scenario

Bring everything together: load messy data, explore, preprocess, build pipelines, tune hyperparameters, and evaluate a model that predicts Titanic passenger survival.

## Learning Objectives

- Execute a complete ML workflow from raw data to submission-ready model
- Handle missing values, encoding, and feature engineering
- Use ColumnTransformer + Pipeline + GridSearchCV
- Document decisions and evaluate with proper metrics

## Prerequisites

- All tutorials 01–29
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

Titanic dataset via seaborn (or CSV)

## Hands-On Solution

Copy and run the complete script below:

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load Titanic data
try:
    import seaborn as sns
    df = sns.load_dataset("titanic")
except ImportError:
  raise SystemExit("pip install seaborn")

# Feature engineering
df["family_size"] = df["sibsp"] + df["parch"] + 1
df["is_alone"] = (df["family_size"] == 1).astype(int)
df["deck"] = df["deck"].fillna("Unknown")

features = ["pclass", "sex", "age", "fare", "embarked", "family_size", "is_alone", "deck"]
target = "survived"

data = df[features + [target]].dropna(subset=[target])
X = data[features]
y = data[target]

num_cols = ["age", "fare", "family_size"]
cat_cols = ["pclass", "sex", "embarked", "is_alone", "deck"]

preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]), num_cols),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ]), cat_cols),
])

pipe = Pipeline([
    ("prep", preprocessor),
    ("clf", RandomForestClassifier(random_state=42)),
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

param_grid = {
    "clf__n_estimators": [100, 200],
    "clf__max_depth": [5, 10, None],
    "clf__min_samples_leaf": [1, 3, 5],
}

search = GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy", n_jobs=-1)
search.fit(X_train, y_train)

print(f"Best params: {search.best_params_}")
print(f"CV accuracy: {search.best_score_:.4f}")
y_pred = search.predict(X_test)
print(f"Test accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred, target_names=["died", "survived"]))

# Feature importances (approximate via permutation on encoded features)
best = search.best_estimator_
importances = best.named_steps["clf"].feature_importances_
print(f"\nTop feature importances (encoded space): {sorted(importances, reverse=True)[:5]}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Add a `title` feature extracted from passenger name (Mr, Mrs, Miss).
2. Try `class_weight='balanced'`. Does recall for 'survived' improve?
3. Write a 1-page project report: problem, approach, results, next steps.
4. Export the best pipeline with `joblib` and load it for predictions on new data.

## Key Takeaways

- Real projects combine EDA, feature engineering, pipelines, and tuning
- ColumnTransformer is the standard pattern for messy tabular data
- Document your workflow — reproducibility matters as much as accuracy
- Congratulations — you've completed the 30-tutorial scikit-learn roadmap!

## Navigation

← [Tutorial 29: Voting and Stacking Ensembles](29_ensemble_voting_stacking.md)

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
