---
layout: page
title: "Tutorial 19: Naive Bayes Text"
permalink: /ml-roadmap/19-naive-bayes-text/
---

> **Level:** Advanced · **Part of:** [ML Learning Roadmap](/ml-learning-roadmap/)

[← Back to roadmap](/ml-learning-roadmap/)

> **Case Study:** Spam Email Filter

## Scenario

Build a spam/ham classifier for an email provider. Naive Bayes is fast, works with small data, and is a classic text classification baseline.

## Learning Objectives

- Use `CountVectorizer` and `TfidfVectorizer`
- Train `MultinomialNB`
- Inspect most informative features per class
- Compare speed with SVM

## Prerequisites

- Tutorial 18
- Python 3.9+, scikit-learn, NumPy, pandas, matplotlib

## Dataset

Built-in spam/ham example corpus

## Hands-On Solution

Copy and run the complete script below:

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import numpy as np

# Mini spam corpus
texts = [
    "win money now click here free prize", "urgent claim your reward today",
    "limited offer act now winner selected", "free vacation click to claim",
    "meeting tomorrow at 3pm conference room", "project deadline moved to Friday",
    "lunch with team at noon today", "quarterly report attached please review",
    "schedule sync for next sprint planning", "budget approval needed by EOD",
] * 10
labels = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0] * 10  # 1=spam, 0=ham

X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

pipe = Pipeline([
    ("vec", CountVectorizer()),
    ("nb", MultinomialNB()),
])
pipe.fit(X_train, y_train)
print(classification_report(y_test, pipe.predict(X_test), target_names=["ham", "spam"]))

# Most spammy words
vec = pipe.named_steps["vec"]
nb = pipe.named_steps["nb"]
feature_names = vec.get_feature_names_out()
spam_log_probs = nb.feature_log_prob_[1]
top_spam = np.argsort(spam_log_probs)[-10:][::-1]
print("Top spam indicators:", [feature_names[i] for i in top_spam])

# Test new email
test = ["congratulations you won a free cruise click now"]
print(f"Prediction: {'spam' if pipe.predict(test)[0] == 1 else 'ham'}")
```

## Expected Output

When you run the script, you should see evaluation metrics printed to the console. Some tutorials also save `.png` plot files in the current directory.

## Exercises

1. Replace CountVectorizer with TfidfVectorizer. Any difference?
2. Add 5 more ham and 5 more spam examples. Retrain and evaluate.
3. Use `fetch_20newsgroups` binary (sci vs rec). Compare NB vs LinearSVC speed.

## Key Takeaways

- Naive Bayes assumes feature independence (naive) but works well for text
- Extremely fast training and prediction
- Great baseline before trying heavier models

## Navigation

← [Tutorial 18: Support Vector Machines](18_svm_classification.md) | [Tutorial 20: Classification Metrics Deep Dive](20_classification_metrics.md) →

---

*Part of the [ML Learning Roadmap](../README.md) — Hands-On with scikit-learn*
