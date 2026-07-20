---
layout: course
title: "01. What is a Language Model, Really?"
permalink: /courses/llm-mastery/01-what-is-a-language-model/
course_track: "LLM Mastery"
description: "An LM is one function: given the tokens so far, output a probability distribution over the next one. Everything else is engineering on top of that fact."
level: Beginner
toc:
  - id: "the-one-function-that-is-the-whole-model"
    label: "The one function that is the whole model"
  - id: "worked-example-a-probability-table-you-can-run"
    label: "Worked example: a probability table you can run"
  - id: "the-anthropomorphism-trap"
    label: "The anthropomorphism trap"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 1/50** · Karpathy-style LLM course

By the end of this article you should be able to write, from scratch, the exact function a language model computes — no hand-waving about "understanding" — and compute the probability of a toy sequence by hand and check it in code.

A language model is not a mind. It is a function: `f(tokens_so_far) -> distribution over the next token`. That is the entire object of study in this course. If you catch yourself reaching for words like "understands" or "knows," stop — you don't need them, and later they will actively mislead your debugging.

## The one function that is the whole model
{: #the-one-function-that-is-the-whole-model }

Text is a sequence of tokens `t1, t2, ..., tn` (we'll define "token" precisely in the next article — for now, think character or word). The chain rule of probability lets us factor the joint probability of the whole sequence into a product of conditionals:

```
P(t1, t2, ..., tn) = P(t1) · P(t2 | t1) · P(t3 | t1, t2) · ... · P(tn | t1, ..., t_{n-1})
```

This factorization isn't a modeling choice we invented — it's a mathematical identity, true for any joint distribution. What *is* a choice is decoding the sequence left-to-right, one conditional at a time. We make that choice because it gives us something enormously convenient: a single, reusable sub-problem. Instead of modeling "all possible sentences" directly (impossible — the space is infinite), we only ever need to solve "given this prefix, what's the distribution over the next token?" Solve that once, well, and you can generate sequences of any length by calling it repeatedly.

That reusable sub-problem is the language model. Concretely:

- **The model** is a parameterized function `f_theta` that maps a prefix to a distribution over the vocabulary.
- **Training** means adjusting `theta` so that `f_theta` assigns high probability to the prefixes-and-next-tokens that actually occur in real text.
- **Sampling** (a.k.a. generation, inference) means calling `f_theta` repeatedly, each time drawing a token from its output distribution and appending it to the prefix.

Everything from bigram counting tables (article 4) to 70-billion-parameter transformers (article 26) is the same three bullets. Only the shape of `f_theta` and the size of `theta` change. A chatbot is not a fundamentally different kind of object — it's this same function, wrapped in a specific way of formatting the prefix (a "chat template") and possibly nudged by fine-tuning (articles 36–38) so its outputs *look like* helpful replies. Strip the product away and the loss function underneath is still boring: maximize the probability of the next real token.

## Worked example: a probability table you can run
{: #worked-example-a-probability-table-you-can-run }

Let's build the tiniest possible language model — one you can hold in your head — and use it to compute a real joint probability with the chain rule above. It has a vocabulary of exactly three tokens: `a`, `b`, `c`, plus a special start marker `^`.

```python
# A toy, hand-specified "trained" model over 3 tokens.
# cond[prev][next] = P(next | prev). "^" marks start-of-sequence.
cond = {
    "^": {"a": 0.5, "b": 0.3, "c": 0.2},
    "a": {"a": 0.1, "b": 0.6, "c": 0.3},
    "b": {"a": 0.2, "b": 0.2, "c": 0.6},
    "c": {"a": 0.7, "b": 0.2, "c": 0.1},
}

def joint_probability(seq, cond):
    """P(seq[0], seq[1], ..., seq[-1]) via the chain rule."""
    p = 1.0
    prev = "^"
    for tok in seq:
        p *= cond[prev][tok]
        prev = tok
    return p

seq = ["a", "b", "c"]
p = joint_probability(seq, cond)
print(f"P({seq}) = {p:.5f}")
assert abs(p - (0.5 * 0.6 * 0.6)) < 1e-9
```

Run it: `P(['a', 'b', 'c']) = 0.18000`. That number is exactly `P(a|^) · P(b|a) · P(c|b) = 0.5 · 0.6 · 0.6`, the chain rule made concrete. `cond` is nothing but a lookup table, but it satisfies our definition of a language model exactly: give it a prefix, it gives you a distribution over what's next. GPT-4's language model is the same *shape* of object — a function from prefix to next-token distribution — just with ~100,000 tokens instead of 3, and the numbers computed by a transformer's forward pass instead of typed in by hand.

Now let's use the same table to generate, i.e. sample:

```python
import random

def sample_sequence(cond, length=5, seed=0):
    rng = random.Random(seed)
    prev = "^"
    out = []
    for _ in range(length):
        options, weights = zip(*cond[prev].items())
        prev = rng.choices(options, weights=weights, k=1)[0]
        out.append(prev)
    return out

for seed in range(3):
    print(sample_sequence(cond, length=6, seed=seed))
```

This is the *entire* algorithm behind every LLM's "generate" button: look up (or compute) a distribution, draw a token, append it, repeat. The only thing that changes across 50 articles is how `cond[prev]` gets computed.

## The anthropomorphism trap
{: #the-anthropomorphism-trap }

The most common mistake beginners make isn't mathematical — it's linguistic. Once you say a model "wants" an answer, "believes" a fact, or "decided" to refuse a request, you've smuggled in a theory of mind that the math doesn't support, and that theory will actively steer you toward the wrong fix when something breaks.

Take hallucination. From the anthropomorphized view, a model that confidently states a wrong fact is "lying" or "confused," and the instinct is to argue with it, rephrase your question more sternly, or assume it needs "more reasoning." From the `f(prefix) -> distribution` view, the behavior is completely unsurprising: nothing in the training objective (maximize probability of the *next real token*) rewards saying "I don't know" over a fluent, confident-sounding, wrong continuation — unless the training data or fine-tuning specifically shaped that behavior in. The fix isn't a sterner prompt; it's better training data, retrieval grounding (article 40), or calibration techniques, because the objective function is the thing actually in control.

Same trap, different flavor: assuming fluent output implies a rich internal "understanding." Fluency is a *side effect* of minimizing next-token loss on huge amounts of text — it doesn't by itself prove there's a coherent world model inside. (There's real evidence that big enough models *do* build useful internal structure — we'll look at this in article 43 on interpretability — but that's an empirical finding you earn from probing the weights, not something you get to assume from good vibes about the outputs.)

The practical habit to build starting now: whenever you're tempted to explain a model's behavior with a mental-state word, replace it with "the training objective made this the highest-probability continuation" and see if the sentence still makes sense. It almost always does, and it points you at the actual lever you can pull.

## Exercise
{: #exercise }

Extend the toy model with a fourth token, `d`, keeping every row a valid probability distribution (each row's values sum to 1.0). Then compute `P(["a", "c", "d"])` and verify it by hand.

```python
cond["d"] = {"a": 0.25, "b": 0.25, "c": 0.25, "d": 0.25}
cond["a"]["d"] = 0.0   # keep "a" a valid distribution over 4 outcomes
cond["b"]["d"] = 0.0
cond["c"]["d"] = 0.0
cond["^"]["d"] = 0.0

for name, row in cond.items():
    total = sum(row.values())
    assert abs(total - 1.0) < 1e-9, f"row {name} sums to {total}, not 1.0"

p = joint_probability(["a", "c", "d"], cond)
print(f"P(['a','c','d']) = {p:.5f}")
assert abs(p - (0.5 * 0.3 * 0.0)) < 1e-9  # this exact path is impossible here — why?
```

Before running it, predict: is `P(["a", "c", "d"])` going to be zero, and if so, which single number in the table forces that? Then run the code and confirm your prediction matches. That habit — predict the number before you run the cell — is the single most valuable skill you will build in this entire course.


---

  
[02. Tokens Are Not Words →](/courses/llm-mastery/02-tokens-not-words/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
