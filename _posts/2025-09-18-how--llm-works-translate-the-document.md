---
layout: post
title: "How to translate to any language engish to hindi using local large language model for free"
date: 2025-09-18
---

# Description
## Today we learn how the LLM translate to any language for free with local Large language models.
### 1. Model: Helsinki-NLP/opus-mt-en-hi

This is a MarianMT (Marian Machine Translation) model.

It was trained on the OPUS dataset (a large collection of parallel corpora).

This particular checkpoint is English → Hindi.

The architecture is based on Transformer Seq2Seq (encoder–decoder).

### 2. Code Walkthrough
#### a. Load Tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)


Tokenizer converts human text ("I am going to school.") into tokens (numbers) that the model can understand.

Example: "I am going to school." → [1234, 567, 890, ...]

It also handles things like lowercasing, splitting into subwords (Byte Pair Encoding).

#### b. Load Model
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)


Loads the encoder-decoder translation model.

Encoder reads English tokens → creates context embeddings.

Decoder takes those embeddings and generates Hindi tokens step by step.

#### c. Prepare Input
inputs = tokenizer(text, return_tensors="pt", padding=True)


Converts text into PyTorch tensors (input_ids, attention_mask).

Example:

input_ids: [37, 14, 567, 2021, ...]

attention_mask: [1, 1, 1, 1, ...] (marks real tokens vs padding).

#### d. Generate Translation
outputs = model.generate(**inputs, max_new_tokens=50)


The generate method runs beam search / greedy decoding to predict Hindi tokens one by one.

Example:

Step 1: <s> → predicts "मैं"

Step 2: "मैं" → predicts "स्कूल"

Step 3: "स्कूल" → predicts "जा"

Step 4: "जा" → predicts "रहा हूँ।"

Continues until </s> (end-of-sequence token) is generated.

#### e. Decode Back to Text

```
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

```

Converts model’s token IDs back into human-readable Hindi text.

Output for "I am going to school." would be something like:

मैं स्कूल जा रहा हूँ।

### 3. Theory Recap

Input text → Tokenization → Encoder → Context embeddings

Decoder → Predicts Hindi tokens step by step using context + attention

Beam search / greedy decoding → Generates most likely translation

Tokenizer.decode → Converts tokens back into Hindi text
# Here is code to use LLM for language translation

```
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load model + tokenizer
model_name = "google/flan-t5-base"   # T5-base, instruction-tuned
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Example 1: Summarization
text = "summarize: The sun rises in the east and sets in the west. It is an important fact in geography."
inputs = tokenizer(text, return_tensors="pt")
outputs = model.generate(**inputs, max_length=40)
print("Summarization:", tokenizer.decode(outputs[0], skip_special_tokens=True))

```
