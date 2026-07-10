---
layout: course
title: "28. KV Cache: Why Chat Is Fast After the First Token"
permalink: /courses/llm-mastery/28-kv-cache/
course_track: "LLM Mastery"
description: "Recomputing every past key and value on every new token is O(T²) generation. Cache them and pay O(T)."
level: Advanced
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-the-stenographer-who-never-relistens"
    label: "Mental model: the stenographer who never re-listens"
  - id: "worked-example-caching-by-hand"
    label: "Worked example: caching, by hand"
  - id: "the-memory-cost-is-not-free"
    label: "The memory cost is not free"
  - id: "failure-mode-forgetting-the-cache-invalidates-on-a-changed-prefix"
    label: "Failure mode: forgetting the cache invalidates on a changed prefix"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 28/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

Naive autoregressive generation recomputes attention over the *entire* sequence from scratch at every single new token: to generate token 500, you feed all 500 tokens through the model again, even though tokens 1 through 499 produced identical keys and values the last four hundred and ninety-nine times you computed them. That's `O(T²)` total work to generate a `T`-token sequence, and essentially all of it is redundant, because keys and values for a given position only depend on that position's input, which never changes once it's been through the model. The KV cache is the fix: compute each position's key and value vectors exactly once, store them, and on every subsequent step only compute the new token's query, key, and value, attending the new query against the *cached* keys and values from everything before it. Generation drops to `O(T)` total work — linear instead of quadratic.

## Mental model: the stenographer who never re-listens
{: #mental-model-the-stenographer-who-never-relistens }

Imagine transcribing a meeting where, every time someone says a new sentence, you insist on replaying the entire meeting recording from the start to "make sure you have full context," instead of just keeping your existing notes and listening to the new sentence. That's naive generation. A competent stenographer keeps running notes (the cache) and only processes the newest input each time, referring back to notes rather than re-listening to the whole recording. The notes — the keys and values — are exactly the information attention needs from the past; nothing about "understanding" the earlier sentences requires re-hearing them, only having their summary (K, V) available to compare against.

## Worked example: caching, by hand
{: #worked-example-caching-by-hand }

Here's single-head causal attention with an explicit cache, generating token by token:

```python
import torch

d_k = 16

def project(x, Wq, Wk, Wv):
    return x @ Wq, x @ Wk, x @ Wv

Wq, Wk, Wv = torch.randn(8, d_k), torch.randn(8, d_k), torch.randn(8, d_k)

cache_k, cache_v = None, None

def step(x_new):                                     # x_new: (1, 8) — one token's embedding
    global cache_k, cache_v
    q_new = x_new @ Wq                                # (1, d_k) — only the new query
    k_new = x_new @ Wk                                # (1, d_k)
    v_new = x_new @ Wv                                # (1, d_k)

    cache_k = k_new if cache_k is None else torch.cat([cache_k, k_new], dim=0)
    cache_v = v_new if cache_v is None else torch.cat([cache_v, v_new], dim=0)

    scores = q_new @ cache_k.T / d_k**0.5             # (1, T_so_far)
    weights = torch.softmax(scores, dim=-1)
    out = weights @ cache_v                           # (1, d_k)
    return out

for t in range(5):
    x_new = torch.randn(1, 8)
    out = step(x_new)
    print(t, cache_k.shape, out.shape)
```

Watch `cache_k.shape` grow by one row per call: `(1, 16)`, `(2, 16)`, `(3, 16)` ... At no point does `step` recompute a key or value for any earlier position — it only ever computes `k_new`/`v_new` for the single new token, then appends. The query is *never* cached, because a fresh query is needed every step; only keys and values, which are reused by every future step's attention, are worth storing.

## The memory cost is not free
{: #the-memory-cost-is-not-free }

The KV cache trades compute for memory, and at long context lengths the memory side becomes the actual bottleneck for serving. The formula: `2 (K and V) × n_layer × n_head × head_dim × T × dtype_bytes`, per sequence. Plug in a realistic 7B-class config — `n_layer=32`, `n_head=32`, `head_dim=128`, `T=4096`, fp16 (`2` bytes):

```
2 × 32 × 32 × 128 × 4096 × 2 bytes
= 2 × 32 × 32 × 128 × 4096 × 2
= 2,147,483,648 bytes ≈ 2.0 GB
```

Two gigabytes, *per sequence*, just for the cache, before you've loaded a single model weight. Serve 32 concurrent 4096-token conversations and the cache alone needs 64 GB — this is precisely why long-context serving is dominated by KV-cache memory management (paged attention, cache eviction, multi-query/grouped-query attention to shrink `n_head` for K/V specifically) rather than by raw compute. The cache isn't an implementation detail; at scale it's the resource constraint that shapes how inference servers are architected.

## Failure mode: forgetting the cache invalidates on a changed prefix
{: #failure-mode-forgetting-the-cache-invalidates-on-a-changed-prefix }

The cache is only valid because keys and values are a pure function of that position's *input up to and including itself* — nothing later ever changes them (that's exactly what the causal mask from article 21 guarantees). Break that assumption and the cache silently lies to you: edit any token in the prefix after you've already cached it (a common bug in chat servers doing prompt-prefix reuse across turns, or speculative decoding implementations that roll back a rejected draft token without invalidating its cache entries), and every subsequent generation step attends against stale keys/values that no longer correspond to the actual current prefix. Nothing crashes — attention runs, softmax normalizes, a plausible-looking token comes out — but it's plausible-looking garbage conditioned on a prefix that technically doesn't exist anymore. This is why cache invalidation logic in serving frameworks is written so defensively: any prefix mutation must either recompute the cache from that point forward or the whole cache is worthless.

## Exercise
{: #exercise }

Using the formula above, compute the KV cache size in GB for `T=32768` (a 32K context window) at the same 7B-class config (`n_layer=32, n_head=32, head_dim=128`, fp16). Then recompute it assuming grouped-query attention with only `n_head_kv=8` distinct K/V heads shared across the 32 query heads (a technique used in LLaMA-2 70B and most current open models specifically to shrink this number). Report both totals and the ratio between them.

---

[← 27. Implement a Tiny GPT (Conceptual Walkthrough)](/courses/llm-mastery/27-implement-tiny-gpt/)  
[29. Batching, Throughput, and the Economics of Tokens →](/courses/llm-mastery/29-batching-and-throughput/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
