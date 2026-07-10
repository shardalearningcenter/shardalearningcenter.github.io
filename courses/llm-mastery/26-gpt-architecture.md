---
layout: course
title: "26. GPT Architecture: Decoder-Only Transformers"
permalink: /courses/llm-mastery/26-gpt-architecture/
course_track: "LLM Mastery"
description: "GPT isn't one clever trick. It's the same boring block, repeated N times, with the discipline to not deviate."
level: Intermediate
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-one-lego-brick-stacked-tall"
    label: "Mental model: one Lego brick, stacked tall"
  - id: "worked-example-the-full-forward-pass-shapes"
    label: "Worked example: the full forward pass, shapes"
  - id: "why-decoder-only-and-not-encoder-decoder"
    label: "Why decoder-only, and not encoder-decoder"
  - id: "failure-mode-the-off-by-one-in-the-target-shift"
    label: "Failure mode: the off-by-one in the target shift"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 26/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

By the time you understand causal self-attention (article 21), multi-head splitting (22), positional embeddings (23), residuals and norm (24), and the MLP (25), you already understand GPT. There is no additional secret. GPT is: embed tokens, add position information, run the input through `N` identical copies of `(causal multi-head attention → residual → norm) → (MLP → residual → norm)`, apply one final norm, and project to vocabulary logits with a linear layer. The entire research contribution of the GPT line of models is *not* a new mechanism — it's the empirical discovery that this exact boring recipe, scaled up honestly with more data and compute and left otherwise untouched, keeps getting better with no ceiling in sight for a long time.

## Mental model: one Lego brick, stacked tall
{: #mental-model-one-lego-brick-stacked-tall }

If you've built the single transformer block from articles 21–25, you have already built 100% of the design surface of GPT — the rest is deciding how many copies to stack (`N`), how wide each one is (`d_model`), and how many attention heads to split into (`n_head`). GPT-2 small is 12 blocks at `d_model=768`, 12 heads. GPT-2 XL is 48 blocks at `d_model=1600`, 25 heads. Same brick, more copies, wider brick. This is precisely why the architecture is so amenable to scaling-law analysis (article 30) — because there are only a handful of knobs, and the same knobs keep producing predictable, smooth improvements as you turn them up, all the way from a million to a trillion parameters.

## Worked example: the full forward pass, shapes
{: #worked-example-the-full-forward-pass-shapes }

Here's a complete forward pass with every shape annotated, so there's nowhere for hand-waving to hide:

```python
import torch
import torch.nn as nn

class Block(nn.Module):
    def __init__(self, d_model, n_head):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = nn.MultiheadAttention(d_model, n_head, batch_first=True)
        self.ln2 = nn.LayerNorm(d_model)
        self.mlp = nn.Sequential(
            nn.Linear(d_model, 4 * d_model), nn.GELU(),
            nn.Linear(4 * d_model, d_model),
        )

    def forward(self, x, causal_mask):
        h = self.ln1(x)
        attn_out, _ = self.attn(h, h, h, attn_mask=causal_mask, need_weights=False)
        x = x + attn_out                    # (B, T, C)
        x = x + self.mlp(self.ln2(x))        # (B, T, C)
        return x

class GPT(nn.Module):
    def __init__(self, vocab_size, max_seq_len, d_model=768, n_head=12, n_layer=12):
        super().__init__()
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(max_seq_len, d_model)
        self.blocks = nn.ModuleList([Block(d_model, n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, idx, targets=None):
        B, T = idx.shape                                          # (B, T)
        pos = torch.arange(T, device=idx.device)
        x = self.tok_emb(idx) + self.pos_emb(pos)                 # (B, T, C)
        mask = torch.triu(torch.full((T, T), float('-inf')), diagonal=1)
        for block in self.blocks:
            x = block(x, mask)                                    # (B, T, C)
        x = self.ln_f(x)                                          # (B, T, C)
        logits = self.head(x)                                     # (B, T, vocab_size)
        loss = None
        if targets is not None:
            loss = nn.functional.cross_entropy(
                logits.view(-1, logits.size(-1)), targets.view(-1)
            )
        return logits, loss

model = GPT(vocab_size=50257, max_seq_len=1024)
idx = torch.randint(0, 50257, (2, 16))
targets = torch.randint(0, 50257, (2, 16))
logits, loss = model(idx, targets)
print(logits.shape, loss.item())  # torch.Size([2, 16, 50257]) <some float>
```

Notice the shape never changes at the block level: `(B, T, C)` goes in, `(B, T, C)` comes out, for all `N` blocks. That invariant — every block is shape-preserving — is *why* you can stack an arbitrary number of them without touching anything else in the architecture. Only at the very end does `head` project `C → vocab_size` to produce logits.

## Why decoder-only, and not encoder-decoder
{: #why-decoder-only-and-not-encoder-decoder }

The original transformer (and T5) uses an encoder-decoder split: a bidirectional encoder reads the full input, and a separate causal decoder generates output while cross-attending to the encoder's representations. GPT throws away the encoder entirely and uses one causal-only stack for everything — the "input" and "output" are just concatenated into one sequence, and the causal mask is the only thing enforcing that generation can't see the future. Three practical consequences follow directly from that choice: (1) no cross-attention module needed, so the block is simpler and the parameter budget goes further; (2) a single unified training objective (next-token prediction over the whole sequence) works for pretraining on raw text with no need for input/output pairs; (3) the same weights handle any task you can phrase as "continue this text," which is the entire basis of few-shot prompting — there's no architectural encoder/decoder split to force a rigid input/output framing onto every task.

## Failure mode: the off-by-one in the target shift
{: #failure-mode-the-off-by-one-in-the-target-shift }

Next-token prediction means `targets` must be `idx` shifted left by one: the model at position `t` should predict the token at position `t+1`, so `targets[t] = idx[t+1]`. Get this wrong — accidentally pass `targets = idx` unshifted, so the model is asked to predict the token it can already see at that exact position — and training doesn't crash. Loss drops fast and looks *great*, misleadingly so, because predicting a token from itself (trivially available via the residual stream and the embedding table) is nearly free. Generation afterward is useless, because you never actually trained the model to predict what comes *next*. This is one of the most common silent bugs in from-scratch GPT implementations, and the tell is a suspiciously low loss within the first few hundred steps — a real next-token loss on natural language rarely craters that fast.

## Exercise
{: #exercise }

Using the shapes from GPT-2 small (`n_layer=12`, `d_model=768`, `n_head=12`, `vocab_size=50257`, `max_seq_len=1024`), estimate total parameter count by hand: token + position embeddings, plus 12 blocks each with attention (`4 × d_model²`) and MLP (`2 × 4 × d_model²`, from article 25), plus the final unembedding layer (note GPT-2 ties the unembedding weight to the token embedding, so don't double-count it). Compare your estimate to the publicly reported 124M parameters for GPT-2 small and account for any gap.

---

[← 25. The Transformer MLP: Where Facts Often Live](/courses/llm-mastery/25-mlp-in-transformer/)  
[27. Implement a Tiny GPT (Conceptual Walkthrough) →](/courses/llm-mastery/27-implement-tiny-gpt/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
