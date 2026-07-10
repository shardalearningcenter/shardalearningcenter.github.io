---
layout: course
title: "38. Preferences: RLHF and DPO"
permalink: /courses/llm-mastery/38-preference-rlhf-dpo/
course_track: "LLM Mastery"
description: "When there's no single correct next token, you need feedback that ranks whole responses against each other."
level: Advanced
toc:
  - id: "rlhf-sketch"
    label: "RLHF sketch"
  - id: "dpo"
    label: "DPO"
  - id: "failure-mode"
    label: "Failure mode"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 38/50** · Karpathy-style LLM course

SFT can teach a model to answer in the right format, but it can't teach it *which of two correct-looking answers is better* — cross-entropy against a single reference answer has no way to express "this alternative would also have been fine, just slightly worse." That's the gap RLHF and DPO exist to fill: turning human (or AI) preference judgments into a training signal.

## RLHF sketch
{: #rlhf-sketch }

The three-stage machine:

1. Start from an SFT model.
2. Collect comparisons: for the same prompt, sample two responses, have a human (or a stronger model) pick the better one. Train a **reward model** to predict that preference as a scalar score, higher is better.
3. Run reinforcement learning (usually PPO) on the SFT model, using the reward model's score as the reward, with a **KL penalty** pulling the policy back toward the original SFT model so it doesn't run off and find weird high-reward text that no longer looks like language.

That KL term isn't optional decoration. A reward model is a *proxy* for what humans actually want, trained on a finite, noisy comparison set. An unconstrained RL policy will find and exploit every gap between the proxy and the real objective — repeating flattery, padding responses because the reward model likes length, whatever gets the score up. The KL penalty is a leash, not a suggestion.

## DPO
{: #dpo }

PPO is finicky: you're training a reward model, then doing on-policy RL against it, babysitting a second neural net's instabilities on top of the first. Direct Preference Optimization (DPO) notices something clever — for a common reward-modeling setup, the *optimal* RLHF policy has a closed-form relationship to the reward function. Invert that relationship and you can write a loss directly on preference pairs, no reward model and no RL loop required. Just supervised-learning-shaped optimization on `(prompt, chosen, rejected)` triples.

```python
import torch
import torch.nn.functional as F

def dpo_loss(logp_chosen, logp_rejected,
             ref_logp_chosen, ref_logp_rejected, beta=0.1):
    """All four inputs are summed log-probs of a response
    under the policy model and the frozen reference (SFT) model."""
    pi_logratio  = logp_chosen - logp_rejected
    ref_logratio = ref_logp_chosen - ref_logp_rejected
    return -F.logsigmoid(beta * (pi_logratio - ref_logratio))

# toy numbers: the policy already prefers "chosen" a bit more than the reference does
loss = dpo_loss(
    logp_chosen=torch.tensor(-12.0), logp_rejected=torch.tensor(-15.0),
    ref_logp_chosen=torch.tensor(-12.5), ref_logp_rejected=torch.tensor(-13.0),
    beta=0.1,
)
print(loss.item())  # small positive number — the two sides are already near-aligned
```

Read it as: reward the policy for increasing the *margin* by which it prefers the chosen response over the rejected one, relative to how much the reference model already preferred it. The sigmoid-and-beta shape means big margins saturate, so the policy doesn't chase infinite separation for free reward.

## Failure mode
{: #failure-mode }

Both methods can go wrong in the same family of ways, because both are still Goodhart's-Law machines: optimize a proxy hard enough and you get the proxy, not the goal.

- **Reward or length hacking.** If preference annotators (human or AI) mildly favor longer, more hedged, more "certainly, I'd be happy to help"-shaped answers, the optimized model amplifies that tic far past usefulness, because it's cheap reward.
- **Mode collapse to safe blandness.** Heavy KL-constrained optimization toward "whatever scores well on average across annotators" squeezes out legitimate stylistic diversity and confident, opinionated answers — everything regresses to the same hedged register.
- **Preference data politics.** Comparisons encode whoever labeled them: their taste, their fatigue at label #4,000 of the day, cultural assumptions about what "helpful" means. The reward model faithfully learns all of that, including the noise.

Worth noting for completeness: neither RLHF nor DPO is the only way to use preference data. Best-of-n sampling — generate several candidates at inference time, score them with a reward model, and return the winner — gets a chunk of the same benefit with zero additional training, at the cost of paying for n generations on every request instead of paying once at training time. It's a useful baseline to beat before investing in a full PPO or DPO run, if only to confirm your preference data is worth the training complexity at all.

## Exercise
{: #exercise }

Using `dpo_loss` above, compute the loss for a case where the policy has *reversed* its preference relative to the reference model: `logp_chosen=-14, logp_rejected=-10, ref_logp_chosen=-11, ref_logp_rejected=-12`. Is the loss larger or smaller than the article's example? Explain, in terms of margins, why that direction makes sense. Then explain in one sentence why `beta=0` would make this loss function useless.


---

[← 37. LoRA and Parameter-Efficient Fine-Tuning](/courses/llm-mastery/37-lora-peft/)  
[39. Prompting as Programming →](/courses/llm-mastery/39-prompting-as-programming/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
