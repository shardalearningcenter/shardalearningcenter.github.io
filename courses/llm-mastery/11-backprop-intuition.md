---
layout: course
title: "11. Backpropagation as Local Blame"
permalink: /courses/llm-mastery/11-backprop-intuition/
course_track: "LLM Mastery"
description: "Every node asks: how did I affect the loss? Then tells its parents."
level: Intermediate
toc:
  - id: "the-story"
    label: "The story"
  - id: "why-grads-vanish-or-explode"
    label: "Why grads vanish or explode"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 11/50** · Karpathy-style LLM course

Every node asks: how did I affect the loss? Then tells its parents.

## The story
{: #the-story }

Forward pass: compute outputs.
Backward pass: each operation receives `dloss/doutput` and multiplies by local derivatives to produce `dloss/dinputs`.

Chain rule, implemented as a graph traversal. Frameworks do it for you; you must still feel it.

## Why grads vanish or explode
{: #why-grads-vanish-or-explode }

Multiply many numbers <1 → vanish. Many >1 → explode. Depth is dangerous without care (init, residual, norm).

## Exercise
{: #exercise }

For `y = a*b`, if `dL/dy = 2`, `a=3`, `b=4`, what are `dL/da` and `dL/db`?


---

[← 10. The MakeMore Mindset: Build Tiny, Understand Deeply](/courses/llm-mastery/10-makemore-mindset/)  
[12. Micrograd Energy: Autograd From Scratch →](/courses/llm-mastery/12-autograd-from-scratch/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
