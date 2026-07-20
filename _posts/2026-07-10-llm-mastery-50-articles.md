---
layout: post
title: "LLM Mastery: 50 articles from tokens to your own tiny model"
date: 2026-07-10
description: "A Karpathy-style LLM course is live — 50 articles, each with runnable code, from 'what is a token' through training a tiny GPT you understand end to end."
tags: [llm, course, deep-learning]
---

We published **[LLM Mastery](/courses/llm-mastery/)**: fifty in-depth articles that go from "what is a language model?" to training a tiny GPT you understand end to end, in the spirit of Andrej Karpathy — build tiny things, distrust vibes, love the loss curve.

## What "mastery" actually means here

Every article follows the same shape: one core idea, one piece of runnable code that demonstrates it, and one exercise that breaks if you don't actually understand the idea. There are no slide-deck articles that just describe a concept in prose — if you can't paste in code and watch a number change (a loss, an accuracy, a generated string), the article isn't done. That's a deliberate constraint on us, not just advice to you.

## Who it's for

- Beginners who want first principles, not marketing decks about "AI"
- Engineers who've called ChatGPT-style APIs and want to know what's actually happening underneath
- Anyone willing to type code, watch loss curves, and debug shape mismatches at 11pm

You'll get the most out of it if you're comfortable with the material in our [Getting Started with Python](/2026/07/10/getting-started-with-python/) and [Getting Started with PyTorch](/2026/07/10/getting-started-with-pytorch/) posts — you don't need to be an expert in either, but you should be able to run a script from the terminal and read a `RuntimeError` without panicking.

## Shape of the path

| Phase | Articles | Focus |
|------:|----------|-------|
| Foundations | 01–10 | Tokens, loss, bigrams, the MLP mindset |
| Neural guts | 11–20 | Autograd from scratch, optimization, attention's precursors |
| Transformers | 21–35 | Self-attention, GPT internals, systems concerns, scaling laws |
| Post-training | 36–50 | Fine-tuning (SFT), LoRA, RLHF/DPO, RAG, agents, safety, and a train-your-own capstone |

Start here: [01. What is a Language Model, Really?](/courses/llm-mastery/01-what-is-a-language-model/)

## A concrete sample, so this isn't just a list of links

Article 4, [Bigram Language Model](/courses/llm-mastery/04-bigram-language-model/), has you build the simplest possible language model — a table of "given this character, what's the next one" counts — and generate text from it. It's a handful of lines, it runs in under a second, and the output is obviously bad (mostly gibberish with occasional real words), which is the point: it gives you a concrete, terrible baseline to improve on for the next 46 articles. By article 27, [Implement Tiny GPT](/courses/llm-mastery/27-implement-tiny-gpt/), you're writing the actual self-attention and feed-forward blocks yourself, not importing them from a library.

## How much time it takes

Plan for 30–90 minutes per article if you type the code yourself rather than copy-pasting — and you should type it yourself, since transcription is where you notice what you don't actually understand. Foundations and neural-guts articles (01–20) run comfortably on a CPU. Transformer-scale training (21–35 onward) benefits from a GPU, but every article's *code* is written to run on a small config first so you can verify correctness before scaling up.

## FAQ

**Do I need a GPU?** Not to follow along and understand the code. You'll want one (even a modest one, or a free-tier cloud GPU) once you start training the larger configs in the transformers and post-training phases.

**Do I need to finish all 50 in order?** Foundations (01–10) and Neural guts (11–20) build directly on each other — don't skip those. Once you're through Transformers (21–35), the post-training articles are more modular; RAG (art. 40) and agents (art. 41) don't require you to have done fine-tuning (art. 36) first.

**What's the capstone?** Article 50, [Capstone: Train Your Own](/courses/llm-mastery/50-capstone-train-your-own/), has you train a small GPT on a dataset of your choosing, end to end, using everything from articles 01–49 — your own tokenizer decisions, your own architecture choices, your own eval.

## Warm-up posts, if you need tooling first

These getting-started posts are short, practical, and each ends with something you build and verify yourself:

- [Python](/2026/07/10/getting-started-with-python/)
- [Git](/2026/07/10/getting-started-with-git/)
- [Linux shell](/2026/07/10/getting-started-with-linux-shell/)
- [Docker](/2026/07/10/getting-started-with-docker/)
- [JavaScript](/2026/07/10/getting-started-with-javascript/)
- [SQL](/2026/07/10/getting-started-with-sql/)
- [PyTorch](/2026/07/10/getting-started-with-pytorch/)
- [FastAPI](/2026/07/10/getting-started-with-fastapi/)
