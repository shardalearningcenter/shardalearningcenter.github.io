---
layout: course
title: "34. Mixed Precision Training"
permalink: /courses/llm-mastery/34-mixed-precision/
course_track: "LLM Mastery"
description: "Lower precision gives you speed and memory for free — but only if you actively manage the numerics it puts at risk."
level: Advanced
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-a-ruler-with-fewer-tick-marks"
    label: "Mental model: a ruler with fewer tick marks"
  - id: "worked-example-loss-scaling-in-code"
    label: "Worked example: loss scaling in code"
  - id: "why-bf16-mostly-sidesteps-the-problem"
    label: "Why bf16 mostly sidesteps the problem"
  - id: "failure-mode-silent-gradient-underflow"
    label: "Failure mode: silent gradient underflow"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 34/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

Training in fp16 or bf16 instead of fp32 roughly doubles memory bandwidth efficiency and unlocks tensor-core throughput that fp32 matmuls can't access on most hardware — real, substantial, essentially free speedup. But "free" undersells what's actually happening: you've reduced the number of bits used to represent every activation, weight, and gradient in the entire network, and some of those values — especially gradients, which can span many orders of magnitude — will get silently mangled by that reduced precision unless something actively compensates. Mixed precision training isn't "just cast everything to fp16 and hope"; it's a specific, carefully engineered protocol (fp16/bf16 compute, fp32 master weights, and for fp16 specifically, loss scaling) built precisely to capture the speedup while managing the numerical risk it introduces.

## Mental model: a ruler with fewer tick marks
{: #mental-model-a-ruler-with-fewer-tick-marks }

fp32 is a ruler with a tick mark every tiny fraction of a millimeter across an enormous range — plenty of resolution almost everywhere you'd ever need it. fp16 is a ruler with the *same total number* of tick marks compressed into a much smaller range: fewer exponent bits means the range of representable magnitudes shrinks dramatically (fp16's smallest positive normal number is around `6.1 × 10⁻⁵`; fp32's is around `1.2 × 10⁻³⁸`). Gradients late in a deep network's backward pass are frequently far smaller than that — not because they're meaningless, but because chain-rule multiplication through many layers naturally shrinks them. Measure something with a ruler whose smallest tick mark is bigger than the thing you're measuring, and you get zero, not "a small number." That's gradient underflow, and it's a direct consequence of fp16's *narrow range*, not its precision (number of significant digits) per se.

## Worked example: loss scaling in code
{: #worked-example-loss-scaling-in-code }

Loss scaling is the standard fix: multiply the loss by a large constant *before* backpropagating (which multiplies every gradient by that same constant, shifting them up into fp16's representable range), then divide the gradients back down by the same constant right before the optimizer step, after they've already survived the backward pass in a safe range:

```python
import torch

model = torch.nn.Linear(512, 512).cuda().half()  # fp16 weights
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
scaler = torch.cuda.amp.GradScaler()               # handles scale factor + skip-on-overflow

x = torch.randn(32, 512, device='cuda')
target = torch.randn(32, 512, device='cuda')

for step in range(100):
    optimizer.zero_grad()
    with torch.autocast(device_type='cuda', dtype=torch.float16):
        out = model(x)
        loss = torch.nn.functional.mse_loss(out, target)
    scaler.scale(loss).backward()   # scales loss up before backward
    scaler.step(optimizer)          # unscales gradients, checks for inf/nan, steps if safe
    scaler.update()                 # adjusts the scale factor for next iteration
```

`GradScaler` automates the whole dance: it picks a scale factor (often starting around `2^16`), multiplies the loss by it, unscales gradients before the optimizer step, and — critically — checks whether unscaling produced any `inf` or `nan` (a sign the scale factor was too aggressive and caused *overflow* in the other direction). If it did, that step is skipped entirely and the scale factor is reduced for next time; if many consecutive steps are clean, the scale factor is increased to push closer to fp16's usable range without wasting headroom. This dynamic adjustment is exactly why nobody hand-picks a fixed scale factor in practice — the "right" value depends on the specific model and even shifts over the course of training.

## Why bf16 mostly sidesteps the problem
{: #why-bf16-mostly-sidesteps-the-problem }

bf16 uses the same number of exponent bits as fp32 (8 bits) but fewer mantissa bits (7 versus fp32's 23) — it trades precision (fewer significant digits) for keeping fp32's *entire dynamic range* intact. That directly targets the actual problem described above: gradient underflow is a range problem, not a precision problem, and bf16's exponent range matches fp32's exactly, so the tiny-gradient-becomes-zero failure mode mostly disappears without needing loss scaling at all. This is precisely why essentially every modern LLM training run (LLaMA, GPT-NeoX, most open pretraining recipes since roughly 2022) defaults to bf16 over fp16 on hardware that supports it (A100s and later) — it captures nearly all of fp16's speed and memory benefit while sidestepping its most dangerous numerical failure mode, at the cost of coarser precision per value, which turns out to matter far less for training stability than range does.

## Failure mode: silent gradient underflow
{: #failure-mode-silent-gradient-underflow }

Train in fp16 with no loss scaling at all, and the failure is deceptively quiet: loss doesn't NaN, doesn't explode, doesn't obviously error — it just stalls, often at a plausible-looking value, because a meaningful fraction of small-but-real gradients silently rounded to exactly zero the moment they were cast to fp16, and "zero gradient" is indistinguishable from "the optimizer step for that parameter." A model with underflowing gradients in, say, its early embedding layers will show those specific parameters barely updating over thousands of steps while later layers train seemingly fine, producing a training curve that looks like normal (if slow) convergence right up until you compare final quality against an fp32 or bf16 baseline and find a real, unexplained gap. This is the exact failure loss scaling exists to prevent, and it's a compelling reason bf16 became the default the moment hardware supported it — the loss-scaling machinery above is real engineering effort spent entirely on working around fp16's narrow range, not a fundamental requirement of low-precision training itself.

## Exercise
{: #exercise }

fp16's smallest positive normal value is `2^-14 ≈ 6.1 × 10⁻⁵`. Suppose a specific gradient during backprop is `3 × 10⁻⁶` in true (fp32) value — smaller than that threshold, so it would underflow to zero if cast directly to fp16. Compute the minimum loss-scaling factor needed to push that gradient above fp16's underflow threshold before the cast (i.e., `gradient × scale_factor ≥ 6.1 × 10⁻⁵`). Then check: fp16's largest representable finite value is roughly `65504`. If a *different* gradient in the same backward pass is `10.0`, would your computed scale factor push that one into overflow? What does that tension tell you about why a single fixed scale factor can fail even when dynamically adjusted per-step?

---

[← 33. Training Parallelism: DDP, FSDP, Pipeline](/courses/llm-mastery/33-parallelism-ddp-fsdp/)  
[35. Evaluation: Beyond Vibes →](/courses/llm-mastery/35-eval-harness-thinking/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
