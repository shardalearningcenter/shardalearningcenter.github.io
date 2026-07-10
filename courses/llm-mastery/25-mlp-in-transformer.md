---
layout: course
title: "25. The Transformer MLP: Where Facts Often Live"
permalink: /courses/llm-mastery/25-mlp-in-transformer/
course_track: "LLM Mastery"
description: "Attention moves information between positions. The MLP is what actually happens once it arrives."
level: Intermediate
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-mail-routing-vs-what-you-do-with-the-mail"
    label: "Mental model: mail routing vs. what you do with the mail"
  - id: "worked-example-shapes-and-param-count"
    label: "Worked example: shapes and param count"
  - id: "where-the-knowledge-lives"
    label: "Where the knowledge lives"
  - id: "failure-mode-killing-the-nonlinearity"
    label: "Failure mode: killing the nonlinearity"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 25/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

Attention is the only part of a transformer block that lets information move *between* token positions. The MLP that follows it operates on each position completely independently — it never looks at any other token. That division of labor is not incidental; it's the entire architectural idea. Attention answers "who should I listen to," and the MLP answers "given what I just heard, what do I do with it." Roughly two-thirds of a standard transformer's parameters live in these MLP blocks, and a growing body of interpretability work suggests a large fraction of a model's factual recall lives there too, not in attention.

## Mental model: mail routing vs. what you do with the mail
{: #mental-model-mail-routing-vs-what-you-do-with-the-mail }

Attention is the mail routing system: it decides which desk's memo gets forwarded to which other desk, and how much weight to give each one. The MLP is what happens *at* a desk once the mail arrives — read it, apply your personal expertise, write a response, file it. Crucially, a desk with the MLP alone, no attention, can't do anything useful with information it never received; and attention alone, no MLP, can only ever produce weighted averages of what already existed — it has no capacity to compute something genuinely new from a token's content. A transformer block needs both: attention to gather the right inputs, MLP to nonlinearly transform them into something attention alone could never construct.

## Worked example: shapes and param count
{: #worked-example-shapes-and-param-count }

The standard transformer MLP is almost insultingly simple — two linear layers with a nonlinearity between them, expanding to 4× the model width and back down:

```python
import torch
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, d_model, expansion=4):
        super().__init__()
        d_ff = expansion * d_model
        self.fc_in = nn.Linear(d_model, d_ff)
        self.act = nn.GELU()
        self.fc_out = nn.Linear(d_ff, d_model)

    def forward(self, x):
        return self.fc_out(self.act(self.fc_in(x)))

d_model = 768
mlp = MLP(d_model)
x = torch.randn(2, 10, d_model)
out = mlp(x)
print(out.shape)  # torch.Size([2, 10, 768])

n_params = sum(p.numel() for p in mlp.parameters())
print(n_params)  # 4,722,432
```

Work out that parameter count by hand before trusting the printout: `fc_in` is `768 × 3072 + 3072 = 2,362,368`, `fc_out` is `3072 × 768 + 768 = 2,360,064`. Total: `4,722,432`. Compare that to a full multi-head attention block at the same `d_model` — `Wq, Wk, Wv, Wo` are each `768 × 768`, for `4 × 768² = 2,359,296` (plus small biases). The MLP block has *twice* the parameters of the attention block in every standard transformer layer. That ratio is why, when people say "most of a transformer's parameters are in the MLPs," it's a literal, countable fact, not a vibe.

## Where the knowledge lives
{: #where-the-knowledge-lives }

Interpretability research (notably the ROME/MEMIT line of work on locating and editing factual associations, and Anthropic's "toy models of superposition") has repeatedly found that specific factual associations — "the Eiffel Tower is in Paris" — can be localized to specific MLP weight matrices in specific middle layers, and edited by directly patching those weights, with the change generalizing correctly to paraphrases of the fact. The intuitive story: the residual stream at a token's position, after attention has gathered relevant context, contains something like "the entity being discussed is the Eiffel Tower, and the query is asking about location." The MLP's first linear layer projects that into a high-dimensional space where "Eiffel Tower + location-query" activates specific neurons, and the second linear layer maps those neurons back down to a residual-stream direction that boosts the logit for "Paris." Attention assembled the *question*; the MLP looked up the *answer*.

## Failure mode: killing the nonlinearity
{: #failure-mode-killing-the-nonlinearity }

Drop the activation function between the two linear layers — `fc_out(fc_in(x))` with nothing in between — and the entire block collapses mathematically into a single linear transformation, `x @ (W_in @ W_out)`, no matter how wide you make `d_ff`. All that 4× expansion buys you *nothing* without the nonlinearity: two consecutive linear layers are, by definition, just one linear layer with more expensive matrix multiplication to compute the same thing. This is a genuine bug people hit when refactoring — swap `nn.GELU()` for `nn.Identity()` while debugging something else, forget to swap it back, and the model still trains and produces a real loss curve, just one that plateaus noticeably higher than it should, because you've silently thrown away the model's only source of position-wise nonlinear capacity.

## Exercise
{: #exercise }

`d_model = 512`, expansion = `4`. Compute the exact parameter count for one MLP block (both linear layers, ignore biases for a round number). Then compute the parameter count for one full multi-head attention block at the same `d_model` (four `d_model × d_model` matrices). Confirm the MLP-to-attention ratio is exactly 2:1, and explain why that ratio is independent of `d_model` — it only depends on the expansion factor.

---

[← 24. Residuals and LayerNorm: The Stabilizers](/courses/llm-mastery/24-layernorm-residuals/)  
[26. GPT Architecture: Decoder-Only Transformers →](/courses/llm-mastery/26-gpt-architecture/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
