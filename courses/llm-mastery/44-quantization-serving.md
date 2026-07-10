---
layout: course
title: "44. Quantization and Local Serving"
permalink: /courses/llm-mastery/44-quantization-serving/
course_track: "LLM Mastery"
description: "Run big models on small machines by shrinking weights."
level: Advanced
toc:
  - id: "idea"
    label: "Idea"
  - id: "formats"
    label: "Formats"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 44/50** · Karpathy-style LLM course

Run big models on small machines by shrinking weights.

## Idea
{: #idea }

Store weights in 8-bit / 4-bit. Accept small quality loss for huge memory wins.

## Formats
{: #formats }

GGUF, GPTQ, AWQ — ecosystem moves fast; principles stay: calibrate, measure perplexity/task drop.

## Exercise
{: #exercise }

Why does 4-bit hurt some tasks more than others?


---

[← 43. Interpretability: Looking Inside](/courses/llm-mastery/43-interpretability-basics/)  
[45. Multimodal LLMs: Vision Enters the Context →](/courses/llm-mastery/45-multimodal-llms/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
