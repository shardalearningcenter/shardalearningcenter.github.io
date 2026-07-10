---
layout: course
title: "03. Next-Token Prediction Is the Game"
permalink: /courses/llm-mastery/03-next-token-prediction/
course_track: "LLM Mastery"
description: "Everything — chat, code, agents — is still next-token prediction underneath."
level: Beginner
toc:
  - id: "autoregressive-generation"
    label: "Autoregressive generation"
  - id: "teacher-forcing-training"
    label: "Teacher forcing (training)"
  - id: "temperature-top-k-top-p"
    label: "Temperature, top-k, top-p"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Beginner · **Article 3/50** · Karpathy-style LLM course

Everything — chat, code, agents — is still next-token prediction underneath.

## Autoregressive generation
{: #autoregressive-generation }

```
context = [BOS]
while not done:
    logits = model(context)          # scores for every vocab token
    probs  = softmax(logits[-1])     # distribution over next token
    next_t = sample(probs)           # or argmax / top-p
    context.append(next_t)
```

That’s the whole loop. Chat templates, tools, RAG — they only change what sits in `context`.

## Teacher forcing (training)
{: #teacher-forcing-training }

During training we don’t sample. We feed the true previous tokens and ask the model to predict the true next one at every position. Loss = average cross-entropy.

## Temperature, top-k, top-p
{: #temperature-top-k-top-p }

Sampling knobs reshape `probs` before you draw. Temperature → 0 is greedy. High temperature is chaotic. Top-p keeps the smallest set of tokens whose cumulative probability ≥ p.

## Exercise
{: #exercise }

Explain why greedy decoding often looks “safer” but more repetitive than sampling.


---

[← 02. Tokens Are Not Words](/courses/llm-mastery/02-tokens-not-words/)  
[04. Your First LM: Bigrams →](/courses/llm-mastery/04-bigram-language-model/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
