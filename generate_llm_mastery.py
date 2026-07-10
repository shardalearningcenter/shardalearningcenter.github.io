#!/usr/bin/env python3
"""Generate 50 Karpathy-style LLM mastery articles + tech getting-started posts."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
COURSE = ROOT / "courses" / "llm-mastery"
POSTS = ROOT / "_posts"
COURSE.mkdir(parents=True, exist_ok=True)
POSTS.mkdir(parents=True, exist_ok=True)

# (num, slug, title, level, summary, sections)
# sections: list of (heading, paragraphs, optional code)

ARTICLES: list[dict] = []


def A(num, slug, title, level, summary, body: str):
    ARTICLES.append(
        {
            "num": num,
            "slug": slug,
            "title": title,
            "level": level,
            "summary": summary,
            "body": body.strip() + "\n",
        }
    )


# —— Foundations (01–10) ——
A(
    1,
    "what-is-a-language-model",
    "What is a Language Model, Really?",
    "Beginner",
    "Strip the hype. An LM is a probability distribution over sequences of tokens.",
    """
## The only definition that matters

A language model answers one question: **given the text so far, what comes next?**

Not “understanding.” Not “consciousness.” Next token.

If you internalize that, everything else in this course is an engineering detail about *how* we approximate that distribution.

## Sequences and probability

Text is a sequence: `t1, t2, t3, …`. A model assigns:

```
P(t1, t2, …, tn) = P(t1) · P(t2|t1) · P(t3|t1,t2) · …
```

Training = adjust parameters so this product is high on real text. Sampling = draw from those conditionals one token at a time.

## Why this is enough for “intelligence-looking” behavior

If next-token prediction is good enough, the model must compress a lot of the world into its weights: grammar, facts, style, even shallow reasoning patterns. That compression is the magic. The objective is still boring: maximize likelihood.

## Exercise

Write, in one sentence each: (1) what an LM predicts, (2) what “training” means, (3) what “sampling” means. Keep them free of marketing words.
""",
)

A(
    2,
    "tokens-not-words",
    "Tokens Are Not Words",
    "Beginner",
    "Tokenization is the unglamorous gatekeeper of every LLM.",
    """
## Characters → bytes → tokens

Models don’t see “words.” They see **token IDs** — integers from a fixed vocabulary.

Modern LLMs use **subword** tokenizers (BPE, SentencePiece). Common words are one token; rare words split into pieces.

```python
# Conceptual — not a real tokenizer
text = "unbelievable"
# might become: ["un", "believ", "able"] → [1045, 8921, 334]
```

## Why tokenization matters more than you think

- Context length is in **tokens**, not words.
- Cost is per token.
- Weird bugs (“the model can’t spell”) are often tokenizer artifacts.
- Multilingual quality depends heavily on how the vocab was built.

## A mental model

Tokenizer = compression codec for text. The neural net only ever sees the compressed stream.

## Exercise

Take a sentence and guess which pieces would be single tokens vs split. Then check with any online BPE demo or `tiktoken` if you have it.
""",
)

A(
    3,
    "next-token-prediction",
    "Next-Token Prediction Is the Game",
    "Beginner",
    "Everything — chat, code, agents — is still next-token prediction underneath.",
    """
## Autoregressive generation

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

During training we don’t sample. We feed the true previous tokens and ask the model to predict the true next one at every position. Loss = average cross-entropy.

## Temperature, top-k, top-p

Sampling knobs reshape `probs` before you draw. Temperature → 0 is greedy. High temperature is chaotic. Top-p keeps the smallest set of tokens whose cumulative probability ≥ p.

## Exercise

Explain why greedy decoding often looks “safer” but more repetitive than sampling.
""",
)

A(
    4,
    "bigram-language-model",
    "Your First LM: Bigrams",
    "Beginner",
    "Count pairs. Normalize. Sample. Feel the soul of language modeling.",
    """
## The smallest interesting model

A **bigram** model only conditions on the previous token:

```
P(t_i | t_{i-1})
```

Count how often `a` is followed by `b`. Divide by counts of `a`. Done.

```python
from collections import defaultdict, Counter

def train_bigrams(tokens):
    counts = defaultdict(Counter)
    for a, b in zip(tokens, tokens[1:]):
        counts[a][b] += 1
    return counts

def sample(counts, start, n=50):
    import random
    out = [start]
    for _ in range(n):
        dist = counts[out[-1]]
        if not dist:
            break
        toks, ws = zip(*dist.items())
        out.append(random.choices(toks, weights=ws, k=1)[0])
    return out
```

## What you learn

Bigrams capture local habits (“q” → “u”) but can’t plan. Long-range structure needs more context — and eventually, neural nets.

## Exercise

Train character bigrams on a tiny text file. Sample 200 characters. Notice the local fluency and global nonsense.
""",
)

A(
    5,
    "loss-cross-entropy",
    "Loss: Cross-Entropy Without the Fear",
    "Beginner",
    "Cross-entropy is just “how surprised was the model by the true next token?”",
    """
## Intuition

If the model puts probability `p` on the correct next token, the loss for that step is `-log(p)`.

