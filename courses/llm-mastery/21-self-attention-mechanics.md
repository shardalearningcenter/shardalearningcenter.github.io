---
layout: course
title: "21. Self-Attention Mechanics"
permalink: /courses/llm-mastery/21-self-attention-mechanics/
course_track: "LLM Mastery"
description: "Q, K, V are just linear projections. The softmax is the routing."
level: Intermediate
toc:
  - id: "equations-with-intent"
    label: "Equations with intent"
  - id: "causal-mask"
    label: "Causal mask"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 21/50** · Karpathy-style LLM course

Q, K, V are just linear projections. The softmax is the routing.

## Equations with intent
{: #equations-with-intent }

```
Q = X Wq
K = X Wk
V = X Wv
attn = softmax(Q K^T / sqrt(d_k))
out = attn V
```

Each token builds a query (“what am I looking for?”), keys answer (“what do I contain?”), values provide content to mix.

## Causal mask
{: #causal-mask }

For LMs, position i cannot see j > i. Mask those scores to `-inf` before softmax.

## Exercise
{: #exercise }

Why divide by `sqrt(d_k)`?


---

[← 20. Reading 'Attention Is All You Need' Like an Engineer](/courses/llm-mastery/20-attention-is-all-you-need-read/)  
[22. Multi-Head Attention →](/courses/llm-mastery/22-multi-head-attention/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
