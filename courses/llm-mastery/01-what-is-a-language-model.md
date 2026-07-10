---
layout: course
title: "01. What is a Language Model, Really?"
permalink: /courses/llm-mastery/01-what-is-a-language-model/
course_track: "LLM Mastery"
description: "Strip the hype. An LM is a probability distribution over sequences of tokens."
level: Beginner
toc:
  - id: "the-only-definition-that-matters"
    label: "The only definition that matters"
  - id: "sequences-and-probability"
    label: "Sequences and probability"
  - id: "why-this-is-enough-for-intelligence-looking-behavior"
    label: "Why this is enough for “intelligence-looking” behavior"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 1/50** · Karpathy-style LLM course

Strip the hype. An LM is a probability distribution over sequences of tokens.

## The only definition that matters
{: #the-only-definition-that-matters }

A language model answers one question: **given the text so far, what comes next?**

Not “understanding.” Not “consciousness.” Next token.

If you internalize that, everything else in this course is an engineering detail about *how* we approximate that distribution.

## Sequences and probability
{: #sequences-and-probability }

Text is a sequence: `t1, t2, t3, …`. A model assigns:

```
P(t1, t2, …, tn) = P(t1) · P(t2|t1) · P(t3|t1,t2) · …
```

Training = adjust parameters so this product is high on real text. Sampling = draw from those conditionals one token at a time.

## Why this is enough for “intelligence-looking” behavior
{: #why-this-is-enough-for-intelligence-looking-behavior }

If next-token prediction is good enough, the model must compress a lot of the world into its weights: grammar, facts, style, even shallow reasoning patterns. That compression is the magic. The objective is still boring: maximize likelihood.

## Exercise
{: #exercise }

Write, in one sentence each: (1) what an LM predicts, (2) what “training” means, (3) what “sampling” means. Keep them free of marketing words.


---

  
[02. Tokens Are Not Words →](/courses/llm-mastery/02-tokens-not-words/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
