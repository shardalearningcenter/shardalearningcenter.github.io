---
layout: course
title: "23. Positional Information: Absolute, Relative, RoPE"
permalink: /courses/llm-mastery/23-positional-embeddings/
course_track: "LLM Mastery"
description: "Attention alone is permutation-equivariant. Position must be injected."
level: Intermediate
toc:
  - id: "absolute-embeddings"
    label: "Absolute embeddings"
  - id: "relative-rope"
    label: "Relative / RoPE"
  - id: "intuition"
    label: "Intuition"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 23/50** · Karpathy-style LLM course

Attention alone is permutation-equivariant. Position must be injected.

## Absolute embeddings
{: #absolute-embeddings }

Add a learned vector per position index. Simple. Weak for very long contexts.

## Relative / RoPE
{: #relative-rope }

Modern LLMs often use **rotary embeddings (RoPE)**: rotate Q/K by position-dependent angles so attention becomes relative-friendly.

## Intuition
{: #intuition }

Without position, “dog bites man” and “man bites dog” are bag-similar to the attention mixer.

## Exercise
{: #exercise }

Why can’t a plain self-attention layer, alone, know order?


---

[← 22. Multi-Head Attention](/courses/llm-mastery/22-multi-head-attention/)  
[24. Residuals and LayerNorm: The Stabilizers →](/courses/llm-mastery/24-layernorm-residuals/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
