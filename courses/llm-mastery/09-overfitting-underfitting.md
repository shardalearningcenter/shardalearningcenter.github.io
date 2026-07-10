---
layout: course
title: "09. Overfitting, Underfitting, and Data"
permalink: /courses/llm-mastery/09-overfitting-underfitting/
course_track: "LLM Mastery"
description: "Split train from val, watch one curve fall and the other rise, and see memorization happen to numbers you can point at."
level: Beginner
toc:
  - id: "two-ways-to-fail"
    label: "Two ways to fail"
  - id: "worked-example-making-the-mlp-overfit-on-purpose"
    label: "Worked example: making the MLP overfit on purpose"
  - id: "the-mistake-of-tuning-on-the-test-set"
    label: "The mistake of tuning on the test set"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 9/50** · Karpathy-style LLM course

After this article you'll be able to split a dataset into train and validation sets correctly, deliberately induce overfitting in a small model so you've *seen* the telltale diverging curves with your own eyes, and explain precisely why "the model does great on my benchmark" is a much weaker claim than most people treat it as.

## Two ways to fail
{: #two-ways-to-fail }

A model can fail to be useful in exactly two directions, and they have opposite fixes, which is why diagnosing which one you have is the first step, not an afterthought.

**Underfitting**: training loss is high, meaning the model does poorly even on the data it was directly trained on. The model is too weak for the pattern in the data (too few parameters, too little training, too small a context window), or it hasn't been trained long enough to reach the capacity it does have. The fix is some combination of a bigger model, more training steps, or a better-tuned learning rate — the model hasn't yet run out of things to learn from the data it's already seeing.

**Overfitting**: training loss is low, but loss on data the model *never saw during training* is much higher. This is memorization, not generalization — the model has effectively encoded specifics of the training examples (sometimes close to verbatim) rather than the underlying pattern that would transfer to new examples. The fix is more/better data, regularization (dropout, weight decay — article 17), or simply stopping training earlier, before the gap between train and validation performance widens.

The reason you need *two* numbers, not one, to tell these apart is the entire point of a train/validation split: hold out a portion of your data that the model never trains on, and compare loss on that held-out set against loss on the training set itself. Training loss alone can't distinguish "genuinely learned" from "memorized" — both look identical on the data that was memorized. It's only by checking performance on data the model has never touched that the difference becomes visible.

This matters enormously at LLM scale, not just in toy examples. Models trained on internet-scale corpora still memorize substantial amounts of their training data — sometimes usefully (memorized facts are often exactly what you want), sometimes not (a chatbot that can reproduce a paragraph of copyrighted text verbatim). And a subtler, very real failure specific to LLMs: if a benchmark's test questions leaked into the pretraining corpus (a well-documented, ongoing problem for widely-used public benchmarks), the model's high score on that benchmark isn't measuring generalization at all — it may just be measuring memorization of the answer key, and you cannot tell the difference from the score alone.

## Worked example: making the MLP overfit on purpose
{: #worked-example-making-the-mlp-overfit-on-purpose }

The clearest way to *recognize* overfitting later is to have deliberately caused it once. Our 36-name dataset is small enough that a moderately oversized MLP will overfit it quickly and visibly.

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

g = torch.Generator().manual_seed(2147483647)
shuffled = names[:]
import random
random.Random(0).shuffle(shuffled)
n_val = 6
train_words, val_words = shuffled[n_val:], shuffled[:n_val]

Xtr, Ytr = build_dataset(train_words)
Xval, Yval = build_dataset(val_words)
print(f"train examples: {Xtr.shape[0]}   val examples: {Xval.shape[0]}")

vocab_size, dim, hidden = 27, 10, 300   # deliberately oversized hidden layer
C = torch.randn((vocab_size, dim), generator=g, requires_grad=True)
W1 = torch.randn((block_size * dim, hidden), generator=g, requires_grad=True)
b1 = torch.randn(hidden, generator=g, requires_grad=True)
W2 = torch.randn((hidden, vocab_size), generator=g, requires_grad=True)
b2 = torch.randn(vocab_size, generator=g, requires_grad=True)
params = [C, W1, b1, W2, b2]
optimizer = torch.optim.SGD(params, lr=0.1)

def model(x):
    emb = C[x].view(x.shape[0], -1)
    h = torch.tanh(emb @ W1 + b1)
    return h @ W2 + b2

for step in range(3000):
    logits = model(Xtr)
    loss = F.cross_entropy(logits, Ytr)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if step % 500 == 0 or step == 2999:
        with torch.no_grad():
            val_loss = F.cross_entropy(model(Xval), Yval)
        print(f"step {step:4d}  train {loss.item():.4f}  val {val_loss.item():.4f}")
```

Watch the two numbers on the right diverge as training proceeds:

```
step    0  train 33.2662  val 22.6676
step  500  train 0.6112   val  9.8384
step 1000  train 0.6091   val  9.9354
step 2000  train 0.6079   val 10.0312
step 2999  train 0.6074   val 10.1059
```

Train loss grinds all the way down to `~0.61` — genuinely low, well below what a model with real generalization would need to achieve on this little data — while validation loss doesn't just fail to improve, it actively *rises* over the same stretch, from `9.84` to `10.11`, even as train loss keeps inching down. That's the classic overfitting signature, and it isn't a hypothetical here: with `hidden=300` and only 30 training words, the network has more than enough capacity to essentially memorize the specific context-to-next-character patterns of those 30 names rather than the general character-sequence structure of names as a category, and the widening train/val gap is the direct, numeric evidence of exactly that happening.

## The mistake of tuning on the test set
{: #the-mistake-of-tuning-on-the-test-set }

Beyond simple overfitting, there's a more insidious version of the same failure that even careful practitioners fall into: **repeatedly checking performance on your "held-out" set and adjusting the model in response.** The moment you use validation performance to make a decision — pick a hyperparameter, choose when to stop, select a checkpoint — that set has started leaking information into your modeling choices, even though the model's *weights* never directly trained on it. Do this enough times across enough experiments and your validation number quietly stops measuring generalization to unseen data and starts measuring how well you've hill-climbed against that one specific held-out sample.

The standard fix is a **three-way split**: train, validation, and test. You tune everything — architecture, hyperparameters, when to stop — against the validation set, as much as you need to. But the test set is touched exactly once, at the very end, to report a final number, and never used to make any decision that feeds back into the model. If you find yourself re-checking the test set and adjusting anything in response to what you see, you no longer have a test set — you have a second validation set that you're calling something else, and your final reported number is now optimistic in a way you can't quantify.

This exact dynamic, scaled up, is precisely what benchmark contamination does to public LLM leaderboards: if a benchmark's answers were in the pretraining data, or if labs (even unintentionally) select checkpoints based on that benchmark's score, the reported number stops being a clean measurement of capability and starts being, at least partly, a measurement of how well that specific benchmark was fit. This is why serious evaluation work (article 35) treats held-out, uncontaminated test sets as a genuinely scarce and valuable resource, not something to check casually.

## Exercise
{: #exercise }

Using the train/val setup above, record the `(train_loss, val_loss)` gap at every logged step, and verify with an assertion — not an eyeball check — that it widens over training:

```python
def gap(train_loss, val_loss):
    return val_loss - train_loss

history = []
for step in range(3000):
    logits = model(Xtr)
    loss = F.cross_entropy(logits, Ytr)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if step % 500 == 0 or step == 2999:
        with torch.no_grad():
            val_loss = F.cross_entropy(model(Xval), Yval)
        history.append((loss.item(), val_loss.item()))

assert gap(*history[-1]) > gap(*history[1]), "expected the train/val gap to widen after early training"
print("gap at step 500:", round(gap(*history[1]), 3))
print("gap at step 2999:", round(gap(*history[-1]), 3))
```

Then, without changing anything else, cut `hidden` from `300` down to `20`, retrain **from scratch** (a fresh `torch.Generator` seed, fresh `C`/`W1`/`b1`/`W2`/`b2`), and compare the *final* gap against the `hidden=300` run. Wrap the whole training procedure in a function so "from scratch" actually means from scratch, not continuing whatever state is left over in your session:

```python
def train_and_get_final_gap(hidden, steps=3000, seed=2147483647):
    g2 = torch.Generator().manual_seed(seed)
    dim = 10
    C2 = torch.randn((27, dim), generator=g2, requires_grad=True)
    W1_ = torch.randn((block_size * dim, hidden), generator=g2, requires_grad=True)
    b1_ = torch.randn(hidden, generator=g2, requires_grad=True)
    W2_ = torch.randn((hidden, 27), generator=g2, requires_grad=True)
    b2_ = torch.randn(27, generator=g2, requires_grad=True)
    opt = torch.optim.SGD([C2, W1_, b1_, W2_, b2_], lr=0.1)

    def m(x):
        emb = C2[x].view(x.shape[0], -1)
        h = torch.tanh(emb @ W1_ + b1_)
        return h @ W2_ + b2_

    for _ in range(steps):
        tr_loss = F.cross_entropy(m(Xtr), Ytr)
        opt.zero_grad()
        tr_loss.backward()
        opt.step()
    with torch.no_grad():
        va_loss = F.cross_entropy(m(Xval), Yval)
    return gap(tr_loss.item(), va_loss.item())

gap_hidden_300 = train_and_get_final_gap(hidden=300)
gap_hidden_20 = train_and_get_final_gap(hidden=20)
print(f"final gap, hidden=300: {gap_hidden_300:.3f}")
print(f"final gap, hidden=20:  {gap_hidden_20:.3f}")
assert gap_hidden_20 < gap_hidden_300, "a smaller model should have less room to memorize"
```

A smaller model has less capacity to memorize, so its final gap should shrink — and it does, roughly in half in this setup (`~9.50` down to `~4.95`). If your numbers disagree with that direction, that's a real signal something else (learning rate, data split, or a bug in how you're measuring the gap) is dominating the effect you're trying to observe, and worth chasing down before you trust any other result from this setup.


---

[← 08. The Training Loop, End to End](/courses/llm-mastery/08-training-loop-basics/)  
[10. The MakeMore Mindset: Build Tiny, Understand Deeply →](/courses/llm-mastery/10-makemore-mindset/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
