---
layout: course
title: "45. Multimodal LLMs: Vision Enters the Context"
permalink: /courses/llm-mastery/45-multimodal-llms/
course_track: "LLM Mastery"
description: "An image, once patchified and projected, is an unusually expensive sentence sharing the same residual stream as your text tokens."
level: Advanced
toc:
  - id: "pattern"
    label: "Pattern"
  - id: "worked-example"
    label: "Worked example"
  - id: "failure-mode"
    label: "Failure mode"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 45/50** · Karpathy-style LLM course

There is no separate "vision brain" bolted onto a language model. The dominant recipe for multimodal LLMs is aggressively simple: chop the image into patches, project each patch into the same vector space the text embeddings live in, and hand the whole mixed sequence to the exact same transformer that was already trained to predict the next token. Vision doesn't get a new architecture. It gets a translator.

## Pattern
{: #pattern }

The recipe, concretely:

1. A vision encoder, commonly a ViT, splits the image into fixed-size patches — say 14×14 pixels — and produces one embedding per patch.
2. A small projector, often just an MLP, maps each patch embedding from the vision encoder's dimension into the language model's `d_model`.
3. Those projected "visual tokens" get spliced into the input sequence — typically prepended or interleaved with text tokens — and the rest of the transformer proceeds exactly as it would for text: same attention, same residual stream, same next-token training objective, now predicting text conditioned on both prior text *and* visual tokens.

Training aligns the two modalities by brute force: show the model enough `(image, caption)` and `(image, instruction, answer)` pairs, and the projector learns to place visual tokens wherever in `d_model`-space makes the language model's existing circuitry interpret them usefully — the same next-token cross-entropy loss from article 5, just with a richer input sequence.

The language model backbone typically doesn't even need to know it's looking at an image. From inside the transformer, a visual token and a text token are the same shape of thing: a vector in the residual stream that attention can query and mix with every other vector, regardless of which encoder produced it. That's the entire elegance of the approach, and also why it inherits every scaling cost text tokens have (context length, KV-cache memory) multiplied by however many hundreds of tokens one image happens to cost.

## Worked example
{: #worked-example }

```python
def num_visual_tokens(image_size: int, patch_size: int) -> int:
    patches_per_side = image_size // patch_size
    return patches_per_side ** 2

# a 224x224 image, 14x14 patches (a common ViT config)
print(num_visual_tokens(224, 14))   # 16 * 16 = 256 tokens

# a 1024x1024 image at the same patch size
print(num_visual_tokens(1024, 14))  # 73 * 73 = 5329 tokens
```

That second number is why high-resolution image support is a real systems problem, not just a quality knob: a single high-res image can cost more context budget than several pages of text. Production multimodal systems spend real engineering effort reducing this — tiling with a shared low-res "thumbnail" token, patch-merging or pooling layers, resolution-adaptive encoders — because "just increase resolution" directly fights the context-window and KV-cache costs from articles 28 and 44.

## Failure mode
{: #failure-mode }

Two failure modes come directly from the patchify-and-project design, not from a generic "the model is dumb" story:

- **Dense text inside images gets garbled.** A photo of a dense spreadsheet or a screenshot of small code gets patchified at a fixed resolution that often can't preserve individual character shapes — the model gets a blurry gist, not the exact characters, and confidently fills in the gaps with plausible-looking, and often wrong, text. This is precisely why production systems still route document-heavy inputs through dedicated OCR before, or alongside, the vision-LLM path: OCR is a specialized, much higher-fidelity way to extract the one thing patchified vision tokens are bad at preserving.
- **Hallucinated visual detail from caption priors.** Because the model was trained on `(image, caption)` pairs where captions follow predictable patterns — "a photo of a [object] on a [surface]" — it can generate plausible details that fit the pattern but aren't actually in the pixels: a shadow, a background object, or a count of items that isn't there, because that's what a caption at this point usually says, and the visual tokens' influence isn't strong enough to override it for underspecified regions of the image.

## Exercise
{: #exercise }

A vision-LLM uses 14×14 patches and processes images at 336×336 resolution. Compute the number of visual tokens per image. If your text prompt budget is 8,000 tokens and each image costs the amount you just computed, how many images can you include before visual tokens alone exceed half your context budget? Then propose one concrete design change — not "use a bigger context window" — that would let you include twice as many images at the same token budget, and name the quality trade-off it makes.


---

[← 44. Quantization and Local Serving](/courses/llm-mastery/44-quantization-serving/)  
[46. Diffusion vs Autoregressive: Two Generative Religions →](/courses/llm-mastery/46-diffusion-vs-ar/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
