---
layout: course
title: "04. Your First LM: Bigrams"
permalink: /courses/llm-mastery/04-bigram-language-model/
course_track: "LLM Mastery"
description: "Count pairs. Normalize. Sample. Feel the soul of language modeling."
level: Beginner
toc:
  - id: "the-smallest-interesting-model"
    label: "The smallest interesting model"
  - id: "what-you-learn"
    label: "What you learn"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 4/50** · Karpathy-style LLM course

Count pairs. Normalize. Sample. Feel the soul of language modeling.

## The smallest interesting model
{: #the-smallest-interesting-model }

A **bigram** model only conditions on the previous token:

```
P(t_i | t_{i-1})
```

Count how often `a` is followed by `b`. Divide by counts of `a`. Done.

```python
from collections import defaultdict, Counter

def train_bigrams(tokens):
    counts = defaultdict(Counter)
    for a, b in zip(tokens, tokens[1:]):
        counts[a][b] += 1
    return counts

def sample(counts, start, n=50):
    import random
    out = [start]
    for _ in range(n):
        dist = counts[out[-1]]
        if not dist:
            break
        toks, ws = zip(*dist.items())
        out.append(random.choices(toks, weights=ws, k=1)[0])
    return out
```

## What you learn
{: #what-you-learn }

Bigrams capture local habits (“q” → “u”) but can’t plan. Long-range structure needs more context — and eventually, neural nets.

## Exercise
{: #exercise }

Train character bigrams on a tiny text file. Sample 200 characters. Notice the local fluency and global nonsense.


---

[← 03. Next-Token Prediction Is the Game](/courses/llm-mastery/03-next-token-prediction/)  
[05. Loss: Cross-Entropy Without the Fear →](/courses/llm-mastery/05-loss-cross-entropy/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