- `p = 1.0` → loss 0 (perfect)
- `p = 0.5` → loss ~0.69
- `p → 0` → loss → ∞ (very bad)

Average over the dataset. That’s training.

## Softmax

The network outputs raw scores (logits). Softmax turns them into a probability distribution. Cross-entropy then compares that distribution to a one-hot (the true token).

## Why we care

Lower loss ≈ better compression of the training text ≈ usually better samples. Not always identical to “usefulness,” but it’s the right north star for pretraining.

## Exercise

If a model assigns 0.1 to the correct token, what’s the per-token loss? (Use natural log.)
""",
)

A(
    6,
    "embeddings-intuition",
    "Embeddings: Meaning as Geometry",
    "Beginner",
    "Tokens live as vectors. Nearby vectors ≈ related usage.",
    """
## Lookup tables with ambition

An embedding matrix `E` has shape `[vocab_size, dim]`. Token id `i` becomes row `E[i]` — a vector in R^d.

Training moves these vectors so that tokens used in similar contexts end up nearby (roughly).

## Why vectors?

Neural nets need continuous inputs. Discrete IDs don’t add or multiply meaningfully. Vectors do.

## Dimensionality

Small dim → underfit. Huge dim → expensive and data-hungry. Typical LLM dims: hundreds to thousands.

## Exercise

In your own words: what does it mean for two embedding vectors to be “close”?
""",
)

A(
    7,
    "mlp-language-model",
    "Neural Nets for Language: The MLP",
    "Beginner",
    "Bengio’s classic: embed context → concatenate → MLP → softmax.",
    """
## From counts to parameters

Instead of a giant count table, learn a function:

1. Take last `n` tokens
2. Embed each
3. Concatenate
4. Feed a multilayer perceptron
5. Softmax over vocabulary

This is the **neural probabilistic language model** lineage. Still local context, but shared parameters generalize better than raw counts.

## Capacity vs context

MLP LMs struggle with long context because the input size grows with `n`, and there’s no clever reuse across positions yet. Transformers will fix that with attention.

## Exercise

If vocab=10k, n=3, dim=32, how big is the concatenated MLP input?
""",
)

A(
    8,
    "training-loop-basics",
    "The Training Loop, End to End",
    "Beginner",
    "Batch → forward → loss → backward → optimizer step. Repeat.",
    """
## The sacred loop

