---
layout: course
title: "12. Micrograd Energy: Autograd From Scratch"
permalink: /courses/llm-mastery/12-autograd-from-scratch/
course_track: "LLM Mastery"
description: "A Value object with a .grad field and a topological sort is the entire trick behind PyTorch autograd — build it once and it stops being magic forever."
level: Intermediate
toc:
  - id: "the-minimal-object-you-need"
    label: "The minimal object you need"
  - id: "building-multiply-and-a-nonlinearity"
    label: "Building multiply and a nonlinearity"
  - id: "backward-is-just-a-reversed-topological-sort"
    label: "Backward is just a reversed topological sort"
  - id: "failure-mode-reusing-a-node-and-double-counting"
    label: "Failure mode: reusing a node and double-counting"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 12/50** · Karpathy-style LLM course

You do not need to read the PyTorch autograd C++ source to trust it. You need about 40 lines of Python. Build a scalar autograd engine once, watch `loss.backward()` populate every `.grad` correctly, and PyTorch stops being a black box — it becomes "the thing I already built, but vectorized and in C++."

## The minimal object you need
{: #the-minimal-object-you-need }

The whole idea rests on one object: a `Value` that remembers its data, its gradient, the nodes that produced it (its "children"), and a function that knows how to push gradient backward through whatever operation created it.

```python
class Value:
    def __init__(self, data, children=(), op=""):
        self.data = data
        self.grad = 0.0
        self._prev = set(children)
        self._backward = lambda: None
        self._op = op

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"
```

That's the whole state. `_backward` starts as a no-op because a leaf node (a raw input or parameter) has nothing to push gradient to. Every operation you define — `__add__`, `__mul__`, `tanh`, whatever — creates a *new* `Value` and attaches a `_backward` closure that knows the local derivative rule for that specific operation.

## Building multiply and a nonlinearity
{: #building-multiply-and-a-nonlinearity }

```python
class Value:
    # ... __init__ as above ...

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), "*")
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def tanh(self):
        t = (2.7182818**(2*self.data) - 1) / (2.7182818**(2*self.data) + 1)
        out = Value(t, (self,), "tanh")
        def _backward():
            self.grad += (1 - t**2) * out.grad
        out._backward = _backward
        return out
```

Notice the pattern repeats exactly: compute the forward value, remember the parents, define a closure that knows *this operation's* local derivative, multiply it by the gradient flowing in (`out.grad`), and **accumulate** (`+=`, never `=`) into each parent's `.grad`. That `+=` matters — if a value is used twice in an expression (like `x` appearing in both branches of `x*x`), it must receive gradient contributions from both uses, added together. This is precisely the chain rule from the previous article, implemented as a dictionary of per-operation rules instead of a single formula.

## Backward is just a reversed topological sort
{: #backward-is-just-a-reversed-topological-sort }

The hard part isn't the derivative rules — it's calling `_backward()` on every node in an order that guarantees a node's `out.grad` is fully accumulated *before* that node propagates it further back. That order is a reverse topological sort of the DAG:

```python
def backward(root):
    topo = []
    visited = set()
    def build(v):
        if v not in visited:
            visited.add(v)
            for child in v._prev:
                build(child)
            topo.append(v)
    build(root)

    root.grad = 1.0
    for node in reversed(topo):
        node._backward()
```

`build()` does a depth-first search and appends a node to `topo` only *after* all its children are appended — so `topo` ends with the root last. Reversing it gives you an order where the root goes first (seeded with gradient 1.0, since `dL/dL = 1`) and every node is processed only after everything that depends on it has already pushed gradient into it. This is exactly what `loss.backward()` does in PyTorch, just with a graph built automatically as you write forward-pass code, and with tensors instead of scalars.

## Failure mode: reusing a node and double-counting
{: #failure-mode-reusing-a-node-and-double-counting }

The bug that catches almost everyone building this for the first time: forgetting to zero out `.grad` before a second `backward()` call, or building a fresh `Value` graph each iteration without resetting old gradients on shared parameters. Because every `_backward()` uses `+=`, calling `backward()` twice on overlapping graphs without zeroing in between silently sums stale and fresh gradients together. The visible symptom is a training loop where loss decreases for a few steps and then starts moving in directions that don't match the math — because the "gradient" being used is actually last step's gradient plus this step's gradient plus the step before that.

The discipline that saves you: zero every parameter's `.grad` at the start of each training step, before the forward pass, not after. This is precisely why every real training loop has a `zero_grad()` call and why it exists at all — it's not boilerplate, it's the reset switch for the `+=` accumulation this whole engine depends on.

## Exercise
{: #exercise }

Implement `__mul__` (shown above) and `__pow__` for integer powers, then verify gradients on `L = (a * b + 3) ** 2` with `a=2, b=-1` by hand, using the chain rule one operation at a time. Then check with your own `Value` class:

```python
a = Value(2.0)
b = Value(-1.0)
c = a * b + 3.0
L = c * c  # stand-in for **2 if you haven't implemented __pow__
backward(L)
print(a.grad, b.grad)
```

Concrete check: `c = a*b + 3 = 1.0`, so `L = c*c = 1.0`, `dL/dc = 2*c = 2.0`. Trace `dc/da = b = -1` and `dc/db = a = 2`, so `dL/da` should print `-2.0` and `dL/db` should print `4.0`. If your numbers differ, the bug is almost always a missing `+=` (overwritten instead of accumulated gradient) — go find it before article 13.


---

[← 11. Backpropagation as Local Blame](/courses/llm-mastery/11-backprop-intuition/)  
[13. Tensor Shapes: The Hidden Curriculum →](/courses/llm-mastery/13-tensors-shapes-discipline/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
