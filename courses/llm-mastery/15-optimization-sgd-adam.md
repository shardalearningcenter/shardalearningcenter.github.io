---
layout: course
title: "15. SGD, Adam, and Why Adam Won LLMs"
permalink: /courses/llm-mastery/15-optimization-sgd-adam/
course_track: "LLM Mastery"
description: "SGD moves downhill at one fixed speed for every parameter. Adam gives each parameter its own speed based on its own gradient history — and that per-parameter adaptivity is why it dominates LLM training."
level: Intermediate
toc:
  - id: "sgd-the-honest-baseline"
    label: "SGD: the honest baseline"
  - id: "momentum-remembering-where-you-were-heading"
    label: "Momentum: remembering where you were heading"
  - id: "adam-a-personal-learning-rate-per-parameter"
    label: "Adam: a personal learning rate per parameter"
  - id: "learning-rate-schedules-warmup-and-decay"
    label: "Learning rate schedules: warmup and decay"
  - id: "failure-mode-the-nan-that-was-actually-the-lr"
    label: "Failure mode: the NaN that was actually the LR"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 15/50** · Karpathy-style LLM course

Optimizers get treated like alchemy — pick the one with the best reputation, tune three knobs, hope. But the actual difference between SGD and Adam is a specific, nameable idea: SGD moves every parameter at the same speed; Adam gives each parameter its own speed, adapted to how noisy and how large that specific parameter's gradients have historically been. Once you see that, the choice stops being folklore.

## SGD: the honest baseline
{: #sgd-the-honest-baseline }

Vanilla stochastic gradient descent is one line:

```
θ ← θ - lr * grad
```

Every parameter moves in the direction that locally reduces the loss fastest, scaled by a single global learning rate. It's honest in the sense that there's nothing hidden — no moving averages, no adaptive state, just "go downhill, this fast." The problem is that "this fast" is almost never the right speed for *every* parameter simultaneously. A parameter with tiny, rarely-firing gradients (common in embedding rows for rare tokens) needs a bigger relative step than a parameter with large, constantly-firing gradients (common in early layers close to the loss), or it'll take forever to learn anything. SGD with a single learning rate can't tell these cases apart.

```python
def sgd_step(params, grads, lr=0.01):
    for p, g in zip(params, grads):
        p -= lr * g
```

## Momentum: remembering where you were heading
{: #momentum-remembering-where-you-were-heading }

Before jumping to Adam, the intermediate idea worth understanding is momentum: keep an exponential moving average of past gradients and step in *that* direction instead of the raw current gradient.

```
v ← β * v + (1 - β) * grad
θ ← θ - lr * v
```

This smooths out noisy, oscillating gradients (common in narrow ravines of the loss landscape) and lets the optimizer build up speed in a consistently good direction rather than zig-zagging. Momentum is real and helps, but it still applies the *same* learning rate to every parameter — it changes the direction of the step, not how differently-scaled parameters should be treated.

## Adam: a personal learning rate per parameter
{: #adam-a-personal-learning-rate-per-parameter }

Adam keeps two moving averages per parameter: `m` (mean of gradients, like momentum) and `v` (mean of *squared* gradients, tracking the typical magnitude of that parameter's gradient). The update divides by `sqrt(v)`, which means parameters with historically large gradients get their effective step size shrunk, and parameters with historically small gradients get their effective step size grown — every parameter is automatically rescaled to a roughly similar step magnitude, regardless of how differently scaled its raw gradients are.

```python
def adam_step(params, grads, state, lr=1e-3, b1=0.9, b2=0.999, eps=1e-8):
    state["t"] += 1
    t = state["t"]
    for i, (p, g) in enumerate(zip(params, grads)):
        state["m"][i] = b1 * state["m"][i] + (1 - b1) * g
        state["v"][i] = b2 * state["v"][i] + (1 - b2) * g**2
        m_hat = state["m"][i] / (1 - b1**t)   # bias correction
        v_hat = state["v"][i] / (1 - b2**t)   # bias correction
        params[i] -= lr * m_hat / (v_hat**0.5 + eps)
```

The bias correction terms (`1 - b1**t`, `1 - b2**t`) exist because `m` and `v` start at zero and are biased toward zero in the first few steps — without correction, the early updates would be artificially small. This is a real detail people skip when reimplementing Adam by hand, and it visibly changes early-training behavior on small models.

**AdamW** is the version almost every modern LLM actually trains with — it's Adam with weight decay applied directly to the parameters (`θ ← θ - lr * decay * θ`) *separately* from the gradient-based update, rather than folding decay into the gradient itself the way classic Adam does. Decoupling the two makes weight decay behave the way you'd intuitively expect (constant shrinkage toward zero) instead of interacting weirdly with Adam's adaptive scaling.

## Learning rate schedules: warmup and decay
{: #learning-rate-schedules-warmup-and-decay }

Even with Adam's per-parameter adaptivity, the *global* learning rate still needs a schedule, because Adam's moving averages (`m`, `v`) are unreliable in the first handful of steps — they haven't seen enough gradients yet to be a good estimate. LLM training recipes almost universally use **linear warmup** (ramp the learning rate up from ~0 over the first few hundred to few thousand steps) followed by **cosine decay** (smoothly ramp it back down toward zero over the rest of training). Warmup protects you from large, unreliable early updates; decay lets the model settle into a sharper minimum instead of bouncing around loudly near the end of training when precision matters most.

Too high a learning rate anywhere in this schedule and loss goes to `NaN`, often within a handful of steps of the spike. Too low and you burn compute making barely perceptible progress. There is no universal correct value — it depends on model size, batch size, and optimizer state — but the warmup-then-cosine-decay *shape* is close to universal across LLM training runs you'll read about.

## Failure mode: the NaN that was actually the LR
{: #failure-mode-the-nan-that-was-actually-the-lr }

A specific, recurring diagnostic trap: loss trains beautifully for a while, then spikes to `NaN` at some later step, and the instinct is to blame data (a bad batch, a corrupted example) or numerics (missing max-subtraction in softmax, covered in the previous article). Often, the real cause is that the learning rate — especially right after warmup ends, or right when a schedule transitions — was simply too aggressive for the current loss landscape, and one unlucky batch with a slightly larger-than-usual gradient pushed a parameter far enough that the *next* forward pass produces logits large enough to overflow.

The fix that catches most of these cases before they happen: **gradient clipping**, which caps the global norm of the gradient vector before the optimizer step is applied (`torch.nn.utils.clip_grad_norm_` in PyTorch, typically clipping to a norm of 1.0). Clipping doesn't fix a fundamentally too-high learning rate, but it absorbs the rare unlucky spike that would otherwise cascade into `NaN`, and it's cheap enough that most serious training loops apply it unconditionally.

## Exercise
{: #exercise }

In one paragraph, explain — in your own words, not the ones used above — why an *adaptive* per-parameter learning rate solves a problem that a single well-tuned global learning rate cannot, no matter how carefully you tune it. Concrete check: your answer should mention that different parameters can have gradients differing by orders of magnitude *within the same model at the same training step*, and that no single scalar learning rate can be simultaneously "large enough" for the small-gradient parameters and "small enough" for the large-gradient ones. If your explanation doesn't reference this per-parameter gradient-scale mismatch, you've described momentum, not adaptivity — go back and isolate what `v` (the squared-gradient moving average) is actually doing in the Adam update.


---

[← 14. Softmax and Temperature, Carefully](/courses/llm-mastery/14-softmax-temperature/)  
[16. Initialization Is Not Optional →](/courses/llm-mastery/16-initialization-matters/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
