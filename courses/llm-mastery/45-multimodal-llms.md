---
layout: course
title: "45. Multimodal LLMs: Vision Enters the Context"
permalink: /courses/llm-mastery/45-multimodal-llms/
course_track: "LLM Mastery"
description: "Images become token-like embeddings in the same residual stream."
level: Advanced
toc:
  - id: "pattern"
    label: "Pattern"
  - id: "implications"
    label: "Implications"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 45/50** · Karpathy-style LLM course

Images become token-like embeddings in the same residual stream.

## Pattern
{: #pattern }

Vision encoder → projector → prefixes into LLM token space. Train so visual tokens speak the language model’s dialect.

## Implications
{: #implications }

UI agents, document understanding, robotics — same next-token core, richer observations.

## Exercise
{: #exercise }

Why might OCR-in-the-loop still beat pure vision-LLM for dense text in images?


---

[← 44. Quantization and Local Serving](/courses/llm-mastery/44-quantization-serving/)  
[46. Diffusion vs Autoregressive: Two Generative Religions →](/courses/llm-mastery/46-diffusion-vs-ar/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
