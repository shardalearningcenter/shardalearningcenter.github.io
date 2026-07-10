---
layout: course
title: "19. Seq2Seq and the Dawn of Attention"
permalink: /courses/llm-mastery/19-seq2seq-attention-dawn/
course_track: "LLM Mastery"
description: "Attention began as “look at the source while decoding.”"
level: Intermediate
toc:
  - id: "encoderdecoder"
    label: "Encoder–decoder"
  - id: "attention-score"
    label: "Attention score"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 19/50** · Karpathy-style LLM course

Attention began as “look at the source while decoding.”

## Encoder–decoder
{: #encoderdecoder }

Encode source sentence to memory. Decode target tokens while attending to encoder states.

## Attention score
{: #attention-score }

For each decoder step, weight encoder positions by relevance. Soft alignment.

This idea — **content-based lookup over a set of vectors** — becomes the Transformer’s core when applied everywhere.

## Exercise
{: #exercise }

In translation, why is a single fixed vector bottleneck painful for long sentences?


---

[← 18. RNNs: The Old Kings and Their Pain](/courses/llm-mastery/18-rnns-and-their-pain/)  
[20. Reading 'Attention Is All You Need' Like an Engineer →](/courses/llm-mastery/20-attention-is-all-you-need-read/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
