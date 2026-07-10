---
layout: course
title: "25. The Transformer MLP: Where Facts Often Live"
permalink: /courses/llm-mastery/25-mlp-in-transformer/
course_track: "LLM Mastery"
description: "Attention routes; MLPs transform. A lot of knowledge is in the MLP weights."
level: Intermediate
toc:
  - id: "structure"
    label: "Structure"
  - id: "role"
    label: "Role"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 25/50** · Karpathy-style LLM course

Attention routes; MLPs transform. A lot of knowledge is in the MLP weights.

## Structure
{: #structure }

Usually: `Linear → GELU/SiLU → Linear`, expanding to 4× (or more) then back.

## Role
{: #role }

Channel mixing. Nonlinear features. Empirically, many “memorized” associations show up in MLP subspaces (interpretability research).

## Exercise
{: #exercise }

If d_model=512 and expansion=4, how many params roughly in one MLP (ignore biases)?


---

[← 24. Residuals and LayerNorm: The Stabilizers](/courses/llm-mastery/24-layernorm-residuals/)  
[26. GPT Architecture: Decoder-Only Transformers →](/courses/llm-mastery/26-gpt-architecture/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
