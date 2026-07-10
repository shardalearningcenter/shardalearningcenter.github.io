---
layout: course
title: "03. Next-Token Prediction Is the Game"
permalink: /courses/llm-mastery/03-next-token-prediction/
course_track: "LLM Mastery"
description: "Implement the autoregressive sampling loop, teacher forcing, and temperature by hand. Everything — chat, code, agents — is still next-token prediction underneath."
level: Beginner
toc:
  - id: "one-loop-to-rule-generation"
    label: "One loop to rule generation"
  - id: "worked-example-sampling-with-temperature"
    label: "Worked example: sampling with temperature"
  - id: "the-training-inference-mismatch"
    label: "The training/inference mismatch"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 3/50** · Karpathy-style LLM course

After this article you'll be able to write the autoregressive generation loop from memory, explain teacher forcing precisely enough to spot when it's *not* happening, and implement temperature and top-p sampling as short, testable functions.

## One loop to rule generation
{: #one-loop-to-rule-generation }

Every LLM demo you've ever seen — chat, code completion, agent tool calls — is the exact same six-line loop underneath, just with a very expensive `model()` call inside it:

```
context = [BOS]
while not done:
    logits = model(context)          # a score for every token in the vocabulary
    probs  = softmax(logits[-1])     # turn scores into a probability distribution
    next_t = sample(probs)           # draw one token (greedy, or randomly)
    context.append(next_t)
```

That's it. There is no separate "reasoning module" or "planning step" bolted onto this loop for a base model — chat formatting, retrieved documents (article 40), and tool outputs (article 41) are all just *more tokens appended to `context`* before the next call. If you understand this loop cold, you understand the mechanical skeleton of every LLM product you will ever use, no matter how much marketing copy sits on top of it.

Two words carry all the weight here: **autoregressive** means each new token is generated conditioned on every token generated so far — the model consumes its own previous output as input. **Sample** is doing more work than it looks like; `probs` is a distribution over the *entire vocabulary* every single step, and how you draw from it (always take the max? draw randomly in proportion to probability? something in between?) has a dramatic effect on the character of the output, independent of how good the underlying model is.

## Worked example: sampling with temperature
{: #worked-example-sampling-with-temperature }

Let's make this concrete with a toy "trained" model — a hand-written transition table over a handful of words — and implement temperature-controlled sampling on top of it.

```python
import random

# A toy "trained" bigram model: P(next word | current word)
transitions = {
    "the": {"cat": 0.4, "dog": 0.3, "sun": 0.3},
    "cat": {"sat": 0.7, "ran": 0.3},
    "dog": {"ran": 0.6, "sat": 0.4},
    "sun": {"rose": 1.0},
    "sat": {"the": 0.5, ".": 0.5},
    "ran": {"the": 0.5, ".": 0.5},
    "rose": {".": 1.0},
}

def sample_next(dist: dict, temperature: float, rng: random.Random):
    words = list(dist.keys())
    probs = [dist[w] for w in words]
    # Temperature reshapes the distribution BEFORE we draw from it.
    # temperature -> 0   : sharpens toward the max (greedy-like)
    # temperature == 1   : unchanged
    # temperature -> inf : flattens toward uniform (more random)
    scaled = [p ** (1.0 / temperature) for p in probs]
    z = sum(scaled)
    scaled = [s / z for s in scaled]
    return rng.choices(words, weights=scaled, k=1)[0]

def generate(start="the", steps=8, temperature=1.0, seed=0):
    rng = random.Random(seed)
    context = start
    out = [context]
    for _ in range(steps):
        if context not in transitions or context == ".":
            break
        context = sample_next(transitions[context], temperature, rng)
        out.append(context)
    return " ".join(out)

for t in [0.2, 1.0, 3.0]:
    print(f"T={t}: {generate(temperature=t, seed=18)}")
```

Running this shows the effect directly:

```
T=0.2: the cat sat the cat sat the cat sat
T=1.0: the cat sat the cat sat the dog ran
T=3.0: the cat ran the cat sat the dog ran
```

At `T=0.2` the walk almost always takes the highest-probability branch at each step — `cat` (0.4) over `dog`/`sun` (0.3 each), `sat` (0.7) over `ran` (0.3) — so it gets stuck orbiting `the -> cat -> sat -> the -> ...` for the entire run. At `T=1.0` the unmodified probabilities occasionally let a less-likely branch (`dog`) through. At `T=3.0` even the *first* step deviates from the highest-probability choice (`ran` instead of `sat`), and low-probability branches (`dog`) show up more readily. There's nothing mystical about the "temperature" the API of your favorite LLM exposes — it's exactly this exponent, applied to logits before softmax, every time.

**Greedy decoding** is the `T -> 0` limit: always take `max(probs)`, no randomness. It looks "safer" because it's deterministic and always picks the model's single most confident guess, but it's also the mode most prone to repetition loops — if the model's most-confident continuation after "the the the" is another "the," greedy decoding will produce it forever, whereas even a little temperature lets the walk escape.

**Top-p (nucleus) sampling** is a smarter compromise: instead of scaling every probability, sort tokens by probability, keep only the smallest prefix set whose cumulative probability exceeds `p`, zero out everything else, renormalize, and sample from what's left. This throws away the long, unreliable tail of low-probability tokens without collapsing all the way to greedy.

## The training/inference mismatch
{: #the-training-inference-mismatch }

Here's the failure mode that surprises almost everyone the first time they hit it: **training does not use this loop.**

During training, we use **teacher forcing** — at every position in a real training sequence, we feed the model the true previous tokens (not tokens it generated itself) and ask it to predict the true next token. The model never has to condition on its own mistakes during training, because it's never fed its own output; it's always fed ground truth, regardless of how well it's currently predicting.

At inference time, this guarantee disappears. The model conditions on tokens *it itself generated*, which may already be slightly wrong or off-distribution — a phrasing it wouldn't have produced from real training data. This train/inference mismatch is called **exposure bias**, and it's the mechanistic reason errors compound during long generations: a small mistake early on shifts the context away from what the model saw during training, making the *next* mistake more likely, which shifts the context further, and so on. It's also why techniques like beam search, repetition penalties, and (much later in this course) reinforcement learning from human feedback (article 38) exist — they're all ways of fighting the fact that the loop you sample from at inference time is not the loop the model was trained under.

A common related mistake: assuming that because a model was trained with cross-entropy loss on *individual* next-token predictions, it's somehow evaluating whole-sequence quality as it generates. It isn't. Nothing in the vanilla loop above ever looks ahead or scores the sentence as a whole — every decision is a greedy-or-sampled draw from a single-step distribution, with no lookahead. Any global coherence you see is an emergent property of a good per-step distribution, not a separate mechanism checking the whole output.

## Exercise
{: #exercise }

Implement top-p sampling as a standalone function and verify it against a distribution you can check by hand:

```python
def top_p_filter(dist: dict, p: float) -> dict:
    """Keep the smallest set of tokens whose cumulative probability >= p."""
    items = sorted(dist.items(), key=lambda kv: kv[1], reverse=True)
    kept = {}
    cumulative = 0.0
    for word, prob in items:
        kept[word] = prob
        cumulative += prob
        if cumulative >= p:
            break
    # renormalize so the kept probabilities sum to 1.0
    z = sum(kept.values())
    return {w: v / z for w, v in kept.items()}

dist = {"a": 0.5, "b": 0.3, "c": 0.15, "d": 0.05}
filtered = top_p_filter(dist, p=0.8)

assert set(filtered.keys()) == {"a", "b"}, filtered   # 0.5 + 0.3 = 0.8, exactly meets p
assert abs(sum(filtered.values()) - 1.0) < 1e-9
print(filtered)  # {'a': 0.625, 'b': 0.375}
```

Then change `p` to `0.95` and predict, before running, whether `"c"` will now be included. Run it and check. Finally, set `p = 1.0` and confirm `filtered` equals the original `dist` — top-p with `p=1.0` should always be a no-op, and if your implementation disagrees, that's a bug worth finding now rather than in a real sampler.


---

[← 02. Tokens Are Not Words](/courses/llm-mastery/02-tokens-not-words/)  
[04. Your First LM: Bigrams →](/courses/llm-mastery/04-bigram-language-model/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