```python
for step in range(max_steps):
    x, y = get_batch()          # context, next-token targets
    logits = model(x)
    loss = cross_entropy(logits, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

Everything fancy (mixed precision, grad clip, LR schedules) decorates this loop. Don’t lose the plot.

## Batches

We train on many sequences in parallel for GPU efficiency. Loss is averaged.

## Checkpoints

Save weights periodically. Training is long; disks are cheap; tears are expensive.

## Exercise

Write the training loop from memory without looking. Then check yourself.
""",
)

A(
    9,
    "overfitting-underfitting",
    "Overfitting, Underfitting, and Data",
    "Beginner",
    "Models memorize. Data is the real moat. Regularization is damage control.",
    """
## Two failure modes

- **Underfit:** train loss high, model too weak or undertrained.
- **Overfit:** train loss low, val loss high — memorization.

LLMs trained on internet-scale data still memorize. That’s not always bad (facts!), but eval leakage is a real scientific problem.

## What actually helps

More diverse data, careful dedup, regularization (dropout, weight decay), early stopping on a true held-out set.

## Exercise

Why is “test set contamination” especially nasty for LLM benchmarks?
""",
)

A(
    10,
    "makemore-mindset",
    "The MakeMore Mindset: Build Tiny, Understand Deeply",
    "Beginner",
    "Karpathy’s method: toy problems that expose the real machinery.",
    """
## Why toy models

If you can’t train a name generator on 10k names, you don’t understand GPT-4’s soul — you only understand its press release.

Tiny models force you to see:
- shapes of tensors
- what loss curves mean
- how sampling feels
- where bugs hide

## A curriculum of toys

1. Bigrams
2. MLP LM
3. WaveNet-ish dilated conv (optional)
4. Tiny Transformer
5. Scale up carefully

## Exercise

Pick a tiny dataset (names, cities, Pokemon). Commit to shipping a sampler this week.
""",
)

# —— Neural guts (11–20) ——
A(
    11,
    "backprop-intuition",
    "Backpropagation as Local Blame",
    "Intermediate",
    "Every node asks: how did I affect the loss? Then tells its parents.",
    """
## The story

Forward pass: compute outputs.
Backward pass: each operation receives `dloss/doutput` and multiplies by local derivatives to produce `dloss/dinputs`.

Chain rule, implemented as a graph traversal. Frameworks do it for you; you must still feel it.

## Why grads vanish or explode

Multiply many numbers <1 → vanish. Many >1 → explode. Depth is dangerous without care (init, residual, norm).

## Exercise

For `y = a*b`, if `dL/dy = 2`, `a=3`, `b=4`, what are `dL/da` and `dL/db`?
""",
)

A(
    12,
    "autograd-from-scratch",
    "Micrograd Energy: Autograd From Scratch",
    "Intermediate",
    "A Value object with .grad is enough to demystify PyTorch.",
    """
## Minimal idea

```python
class Value:
    def __init__(self, data, children=()):
        self.data = data
        self.grad = 0.0
        self._prev = set(children)
        self._backward = lambda: None

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other))
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out
```

Build `*`, `tanh`, `backward()` topological sort. Suddenly `loss.backward()` is not magic.

## Exercise

Implement `__mul__` and verify a tiny expression’s gradients by hand.
""",
)

A(
    13,
    "tensors-shapes-discipline",
    "Tensor Shapes: The Hidden Curriculum",
    "Intermediate",
    "Most LLM bugs are shape bugs. Become religious about them.",
    """
## Always know

For a Transformer block, chant:

```
B = batch
T = time (tokens)
C = channels (d_model)
```

Attention scores: `B, n_head, T, T`
Values projected: `B, n_head, T, head_dim`

## Print shapes

`print(x.shape)` is not shameful. It’s professionalism.

## Exercise

If B=2, T=8, C=32, n_head=4, what is `head_dim`?
""",
)

A(
    14,
    "softmax-temperature",
    "Softmax and Temperature, Carefully",
    "Intermediate",
    "Softmax is competitive normalization. Temperature rewires the competition.",
    """
## Softmax

```
softmax(z)_i = exp(z_i) / sum_j exp(z_j)
```

Numerically: subtract `max(z)` first or you explode `exp`.

## Temperature

Use `softmax(z / T)`.
- T→0: winner-take-all
- T=1: default
- T>1: flatter, more random

## Exercise

Why is subtracting max(z) safe (doesn’t change softmax)?
""",
)

A(
    15,
    "optimization-sgd-adam",
    "SGD, Adam, and Why Adam Won LLMs",
    "Intermediate",
    "Adaptive methods handle messy gradient scales in deep nets.",
    """
## SGD

`θ ← θ - lr * grad`

Simple. Sensitive to LR. Needs help (momentum).

## Adam

Keeps exponential moving averages of grad and grad². Per-parameter step sizes. Default for many LLM runs (AdamW = Adam + decoupled weight decay).

## Learning rate

Too high: loss NaNs. Too low: you age waiting. Warmup + cosine decay is a common LLM recipe.

## Exercise

In one paragraph: what problem does adaptive LR solve?
""",
)

A(
    16,
    "initialization-matters",
    "Initialization Is Not Optional",
    "Intermediate",
    "Bad init → dead ReLUs / exploding signals. Good init → training starts.",
    """
## Goal

Keep activation variances reasonable as you go deeper.

## Common practices

- Xavier / Kaiming init depending on nonlinearity
- Residual networks prefer specific scales
- Embedding init often small random

## Signal

If day-0 loss is insane or grads are zero, suspect init + architecture before “more data.”

## Exercise

What happens to a deep net with all weights initialized to 0?
""",
)

A(
    17,
    "regularization-dropout",
    "Dropout, Weight Decay, and Noise as Teachers",
    "Intermediate",
    "Regularization = deliberate handicap so the model can’t memorize casually.",
    """
## Dropout

Randomly zero activations in training. Forces redundant representations. Off at eval (rescale).

## Weight decay

Penalize large weights. AdamW does this cleanly.

## Data > tricks

For LLMs, scale and data quality dominate. Regularization still matters, especially on smaller runs.

## Exercise

Why must dropout behave differently at train vs eval?
""",
)

A(
    18,
    "rnns-and-their-pain",
    "RNNs: The Old Kings and Their Pain",
    "Intermediate",
    "Recurrence is elegant and slow. Parallelism wants Transformers.",
    """
## The idea

Hidden state `h_t = f(h_{t-1}, x_t)`. Sequential by construction.

## Why we moved on

- Hard to parallelize across time on GPUs
- Long-range gradients struggle (LSTM/GRU help, don’t solve)
- Transformers train faster at scale

Still worth knowing: sequential state is a clean mental model.

## Exercise

Name one strength RNNs still have vs vanilla Transformers.
""",
)

A(
    19,
    "seq2seq-attention-dawn",
    "Seq2Seq and the Dawn of Attention",
    "Intermediate",
    "Attention began as “look at the source while decoding.”",
    """
## Encoder–decoder

Encode source sentence to memory. Decode target tokens while attending to encoder states.

## Attention score

For each decoder step, weight encoder positions by relevance. Soft alignment.

This idea — **content-based lookup over a set of vectors** — becomes the Transformer’s core when applied everywhere.

## Exercise

In translation, why is a single fixed vector bottleneck painful for long sentences?
""",
)

A(
    20,
    "attention-is-all-you-need-read",
    "Reading 'Attention Is All You Need' Like an Engineer",
    "Intermediate",
    "Skip the mystique. It’s a stack of attention + MLP blocks with residuals.",
    """
## The Transformer block (decoder-ish)

1. Multi-head self-attention
2. Add & LayerNorm (or Pre-Norm variants)
3. Feed-forward MLP (usually 4× width)
4. Add & LayerNorm

Stack N times. Add token + position embeddings at the front. Linear + softmax at the end.

## Why it scaled

Attention is parallel across positions (with a cost). GPUs love that. Add data and depth.

## Exercise

Draw one block. Label tensors with `B,T,C`.
""",
)

# —— Transformers deep (21–35) ——
A(
    21,
    "self-attention-mechanics",
    "Self-Attention Mechanics",
    "Intermediate",
    "Q, K, V are just linear projections. The softmax is the routing.",
    """
## Equations with intent

```
Q = X Wq
K = X Wk
V = X Wv
attn = softmax(Q K^T / sqrt(d_k))
out = attn V
```

Each token builds a query (“what am I looking for?”), keys answer (“what do I contain?”), values provide content to mix.

## Causal mask

For LMs, position i cannot see j > i. Mask those scores to `-inf` before softmax.

## Exercise

Why divide by `sqrt(d_k)`?
""",
)

A(
    22,
    "multi-head-attention",
    "Multi-Head Attention",
    "Intermediate",
    "Multiple smaller attentions in parallel = several routing specialists.",
    """
## Idea

Split channels into `h` heads. Each head attends independently, then concatenate and project.

Different heads can learn different patterns: local syntax, brackets, rare long links.

## Cost

Attention is `O(T²)` per head in the naive form. Long context is expensive. Hence all the efficient-attention research.

## Exercise

If C=768 and h=12, what’s `head_dim`?
""",
)

A(
    23,
    "positional-embeddings",
    "Positional Information: Absolute, Relative, RoPE",
    "Intermediate",
    "Attention alone is permutation-equivariant. Position must be injected.",
    """
## Absolute embeddings

Add a learned vector per position index. Simple. Weak for very long contexts.

## Relative / RoPE

Modern LLMs often use **rotary embeddings (RoPE)**: rotate Q/K by position-dependent angles so attention becomes relative-friendly.

## Intuition

Without position, “dog bites man” and “man bites dog” are bag-similar to the attention mixer.

## Exercise

Why can’t a plain self-attention layer, alone, know order?
""",
)

A(
    24,
    "layernorm-residuals",
    "Residuals and LayerNorm: The Stabilizers",
    "Intermediate",
    "Skip connections make depth trainable. Norm keeps scales sane.",
    """
## Residual stream

`x = x + SubLayer(x)`

The model learns *edits* to a running representation. Gradients have a highway.

## LayerNorm / RMSNorm

Normalize across features. Pre-Norm (norm before sublayer) is common in LLMs for stability.

## Exercise

If you remove residuals from a 24-layer net, what usually happens to training?
""",
)

A(
    25,
    "mlp-in-transformer",
    "The Transformer MLP: Where Facts Often Live",
    "Intermediate",
    "Attention routes; MLPs transform. A lot of knowledge is in the MLP weights.",
    """
## Structure

Usually: `Linear → GELU/SiLU → Linear`, expanding to 4× (or more) then back.

## Role

Channel mixing. Nonlinear features. Empirically, many “memorized” associations show up in MLP subspaces (interpretability research).

## Exercise

If d_model=512 and expansion=4, how many params roughly in one MLP (ignore biases)?
""",
)

A(
    26,
    "gpt-architecture",
    "GPT Architecture: Decoder-Only Transformers",
    "Intermediate",
    "Causal self-attention stack. No encoder. Generate left to right.",
    """
## Recipe

- Token embedding + position scheme
- N × (causal MHA + MLP) with norms/residuals
- Final norm + vocab projection
- Train with next-token cross-entropy

That’s GPT-2/3-style at a high level. Details differ (norm placement, activation, bias, RoPE, etc.).

## Exercise

Name three differences between encoder-decoder T5 and decoder-only GPT.
""",
)

A(
    27,
    "implement-tiny-gpt",
    "Implement a Tiny GPT (Conceptual Walkthrough)",
    "Advanced",
    "If you can write the shapes, you can write the model.",
    """
## Skeleton

```python
class CausalSelfAttention(nn.Module):
    ...

