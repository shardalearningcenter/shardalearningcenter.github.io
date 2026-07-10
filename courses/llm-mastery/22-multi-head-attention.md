---
layout: course
title: "22. Multi-Head Attention"
permalink: /courses/llm-mastery/22-multi-head-attention/
course_track: "LLM Mastery"
description: "Multiple smaller attentions in parallel = several routing specialists."
level: Intermediate
toc:
  - id: "idea"
    label: "Idea"
  - id: "cost"
    label: "Cost"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 22/50** · Karpathy-style LLM course

Multiple smaller attentions in parallel = several routing specialists.

## Idea
{: #idea }

Split channels into `h` heads. Each head attends independently, then concatenate and project.

Different heads can learn different patterns: local syntax, brackets, rare long links.

## Cost
{: #cost }

Attention is `O(T²)` per head in the naive form. Long context is expensive. Hence all the efficient-attention research.

## Exercise
{: #exercise }

If C=768 and h=12, what’s `head_dim`?


---

[← 21. Self-Attention Mechanics](/courses/llm-mastery/21-self-attention-mechanics/)  
[23. Positional Information: Absolute, Relative, RoPE →](/courses/llm-mastery/23-positional-embeddings/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
