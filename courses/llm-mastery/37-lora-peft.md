---
layout: course
title: "37. LoRA and Parameter-Efficient Fine-Tuning"
permalink: /courses/llm-mastery/37-lora-peft/
course_track: "LLM Mastery"
description: "Train low-rank adapters instead of all weights."
level: Advanced
toc:
  - id: "idea"
    label: "Idea"
  - id: "when-to-use"
    label: "When to use"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 37/50** · Karpathy-style LLM course

Train low-rank adapters instead of all weights.

## Idea
{: #idea }

Freeze base W. Learn `ΔW ≈ B A` with small rank r. Store adapters cheaply; swap personas.

## When to use
{: #when-to-use }

Limited compute, many tasks, fast iteration. Full finetune still wins sometimes at scale.

## Exercise
{: #exercise }

If W is 4096×4096 and r=8, how many adapter params roughly (A and B)?


---

[← 36. Supervised Fine-Tuning (SFT)](/courses/llm-mastery/36-finetuning-sft/)  
[38. Preferences: RLHF and DPO →](/courses/llm-mastery/38-preference-rlhf-dpo/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