class Block(nn.Module):
    def __init__(self, cfg):
        ...
    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.mlp(self.ln2(x))
        return x

class GPT(nn.Module):
    def forward(self, idx, targets=None):
        # embed → blocks → ln → logits
        # optional loss
```

Fill the blanks with real code in your environment. Start with char-level Shakespeare.

## Exercise

Train until loss drops meaningfully. Sample. Celebrate ugly but real text.
""",
)

A(
    28,
    "kv-cache",
    "KV Cache: Why Chat Is Fast After the First Token",
    "Advanced",
    "Don’t recompute past keys/values every step.",
    """
## Problem

Naive generation recomputes attention over the full context each new token → wasteful.

## Fix

Cache K and V for past positions. Each step only computes the new row.

## Memory

KV cache is often the memory bottleneck for long-context serving.

## Exercise

If T=4096, layers=32, heads=32, head_dim=128, dtype=fp16, rough KV cache size per sequence?
""",
)

A(
    29,
    "batching-and-throughput",
    "Batching, Throughput, and the Economics of Tokens",
    "Advanced",
    "LLMs are memory-bandwidth beasts. Batching amortizes weight reads.",
    """
## Two regimes

- **Prefill:** process prompt (compute heavy, parallel over T)
- **Decode:** one token at a time (memory heavy)

## Continuous batching

Servers pack many sequences at different lengths to keep GPUs busy.

## Exercise

Why might increasing batch size stop helping after a point?
""",
)

A(
    30,
    "scaling-laws-intuition",
    "Scaling Laws: The Bitter Lesson, Quantified",
    "Advanced",
    "Loss improves predictably with scale — until data or compute is misallocated.",
    """
## The empirical story

Bigger models + more data + more compute → better loss, often smoothly.

Chinchilla-style results: **match model size to data**; don’t starve either.

## Caveats

Benchmarks saturate. Contamination. Emergent jumps can be metric artifacts. Still, scale is the default strategy.

## Exercise

If you double parameters but keep data fixed, what risk do you invite?
""",
)

A(
    31,
    "tokenization-deep-dive",
    "Tokenization Deep Dive: BPE Under the Hood",
    "Advanced",
    "Merge frequent pairs until vocab is full. That’s BPE.",
    """
## Algorithm (sketch)

1. Start with character/byte vocab
2. Count adjacent pairs in corpus
3. Merge the most frequent pair into a new token
4. Repeat until vocab_size

## Gotchas

Leading spaces, Unicode normalization, special tokens, domain shift (code vs prose).

## Exercise

Explain why “NotImplementedError” might be multiple tokens.
""",
)

A(
    32,
    "pretraining-data",
    "Pretraining Data: The Real Model",
    "Advanced",
    "Weights are a lossy compress of the dataset. Curate accordingly.",
    """
## Pipeline themes

Crawl → extract → filter → dedup → mix domains → pack into sequences.

Quality filters beat naive “more web.” Dedup matters for both loss and memorization.

## Mixtures

Code, math, multilingual, books — mixture weights are a product decision.

## Exercise

List three failure modes of training on raw unfiltered web text.
""",
)

A(
    33,
    "parallelism-ddp-fsdp",
    "Training Parallelism: DDP, FSDP, Pipeline",
    "Advanced",
    "One GPU is not enough. Split data, params, or layers.",
    """
## Data parallel

Same model, different batches, allreduce grads. Simple.

## FSDP / ZeRO

Shard parameters/optimizer states across ranks to fit bigger models.

## Pipeline / tensor parallel

Split the model graph. Harder engineering, needed at frontier scale.

## Exercise

Which parallelism primarily reduces **memory per GPU** for a single giant layer?
""",
)

A(
    34,
    "mixed-precision",
    "Mixed Precision Training",
    "Advanced",
    "fp16/bf16 for speed; keep master weights in fp32 for sanity.",
    """
## Why

Tensor Cores love lower precision. Memory bandwidth drops. Throughput rises.

## How

Forward/backward in bf16/fp16, update fp32 master copy. Loss scaling for fp16.

## bf16 vs fp16

bf16 has friendlier range; often stabler for LLMs on modern hardware.

## Exercise

Name one numerical failure mode fp16 introduces that bf16 softens.
""",
)

A(
    35,
    "eval-harness-thinking",
    "Evaluation: Beyond Vibes",
    "Advanced",
    "Loss, harnesses, human prefs — each lies in a different way.",
    """
## Layers of eval

1. Train/val loss
2. Standard NLP/code/math harnesses
3. Blind human preference (A/B)
4. Product metrics (task success)

## Contamination

If the test is in the train scrape, your “SOTA” is cosplay.

## Exercise

Design a tiny private eval set for *your* use case that won’t leak easily.
""",
)

# —— Post-training & systems (36–50) ——
A(
    36,
    "finetuning-sft",
    "Supervised Fine-Tuning (SFT)",
    "Advanced",
    "Teach the base model to follow instructions with curated demos.",
    """
## What changes

Same next-token loss, but data is (prompt, high-quality answer) dialogues.

## Data quality

A few thousand *excellent* examples can beat millions of mediocre ones for assistants.

## Risk

Catastrophic forgetting / style collapse. Mix a bit of pretraining distribution if needed.

## Exercise

Write 3 SFT examples for a “patient Python tutor” persona.
""",
)

A(
    37,
    "lora-peft",
    "LoRA and Parameter-Efficient Fine-Tuning",
    "Advanced",
    "Train low-rank adapters instead of all weights.",
    """
## Idea

Freeze base W. Learn `ΔW ≈ B A` with small rank r. Store adapters cheaply; swap personas.

## When to use

Limited compute, many tasks, fast iteration. Full finetune still wins sometimes at scale.

## Exercise

If W is 4096×4096 and r=8, how many adapter params roughly (A and B)?
""",
)

A(
    38,
    "preference-rlhf-dpo",
    "Preferences: RLHF and DPO",
    "Advanced",
    "Align to human (or AI) preferences when “correct next token” isn’t enough.",
    """
## RLHF sketch

SFT model → reward model on comparisons → RL (PPO) against reward with KL tether to SFT.

## DPO

Skip explicit RL: optimize a closed-form objective on preference pairs. Often simpler.

## Reality

Alignment is underspecified. Pref data has politics, taste, and annotator fatigue.

## Exercise

Why do we KL-penalize away from the SFT model during RLHF?
""",
)

A(
    39,
    "prompting-as-programming",
    "Prompting as Programming",
    "Intermediate",
    "The context window is a programmable scratchpad.",
    """
## Patterns

- Specs and constraints first
- Show formats with examples
- Chain of thought *when it helps* (and when you can verify)
- Tool contracts: clear JSON schemas

## Failure modes

Ambiguity, conflicting instructions, buried requirements, unvalidated outputs.

## Exercise

Rewrite a vague prompt into a tight spec with inputs/outputs/failure behavior.
""",
)

A(
    40,
    "rag-retrieval",
    "RAG: Retrieval-Augmented Generation",
    "Advanced",
    "Don’t stuff the world into weights. Fetch evidence at runtime.",
    """
## Pipeline

1. Index docs as embeddings
2. Retrieve top-k chunks for a query
3. Stuff into context with citations
4. Generate answer grounded in chunks

## Hard parts

Chunking, recall vs precision, stale indexes, citation faithfulness.

## Exercise

When is RAG better than finetuning? When is it worse?
""",
)

A(
    41,
    "agents-tool-use",
    "Agents and Tool Use",
    "Advanced",
    "Let the model call functions. Keep a tight loop and verify.",
    """
## Loop

```
observe → think → act(tool) → observe → …
```

Tools: search, code exec, DB, browser. The model emits structured calls; your runtime executes.

## Safety

Sandbox code. Rate-limit. Never trust free-form shell. Log everything.

## Exercise

Design 3 tools for a “repo assistant” and specify their schemas.
""",
)

A(
    42,
    "hallucinations",
    "Hallucinations: Why They Happen",
    "Advanced",
    "Sampling from a prior over text is not querying a database.",
    """
## Cause

The objective doesn’t require truth — only plausible continuation. If evidence isn’t in context/weights, fluent falsehoods appear.

## Mitigations

RAG, tools, calibration prompts, abstention, verification agents, smaller claims.

## Exercise

Give an example where higher temperature increases hallucination risk and why.
""",
)

A(
    43,
    "interpretability-basics",
    "Interpretability: Looking Inside",
    "Advanced",
    "Probes, activations, circuits — maps of a foreign city.",
    """
## Tools of the trade

- Activation inspection
- Linear probes
- Causal interventions / ablation
- Sparse autoencoders (features)

## Humility

We don’t fully “understand” frontier models. Partial maps still help debugging and safety.

## Exercise

What’s the difference between correlation (probe accuracy) and causation (intervention)?
""",
)

A(
    44,
    "quantization-serving",
    "Quantization and Local Serving",
    "Advanced",
    "Run big models on small machines by shrinking weights.",
    """
## Idea

Store weights in 8-bit / 4-bit. Accept small quality loss for huge memory wins.

## Formats

GGUF, GPTQ, AWQ — ecosystem moves fast; principles stay: calibrate, measure perplexity/task drop.

## Exercise

Why does 4-bit hurt some tasks more than others?
""",
)

A(
    45,
    "multimodal-llms",
    "Multimodal LLMs: Vision Enters the Context",
    "Advanced",
    "Images become token-like embeddings in the same residual stream.",
    """
## Pattern

Vision encoder → projector → prefixes into LLM token space. Train so visual tokens speak the language model’s dialect.

## Implications

UI agents, document understanding, robotics — same next-token core, richer observations.

## Exercise

Why might OCR-in-the-loop still beat pure vision-LLM for dense text in images?
""",
)

A(
    46,
    "diffusion-vs-ar",
    "Diffusion vs Autoregressive: Two Generative Religions",
    "Advanced",
    "LMs are usually AR. Images often diffusion. Hybrids exist.",
    """
## Autoregressive

Factorize sequence left-to-right. Natural for text.

## Diffusion

Iteratively denoising from noise. Strong for continuous data like images.

## Convergence

Research explores discrete diffusion for text and AR for pixels. Know both toolkits.

## Exercise

Name one pros/cons for AR text generation vs a hypothetical diffusion LM.
""",
)

A(
    47,
    "safety-security",
    "Safety, Security, and Prompt Injection",
    "Advanced",
    "Untrusted text in the context window is a control-plane attack.",
    """
## Prompt injection

Retrieved docs or user content says: “Ignore previous instructions…” The model might obey.

## Defenses

Separation of instructions vs data, least-privilege tools, output filters, human approvals for risky actions.

## Exercise

Write an attack string against a naive “summarize this email and send reply” agent.
""",
)

A(
    48,
    "building-eval-driven",
    "Build Eval-Driven: A Practical Workflow",
    "Advanced",
    "Ship loops: measure → change one thing → measure again.",
    """
## Workflow

1. Define tasks with golden checks
2. Log traces (prompt, tools, output)
3. Change one variable (prompt, model, retriever)
4. Compare scores + spot-check failures

## Anti-pattern

Vibes-only demos. They don’t survive contact with users.

## Exercise

Create a 10-case eval for a FAQ bot you care about.
""",
)

A(
    49,
    "research-taste",
    "Research Taste: How to Read Papers",
    "Master",
    "Figures first. Ablations second. Claims last.",
    """
## A Karpathy-ish reading order

1. What problem? Why now?
2. Method diagram
3. Main result table
4. Ablations (did they earn the claim?)
5. Limitations
6. Skim math if needed

## Reimplement

If it matters, reimplement a toy version. Understanding is a verb.

## Exercise

Pick one paper. Write a half-page “what I’d reimplement in a weekend.”
""",
)

A(
    50,
    "capstone-train-your-own",
    "Capstone: Train Your Own Tiny LLM",
    "Master",
    "Data → tokenizer → GPT → train → sample → eval → writeup.",
    """
## The project

1. Collect 10–100MB of text you like (public domain / permitted)
2. Train a tokenizer (or reuse a small one)
3. Implement a ~10–50M param GPT
4. Train until loss is healthy
5. Build a tiny sampling UI
6. Write a post: curves, samples, failures

## Success criteria

Not SOTA. **Understanding.** You can explain every tensor.

## Final words

The field moves. The primitives don’t: tokens, loss, attention, data, eval. Master those and you can absorb tomorrow’s paper before lunch.

Now go train something.
""",
)


def write_article(a: dict, toc_entries: list[dict]) -> Path:
    num = a["num"]
    slug = f"{num:02d}-{a['slug']}"
    path = COURSE / f"{slug}.md"
    prev_link = ""
    next_link = ""
    if num > 1:
        p = ARTICLES[num - 2]
        prev_link = f"[← {p['num']:02d}. {p['title']}](/courses/llm-mastery/{p['num']:02d}-{p['slug']}/)"
    if num < 50:
        n = ARTICLES[num]
        next_link = f"[{n['num']:02d}. {n['title']} →](/courses/llm-mastery/{n['num']:02d}-{n['slug']}/)"

    toc_yaml = "\n".join(
        f'  - id: "{t["id"]}"\n    label: "{t["label"]}"' for t in toc_entries
    )

    # inject heading ids for ## in body
    body = a["body"]
    import re

    def repl(m):
        label = m.group(1).strip()
        sid = re.sub(r"[^\w\s-]", "", label.lower())
        sid = re.sub(r"[-\s]+", "-", sid).strip("-")
        return f"## {label}\n{{: #{sid} }}"

    body_ids = re.sub(r"^##\s+(.+)$", repl, body, flags=re.M)

    nav = f"\n\n---\n\n{prev_link}  \n{next_link}\n\n[Course hub](/courses/llm-mastery/) · [All courses](/courses/)\n"

    fm = f"""---
layout: course
title: "{num:02d}. {a['title']}"
permalink: /courses/llm-mastery/{slug}/
course_track: "LLM Mastery"
description: "{a['summary']}"
level: {a['level']}
toc:
{toc_yaml}
---
"""
    content = (
        f"> **Level:** {a['level']} · **Article {num}/50** · Karpathy-style LLM course\n\n"
        f"{a['summary']}\n\n{body_ids}{nav}"
    )
    path.write_text(fm + "\n" + content, encoding="utf-8")
    return path


def toc_for_body(body: str) -> list[dict]:
    import re

    out = []
    for m in re.finditer(r"^##\s+(.+)$", body, re.M):
        label = m.group(1).strip()
        sid = re.sub(r"[^\w\s-]", "", label.lower())
        sid = re.sub(r"[-\s]+", "-", sid).strip("-")
        out.append({"id": sid, "label": label[:70]})
    return out


def write_hub():
    rows = []
    toc = []
    for a in ARTICLES:
        slug = f"{a['num']:02d}-{a['slug']}"
        url = f"/courses/llm-mastery/{slug}/"
        rows.append(
            f"| {a['num']:02d} | [{a['title']}]({url}) | {a['level']} |"
        )
        toc.append({"id": f"part-{a['num']}", "label": f"{a['num']:02d}. {a['title'][:50]}"})

    phases = """
## How to use this course

1. Go in order. Later articles assume earlier scars.
2. Type code yourself. Reading is not training.
3. Keep a notes file of tensor shapes and failure modes.
4. Capstone (article 50) is mandatory if you want the “master” badge from yourself.

## Curriculum map

| Phase | Articles | Focus |
|------:|----------|-------|
| Foundations | 01–10 | Tokens, loss, bigrams, MLP mindset |
| Neural guts | 11–20 | Autograd, optimization, attention dawn |
| Transformers | 21–35 | GPT internals, systems, scaling |
| Post-training | 36–50 | SFT, LoRA, RLHF/DPO, RAG, agents, capstone |
"""

    toc_yaml = "\n".join(
        f'  - id: "art-{a["num"]:02d}"\n    label: "{a["num"]:02d}. {a["title"][:55].replace(chr(34), "")}"'
        for a in ARTICLES
    )

    hub = f"""---
layout: course
title: "LLM Mastery: Beginner to Master (50 Articles)"
permalink: /courses/llm-mastery/
course_track: "LLM Mastery"
description: "A Karpathy-style path from tokens to transformers, alignment, RAG, and training your own tiny LLM."
toc:
{toc_yaml}
---

# LLM Mastery — 50 articles, first principles

Written in the spirit of **Andrej Karpathy**: build tiny things, understand deeply, distrust vibes, love loss curves.

{phases}

## All articles

| # | Article | Level |
|---|---------|-------|
{chr(10).join(rows)}

## Start

→ [01. What is a Language Model, Really?](/courses/llm-mastery/01-what-is-a-language-model/)
"""
    # Hub lives at courses/llm-mastery.md (permalink /courses/llm-mastery/)
    # Articles live in courses/llm-mastery/*.md — do not write index.md here.
    (ROOT / "courses" / "llm-mastery.md").write_text(hub, encoding="utf-8")


TECH_POSTS = [
    (
        "2026-07-10-getting-started-with-python.md",
        "Getting Started with Python (the useful parts)",
        """
Python is the glue language of modern AI. Here’s the minimum to be dangerous.

## Install

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install numpy
```

