---
layout: course
title: "23. Positional Information: Absolute, Relative, RoPE"
permalink: /courses/llm-mastery/23-positional-embeddings/
course_track: "LLM Mastery"
description: "Attention is a bag-of-tokens operation by default. Position has to be smuggled in on purpose."
level: Intermediate
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-the-round-table-problem"
    label: "Mental model: the round table problem"
  - id: "worked-example-learned-absolute-embeddings"
    label: "Worked example: learned absolute embeddings"
  - id: "worked-example-rope-rotating-instead-of-adding"
    label: "Worked example: RoPE, rotating instead of adding"
  - id: "failure-mode-context-length-extrapolation"
    label: "Failure mode: context-length extrapolation"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 23/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

Self-attention, as derived in article 21, is permutation-equivariant: shuffle the input tokens and the outputs shuffle identically, because the operation is defined purely in terms of pairwise similarity between vectors, with no reference to *where* those vectors sit in the sequence. That's mathematically clean and practically useless for language, where "dog bites man" and "man bites dog" must not be treated as the same bag of tokens. Every transformer variant injects position information somewhere — the only real design question is *how*, and the answer has evolved for good, benchmarkable reasons.

## Mental model: the round table problem
{: #mental-model-the-round-table-problem }

Imagine a meeting where everyone can hear everyone else equally (that's attention) but nobody's wearing a name tag and there's no seating chart. You can still figure out *who said what and how it relates*, but you have no idea about order — who spoke first, who's sitting next to whom, which comment was a reply to which. Positional information is the seating chart handed out before the meeting starts. Without it, "the cat sat on the mat" and "the mat sat on the cat" produce the exact same set of query/key/value interactions — order lives entirely outside the attention operation itself, so it must be injected into the vectors before attention ever runs (absolute embeddings) or baked into the *comparison* between vectors (relative schemes like RoPE).

## Worked example: learned absolute embeddings
{: #worked-example-learned-absolute-embeddings }

The simplest fix, used in GPT-2: maintain a learned embedding table of shape `(max_seq_len, d_model)`, one row per position, and add it elementwise to the token embeddings before the first block:

```python
import torch

vocab_size, max_seq_len, d_model = 50257, 1024, 768
tok_emb = torch.nn.Embedding(vocab_size, d_model)
pos_emb = torch.nn.Embedding(max_seq_len, d_model)

idx = torch.randint(0, vocab_size, (2, 10))          # (B, T) token ids
positions = torch.arange(10).unsqueeze(0)            # (1, T) -> broadcasts over B

x = tok_emb(idx) + pos_emb(positions)                 # (B, T, d_model)
print(x.shape)  # torch.Size([2, 10, 768])
```

That's the entire mechanism: position 5 always gets the exact same learned vector added, regardless of what token sits there or how long the sequence is. It's cheap and it works, with one glaring limitation baked into the code above — `pos_emb` has exactly `max_seq_len` rows. Ask for position 1024 and you get an index error; there is no row for it, and no amount of training teaches the model what a position it has *never seen* should look like.

## Worked example: RoPE, rotating instead of adding
{: #worked-example-rope-rotating-instead-of-adding }

Rotary Position Embeddings (used in LLaMA, Mistral, Qwen, and most current open models) take a different approach entirely: instead of adding a position vector to the embedding, *rotate* each query and key vector by an angle proportional to its position, in a set of 2D subspaces:

```python
import torch

def rope_angles(head_dim, seq_len, base=10000.0):
    # one frequency per pair of dimensions
    freqs = 1.0 / (base ** (torch.arange(0, head_dim, 2).float() / head_dim))
    t = torch.arange(seq_len).float()
    angles = torch.outer(t, freqs)      # (seq_len, head_dim/2)
    return angles

def apply_rope(x, angles):
    # x: (..., seq_len, head_dim), split into even/odd pairs
    x1, x2 = x[..., ::2], x[..., 1::2]
    cos, sin = angles.cos(), angles.sin()
    rotated_even = x1 * cos - x2 * sin
    rotated_odd  = x1 * sin + x2 * cos
    out = torch.stack([rotated_even, rotated_odd], dim=-1).flatten(-2)
    return out

head_dim, seq_len = 8, 6
q = torch.randn(seq_len, head_dim)
angles = rope_angles(head_dim, seq_len)
q_rot = apply_rope(q, angles)
print(q_rot.shape)  # torch.Size([6, 8])
```

The payoff shows up in the dot product: when you rotate query at position `i` by angle `iθ` and key at position `j` by angle `jθ`, their dot product depends only on `(i - j)θ` — the *relative* distance, not the absolute positions. Slide both `i` and `j` forward by the same amount and attention scores between them are unchanged. That's exactly the invariance "dog bites man" needs and absolute embeddings can't give you: a phrase's internal structure should mean the same thing whether it appears at token 5 or token 5000.

## Failure mode: context-length extrapolation
{: #failure-mode-context-length-extrapolation }

Train a model with learned absolute embeddings up to `max_seq_len=1024`, then feed it a 2000-token prompt at inference time, and you either crash (index out of range) or, if someone patches around it by clamping/interpolating positions, get badly degraded outputs — the model never saw those position vectors during training and has no reason to handle them sensibly. RoPE softens this problem (it's defined for any position mathematically, not just ones seen during training) but doesn't eliminate it: attention patterns still degrade past the trained length because the *relative distance distribution* the model learned to expect shifts. This is precisely why "context length extension" techniques exist — position interpolation, YaRN, ABF — all of them rescaling RoPE's frequency base after the fact so a model trained at 4K can behave reasonably at 32K without retraining from scratch.

## Exercise
{: #exercise }

Take the `apply_rope` function above. Compute `q_rot` for a query vector at position `i=3` and a key vector at position `j=3` (identical position) versus a query at `i=3` and key at `j=103`. Compute the dot product `q_rot(i) · k_rot(j)` in both cases using the same original vector for query and key. Then repeat with query at `i=13, j=13` and `i=13, j=113` — same relative distances (0 and 100) but shifted by +10. Confirm the two dot-product pairs are equal, demonstrating relative-position invariance directly from the code rather than trusting the claim above.

---

[← 22. Multi-Head Attention](/courses/llm-mastery/22-multi-head-attention/)  
[24. Residuals and LayerNorm: The Stabilizers →](/courses/llm-mastery/24-layernorm-residuals/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
