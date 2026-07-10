---
layout: course
title: "30. Scaling Laws: The Bitter Lesson, Quantified"
permalink: /courses/llm-mastery/30-scaling-laws-intuition/
course_track: "LLM Mastery"
description: "Loss vs. compute isn't a vibe, it's a power law you can fit and extrapolate — and misallocating the budget is a real, costly mistake."
level: Advanced
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-a-recipe-with-a-fixed-grocery-budget"
    label: "Mental model: a recipe with a fixed grocery budget"
  - id: "worked-example-the-chinchilla-formula"
    label: "Worked example: the Chinchilla formula"
  - id: "the-practical-rule-of-thumb"
    label: "The practical rule of thumb"
  - id: "failure-mode-misallocated-compute"
    label: "Failure mode: misallocated compute"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 30/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

Pretraining loss as a function of model size, dataset size, and compute follows a smooth, predictable power law across many orders of magnitude — not a rough trend, an equation you can fit to a handful of small training runs and use to forecast the loss of a run 10,000x larger before you spend the money on it. That predictability is the entire reason scaling has been the dominant strategy in frontier LLM development: when the relationship between "resources spent" and "loss achieved" is this well-behaved, the highest-leverage research question stops being "what clever architecture change helps" and becomes "how do I allocate a fixed compute budget between model size and data to minimize loss" — a question with a computable answer.

## Mental model: a recipe with a fixed grocery budget
{: #mental-model-a-recipe-with-a-fixed-grocery-budget }

Picture a fixed grocery budget you must split between "how big a pot you buy" (parameters) and "how much food you cook in it" (training tokens). A bigger pot with too little food in it is wasted capacity — you paid for space you didn't use. A small pot with too much food overflows — you paid for ingredients the pot can't hold and process properly (the model underfits, unable to extract everything the data offers before running out of capacity). Scaling laws are the empirical answer to "for this exact grocery budget, what pot size and food quantity minimizes waste" — and the striking empirical finding (from DeepMind's 2022 Chinchilla paper) is that the pre-Chinchilla era of LLM training was systematically buying pots too big for the food available: models like the original GPT-3 and Gopher were substantially undertrained relative to their size.

## Worked example: the Chinchilla formula
{: #worked-example-the-chinchilla-formula }

The Chinchilla paper fits loss as a function of parameters `N` and training tokens `D`:

```
L(N, D) = E + A / N^alpha + B / D^beta
```

where `E` is an irreducible loss floor (entropy of natural language itself), and the two power-law terms capture loss reduction from more parameters and more data respectively. Fitted constants from the paper (approximately): `E ≈ 1.69`, `A ≈ 406.4`, `B ≈ 410.7`, `alpha ≈ 0.34`, `beta ≈ 0.28`. Plug in numbers:

```python
E, A, B, alpha, beta = 1.69, 406.4, 410.7, 0.34, 0.28

def loss(N, D):
    return E + A / N**alpha + B / D**beta

# GPT-3-scale: 175B params, but trained on only ~300B tokens
print(loss(175e9, 300e9))

# Chinchilla-recommended allocation for the same compute budget:
# roughly 4x smaller model, 4x more tokens
print(loss(175e9 / 4, 300e9 * 4))
```

Run this and the second number comes out lower — a *smaller* model trained on *more* tokens, using roughly the same total compute (compute scales with `N × D` for a fixed number of training steps), achieves better loss than the larger undertrained one. That's not a hand-wavy claim about "more data is good" — it's a direct consequence of `alpha` and `beta` both being well under 1: each term has strongly diminishing returns, so overinvesting in one dimension while starving the other leaves loss on the table that a rebalance would recover for free, at the same total compute cost.

## The practical rule of thumb
{: #the-practical-rule-of-thumb }

The paper's headline finding, distilled: for compute-optimal training, model size and dataset size should scale at roughly the same rate as compute grows — practically, aim for something in the neighborhood of 20 training tokens per parameter (this ratio has crept up over time as later work found even more tokens per parameter helps when you're not purely compute-constrained, e.g. LLaMA-scale models trained on ratios well above 20:1 because inference cost, not just training compute, factors into the real-world optimization). The headline lesson generalizes past the exact ratio: whatever your compute budget, there is a loss-minimizing split between "spend it on parameters" and "spend it on tokens," and it is not automatically "make the model as big as possible."

## Failure mode: misallocated compute
{: #failure-mode-misallocated-compute }

Train a model far larger than your token budget supports compute-optimally, and you get a model that's *more expensive to run at inference time forever* for a loss that a smaller, better-trained model would have matched or beaten. This isn't a training-time-only mistake — every single inference call for that model's entire deployed lifetime pays the larger model's compute and memory cost, for training-time savings you didn't even get. The Chinchilla paper's own headline example, a 70B model trained compute-optimally, matched or beat the 280B-parameter Gopher on most benchmarks while being roughly 4x cheaper to run at inference. Scaling laws don't just tell you "bigger is better" — read carefully, they tell you exactly where "bigger" stops being the loss-minimizing choice for your specific budget.

## Exercise
{: #exercise }

Using the `loss(N, D)` function above, fix total compute proportional to `N * D = 175e9 * 300e9` (GPT-3's approximate training FLOPs profile). Sweep `N` from `10e9` to `500e9` in steps, computing `D = (175e9 * 300e9) / N` for each, and evaluate `loss(N, D)`. Plot or print loss against `N`. Find the `N` that minimizes loss at fixed compute, and report how far GPT-3's actual `N=175e9` sits from that optimum.

---

[← 29. Batching, Throughput, and the Economics of Tokens](/courses/llm-mastery/29-batching-and-throughput/)  
[31. Tokenization Deep Dive: BPE Under the Hood →](/courses/llm-mastery/31-tokenization-deep-dive/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
