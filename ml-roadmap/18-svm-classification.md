---
layout: page
title: "Tutorial 18: SVM Classification"
permalink: /ml-roadmap/18-svm-classification/
---

> **Level:** Advanced · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** Document Topic Classification

## Scenario

A news aggregator classifies articles into categories. SVMs with TF-IDF features excel at high-dimensional sparse text data.

## Learning Objectives

- Train `SVC` with RBF and linear kernels
- Tune `C` and `gamma` hyperparameters
- Use SVM with text features via Pipeline
- Understand support vectors concept

## Prerequisites

- Tutorial 05
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

`fetch_20newsgroups` subset (4 categories)

## Hands-On Solution

Copy and run the complete script below:

```python
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

categories = ["sci.space", "comp.graphics", "rec.sport.baseball", "talk.politics.misc"]
data = fetch_20newsgroups(subset="train", categories=categories, shuffle=True, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

pipe = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000, stop_words="english")),
    ("svm", LinearSVC(C=1.0, max_iter=5000)),
])
pipe.fit(X_train, y_train)
print(classification_report(y_test, pipe.predict(X_test), target_names=data.target_names))

for C in [0.1, 1.0, 10.0]:
    pipe.named_steps["svm"].set_params(C=C)
    pipe.fit(X_train, y_train)
    acc = pipe.score(X_test, y_test)
    print(f"C={C:5.1f}  accuracy={acc:.4f}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Try `TfidfVectorizer(ngram_range=(1, 2))`. Does accuracy improve?
2. Use `SVC(kernel='rbf')` on a numeric dataset (digits). Compare with linear.
3. How many support vectors does LinearSVC use? (Check `n_support_` on SVC.)

## Key Takeaways

- LinearSVC scales well to high-dimensional sparse text features
- C controls the regularization tradeoff (smaller C = more regularization)
- Always pair text models with TfidfVectorizer in a Pipeline

## Navigation

← [Tutorial 17: Gradient Boosting for Churn Prediction](17_gradient_boosting.md) | [Tutorial 19: Naive Bayes for Text Classification](19_naive_bayes_text.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
