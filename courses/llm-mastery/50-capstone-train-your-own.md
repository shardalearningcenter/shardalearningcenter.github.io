---
layout: course
title: "50. Capstone: Train Your Own Tiny LLM"
permalink: /courses/llm-mastery/50-capstone-train-your-own/
course_track: "LLM Mastery"
description: "Data, tokenizer, model, training loop, sampling, eval — every primitive from this course, assembled by your own hands."
level: Master
toc:
  - id: "the-project"
    label: "The project"
  - id: "worked-example"
    label: "Worked example"
  - id: "debugging-checklist"
    label: "Debugging checklist"
  - id: "success-criteria"
    label: "Success criteria"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Master · **Article 50/50** · Karpathy-style LLM course

You do not understand a language model until you have watched your own tiny one fail to train, found the bug, and watched it start producing garbage-but-real text instead. Every article before this one gave you the pieces. This one is the assembly instructions, and the only grade that matters is whether you can explain every tensor in your own code.

## The project
{: #the-project }

Scope it small enough to finish in days, not a scale that requires a cluster:

1. Pick 10–100MB of text you're allowed to use — public domain books, your own writing, a permitted dataset. Small enough to iterate on, large enough for real structure to emerge.
2. Train or reuse a tokenizer — character-level is fine for a first pass, BPE (article 31) if you want subword behavior.
3. Implement a small GPT (articles 26–27): 6–12 layers, `d_model` 128–384, a handful of heads. Aim for 10–50M parameters, trainable on a single consumer GPU in hours, not days.
4. Train with the loop from article 8, mixed precision from article 34 if your hardware supports it, until validation loss plateaus meaningfully below your bigram baseline (article 4) — that comparison is your sanity floor.
5. Optionally, run one round of SFT (article 36) on a tiny curated instruction set, so you feel the pretraining-to-post-training transition with your own hands, not just in the abstract.
6. Build a tiny sampler with temperature and top-p controls (articles 3, 14) and a minimal eval set (articles 35, 48) — even five hand-written prompts with a pass/fail check beats "I typed some things and it looked okay."

## Worked example
{: #worked-example }

```python
from dataclasses import dataclass
import torch

@dataclass
class Config:
    vocab_size: int
    d_model: int = 256
    n_layer: int = 8
    n_head: int = 8
    block_size: int = 256
    lr: float = 3e-4

def train(cfg: Config, model, train_data, val_data, steps: int = 5000):
    opt = torch.optim.AdamW(model.parameters(), lr=cfg.lr)
    for step in range(steps):
        x, y = get_batch(train_data, cfg.block_size)
        logits, loss = model(x, targets=y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()

        if step % 500 == 0:
            val_loss = evaluate(model, val_data, cfg.block_size)
            print(f"step {step}: train {loss.item():.3f}  val {val_loss:.3f}")
            sample = generate(model, prompt="The ", max_new_tokens=100, temperature=0.8)
            print("sample:", sample)
```

Notice this is nothing new — it's article 8's training loop, article 3's sampling loop, and article 35's evaluation logged at the same cadence, in one script. That's deliberate. The capstone isn't a new skill; it's proof the old skills compose.

## Debugging checklist
{: #debugging-checklist }

In rough order of how often each one bites first-time builders:

- **Loss doesn't move at all.** Almost always a data pipeline bug — check that `x` and `y` are actually offset by one token, not accidentally identical (which gives the model a free answer and a suspiciously fast-dropping loss that then plateaus at something meaningless), or check that gradients are flowing at all: `loss.backward()` runs before `opt.step()`, and parameters aren't accidentally frozen.
- **Loss looks great, samples are garbage.** Usually a sampling bug, not a training bug — check you're applying the same tokenizer for decoding that you used for encoding, and that temperature or argmax logic isn't accidentally always picking token 0.
- **Loss is suspiciously low, samples are suspiciously good.** Check for a train/val leak — is your validation split actually disjoint text, or an overlapping window of the same document? Cross-entropy on memorized text looks fantastic and means nothing.
- **Comparing loss across two runs that used different tokenizers.** A char-level loss of 1.5 and a BPE loss of 1.5 are not comparable numbers — they measure surprise-per-different-sized-unit. Always compare loss curves within a fixed tokenizer, or convert to bits-per-byte if you need to compare across.

## Success criteria
{: #success-criteria }

Not SOTA. Understanding, checked mechanically: your validation loss beats the bigram baseline from article 4 by a wide margin, your samples are locally fluent even when globally nonsensical, and you can point at any tensor in your training loop and state its exact shape without checking. That's the actual bar, not a leaderboard number.

The field will keep moving past whatever's true the day you read this. The primitives from these fifty articles won't: tokens, loss, attention, data, evaluation, and now the post-training loop of fine-tuning and alignment on top of it. Master those and the next paper is a Tuesday afternoon read, not a mystery. Now go train something.

## Exercise
{: #exercise }

Train your tiny GPT until validation loss plateaus. Report three numbers: your model's final validation loss, the loss of a bigram model (article 4) trained on the exact same data and tokenizer, and the ratio between them. If your ratio isn't at least 1.3–1.5x better than the bigram floor, use the debugging checklist above to find out why before you call the capstone done — a transformer that barely beats bigrams almost always has a bug, not a fundamental limitation.


---

[← 49. Research Taste: How to Read Papers](/courses/llm-mastery/49-research-taste/)  

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
