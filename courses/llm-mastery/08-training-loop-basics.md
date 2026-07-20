---
layout: course
title: "08. The Training Loop, End to End"
permalink: /courses/llm-mastery/08-training-loop-basics/
course_track: "LLM Mastery"
description: "Batch, forward, loss, backward, step. Wire the MLP from article 7 into a real training loop and watch the loss curve actually move."
level: Beginner
toc:
  - id: "the-five-lines-everything-else-decorates"
    label: "The five lines everything else decorates"
  - id: "worked-example-training-the-mlp-and-reading-the-curve"
    label: "Worked example: training the MLP and reading the curve"
  - id: "the-mistake-of-not-watching-the-curve"
    label: "The mistake of not watching the curve"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 8/50** · Karpathy-style LLM course

After this article you'll have taken the MLP from article 7 — sitting at a random, useless initialization — and actually trained it, watching the loss curve fall from "no better than guessing" to "clearly learned something," using nothing but the training loop below. You'll also know what a *healthy* loss curve looks like well enough to spot an unhealthy one on sight.

## The five lines everything else decorates
{: #the-five-lines-everything-else-decorates }

```
for step in range(max_steps):
    x, y = get_batch()          # sample a batch: contexts and their true next tokens
    logits = model(x)           # forward pass
    loss = cross_entropy(logits, y)
    optimizer.zero_grad()       # clear old gradients
    loss.backward()             # backward pass: compute d(loss)/d(every parameter)
    optimizer.step()            # nudge every parameter against its gradient
```

Every training run you will ever hear about — GPT-4's pretraining, a LoRA fine-tune (article 37), an RLHF pass (article 38) — is this loop, with more machinery bolted around it: gradient clipping, learning-rate schedules, mixed precision (article 34), distributed data parallelism across thousands of GPUs (article 33). None of that machinery changes what the loop *is*; it changes how efficiently, stably, and cheaply you can execute it at scale. If you get lost in an advanced training script later in this course, come back to these five lines and find where each one lives in the more complicated code — it's always in there.

Two lines deserve a second look because they're the ones beginners get subtly wrong. `optimizer.zero_grad()` exists because, by default, `.backward()` in PyTorch *accumulates* gradients into `.grad` rather than overwriting them — this is a deliberate feature for advanced use cases (like accumulating gradients over several batches before stepping) but means that if you forget to zero them, every step trains on the *sum* of every gradient computed since the last time you cleared them, silently corrupting your training dynamics without ever raising an error. And `optimizer.step()` moves parameters *against* the gradient (down the loss surface) — a gradient points in the direction of steepest *increase*, so if your update ever accidentally adds instead of subtracts the gradient, loss will rise every step in a way that looks like a bug but is really just backwards math.

## Worked example: training the MLP and reading the curve
{: #worked-example-training-the-mlp-and-reading-the-curve }

Let's wire up the exact MLP from article 7 into a real loop, using `torch.optim` instead of manual parameter updates, and actually watch it learn.

```python
import torch
import torch.nn.functional as F

names = [
    "emma", "olivia", "ava", "isabella", "sophia", "charlotte", "mia", "amelia",
    "harper", "evelyn", "abigail", "emily", "ella", "elizabeth", "camila", "luna",
    "sofia", "avery", "mila", "aria", "liam", "noah", "oliver", "elijah", "james",
    "benjamin", "lucas", "mason", "ethan", "logan", "daniel", "kai", "wyatt",
    "felix", "quinn", "jax",
]
chars = sorted(set("".join(names)))
stoi = {c: i + 1 for i, c in enumerate(chars)}
stoi["."] = 0

block_size = 3

def build_dataset(words):
    X, Y = [], []
    for w in words:
        context = [0] * block_size
        for ch in w + ".":
            ix = stoi[ch]
            X.append(context)
            Y.append(ix)
            context = context[1:] + [ix]
    return torch.tensor(X), torch.tensor(Y)

X, Y = build_dataset(names)

vocab_size, dim, hidden = 27, 10, 64
g = torch.Generator().manual_seed(2147483647)
C = torch.randn((vocab_size, dim), generator=g, requires_grad=True)
W1 = torch.randn((block_size * dim, hidden), generator=g, requires_grad=True)
b1 = torch.randn(hidden, generator=g, requires_grad=True)
W2 = torch.randn((hidden, vocab_size), generator=g, requires_grad=True)
b2 = torch.randn(vocab_size, generator=g, requires_grad=True)
params = [C, W1, b1, W2, b2]

optimizer = torch.optim.SGD(params, lr=0.1)

def get_batch(batch_size=32):
    ix = torch.randint(0, X.shape[0], (batch_size,), generator=g)
    return X[ix], Y[ix]

def model(x):
    emb = C[x].view(x.shape[0], -1)
    h = torch.tanh(emb @ W1 + b1)
    return h @ W2 + b2

losses = []
for step in range(2000):
    x, y = get_batch()
    logits = model(x)
    loss = F.cross_entropy(logits, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    losses.append(loss.item())
    if step % 400 == 0 or step == 1999:
        print(f"step {step:4d}  loss {loss.item():.4f}")

# A cheap but real sanity check: average loss over the LAST 100 steps should
# be well below the average loss over the FIRST 100 steps.
early = sum(losses[:100]) / 100
late = sum(losses[-100:]) / 100
print(f"early avg loss: {early:.3f}   late avg loss: {late:.3f}")
assert late < early - 0.3, "loss should have dropped meaningfully during training"
```

Run this and the printed steps should show loss falling from around `15` at step 0 — recall from article 7 that this architecture's raw random initialization is badly overconfident, not the tidy `ln(27) ≈ 3.30` guessing floor — down to somewhere around `0.4`–`0.6` by step 2000. That number being *below* the guessing floor, not just close to it, tells you the model has gone past "as good as random" and is now confidently, correctly predicting a meaningful fraction of the characters in this small, repetitive dataset (partly genuine pattern-learning, partly the beginning of memorization we'll measure properly in article 9). The `early` vs. `late` assertion at the end turns "did training work" from a vibe you eyeball in a printout into a number you can actually assert on — this is the single habit that separates "I think it trained" from "I verified it trained," and it costs three lines of code.

## The mistake of not watching the curve
{: #the-mistake-of-not-watching-the-curve }

The most expensive mistake at this stage isn't a bug in the loop — it's writing the loop correctly and then not looking at what it produces. A training run that "completes without errors" and a training run that "actually learned something" are completely different claims, and only one of them is checkable by watching the process finish. Always print (or log, or plot) the loss on a regular cadence, and always look at the *shape* of the curve, not just the final number:

- **Steadily decreasing, then flattening** is healthy — the model is learning, then approaching the limit of what this architecture and this data can achieve.
- **Flat from step 0** almost always means the optimizer isn't actually updating parameters — check for a missing `.backward()`, a learning rate of effectively zero, or parameters that were never actually passed to the optimizer (a very common bug: constructing `params` in one place, then accidentally optimizing a *different* list, so gradients compute correctly but nothing you're tracking ever moves).
- **Noisy but flat, never trending down** often means the learning rate is too high for the batch size and the model is bouncing around a region of the loss surface without making net progress — the fix is almost always to lower the learning rate before you touch anything else, a topic article 15 covers in depth.
- **Suddenly spikes to a huge number, or to `nan`,** is the exploding-loss failure mode from article 5 — probability collapsing to exactly zero on some token, usually from too large a learning rate.

A loss curve is the closest thing training has to a heart-rate monitor. Skipping it because "the code ran without an exception" is like skipping a patient's vitals because the machine is plugged in.

## Exercise
{: #exercise }

Without looking back at the code above, write the training loop from memory — the five conceptual lines, filled in with real PyTorch calls for this model. Then compare against the reference and specifically check these three things, which are the most common places a from-memory version goes wrong:

```python
# 1. Did you call optimizer.zero_grad() BEFORE loss.backward(), every step?
# 2. Did you call loss.backward() BEFORE optimizer.step()?
# 3. Are `params` (or your optimizer's tracked parameters) the SAME objects
#    used inside model(x) -- not a copy, not a re-initialized version?

assert all(p.requires_grad for p in params)
assert all(p.grad is not None for p in params), "run at least one step first"
print("all params have gradients attached:", all(p.grad is not None for p in params))
```

If your from-memory version trains but the loss never moves, it is overwhelmingly likely to be one of those three ordering mistakes — find which one before reading any further in this course, since every later training loop (fine-tuning, RLHF, the capstone) is built on top of this exact skeleton staying correct.


---

[← 07. Neural Nets for Language: The MLP](/courses/llm-mastery/07-mlp-language-model/)  
[09. Overfitting, Underfitting, and Data →](/courses/llm-mastery/09-overfitting-underfitting/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
