---
layout: course
title: "06. Embeddings: Meaning as Geometry"
permalink: /courses/llm-mastery/06-embeddings-intuition/
course_track: "LLM Mastery"
description: "Tokens live as vectors. Nearby vectors ≈ related usage."
level: Beginner
toc:
  - id: "lookup-tables-with-ambition"
    label: "Lookup tables with ambition"
  - id: "why-vectors"
    label: "Why vectors?"
  - id: "dimensionality"
    label: "Dimensionality"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 6/50** · Karpathy-style LLM course

Tokens live as vectors. Nearby vectors ≈ related usage.

## Lookup tables with ambition
{: #lookup-tables-with-ambition }

An embedding matrix `E` has shape `[vocab_size, dim]`. Token id `i` becomes row `E[i]` — a vector in R^d.

Training moves these vectors so that tokens used in similar contexts end up nearby (roughly).

## Why vectors?
{: #why-vectors }

Neural nets need continuous inputs. Discrete IDs don’t add or multiply meaningfully. Vectors do.

## Dimensionality
{: #dimensionality }

Small dim → underfit. Huge dim → expensive and data-hungry. Typical LLM dims: hundreds to thousands.

## Exercise
{: #exercise }

In your own words: what does it mean for two embedding vectors to be “close”?


---

[← 05. Loss: Cross-Entropy Without the Fear](/courses/llm-mastery/05-loss-cross-entropy/)  
[07. Neural Nets for Language: The MLP →](/courses/llm-mastery/07-mlp-language-model/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
