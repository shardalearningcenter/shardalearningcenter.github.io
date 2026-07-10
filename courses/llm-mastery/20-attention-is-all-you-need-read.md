---
layout: course
title: "20. Reading 'Attention Is All You Need' Like an Engineer"
permalink: /courses/llm-mastery/20-attention-is-all-you-need-read/
course_track: "LLM Mastery"
description: "Strip away the mystique and the paper describes something you can draw on one whiteboard: a stack of attention-plus-MLP blocks with residual connections, made parallel-friendly on purpose."
level: Intermediate
toc:
  - id: "what-problem-the-paper-is-actually-solving"
    label: "What problem the paper is actually solving"
  - id: "the-decoder-block-in-full"
    label: "The decoder block, in full"
  - id: "a-minimal-block-you-can-run"
    label: "A minimal block you can run"
  - id: "why-it-scaled-the-parallelism-argument-again"
    label: "Why it scaled: the parallelism argument, again"
  - id: "failure-mode-mistaking-the-diagram-for-the-details"
    label: "Failure mode: mistaking the diagram for the details"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 20/50** · Karpathy-style LLM course

"Attention Is All You Need" (Vaswani et al., 2017) gets talked about as if it dropped a wholly new kind of intelligence on the world. Read past the framing and it's a systems paper as much as a modeling paper: nearly every individual piece — attention, residual connections, layer normalization, position-wise feed-forward layers — already existed. The contribution was combining them into an architecture with *no* recurrence at all, engineered specifically so every position in a sequence could be processed in parallel.

