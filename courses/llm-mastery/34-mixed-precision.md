---
layout: course
title: "34. Mixed Precision Training"
permalink: /courses/llm-mastery/34-mixed-precision/
course_track: "LLM Mastery"
description: "fp16/bf16 for speed; keep master weights in fp32 for sanity."
level: Advanced
toc:
  - id: "why"
    label: "Why"
  - id: "how"
    label: "How"
  - id: "bf16-vs-fp16"
    label: "bf16 vs fp16"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 34/50** · Karpathy-style LLM course

fp16/bf16 for speed; keep master weights in fp32 for sanity.

## Why
{: #why }

Tensor Cores love lower precision. Memory bandwidth drops. Throughput rises.

## How
{: #how }

Forward/backward in bf16/fp16, update fp32 master copy. Loss scaling for fp16.

## bf16 vs fp16
{: #bf16-vs-fp16 }

bf16 has friendlier range; often stabler for LLMs on modern hardware.

## Exercise
{: #exercise }

Name one numerical failure mode fp16 introduces that bf16 softens.


---

[← 33. Training Parallelism: DDP, FSDP, Pipeline](/courses/llm-mastery/33-parallelism-ddp-fsdp/)  
[35. Evaluation: Beyond Vibes →](/courses/llm-mastery/35-eval-harness-thinking/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
