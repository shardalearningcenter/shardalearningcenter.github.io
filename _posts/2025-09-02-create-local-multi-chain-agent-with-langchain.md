---
layout: post
title: "How to Build a Local AI Agent With Python (Huggingface, LangChain,text summarization and translation)"
date: 2025-09-02
---

# How to Build a Local AI Agent With Python (Huggingface, LangChain,text summarization and translation)

AI agents don’t always need cloud APIs. With HuggingFace models and LangChain, you can build your own local AI agent that runs on your laptop (even with small GPUs or CPUs). In this tutorial, we’ll walk through building a simple agent in Python that can summarize text, translate text, and answer questions — all using open-source models.

## Why Build a Local AI Agent?

Most tutorials use OpenAI or Anthropic APIs, but that comes with cost and dependency. Running locally has benefits:

✅ No API costs

✅ Works offline

✅ Customizable

✅ Privacy-friendly

By combining HuggingFace pipelines with LangChain, you can create your own chain of tasks like text summarization and translation.

### Step 1: Install Dependencies

Create a requirements.txt:

```langchain
langchain>=0.2.0
langchain-huggingface
transformers
torch

```


- Then install:

pip install -r requirements.txt

# Step 2: Load a HuggingFace Model With LangChain

## Create Summarization pipeline
## Create Translate pipeline
```
# 2. Summarization pipeline
sum_pipeline = pipeline("summarization", model="google/flan-t5-base", max_new_tokens=128)
sum_llm = HuggingFacePipeline(pipeline=sum_pipeline)

# 3. Translation pipeline
trans_pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")
trans_llm = HuggingFacePipeline(pipeline=trans_pipeline)

```
We’ll use the google/flan-t5-base model because it’s lightweight and works well for summarization and translation.
```python
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain

# ----------- SETUP PIPELINES -------------
# 1. QA pipeline
qa_pipeline = pipeline("text-generation", model="google/flan-t5-base", max_new_tokens=256)
qa_llm = HuggingFacePipeline(pipeline=qa_pipeline)

# 2. Summarization pipeline
sum_pipeline = pipeline("summarization", model="google/flan-t5-base", max_new_tokens=128)
sum_llm = HuggingFacePipeline(pipeline=sum_pipeline)

# 3. Translation pipeline
trans_pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")
trans_llm = HuggingFacePipeline(pipeline=trans_pipeline)

# ----------- PROMPTS ---------------------
qa_prompt = PromptTemplate(
    input_variables=["question"],
    template="Answer this question clearly:\n{question}"
)

sum_prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize this text:\n{text}"
)

trans_prompt = PromptTemplate(
    input_variables=["text"],
    template="Translate this text to French:\n{text}"
)

# ----------- CHAINS ---------------------
# qa_chain = LLMChain(llm=qa_llm, prompt=qa_prompt)
sum_chain = LLMChain(llm=sum_llm, prompt=sum_prompt)
trans_chain = LLMChain(llm=trans_llm, prompt=trans_prompt)

# ----------- PIPE THEM TOGETHER ----------
# Example: Ask a question -> Summarize answer -> Translate summary
overall_chain = SimpleSequentialChain(
    chains=[sum_chain, trans_chain],
    verbose=True
)

# ----------- RUN -------------------------
result = (overall_chain.
          run("Goods and Services Tax (GST) is a "
                           "unified indirect tax levied in UK "
                           "on the supply of goods and services. "
                           "Businesses, freelancers, shop owners, a"
                           "nd even customers often need to calculate "
                           "GST quickly for invoices, bills, or estimates. "
                           "A Free GST Calculator helps you determine the GST amount, "
                           "net price, or gross price in just a few seconds."))
print("\nFinal Output in French:\n", result)
#Summary output
#Use a Free GST Calculator to calculate the GST amount,
# net price, or gross price of goods and services in just a few seconds.

#Translator
#Final Output in French:
# Traduire ce texte en français :
#Utilisez un calculateur gratuit de la TPS pour calculer le montant de la TPS,
#le prix net ou le prix brut des produits et services en quelques secondes seulement.
```