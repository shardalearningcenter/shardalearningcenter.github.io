---
layout: course
title: "35. Evaluation: Beyond Vibes"
permalink: /courses/llm-mastery/35-eval-harness-thinking/
course_track: "LLM Mastery"
description: "Loss, harnesses, human prefs — each lies in a different way."
level: Advanced
toc:
  - id: "layers-of-eval"
    label: "Layers of eval"
  - id: "contamination"
    label: "Contamination"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 35/50** · Karpathy-style LLM course

Loss, harnesses, human prefs — each lies in a different way.

## Layers of eval
{: #layers-of-eval }

1. Train/val loss
2. Standard NLP/code/math harnesses
3. Blind human preference (A/B)
4. Product metrics (task success)

## Contamination
{: #contamination }

If the test is in the train scrape, your “SOTA” is cosplay.

## Exercise
{: #exercise }

Design a tiny private eval set for *your* use case that won’t leak easily.


---

[← 34. Mixed Precision Training](/courses/llm-mastery/34-mixed-precision/)  
[36. Supervised Fine-Tuning (SFT) →](/courses/llm-mastery/36-finetuning-sft/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
