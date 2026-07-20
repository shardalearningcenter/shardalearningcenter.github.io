---
layout: course
title: "32. Pretraining Data: The Real Model"
permalink: /courses/llm-mastery/32-pretraining-data/
course_track: "LLM Mastery"
description: "The weights are a lossy compression of the training set. Whatever's wrong with the data is now architecturally baked into the model."
level: Advanced
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-compression-not-comprehension"
    label: "Mental model: compression, not comprehension"
  - id: "worked-example-a-minimal-filtering-pipeline"
    label: "Worked example: a minimal filtering pipeline"
  - id: "why-deduplication-matters-more-than-people-expect"
    label: "Why deduplication matters more than people expect"
  - id: "failure-mode-test-set-contamination"
    label: "Failure mode: test-set contamination"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 32/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

A pretrained LLM's weights are, in a real information-theoretic sense, a lossy compression of its training corpus — the next-token objective directly rewards the model for internalizing the statistical structure of that exact dataset, no more and no less. No architecture choice, no amount of compute, no clever training trick changes what data actually went in. If the corpus is full of duplicated boilerplate, the model wastes capacity memorizing that boilerplate instead of learning generalizable patterns. If the corpus contains the test set you plan to evaluate on, your benchmark score measures memorization, not capability. Architecture and training dynamics get almost all the attention in casual conversation about LLMs; the data pipeline is where a huge fraction of the real, measurable quality difference between models actually comes from.

## Mental model: compression, not comprehension
{: #mental-model-compression-not-comprehension }

Don't think of pretraining as "teaching the model facts about the world." Think of it as running an enormous, extremely lossy compression algorithm over a text corpus, where the compressed representation (the weights) is optimized specifically to make good next-token predictions when "decompressed" via a forward pass. Compression only works well on data that has structure to exploit. A corpus that's 40% near-duplicate template pages gives the compressor an easy, low-value pattern to exploit (predict the boilerplate) at the expense of budget that could have gone toward harder, more generalizable patterns. This framing is why "just scrape more web pages" stopped being a winning strategy on its own — a bigger low-quality corpus doesn't compress into a better model, it just gives the compressor more low-value structure to latently memorize.

## Worked example: a minimal filtering pipeline
{: #worked-example-a-minimal-filtering-pipeline }

Real pretraining pipelines (CCNet, RefinedWeb, FineWeb, Dolma) share the same broad stages. Here's a minimal, runnable sketch of the core idea — a perplexity-based quality filter, using a small pretrained model to score how "surprising" a document looks:

```python
import re

def basic_quality_filters(text):
    if len(text) < 200:
        return False                          # too short to be useful
    words = text.split()
    if len(words) == 0:
        return False
    avg_word_len = sum(len(w) for w in words) / len(words)
    if avg_word_len > 12 or avg_word_len < 2:
        return False                          # likely garbled/boilerplate
    alpha_ratio = sum(c.isalpha() for c in text) / max(len(text), 1)
    if alpha_ratio < 0.6:
        return False                          # too much non-prose (markup, ids)
    if len(re.findall(r"http\S+", text)) / max(len(words), 1) > 0.1:
        return False                          # link-farm-like
    return True

def dedup_key(text, n=8):
    words = text.split()
    shingles = {" ".join(words[i:i+n]) for i in range(len(words) - n + 1)}
    return frozenset(shingles)  # compare via Jaccard similarity across documents

docs = ["short", "A reasonably long paragraph of real prose that reads like an article " * 10]
kept = [d for d in docs if basic_quality_filters(d)]
print(len(kept))
```

This is a deliberately simplified stand-in for the real thing — production pipelines use trained classifiers (often a small model trained to distinguish "text that resembles a curated reference corpus" from "random web text"), not hand-written heuristics — but the *shape* of the pipeline is identical: crawl, extract text from HTML, run cheap heuristic filters first (fast, catches obvious junk), run a quality classifier second (slower, catches subtler junk), deduplicate, then mix domains (web text, code, books, academic papers) at deliberately chosen ratios before packing into fixed-length training sequences.

## Why deduplication matters more than people expect
{: #why-deduplication-matters-more-than-people-expect }

Large web crawls contain enormous amounts of near-duplicate content — syndicated news articles, boilerplate legal text, template-generated pages, quoted forum replies. The `dedup_key` function above sketches the standard approach: represent each document as a set of overlapping n-grams ("shingles") and compare documents via set similarity (Jaccard index) or a hashing scheme like MinHash that approximates it cheaply at scale. Papers studying this directly (e.g. the CCNet and Lee et al. "deduplicating training data" work) found measurable effects from deduplication beyond just "saving compute": models trained on deduplicated data show reduced verbatim memorization of training examples, and training loss curves suggest the model spends less capacity re-encoding redundant patterns, freeing it up for content that only appears once or a few times but is genuinely informative.

## Failure mode: test-set contamination
{: #failure-mode-test-set-contamination }

If any portion of a standard benchmark's actual test questions leaked into the pretraining corpus — a startlingly common occurrence, since benchmark questions and answers frequently get posted, quoted, and re-quoted across the web the corpus was scraped from — a model's benchmark score on that test partially reflects memorization of the specific answer, not the capability the benchmark claims to measure. This is not a hypothetical: multiple papers (including analyses of GSM8K and MMLU contamination) have found measurable overlap between popular benchmark test sets and common web-scrape training corpora, and reported score changes when contaminated examples are removed and models are re-evaluated. The fix requires active work — n-gram overlap checks between your training corpus and every benchmark you intend to report scores on, run *before* training, not treated as a courtesy check afterward. A benchmark score with an unexamined contamination risk is not evidence of anything you can trust.

## Exercise
{: #exercise }

Using the `dedup_key` function above, generate three short documents: two that share a long common sentence with only minor edits, and one that's genuinely unrelated. Compute pairwise Jaccard similarity (`len(intersection) / len(union)` of the shingle sets) between all three pairs. Pick a similarity threshold that correctly flags the near-duplicate pair while leaving the unrelated pair unflagged, and justify your threshold choice using the actual numbers you computed.

---

[← 31. Tokenization Deep Dive: BPE Under the Hood](/courses/llm-mastery/31-tokenization-deep-dive/)  
[33. Training Parallelism: DDP, FSDP, Pipeline →](/courses/llm-mastery/33-parallelism-ddp-fsdp/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
