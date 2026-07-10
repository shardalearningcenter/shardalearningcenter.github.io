---
layout: course
title: "07. Neural Nets for Language: The MLP"
permalink: /courses/llm-mastery/07-mlp-language-model/
course_track: "LLM Mastery"
description: "Bengio's classic recipe, implemented: embed a multi-character context, concatenate, feed an MLP, softmax. This is where the model finally gets a memory longer than one token."
level: Beginner
toc:
  - id: "from-one-token-of-memory-to-several"
    label: "From one token of memory to several"
  - id: "worked-example-a-context-window-mlp"
    label: "Worked example: a context-window MLP"
  - id: "the-shape-mismatch-that-crashes-everything"
    label: "The shape mismatch that crashes everything"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 7/50** · Karpathy-style LLM course

After this article you'll be able to build, by hand, the architecture that ended the era of count tables: a fixed context window of previous tokens, each embedded, concatenated into one vector, and pushed through a small neural network to produce the next-token distribution. This is Bengio et al.'s 2003 neural probabilistic language model, and understanding it cold makes the transformer in article 26 feel like a natural next step rather than a leap.

## From one token of memory to several
{: #from-one-token-of-memory-to-several }

Article 4 established the core problem with counting: extending a bigram table to trigrams, 4-grams, or beyond blows up the table size exponentially (`27^n` cells) while the *data* to fill it grows nowhere near as fast, so almost every long context you'd want a probability for simply never appeared during training. The count table has no way to generalize from "I've seen `the cat sat`" to "I've never seen `the dog sat` but it should behave similarly" — every context is its own isolated row with its own isolated counts.

The MLP language model fixes this by refusing to build one giant table indexed by the *whole* context. Instead:

1. Fix a **context length** `n` (a hyperparameter — how many previous tokens the model is allowed to look at).
2. **Embed** each of the `n` tokens independently, using the same shared embedding table `C` for all positions (article 6's trick, applied `n` times).
3. **Concatenate** the `n` embedding vectors into one long vector.
4. Feed that vector through a small **multilayer perceptron** — a linear layer, a nonlinearity (`tanh`), another linear layer.
5. **Softmax** the final layer's output over the vocabulary, exactly as in article 5.

The generalization comes from step 2 and step 4 sharing parameters *across every context ever seen*. Because the same embedding table is used no matter which position a token occupies, and the same MLP weights process every context, a context the model has literally never seen during training can still produce a sensible prediction, as long as the *individual tokens* in that context resemble tokens the model has seen elsewhere. This is the generalization a lookup table structurally cannot provide, no matter how much smoothing you add to it.

## Worked example: a context-window MLP
{: #worked-example-a-context-window-mlp }

Let's build it concretely on our names dataset, with context length `block_size = 3` — the model conditions on the previous 3 characters to predict the next one.

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

block_size = 3   # how many previous characters we condition on

def build_dataset(words):
    X, Y = [], []
    for w in words:
        context = [0] * block_size          # pad start with '.' tokens
        for ch in w + ".":
            ix = stoi[ch]
            X.append(context)
            Y.append(ix)
            context = context[1:] + [ix]    # slide the window forward
    return torch.tensor(X), torch.tensor(Y)

X, Y = build_dataset(names)
print("X shape:", X.shape, " Y shape:", Y.shape)   # [num_examples, 3]  [num_examples]

vocab_size, dim, hidden = 27, 10, 64
g = torch.Generator().manual_seed(2147483647)
C = torch.randn((vocab_size, dim), generator=g, requires_grad=True)
W1 = torch.randn((block_size * dim, hidden), generator=g, requires_grad=True)
b1 = torch.randn(hidden, generator=g, requires_grad=True)
W2 = torch.randn((hidden, vocab_size), generator=g, requires_grad=True)
b2 = torch.randn(vocab_size, generator=g, requires_grad=True)
params = [C, W1, b1, W2, b2]

def forward(X_batch):
    emb = C[X_batch]                          # [batch, block_size, dim]
    flat = emb.view(emb.shape[0], -1)          # [batch, block_size * dim] -- the concatenation
    h = torch.tanh(flat @ W1 + b1)             # [batch, hidden]
    logits = h @ W2 + b2                       # [batch, vocab_size]
    return logits

logits = forward(X[:32])
loss = F.cross_entropy(logits, Y[:32])
print(f"loss on a random-init batch: {loss.item():.4f}")
```

Trace the shapes once, on paper, before you ever run this: `X_batch` is `[batch, 3]` (three token IDs per example). `C[X_batch]` looks up an embedding for each of those three IDs independently, giving `[batch, 3, 10]`. `.view(emb.shape[0], -1)` is the concatenation step — it doesn't move any data, it just reinterprets that `[3, 10]` block per example as one flat `30`-length vector, which is exactly "take the three embeddings and lay them end to end." From there it's an ordinary two-layer MLP: `[batch, 30] -> [batch, 64] -> [batch, 27]`. If you can narrate that shape chain from memory, you understand the architecture; if any step in it is fuzzy, that's exactly where to slow down (article 13 is entirely dedicated to this shape-tracing discipline, because it's the single most common source of real-world bugs).

Run it and check the printed loss: it comes out around `17`, not the `ln(27) ≈ 3.30` "pure guessing" floor you might expect from articles 4 and 5. That's not a bug — it's `torch.randn` handing every one of `W1`, `W2`, `b1`, `b2` values drawn from a standard normal with no regard for how many numbers get summed together downstream. With `block_size * dim = 30` inputs into `W1` and 64 inputs into `W2`, the pre-activation sums are far larger in magnitude than a well-behaved network wants, `tanh` saturates hard near `+/-1` almost everywhere, and the final logits land far from zero — producing an extremely confident, extremely *wrong* distribution on most examples, which cross-entropy punishes severely (recall from article 5: confident-and-wrong is the worst case). File this away; article 16 ("Initialization Is Not Optional") is entirely about fixing exactly this, by scaling initial weights to the size of the layer they feed into. For now, the training loop in the next article will grind this down regardless — but a healthy initialization gets you there in far fewer steps, which matters enormously once "a few thousand steps" becomes "a few thousand GPU-hours."

## The shape mismatch that crashes everything
{: #the-shape-mismatch-that-crashes-everything }

The overwhelmingly most common way to break this architecture is a **shape mismatch between the flatten step and `W1`'s input dimension** — and it usually happens the moment you change one hyperparameter without updating the other. If you bump `block_size` from 3 to 4 without updating `W1`'s first dimension from `block_size * dim` to the new value, you get a matrix multiply error, but a *worse* version of this bug happens when the shapes accidentally still multiply (e.g. because `dim` also changed in a way that keeps the total the same) — then you get no crash at all, just a model quietly training on scrambled, meaningless input, with a loss curve that looks plausible but never gets genuinely good. A crash is a gift; a silent shape coincidence is the dangerous version of this bug.

The discipline that prevents this: after writing (or changing) any `forward` function, print every intermediate tensor's `.shape` once, with a comment stating what you *expect* it to be, before you trust the loss number. `emb.shape` should be `[batch, block_size, dim]` — not `[batch, dim, block_size]`, not `[block_size, batch, dim]`. It is extremely easy to write code that runs and produces numbers while silently having two dimensions swapped, and cross-entropy loss will still output *some* number either way — it has no way to know your semantics are scrambled, only that some numbers went in and some came out. A model that trains "successfully" to a mediocre-but-plausible loss on scrambled input is a much harder bug to notice than a crash, which is exactly why it's the one worth actively guarding against.

A second, related mistake: forgetting to pad the context at the start of each word with the `.` token. Without padding, the first real character of every name has no valid 3-token context to look back on, and you either crash on an index error or — worse — silently train on whatever garbage happens to sit in an under-sized context array. The `context = [0] * block_size` initialization above exists specifically to give every position, including the very first character of a word, a well-defined, fixed-length context to condition on.

## Exercise
{: #exercise }

Work out the concatenated input size by hand for `vocab_size=10_000`, `block_size=3`, `dim=32`, then verify your arithmetic matches what the code actually produces:

```python
vocab_size, block_size, dim = 10_000, 3, 32
predicted_input_size = block_size * dim
print(f"predicted flattened input size: {predicted_input_size}")

# sanity-check with a fake batch of the given shape
fake_emb = torch.randn(5, block_size, dim)   # [batch=5, block_size, dim]
flat = fake_emb.view(fake_emb.shape[0], -1)
assert flat.shape == (5, predicted_input_size)
print("actual flattened shape:", flat.shape)
```

Then answer without running code: if you doubled `dim` to `64` but kept `block_size=3`, would `W1`'s row count need to change, and to what? Then double it in the actual code above, re-run the loss computation, and confirm it still executes without a shape error.


---

[← 06. Embeddings: Meaning as Geometry](/courses/llm-mastery/06-embeddings-intuition/)  
[08. The Training Loop, End to End →](/courses/llm-mastery/08-training-loop-basics/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
