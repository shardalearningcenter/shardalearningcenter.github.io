---
layout: course
title: "19. Seq2Seq and the Dawn of Attention"
permalink: /courses/llm-mastery/19-seq2seq-attention-dawn/
course_track: "LLM Mastery"
description: "Attention was invented to fix one specific, nameable bottleneck in encoder-decoder translation models — a single fixed-size vector forced to carry an entire sentence. Everything downstream, including the modern Transformer, is that fix generalized."
level: Intermediate
toc:
  - id: "the-encoder-decoder-bottleneck"
    label: "The encoder-decoder bottleneck"
  - id: "attention-as-a-learned-lookup"
    label: "Attention as a learned lookup"
  - id: "a-worked-alignment-example"
    label: "A worked alignment example"
  - id: "the-generalization-that-mattered"
    label: "The generalization that mattered"
  - id: "failure-mode-treating-attention-weights-as-explanations"
    label: "Failure mode: treating attention weights as explanations"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 19/50** · Karpathy-style LLM course

Attention did not begin as the centerpiece of a new architecture. It began as a specific, targeted fix for a specific, measurable failure in machine translation models, and understanding that origin story makes the mechanism far less mysterious than it looks when you meet it for the first time inside a Transformer diagram.

## The encoder-decoder bottleneck
{: #the-encoder-decoder-bottleneck }

Before attention, the standard sequence-to-sequence recipe (Sutskever, Vinyals, and Le, 2014, among others) was: run an RNN encoder over the source sentence, take its *final* hidden state as a single fixed-size vector summarizing the entire sentence, then run an RNN decoder that generates the target sentence conditioned only on that one vector.

```
encoder: h_1, h_2, ..., h_T = RNN(source_tokens)
context = h_T                       # one vector, the entire sentence's memory
decoder: y_1, y_2, ..., y_S = RNN(context, previous_outputs)
```

This works for short sentences and degrades measurably as sentences get longer, and the reason is mechanical, not mysterious: `h_T` is a fixed-size vector — say, 512 numbers — and you're asking it to losslessly represent a 5-word sentence *and* a 50-word sentence with the same capacity budget. Information has to get compressed away as the sentence grows, and empirically, translation quality on long sentences dropped off measurably faster than on short ones in exactly this class of model. This is the concrete, checkable failure that motivated attention — not an abstract dissatisfaction with RNNs, but a specific bottleneck with a specific symptom.

## Attention as a learned lookup
{: #attention-as-a-learned-lookup }

The fix (Bahdanau, Cho, and Bengio, 2014): stop forcing the decoder to work from a single compressed vector. Instead, keep *all* the encoder's hidden states around — `h_1` through `h_T`, one per source position — and let the decoder, at every single output step, compute a fresh, learned weighting over all of them, based on what it currently needs.

```
score(s, h_i) = a(decoder_state_s, encoder_state_h_i)   # a learned compatibility function
weights = softmax(scores)                                # normalize into a distribution over source positions
context_s = sum_i(weights_i * h_i)                        # weighted blend of encoder states
```

This is, mechanically, precisely the query/key/value pattern you'll meet formally in article 21 — the decoder's current state acts as a **query** ("what do I need right now to produce the next word?"), every encoder hidden state acts as both a **key** (something to be scored against the query) and a **value** (the actual content to blend in if it scores well), and softmax turns raw compatibility scores into a normalized weighting. The vocabulary changed and the surrounding architecture changed dramatically over the following three years, but this core operation — score, normalize, weighted-blend — is unchanged from 2014 to the frontier models of today.

## A worked alignment example
{: #a-worked-alignment-example }

Here's a minimal, fully worked version of the mechanism, in numpy, translating the idea into code you can actually run and inspect:

```python
import numpy as np

def softmax(z):
    z = z - z.max()
    return np.exp(z) / np.exp(z).sum()

# 4 source positions, hidden size 6
encoder_states = np.random.randn(4, 6)   # h_1..h_4, shape (T=4, hidden=6)
decoder_query = np.random.randn(6)        # current decoder state

# simplest scoring function: dot product
scores = encoder_states @ decoder_query   # shape (4,) — one score per source position
weights = softmax(scores)                 # shape (4,) — sums to 1
context = weights @ encoder_states        # shape (6,) — weighted blend of encoder states

print(weights)   # e.g. [0.61, 0.05, 0.29, 0.05] — position 1 dominates this step
print(context.shape)
```

Run this with a decoder state that's deliberately made similar to `encoder_states[2]` (say, `decoder_query = encoder_states[2] + small noise`) and watch `weights` concentrate sharply on index 2 — the dot-product score for a well-matched pair is large, softmax amplifies that gap exponentially (article 14), and the resulting context vector is dominated by that one source position. This is the entire "soft alignment" story: the decoder learns, through training, to construct queries that align with the right source position at the right output step, and the mechanism itself is just scoring plus softmax plus weighted sum.

## The generalization that mattered
{: #the-generalization-that-mattered }

The 2014-2015 version of attention was still bolted onto an RNN encoder and an RNN decoder — attention fixed the *bottleneck*, but the sequential-processing cost from article 18 was still fully present on both sides. The generalization that produced the Transformer (article 20) was the realization that attention doesn't need an RNN at all: you can compute queries, keys, and values directly from a sequence's own token representations (this is **self**-attention — a sequence attending to itself, rather than a decoder attending to a separate encoder), stack these self-attention layers, and get a sequence model with *no* recurrence, hence no sequential bottleneck, hence something that actually scales on GPUs.

Everything mechanically difficult about the 2014 version — computing a score, normalizing with softmax, blending values — survives completely unchanged into the modern Transformer. What changed is what plays the role of query, key, and value, and the removal of the RNN scaffolding that used to surround the attention step.

## Failure mode: treating attention weights as explanations
{: #failure-mode-treating-attention-weights-as-explanations }

A specific interpretive trap that shows up constantly once people start visualizing attention weights (whether from this era's alignment matrices or a modern Transformer's attention maps): a high attention weight from position A to position B is evidence that the model is *using* information from B when computing A, but it is not automatically a full causal explanation of *why* the model produced a particular output. Multiple heads, multiple layers, residual connections carrying information around attention entirely, and the downstream MLP layers all contribute to the final output — attention weights are one legible signal among several mechanisms, not a complete window into "what the model is thinking." Papers throughout the field's history have shown cases where attention weight patterns look intuitive and human-interpretable while turning out not to be load-bearing for the actual prediction when you intervene on them directly.

The practical habit: use attention visualizations as a hypothesis-generating tool, not a proof. If you want to know whether a specific attention pattern is actually *causally* responsible for a behavior, the only reliable way to find out is to intervene — ablate that attention weight or head and measure whether the output changes — rather than trusting the visualization alone.

## Exercise
{: #exercise }

In translation, why is a single fixed-size context vector especially painful for long sentences specifically — not just "worse," but *why* worse, mechanically? Concrete check: your answer should identify that the vector's capacity (its dimensionality) doesn't grow with sentence length, so the amount of information available *per source word* shrinks as sentences get longer, while a full attention mechanism keeps one hidden state *per source position* around, so total available information scales with sentence length instead of staying fixed. Then run the numpy example above with `encoder_states` of 4 positions versus 40 positions (same hidden size) and reflect on why the attention-based approach doesn't need to change its per-position capacity at all to handle the longer sequence, while the single-vector approach fundamentally cannot avoid it.


---

[← 18. RNNs: The Old Kings and Their Pain](/courses/llm-mastery/18-rnns-and-their-pain/)  
[20. Reading 'Attention Is All You Need' Like an Engineer →](/courses/llm-mastery/20-attention-is-all-you-need-read/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
