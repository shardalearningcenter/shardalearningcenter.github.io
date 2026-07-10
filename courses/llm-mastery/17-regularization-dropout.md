---
layout: course
title: "17. Dropout, Weight Decay, and Noise as Teachers"
permalink: /courses/llm-mastery/17-regularization-dropout/
course_track: "LLM Mastery"
description: "Regularization = deliberate handicap so the model can’t memorize casually."
level: Intermediate
toc:
  - id: "dropout"
    label: "Dropout"
  - id: "weight-decay"
    label: "Weight decay"
  - id: "data-tricks"
    label: "Data > tricks"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 17/50** · Karpathy-style LLM course

Regularization = deliberate handicap so the model can’t memorize casually.

## Dropout
{: #dropout }

Randomly zero activations in training. Forces redundant representations. Off at eval (rescale).

## Weight decay
{: #weight-decay }

Penalize large weights. AdamW does this cleanly.

## Data > tricks
{: #data-tricks }

For LLMs, scale and data quality dominate. Regularization still matters, especially on smaller runs.

## Exercise
{: #exercise }

Why must dropout behave differently at train vs eval?


---

[← 16. Initialization Is Not Optional](/courses/llm-mastery/16-initialization-matters/)  
[18. RNNs: The Old Kings and Their Pain →](/courses/llm-mastery/18-rnns-and-their-pain/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
