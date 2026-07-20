---
layout: course
title: "42. Hallucinations: Why They Happen"
permalink: /courses/llm-mastery/42-hallucinations/
course_track: "LLM Mastery"
description: "The objective rewards fluent continuation, not truth. A confident fabrication is often the better completion, by that objective."
level: Advanced
toc:
  - id: "cause"
    label: "Cause"
  - id: "worked-example"
    label: "Worked example"
  - id: "mitigations"
    label: "Mitigations"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 42/50** · Karpathy-style LLM course

There is no "truth neuron" to turn up. A language model is trained to make the next token likely given everything before it — and a fluent, confident, entirely fabricated citation is, by that objective, often a *better* completion than an honest "I don't know," because "I don't know" rarely appears in training data as the continuation of a specific, plausible-sounding question.

## Cause
{: #cause }

Cross-entropy training pushes probability mass toward whatever token distribution matches the training corpus, conditioned on context. If the true fact isn't recoverable from the model's weights or the provided context, the model doesn't have a "null" fallback baked into the objective — it has whatever continuation looked most probable during training, and confident, specific, wrong answers are exactly the shape the training distribution rewards, because specific claims look like the specific claims that fill technical documents, papers, and Q&A pairs the model was trained on. The failure isn't "the model is broken." The failure is expecting an objective that never mentioned truth to produce it as a side effect, every time, for free.

## Worked example
{: #worked-example }

You can't read the model's mind, but you can read its next-token distribution, and a flat distribution across many plausible tokens is a real, if imperfect, signal of uncertainty. Compare two toy logit vectors over a 5-token vocabulary:

```python
import numpy as np

def entropy(logits: np.ndarray) -> float:
    p = np.exp(logits - logits.max())
    p /= p.sum()
    return float(-(p * np.log(p + 1e-12)).sum())

confident = np.array([8.0, 1.0, 0.5, 0.2, 0.1])   # one token dominates
uncertain = np.array([2.1, 2.0, 1.9, 2.2, 1.8])   # nearly uniform

print(entropy(confident))  # ~0.06 nats — model has a clear favorite
print(entropy(uncertain))  # ~1.60 nats — close to max entropy for 5 tokens (ln 5 ≈ 1.61)
```

A specific factual-recall token — a name, a date, an API signature — sampled from a low-entropy distribution is much more likely to reflect something the model actually memorized well. Sampled from a near-uniform distribution over plausible-looking alternatives, it's closer to a coin flip that happens to produce fluent text either way. Production systems use exactly this kind of signal — average token entropy, or the entropy of specific "fact-shaped" spans — to gate abstention or trigger a retrieval fallback.

## Mitigations
{: #mitigations }

Every mitigation reduces the *rate* of hallucination for a specific failure mode; none eliminates the underlying cause, because the underlying cause is the training objective itself:

- **RAG and tools** ground specific claims in retrieved evidence, but only for the claims that are actually retrieved (see article 40) — the model still fluently hallucinates about everything outside the retrieved context.
- **Calibration prompts** ("say 'I don't know' if unsure") help somewhat but ask the model to introspect on its own uncertainty using the same unreliable next-token machinery that produced the hallucination in the first place.
- **Lower temperature** reduces hallucinations that come from unlucky sampling of a low-probability tail token, but does nothing for hallucinations that come from the *mode* of the distribution being wrong — a confidently wrong answer stays confidently wrong at temperature 0.
- **Verification agents and self-consistency** — sample multiple times, check agreement — catch high-entropy hallucinations well but sail right past confidently, consistently wrong ones, since the model can be wrong the same way every time.
- **Forcing structured, checkable claims** (a citation with a specific chunk ID, a function call with a real return value) turns an unverifiable prose assertion into something a separate, deterministic check can validate or reject before it ever reaches a user — moving the burden of truth off the model's fluency and onto something you actually control.

## Exercise
{: #exercise }

Using the entropy code above, explain why *raising* temperature specifically increases hallucination risk for factual recall questions but has much less effect on hallucination risk for creative writing tasks. Then, for a customer-support bot answering questions about a specific product's return policy, propose one concrete architectural change — not a prompt change — that would catch the case where the model is asked about a policy that doesn't exist for that product at all.


---

[← 41. Agents and Tool Use](/courses/llm-mastery/41-agents-tool-use/)  
[43. Interpretability: Looking Inside →](/courses/llm-mastery/43-interpretability-basics/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
