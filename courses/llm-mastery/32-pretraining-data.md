---
layout: course
title: "32. Pretraining Data: The Real Model"
permalink: /courses/llm-mastery/32-pretraining-data/
course_track: "LLM Mastery"
description: "Weights are a lossy compress of the dataset. Curate accordingly."
level: Advanced
toc:
  - id: "pipeline-themes"
    label: "Pipeline themes"
  - id: "mixtures"
    label: "Mixtures"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 32/50** · Karpathy-style LLM course

Weights are a lossy compress of the dataset. Curate accordingly.

## Pipeline themes
{: #pipeline-themes }

Crawl → extract → filter → dedup → mix domains → pack into sequences.

Quality filters beat naive “more web.” Dedup matters for both loss and memorization.

## Mixtures
{: #mixtures }

Code, math, multilingual, books — mixture weights are a product decision.

## Exercise
{: #exercise }

List three failure modes of training on raw unfiltered web text.


---

[← 31. Tokenization Deep Dive: BPE Under the Hood](/courses/llm-mastery/31-tokenization-deep-dive/)  
[33. Training Parallelism: DDP, FSDP, Pipeline →](/courses/llm-mastery/33-parallelism-ddp-fsdp/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