## Core ideas in one screen

- Everything is an object
- Lists vs dicts vs sets
- Functions are first-class
- `with` for resources
- Virtualenvs keep projects sane

## Tiny project

Write a script that reads a text file and prints the 20 most common words.

## Next

[Python in 10 Days course](/courses/python-10-days/)
""",
    ),
    (
        "2026-07-10-getting-started-with-git.md",
        "Getting Started with Git (without the fear)",
        """
Git is a time machine for your files. Learn five commands deeply.

## Daily driver

```bash
git status
git add -p
git commit -m "message"
git log --oneline
git diff
```

## Mental model

- Working tree → staging → commit
- Branches are movable labels
- `pull --rebase` keeps history readable (when you understand it)

## Exercise

Init a repo, make 3 commits, create a branch, merge it back.
""",
    ),
    (
        "2026-07-10-getting-started-with-linux-shell.md",
        "Getting Started with the Linux Shell",
        """
The shell is how you talk to the machine without a mouse.

## Survival kit

```bash
pwd; ls -la; cd; mkdir; cp; mv; rm
cat; less; head; tail
grep -R "TODO" .
curl -I https://example.com
```

## Pipes

```bash
cat log.txt | grep ERROR | wc -l
```

## Exercise

Write a one-liner that counts unique IP addresses in a log file format you invent.
""",
    ),
    (
        "2026-07-10-getting-started-with-docker.md",
        "Getting Started with Docker",
        """
