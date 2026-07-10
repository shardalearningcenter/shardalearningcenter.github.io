---
layout: course
title: "33. Training Parallelism: DDP, FSDP, Pipeline"
permalink: /courses/llm-mastery/33-parallelism-ddp-fsdp/
course_track: "LLM Mastery"
description: "One GPU is not enough. Split data, params, or layers."
level: Advanced
toc:
  - id: "data-parallel"
    label: "Data parallel"
  - id: "fsdp-zero"
    label: "FSDP / ZeRO"
  - id: "pipeline-tensor-parallel"
    label: "Pipeline / tensor parallel"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 33/50** · Karpathy-style LLM course

One GPU is not enough. Split data, params, or layers.

## Data parallel
{: #data-parallel }

Same model, different batches, allreduce grads. Simple.

## FSDP / ZeRO
{: #fsdp-zero }

Shard parameters/optimizer states across ranks to fit bigger models.

## Pipeline / tensor parallel
{: #pipeline-tensor-parallel }

Split the model graph. Harder engineering, needed at frontier scale.

## Exercise
{: #exercise }

Which parallelism primarily reduces **memory per GPU** for a single giant layer?


---

[← 32. Pretraining Data: The Real Model](/courses/llm-mastery/32-pretraining-data/)  
[34. Mixed Precision Training →](/courses/llm-mastery/34-mixed-precision/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
