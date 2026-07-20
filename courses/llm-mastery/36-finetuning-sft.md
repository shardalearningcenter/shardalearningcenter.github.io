---
layout: course
title: "36. Supervised Fine-Tuning (SFT)"
permalink: /courses/llm-mastery/36-finetuning-sft/
course_track: "LLM Mastery"
description: "Fine-tuning doesn't add facts. It teaches a base model to become a character: the helpful assistant."
level: Advanced
toc:
  - id: "mental-model"
    label: "Mental model"
  - id: "the-loss-mask"
    label: "The loss mask trick"
  - id: "data-quality"
    label: "Data quality"
  - id: "failure-mode"
    label: "Failure mode"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 36/50** · Karpathy-style LLM course

Pretraining already taught the model to write fluent, mostly-correct text about nearly everything humans have written down. Supervised fine-tuning (SFT) doesn't teach it more facts — it teaches it a *format*: stop completing documents, start playing the role of a helpful assistant answering a question. That's the whole claim of this article. If you remember one sentence from it, remember that one.

## Mental model
{: #mental-model }

SFT changes nothing about the math of training a language model. It's still next-token cross-entropy, still teacher forcing, still Adam nudging weights downhill. What changes is *which documents* you show it. Pretraining data looks like "the internet continuing itself" — blog posts, code, forum threads, novels. SFT data looks like `(instruction, ideal response)` pairs, formatted with a chat template so the model can tell where the human's turn ends and its turn begins.

Because the base model already models "text that looks like a helpful assistant answering a question" reasonably well — that pattern exists all over its pretraining corpus (docs, Stack Overflow answers, tutorials) — SFT is mostly *distribution shifting*: reweighting the model toward an assistant-shaped mode it already partially knows, rather than building brand-new capability. This is why SFT works with astonishingly little data compared to pretraining: you're not growing new circuits, you're turning up the gain on ones that already exist.

## The loss mask trick
{: #the-loss-mask }

Here's the part tutorials gloss over: you don't compute loss on every token in an SFT example. You mask the prompt.

If you trained on the full sequence — system prompt, user question, and answer — the model would spend gradient budget learning to *predict the user's question*, which is useless (you already know the question; you're not sampling it) and actively harmful, since it dilutes the signal that actually matters: predicting good answers.

```python
import torch

def make_labels(input_ids: torch.Tensor, response_start: int) -> torch.Tensor:
    """Mask everything before the assistant's answer.
    -100 is PyTorch's ignore_index for cross_entropy — those
    positions contribute zero gradient."""
    labels = input_ids.clone()
    labels[:response_start] = -100
    return labels

# [BOS] "User: What is the capital of Peru?" [SEP] "Assistant: Lima." [EOS]
input_ids      = torch.tensor([1, 88, 4, 210, 990, 5, 2, 771, 44, 3])
response_start = 7  # index of "Assistant:" — everything before is prompt

labels = make_labels(input_ids, response_start)
print(labels.tolist())
# [-100, -100, -100, -100, -100, -100, -100, 771, 44, 3]
```

Only 3 of 10 tokens generate gradient here. That ratio — response tokens over total tokens — is a real number worth logging per batch. If it's tiny (long system prompts, short answers) your effective learning signal per step is much smaller than your token count suggests, and you'll need more steps than the raw dataset size implies.

## Data quality
{: #data-quality }

The famous result behind SFT (LIMA, and every serious post-training report since) is that a few thousand *meticulously* curated examples — diverse tasks, consistent style, genuinely correct answers — outperform hundreds of thousands of scraped or synthetic ones. This is the opposite lesson from pretraining, where scale is king, and it trips people up constantly.

Why? Pretraining teaches *capability* (compress the world). SFT teaches *calibration of an existing capability toward a format*. Once the model has reliably seen "answer directly, be concise, cite uncertainty" a few thousand times in a row, it generalizes that behavior to unseen questions — because it already knew how to answer questions, it just needed to learn when to stop pretending it's writing a Wikipedia article.

## Failure mode
{: #failure-mode }

Push SFT too hard — too many epochs, too high a learning rate, too narrow a dataset — and two things go wrong, often together:

1. **Catastrophic forgetting.** The model gets so specialized on the SFT distribution that broad pretraining capability degrades. Ask it something slightly outside the fine-tuning domain and quality craters.
2. **Style collapse.** The model memorizes surface patterns instead of the underlying skill: every answer starts with "Certainly! I'd be happy to help," every list has exactly three bullets, every response is exactly as long as the training median regardless of what the question needs.

Both symptoms share a root cause: too many gradient steps relative to how diverse and large the SFT set is. The fix is boring but effective — 1 to 3 epochs, a learning rate an order of magnitude below pretraining's, and, if you can, mixing in a small slice of the original pretraining distribution so the model doesn't forget it ever knew anything else.

## Exercise
{: #exercise }

Take this tokenized example (each number is one token): prompt = 12 tokens, full sequence with answer = 20 tokens. Write the `labels` tensor a correct SFT loss mask would produce, and compute what fraction of the 20 tokens actually contribute to the loss. Then explain, in your own words, why training on the full 20 tokens unmasked would make the model *worse* at being an assistant, not just wasteful.


---

[← 35. Evaluation: Beyond Vibes](/courses/llm-mastery/35-eval-harness-thinking/)  
[37. LoRA and Parameter-Efficient Fine-Tuning →](/courses/llm-mastery/37-lora-peft/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
