---
layout: course
title: "46. Diffusion vs Autoregressive: Two Generative Religions"
permalink: /courses/llm-mastery/46-diffusion-vs-ar/
course_track: "LLM Mastery"
description: "AR writes one token at a time and never looks back. Diffusion writes badly, all at once, then iteratively makes it less bad."
level: Advanced
toc:
  - id: "autoregressive"
    label: "Autoregressive"
  - id: "diffusion"
    label: "Diffusion"
  - id: "convergence"
    label: "Convergence"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 46/50** · Karpathy-style LLM course

Autoregressive models and diffusion models are both, at bottom, ways of factorizing a probability distribution so you can sample from it one manageable piece at a time. They just made different bets about which axis to chop the problem along, and those bets explain almost everything about where each one dominates.

## Autoregressive
{: #autoregressive }

You already know this factorization from article 3: `p(x) = p(x1) · p(x2|x1) · p(x3|x1,x2) · …`. Generate left to right, one token locked in per step, each future token conditioned on everything already committed. It's a natural fit for text because text already has an inherent left-to-right structure in most languages, and it makes training embarrassingly parallel via teacher forcing even though *sampling* is inherently sequential — you can't compute token 50 without having already sampled token 49.

## Diffusion
{: #diffusion }

Diffusion factorizes generation completely differently: instead of a left-to-right chain over tokens, it's a chain over *noise levels*. Training teaches a model to reverse a fixed, known process that gradually corrupts real data into pure noise — learn to predict what this looked like one noise-step ago, and chain that prediction backward from pure noise to a full sample.

```python
import numpy as np

def forward_noise_step(x: np.ndarray, noise_scale: float, rng) -> np.ndarray:
    """One step of the fixed forward process: corrupt x a little more."""
    return x + noise_scale * rng.standard_normal(x.shape)

def reverse_denoise_step(x_noisy: np.ndarray, predicted_noise: np.ndarray,
                          noise_scale: float) -> np.ndarray:
    """One step of the learned reverse process: undo a little of the noise."""
    return x_noisy - noise_scale * predicted_noise

# toy 1D "image": a single value, corrupted over 4 steps then denoised back
rng = np.random.default_rng(0)
x = np.array([1.0])
for _ in range(4):
    x = forward_noise_step(x, 0.3, rng)   # forward process: fixed, no learning involved
# a trained model would now predict the noise at each step and reverse it:
# x = reverse_denoise_step(x, model_predicts_noise(x, step), 0.3)  # repeated 4 times
```

Crucially, nothing here has an inherent left-to-right order over the *data* — every pixel, or in a discrete-text analogue every token position, gets denoised together, in parallel, at every step. The sequential part is over noise levels, typically tens to thousands of them, not over positions in the data. That's what makes it a great fit for continuous, spatially unstructured-by-order data like images, where there's no natural "first pixel," and a much less obvious fit for text.

This also changes what "sampling speed" trades off against. An AR model's quality-vs-speed knob is mostly about model size and KV-cache tricks (article 28) — the number of forward passes is fixed by the output length. A diffusion model's knob is the number of denoising steps itself: fewer steps means faster but blurrier or less coherent samples, more steps means slower but sharper ones, and a large fraction of diffusion research (distillation, consistency models, fewer-step samplers) is specifically about pushing that step count down without giving back the quality it buys.

## Convergence
{: #convergence }

Research pushes on both boundaries — discrete diffusion models for text, and autoregressive-flavored generation for images and video that predicts patches or scales in sequence — but as of now, the practical default split holds because of a real structural mismatch, not just habit. Diffusion was built for continuous data where "add a little Gaussian noise" is a natural corruption; text is discrete tokens, where there's no obviously "small" corruption between "the" and "cat" the way there is between pixel value 128 and 130. Discrete diffusion approaches exist — masking tokens and learning to unmask, or working in continuous embedding space and rounding at the end — but they're an active research area, not the default recipe, precisely because that continuous-noise intuition doesn't transfer cleanly.

## Exercise
{: #exercise }

An autoregressive model generates a 100-token response with one forward pass per token — 100 forward passes, ignoring KV-cache reuse of past computation. A diffusion model generates an equivalent-length output using 50 denoising steps, each of which is one forward pass over the *entire* sequence at once. Which one does more total floating-point work per response, and which one can start returning partial results to a user sooner? Then explain, in one paragraph, why AR's "never look back" property is both its biggest weakness — exposure bias, where an early mistake can't be un-committed — and diffusion's core design advantage, where every step gets a chance to revise the whole thing.


---

[← 45. Multimodal LLMs: Vision Enters the Context](/courses/llm-mastery/45-multimodal-llms/)  
[47. Safety, Security, and Prompt Injection →](/courses/llm-mastery/47-safety-security/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
