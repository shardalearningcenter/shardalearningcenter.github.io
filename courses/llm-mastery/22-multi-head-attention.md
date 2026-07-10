---
layout: course
title: "22. Multi-Head Attention"
permalink: /courses/llm-mastery/22-multi-head-attention/
course_track: "LLM Mastery"
description: "One attention pattern per layer is a bottleneck. Split the channels and let specialists form."
level: Intermediate
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-a-committee-not-a-bigger-brain"
    label: "Mental model: a committee, not a bigger brain"
  - id: "worked-example-the-reshape-that-creates-heads"
    label: "Worked example: the reshape that creates heads"
  - id: "what-heads-actually-learn"
    label: "What heads actually learn"
  - id: "failure-mode-the-silent-transpose-bug"
    label: "Failure mode: the silent transpose bug"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 22/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

A single attention head forces every token to compute one weighted average per layer, using one shared notion of "relevance." That's a bottleneck — language needs several simultaneous notions of relevance at once (this pronoun's referent, this bracket's match, this verb's subject). Multi-head attention doesn't add parameters to fix this; it *splits existing parameters* into `h` independent subspaces, runs attention separately in each, and concatenates the results. Same total compute and parameter count as one big head, radically more expressive because each head is forced to specialize.

## Mental model: a committee, not a bigger brain
{: #mental-model-a-committee-not-a-bigger-brain }

Picture `d_model=768` as one wide committee room. One-head attention makes everyone vote on a single question and average the results — mushy consensus. Multi-head attention splits the room into 12 smaller committees of 64 people each, gives each committee its *own* question (its own `Wq`, `Wk`, `Wv` slice), lets them deliberate independently, then reconvenes and reads out all 12 verdicts side by side before the next layer decides what to do with them. No committee sees what the others decided during their own deliberation — the mixing across heads only happens through the output projection at the end. That constraint is a feature: it's what forces specialization instead of 12 copies of the same behavior.

## Worked example: the reshape that creates heads
{: #worked-example-the-reshape-that-creates-heads }

The "split into heads" step is just a reshape and a transpose — no new math beyond article 21's single-head attention. Here's the shape-annotated version, which is the part people actually get wrong:

```python
import torch

B, T, C = 2, 5, 768   # batch, sequence length, model dim
n_head = 12
head_dim = C // n_head  # 64

x = torch.randn(B, T, C)
Wqkv = torch.nn.Linear(C, 3 * C, bias=False)

qkv = Wqkv(x)                      # (B, T, 3C)
q, k, v = qkv.split(C, dim=-1)     # each (B, T, C)

def to_heads(t):
    return t.view(B, T, n_head, head_dim).transpose(1, 2)  # (B, nh, T, hd)

q, k, v = to_heads(q), to_heads(k), to_heads(v)
print(q.shape)  # torch.Size([2, 12, 5, 64])

scores = q @ k.transpose(-2, -1) / head_dim**0.5   # (B, nh, T, T)
mask = torch.triu(torch.ones(T, T), diagonal=1).bool()
scores = scores.masked_fill(mask, float('-inf'))
attn = torch.softmax(scores, dim=-1)
out = attn @ v                                      # (B, nh, T, hd)

out = out.transpose(1, 2).contiguous().view(B, T, C)  # back to (B, T, C)
Wo = torch.nn.Linear(C, C, bias=False)
out = Wo(out)
print(out.shape)  # torch.Size([2, 5, 768])
```

The entire trick is `view(B, T, n_head, head_dim).transpose(1, 2)`: channel dimension `C` gets carved into `n_head` groups of `head_dim`, and then `T` and `n_head` swap places so attention (which operates over the `T, T` pair) batches cleanly over both `B` and `n_head` at once. Batched matmul does all 12 heads in parallel with zero extra Python.

## What heads actually learn
{: #what-heads-actually-learn }

This isn't hand-waving — interpretability work on GPT-2-scale models (see the "attention head" circuit analyses from Anthropic and Redwood Research) consistently finds specific heads doing specific jobs: "induction heads" that copy a token seen earlier after its predecessor repeats (the mechanism behind in-context learning), heads that track the previous token, heads that attend to the matching opening bracket, heads that resolve simple coreference. No two of these are the same computation, and they emerge purely from gradient descent on next-token prediction — nobody labels "bracket-matching head" during training.

## Failure mode: the silent transpose bug
{: #failure-mode-the-silent-transpose-bug }

The classic hand-rolled-attention bug: reshape straight to `(B, T, n_head, head_dim)` and forget the `.transpose(1, 2)`, or reshape to the wrong axis order like `(B, n_head, head_dim, T)`. The code still *runs* — shapes broadcast, matmuls complete, loss is a number — but you've silently scrambled which channels belong to which head, or mixed sequence position into the head dimension. Training usually still converges to *something*, just worse, because the network partially learns to route around your bug. This is the single most dangerous class of transformer bug: no crash, no NaN, just quietly worse loss that you'll blame on hyperparameters for a week before you diff your reshape against a reference implementation. The fix is discipline: after every reshape involving heads, print the shape and say out loud what each axis means.

## Exercise
{: #exercise }

`C = 768`, `n_head = 12`. What's `head_dim`? Now suppose someone hands you a checkpoint trained with `n_head = 16` on the same `C = 768` and you accidentally load it into a model configured for `n_head = 12`. The state dict shapes for `Wq`/`Wk`/`Wv`/`Wo` are identical (`768 × 768`) either way, so PyTorch's `load_state_dict` won't complain. Explain concretely, in terms of the reshape above, why the loaded model will still run forward passes without error but produce garbage output.

---

[← 21. Self-Attention Mechanics](/courses/llm-mastery/21-self-attention-mechanics/)  
[23. Positional Information: Absolute, Relative, RoPE →](/courses/llm-mastery/23-positional-embeddings/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
