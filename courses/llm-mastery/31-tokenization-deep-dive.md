---
layout: course
title: "31. Tokenization Deep Dive: BPE Under the Hood"
permalink: /courses/llm-mastery/31-tokenization-deep-dive/
course_track: "LLM Mastery"
description: "BPE has no idea what a word is. It's a greedy compression algorithm that happens to produce something usable as a vocabulary."
level: Advanced
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-greedy-compression-not-linguistics"
    label: "Mental model: greedy compression, not linguistics"
  - id: "worked-example-running-bpe-by-hand"
    label: "Worked example: running BPE by hand"
  - id: "why-leading-spaces-matter"
    label: "Why leading spaces matter"
  - id: "failure-mode-glitch-tokens"
    label: "Failure mode: glitch tokens"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 31/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

Byte-Pair Encoding has zero concept of morphemes, syllables, or words. It's a greedy, purely statistical compression algorithm: start from individual bytes or characters, repeatedly find the single most frequent adjacent pair in your training corpus, merge it into one new token, and repeat until you hit your target vocabulary size. Nothing in that loop knows or cares about linguistics — the fact that the resulting tokens often *look* like meaningful word pieces is an emergent side effect of frequency statistics in real text, not a design goal. This matters practically: it explains why tokenization does bizarre, seemingly arbitrary things to numbers, code, and rare words, and why those quirks are entirely predictable once you think in terms of "what pairs were frequent in the training corpus" rather than "what would a linguist consider a sensible split."

## Mental model: greedy compression, not linguistics
{: #mental-model-greedy-compression-not-linguistics }

Think of BPE as the same family of idea as gzip, not the same family of idea as a dictionary. Gzip doesn't know what a "word" is either — it just finds byte sequences that recur often enough to be worth replacing with a shorter code. BPE does the same thing, except the "shorter code" is a new vocabulary entry instead of a compression symbol, and it's frozen once training finishes (a real LLM tokenizer's merge list is fixed at training time, not adaptive per-document like gzip). "ing" ends up as a token not because anyone told the algorithm it's a suffix, but because the character pair `i, n` and then `in, g` were extremely frequent in English training text. Feed BPE a corpus of a different language or of raw protein sequences and it produces an equally "sensible-looking" vocabulary for *that* distribution — with zero code changes, because the algorithm never encoded any assumption about English in the first place.

## Worked example: running BPE by hand
{: #worked-example-running-bpe-by-hand }

Here's the actual merge loop, small enough to trace by hand on a toy corpus:

```python
from collections import Counter

corpus = ["low", "lower", "lowest", "newest", "widest"]
# start as tuples of characters, with an end-of-word marker
words = [tuple(w) + ("_",) for w in corpus]

def get_pair_counts(words):
    counts = Counter()
    for w in words:
        for pair in zip(w, w[1:]):
            counts[pair] += 1
    return counts

def merge_pair(words, pair):
    merged = "".join(pair)
    new_words = []
    for w in words:
        new_w, i = [], 0
        while i < len(w):
            if i < len(w) - 1 and (w[i], w[i+1]) == pair:
                new_w.append(merged)
                i += 2
            else:
                new_w.append(w[i])
                i += 1
        new_words.append(tuple(new_w))
    return new_words

for step in range(5):
    counts = get_pair_counts(words)
    best_pair = counts.most_common(1)[0][0]
    words = merge_pair(words, best_pair)
    print(step, best_pair, words)
```

Trace it: step 0 will merge `('e', 's')` — it's the most frequent adjacent pair across "lower", "lowest", "newest", "widest" (four occurrences of "es"). Step 1 merges `('es', 't')` into "est", since every word containing "es" is also followed by "t". Notice this is exactly BPE's core property: merges compound — "est" only becomes mergeable *after* "es" already exists as a unit, so the algorithm builds up longer subword units incrementally, always greedily choosing whatever pair is currently most frequent, never revisiting an earlier choice.

## Why leading spaces matter
{: #why-leading-spaces-matter }

Production BPE tokenizers (GPT-2's included) treat a leading space as part of the token, not a separate character to strip — `" dog"` and `"dog"` are different byte sequences fed into the same merge algorithm, and typically end up as genuinely different tokens in the final vocabulary. This is a direct, mechanical consequence of training on running text where words are usually preceded by spaces: the pair `(space, d)` is common enough to merge, giving you a `" d"`-prefixed token family distinct from word-start-of-sequence `"d"` occurrences. The practical upshot: the same word can tokenize completely differently depending on whether it's preceded by a space, at the start of a string, or preceded by punctuation — `"Hello"`, `" Hello"`, and `"(Hello"` are not guaranteed to share a single token, and this is a frequent source of confusion when comparing model behavior on superficially "the same" input string with different surrounding context.

## Failure mode: glitch tokens
{: #failure-mode-glitch-tokens }

If a specific byte sequence appears in the tokenizer's training corpus often enough to earn its own dedicated token, but then appears *rarely or never* in the model's actual pretraining corpus (a mismatch between the tokenizer's training data and the model's), that token's embedding row gets almost no gradient signal during pretraining — it stays close to its random initialization forever. The infamous "SolidGoldMagikarp" incident (a Reddit username that earned a GPT token from web-scrape tokenizer training data, but essentially never appeared in OpenAI's actual model training corpus) produced wildly unpredictable, sometimes disturbing completions whenever that specific token showed up, precisely because the model had a real vocabulary slot for it but had never learned anything meaningful to put there. The general failure mode — "glitch tokens" — is a direct, mechanical consequence of a mismatch between tokenizer training data and model training data, not a mysterious model malfunction, and it's a genuine risk any time those two datasets diverge.

## Exercise
{: #exercise }

Using the merge loop above, run it for the full 8 possible merge steps (until every character in the corpus has been absorbed into larger units) and write out the final tokenization of the word "lowest" as a sequence of tokens. Then add the word "loudest" to the corpus and rerun from scratch. Explain, citing the specific pair-frequency counts at each step, why adding one new word can change the merge order and therefore change how *other*, unrelated words in the corpus end up tokenized.

---

[← 30. Scaling Laws: The Bitter Lesson, Quantified](/courses/llm-mastery/30-scaling-laws-intuition/)  
[32. Pretraining Data: The Real Model →](/courses/llm-mastery/32-pretraining-data/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
