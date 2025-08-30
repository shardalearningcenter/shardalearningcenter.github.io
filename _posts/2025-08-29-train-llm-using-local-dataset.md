---
layout: post
title: "How to train LLM using local dataset"
date: 2029-08-29
---
# How to train LLM using local dataset

Clone the required repo for training
- git clone https://github.com/huggingface/transformers
- cd transformers
- pip install .
-    cd /mnt/d/karm/slc-bootcamp/
-    cd training-exmple/
-    cd transformers/
-    pip install .
-    python run_summarization.py
-    pip install datasets
-    python run_summarization.py
-    cd my-example/
-    pip install -r requirements.txt

## create requirements.txt
```python
transformers>=4.44.0
datasets>=2.20.0
evaluate>=0.4.2
torch>=2.3.0
accelerate>=0.33.0
sentencepiece>=0.2.0

```
## Take this code snipette to train the llm using the cnn data set
- create file run_summarization.py
```python
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments, AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq
from datasets import load_dataset

# 1. Load dataset
dataset = load_dataset("cnn_dailymail", "3.0.0")

# 2. Load tokenizer and model
# model_name = "google-t5/t5-small"
model_name="google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Preprocess function
def preprocess_function(examples):
    inputs = ["summarize: " + doc for doc in examples["article"]]
    model_inputs = tokenizer(inputs, max_length=512, truncation=True)
    labels = tokenizer(examples["highlights"], max_length=128, truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Tokenize dataset
tokenized_datasets = dataset.map(preprocess_function, batched=True, remove_columns=["article", "highlights", "id"])

# 3. Data collator
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# 4. Training arguments (LOCAL SAVE ONLY)
training_args = Seq2SeqTrainingArguments(
    output_dir="./local_t5_summarization",   # local dir
    eval_strategy="epoch",
    # evaluate_during_training=True,  # old name
    learning_rate=2e-5,
# max_steps=2000,  # overrides num_train_epochs

    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    weight_decay=0.01,
    save_total_limit=2,
    num_train_epochs=10,
    predict_with_generate=True,
    logging_dir="./logs",
    logging_steps=50,
    save_strategy="epoch",
    report_to="none"  # disables wandb/hub
)

# 5. Trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"].select(range(1000)),  # small subset for local test
    eval_dataset=tokenized_datasets["validation"].select(range(200)),
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# 6. Train
trainer.train()

# 7. Save locally
trainer.save_model("./local_t5_summarization")
tokenizer.save_pretrained("./local_t5_summarization")

print("✅ Model saved locally at ./local_t5_summarization")


```

## Use this trained model 
This model is saved at local_t5_summarization load it 

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Path where your trained model was saved
# model_path = "./local_t5_summarization/checkpoint-250"
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "./local_t5_summarization/checkpoint-250"  # your trained checkpoint
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

text = """Prime Minister Narendra Modi on Saturday (August 30, 2025) travelled to Sendai in the Japanese prefecture of Miyagi to visit a semiconductor plant. Narendra Modi on Saturday (August 30, 2025) also met governors of 16 Japanese prefectures in Tokyo and called for strengthening state-prefecture cooperation under the India-Japan Special Strategic and Global Partnership, the Ministry of External Affairs (MEA) said in a statement."""

inputs = tokenizer("summarize: " + text, return_tensors="pt", truncation=True)

summary_ids = model.generate(
    inputs["input_ids"],
    num_beams=4,
    max_length=50,
    min_length=10,
    length_penalty=2.0,
    early_stopping=True
)

print("Summary:", tokenizer.decode(summary_ids[0], skip_special_tokens=True))


```
