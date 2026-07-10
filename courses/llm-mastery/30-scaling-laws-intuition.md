---
layout: course
title: "30. Scaling Laws: The Bitter Lesson, Quantified"
permalink: /courses/llm-mastery/30-scaling-laws-intuition/
course_track: "LLM Mastery"
description: "Loss improves predictably with scale — until data or compute is misallocated."
level: Advanced
toc:
  - id: "the-empirical-story"
    label: "The empirical story"
  - id: "caveats"
    label: "Caveats"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 30/50** · Karpathy-style LLM course

Loss improves predictably with scale — until data or compute is misallocated.

## The empirical story
{: #the-empirical-story }

Bigger models + more data + more compute → better loss, often smoothly.

Chinchilla-style results: **match model size to data**; don’t starve either.

## Caveats
{: #caveats }

Benchmarks saturate. Contamination. Emergent jumps can be metric artifacts. Still, scale is the default strategy.

## Exercise
{: #exercise }

If you double parameters but keep data fixed, what risk do you invite?


---

[← 29. Batching, Throughput, and the Economics of Tokens](/courses/llm-mastery/29-batching-and-throughput/)  
[31. Tokenization Deep Dive: BPE Under the Hood →](/courses/llm-mastery/31-tokenization-deep-dive/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
