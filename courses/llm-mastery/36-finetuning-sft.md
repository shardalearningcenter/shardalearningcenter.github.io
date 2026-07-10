---
layout: course
title: "36. Supervised Fine-Tuning (SFT)"
permalink: /courses/llm-mastery/36-finetuning-sft/
course_track: "LLM Mastery"
description: "Teach the base model to follow instructions with curated demos."
level: Advanced
toc:
  - id: "what-changes"
    label: "What changes"
  - id: "data-quality"
    label: "Data quality"
  - id: "risk"
    label: "Risk"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 36/50** · Karpathy-style LLM course

Teach the base model to follow instructions with curated demos.

## What changes
{: #what-changes }

Same next-token loss, but data is (prompt, high-quality answer) dialogues.

## Data quality
{: #data-quality }

A few thousand *excellent* examples can beat millions of mediocre ones for assistants.

## Risk
{: #risk }

Catastrophic forgetting / style collapse. Mix a bit of pretraining distribution if needed.

## Exercise
{: #exercise }

Write 3 SFT examples for a “patient Python tutor” persona.


---

[← 35. Evaluation: Beyond Vibes](/courses/llm-mastery/35-eval-harness-thinking/)  
[37. LoRA and Parameter-Efficient Fine-Tuning →](/courses/llm-mastery/37-lora-peft/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
