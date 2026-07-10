---
layout: course
title: "16. Initialization Is Not Optional"
permalink: /courses/llm-mastery/16-initialization-matters/
course_track: "LLM Mastery"
description: "Initialization is a variance-control problem, not a superstition. Get the scale wrong and either every activation dies at zero or every activation explodes — before the optimizer takes a single useful step."
level: Intermediate
toc:
  - id: "the-actual-goal-constant-variance-with-depth"
    label: "The actual goal: constant variance with depth"
  - id: "deriving-why-1-sqrtn-shows-up"
    label: "Deriving why 1/sqrt(n) shows up"
  - id: "kaiming-vs-xavier-in-one-sentence-each"
    label: "Kaiming vs Xavier, in one sentence each"
  - id: "the-day-0-loss-sanity-check"
    label: "The day-0 loss sanity check"
  - id: "failure-mode-symmetric-init-that-never-breaks-symmetry"
    label: "Failure mode: symmetric init that never breaks symmetry"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 16/50** · Karpathy-style LLM course

Initialization looks like a footnote — one line of code before the "real" training loop starts — but it decides whether that training loop ever has a chance. Get the initial scale of your weights wrong and you don't get a slightly worse model; you get activations that are either all zero or all `inf` before a single gradient step has meaningfully updated anything.

## The actual goal: constant variance with depth
{: #the-actual-goal-constant-variance-with-depth }

Here's the concrete quantity you're controlling: the **variance of activations** as signal passes through layer after layer. If each layer's weights are scaled so that its output variance is systematically larger than its input variance, that multiplicative effect compounds with depth — by layer 20 your activations are astronomically large, `exp()` inside any softmax overflows, and you get `NaN` before training even properly starts. If each layer shrinks variance instead, activations collapse toward zero by some depth, gradients through them vanish (article 11's problem, reappearing at initialization time instead of during training), and the network effectively can't learn because there's no signal left to learn from.

The goal of a good initialization scheme is boring and precise: choose the initial weight scale so that, *on average, at initialization*, the variance of a layer's output roughly equals the variance of its input. Not smaller, not larger. Just preserved.

## Deriving why 1/sqrt(n) shows up
{: #deriving-why-1-sqrtn-shows-up }

Consider one output neuron of a linear layer: `y = sum(w_i * x_i)` over `n` inputs. If the `x_i` are independent with variance `Var(x)`, and the `w_i` are independent with mean 0 and variance `Var(w)`, then by basic properties of variance of a sum of independent products:

```
Var(y) = n * Var(w) * Var(x)
```

For `Var(y)` to equal `Var(x)` — the "preserve variance" goal — you need `n * Var(w) = 1`, so `Var(w) = 1/n`, which means the standard deviation of your weights should be `1/sqrt(n)`. That's the entire derivation behind the ubiquitous `1/sqrt(fan_in)` scaling you see in almost every initialization scheme. It isn't a magic constant somebody discovered empirically — it falls directly out of demanding that variance doesn't compound with depth.

```python
import numpy as np

def linear_init(fan_in, fan_out):
    std = 1.0 / np.sqrt(fan_in)
    return np.random.randn(fan_in, fan_out) * std

W = linear_init(512, 512)
x = np.random.randn(1000, 512)  # 1000 samples, dim 512, unit variance
y = x @ W
print(x.var(), y.var())  # should both be close to 1.0
```

## Kaiming vs Xavier, in one sentence each
{: #kaiming-vs-xavier-in-one-sentence-each }

**Xavier/Glorot init** balances the variance-preservation derivation above for *both* the forward pass and the backward pass simultaneously (since backward gradients flow through the transpose of the weight matrix, which has `fan_out` playing the role `fan_in` played forward), landing on `std = sqrt(2 / (fan_in + fan_out))` as a compromise — appropriate for symmetric activations like `tanh` where the derivation above holds cleanly.

**Kaiming/He init** corrects the same derivation for **ReLU**, which zeroes out roughly half its inputs (everything negative), effectively halving the variance an ReLU layer passes through compared to what the linear-algebra-only derivation predicts. Kaiming compensates by doubling the variance target: `std = sqrt(2 / fan_in)`. That factor of 2 is not arbitrary — it's the exact correction for "half the signal gets zeroed by the nonlinearity," derived the same way you derived `1/sqrt(n)` above, just accounting for ReLU's effect on the output variance.

The practical rule: match your init scheme to your nonlinearity. Using Xavier init with ReLU networks systematically under-scales weights and slowly shrinks activation variance with depth — a subtle version of the vanishing problem that shows up as unexpectedly slow early training rather than an outright crash.

## The day-0 loss sanity check
{: #the-day-0-loss-sanity-check }

Before you trust any training run, check the loss at step 0, before any optimizer step. For a classification or next-token-prediction task with `V` classes/vocab and a reasonably initialized network, the model's output distribution at step 0 should be close to uniform (since the last layer's logits should be small in magnitude if initialized correctly), which means the expected cross-entropy loss should be close to `-log(1/V) = log(V)`.

```python
import math
V = 50000  # example vocab size
expected_day0_loss = math.log(V)
print(expected_day0_loss)  # ~10.8
```

If your measured day-0 loss is wildly higher than `log(V)`, some layer's initialization (or the network's overall architecture) is producing an overconfident, badly-wrong initial distribution — a real, checkable symptom, not a vague feeling that something's off. If it's `NaN` or absurdly large, you almost certainly have an initialization-scale explosion happening before training even starts. This single check — comparing measured day-0 loss to `log(V)` — catches a surprising fraction of "my model won't train" bug reports, and it takes ten seconds to run.

## Failure mode: symmetric init that never breaks symmetry
{: #failure-mode-symmetric-init-that-never-breaks-symmetry }

The most dramatic and instructive initialization failure: set every weight in a layer to exactly zero (or any single constant value). Every neuron in that layer computes the exact same output for the exact same input, because they have identical weights. During backprop, every neuron in that layer receives the exact same gradient too, for the same reason — the chain rule doesn't care about position, only about the computation, and identical weights mean identical local derivatives. The result is that every neuron in the layer updates identically forever; you effectively have a layer with one useful neuron's worth of capacity, duplicated `n` times, no matter how wide you make it. This is called the **symmetry-breaking problem**, and it's why initialization must be *random*, not merely "small" — small-but-identical is just as broken as large-but-identical.

Biases, by contrast, are conventionally initialized to zero and this is fine, because the weights connecting to different neurons are already random, which is enough asymmetry to break the symmetry problem; the bias just needs a reasonable starting offset, and zero is a perfectly reasonable one.

## Exercise
{: #exercise }

What happens to a deep, fully-connected ReLU network if every weight (not just one layer) is initialized to exactly zero? Trace it layer by layer: what is the output of layer 1, and therefore the input to layer 2, and so on. Concrete check: run this and confirm your prediction matches —

```python
import numpy as np
W = np.zeros((64, 64))
x = np.random.randn(1, 64)
for layer in range(5):
    x = np.maximum(0, x @ W)  # ReLU(x @ W)
    print(layer, x.sum())     # should be exactly 0.0 every single layer
```

If every printed sum is `0.0`, you've confirmed the network is dead on arrival — no amount of training will move it, because the gradient of a dead ReLU with zero input is also zero everywhere. This is the single most common "my loss never moves" bug reported by people implementing a network from scratch for the first time.


---

[← 15. SGD, Adam, and Why Adam Won LLMs](/courses/llm-mastery/15-optimization-sgd-adam/)  
[17. Dropout, Weight Decay, and Noise as Teachers →](/courses/llm-mastery/17-regularization-dropout/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
