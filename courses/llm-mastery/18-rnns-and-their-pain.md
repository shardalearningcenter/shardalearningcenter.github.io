---
layout: course
title: "18. RNNs: The Old Kings and Their Pain"
permalink: /courses/llm-mastery/18-rnns-and-their-pain/
course_track: "LLM Mastery"
description: "A recurrent network is a for-loop with memory, and that for-loop is exactly what makes it both elegant on paper and unable to keep up with a GPU built to do everything in parallel."
level: Intermediate
toc:
  - id: "the-idea-a-hidden-state-carried-forward"
    label: "The idea: a hidden state carried forward"
  - id: "a-worked-forward-pass-in-numpy"
    label: "A worked forward pass in numpy"
  - id: "backpropagation-through-time-and-why-it-hurts"
    label: "Backpropagation through time, and why it hurts"
  - id: "why-we-moved-on-the-parallelism-argument"
    label: "Why we moved on: the parallelism argument"
  - id: "failure-mode-truncating-bptt-without-noticing"
    label: "Failure mode: truncating BPTT without noticing"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 18/50** · Karpathy-style LLM course

Before attention, this was the entire approach to sequence modeling, and it's worth understanding on its own terms rather than as a strawman to make Transformers look good. A recurrent network is a genuinely elegant idea: one small function, applied over and over, carrying a summary of everything seen so far in a fixed-size vector. The reason it lost is not that the idea was wrong — it's that the idea is fundamentally sequential, and sequential doesn't parallelize on hardware built for parallelism.

