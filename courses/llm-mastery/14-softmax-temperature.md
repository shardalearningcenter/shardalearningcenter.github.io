---
layout: course
title: "14. Softmax and Temperature, Carefully"
permalink: /courses/llm-mastery/14-softmax-temperature/
course_track: "LLM Mastery"
description: "Softmax is competitive normalization. Temperature rewires the competition."
level: Intermediate
toc:
  - id: "softmax"
    label: "Softmax"
  - id: "temperature"
    label: "Temperature"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 14/50** · Karpathy-style LLM course

Softmax is competitive normalization. Temperature rewires the competition.

## Softmax
{: #softmax }

```
softmax(z)_i = exp(z_i) / sum_j exp(z_j)
```

Numerically: subtract `max(z)` first or you explode `exp`.

## Temperature
{: #temperature }

Use `softmax(z / T)`.
- T→0: winner-take-all
- T=1: default
- T>1: flatter, more random

## Exercise
{: #exercise }

Why is subtracting max(z) safe (doesn’t change softmax)?


---

[← 13. Tensor Shapes: The Hidden Curriculum](/courses/llm-mastery/13-tensors-shapes-discipline/)  
[15. SGD, Adam, and Why Adam Won LLMs →](/courses/llm-mastery/15-optimization-sgd-adam/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
