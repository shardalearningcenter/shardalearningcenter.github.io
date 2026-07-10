---
layout: course
title: "31. Tokenization Deep Dive: BPE Under the Hood"
permalink: /courses/llm-mastery/31-tokenization-deep-dive/
course_track: "LLM Mastery"
description: "Merge frequent pairs until vocab is full. That’s BPE."
level: Advanced
toc:
  - id: "algorithm-sketch"
    label: "Algorithm (sketch)"
  - id: "gotchas"
    label: "Gotchas"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 31/50** · Karpathy-style LLM course

Merge frequent pairs until vocab is full. That’s BPE.

## Algorithm (sketch)
{: #algorithm-sketch }

1. Start with character/byte vocab
2. Count adjacent pairs in corpus
3. Merge the most frequent pair into a new token
4. Repeat until vocab_size

## Gotchas
{: #gotchas }

Leading spaces, Unicode normalization, special tokens, domain shift (code vs prose).

## Exercise
{: #exercise }

Explain why “NotImplementedError” might be multiple tokens.


---

[← 30. Scaling Laws: The Bitter Lesson, Quantified](/courses/llm-mastery/30-scaling-laws-intuition/)  
[32. Pretraining Data: The Real Model →](/courses/llm-mastery/32-pretraining-data/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
