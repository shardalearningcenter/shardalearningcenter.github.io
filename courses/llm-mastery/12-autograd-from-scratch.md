---
layout: course
title: "12. Micrograd Energy: Autograd From Scratch"
permalink: /courses/llm-mastery/12-autograd-from-scratch/
course_track: "LLM Mastery"
description: "A Value object with .grad is enough to demystify PyTorch."
level: Intermediate
toc:
  - id: "minimal-idea"
    label: "Minimal idea"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 12/50** · Karpathy-style LLM course

A Value object with .grad is enough to demystify PyTorch.

## Minimal idea
{: #minimal-idea }

```python
class Value:
    def __init__(self, data, children=()):
        self.data = data
        self.grad = 0.0
        self._prev = set(children)
        self._backward = lambda: None

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other))
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out
```

Build `*`, `tanh`, `backward()` topological sort. Suddenly `loss.backward()` is not magic.

## Exercise
{: #exercise }

Implement `__mul__` and verify a tiny expression’s gradients by hand.


---

[← 11. Backpropagation as Local Blame](/courses/llm-mastery/11-backprop-intuition/)  
[13. Tensor Shapes: The Hidden Curriculum →](/courses/llm-mastery/13-tensors-shapes-discipline/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
