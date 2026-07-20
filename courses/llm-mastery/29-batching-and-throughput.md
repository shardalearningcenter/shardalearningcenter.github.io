---
layout: course
title: "29. Batching, Throughput, and the Economics of Tokens"
permalink: /courses/llm-mastery/29-batching-and-throughput/
course_track: "LLM Mastery"
description: "Decode is bottlenecked on memory bandwidth, not compute. That single fact explains why batching is the entire game."
level: Advanced
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-highway-vs-toll-booth"
    label: "Mental model: highway vs. toll booth"
  - id: "worked-example-arithmetic-intensity"
    label: "Worked example: arithmetic intensity"
  - id: "continuous-batching-fixes-the-mismatch"
    label: "Continuous batching fixes the mismatch"
  - id: "failure-mode-padding-waste-and-the-batch-size-cliff"
    label: "Failure mode: padding waste and the batch-size cliff"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 29/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

An LLM decode step — generating one token, one KV-cache lookup at a time — has an unusual property: it moves an enormous amount of data (every weight in the model) to compute a comparatively tiny amount of arithmetic (a single token's worth of matmuls). That imbalance means decode is almost always bottlenecked by GPU *memory bandwidth*, not by GPU *compute (FLOPs)* — the GPU sits mostly idle waiting for weights to stream in from HBM, while its compute units, capable of trillions of FLOPs per second, do a comparatively trivial amount of work per byte moved. Batching multiple sequences' decode steps together doesn't reduce the bytes moved (same weights, read once), but it multiplies the compute done per byte, since you're now computing that token for `B` sequences simultaneously off the same weight read. That single lever — do more compute per weight-byte-read by batching — is most of what LLM inference serving engineering is about.

## Mental model: highway vs. toll booth
{: #mental-model-highway-vs-toll-booth }

Prefill (processing the initial prompt) is a wide-open highway: all `T` prompt tokens are known upfront and can be processed in parallel through matmuls that keep the GPU's compute units genuinely busy — this phase is compute-bound. Decode is a single-lane toll booth: exactly one new token per sequence per step, so no matter how fast the GPU's compute units are, they're waiting on the same "read every weight from memory" tax for a comparatively tiny amount of work. The toll booth doesn't get faster by making cars faster — it gets faster by letting several cars through per barrier-raise. That's batching: pack `B` sequences' decode steps into one weight read, and you've effectively opened `B` lanes through the same booth.

## Worked example: arithmetic intensity
{: #worked-example-arithmetic-intensity }

"Arithmetic intensity" is FLOPs performed per byte of memory moved — the number that tells you whether an operation is compute-bound or memory-bound on a given GPU. For a single-sequence decode step through a dense linear layer of shape `(d_in, d_out)`:

```python
d_in, d_out = 4096, 4096
dtype_bytes = 2  # fp16/bf16

flops = 2 * d_in * d_out            # one matmul, one token: 2*d_in*d_out
bytes_moved = d_in * d_out * dtype_bytes   # reading the weight matrix once

intensity = flops / bytes_moved
print(intensity)  # 1.0 FLOPs/byte
```

Modern GPUs (e.g. an A100) have a compute-to-bandwidth "ridge point" — the arithmetic intensity above which you're compute-bound — around 100+ FLOPs/byte for fp16 tensor-core math. An intensity of `1.0` is nowhere close; this operation is severely memory-bound, meaning the GPU's tensor cores are drastically underutilized while it waits on HBM reads. Now redo the calculation with a batch of `B=64` sequences sharing the same weight read:

```python
B = 64
flops_batched = 2 * d_in * d_out * B     # same weight, B tokens' worth of matmul
bytes_moved_batched = d_in * d_out * dtype_bytes   # weight read only once, still

intensity_batched = flops_batched / bytes_moved_batched
print(intensity_batched)  # 64.0 FLOPs/byte
```

`bytes_moved` didn't change — you still read the weight matrix exactly once — but `flops` scaled by `B`, so intensity scaled by `B` too, from `1.0` to `64.0`, much closer to the ridge point where the GPU's compute capacity actually gets used. This is the entire quantitative justification for batching decode requests: it's the only lever that increases arithmetic intensity without touching model size or hardware.

## Continuous batching fixes the mismatch
{: #continuous-batching-fixes-the-mismatch }

Naive batching waits for a fixed group of requests to all arrive, batches their prefill and decode together, and doesn't release any GPU slot until the *entire batch* finishes — even though different sequences in a chat workload finish at wildly different token counts (a one-word answer vs. a three-paragraph one). One long sequence in the batch holds every other slot hostage until it's done. Continuous batching (the technique behind vLLM, TensorRT-LLM, and most production serving stacks) instead treats each decode step as an opportunity to reshuffle the batch: finished sequences drop out immediately, newly arrived requests slot into the freed capacity, all without waiting for a batch boundary. The GPU stays near its achievable throughput ceiling continuously instead of oscillating between "fully packed" and "waiting for the slowest straggler."

## Failure mode: padding waste and the batch-size cliff
{: #failure-mode-padding-waste-and-the-batch-size-cliff }

Naive fixed-size batching pads every sequence in a batch to the length of the longest one, so a batch containing one 2000-token sequence and seven 50-token sequences pays full compute (and attention cost) for all eight as if they were 2000 tokens long — the seven short sequences spend nearly all their "processing" attending over pad tokens that contribute nothing. This is silent waste, not a crash: throughput numbers just come in far below what the hardware should support, and it's easy to misdiagnose as "the model is slow" rather than "the batching strategy is wasting >90% of the compute on padding." Separately, there's a real batch-size cliff: past a certain `B`, KV cache memory (article 28) for all sequences in the batch exceeds GPU memory, and you get an OOM crash rather than a graceful slowdown — arithmetic intensity gains from batching are capped by how much cache memory the GPU actually has, not by compute.

## Exercise
{: #exercise }

Using the arithmetic-intensity formula above, and an A100's published fp16 ridge point of roughly 140 FLOPs/byte (compute throughput ÷ memory bandwidth), compute the batch size `B` at which single-token decode through a `d_in=d_out=4096` linear layer crosses from memory-bound into compute-bound. Then explain, using article 28's cache-size formula, why you can't just keep increasing `B` to push intensity arbitrarily higher on a fixed GPU.

---

[← 28. KV Cache: Why Chat Is Fast After the First Token](/courses/llm-mastery/28-kv-cache/)  
[30. Scaling Laws: The Bitter Lesson, Quantified →](/courses/llm-mastery/30-scaling-laws-intuition/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
