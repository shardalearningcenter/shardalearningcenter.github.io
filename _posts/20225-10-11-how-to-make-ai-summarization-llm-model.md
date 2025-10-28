---
layout: post
title: "How to train ai summarization llm model using your dataset"
date: 2025-09-13
---
# 1️⃣ Tokenizer and Model Loading
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")


## Theory:

AutoTokenizer loads the pre-trained tokenizer for the model.

The tokenizer converts text → tokens → IDs that the model can understand.

It also handles special tokens, padding, truncation, and vocabulary mapping.

AutoModelForSeq2SeqLM loads a pre-trained sequence-to-sequence model (here BART).

## Seq2SeqLM = Sequence-to-Sequence Language Model, ideal for tasks like summarization or translation.

BART has an encoder-decoder architecture:

Encoder: reads input text

Decoder: generates output text (summary)

# 2️⃣ Tokenization Function

```
def tokenize_function(example):
    return tokenizer(
        example["prompt"],
        text_target=example["completion"],
        truncation=True,
        max_length=512
    )
```

## Theory:

- example["prompt"]: the input text (article)

- text_target=example["completion"]: the target text (summary)

- truncation=True: cuts off sequences longer than max_length

- max_length=512: ensures sequences fit the model’s positional embeddings

## Why?

Transformers require fixed-length input IDs for batching.

Tokenization converts text → integer IDs → tensors → fed to the model.

# 3️⃣ Mapping Tokenizer to Dataset
tokenized = formatted_dataset.map(tokenize_function, batched=True)


## Theory:

- .map() applies tokenize_function to every example in formatted_dataset.

- batched=True → processes a batch of examples at a time (faster).

- Result: tokenized now has input IDs and labels, ready for training.

# 4️⃣ Data Collator and Seq2SeqModel

- Batch Before Collator:

[ I am happy ]

[ We love Python coding ]

- Batch After Collator:

[ I am happy PAD PAD ]

[ We love Python coding ]

- Attention Mask:

[ 1 1 1 0 0 ]

[ 1 1 1 1 1 ]

- Labels Padded:

[ Summary1 PAD PAD ]

[ Summary2 PAD PAD ]

## What is attention mask

An attention mask is like a highlighter for the model:

1 (or True) → pay attention to this token

0 (or False) → ignore this token (usually padding)

### Transformers look at all tokens at once.
### Without an attention mask, the model might treat PAD tokens as real words, which would confuse it.

#### Example

Say you have these sentences:

Sentence	Tokens	Padded Tokens
"I am happy"	[I, am, happy]	[I, am, happy, PAD, PAD]

#### Attention mask:

[1, 1, 1, 0, 0]


The model attends only to real tokens: I, am, happy

Ignores **PAD tokens**  when computing self-attention and loss

```
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

def tokenize_function(example):
    return tokenizer(
        example["prompt"],
        text_target=example["completion"],
        truncation=True,
        max_length=512
    )

tokenized = formatted_dataset.map(tokenize_function, batched=True)
data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

```

## Theory:

Handles dynamic padding for batches:

Sequences in a batch can have different lengths.

Collator pads shorter sequences to match the longest in the batch.

For Seq2Seq tasks:

Pads both input sequences and target labels

Ensures proper batching without shape mismatch errors.

# 5️⃣ Training Arguments
args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=2,
    num_train_epochs=1,
    logging_steps=10,
)


## Theory:

output_dir: where the model checkpoints will be saved

per_device_train_batch_size: number of examples per GPU/CPU per step

num_train_epochs: number of passes over the training dataset

logging_steps: frequency of logging metrics

## Why important?

Manages training hyperparameters and checkpointing.

Small batch size recommended for CPU; GPU can handle larger batches.

# 6️⃣ Trainer

```
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized,
    data_collator=data_collator,
)

```


## Theory:

Trainer is Hugging Face’s high-level training API

### Handles:

- Forward pass + loss computation

- Backpropagation + optimizer steps

- Logging, checkpointing, evaluation

### Inputs:

- model: your seq2seq model

- args: training hyperparameters

- train_dataset: tokenized dataset

- data_collator: manages batching & padding

## Result:

Once you call trainer.train(), it fine-tunes your BART model on the dataset.

# ✅ Key Theory Points

- Tokenizer = text → IDs

- Seq2Seq model = encoder-decoder architecture for text generation tasks

- Tokenization + map() prepares dataset in the model-friendly format

- DataCollator handles dynamic padding → avoids tensor shape errors

- Trainer abstracts all training loops, batching, and optimizer steps