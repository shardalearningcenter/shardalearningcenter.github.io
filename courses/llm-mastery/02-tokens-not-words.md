---
layout: course
title: "02. Tokens Are Not Words"
permalink: /courses/llm-mastery/02-tokens-not-words/
course_track: "LLM Mastery"
description: "Build a byte-pair encoder in 20 lines and watch a vocabulary emerge from raw bytes. Tokenization is the unglamorous gatekeeper of every LLM."
level: Beginner
toc:
  - id: "the-model-never-sees-text"
    label: "The model never sees text"
  - id: "worked-example-byte-pair-encoding-from-scratch"
    label: "Worked example: byte-pair encoding from scratch"
  - id: "where-tokenization-bites-you"
    label: "Where tokenization bites you"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 2/50** · Karpathy-style LLM course

After this article you'll be able to implement byte-pair encoding (BPE) from raw bytes, explain why "strawberry has how many r's" trips up LLMs, and predict — before you check — whether a given word will be one token or several.

## The model never sees text
{: #the-model-never-sees-text }

Here's the thing nobody tells you early enough: a language model never touches a string. It touches a sequence of integers. Somewhere before the string ever reaches the neural network, a completely separate program — the **tokenizer** — has already carved it into pieces and mapped each piece to an integer ID from a fixed, finite vocabulary. The network's embedding table (article 6) has exactly that many rows. Add a new piece of text the tokenizer has never seen, and it doesn't get a new row — it gets split into pieces the tokenizer *does* know, however awkward that split looks.

Early tokenizers just split on whitespace and called each resulting chunk a "word." That fails almost immediately: vocabularies explode (every misspelling, every inflection, every compound is a new word), and any word not seen during training becomes an unrepresentable `<UNK>` token, which is a disaster for a model whose entire job is predicting *specific* tokens. The fix used by essentially every modern LLM is **subword tokenization**: build a vocabulary of frequently-occurring byte or character sequences, so that common words are a single token and rare or novel words decompose into a handful of familiar pieces. `"unbelievable"` might become `["un", "believ", "able"]`; a word the tokenizer has genuinely never encountered can still always be spelled out, in the worst case, one byte at a time. No `<UNK>`, no dead ends.

The most widely used algorithm for building this vocabulary is **byte-pair encoding (BPE)**. Its logic is embarrassingly simple, which is exactly why it's worth implementing yourself rather than trusting the description: start with every byte as its own token (256 possible values), then repeatedly find the *most frequent adjacent pair* of tokens in your corpus and merge it into one new token. Do that a few thousand times and you've grown a vocabulary of common substrings — chunks of language chosen entirely by frequency, not by any linguist's notion of "word."

## Worked example: byte-pair encoding from scratch
{: #worked-example-byte-pair-encoding-from-scratch }

Let's build it. We start at the byte level — `text.encode("utf-8")` gives us a list of integers from 0–255 — so this works for *any* language or symbol without special-casing anything.

```python
def get_pair_counts(tokens: list[int]) -> dict[tuple[int, int], int]:
    counts: dict[tuple[int, int], int] = {}
    for pair in zip(tokens, tokens[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    return counts

def merge(tokens: list[int], pair: tuple[int, int], new_id: int) -> list[int]:
    merged = []
    i = 0
    while i < len(tokens):
        if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == pair:
            merged.append(new_id)
            i += 2
        else:
            merged.append(tokens[i])
            i += 1
    return merged

text = "the cat sat on the mat the cat ran the cat sat again"
tokens = list(text.encode("utf-8"))
original_len = len(tokens)

vocab_size = 256   # ids 0-255 are raw bytes
num_merges = 8
merges: dict[tuple[int, int], int] = {}

for _ in range(num_merges):
    counts = get_pair_counts(tokens)
    if not counts:
        break
    top_pair = max(counts, key=counts.get)
    new_id = vocab_size
    merges[top_pair] = new_id
    tokens = merge(tokens, top_pair, new_id)
    vocab_size += 1

print(f"bytes: {original_len} -> tokens: {len(tokens)} after {len(merges)} merges")
print("first few merges learned:", list(merges.items())[:3])
```

Run this and you'll see `bytes: 52 -> tokens: 20 after 8 merges` — more than 2.5x compression from 8 tiny merge steps. Every merge takes the single most frequent adjacent pair and folds it into one new symbol. On this corpus, that's `a` + `t` first (from "cat," "sat," and "mat," which all repeat and all contain that pair), then that new `at` token plus a following space (because "cat " and "sat " each show up multiple times), then `t` + `h` (from "the," which also repeats). Keep going and `" the"` and `" cat"` each end up as effectively a single token, because they were the most repeated substrings, while a word that only appears once stays spelled out in smaller pieces the whole way through. Nobody told the algorithm English has a word "the" — it discovered a frequent byte pattern and rewarded it with its own ID. That's the entire trick. Real tokenizers (GPT's, Llama's) run this same loop tens of thousands of times over trillions of bytes of training text, plus some engineering to handle whitespace and Unicode boundaries cleanly, but the core loop above is not a simplification for teaching purposes — it *is* the algorithm.

## Where tokenization bites you
{: #where-tokenization-bites-you }

Once tokenization clicks, a whole category of "the model is dumb" bugs stops being mysterious.

**"How many r's in strawberry?"** is the famous one. The model isn't counting letters — it can't, because it never sees letters. It sees whatever tokens `strawberry` decomposed into (commonly something like `straw` + `berry`, or split differently depending on the tokenizer), and it has to infer letter counts indirectly from patterns in training text about spelling, which it's never reliably learned to do. A task that's trivial for a for-loop over characters is often genuinely hard for a token-level model. If you need exact character-level operations, don't ask the LLM to do arithmetic on tokens it can't see the letters of — write a for-loop.

**Digit tokenization wrecks arithmetic.** Depending on the tokenizer, `1234` might be one token, or `12` + `34`, or four separate digit tokens — and that grouping can differ between two numbers that "look" similarly structured to you. A model that's never consistently seen numbers chunked the same way struggles to learn place-value arithmetic reliably, which is part of why LLMs are surprisingly bad at multi-digit multiplication compared to how good they are at, say, translation.

**Context windows are token budgets, not word or character budgets.** "This model has a 128k context window" means 128,000 *tokens*, and the same paragraph can cost more tokens in one language than another because the tokenizer's vocabulary was built from a training corpus skewed toward a particular language. This is also directly why API pricing is quoted per token — you're literally being billed by the unit the model actually consumes.

**A leading space is not nothing.** In BPE vocabularies built on real text, `" the"` (with a leading space) and `"the"` (without) are typically two entirely different token IDs. This is a frequent source of "why does the same word behave differently depending on where it appears in my prompt" confusion — it's not a semantic difference to the model, it's a completely different vocabulary entry.

## Exercise
{: #exercise }

Take the BPE code above and run it with `num_merges = 20` on a longer, more repetitive string of your choosing (concatenate a paragraph with itself a few times to guarantee repeated patterns). Confirm two things with asserts:

```python
assert len(tokens) < original_len, "merging should never increase token count"
assert len(merges) <= 20, "we asked for at most 20 merges"
print("compression ratio:", round(original_len / len(tokens), 2))
```

Then, without running anything, write down your guess for which single pair gets merged *first* on a text of your choice, based on which two adjacent bytes you think repeat most. Run the code and check `list(merges.items())[0]` against your guess. If you're wrong, print `get_pair_counts(tokens)` sorted by count and see what you missed — that's the fastest way to build real intuition for how greedy frequency-based merging behaves.


---

[← 01. What is a Language Model, Really?](/courses/llm-mastery/01-what-is-a-language-model/)  
[03. Next-Token Prediction Is the Game →](/courses/llm-mastery/03-next-token-prediction/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
