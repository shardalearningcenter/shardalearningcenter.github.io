---
layout: course
title: "24. Residuals and LayerNorm: The Stabilizers"
permalink: /courses/llm-mastery/24-layernorm-residuals/
course_track: "LLM Mastery"
description: "Skip connections make depth trainable. Norm keeps scales sane."
level: Intermediate
toc:
  - id: "residual-stream"
    label: "Residual stream"
  - id: "layernorm-rmsnorm"
    label: "LayerNorm / RMSNorm"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 24/50** · Karpathy-style LLM course

Skip connections make depth trainable. Norm keeps scales sane.

## Residual stream
{: #residual-stream }

`x = x + SubLayer(x)`

The model learns *edits* to a running representation. Gradients have a highway.

## LayerNorm / RMSNorm
{: #layernorm-rmsnorm }

Normalize across features. Pre-Norm (norm before sublayer) is common in LLMs for stability.

## Exercise
{: #exercise }

If you remove residuals from a 24-layer net, what usually happens to training?


---

[← 23. Positional Information: Absolute, Relative, RoPE](/courses/llm-mastery/23-positional-embeddings/)  
[25. The Transformer MLP: Where Facts Often Live →](/courses/llm-mastery/25-mlp-in-transformer/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
