---
layout: course
title: "02. Tokens Are Not Words"
permalink: /courses/llm-mastery/02-tokens-not-words/
course_track: "LLM Mastery"
description: "Tokenization is the unglamorous gatekeeper of every LLM."
level: Beginner
toc:
  - id: "characters-bytes-tokens"
    label: "Characters → bytes → tokens"
  - id: "why-tokenization-matters-more-than-you-think"
    label: "Why tokenization matters more than you think"
  - id: "a-mental-model"
    label: "A mental model"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 2/50** · Karpathy-style LLM course

Tokenization is the unglamorous gatekeeper of every LLM.

## Characters → bytes → tokens
{: #characters-bytes-tokens }

Models don’t see “words.” They see **token IDs** — integers from a fixed vocabulary.

Modern LLMs use **subword** tokenizers (BPE, SentencePiece). Common words are one token; rare words split into pieces.

```python
# Conceptual — not a real tokenizer
text = "unbelievable"
# might become: ["un", "believ", "able"] → [1045, 8921, 334]
```

## Why tokenization matters more than you think
{: #why-tokenization-matters-more-than-you-think }

- Context length is in **tokens**, not words.
- Cost is per token.
- Weird bugs (“the model can’t spell”) are often tokenizer artifacts.
- Multilingual quality depends heavily on how the vocab was built.

## A mental model
{: #a-mental-model }

Tokenizer = compression codec for text. The neural net only ever sees the compressed stream.

## Exercise
{: #exercise }

Take a sentence and guess which pieces would be single tokens vs split. Then check with any online BPE demo or `tiktoken` if you have it.


---

[← 01. What is a Language Model, Really?](/courses/llm-mastery/01-what-is-a-language-model/)  
[03. Next-Token Prediction Is the Game →](/courses/llm-mastery/03-next-token-prediction/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
