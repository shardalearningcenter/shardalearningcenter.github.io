---
layout: course
title: "26. GPT Architecture: Decoder-Only Transformers"
permalink: /courses/llm-mastery/26-gpt-architecture/
course_track: "LLM Mastery"
description: "Causal self-attention stack. No encoder. Generate left to right."
level: Intermediate
toc:
  - id: "recipe"
    label: "Recipe"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 26/50** · Karpathy-style LLM course

Causal self-attention stack. No encoder. Generate left to right.

## Recipe
{: #recipe }

- Token embedding + position scheme
- N × (causal MHA + MLP) with norms/residuals
- Final norm + vocab projection
- Train with next-token cross-entropy

That’s GPT-2/3-style at a high level. Details differ (norm placement, activation, bias, RoPE, etc.).

## Exercise
{: #exercise }

Name three differences between encoder-decoder T5 and decoder-only GPT.


---

[← 25. The Transformer MLP: Where Facts Often Live](/courses/llm-mastery/25-mlp-in-transformer/)  
[27. Implement a Tiny GPT (Conceptual Walkthrough) →](/courses/llm-mastery/27-implement-tiny-gpt/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
