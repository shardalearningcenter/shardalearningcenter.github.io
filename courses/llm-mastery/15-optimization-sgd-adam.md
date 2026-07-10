---
layout: course
title: "15. SGD, Adam, and Why Adam Won LLMs"
permalink: /courses/llm-mastery/15-optimization-sgd-adam/
course_track: "LLM Mastery"
description: "Adaptive methods handle messy gradient scales in deep nets."
level: Intermediate
toc:
  - id: "sgd"
    label: "SGD"
  - id: "adam"
    label: "Adam"
  - id: "learning-rate"
    label: "Learning rate"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 15/50** · Karpathy-style LLM course

Adaptive methods handle messy gradient scales in deep nets.

## SGD
{: #sgd }

`θ ← θ - lr * grad`

Simple. Sensitive to LR. Needs help (momentum).

## Adam
{: #adam }

Keeps exponential moving averages of grad and grad². Per-parameter step sizes. Default for many LLM runs (AdamW = Adam + decoupled weight decay).

## Learning rate
{: #learning-rate }

Too high: loss NaNs. Too low: you age waiting. Warmup + cosine decay is a common LLM recipe.

## Exercise
{: #exercise }

In one paragraph: what problem does adaptive LR solve?


---

[← 14. Softmax and Temperature, Carefully](/courses/llm-mastery/14-softmax-temperature/)  
[16. Initialization Is Not Optional →](/courses/llm-mastery/16-initialization-matters/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
