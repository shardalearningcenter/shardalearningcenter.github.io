---
layout: course
title: "27. Implement a Tiny GPT (Conceptual Walkthrough)"
permalink: /courses/llm-mastery/27-implement-tiny-gpt/
course_track: "LLM Mastery"
description: "If you can't write it in under 150 lines, you don't understand it yet. Here's the 150 lines."
level: Advanced
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-shapes-are-the-spec"
    label: "Mental model: shapes are the spec"
  - id: "worked-example-a-real-character-level-gpt"
    label: "Worked example: a real character-level GPT"
  - id: "the-training-loop"
    label: "The training loop"
  - id: "failure-mode-loss-that-plateaus-around-ln-vocab-size"
    label: "Failure mode: loss that plateaus around ln(vocab_size)"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 27/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

Everything in articles 21 through 26 was math and diagrams. This one is code that actually runs, trains, and produces text — because reading about attention and *having implemented* attention are different levels of understanding, and only one of them survives contact with a debugger. The target here is deliberately small: a character-level GPT trained on a small text file, small enough to train on a laptop CPU in a few minutes and small enough to fit in your head all at once.

## Mental model: shapes are the spec
{: #mental-model-shapes-are-the-spec }

The fastest way to write a transformer without bugs is to write the shape of every tensor as a comment on the line that produces it, before you write the line. If you can't state the shape, you don't know what the line is supposed to do yet. This isn't a style preference — it's the debugging method, because the overwhelming majority of transformer implementation bugs (as seen in articles 21 and 22) are shape bugs that don't crash: a silent transpose, a reshape that mixes the wrong axes, a broadcast that quietly does something other than what you intended. Shape discipline is the whole defense.

## Worked example: a real character-level GPT
{: #worked-example-a-real-character-level-gpt }

This is the complete model — not a skeleton with `...` placeholders, an actual implementation you can paste and run:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class Head(nn.Module):
    def __init__(self, d_model, head_size, block_size):
        super().__init__()
        self.key = nn.Linear(d_model, head_size, bias=False)
        self.query = nn.Linear(d_model, head_size, bias=False)
        self.value = nn.Linear(d_model, head_size, bias=False)
        self.register_buffer('mask', torch.tril(torch.ones(block_size, block_size)))

    def forward(self, x):
        B, T, C = x.shape
        k, q, v = self.key(x), self.query(x), self.value(x)       # (B, T, head_size)
        scores = q @ k.transpose(-2, -1) / k.shape[-1]**0.5       # (B, T, T)
        scores = scores.masked_fill(self.mask[:T, :T] == 0, float('-inf'))
        weights = F.softmax(scores, dim=-1)
        return weights @ v                                        # (B, T, head_size)

class MultiHead(nn.Module):
    def __init__(self, d_model, n_head, block_size):
        super().__init__()
        head_size = d_model // n_head
        self.heads = nn.ModuleList([Head(d_model, head_size, block_size) for _ in range(n_head)])
        self.proj = nn.Linear(d_model, d_model)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)        # (B, T, C)
        return self.proj(out)

class Block(nn.Module):
    def __init__(self, d_model, n_head, block_size):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = MultiHead(d_model, n_head, block_size)
        self.ln2 = nn.LayerNorm(d_model)
        self.mlp = nn.Sequential(
            nn.Linear(d_model, 4 * d_model), nn.GELU(), nn.Linear(4 * d_model, d_model)
        )

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.mlp(self.ln2(x))
        return x

class TinyGPT(nn.Module):
    def __init__(self, vocab_size, block_size, d_model=128, n_head=4, n_layer=4):
        super().__init__()
        self.block_size = block_size
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(block_size, d_model)
        self.blocks = nn.Sequential(*[Block(d_model, n_head, block_size) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = self.tok_emb(idx) + self.pos_emb(pos)
        x = self.blocks(x)
        x = self.ln_f(x)
        logits = self.head(x)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            logits, _ = self(idx[:, -self.block_size:])
            probs = F.softmax(logits[:, -1, :], dim=-1)
            next_id = torch.multinomial(probs, num_samples=1)
            idx = torch.cat([idx, next_id], dim=1)
        return idx
```

This is the full model, no ellipses. `Head` is exactly the causal single-head attention from article 21. `MultiHead` is exactly the concat-and-project from article 22. `Block` is exactly the pre-norm residual pattern from article 24 plus the MLP from article 25. `TinyGPT` is exactly the stacking from article 26. There is genuinely nothing new here — this article's only job is proving that the previous five, taken together, are a complete, runnable spec.

## The training loop
{: #the-training-loop }

```python
text = open('input.txt').read()          # e.g. tinyshakespeare.txt
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in text], dtype=torch.long)

block_size, batch_size = 128, 64

def get_batch():
    ix = torch.randint(len(data) - block_size - 1, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    return x, y

model = TinyGPT(vocab_size=len(chars), block_size=block_size)
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)

for step in range(3000):
    xb, yb = get_batch()
    logits, loss = model(xb, yb)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if step % 500 == 0:
        print(step, loss.item())
```

Note `y = data[i+1 : i+block_size+1]` — the shift-by-one target from article 26's failure mode, applied for real this time. Get this line wrong and everything above still "works" in the sense of running without error.

## Failure mode: loss that plateaus around ln(vocab_size)
{: #failure-mode-loss-that-plateaus-around-ln-vocab-size }

If your loss starts near `ln(vocab_size)` (for a ~65-character vocab, that's `ln(65) ≈ 4.17`, the cross-entropy of a uniform random guesser) and *stays there* instead of dropping, the model isn't learning at all, even though nothing crashed. The usual causes, in order of how often they actually happen: the target shift is missing or wrong (article 26's bug, still the most common one); the learning rate is too low for the optimizer and model size to move in 3000 steps; or the causal mask is inverted (masking the *past* instead of the *future*), which cripples the model's ability to use any real context. A loss curve that's flat from step 1 is not a "let it train longer" problem — it's a bug, and the fix is almost always in the three lines around the target shift or the mask, not in the architecture.

## Exercise
{: #exercise }

Run the training loop on a plain-text file (Tiny Shakespeare is the standard choice — a few hundred KB works fine). Confirm the loss drops from roughly `ln(vocab_size)` to somewhere under `1.5` within 3000 steps. Then call `model.generate` starting from a single newline character and print the decoded output. It won't be coherent, but it should look *like English orthography* — real words some of the time, plausible letter sequences even when the words are made up. If it's still producing uniform noise after 3000 steps, that's your signal to go find the bug rather than train longer.

---

[← 26. GPT Architecture: Decoder-Only Transformers](/courses/llm-mastery/26-gpt-architecture/)  
[28. KV Cache: Why Chat Is Fast After the First Token →](/courses/llm-mastery/28-kv-cache/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
