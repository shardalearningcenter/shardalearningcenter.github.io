---
layout: course
title: "14. Softmax and Temperature, Carefully"
permalink: /courses/llm-mastery/14-softmax-temperature/
course_track: "LLM Mastery"
description: "Softmax is competitive normalization, not a mystical activation. Temperature rescales the competition before it happens, and getting the numerics wrong is a one-line NaN bug."
level: Intermediate
toc:
  - id: "softmax-is-exponentiate-then-normalize"
    label: "Softmax is exponentiate, then normalize"
  - id: "the-max-subtraction-trick-is-not-optional"
    label: "The max-subtraction trick is not optional"
  - id: "temperature-rescaling-the-competition"
    label: "Temperature: rescaling the competition"
  - id: "failure-mode-softmax-of-large-logits"
    label: "Failure mode: softmax of large logits"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 14/50** · Karpathy-style LLM course

Softmax gets talked about like it's some elegant probabilistic object descended from information theory. It is that, eventually — but first, treat it mechanically: it's a way to turn a list of arbitrary real numbers into a list of positive numbers that sum to 1, while preserving their relative order and *exaggerating* the gaps between large and small values. That exaggeration, and how you control it, is the entire story of this article.

## Softmax is exponentiate, then normalize
{: #softmax-is-exponentiate-then-normalize }

```
softmax(z)_i = exp(z_i) / sum_j exp(z_j)
```

Two steps, no more: exponentiate every logit (guarantees positivity), then divide by the sum (guarantees they sum to 1). The exponential is doing something specific and worth naming — it converts *additive* differences in the logits into *multiplicative* differences in the output probabilities. A logit gap of `+1` between two classes becomes roughly a `2.7x` probability ratio (`e^1`); a gap of `+5` becomes roughly `148x`. This is why softmax feels "winner take all" even for modestly different logits — it's exponential amplification of whatever gap already existed, not a gentle rescaling.

```python
import numpy as np

def softmax(z):
    return np.exp(z) / np.sum(np.exp(z))

print(softmax(np.array([2.0, 1.0, 0.1])))
# [0.659, 0.242, 0.099] — note the gap between logits 2.0 and 1.0 already
# produces a 2.7x ratio in the output, matching exp(1) exactly
```

## The max-subtraction trick is not optional
{: #the-max-subtraction-trick-is-not-optional }

The naive formula above is mathematically correct and numerically dangerous. `exp(z)` for even moderately large `z` overflows a float32 fast — `exp(89)` is already past float32's max representable value, and transformer logits routinely swing into the tens or hundreds during training, especially early on or when something upstream is misbehaving. The fix is a small algebraic identity: subtract the max logit before exponentiating.

```
softmax(z)_i = exp(z_i - max(z)) / sum_j exp(z_j - max(z))
```

This produces the **exact same output** — subtracting a constant from every logit before exponentiating cancels out in the ratio, because `exp(z_i - m) / sum(exp(z_j - m)) = exp(z_i)/exp(m) / (sum(exp(z_j))/exp(m))`, and the `exp(m)` cancels top and bottom. But now the largest exponentiated value is `exp(0) = 1` instead of `exp(huge)`, so you never overflow. Every production softmax implementation — PyTorch's `F.softmax`, numpy-based reference code, everything — does this subtraction internally. If you're ever implementing softmax from scratch (which you should do at least once), do it too.

```python
def softmax_stable(z):
    z = z - np.max(z)
    return np.exp(z) / np.sum(np.exp(z))
```

## Temperature: rescaling the competition
{: #temperature-rescaling-the-competition }

Temperature is applied *before* the softmax, by dividing the logits: `softmax(z / T)`. Since softmax amplifies additive gaps exponentially, dividing the logits by `T` shrinks or grows those gaps before the exponential gets to them.

- `T → 0`: gaps between logits get amplified toward infinity, so softmax collapses onto the single largest logit — this is greedy, deterministic argmax in the limit.
- `T = 1`: the network's logits are used exactly as trained; this is the "default" the model was calibrated against during training.
- `T > 1`: gaps shrink, the distribution flattens toward uniform, and sampling becomes more random — useful for creative generation, dangerous for anything that needs to be reliable.

```python
def softmax_temp(z, T=1.0):
    z = z / T
    z = z - np.max(z)
    return np.exp(z) / np.sum(np.exp(z))

logits = np.array([2.0, 1.0, 0.1])
print(softmax_temp(logits, T=0.5))  # sharper — [0.87, 0.12, 0.01]
print(softmax_temp(logits, T=2.0))  # flatter — [0.47, 0.31, 0.22]
```

Notice temperature never changes *which* token has the highest probability — it only changes *how much* higher. That's why temperature alone can't fix a model that's confidently wrong; it can only make a correct model's confidence more or less pronounced.

## Failure mode: softmax of large logits
{: #failure-mode-softmax-of-large-logits }

The concrete bug this whole article is protecting you from: implementing softmax the textbook way (no max-subtraction) inside a custom attention or loss function, having it work fine on your tiny test tensor, and then watching training produce `NaN` loss at step 340 for no apparent reason. What actually happened is that some intermediate activation grew large enough — through normal training dynamics, or through a learning rate slightly too high — that `exp()` of an unshifted logit overflowed to `inf`, and `inf / inf` (or `inf / sum-containing-inf`) evaluates to `NaN`. The NaN then propagates through every subsequent computation, including gradients, and your entire model's parameters become `NaN` within a step or two.

The debugging trap is that the *root cause* (missing max-subtraction) is far upstream of the *symptom* (NaN loss reported at step 340), so people chase learning rate, initialization, and data bugs for hours before checking whether their softmax is numerically stable. If you ever write softmax, cross-entropy, or attention from scratch instead of calling a library function, subtract the max. Always. There is no situation where it changes the mathematical answer and no situation where skipping it is safe at scale.

## Exercise
{: #exercise }

Prove to yourself, algebraically, why `softmax(z)` and `softmax(z - c)` are identical for any constant `c` (write out the ratio and cancel the `exp(-c)` factor top and bottom). Then verify numerically:

```python
z = np.array([1000.0, 1001.0, 999.0])  # will overflow naive softmax
try:
    print(softmax(z))       # naive version — check what happens
except Exception as e:
    print("naive blew up:", e)
print(softmax_stable(z))    # stable version — should print real probabilities
```

Concrete check: the naive version should produce `nan` values (from `inf/inf`), while `softmax_stable` should print approximately `[0.09, 0.24, 0.03]`-scale real numbers summing to 1. If the naive version doesn't visibly fail on your machine, push the logits higher (`10000.0`) until it does — the point is to see the failure with your own eyes once, so you never forget to subtract the max again.


---

[← 13. Tensor Shapes: The Hidden Curriculum](/courses/llm-mastery/13-tensors-shapes-discipline/)  
[15. SGD, Adam, and Why Adam Won LLMs →](/courses/llm-mastery/15-optimization-sgd-adam/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