Docker packages “it works on my machine” into something shippable.

## Concepts

Image = recipe + filesystem snapshot. Container = running instance.

```bash
docker run --rm -it python:3.12-slim bash
```

## Minimal Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## Exercise

Containerize a 10-line Flask or FastAPI hello world.
""",
    ),
    (
        "2026-07-10-getting-started-with-javascript.md",
        "Getting Started with JavaScript",
        """
JS runs in the browser and on the server (Node). Start in the browser console.

## Essentials

- `let` / `const`
- Functions and arrow functions
- Arrays + `map`/`filter`
- Promises / `async await`
- DOM basics

## Exercise

Build a page with a button that fetches `https://httpbin.org/get` and shows JSON.
""",
    ),
    (
        "2026-07-10-getting-started-with-sql.md",
        "Getting Started with SQL",
        """
SQL is how you ask structured questions of tables.

## Core verbs

```sql
SELECT col FROM table WHERE cond ORDER BY col LIMIT 10;
JOIN ... ON ...
GROUP BY ... HAVING ...
INSERT/UPDATE/DELETE
```

## Exercise

Design tables for a blog (users, posts, comments) and write a query for “top 5 commenters.”
""",
    ),
    (
        "2026-07-10-getting-started-with-pytorch.md",
        "Getting Started with PyTorch for LLMs",
        """
