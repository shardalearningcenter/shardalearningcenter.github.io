---
layout: course
title: "27. Implement a Tiny GPT (Conceptual Walkthrough)"
permalink: /courses/llm-mastery/27-implement-tiny-gpt/
course_track: "LLM Mastery"
description: "If you can write the shapes, you can write the model."
level: Advanced
toc:
  - id: "skeleton"
    label: "Skeleton"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 27/50** · Karpathy-style LLM course

If you can write the shapes, you can write the model.

## Skeleton
{: #skeleton }

```python
class CausalSelfAttention(nn.Module):
    ...

class Block(nn.Module):
    def __init__(self, cfg):
        ...
    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.mlp(self.ln2(x))
        return x

class GPT(nn.Module):
    def forward(self, idx, targets=None):
        # embed → blocks → ln → logits
        # optional loss
```

Fill the blanks with real code in your environment. Start with char-level Shakespeare.

## Exercise
{: #exercise }

Train until loss drops meaningfully. Sample. Celebrate ugly but real text.


---

[← 26. GPT Architecture: Decoder-Only Transformers](/courses/llm-mastery/26-gpt-architecture/)  
[28. KV Cache: Why Chat Is Fast After the First Token →](/courses/llm-mastery/28-kv-cache/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
