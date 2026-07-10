---
layout: course
title: "05. Loss: Cross-Entropy Without the Fear"
permalink: /courses/llm-mastery/05-loss-cross-entropy/
course_track: "LLM Mastery"
description: "Cross-entropy is just “how surprised was the model by the true next token?”"
level: Beginner
toc:
  - id: "intuition"
    label: "Intuition"
  - id: "softmax"
    label: "Softmax"
  - id: "why-we-care"
    label: "Why we care"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 5/50** · Karpathy-style LLM course

Cross-entropy is just “how surprised was the model by the true next token?”

## Intuition
{: #intuition }

If the model puts probability `p` on the correct next token, the loss for that step is `-log(p)`.

- `p = 1.0` → loss 0 (perfect)
- `p = 0.5` → loss ~0.69
- `p → 0` → loss → ∞ (very bad)

Average over the dataset. That’s training.

## Softmax
{: #softmax }

The network outputs raw scores (logits). Softmax turns them into a probability distribution. Cross-entropy then compares that distribution to a one-hot (the true token).

## Why we care
{: #why-we-care }

Lower loss ≈ better compression of the training text ≈ usually better samples. Not always identical to “usefulness,” but it’s the right north star for pretraining.

## Exercise
{: #exercise }

If a model assigns 0.1 to the correct token, what’s the per-token loss? (Use natural log.)


---

[← 04. Your First LM: Bigrams](/courses/llm-mastery/04-bigram-language-model/)  
[06. Embeddings: Meaning as Geometry →](/courses/llm-mastery/06-embeddings-intuition/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
