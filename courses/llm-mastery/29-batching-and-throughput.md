---
layout: course
title: "29. Batching, Throughput, and the Economics of Tokens"
permalink: /courses/llm-mastery/29-batching-and-throughput/
course_track: "LLM Mastery"
description: "LLMs are memory-bandwidth beasts. Batching amortizes weight reads."
level: Advanced
toc:
  - id: "two-regimes"
    label: "Two regimes"
  - id: "continuous-batching"
    label: "Continuous batching"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 29/50** · Karpathy-style LLM course

LLMs are memory-bandwidth beasts. Batching amortizes weight reads.

## Two regimes
{: #two-regimes }

- **Prefill:** process prompt (compute heavy, parallel over T)
- **Decode:** one token at a time (memory heavy)

## Continuous batching
{: #continuous-batching }

Servers pack many sequences at different lengths to keep GPUs busy.

## Exercise
{: #exercise }

Why might increasing batch size stop helping after a point?


---

[← 28. KV Cache: Why Chat Is Fast After the First Token](/courses/llm-mastery/28-kv-cache/)  
[30. Scaling Laws: The Bitter Lesson, Quantified →](/courses/llm-mastery/30-scaling-laws-intuition/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
