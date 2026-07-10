---
layout: course
title: "28. KV Cache: Why Chat Is Fast After the First Token"
permalink: /courses/llm-mastery/28-kv-cache/
course_track: "LLM Mastery"
description: "Don’t recompute past keys/values every step."
level: Advanced
toc:
  - id: "problem"
    label: "Problem"
  - id: "fix"
    label: "Fix"
  - id: "memory"
    label: "Memory"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 28/50** · Karpathy-style LLM course

Don’t recompute past keys/values every step.

## Problem
{: #problem }

Naive generation recomputes attention over the full context each new token → wasteful.

## Fix
{: #fix }

Cache K and V for past positions. Each step only computes the new row.

## Memory
{: #memory }

KV cache is often the memory bottleneck for long-context serving.

## Exercise
{: #exercise }

If T=4096, layers=32, heads=32, head_dim=128, dtype=fp16, rough KV cache size per sequence?


---

[← 27. Implement a Tiny GPT (Conceptual Walkthrough)](/courses/llm-mastery/27-implement-tiny-gpt/)  
[29. Batching, Throughput, and the Economics of Tokens →](/courses/llm-mastery/29-batching-and-throughput/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