## The idea: a hidden state carried forward
{: #the-idea-a-hidden-state-carried-forward }

The core recurrence is one equation:

```
h_t = f(h_{t-1}, x_t)
```

At every time step, the network takes the previous hidden state `h_{t-1}` (its entire memory of everything before now, compressed into a fixed-size vector) and the current input `x_t`, and produces a new hidden state. The same function `f` — the same weights — is reused at every single time step. This weight-sharing across time is what lets an RNN process sequences of any length with a fixed number of parameters, which was a genuinely important property before Transformers found a different way to get it (positional-agnostic attention plus explicit position information, covered starting in article 19).

A concrete vanilla RNN cell:

```
h_t = tanh(W_hh @ h_{t-1} + W_xh @ x_t + b)
```

`W_hh` transforms the previous hidden state, `W_xh` transforms the current input, they're summed and squashed through `tanh` to keep the hidden state bounded. That's it — the entire recurrent core of a vanilla RNN is one matrix-vector product, one more matrix-vector product, a sum, and a nonlinearity, repeated at every position.

## A worked forward pass in numpy
{: #a-worked-forward-pass-in-numpy }

```python
import numpy as np

def rnn_forward(xs, h0, Whh, Wxh, b):
    h = h0
    hidden_states = [h]
    for x in xs:
        h = np.tanh(Whh @ h + Wxh @ x + b)
        hidden_states.append(h)
    return hidden_states

hidden_size, input_size, T = 8, 4, 6
Whh = np.random.randn(hidden_size, hidden_size) * 0.1
Wxh = np.random.randn(hidden_size, input_size) * 0.1
b = np.zeros(hidden_size)
h0 = np.zeros(hidden_size)
xs = [np.random.randn(input_size) for _ in range(T)]

states = rnn_forward(xs, h0, Whh, Wxh, b)
print(len(states))          # T + 1 = 7, including h0
print(states[-1].shape)     # (8,) — final hidden state summarizes all 6 inputs
```

Notice the loop: `states[6]` was computed from `states[5]`, which was computed from `states[4]`, and so on, in strict order — you cannot compute `states[3]` before `states[2]` exists. That data dependency, right there in the `for` loop, is the entire reason RNNs resist GPU parallelism across the time dimension: a GPU wants to do the same operation on many independent pieces of data simultaneously, and each RNN step is *not* independent of the previous one by construction.

## Backpropagation through time, and why it hurts
{: #backpropagation-through-time-and-why-it-hurts }

Training an RNN means backpropagating the loss gradient through every one of those `T` sequential steps — a procedure called **backpropagation through time (BPTT)**. Because `h_t` depends on `h_{t-1}` through the *same* weight matrix `W_hh` at every step, the gradient flowing back to an early time step is a product of `T` copies of (roughly) the same Jacobian, applied repeatedly. This is article 11's vanishing/exploding gradient problem, except now it isn't a property of network *depth* — it's a property of *sequence length*. A 200-token sequence is, from the gradient's perspective, a 200-layer-deep network with tied weights at every layer.

LSTMs and GRUs were invented specifically to fight this: they add explicit gating mechanisms (a "forget gate," an "input gate") that let the network learn to preserve gradient along a near-identity path when useful, similar in spirit to the residual connections that later helped deep Transformers. They meaningfully extend how far gradient can usefully flow back — but they manage the symptom, they don't eliminate the underlying sequential-depth-equals-sequence-length problem.

## Why we moved on: the parallelism argument
{: #why-we-moved-on-the-parallelism-argument }

The case against RNNs at LLM scale is almost entirely an engineering argument, not an accuracy argument: modern GPUs get their throughput from doing enormous numbers of independent operations in parallel. Self-attention, covered starting next article and in depth in article 21, computes relationships between *all* pairs of positions in a sequence in one large parallel matrix operation — every position's computation is independent of every other position's computation within a layer, which maps beautifully onto GPU parallelism. An RNN's per-step computation cannot start until the previous step's hidden state exists, full stop, no matter how much parallel compute you throw at the problem.

This single property — parallel-across-time versus sequential-across-time — is why Transformers could absorb vastly more compute and data than RNNs ever practically could, and it is the actual mechanistic reason "attention is all you need" turned out to matter as much as it did, well before anyone had coined the term "scaling laws."

## Failure mode: truncating BPTT without noticing
{: #failure-mode-truncating-bptt-without-noticing }

Because full BPTT over very long sequences is both computationally expensive and numerically painful, RNN training in practice almost always uses **truncated BPTT**: run the recurrence forward across the whole sequence, but only backpropagate gradient through the last `k` steps, treating `h_{t-k}` as a constant (detached from the graph) for the purposes of that gradient computation. This is a reasonable, standard engineering tradeoff — but it's also a silent one: if you don't explicitly reason about your truncation window `k` relative to how far back in the sequence the actual dependencies you care about live, you can train a model that appears to converge just fine while being structurally incapable of learning any dependency longer than `k` steps, because gradient literally never flows back further than that.

The diagnostic habit this demands: know your truncation window as a concrete number, and know whether the task you're training on has dependencies longer than that number. A model trained with `k=35` truncated BPTT that needs to remember something from 100 steps back will train, will show a reasonable loss curve, and will simply never learn that specific long-range dependency — and nothing about the loss curve alone will tell you that's what's happening.

## Exercise
{: #exercise }

Name one concrete strength RNNs still have over a vanilla (no KV-cache tricks) Transformer, and justify it in terms of *compute or memory*, not just accuracy. Concrete check: a correct answer should point at inference-time memory — an RNN's hidden state is a single fixed-size vector regardless of how many tokens have been processed, so generating the 10,000th token costs the same memory as generating the 10th, while a Transformer's KV cache (covered in article 28) grows linearly with sequence length. If your answer doesn't reference this fixed-memory-per-step property, look up how RNN hidden state size relates to sequence length versus how Transformer KV cache size relates to sequence length, and reconsider.


---

[← 17. Dropout, Weight Decay, and Noise as Teachers](/courses/llm-mastery/17-regularization-dropout/)  
[19. Seq2Seq and the Dawn of Attention →](/courses/llm-mastery/19-seq2seq-attention-dawn/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
