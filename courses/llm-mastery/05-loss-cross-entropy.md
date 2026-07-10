---
layout: course
title: "05. Loss: Cross-Entropy Without the Fear"
permalink: /courses/llm-mastery/05-loss-cross-entropy/
course_track: "LLM Mastery"
description: "Score the bigram model's counts as a loss number, then rediscover the same model with gradient descent instead of counting. Cross-entropy is just how surprised the model was."
level: Beginner
toc:
  - id: "surprise-measured-in-nats"
    label: "Surprise, measured in nats"
  - id: "worked-example-scoring-then-learning-the-same-model"
    label: "Worked example: scoring, then learning, the same model"
  - id: "the-mistake-that-produces-inf"
    label: "The mistake that produces inf"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 5/50** · Karpathy-style LLM course

After this article you'll be able to compute cross-entropy loss by hand from raw probabilities, explain precisely what a loss of 2.45 versus 4.9 means, and — this is the payoff — train a single-layer neural network with gradient descent that converges to the *exact same numbers* as the counting-based bigram model from article 4. That equivalence is the moment counting-based language modeling and neural language modeling turn out to be the same idea wearing different clothes.

## Surprise, measured in nats
{: #surprise-measured-in-nats }

Cross-entropy loss answers one question, per token: *how surprised was the model by the token that actually came next?* If the model assigned probability `p` to the correct token, its loss at that position is `-log(p)`. Sit with why, briefly: when `p = 1.0` (total confidence, and it was right), `-log(1.0) = 0` — no surprise, no loss. As `p` shrinks toward 0, `-log(p)` grows without bound — the model was confidently wrong, and it's punished severely, not mildly, for that confidence. This is why cross-entropy is a much better training signal than something like accuracy: a model that puts `0.4` on the right answer and one that puts `0.001` on it are *both wrong* under accuracy, but cross-entropy correctly treats the second as a far more serious failure.

```
p = 1.0  -> loss = -log(1.0)  = 0.000   (perfect)
p = 0.5  -> loss = -log(0.5)  = 0.693
p = 0.1  -> loss = -log(0.1)  = 2.303
p = 0.01 -> loss = -log(0.01) = 4.605   (confidently wrong)
p -> 0   -> loss -> infinity
```

Average `-log(p)` over every token in your dataset (where `p` is always the probability the model assigned to the *actual* next token at that position) and you get the **negative log-likelihood**, which is what people mean when they casually say "the loss." Lower is better, 0 is the unreachable floor, and — this is the detail that makes it directly interpretable — a loss of `L` nats means the model was, on average, about as surprised as if it were choosing uniformly among `e^L` equally likely options. A loss around `ln(27) ≈ 3.3` on our 27-token name vocabulary is exactly what you'd get from a model that has learned *nothing* and guesses uniformly; anything meaningfully below that means it has actually learned structure.

Where does `p` come from mechanically? The network doesn't output probabilities directly — it outputs raw, unconstrained real numbers called **logits**, one per vocabulary entry. **Softmax** converts logits into a valid probability distribution: exponentiate each logit (which makes everything positive) and divide by the sum (which makes them sum to 1). Cross-entropy loss is almost always computed as "softmax, then compare to the true token" fused into a single numerically stable operation — that's exactly what `torch.nn.functional.cross_entropy` does, and why you'll see it take raw logits, never pre-softmaxed probabilities, as input.

## Worked example: scoring, then learning, the same model
{: #worked-example-scoring-then-learning-the-same-model }

First, let's *score* the counting-based bigram model from article 4 — turn its quality into a single loss number.

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
itos = {i: c for c, i in stoi.items()}

N = torch.zeros((27, 27), dtype=torch.int32)
for w in names:
    chs = ["."] + list(w) + ["."]
    for ch1, ch2 in zip(chs, chs[1:]):
        N[stoi[ch1], stoi[ch2]] += 1
P = (N + 1).float()
P = P / P.sum(dim=1, keepdim=True)

log_likelihood = 0.0
n = 0
for w in names:
    chs = ["."] + list(w) + ["."]
    for ch1, ch2 in zip(chs, chs[1:]):
        prob = P[stoi[ch1], stoi[ch2]]
        log_likelihood += torch.log(prob)
        n += 1
nll = -log_likelihood / n
print(f"counting-based bigram loss (with +1 smoothing): {nll.item():.4f}")   # ~2.46
```

That `~2.46` is worse than it should be, and the reason is instructive: with only 36 tiny training words, most rows of the count table are extremely sparse, and Laplace smoothing adds `+1` to *every* cell regardless of how little data that row had — which, on a dataset this small, meaningfully drags the whole distribution toward uniform. If you rerun the exact same loop with `P = N.float(); P = P / P.sum(dim=1, keepdim=True)` (no `+1`), you'll get a noticeably lower, more honest `~1.69`, at the cost of assigning probability exactly 0 to any bigram that never appeared in training — which is exactly the "loss becomes infinite the moment it shows up" trap this article opened with. Smoothing is a real trade-off, not a free lunch: safety against `-inf` in exchange for a worse fit to the data you actually have.

Now the interesting part. Instead of counting, let's *learn* the bigram probabilities with gradient descent on a single trainable matrix `W`, using one-hot vectors as input and cross-entropy as the loss. This is not a different model — a bigram table and a single linear layer with no bias, fed a one-hot current-character vector, are mathematically the same function. And it sidesteps the smoothing trade-off entirely: softmax is a sum of exponentials, so it mathematically cannot output an exact 0 for any token, no matter how untrained the weights — no bigram ever gets a hard-zero probability, with no explicit smoothing term required. Let's watch gradient descent find a solution close to the *unsmoothed* counting optimum, purely by minimizing cross-entropy.

```python
# Build the full (context, target) training pairs.
xs, ys = [], []
for w in names:
    chs = ["."] + list(w) + ["."]
    for ch1, ch2 in zip(chs, chs[1:]):
        xs.append(stoi[ch1])
        ys.append(stoi[ch2])
xs = torch.tensor(xs)
ys = torch.tensor(ys)

xenc = F.one_hot(xs, num_classes=27).float()   # shape [N, 27]

g = torch.Generator().manual_seed(2147483647)
W = torch.randn((27, 27), generator=g, requires_grad=True)

for step in range(300):
    logits = xenc @ W                 # shape [N, 27] -- raw scores
    loss = F.cross_entropy(logits, ys)
    W.grad = None
    loss.backward()
    W.data += -10 * W.grad            # gradient descent step

    if step % 100 == 0 or step == 299:
        print(f"step {step:3d}  loss {loss.item():.4f}")
```

Watch the printed losses: they descend from `3.7568` (random init — worse than the `ln(27) ≈ 3.30` guessing floor, purely because this particular random `W` happened to start unlucky) down to `1.7253` by step 300 — landing right next to the `~1.69` *unsmoothed* counting optimum we computed above, not the smoothed `2.46` one. `xenc @ W` for a one-hot input `x` just *selects a row of `W`* — that row is, after training, functionally the same as a row of log-probabilities in the counting table. Gradient descent found the counts by trial and error, driven purely by "reduce cross-entropy," because for this simple a model, minimizing cross-entropy *is* maximum-likelihood estimation, and maximum-likelihood estimation *is* counting-and-normalizing. This equivalence stops holding once the model gets more expressive than a lookup table — which is precisely why articles 6 onward introduce embeddings and MLPs — but it's the cleanest possible proof that "train with gradients" and "count frequencies" are not two different philosophies of language modeling; they're the same objective, solved two different ways.

## The mistake that produces inf
{: #the-mistake-that-produces-inf }

The single most common bug beginners hit here is `loss = inf` or `loss = nan`, and it has one recurring cause: a token that had probability *exactly* zero under the model got asked to be the correct answer. `-log(0)` is `inf` in exact math, and floating point makes it either `inf` or a `nan` a step later once it propagates through a gradient update. In the counting-based model, this happens when Laplace smoothing (the `+1` in article 4) is forgotten or applied inconsistently, and some bigram in your evaluation set simply never appeared during training. In the gradient-based model, it more often shows up as an exploding learning rate: if the gradient step is too large, `W` can blow up to extreme values, softmax saturates so hard that some probabilities round to exactly 0.0 in float32, and the very next cross-entropy computation on that token is `-log(0.0) = inf`.

The fix in both cases is the same instinct: never let a probability that matters to you be permitted to reach exactly zero. Smoothing does this for counting models. For gradient-based models, this is one of the reasons for the learning-rate discipline and initialization care we'll cover properly in articles 15 and 16 — for now, if your loss ever prints `nan`, the first thing to check is whether your learning rate is too large for the scale of your gradients, not whether your model architecture is wrong.

## Exercise
{: #exercise }

Compute, entirely by hand (then verify in code), the per-token loss if a model assigns probability `0.1` to the correct token, using the *natural* log (not log base 10 — cross-entropy in every deep learning framework uses natural log, and mixing them up is a classic silent bug):

```python
import math

p = 0.1
loss_by_hand = -math.log(p)
print(f"{loss_by_hand:.4f}")   # should be ~2.3026

assert abs(loss_by_hand - 2.302585) < 1e-4

# Now confirm it matches torch's cross_entropy on a single example.
import torch
import torch.nn.functional as F

logits = torch.tensor([[0.0, 0.0]])          # two-token toy vocab, equal logits
logits[0, 0] = math.log(0.1) - math.log(0.9)  # rig softmax to output [0.1, 0.9]
target = torch.tensor([0])                    # correct answer is token 0, p=0.1
loss = F.cross_entropy(logits, target)
assert abs(loss.item() - loss_by_hand) < 1e-3
print(f"cross_entropy agrees: {loss.item():.4f}")
```

If the two numbers don't match, the bug is almost always a `log` base mix-up or a probability-versus-logit mix-up — check both before assuming anything more exotic is wrong.


---

[← 04. Your First LM: Bigrams](/courses/llm-mastery/04-bigram-language-model/)  
[06. Embeddings: Meaning as Geometry →](/courses/llm-mastery/06-embeddings-intuition/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
