---
layout: course
title: "10. The MakeMore Mindset: Build Tiny, Understand Deeply"
permalink: /courses/llm-mastery/10-makemore-mindset/
course_track: "LLM Mastery"
description: "Six articles of pieces, assembled into one working sampler, plus the checklist for building your own toy language model on any tiny dataset you choose."
level: Beginner
toc:
  - id: "why-toy-models-are-not-a-lesser-version-of-the-real-thing"
    label: "Why toy models are not a lesser version of the real thing"
  - id: "worked-example-the-whole-pipeline-in-one-script"
    label: "Worked example: the whole pipeline in one script"
  - id: "the-mistake-of-skipping-straight-to-scale"
    label: "The mistake of skipping straight to scale"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 10/50** · Karpathy-style LLM course

After this article you'll have one complete script — tokenizer, dataset builder, model, training loop, sampler — that you personally assembled piece by piece across articles 4 through 9, and a concrete checklist for pointing that same script at a new toy dataset of your choosing and shipping a working sampler within a week.

## Why toy models are not a lesser version of the real thing
{: #why-toy-models-are-not-a-lesser-version-of-the-real-thing }

If you can't train a name generator on three dozen examples, you don't yet understand GPT-4 — you understand its press release. That's not a rhetorical flourish; it's a literal claim about what's transferable. Every mechanism a frontier model uses to go from raw text to fluent output — tokenization, embeddings, a forward pass through learned weights, a softmax over a vocabulary, cross-entropy loss, gradient descent, a train/validation split — is present, unabbreviated, in the 36-name character model you built across the last six articles. Scale changes the *numbers*: vocabulary size, embedding dimension, number of layers, dataset size, compute budget. It does not change which mechanisms are present or how they compose. A tiny model that you built, broke, and fixed yourself teaches you things a frontier model's API never will, because the API hides every one of those mechanisms behind a text box.

This is deliberate methodology, not a beginner's stepping stone you graduate away from. Toy problems force four things into direct view that large-scale training obscures behind engineering complexity and compute cost: the actual **shapes** of your tensors at every step (article 7's flatten step, article 13's whole focus), what a **loss curve** genuinely looks like when something is wrong versus healthy (article 8, article 9), how **sampling** feels when you change temperature or model capacity (article 3, article 4), and — the most valuable of all — where **bugs hide**, because at this scale you can actually find them by inspection rather than by faith in a framework. A silent shape-swap bug (article 7) that would take days to notice in a billion-parameter run announces itself almost immediately in a 36-name dataset, because the outputs are small enough to read directly.

## Worked example: the whole pipeline in one script
{: #worked-example-the-whole-pipeline-in-one-script }

Here is everything from articles 4 through 9, assembled into one script that trains and then generates novel names. Nothing here is new — it's the same pieces, wired together end to end.

```python
import random
import torch
import torch.nn.functional as F

names = [
    "emma", "olivia", "ava", "isabella", "sophia", "charlotte", "mia", "amelia",
    "harper", "evelyn", "abigail", "emily", "ella", "elizabeth", "camila", "luna",
    "sofia", "avery", "mila", "aria", "liam", "noah", "oliver", "elijah", "james",
    "benjamin", "lucas", "mason", "ethan", "logan", "daniel", "kai", "wyatt",
    "felix", "quinn", "jax",
]

# 1. Tokenizer (article 2/4): characters -> integer IDs, '.' = start/end
chars = sorted(set("".join(names)))
stoi = {c: i + 1 for i, c in enumerate(chars)}
stoi["."] = 0
itos = {i: c for c, i in stoi.items()}
vocab_size = len(itos)

# 2. Dataset (article 7): sliding context windows
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

shuffled = names[:]
random.Random(0).shuffle(shuffled)
n_val = 6
Xtr, Ytr = build_dataset(shuffled[n_val:])
Xval, Yval = build_dataset(shuffled[:n_val])

# 3. Model (article 6/7): embedding + MLP
dim, hidden = 10, 32
g = torch.Generator().manual_seed(2147483647)
C = torch.randn((vocab_size, dim), generator=g, requires_grad=True)
W1 = torch.randn((block_size * dim, hidden), generator=g, requires_grad=True)
b1 = torch.randn(hidden, generator=g, requires_grad=True)
W2 = torch.randn((hidden, vocab_size), generator=g, requires_grad=True)
b2 = torch.randn(vocab_size, generator=g, requires_grad=True)
params = [C, W1, b1, W2, b2]

def model(x):
    emb = C[x].view(x.shape[0], -1)
    h = torch.tanh(emb @ W1 + b1)
    return h @ W2 + b2

# 4. Training loop (article 8), with a train/val check (article 9)
optimizer = torch.optim.SGD(params, lr=0.1)
for step in range(800):
    logits = model(Xtr)
    loss = F.cross_entropy(logits, Ytr)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if step % 200 == 0 or step == 799:
        with torch.no_grad():
            val_loss = F.cross_entropy(model(Xval), Yval)
        print(f"step {step:4d}  train {loss.item():.4f}  val {val_loss.item():.4f}")

# 5. Sampler (article 3/4): autoregressive generation from the trained model
def sample_name(seed):
    rng = torch.Generator().manual_seed(seed)
    context = [0] * block_size
    out = []
    with torch.no_grad():
        while True:
            logits = model(torch.tensor([context]))
            probs = F.softmax(logits, dim=1)
            ix = torch.multinomial(probs, num_samples=1, generator=rng).item()
            if ix == 0:
                break
            out.append(itos[ix])
            context = context[1:] + [ix]
    return "".join(out)

print("\nsampled names:")
for seed in range(10):
    print(" ", sample_name(seed))
```

Run the whole thing and you'll see:

```
step    0  train 11.6685  val  9.7230
step  200  train  1.6499  val  4.5019
step  400  train  0.9924  val  4.1931
step  600  train  0.7819  val  4.2501
step  799  train  0.7101  val  4.3555

sampled names:
  benr
  hares
  isabeth
  elia
  benjamih
  ethai
  lunj
  aja
  oliv
```

Training loss falls hard, validation loss falls too then plateaus — a mild, expected version of the overfitting from article 9, since 30 training words is still not a lot for even this small a model — and then nine of the ten sampled strings are novel, name-shaped character sequences that never appeared in the training list, generated one character at a time from a model that learned everything it knows from 30 training examples. `benjamih` and `ethai` are visibly "near" real training names (`benjamin`, `ethan`) without being exact copies — that's generalization, caught in the act, not memorization. That's the complete arc of articles 1 through 9, compressed into roughly sixty lines you can read start to finish in a few minutes.

## The mistake of skipping straight to scale
{: #the-mistake-of-skipping-straight-to-scale }

The most common way people waste weeks at this stage of learning is skipping tiny models entirely and jumping straight to fine-tuning a large pretrained model, on the theory that toy problems are "beginner stuff" you graduate past once you understand the concepts in the abstract. This backfires for a specific, mechanical reason: at large scale, a training run failing to learn well looks *identical*, from the outside, to a training run that's merely slow, or under-trained, or has a subtly wrong hyperparameter. A 3-hour, $200 training run that produces a mediocre model gives you almost no diagnostic signal about *which* of a dozen possible causes is responsible, and re-running it to test one hypothesis at a time is expensive enough that most people don't.

A tiny model sidesteps this entirely because every run costs seconds and every intermediate value is small enough to print and read. If your MLP-on-names loss curve looks wrong, you can test five different hypotheses (learning rate, initialization, a shape bug, insufficient capacity, a data-loading mistake) in the time it takes a large run to finish loading its checkpoint. The skill you're building by working through tiny models first is not "how to generate names" — it's "how to recognize, within seconds, which of the handful of usual-suspect failure modes is responsible for a bad loss curve." That skill transfers directly and is precisely what separates someone who can debug a stalled fine-tuning run from someone who can only restart it and hope.

The curriculum this course follows from here builds in exactly that spirit, each stage staying small enough to fully inspect before growing: bigrams (article 4) exposed the counting-vs-generalization ceiling; the MLP (article 7) fixed generalization but is still capped by a fixed context window; a tiny transformer (articles 21–27) replaces that fixed window with attention, letting context length grow without the input size exploding; and only once all of that is solid does "scale up carefully" (articles 30, 32–34) become a reasonable next move rather than a way to hide bugs under more compute.

## Exercise
{: #exercise }

Pick a different tiny dataset — city names, dog breeds, Pokémon, anything with a few dozen short strings you can type into a Python list — and adapt the script above to it. Commit to a concrete, checkable definition of "done" before you start, not just "it looks kind of name-like":

```python
# Concrete check 1: training loss should drop well below the "guessing" floor.
guess_floor = torch.log(torch.tensor(float(vocab_size)))  # ln(vocab_size)
assert loss.item() < guess_floor.item() - 0.5, "model should clearly beat random guessing"

# Concrete check 2: at least 7 of 10 sampled outputs should be genuinely NEW
# strings -- not verbatim copies of your training data (a sign of overfitting,
# straight out of article 9).
samples = [sample_name(seed) for seed in range(10)]
novel = [s for s in samples if s not in shuffled]
assert len(novel) >= 7, f"too many exact copies of training data: {samples}"
print(f"{len(novel)}/10 samples were novel: {novel}")
```

Ship it this week — a working sampler on a dataset you chose, passing both checks above. That's the actual milestone this entire "Foundations" arc (articles 1–10) has been building toward: not reading about language models, but having personally trained and sampled from one, with numbers you can point to proving it generalized rather than memorized.


---

[← 09. Overfitting, Underfitting, and Data](/courses/llm-mastery/09-overfitting-underfitting/)  
[11. Backpropagation as Local Blame →](/courses/llm-mastery/11-backprop-intuition/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
