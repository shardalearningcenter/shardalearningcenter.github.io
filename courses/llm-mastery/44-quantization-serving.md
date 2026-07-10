---
layout: course
title: "44. Quantization and Local Serving"
permalink: /courses/llm-mastery/44-quantization-serving/
course_track: "LLM Mastery"
description: "A 70B model in fp16 needs about 140GB just for weights. Quantization rounds numbers aggressively without the model noticing — until it does."
level: Advanced
toc:
  - id: "idea"
    label: "Idea"
  - id: "worked-example"
    label: "Worked example"
  - id: "failure-mode"
    label: "Failure mode"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 44/50** · Karpathy-style LLM course

Every weight in a model is a 16- or 32-bit float. Quantization stores it in 8 or 4 bits instead, which is a straightforward win for memory and often bandwidth-bound inference speed — but naive rounding destroys quality, because weight magnitudes aren't uniform. The whole field is one idea, applied carefully: find the right scale before you round.

## Idea
{: #idea }

Most weights in a given layer cluster in a narrow range; a handful of outliers are 10 to 100 times larger. Round everything with one global scale and the outliers force a coarse scale that wastes precision on the majority of small weights. The fix that actually works: compute a scale *per group* — per channel, per row, sometimes per small block of 32 to 128 values — so each group's rounding error stays small relative to its own magnitude, not the whole tensor's.

The ecosystem names (GGUF, GPTQ, AWQ, bitsandbytes) change every few months and none of them are worth memorizing as brands. What's worth internalizing is which problem each family is solving: GPTQ and AWQ mostly optimize *how* the calibration scale is chosen per group to minimize output error on a small calibration set, rather than just minimizing raw weight rounding error; GGUF is primarily a serialization format for CPU-friendly local inference. Whatever format you pick, the question to ask is the same: what granularity is the scale computed at, and was it calibrated against representative data or just against the weights in isolation?

## Worked example
{: #worked-example }

```python
import numpy as np

def quantize_int8(w: np.ndarray) -> tuple[np.ndarray, float]:
    scale = np.abs(w).max() / 127.0
    q = np.round(w / scale).clip(-127, 127).astype(np.int8)
    return q, scale

def dequantize(q: np.ndarray, scale: float) -> np.ndarray:
    return q.astype(np.float32) * scale

w = np.array([0.02, -0.05, 0.01, 4.80, 0.03, -0.02])  # one outlier at 4.80
q, scale = quantize_int8(w)
w_hat = dequantize(q, scale)

print(scale)                      # 4.80 / 127 ≈ 0.0378
print(w_hat)                      # small values collapse toward 0
print(np.abs(w - w_hat).mean())   # mean absolute error, dominated by the small weights
```

Run this and the small weights — 0.02, -0.05, 0.01, 0.03, -0.02 — all get crushed toward zero because the scale of about 0.038 is set by the one outlier at 4.80: anything smaller than half the scale rounds to zero. This single-vector example *is* the entire quantization problem in miniature. One outlier in a 4096-wide row of a real weight matrix can force the same crushing across thousands of otherwise well-behaved values, which is exactly why per-channel — not per-tensor — scales, and outlier-aware methods that smooth outlier magnitude into activations before quantizing, are the difference between a quantized model that works and one that quietly gets worse at everything involving small, precise adjustments.

## Failure mode
{: #failure-mode }

Quantization quality loss is never evenly spread across capabilities, which is what makes it dangerous to evaluate with a single aggregate metric:

- **Outlier-heavy layers degrade more.** Certain layers, often specific attention projections, have systematically larger outliers than others; per-tensor quantization schemes hurt exactly those layers disproportionately.
- **Precision-sensitive tasks degrade first.** Arithmetic, multi-step reasoning chains, and long-tail factual recall tend to need finer distinctions between similar-but-different weight values than casual conversational fluency does — a model that "seems fine" in chat can be measurably worse at math after quantization while perplexity barely moves.
- **KV-cache quantization compounds over length.** If you quantize the KV cache — common for long-context serving to save memory — rather than just the weights, small per-token errors accumulate across a long generation, and quality can degrade specifically as sequences get longer, a bug that's invisible in short-prompt evals and shows up only in production.

## Exercise
{: #exercise }

Using `quantize_int8` above, quantize the vector `[0.01, 0.02, -0.01, 12.0, 0.015]` and compute the mean absolute dequantization error. Then quantize just the first four values, excluding the outlier at 12.0, separately, and compute that group's mean absolute error. By what factor did excluding the outlier from the scale computation reduce the error on the small values? That factor is, roughly, the argument for per-channel over per-tensor quantization.


---

[← 43. Interpretability: Looking Inside](/courses/llm-mastery/43-interpretability-basics/)  
[45. Multimodal LLMs: Vision Enters the Context →](/courses/llm-mastery/45-multimodal-llms/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
