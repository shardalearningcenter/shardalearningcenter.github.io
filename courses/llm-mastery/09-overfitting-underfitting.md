---
layout: course
title: "09. Overfitting, Underfitting, and Data"
permalink: /courses/llm-mastery/09-overfitting-underfitting/
course_track: "LLM Mastery"
description: "Models memorize. Data is the real moat. Regularization is damage control."
level: Beginner
toc:
  - id: "two-failure-modes"
    label: "Two failure modes"
  - id: "what-actually-helps"
    label: "What actually helps"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 9/50** · Karpathy-style LLM course

Models memorize. Data is the real moat. Regularization is damage control.

## Two failure modes
{: #two-failure-modes }

- **Underfit:** train loss high, model too weak or undertrained.
- **Overfit:** train loss low, val loss high — memorization.

LLMs trained on internet-scale data still memorize. That’s not always bad (facts!), but eval leakage is a real scientific problem.

## What actually helps
{: #what-actually-helps }

More diverse data, careful dedup, regularization (dropout, weight decay), early stopping on a true held-out set.

## Exercise
{: #exercise }

Why is “test set contamination” especially nasty for LLM benchmarks?


---

[← 08. The Training Loop, End to End](/courses/llm-mastery/08-training-loop-basics/)  
[10. The MakeMore Mindset: Build Tiny, Understand Deeply →](/courses/llm-mastery/10-makemore-mindset/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
