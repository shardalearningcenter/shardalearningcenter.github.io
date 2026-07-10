---
layout: course
title: "43. Interpretability: Looking Inside"
permalink: /courses/llm-mastery/43-interpretability-basics/
course_track: "LLM Mastery"
description: "You can read every one of a model's numbers and still not know why it said what it said. Interpretability builds partial, testable maps anyway."
level: Advanced
toc:
  - id: "mental-model"
    label: "Mental model"
  - id: "worked-example"
    label: "Worked example"
  - id: "failure-mode"
    label: "Failure mode"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 43/50** · Karpathy-style LLM course

A trained model's weights are fully known to you — every float, in the open if it's an open model — and that transparency buys you almost nothing on its own. Interpretability isn't about having access to the numbers; it's about building structured, testable hypotheses about what those numbers *compute*, then trying hard to break your own hypothesis.

## Mental model
{: #mental-model }

A useful working hypothesis, the "linear representation hypothesis," is that many meaningful concepts a model has learned correspond, at least approximately, to *directions* in activation space — not single neurons, but linear combinations of them. "Is this text about France," "is this a sycophantic completion," "is this token inside a code block" — each might correspond to some vector `v` such that `activation · v` tracks the concept's presence.

If that hypothesis holds for some concept, you get two tools for free: **probing** — train a simple linear classifier on activations to predict the concept, testing whether the direction exists and is findable — and **causal intervention** — add or subtract that direction from live activations and see if behavior changes as predicted, testing whether the direction actually *does* something rather than just correlating with something that does. The gap between those two tools is where most of the interesting and misleading results in interpretability live.

## Worked example
{: #worked-example }

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

# activations: [n_examples, hidden_dim], labels: 1 if text is formal register, else 0
def train_probe(activations: np.ndarray, labels: np.ndarray) -> np.ndarray:
    probe = LogisticRegression().fit(activations, labels)
    direction = probe.coef_[0]
    return direction / np.linalg.norm(direction)

def ablate(activations: np.ndarray, direction: np.ndarray, strength: float = 5.0) -> np.ndarray:
    """Push activations along -direction to suppress the 'formal register' feature,
    then feed this back into the model's forward pass and see what it generates."""
    return activations - strength * direction

direction = train_probe(train_activations, train_labels)
edited = ablate(live_activations, direction)
# now run the rest of the forward pass on `edited` instead of `live_activations`,
# and check whether generated text becomes measurably less formal
```

The probe alone tells you the direction is *findable* — that formal and informal text differ along it, which could mean the model computes formality there, or could mean formality is merely correlated with something else the direction actually tracks, like sentence length or punctuation density. Only the ablation step — pushing along that direction and checking whether generation changes in the *predicted* way — gives you evidence the direction is causally load-bearing rather than a bystander correlation.

## Failure mode
{: #failure-mode }

Two traps catch even careful researchers:

- **Probe accuracy is not causal evidence.** A linear probe can hit 95% accuracy on a concept the model doesn't "use" for anything — it's just linearly readable as a side effect of something else. High probe accuracy is necessary but nowhere near sufficient for claiming "the model represents X here." Always pair a probe with an intervention before making a causal claim.
- **Superposition.** Models are believed to pack far more features than they have dimensions, overlapping the same directions for multiple, only-loosely-related concepts, because most features are sparse — active on a small fraction of inputs — so the model can afford collisions. Ablate a direction expecting to suppress one concept and you often perturb several unrelated ones at once, making a "clean" single-feature story much rarer than early interpretability writing suggested.

Sparse autoencoders are the current best attempt at untangling superposition: train a much wider, sparsity-constrained autoencoder on a layer's activations, and hope that its learned dictionary of directions decomposes the crowded original space into cleaner, more monosemantic features than raw activation directions gave you. It's a genuine improvement in practice, not a solution — you've traded "a few crowded directions" for "many more directions, some of which are still crowded," and you still need the same probe-then-ablate discipline to trust any individual one of them.

## Exercise
{: #exercise }

You train a probe that predicts, with 92% accuracy from layer-12 activations, whether a math problem's answer will be correct. Design the ablation experiment that would distinguish two hypotheses: (a) the model has an internal "confidence" feature that causally drives whether it commits to an answer or hedges, versus (b) the probe is just picking up on problem difficulty, which correlates with both correctness and something else entirely unrelated to the model's internal confidence. What specific outcome of your intervention would falsify hypothesis (a)?


---

[← 42. Hallucinations: Why They Happen](/courses/llm-mastery/42-hallucinations/)  
[44. Quantization and Local Serving →](/courses/llm-mastery/44-quantization-serving/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
