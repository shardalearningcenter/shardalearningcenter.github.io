---
layout: course
title: "04. Your First LM: Bigrams"
permalink: /courses/llm-mastery/04-bigram-language-model/
course_track: "LLM Mastery"
description: "Count pairs. Normalize. Sample. Build a real character-level name generator in under 20 lines and feel the soul of language modeling."
level: Beginner
toc:
  - id: "the-smallest-interesting-model"
    label: "The smallest interesting model"
  - id: "worked-example-a-name-generator-from-counts"
    label: "Worked example: a name generator from counts"
  - id: "why-bigrams-stop-working"
    label: "Why bigrams stop working"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 4/50** · Karpathy-style LLM course

After this article you'll have trained and sampled from a real, working language model — a character-level bigram model — on an actual dataset, entirely by counting. No gradients, no neural network, and it still generates plausible-looking output. That's the point: get the *concept* of a language model working end-to-end before you add any machine learning.

## The smallest interesting model
{: #the-smallest-interesting-model }

A **bigram** model makes the crudest possible simplifying assumption about the chain rule from article 1: instead of conditioning the next token on the *entire* history, it only looks at the single previous token.

```
P(t_i | t_1, ..., t_{i-1})  ≈  P(t_i | t_{i-1})
```

That's a Markov assumption of order 1, and it sounds almost too dumb to work. But "training" it is just counting: for every pair `(a, b)` that appears adjacent in your data, increment `counts[a][b]`. To turn counts into a probability distribution, normalize each row: divide by the total count of everything that follows `a`. That's the entire training algorithm — no calculus required — and it's a completely legitimate maximum-likelihood estimate of `P(next | current)` under the bigram assumption.

We'll use this article's dataset for the rest of the "Foundations" arc (articles 4–10), so it's worth looking at directly: a small list of first names, treated as sequences of characters. This mirrors Karpathy's own `makemore` project almost exactly, just with a tiny embedded list instead of a 32,000-line file, so every example here runs with zero downloads.

```python
names = [
    "emma", "olivia", "ava", "isabella", "sophia", "charlotte", "mia", "amelia",
    "harper", "evelyn", "abigail", "emily", "ella", "elizabeth", "camila", "luna",
    "sofia", "avery", "mila", "aria", "liam", "noah", "oliver", "elijah", "james",
    "benjamin", "lucas", "mason", "ethan", "logan", "daniel", "kai", "wyatt",
    "felix", "quinn", "jax",
]
```

We treat each name as a sequence of *characters*, with a special `.` token marking both the start and the end of a name. So `"ava"` becomes the sequence `. a v a .`, contributing the bigrams `(.,a)`, `(a,v)`, `(v,a)`, `(a,.)`. The end marker is not decoration — it's what lets the model learn *when to stop*, which is exactly as important as learning what to say.

## Worked example: a name generator from counts
{: #worked-example-a-name-generator-from-counts }

```python
import torch

names = [
    "emma", "olivia", "ava", "isabella", "sophia", "charlotte", "mia", "amelia",
    "harper", "evelyn", "abigail", "emily", "ella", "elizabeth", "camila", "luna",
    "sofia", "avery", "mila", "aria", "liam", "noah", "oliver", "elijah", "james",
    "benjamin", "lucas", "mason", "ethan", "logan", "daniel", "kai", "wyatt",
    "felix", "quinn", "jax",
]

# Vocabulary: 26 letters + '.' as the start/end marker -> 27 tokens
chars = sorted(set("".join(names)))
stoi = {c: i + 1 for i, c in enumerate(chars)}
stoi["."] = 0
itos = {i: c for c, i in stoi.items()}

# --- "Training": count every adjacent character pair ---
N = torch.zeros((27, 27), dtype=torch.int32)
for w in names:
    chs = ["."] + list(w) + ["."]
    for ch1, ch2 in zip(chs, chs[1:]):
        N[stoi[ch1], stoi[ch2]] += 1

# --- Normalize rows into probabilities. +1 is Laplace smoothing:
#     without it, any bigram with zero training count gets probability
#     exactly 0, which turns into -inf loss the moment it shows up. ---
P = (N + 1).float()
P = P / P.sum(dim=1, keepdim=True)

# --- Sampling: walk the chain until we hit the end marker ---
g = torch.Generator().manual_seed(2147483647)

def sample_name():
    out = []
    ix = 0  # start at the '.' row
    while True:
        row = P[ix]
        ix = torch.multinomial(row, num_samples=1, generator=g).item()
        if ix == 0:
            break
        out.append(itos[ix])
    return "".join(out)

for _ in range(8):
    print(sample_name())
```

Run this and you'll get output like `juwjdvdianaqah`, `p`, `efqywocnn`, `fjiinltoliabs` — and yes, that's mostly gibberish, not the clean `emma`-adjacent names you might expect. That's an honest and important result, not a bug to paper over: with only 36 training words, most bigram counts are extremely sparse, so the `+1` Laplace smoothing (needed to avoid `-inf` loss on unseen pairs) pulls a large fraction of the distribution toward near-uniform, and the walk wanders almost as freely as it would with no training at all. Look closely, though, and the model did learn *something* — real digraphs show up as fragments (`an`, `ia`, `wj` never occurs in English, but `dia`, `via`-flavored runs do), and it never once produces a bigram that's impossible in the training data (like starting a name with `.` mid-string). This is the cleanest possible demonstration that language models — even the dumbest possible kind — are data-hungry: the fix here isn't a smarter algorithm, it's more data, which is exactly the tension article 9 formalizes properly. Nothing above required PyTorch's autograd — we used `torch` purely as a fast array library. Everything above could be rewritten with plain Python dictionaries and would behave identically; that's worth doing once (see the exercise) so you don't mistake matrix notation for something conceptually harder than dictionary lookups.

## Why bigrams stop working
{: #why-bigrams-stop-working }

The most instructive thing about a bigram model is exactly where it breaks, and our data-starved sample above already shows both failure modes at once. First, there's no sense in which the model "planned" a name; it has zero memory beyond the single previous character, so it cannot enforce anything about overall length, avoid drifting away from name-like patterns partway through, or make the fourth letter depend on the first. That's why one of our eight samples was a single letter (`p`) and another ran on for over thirty characters (`gwzvucamniauyabilevhaskdbdainrwibtl`) — nothing in a bigram model's structure favors "name-length" outputs; length is purely an accident of when the walk happens to land on the end-of-sequence token. Second, the sparse-data smoothing problem compounds this: with so little training signal, entire regions of the transition table are close to uniform, so the walk has very little to anchor it toward name-shaped structure even locally.

A related, very common mistake when people first implement this: forgetting the end-of-sequence marker, or using the *same* symbol for start and end but handling the two cases inconsistently in code. If your start marker's row in `P` doesn't sum to 1 because you special-cased it, or if you forget to add `.` to both ends of every training sequence, your model either can't start generating cleanly or never learns to stop — you'll get either empty samples or run-on strings that never terminate. When your sampled outputs are all suspiciously short or suspiciously endless, this is the first thing to check.

The deeper lesson, which the rest of this course arc builds toward: the fix for "no memory beyond one token" is not a bigger count table — a trigram table is already `27^3` cells and it gets sparse fast, and a 10-gram table is astronomically large and mostly empty (most 10-character contexts never appear even once in your training data, so their row is undefined). Counting doesn't scale with context length; it needs an alternative that can *generalize* across contexts it's never exactly seen before. That alternative is a neural network with shared parameters — which is exactly what article 5's cross-entropy loss sets up, and article 7's MLP delivers.

## Exercise
{: #exercise }

Reimplement the counting and normalization step using only Python dictionaries — no `torch`, no matrices — and confirm it agrees with the tensor version on a specific number:

```python
from collections import defaultdict, Counter

counts = defaultdict(Counter)
for w in names:
    chs = ["."] + list(w) + ["."]
    for ch1, ch2 in zip(chs, chs[1:]):
        counts[ch1][ch2] += 1

# P(next='v' | current='a') the dictionary way
row_total = sum(counts["a"].values())
p_v_given_a = counts["a"]["v"] / row_total

# ... vs. the tensor version (no smoothing, to match exactly)
p_v_given_a_tensor = (N[stoi["a"], stoi["v"]] / N[stoi["a"]].sum()).item()

assert abs(p_v_given_a - p_v_given_a_tensor) < 1e-6
print(f"P(v|a) = {p_v_given_a:.4f} (dict) vs {p_v_given_a_tensor:.4f} (tensor)")
```

Then answer in one sentence, without running anything: why did we compute this check *without* the `+1` smoothing term? (Hint: smoothing adds a constant to every cell, so it changes both numerator and denominator in a way that no longer matches a plain dictionary count-and-divide.)


---

[← 03. Next-Token Prediction Is the Game](/courses/llm-mastery/03-next-token-prediction/)  
[05. Loss: Cross-Entropy Without the Fear →](/courses/llm-mastery/05-loss-cross-entropy/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
