---
layout: course
course_track: "AI / ML"
title: "Tutorial 06: Categorical Encoding"
permalink: /courses/ml-roadmap/06-categorical-encoding/
---

> **Level:** Beginner · **Part of:** [ML Learning Roadmap](/courses/ml-learning-roadmap/)

[← Back to roadmap](/courses/ml-learning-roadmap/)

> **Case Study:** Employee Attrition Prediction

## Scenario

HR data contains categorical fields (department, job role, education). ML algorithms need numeric representations.

## Learning Objectives

- Use `OneHotEncoder` for nominal categories
- Use `OrdinalEncoder` for ordered categories
- Handle unknown categories at inference time
- Combine encoded features with numeric columns

## Prerequisites

- Tutorial 05
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

Synthetic employee dataset (generated in code)

## Hands-On Solution

Copy and run the complete script below:

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer

np.random.seed(42)
n = 200
df = pd.DataFrame({
    "age": np.random.randint(22, 60, n),
    "salary": np.random.randint(30000, 120000, n),
    "department": np.random.choice(["HR", "Engineering", "Sales"], n),
    "education": np.random.choice(["Bachelor", "Master", "PhD"], n),
    "left_company": np.random.randint(0, 2, n),
})

X = df.drop("left_company", axis=1)
y = df["left_company"]

preprocessor = ColumnTransformer([
    ("num", "passthrough", ["age", "salary"]),
    ("dept", OneHotEncoder(handle_unknown="ignore"), ["department"]),
    ("edu", OrdinalEncoder(categories=[["Bachelor", "Master", "PhD"]]), ["education"]),
])

X_encoded = preprocessor.fit_transform(X)
print(f"Original shape: {X.shape}")
print(f"Encoded shape:  {X_encoded.shape}")
print(f"Feature names: {preprocessor.get_feature_names_out()}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Add a new department 'Legal' in test data. Verify `handle_unknown='ignore'` works.
2. Compare OneHotEncoder output with `pd.get_dummies`.
3. Why is OrdinalEncoder risky for unordered categories like department?

## Key Takeaways

- One-hot encoding for nominal categories without order
- Ordinal encoding only when a true order exists
- ColumnTransformer cleanly handles mixed feature types

## Navigation

← [Tutorial 05: Feature Scaling with StandardScaler](05_feature_scaling.md) | [Tutorial 07: Handling Missing Values](07_missing_value_imputation.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
