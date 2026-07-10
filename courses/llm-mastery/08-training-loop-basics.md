---
layout: course
title: "08. The Training Loop, End to End"
permalink: /courses/llm-mastery/08-training-loop-basics/
course_track: "LLM Mastery"
description: "Batch → forward → loss → backward → optimizer step. Repeat."
level: Beginner
toc:
  - id: "the-sacred-loop"
    label: "The sacred loop"
  - id: "batches"
    label: "Batches"
  - id: "checkpoints"
    label: "Checkpoints"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 8/50** · Karpathy-style LLM course

Batch → forward → loss → backward → optimizer step. Repeat.

## The sacred loop
{: #the-sacred-loop }

```python
for step in range(max_steps):
    x, y = get_batch()          # context, next-token targets
    logits = model(x)
    loss = cross_entropy(logits, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

Everything fancy (mixed precision, grad clip, LR schedules) decorates this loop. Don’t lose the plot.

## Batches
{: #batches }

We train on many sequences in parallel for GPU efficiency. Loss is averaged.

## Checkpoints
{: #checkpoints }

Save weights periodically. Training is long; disks are cheap; tears are expensive.

## Exercise
{: #exercise }

Write the training loop from memory without looking. Then check yourself.


---

[← 07. Neural Nets for Language: The MLP](/courses/llm-mastery/07-mlp-language-model/)  
[09. Overfitting, Underfitting, and Data →](/courses/llm-mastery/09-overfitting-underfitting/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
