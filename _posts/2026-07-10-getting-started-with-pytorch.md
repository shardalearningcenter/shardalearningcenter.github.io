---
layout: post
title: "Getting Started with PyTorch for LLMs"
date: 2026-07-10
description: "Tensors, autograd, nn.Module, and a tiny training step — the PyTorch dialect used throughout LLM Mastery."
tags: [pytorch, llm, getting-started]
---

PyTorch is the default dialect for researchy deep learning. If you can shape tensors, write a `forward`, and run a training step, you can follow almost any LLM tutorial.

## Install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install torch  # see pytorch.org for CUDA builds
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

## Tensors

```python
import torch

x = torch.randn(2, 3)       # shape (2, 3)
y = x @ x.T                 # (2, 2)
print(y.shape, y.dtype)

a = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
loss = (a ** 2).sum()
loss.backward()
print(a.grad)               # d(loss)/da
```

Shapes are a language. Write them in comments until they become muscle memory: `(B, T, C)` for batch, time, channels.

## nn.Module in one page

```python
import torch.nn as nn
import torch.optim as optim

class TinyMLP(nn.Module):
    def __init__(self, d_in: int, d_hid: int, d_out: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_in, d_hid),
            nn.ReLU(),
            nn.Linear(d_hid, d_out),
        )

    def forward(self, x):
        return self.net(x)

model = TinyMLP(16, 32, 4)
opt = optim.AdamW(model.parameters(), lr=1e-3)
x = torch.randn(8, 16)
y = torch.randint(0, 4, (8,))
logits = model(x)
loss = nn.functional.cross_entropy(logits, y)
opt.zero_grad(set_to_none=True)
loss.backward()
opt.step()
print(float(loss))
```

That loop — forward, loss, backward, step — is the heartbeat of every LLM training run.

## Habits for LLM work

- Prefer `torch.no_grad()` / `torch.inference_mode()` when evaluating
- Move tensors with `.to(device)` once; keep the model and batch on the same device
- Log **shapes** when debugging, not just values
- Start CPU-small; add GPU when the toy version works

## Next

[LLM Mastery](/courses/llm-mastery/) — especially articles 11–27 (autograd through GPT guts). Pair with [Python](/blog/2026/07/10/getting-started-with-python/) if the syntax still feels new.
