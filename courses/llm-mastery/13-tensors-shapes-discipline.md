---
layout: course
title: "13. Tensor Shapes: The Hidden Curriculum"
permalink: /courses/llm-mastery/13-tensors-shapes-discipline/
course_track: "LLM Mastery"
description: "Most LLM bugs are shape bugs. Become religious about them."
level: Intermediate
toc:
  - id: "always-know"
    label: "Always know"
  - id: "print-shapes"
    label: "Print shapes"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 13/50** · Karpathy-style LLM course

Most LLM bugs are shape bugs. Become religious about them.

## Always know
{: #always-know }

For a Transformer block, chant:

```
B = batch
T = time (tokens)
C = channels (d_model)
```

Attention scores: `B, n_head, T, T`
Values projected: `B, n_head, T, head_dim`

## Print shapes
{: #print-shapes }

`print(x.shape)` is not shameful. It’s professionalism.

## Exercise
{: #exercise }

If B=2, T=8, C=32, n_head=4, what is `head_dim`?


---

[← 12. Micrograd Energy: Autograd From Scratch](/courses/llm-mastery/12-autograd-from-scratch/)  
[14. Softmax and Temperature, Carefully →](/courses/llm-mastery/14-softmax-temperature/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