PyTorch is the default dialect for researchy deep learning.

## Tensors

```python
import torch
x = torch.randn(2, 3)
y = x @ x.T
y.sum().backward()  # needs requires_grad_
```

## nn.Module

Subclass `nn.Module`, define `forward`, use `torch.optim`.

## Next

[LLM Mastery course](/courses/llm-mastery/) — especially articles 11–27.
""",
    ),
    (
        "2026-07-10-getting-started-with-fastapi.md",
        "Getting Started with FastAPI",
        """
FastAPI is a pleasant way to wrap models behind HTTP.

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}
```

## Exercise

Add a `POST /echo` that returns the JSON body. Then add input validation with Pydantic.
""",
    ),
]


def write_posts():
    for fname, title, body in TECH_POSTS:
        path = POSTS / fname
        path.write_text(
            f"""---
layout: post
title: "{title}"
date: 2026-07-10
description: "A practical getting-started guide."
---

{body.strip()}
""",
            encoding="utf-8",
        )
        print("post", fname)


def main():
    raise SystemExit(
        "REFUSING TO RUN: courses/llm-mastery/*.md and getting-started posts "
        "were rewritten in depth (see docs/PLAN-docs-rewrite.md). "
        "Re-running this generator would overwrite them with stubs. "
        "Edit the markdown files directly; do not regenerate from this script."
    )


if __name__ == "__main__":
    main()
