---
layout: course
title: "18. RNNs: The Old Kings and Their Pain"
permalink: /courses/llm-mastery/18-rnns-and-their-pain/
course_track: "LLM Mastery"
description: "Recurrence is elegant and slow. Parallelism wants Transformers."
level: Intermediate
toc:
  - id: "the-idea"
    label: "The idea"
  - id: "why-we-moved-on"
    label: "Why we moved on"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 18/50** · Karpathy-style LLM course

Recurrence is elegant and slow. Parallelism wants Transformers.

## The idea
{: #the-idea }

Hidden state `h_t = f(h_{t-1}, x_t)`. Sequential by construction.

## Why we moved on
{: #why-we-moved-on }

- Hard to parallelize across time on GPUs
- Long-range gradients struggle (LSTM/GRU help, don’t solve)
- Transformers train faster at scale

Still worth knowing: sequential state is a clean mental model.

## Exercise
{: #exercise }

Name one strength RNNs still have vs vanilla Transformers.


---

[← 17. Dropout, Weight Decay, and Noise as Teachers](/courses/llm-mastery/17-regularization-dropout/)  
[19. Seq2Seq and the Dawn of Attention →](/courses/llm-mastery/19-seq2seq-attention-dawn/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
