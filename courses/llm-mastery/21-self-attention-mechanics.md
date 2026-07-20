---
layout: course
title: "21. Self-Attention Mechanics"
permalink: /courses/llm-mastery/21-self-attention-mechanics/
course_track: "LLM Mastery"
description: "Attention is a weighted average. The only hard part is learning good weights."
level: Intermediate
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-a-differentiable-lookup"
    label: "Mental model: a differentiable lookup"
  - id: "worked-example-by-hand"
    label: "Worked example, by hand"
  - id: "the-causal-mask"
    label: "The causal mask"
  - id: "failure-mode-forgetting-to-scale"
    label: "Failure mode: forgetting to scale"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 21/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

Attention is a weighted average of value vectors, and the weights come from comparing a query against a set of keys. That's it. There's no hidden magic in the softmax, no mystical "understanding" happening. Once you accept that attention is arithmetic — three matrix multiplies and a normalization — the rest of the transformer literature stops reading like scripture and starts reading like an engineering decision log.

Here's the equation, and I want you to actually look at it instead of skimming past it:

```
Q = X Wq        # (T, d_k)  "what am I looking for?"
K = X Wk        # (T, d_k)  "what do I contain?"
V = X Wv        # (T, d_v)  "what do I offer if picked?"

scores = Q K^T / sqrt(d_k)     # (T, T)
attn   = softmax(scores, dim=-1)
out    = attn @ V              # (T, d_v)
```

Every token in the sequence produces three vectors: a query, a key, and a value, all via learned linear projections of the same input `X`. The query asks a question. The keys of every other token answer. The softmax turns raw similarity scores into a probability distribution over "how much should I listen to you." The output is a weighted blend of everyone's value vectors, weighted by how relevant their key was to my query.

## Mental model: a differentiable lookup
{: #mental-model-a-differentiable-lookup }

Think of a hash map lookup, except every step is soft. In a real dict, `d[key]` either matches exactly or throws a `KeyError`. In attention, every key partially matches every query, and you get back a blend of all values, weighted by match quality. Turn the temperature of the softmax down (or scale scores up) and it behaves more like a hard lookup — winner takes most. Turn it up and it behaves like an average over everyone.

This is why attention composes so well with gradient descent: there is no discrete argmax anywhere in the forward pass. The routing decision — who listens to whom — is itself learned by backprop, jointly with everything else. Nobody hand-designs the routing table. The model discovers, from data, that verbs should attend to their subjects, that closing parentheses should attend to their opener, and a thousand other patterns nobody explicitly programmed.

## Worked example, by hand
{: #worked-example-by-hand }

Small numbers make this concrete. Say `T=3` tokens, `d_k=2`. Skip the projections — pretend `Q`, `K`, `V` came out of them already:

```python
import numpy as np

Q = np.array([[1.0, 0.0],
              [0.0, 1.0],
              [1.0, 1.0]])
K = np.array([[1.0, 0.0],
              [0.0, 1.0],
              [1.0, 1.0]])
V = np.array([[10.0, 0.0],
              [0.0, 10.0],
              [5.0, 5.0]])

d_k = Q.shape[-1]
scores = Q @ K.T / np.sqrt(d_k)          # (3,3)
scores -= scores.max(axis=-1, keepdims=True)  # stability
weights = np.exp(scores)
weights /= weights.sum(axis=-1, keepdims=True)
out = weights @ V

print(np.round(weights, 3))
print(np.round(out, 3))
```

Run it and inspect the weights matrix. Row 0 is token 0's query (`[1,0]`), which matches key 0 (`[1,0]`) exactly and key 2 (`[1,1]`) partially, so its output leans heavily toward `V[0] = [10,0]` with some contribution from `V[2]`. That's the whole mechanism, laid bare with numbers you can trace by hand. If you can't predict the shape of `weights` and roughly which row will dominate before running the code, stop and re-derive it — this is the one piece of a transformer that has zero excuse for being fuzzy in your head.

## The causal mask
{: #the-causal-mask }

For language modeling, token `i` is not allowed to see token `j > i` — that would be cheating, since the model's job is to predict token `i+1` from everything *before* it. Before the softmax, add `-inf` (in practice, a large negative number like `-1e9` in fp32, or the dtype's min value) to every score where `j > i`:

```python
mask = np.triu(np.ones((T, T)), k=1).astype(bool)
scores = np.where(mask, -1e9, scores)
```

After softmax, those positions become exactly zero weight. This single triangular mask is the difference between a language model and a bidirectional encoder like BERT — same attention math, different visibility rules.

## Failure mode: forgetting to scale
{: #failure-mode-forgetting-to-scale }

Drop the `/ sqrt(d_k)` and watch your model quietly get worse in a way that's hard to diagnose from the loss curve alone. As `d_k` grows, the dot products `Q · K` grow with it (variance scales roughly linearly with `d_k` for random unit vectors). Larger raw scores push softmax toward one-hot outputs — the gradient of softmax is `p(1-p)`, which collapses toward zero once one logit dominates. You get vanishing gradients through the attention weights specifically, while the rest of the network trains fine, so the symptom is "training is slow and attention patterns look weirdly peaky" rather than a crash. This is exactly the bug the original "Attention Is All You Need" scaling term exists to prevent, and it's the first thing to check if you hand-roll attention and training stalls.

## Exercise
{: #exercise }

Extend the worked example above to `T=5`, random `Q, K, V` with `d_k=8` (use `np.random.seed(0)` for reproducibility). Compute attention twice: once with the `sqrt(d_k)` scaling, once without. Print the max value in each row of the softmax output for both cases. Confirm the unscaled version produces rows that are noticeably closer to one-hot (max weight near 1.0) than the scaled version. That gap *is* the bug, made visible.

---

[← 20. Reading 'Attention Is All You Need' Like an Engineer](/courses/llm-mastery/20-attention-is-all-you-need-read/)  
[22. Multi-Head Attention →](/courses/llm-mastery/22-multi-head-attention/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
