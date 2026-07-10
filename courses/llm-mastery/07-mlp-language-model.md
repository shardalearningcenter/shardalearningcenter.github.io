---
layout: course
title: "07. Neural Nets for Language: The MLP"
permalink: /courses/llm-mastery/07-mlp-language-model/
course_track: "LLM Mastery"
description: "Bengio’s classic: embed context → concatenate → MLP → softmax."
level: Beginner
toc:
  - id: "from-counts-to-parameters"
    label: "From counts to parameters"
  - id: "capacity-vs-context"
    label: "Capacity vs context"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 7/50** · Karpathy-style LLM course

Bengio’s classic: embed context → concatenate → MLP → softmax.

## From counts to parameters
{: #from-counts-to-parameters }

Instead of a giant count table, learn a function:

1. Take last `n` tokens
2. Embed each
3. Concatenate
4. Feed a multilayer perceptron
5. Softmax over vocabulary

This is the **neural probabilistic language model** lineage. Still local context, but shared parameters generalize better than raw counts.

## Capacity vs context
{: #capacity-vs-context }

MLP LMs struggle with long context because the input size grows with `n`, and there’s no clever reuse across positions yet. Transformers will fix that with attention.

## Exercise
{: #exercise }

If vocab=10k, n=3, dim=32, how big is the concatenated MLP input?


---

[← 06. Embeddings: Meaning as Geometry](/courses/llm-mastery/06-embeddings-intuition/)  
[08. The Training Loop, End to End →](/courses/llm-mastery/08-training-loop-basics/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
