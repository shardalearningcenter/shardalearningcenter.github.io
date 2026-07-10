---
layout: course
title: "11. Backpropagation as Local Blame"
permalink: /courses/llm-mastery/11-backprop-intuition/
course_track: "LLM Mastery"
description: "Backprop is the chain rule wearing a compiler's clothes: every node computes one local derivative and multiplies it into whatever gradient arrives from above."
level: Intermediate
toc:
  - id: "the-chain-rule-is-the-whole-thing"
    label: "The chain rule is the whole thing"
  - id: "a-graph-you-can-hold-in-your-head"
    label: "A graph you can hold in your head"
  - id: "why-gradients-vanish-or-explode"
    label: "Why gradients vanish or explode"
  - id: "failure-mode-the-gradient-you-forgot-to-zero"
    label: "Failure mode: the gradient you forgot to zero"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 11/50** · Karpathy-style LLM course

Backpropagation is not a deep learning trick you have to trust from a textbook. It is the chain rule from second-year calculus, applied mechanically by a program that never gets bored of bookkeeping. If you can differentiate `f(x) = x^2` by hand, you already understand most of what happens when you call `loss.backward()`.

## The chain rule is the whole thing
{: #the-chain-rule-is-the-whole-thing }

Every neural network, no matter how large, is a composition of simple functions: adds, multiplies, matrix multiplies, a nonlinearity here, a normalization there. Composition means chain rule:

```
if  L = f(g(x))
then  dL/dx = dL/dg · dg/dx
```

Backprop just generalizes this to graphs with many nodes and many paths. Each node in the computation graph knows exactly two things: how to compute its output from its inputs (the forward pass), and how to compute the derivative of its output with respect to each of its inputs, given the derivative of the *loss* with respect to its output (the backward pass). That second piece is called the **local gradient**. The node doesn't need to know anything about the rest of the network — it just needs `dL/d(my output)` handed to it, and it multiplies that by its own local derivative to produce `dL/d(my inputs)`, then passes those further back.

This is why I call it "local blame." No node reasons globally about the loss. Each node only asks: *given how much the final loss changed per unit change in my output, and given how my output changes per unit change in my input, how much does the loss change per unit change in my input?* That's it. Multiply and pass along.

## A graph you can hold in your head
{: #a-graph-you-can-hold-in-your-head }

Take `f = (a + b) * c`. Draw it as two nodes: an add node producing `d = a + b`, and a multiply node producing `f = d * c`. Suppose `a=2, b=-3, c=4`, so `d=-1` and `f=-4`.

Forward pass computes `d=-1`, `f=-4` — nothing interesting yet. The backward pass starts at the end with `dL/df = 1` (we're asking "how does f affect f" — trivially 1, or plug in whatever upstream gradient arrives if `f` feeds into something else).

```python
# forward
a, b, c = 2.0, -3.0, 4.0
d = a + b        # -1.0
f = d * c        # -4.0

# backward, seeded with dL/df = 1.0
dL_df = 1.0
dL_dd = dL_df * c    # local derivative of f w.r.t. d is c → -1*... wait: d(f)/d(d) = c
dL_dc = dL_df * d    # d(f)/d(c) = d
dL_da = dL_dd * 1.0  # d(d)/d(a) = 1
dL_db = dL_dd * 1.0  # d(d)/d(b) = 1

print(dL_dd, dL_dc, dL_da, dL_db)  # 4.0 -1.0 4.0 4.0
```

Every operation in PyTorch or a numpy autograd toy is this pattern, repeated millions of times across a graph with millions of nodes. The multiply node's local derivative rule is "swap and multiply the other input"; the add node's rule is "just pass the gradient through unchanged, to both inputs." Learn five or six of these local rules (add, multiply, matmul, tanh, ReLU, softmax+cross-entropy fused) and you can trace gradients through anything.

## Why gradients vanish or explode
{: #why-gradients-vanish-or-explode }

Because backward passes are chains of multiplications, depth compounds whatever each factor tends to be. If most local derivatives along a long path are less than 1 in magnitude — which happens naturally with `sigmoid` or `tanh` saturating away from zero — the product shrinks geometrically. Twenty layers with an average factor of 0.7 gives you `0.7^20 ≈ 0.0008`: the gradient signal reaching early layers is nearly zero, and those layers stop learning. This is the **vanishing gradient** problem, and it's why sigmoid-heavy deep nets were painful to train before ReLU, residual connections, and normalization layers became standard.

Run the arithmetic the other way — local derivatives averaging above 1 — and the product explodes instead, blowing up to `NaN` within a few layers. This is why residual connections matter so much for depth: `x = x + sublayer(x)` guarantees at least one path back to every earlier layer with a local derivative of exactly 1 (from the identity branch), which is a highway for gradient that doesn't get multiplied down to nothing.

## Failure mode: the gradient you forgot to zero
{: #failure-mode-the-gradient-you-forgot-to-zero }

The single most common backprop bug in practice has nothing to do with math — it's bookkeeping. Gradients in frameworks like PyTorch **accumulate** into `.grad` by design (this is what makes gradient accumulation across micro-batches possible). If you call `loss.backward()` in a loop without calling `optimizer.zero_grad()` (or `param.grad = None`) first, each step's gradient gets added on top of the last one instead of replacing it. Loss will look like it's training, sort of, but the effective learning rate silently grows every step until training diverges or plateaus in a way that makes no sense from the math alone.

The fix is one line, but the diagnosis takes people hours because the symptom (loss goes weird after N steps) looks like a hyperparameter problem, not a bookkeeping problem. Whenever a training run misbehaves in a way you can't explain from architecture or learning rate, check the boring stuff first: is grad being zeroed, is `.detach()` missing somewhere it's needed, is a tensor being reused across the graph in a way that double-counts it.

## Exercise
{: #exercise }

For `y = a * b`, if `dL/dy = 2`, `a = 3`, `b = 4`: compute `dL/da` and `dL/db` by hand using the local-derivative rule for multiply (swap and multiply). Then verify your answer in three lines of PyTorch:

```python
import torch
a = torch.tensor(3.0, requires_grad=True)
b = torch.tensor(4.0, requires_grad=True)
y = a * b
y.backward(torch.tensor(2.0))  # seed dL/dy = 2
print(a.grad, b.grad)  # should match your hand-computed values
```

If `a.grad` and `b.grad` don't match your hand calculation, you have a sign or ordering error in the multiply rule — go back and re-derive `d(a*b)/da` from first principles before moving on. Backprop later in this course only gets more graph, never more calculus.


---

[← 10. The MakeMore Mindset: Build Tiny, Understand Deeply](/courses/llm-mastery/10-makemore-mindset/)  
[12. Micrograd Energy: Autograd From Scratch →](/courses/llm-mastery/12-autograd-from-scratch/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
