---
layout: course
title: "37. LoRA and Parameter-Efficient Fine-Tuning"
permalink: /courses/llm-mastery/37-lora-peft/
course_track: "LLM Mastery"
description: "You don't need to touch every weight to change model behavior — a rank-8 detour around the matrix is often enough."
level: Advanced
toc:
  - id: "idea"
    label: "Idea"
  - id: "parameter-math"
    label: "The parameter math"
  - id: "failure-mode"
    label: "Failure mode"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 37/50** · Karpathy-style LLM course

Full fine-tuning of a 7B model means updating 7 billion numbers, storing optimizer state for each, and checkpointing a full new copy of the model for every task you care about. LoRA (Low-Rank Adaptation) gets you most of the benefit while touching a fraction of a percent of the parameters — and its central bet, that task adaptation lives in a low-dimensional subspace, turned out to be right often enough to become the default.

## Idea
{: #idea }

Full fine-tune: `W → W + ΔW`, where `ΔW` is the same shape as `W` — a dense update over every entry. LoRA instead freezes `W` and adds an adapter constrained to low rank: `ΔW ≈ B @ A`, where `A` is `r × d_in`, `B` is `d_out × r`, and `r` is small (often 4–64) relative to `d_in`, `d_out`.

```python
import torch, torch.nn as nn

class LoRALinear(nn.Module):
    def __init__(self, base: nn.Linear, r: int = 8, alpha: int = 16):
        super().__init__()
        self.base = base
        for p in self.base.parameters():
            p.requires_grad = False
        d_out, d_in = base.weight.shape
        self.A = nn.Parameter(torch.randn(r, d_in) * 0.01)
        self.B = nn.Parameter(torch.zeros(d_out, r))
        self.scale = alpha / r

    def forward(self, x):
        return self.base(x) + self.scale * (x @ self.A.T @ self.B.T)
```

`B` starts at zero, so `x @ A.T @ B.T` is exactly zero on step one — the adapter is a no-op until gradients pull it somewhere useful. That's a deliberate design choice, not an accident: it guarantees fine-tuning starts from a model that behaves identically to the base checkpoint, then edits from there.

## The parameter math
{: #parameter-math }

For a 4096×4096 attention projection with `r=8`:

- Full fine-tune: 4096 × 4096 ≈ 16.8M trainable params, for that one matrix.
- LoRA: `A` is 8×4096 = 32,768, `B` is 4096×8 = 32,768. Total ≈ 65,536.

That's **256× fewer trainable parameters** for that matrix, and the ratio only improves as the base matrix gets bigger — LoRA cost grows linearly with `d`, full fine-tuning grows quadratically. Apply it to attention Q/K/V/O projections across a 32-layer model and you're typically fine-tuning under 1% of total weights, with an Adam optimizer state (two moment buffers) that's correspondingly under 1% the size. That's the difference between fine-tuning on a single consumer GPU and needing a cluster.

## Failure mode
{: #failure-mode }

LoRA fails quietly, not loudly — you get a model that trains without errors and is just... mediocre. Three usual suspects:

- **Rank too small for the task.** `r=4` might be plenty for a narrow style adapter, hopeless for teaching a genuinely new skill across many domains. If validation loss plateaus higher than a full fine-tune's, double `r` before touching anything else.
- **Adapting the wrong modules.** Bolting LoRA only onto attention projections and skipping the MLP layers misses where a lot of factual and associative knowledge actually lives (see article 25). If your task is knowledge-heavy rather than style-heavy, adapt the MLP too.
- **Mistuned alpha/r ratio.** `scale = alpha / r` sets the adapter's effective learning-rate multiplier. Change `r` without adjusting `alpha` and you silently change how strongly the adapter can perturb the base model — a classic "tuned one hyperparameter, forgot it was coupled to another" bug.

Full fine-tuning still wins when you have the compute and data and need to move the model *further* than a low-rank detour can reach — think base-capability shifts, not persona or format shifts.

There's a second, less obvious payoff: because the base weights never change, you can keep dozens of task-specific adapters — each a few tens of megabytes — and swap them into the same loaded base model at request time. That's the difference between hosting one fine-tune per customer on separate GPUs and hosting one base model with a folder of adapters, which is why LoRA shows up as much in serving architecture diagrams as it does in training scripts.

## Exercise
{: #exercise }

A model has 32 transformer layers. Each layer applies LoRA (`r=8`, `alpha=16`) to four projections — Q, K, V, O — each of shape 4096×4096. Compute the total number of trainable LoRA parameters across the whole model, and compare it to the model's total parameter count (roughly 7B for a model this shape). What percentage of the model is trainable? Then answer: if you doubled `r` to 16 without changing `alpha`, what happens to the adapter's effective contribution at initialization, and why doesn't it matter that `B` starts at zero either way?


---

[← 36. Supervised Fine-Tuning (SFT)](/courses/llm-mastery/36-finetuning-sft/)  
[38. Preferences: RLHF and DPO →](/courses/llm-mastery/38-preference-rlhf-dpo/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
