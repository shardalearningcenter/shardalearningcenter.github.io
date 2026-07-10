---
layout: post
title: "Getting Started with PyTorch for LLMs"
date: 2026-07-10
description: "Tensors, autograd, nn.Module, and a full training loop on real synthetic data — watch loss actually drop and accuracy actually climb."
tags: [pytorch, llm, getting-started]
---

PyTorch is the default dialect for research-flavored deep learning. If you can shape tensors, write a `forward`, and run a training step, you can follow almost any LLM tutorial. This post trains an actual (tiny) classifier to convergence, so you have numbers to check rather than code to take on faith.

## Install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install torch    # see pytorch.org for a CUDA-specific build if you have an NVIDIA GPU
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

`torch.cuda.is_available()` prints `False` on most laptops — that's expected, not broken. Everything below runs fine on CPU; it's small on purpose.

## Tensors

```python
import torch

x = torch.randn(2, 3)       # shape (2, 3)
y = x @ x.T                 # (2, 2)
print(y.shape, y.dtype)

a = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
loss = (a ** 2).sum()
loss.backward()
print(a.grad)                # d(loss)/da == 2*a == [2., 4., 6.]
```

Shapes are a language. Write them in comments until they're muscle memory: `(B, T, C)` for batch, time, channels. A `RuntimeError: shapes cannot be multiplied` is PyTorch telling you exactly where your mental model diverged from reality — read it, don't guess.

## nn.Module in one page

```python
import torch.nn as nn

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
```

## Mini project: train it to convergence and check the numbers

Two Gaussian blobs, one small network, fifty epochs. This is small enough to run in seconds on a CPU and large enough to show a real loss curve.

```python
import torch
import torch.nn as nn
import torch.optim as optim

torch.manual_seed(0)

n = 200
x0 = torch.randn(n // 2, 2) + torch.tensor([-2.0, -2.0])   # class 0, centered at (-2,-2)
x1 = torch.randn(n // 2, 2) + torch.tensor([2.0, 2.0])      # class 1, centered at (2,2)
X = torch.cat([x0, x1])
y = torch.cat([torch.zeros(n // 2), torch.ones(n // 2)]).long()   # CrossEntropyLoss needs Long targets

model = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2))
opt = optim.AdamW(model.parameters(), lr=0.05)

for epoch in range(50):
    logits = model(X)
    loss = nn.functional.cross_entropy(logits, y)
    opt.zero_grad(set_to_none=True)
    loss.backward()
    opt.step()
    if epoch % 10 == 0:
        acc = (logits.argmax(dim=1) == y).float().mean()
        print(f"epoch {epoch:3d}  loss {loss.item():.4f}  acc {acc.item():.2f}")

with torch.no_grad():
    final_acc = (model(X).argmax(dim=1) == y).float().mean()
print(f"final accuracy: {final_acc.item():.2f}")
```

Run it and check two things concretely: the printed `loss` should trend down across epochs (not flat, not `nan`), and `final accuracy` should land at or near `1.00` — the two blobs are far enough apart (centers 4 units apart, unit-variance noise) that a tiny two-layer network separates them almost perfectly. If accuracy stays near `0.50`, something upstream is broken — gradients not flowing, wrong loss, or a shape mismatch silently broadcasting incorrectly — not "the model needs more epochs."

That loop — forward, loss, `zero_grad`, `backward`, `step` — is the heartbeat of every LLM training run, from this ten-line example to a multi-billion parameter model.

## Habits for LLM work

- Use `torch.no_grad()` or `torch.inference_mode()` when evaluating — it skips building the autograd graph, saving memory and time for computations you won't backpropagate through (used above in the final accuracy check).
- Move tensors with `.to(device)` once, near the top; keep the model and every batch on the *same* device — mismatches raise `RuntimeError: Expected all tensors to be on the same device`.
- Log **shapes** when debugging, not just values — `print(x.shape)` finds broadcasting bugs faster than staring at numbers.
- Start CPU-small, like this example; add GPU only once the toy version is verified correct. Debugging correctness and debugging performance are different problems — don't mix them.

## Common footguns

- **Forgetting `zero_grad()`** — gradients *accumulate* by default across `.backward()` calls; skip clearing them and your updates silently compound garbage from previous steps.
- **Wrong target dtype** — `nn.functional.cross_entropy` requires `Long` (integer class index) targets, not `Float`. Passing floats raises a cryptic error or silently misbehaves depending on the PyTorch version.
- **Missing `model.eval()` / `torch.no_grad()` during evaluation** — irrelevant for this tiny model (no dropout or batchnorm), but essential once you add either; forgetting `eval()` leaves dropout active during "evaluation," giving noisy, non-reproducible metrics.
- **Device mismatches** — moving the model to GPU but leaving a batch on CPU (or vice versa) is one of the most common real-world PyTorch errors.
- **Reusing a model/optimizer across notebook cells without resetting** — re-running a training cell without re-initializing `model`/`opt` continues training from wherever it left off, which is easy to mistake for "starting fresh."

## You know you're done when…

- [ ] The printed loss trends downward across the 50 epochs, never flat or `nan`
- [ ] Final accuracy prints at or near `1.00`
- [ ] `torch.cuda.is_available()` correctly reflects your actual hardware, so you're not debugging "slow training" on a CPU-only box expecting GPU speed
- [ ] You can point to the exact three lines where gradients are cleared, computed, and applied
- [ ] You can explain why `y` is `.long()`, not `.float()`, for `cross_entropy`

## Next

[LLM Mastery](/courses/llm-mastery/) — especially articles 11–27 (autograd through GPT internals). Pair with [Getting Started with Python](/2026/07/10/getting-started-with-python/) if the syntax still feels new.
