---
layout: course
title: "16. Initialization Is Not Optional"
permalink: /courses/llm-mastery/16-initialization-matters/
course_track: "LLM Mastery"
description: "Bad init → dead ReLUs / exploding signals. Good init → training starts."
level: Intermediate
toc:
  - id: "goal"
    label: "Goal"
  - id: "common-practices"
    label: "Common practices"
  - id: "signal"
    label: "Signal"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 16/50** · Karpathy-style LLM course

Bad init → dead ReLUs / exploding signals. Good init → training starts.

## Goal
{: #goal }

Keep activation variances reasonable as you go deeper.

## Common practices
{: #common-practices }

- Xavier / Kaiming init depending on nonlinearity
- Residual networks prefer specific scales
- Embedding init often small random

## Signal
{: #signal }

If day-0 loss is insane or grads are zero, suspect init + architecture before “more data.”

## Exercise
{: #exercise }

What happens to a deep net with all weights initialized to 0?


---

[← 15. SGD, Adam, and Why Adam Won LLMs](/courses/llm-mastery/15-optimization-sgd-adam/)  
[17. Dropout, Weight Decay, and Noise as Teachers →](/courses/llm-mastery/17-regularization-dropout/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
