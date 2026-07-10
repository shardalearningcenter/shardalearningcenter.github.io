---
layout: course
title: "13. Tensor Shapes: The Hidden Curriculum"
permalink: /courses/llm-mastery/13-tensors-shapes-discipline/
course_track: "LLM Mastery"
description: "The vast majority of transformer bugs are not modeling bugs — they are shape bugs wearing a modeling costume. Learn to think in B, T, C before you write a single layer."
level: Intermediate
toc:
  - id: "b-t-c-the-only-three-letters-that-matter"
    label: "B, T, C: the only three letters that matter"
  - id: "tracing-shapes-through-attention"
    label: "Tracing shapes through attention"
  - id: "broadcasting-is-a-feature-and-a-trap"
    label: "Broadcasting is a feature and a trap"
  - id: "failure-mode-the-silent-broadcast-bug"
    label: "Failure mode: the silent broadcast bug"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 13/50** · Karpathy-style LLM course

Nobody warns you about this in the marketing materials, but here's the truth from actually building these things: the majority of bugs in transformer code are not conceptual mistakes about attention or gradients. They are shape mismatches that either crash loudly or, worse, silently broadcast into the wrong answer and train a model that quietly learns garbage. Shape discipline is not pedantry. It is the debugging skill that separates people who ship models from people who file GitHub issues.

## B, T, C: the only three letters that matter
{: #b-t-c-the-only-three-letters-that-matter }

Every tensor flowing through a transformer language model can be described with three letters, and you should be able to name them for any tensor in your code without looking:

```
B = batch size        — how many independent sequences you're processing at once
T = time / sequence length — how many token positions
C = channels / d_model — the width of the representation at each position
```

The base activation tensor flowing through the residual stream is `(B, T, C)`. This is the one shape you should be able to recite in your sleep, because almost every layer takes it in and hands back the same shape — that's the entire point of a residual stream: each block *edits* a `(B, T, C)` tensor rather than reshaping it into something foreign.

```python
import torch
B, T, C = 4, 16, 64
x = torch.randn(B, T, C)
print(x.shape)  # torch.Size([4, 16, 64])
```

If you can't answer "what is B, T, and C right now" while stepping through a forward pass, you don't yet understand the code you're running — you're pattern-matching on tutorials. That's fine as a stage, but don't stop there.

## Tracing shapes through attention
{: #tracing-shapes-through-attention }

Self-attention introduces two more letters worth memorizing: `n_head` (number of attention heads) and `head_dim = C / n_head`. Trace the shapes explicitly:

```python
n_head = 8
head_dim = C // n_head  # 64 // 8 = 8

q = torch.randn(B, T, C)
k = torch.randn(B, T, C)
v = torch.randn(B, T, C)

# split C into (n_head, head_dim), then move heads before time
q = q.view(B, T, n_head, head_dim).transpose(1, 2)  # (B, n_head, T, head_dim)
k = k.view(B, T, n_head, head_dim).transpose(1, 2)  # (B, n_head, T, head_dim)
v = v.view(B, T, n_head, head_dim).transpose(1, 2)  # (B, n_head, T, head_dim)

scores = q @ k.transpose(-2, -1) / head_dim**0.5     # (B, n_head, T, T)
attn = torch.softmax(scores, dim=-1)                  # (B, n_head, T, T)
out = attn @ v                                        # (B, n_head, T, head_dim)

out = out.transpose(1, 2).contiguous().view(B, T, C)  # back to (B, T, C)
```

Every single line has a comment stating the resulting shape, and that is not decoration — it's how you should actually write this code the first ten times you write it. `scores` has shape `(B, n_head, T, T)` because it's an attention matrix per head: for every query position, a distribution of weight over every key position. That `T, T` block is why attention is quadratic in sequence length — it's not an abstract fact, it's staring at you in the shape.

## Broadcasting is a feature and a trap
{: #broadcasting-is-a-feature-and-a-trap }

NumPy and PyTorch broadcasting rules let tensors of different shapes combine without explicit expansion, by aligning shapes from the right and treating missing or size-1 dimensions as "stretch to match." This is what lets you add a bias vector of shape `(C,)` to an activation of shape `(B, T, C)` without writing a loop — the bias is broadcast across `B` and `T` automatically. It's genuinely useful, and also the source of an entire category of bugs where two tensors combine "successfully" (no crash) but mean two completely different things.

The rule to internalize: broadcasting compares shapes from the *trailing* dimension backward, and two dimensions are compatible if they're equal or one of them is 1. `(B, T, C)` and `(T, C)` broadcast fine (batch is implicitly repeated). `(B, T, C)` and `(B, C)` do **not** broadcast the way you probably want — PyTorch will either error, or worse, silently insert a mismatched dimension if you're not paying attention to *which* axis is size 1.

## Failure mode: the silent broadcast bug
{: #failure-mode-the-silent-broadcast-bug }

Here's the exact bug, in miniature, that has cost engineers entire debugging afternoons:

```python
attn_bias = torch.randn(T)          # intended: per-position bias, shape (T,)
scores = torch.randn(B, T, T)
scores = scores + attn_bias          # "works" — no error
```

This "works" because `attn_bias` of shape `(T,)` broadcasts against the *last* dimension of `scores`, adding the bias to every query row identically — which might be what you wanted, or might silently be wrong if you actually intended a per-query bias (shape `(T, 1)`) instead of a per-key bias. No error is raised. No warning is printed. The model trains — a little worse than it should, in a way you'll never diagnose from the loss curve alone.

The professional habit that catches this class of bug before it costs you a day: print `.shape` liberally while developing, and once code is stable, assert on shapes explicitly (`assert scores.shape == (B, T, T)`). Asserting shapes is not defensive over-engineering for a research prototype. It's the fastest, cheapest unit test you will ever write, and it will catch broadcast bugs at the exact line they happen instead of three layers downstream.

## Exercise
{: #exercise }

Given `B=2, T=8, C=32, n_head=4`, compute `head_dim` by hand, then verify: write the four-line attention shape trace above with these numbers, insert an `assert` after each reshape, and confirm every assert passes. Then deliberately break it — change `n_head` to 5 (which doesn't divide 32 evenly) and read the exact error PyTorch gives you. That error message is worth memorizing; it's the single most common crash in transformer code written by beginners.


---

[← 12. Micrograd Energy: Autograd From Scratch](/courses/llm-mastery/12-autograd-from-scratch/)  
[14. Softmax and Temperature, Carefully →](/courses/llm-mastery/14-softmax-temperature/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
