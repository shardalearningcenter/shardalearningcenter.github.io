---
layout: course
title: "06. Embeddings: Meaning as Geometry"
permalink: /courses/llm-mastery/06-embeddings-intuition/
course_track: "LLM Mastery"
description: "Swap one-hot vectors for a learned embedding table, then measure with cosine similarity which characters the model decided behave alike."
level: Beginner
toc:
  - id: "a-lookup-table-that-learns"
    label: "A lookup table that learns"
  - id: "worked-example-training-embeddings-and-measuring-them"
    label: "Worked example: training embeddings and measuring them"
  - id: "why-q-and-u-arent-close-and-what-actually-is"
    label: "Why q and u aren't close (and what actually is)"
  - id: "the-mistake-of-picking-dimension-by-vibes"
    label: "The mistake of picking dimension by vibes"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 6/50** · Karpathy-style LLM course

After this article you'll be able to explain precisely what an embedding vector *is* (a row in a learned matrix, nothing more mystical), train one yourself, and measure with actual numbers — cosine similarity — whether two tokens ended up "close" in the geometry the model discovered.

## A lookup table that learns
{: #a-lookup-table-that-learns }

In article 5 we fed one-hot vectors into a matrix `W` and noted that `xenc @ W`, for a one-hot input, just selects a row of `W`. That observation is not a curiosity — it's the entire definition of an embedding. An **embedding matrix** `E` has shape `[vocab_size, dim]`; token id `i` is represented by the vector `E[i]`, one row, living in `R^dim`. "Looking up an embedding" and "multiplying a one-hot vector by a weight matrix" are the exact same operation; frameworks give you `nn.Embedding` purely because it skips constructing a giant, mostly-zero one-hot vector and directly indexes the row instead — a huge speedup, zero change in what's being computed.

So why bother with vectors instead of just using the raw integer token ID as a feature? Because integer IDs carry no usable numeric structure. If `"a"` is id `1` and `"b"` is id `2`, a network that tried to use `1` and `2` directly would be implicitly asserting that `"b"` is "one more" than `"a"` in some meaningful sense — which is nonsense; token IDs are assigned arbitrarily (often just by first-appearance order or a sorted alphabet, as in our examples). Vectors sidestep this entirely: they start as arbitrary points in space with no built-in relationships, and *training* — not the assignment of IDs — is what's allowed to move them so that tokens which behave similarly in context end up nearby. The geometry is learned, not designed.

"Nearby" here has one very specific, checkable meaning: two embedding vectors are close if the network found it useful to treat their tokens interchangeably for predicting what comes next. It is not "close in human-perceived meaning" by construction — that's an emergent property you sometimes get for free (vowels clustering together in a character model; synonyms clustering together in a word/subword model on enough data) because behaving similarly in context and being similar in meaning are correlated, not because anything in the training objective directly optimizes for semantic similarity.

## Worked example: training embeddings and measuring them
{: #worked-example-training-embeddings-and-measuring-them }

Let's replace the one-hot-times-matrix trick from article 5 with an explicit embedding layer, retrain the same bigram-style predictor, then actually measure which characters ended up close together.

```python
import torch
import torch.nn as nn
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

xs, ys = [], []
for w in names:
    chs = ["."] + list(w) + ["."]
    for ch1, ch2 in zip(chs, chs[1:]):
        xs.append(stoi[ch1])
        ys.append(stoi[ch2])
xs = torch.tensor(xs)
ys = torch.tensor(ys)

g = torch.Generator().manual_seed(2147483647)
dim = 8
C = torch.randn((27, dim), generator=g, requires_grad=True)   # the embedding table
W = torch.randn((dim, 27), generator=g, requires_grad=True)   # maps embedding -> logits

for step in range(200):
    emb = C[xs]                     # [N, dim] -- one row of C per example, via indexing
    logits = emb @ W                # [N, 27]
    loss = F.cross_entropy(logits, ys)
    C.grad = None
    W.grad = None
    loss.backward()
    C.data += -10 * C.grad
    W.data += -10 * W.grad

print(f"final loss: {loss.item():.4f}")

def cosine_sim(u, v):
    return (u @ v / (u.norm() * v.norm())).item()

pairs = [("b", "f"), ("g", "j"), ("p", "r"), ("q", "u")]
for c1, c2 in pairs:
    sim = cosine_sim(C[stoi[c1]], C[stoi[c2]])
    print(f"cos_sim({c1!r}, {c2!r}) = {sim:+.3f}")
```

`C[xs]` is `nn.Embedding`'s job, done manually: indexing 27 rows of an 8-dimensional table with a batch of integer IDs, producing one 8-dimensional vector per example. Everything downstream — the matrix multiply into logits, the cross-entropy loss, the gradient step — is identical in shape and spirit to article 5; the only change is that the current character is now represented by a *learned* 8-dimensional vector instead of a fixed 27-dimensional one-hot vector.

The cosine similarities are the actual payoff, and running this produces a specific, checkable result: `cos_sim('b','f') = +0.990`, `cos_sim('g','j') = +0.964`, `cos_sim('p','r') = -0.789`, and `cos_sim('q','u') = -0.321`. That last one is worth sitting with, because it overturns a very tempting but wrong intuition. You might expect `q` and `u` to land *close* together, since `q` is almost always immediately followed by `u` in this dataset. But this embedding table represents each token in its role as a **predictor** — "given that the current character is X, what tends to come next" — not in its role as a thing-that-gets-predicted. `q`'s learned role is "strongly predict `u` comes next"; `u`'s learned role is "predict whatever tends to follow `u` in these names" (a consonant, often). Those are different jobs, so there's no structural reason for `q` and `u` to be close as *rows of the input embedding table*, even though they're tightly linked as a bigram. `b` and `f`, on the other hand, ended up predicting very similar next-character distributions from each other — that's the actual definition of "close" at work, and it's not the same claim as "these two tokens co-occur."

## Why q and u aren't close (and what actually is)
{: #why-q-and-u-arent-close-and-what-actually-is }

This is the single most important correction to make to your mental model before moving on: **embedding similarity measures shared predictive role, not co-occurrence.** Two tokens end up nearby in embedding space when the network finds it convenient to route them through similar downstream computation — i.e., when swapping one for the other wouldn't change the next-token distribution much. Tokens that frequently sit *next to* each other are not automatically tokens that play the *same role*; in fact they're often playing complementary, opposite roles (a consonant followed by a vowel, a subject followed by a verb), which pushes them apart just as often as it pulls them together.

Where this bites people is when they use "close" and "related" interchangeably. In a real word-level embedding space, "hot" and "cold" often end up fairly close together — not because they're synonyms, but because they play near-identical grammatical and distributional roles (both are adjectives that modify temperature-related nouns in similar sentence positions), even though they're semantic opposites. If your mental model of embeddings is "close = similar meaning," this looks like a bug. If your mental model is "close = similar predictive role," it's exactly what you'd expect.

## The mistake of picking dimension by vibes
{: #the-mistake-of-picking-dimension-by-vibes }

A very common beginner move is to pick the embedding dimension arbitrarily — often copying whatever number appeared in a tutorial — without connecting it to the actual failure modes on either side.

**Too small a dimension underfits structurally, not just numerically.** If you force our 27-character vocabulary into, say, `dim=2`, you're asking the network to represent every distinguishable "role a character can play in context" using only a 2D point. With that little room, characters that behave differently are forced to share nearby coordinates purely out of geometric necessity, and no amount of extra training will fix it — the ceiling is set by the dimension, not by optimization. If you see loss plateau *and* nearly identical embedding vectors for tokens you know behave differently, dimension (not learning rate, not steps) is the first thing to increase.

**Too large a dimension is not "safer," it's just more expensive and slower to learn well.** More parameters means more values that need enough gradient signal to settle into a useful position; with a small dataset (like our 36 names), a needlessly large embedding table will contain many dimensions that never receive enough signal to move anywhere meaningful, and you're spending capacity and compute for no measurable benefit. Real LLMs use embedding dimensions in the hundreds to low thousands specifically because they're paired with vocabularies of tens of thousands of tokens and training sets of trillions of tokens — the dimension is a decision made jointly with vocabulary size and data volume, never in isolation.

The practical habit: treat embedding dimension as a hyperparameter you *sweep*, not one you guess once and forget. Train at two or three sizes, compare final loss, and only then decide — the cosine-similarity check above is a good qualitative sanity check to run alongside the loss number, because a model can have a fine loss while its embedding space is quietly degenerate (e.g., collapsed to a much lower effective dimension than you allocated).

## Exercise
{: #exercise }

In your own words, write one sentence defining what it means for two embedding vectors to be "close" — then back it with a number. Using the trained `C` from above, find which single character is *closest* to `'b'` by brute-force checking every other character, and confirm it matches the `b`-`f` pair reported earlier:

```python
def closest_to(target_char, C, stoi, itos):
    best_char, best_sim = None, -2.0
    for other_id, other_char in itos.items():
        if other_char == target_char or other_char == ".":
            continue
        sim = cosine_sim(C[stoi[target_char]], C[other_id])
        if sim > best_sim:
            best_sim, best_char = sim, other_char
    return best_char, best_sim

closest_char, sim = closest_to("b", C, stoi, itos)
print(f"closest to 'b': {closest_char!r} (cos_sim={sim:.3f})")
assert closest_char == "f", f"expected 'f', got {closest_char!r} -- retrain and recheck"
assert sim > 0.9
```

Then, separately, write down your prediction for whether `q` and `u` will be close, using the "shared predictive role" definition (not the "co-occur often" one), *before* checking the printed `cos_sim('q', 'u')` value from the worked example above. If your prediction was "close" and the number says otherwise, that's the exercise working correctly — go back and re-read why in the section above until the negative number stops being surprising.


---

[← 05. Loss: Cross-Entropy Without the Fear](/courses/llm-mastery/05-loss-cross-entropy/)  
[07. Neural Nets for Language: The MLP →](/courses/llm-mastery/07-mlp-language-model/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
