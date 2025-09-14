---
layout: post
title: "How LLM works and summarizes the input"
date: 2025-09-13
---

# Description
## Today we learn how the LLM summarize the document.
-An encoder–decoder model (also called a sequence-to-sequence model) is a neural network architecture used in natural language processing (NLP) for tasks that transform one sequence into another.

-The **encoder** reads the **input sequence** (e.g., a sentence) and converts it into a rich contextual representation.

-The **decoder** takes this representation and generates the **output sequence** step by step (e.g., a translated sentence or completed text).

-This architecture powers models like T5, FLAN-T5, and BART, making them suitable for tasks such as translation, summarization, question answering, and sentence completion. Unlike GPT (decoder-only) or BERT (encoder-only), encoder–decoder models combine both reading (understanding) and writing (generating).
## Tokenizer
- Convert human input to number presentation
## Seq2Seq
- Generate take input sequence generate output sequence
# Here is code

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
