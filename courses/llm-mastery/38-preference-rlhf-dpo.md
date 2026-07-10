---
layout: course
title: "38. Preferences: RLHF and DPO"
permalink: /courses/llm-mastery/38-preference-rlhf-dpo/
course_track: "LLM Mastery"
description: "Align to human (or AI) preferences when “correct next token” isn’t enough."
level: Advanced
toc:
  - id: "rlhf-sketch"
    label: "RLHF sketch"
  - id: "dpo"
    label: "DPO"
  - id: "reality"
    label: "Reality"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 38/50** · Karpathy-style LLM course

Align to human (or AI) preferences when “correct next token” isn’t enough.

## RLHF sketch
{: #rlhf-sketch }

SFT model → reward model on comparisons → RL (PPO) against reward with KL tether to SFT.

## DPO
{: #dpo }

Skip explicit RL: optimize a closed-form objective on preference pairs. Often simpler.

## Reality
{: #reality }

Alignment is underspecified. Pref data has politics, taste, and annotator fatigue.

## Exercise
{: #exercise }

Why do we KL-penalize away from the SFT model during RLHF?


---

[← 37. LoRA and Parameter-Efficient Fine-Tuning](/courses/llm-mastery/37-lora-peft/)  
[39. Prompting as Programming →](/courses/llm-mastery/39-prompting-as-programming/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
