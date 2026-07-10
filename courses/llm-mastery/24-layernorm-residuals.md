---
layout: course
title: "24. Residuals and LayerNorm: The Stabilizers"
permalink: /courses/llm-mastery/24-layernorm-residuals/
course_track: "LLM Mastery"
description: "Depth doesn't work by default. Residuals give gradients a highway; norm keeps the traffic from exploding."
level: Intermediate
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-the-shared-whiteboard"
    label: "Mental model: the shared whiteboard"
  - id: "worked-example-variance-growth-without-norm"
    label: "Worked example: variance growth without norm"
  - id: "pre-norm-vs-post-norm"
    label: "Pre-norm vs post-norm"
  - id: "failure-mode-deep-post-norm-nets-refuse-to-train"
    label: "Failure mode: deep post-norm nets refuse to train"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 24/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

`x = x + SubLayer(x)` looks like a throwaway line, but it's the single change that made networks past ~20 layers trainable at all. Without it, gradients have to survive an unbroken chain of matrix multiplications and nonlinearities from loss back to layer 1, and in practice they either vanish toward zero or blow up toward infinity long before they get there. The residual connection gives every layer a direct, unimpeded path straight back to the loss — the gradient of `x + f(x)` with respect to `x` always contains an identity term, no matter how badly-scaled `f` is. LayerNorm's job is a separate, complementary problem: keeping the *scale* of activations sane as they accumulate across dozens of residual additions, so no single layer's contribution dominates or vanishes numerically.

## Mental model: the shared whiteboard
{: #mental-model-the-shared-whiteboard }

Don't think of a transformer as 96 layers passing a baton, each one replacing what the last one wrote. Think of it as 96 people taking turns at one shared whiteboard (the residual stream), each one allowed only to *add* a small edit — never erase, never overwrite. Attention adds "route information between these positions." The MLP adds "transform this position's content." Nothing after layer 1 can undo what layer 1 wrote; it can only append a correction on top. This is why residual-stream interpretability (looking at what accumulates in `x` layer by layer) is such a productive lens for understanding transformers — the object being built is genuinely cumulative, not a black box being replaced at each stage.

## Worked example: variance growth without norm
{: #worked-example-variance-growth-without-norm }

Simulate what happens to activation scale as you stack residual additions with no normalization at all:

```python
import torch

torch.manual_seed(0)
d = 768
x = torch.randn(1, d)

def fake_sublayer(x):
    # a linear layer with roughly unit-variance output, like an untrained block
    w = torch.randn(d, d) / d**0.5
    return x @ w

variances = [x.var().item()]
for layer in range(24):
    x = x + fake_sublayer(x)      # residual add, no norm
    variances.append(x.var().item())

print([round(v, 2) for v in variances[::4]])
```

Each residual add is roughly independent noise being summed, so variance grows layer over layer — roughly additively if each sublayer output has comparable variance to the running stream. By layer 24, activation scale has drifted far from where the network's weights were initialized to operate well (most init schemes assume roughly unit variance at every layer). Every downstream matmul, softmax, and loss computation is now operating outside the numerical range the model was designed for. This is not a hypothetical: it's the default behavior of residual stacks unless something actively intervenes, which is exactly what LayerNorm is there to do — renormalize the stream back to a controlled scale before (or after) each sublayer touches it.

## Pre-norm vs post-norm
{: #pre-norm-vs-post-norm }

The original "Attention Is All You Need" transformer normalized *after* each sublayer and residual add (post-norm): `x = LayerNorm(x + SubLayer(x))`. GPT-2 and essentially every LLM since switched to pre-norm: `x = x + SubLayer(LayerNorm(x))`. The difference matters enormously at depth. In post-norm, the residual stream itself passes through a normalization every layer, which means the "clean highway" for gradients described above gets partially obstructed — the identity path is no longer purely identity. In pre-norm, the raw residual stream `x = x + ...` is never itself normalized; only the *copy* fed into each sublayer is. The gradient highway stays completely unobstructed all the way from the final loss to the embedding layer, which is why pre-norm transformers train stably at 50+ layers where post-norm ones need careful learning-rate warmup and often fail outright past a certain depth.

## Failure mode: deep post-norm nets refuse to train
{: #failure-mode-deep-post-norm-nets-refuse-to-train }

If you build a 24+ layer post-norm transformer from scratch and skip a careful learning-rate warmup schedule, the classic symptom is loss that spikes to NaN in the first few hundred steps, or trains but plateaus far above where a shallower model would land — the gradient signal reaching early layers is too degraded by the repeated normalization-inside-the-residual-path to make useful updates. This is a documented, reproducible failure, not folklore: it's the concrete reason the field's default architecture moved to pre-norm, and it's why you'll see "warmup steps" as a near-universal hyperparameter in transformer training configs — it's compensating for exactly this instability during the first steps when the norm statistics haven't settled yet.

## Exercise
{: #exercise }

Rerun the variance-growth simulation above, but after every residual add, apply `x = (x - x.mean(-1, keepdim=True)) / (x.std(-1, keepdim=True) + 1e-5)` (a bare-bones LayerNorm, no learned scale/shift). Print variance every 4 layers as before. Confirm it stays near 1.0 across all 24 layers instead of drifting. Then explain in one sentence why pre-norm's version of this fix — normalizing the *input to each sublayer* rather than the *residual stream itself* — preserves the unobstructed gradient highway while post-norm's placement doesn't.

---

[← 23. Positional Information: Absolute, Relative, RoPE](/courses/llm-mastery/23-positional-embeddings/)  
[25. The Transformer MLP: Where Facts Often Live →](/courses/llm-mastery/25-mlp-in-transformer/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
