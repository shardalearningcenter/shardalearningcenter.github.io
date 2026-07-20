---
layout: course
title: "33. Training Parallelism: DDP, FSDP, Pipeline"
permalink: /courses/llm-mastery/33-parallelism-ddp-fsdp/
course_track: "LLM Mastery"
description: "DDP replicates the model and syncs gradients — it does nothing for memory. FSDP shards the model itself, which is the actual constraint at scale."
level: Advanced
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-more-hands-vs-a-bigger-desk"
    label: "Mental model: more hands vs. a bigger desk"
  - id: "worked-example-memory-per-gpu-under-each-scheme"
    label: "Worked example: memory per GPU under each scheme"
  - id: "pipeline-and-tensor-parallelism-splitting-the-graph-itself"
    label: "Pipeline and tensor parallelism: splitting the graph itself"
  - id: "failure-mode-duplicated-data-across-ranks"
    label: "Failure mode: duplicated data across ranks"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 33/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

Distributed Data Parallel (DDP) solves exactly one problem: not enough *compute* on one GPU. It replicates the entire model on every GPU, splits the batch across them, and averages gradients via all-reduce after the backward pass — every GPU still holds a full, complete copy of every parameter, gradient, and optimizer state. That means DDP does absolutely nothing to help when the actual constraint is *memory*: a model too large to fit on a single GPU in the first place, or one that fits but leaves no room for a large enough batch or optimizer state. That's a fundamentally different problem, and it needs a fundamentally different solution — sharding the model itself across GPUs so no single one ever holds the whole thing. That's what FSDP (Fully Sharded Data Parallel) and its predecessor ZeRO are for. Conflating "more GPUs for more compute" with "more GPUs because it doesn't fit" is the single most common confusion in this topic, and the fix in each case is a completely different piece of infrastructure.

## Mental model: more hands vs. a bigger desk
{: #mental-model-more-hands-vs-a-bigger-desk }

DDP is hiring more people, each with their own complete copy of the same reference book, to grade more homework in parallel and then average their notes — great for throughput, useless if the book itself doesn't fit on any one person's desk. FSDP is instead ripping that one book into chapters and giving each person only their chapter, trusting them to fetch a neighbor's chapter for the few minutes they actually need it (during the forward/backward pass touching that chapter's parameters) and hand it right back afterward. No single desk ever needs to hold the entire book, which is exactly the property you need once "the model" and "one GPU's memory" stop being comparable sizes.

## Worked example: memory per GPU under each scheme
{: #worked-example-memory-per-gpu-under-each-scheme }

For a model with `P` parameters trained with Adam in mixed precision, memory per GPU is dominated by: parameters (fp16, `2P` bytes), gradients (fp16, `2P` bytes), and Adam's optimizer states — fp32 master weights, momentum, and variance, `4P` bytes each, `12P` total. That's `16P` bytes of "model state" per GPU under plain DDP, since every GPU holds a full copy:

```python
def ddp_memory_per_gpu(P):
    return 16 * P  # bytes: full replica everywhere, independent of N_gpus

def fsdp_memory_per_gpu(P, N_gpus, stage=3):
    # stage 1: shard optimizer states only
    # stage 2: shard optimizer states + gradients
    # stage 3: shard optimizer states + gradients + parameters (full FSDP)
    if stage == 1:
        return 4 * P + (12 * P) / N_gpus
    if stage == 2:
        return 2 * P + (14 * P) / N_gpus
    return (16 * P) / N_gpus  # stage 3 / full FSDP

P = 70e9  # a 70B-parameter model
N_gpus = 64

print(ddp_memory_per_gpu(P) / 1e9, "GB per GPU under plain DDP")
print(fsdp_memory_per_gpu(P, N_gpus, stage=3) / 1e9, "GB per GPU under full FSDP")
```

Plain DDP: `16 × 70e9 = 1,120e9` bytes ≈ 1120 GB per GPU — nowhere close to fitting on any real accelerator, meaning DDP alone simply cannot train this model regardless of how many GPUs you throw at the *compute* side. Full FSDP across 64 GPUs: `1120e9 / 64 ≈ 17.5` GB per GPU for model state — suddenly plausible on an 80GB accelerator, with room left for activations and a reasonable batch size. The sharding is what makes the difference, not the number of GPUs per se — DDP with 1000 GPUs still needs 1120 GB per GPU for this model; FSDP with 8 GPUs already gets you to 140 GB per GPU, a meaningfully different regime.

## Pipeline and tensor parallelism: splitting the graph itself
{: #pipeline-and-tensor-parallelism-splitting-the-graph-itself }

FSDP shards *state* (params/grads/optimizer) but each GPU still runs the *entire* forward and backward computation graph, temporarily reassembling the full parameters it needs layer by layer. Pipeline parallelism instead splits the model's *layers* across GPUs — GPU 0 holds layers 1–8, GPU 1 holds layers 9–16, and activations physically travel between GPUs as data flows through the stack, at the cost of "bubble" idle time while later stages wait for earlier ones. Tensor parallelism goes further, splitting *individual* large matrix multiplications (a single attention or MLP weight matrix) across GPUs, requiring communication *within* a single layer's forward pass rather than just between layers. Frontier-scale training (GPT-4-class, Llama-3-405B-class) typically combines all of these — data parallelism across groups of GPUs, tensor parallelism within a fast-interconnect node, pipeline parallelism across nodes — because no single technique alone solves both the compute and the memory constraint at that scale.

## Failure mode: duplicated data across ranks
{: #failure-mode-duplicated-data-across-ranks }

DDP's correctness depends entirely on every rank (GPU process) seeing a genuinely *different* shard of the training data each step — that's the entire point of splitting the batch. Forget to wrap your dataloader with `DistributedSampler` (or its equivalent) and every rank independently shuffles and iterates the *full* dataset from the start, meaning every rank processes largely the same examples in roughly the same order. Nothing crashes. Training proceeds, loss goes down, and it looks completely normal in the loss curve — but you're paying for `N` GPUs' worth of compute while getting the effective batch diversity of one, since the "parallel" data is heavily duplicated across ranks rather than genuinely distinct. This bug is specifically insidious because there is no error message anywhere in the stack to catch it; the only tell is throughput and final model quality quietly underperforming what the GPU count should deliver, which people routinely misattribute to hyperparameters instead of a dataloader misconfiguration.

## Exercise
{: #exercise }

Using the memory formulas above, compute the per-GPU memory for a 13B-parameter model under (a) plain DDP, (b) ZeRO/FSDP stage 1, (c) stage 2, (d) stage 3, all at `N_gpus=8`. Identify the smallest `N_gpus` at which full FSDP (stage 3) brings a 13B model's per-GPU memory footprint under 24 GB — the memory of a consumer-class GPU — and state whether that number seems achievable on commodity hardware, given you also need memory for activations on top of the model state computed here.

---

[← 32. Pretraining Data: The Real Model](/courses/llm-mastery/32-pretraining-data/)  
[34. Mixed Precision Training →](/courses/llm-mastery/34-mixed-precision/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