## What problem the paper is actually solving
{: #what-problem-the-paper-is-actually-solving }

Article 18 established the actual engineering problem: RNNs (even with the attention bolted on from article 19) are sequential across time, and sequential doesn't parallelize on GPUs. The paper's title is a direct claim about the fix — you don't need recurrence at all, *only* attention (plus the standard supporting cast of MLPs, residuals, and normalization) is sufficient to model sequences well, and doing so removes the sequential bottleneck entirely. Every architectural choice in the paper should be read through that lens: what does this choice buy in terms of parallelism, and what does it cost.

## The decoder block, in full
{: #the-decoder-block-in-full }

The repeating unit — stacked `N` times to build the full model — is four operations, in order:

```
1. x = x + MultiHeadSelfAttention(LayerNorm(x))     # attention sublayer, residual
2. x = x + FeedForwardMLP(LayerNorm(x))              # MLP sublayer, residual
```

(This is the modern **Pre-Norm** ordering — normalize, then transform, then add back to the residual stream — which is what nearly every LLM you'll encounter actually uses, even though the original 2017 paper used Post-Norm, normalizing *after* the residual addition instead. Pre-Norm turned out to train more stably at depth, and the field converged on it within a couple of years.)

Read those two lines carefully, because they are the entire repeating unit of a GPT-style model: attention mixes information *across* positions (each token gets to look at other tokens), the MLP transforms information *within* a position independently (no cross-token mixing at all inside the MLP — every position runs through the identical MLP weights, but on its own data), and both sublayers are wrapped in a residual connection so gradient always has an unimpeded identity path back through arbitrarily many stacked blocks, exactly the mechanism discussed in article 11 for taming vanishing gradients at depth.

Around this repeating block: a token embedding table converts input IDs into vectors, a positional signal is added (since self-attention alone has no notion of order — permute the input tokens and attention's output permutes identically, with nothing telling it "token 3 comes before token 7"), the block is stacked `N` times, and a final linear layer projects back to vocabulary size followed by softmax to produce next-token probabilities.

## A minimal block you can run
{: #a-minimal-block-you-can-run }

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
            nn.Linear(d_model, 4 * d_model),
            nn.GELU(),
            nn.Linear(4 * d_model, d_model),
        )

    def forward(self, x, causal_mask):
        h = self.ln1(x)
        attn_out, _ = self.attn(h, h, h, attn_mask=causal_mask, need_weights=False)
        x = x + attn_out
        x = x + self.mlp(self.ln2(x))
        return x

B, T, d_model, n_head = 2, 16, 128, 8
x = torch.randn(B, T, d_model)
causal_mask = torch.triu(torch.full((T, T), float("-inf")), diagonal=1)
block = Block(d_model, n_head)
out = block(x, causal_mask)
print(out.shape)  # torch.Size([2, 16, 128]) — same shape as input, every time
```

The output shape matching the input shape (`B, T, d_model` in, `B, T, d_model` out) is not incidental — it's the residual-stream design from article 13 restated: every block *edits* the same-shaped tensor, which is exactly what lets you stack `N` identical blocks without any reshaping logic between them. `causal_mask` fills the upper triangle with `-inf` so that, after softmax, positions can never attend to positions after themselves — this is what makes the model a valid autoregressive next-token predictor rather than one that peeks at the future during training.

## Why it scaled: the parallelism argument, again
{: #why-it-scaled-the-parallelism-argument-again }

Compute the attention scores in the code above (`Q @ K^T`) and every entry of that `T × T` matrix is computable independently of every other entry — there is no data dependency like the `h_t` depends-on-`h_{t-1}` chain from article 18. The entire self-attention operation for a whole sequence is one matrix multiplication, and matrix multiplication is precisely the operation GPUs are built to do at enormous scale in parallel. Combine that with the position-wise MLP (also fully parallel across positions, since it applies the same weights independently at every position with no cross-talk) and the entire forward pass of a Transformer block has no forced sequential dependency across the time dimension at all — only across depth (layer `N` needs layer `N-1`'s output), which is a much shallower dependency chain than one step per token.

This parallelism is the actual mechanistic reason Transformers could absorb far more training compute and far more data than RNN-based approaches ever practically could — not because attention is a "smarter" mechanism in some abstract sense, but because it maps onto the hardware differently, and that mapping is what let the following decade of scaling laws research (article 30) even become a viable strategy.

## Failure mode: mistaking the diagram for the details
{: #failure-mode-mistaking-the-diagram-for-the-details }

The most common way people misread this paper: treating the now-famous architecture diagram as if it fully specifies a working model, when several load-bearing details live only in the text or have since been revised by the field's collective experience. The original paper uses Post-Norm; almost every model you'll actually use uses Pre-Norm, for concrete, measurable training-stability reasons discovered after publication. The original uses a specific hand-designed sinusoidal positional encoding; many modern models use learned positional embeddings or RoPE instead (article 23). The original uses ReLU in the feed-forward block; most modern models use GELU or SwiGLU. None of these are "the paper was wrong" — they're the field iterating on a specific component while keeping the overall attention-plus-MLP-plus-residual skeleton intact.

The habit this should build: when you read *any* architecture paper, separate "the core idea being demonstrated" from "the specific hyperparameter and component choices used to demonstrate it." The core idea of this paper — recurrence-free, fully parallel sequence modeling via attention — has survived essentially unchanged for years. Nearly every specific component choice around that core idea has been revised at least once by later work.

## Exercise
{: #exercise }

Draw one decoder block by hand — literally sketch it, don't just read the diagram above — and label every tensor with its `(B, T, C)` shape as it flows through: input, after `LayerNorm`, after attention, after the residual add, after the second `LayerNorm`, after the MLP's expansion to `4*C`, after the MLP's projection back to `C`, and after the second residual add. Concrete check: every single tensor you label should have exactly the same shape, `(B, T, C)`, *except* the intermediate MLP activation right after the expansion layer, which should be `(B, T, 4*C)`. If any other tensor in your drawing has a different shape than `(B, T, C)`, you've misdrawn the residual stream — go back to article 13 and re-trace where the mismatch happened.


---

[← 19. Seq2Seq and the Dawn of Attention](/courses/llm-mastery/19-seq2seq-attention-dawn/)  
[21. Self-Attention Mechanics →](/courses/llm-mastery/21-self-attention-mechanics/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
