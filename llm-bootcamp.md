---
layout: page
title: LLM Bootcamp
permalink: /llm-bootcamp/
---

<style>
  .body1 {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background: #f9f9f9;
      color: #333;
      scroll-behavior: smooth;
      width: 100%;
    }
.course-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}
.course-card {
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 1rem;
  background: var(--bg-card, #fff);
  box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
  transition: transform 0.2s;
}
.course-card:hover {
  transform: translateY(-5px);
}
.course-title {
  font-weight: bold;
  font-size: 1.2rem;
  color: var(--text-heading, #000);
}
.course-desc {
  color: var(--text-body, #555);
}
section {
      padding: 60px 20px;
      max-width: 1100px;
      margin: 0 auto;
}
/* Reset + font */
body {
  margin: 0;
  font-family: Arial, sans-serif;
  line-height: 1.6;
  background-color: #f9f9f9;
  color: #333;
}

/* Consistent centered wrapper */
.page-wrapper {
  max-width: 900px;   /* keeps layout narrow for readability */
  margin: 0 auto;     /* centers horizontally */
  padding: 20px;
  background: #fff;
  min-height: 100vh;  /* ensures full screen height */
  display: flex;
  flex-direction: column;
}

/* Header, content, footer */
.site-header,
.site-footer {
  text-align: center;
  padding: 1rem;
  background: #eaeaea;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.content {
  flex: 1; /* pushes footer to bottom */
  text-align: center; /* centers text */
}

/* Responsive typography */
h1 {
  font-size: clamp(1.8rem, 4vw, 2.5rem);
}
h2 {
  font-size: clamp(1.2rem, 3vw, 1.8rem);
}
p {
  font-size: clamp(1rem, 2.5vw, 1.2rem);
}

</style>
 <div class="page-wrapper">
     <header class="site-header">
      <h1>Welcome to Sharda Learning Center</h1>
    </header>

   

<div class="course-cards">
# 🧠 LLM Boot Camp Curriculum


## 📘 Module 1: Foundations of Large Language Models
### 1. What is a Language Model?
- Evolution from N-grams to Transformers
- Why "large" matters in modern AI

### 2. Transformers 101
- Self-attention mechanism
- Positional encoding & architecture
- Mini Transformer demo in PyTorch

---

## 📘 Module 2: Pre-trained LLMs – Under the Hood
### 3. Tokenization Deep Dive
- BPE, WordPiece, SentencePiece
- Tokenizer visualization & decoding

### 4. Exploring Popular LLMs
- GPT, LLaMA, Falcon, Mistral
- Model card reading and comparison

### 5. Embeddings & Representations
- Sentence and word embeddings
- Using OpenAI or Hugging Face APIs

---

## 📘 Module 3: Prompting & Fine-Tuning
### 6. Prompt Engineering Basics
- Zero, one, few-shot prompting
- Prompt hacks & real-world examples

### 7. Fine-Tuning vs LoRA
- Why and when to fine-tune
- Fine-tune with PEFT / LoRA on Hugging Face

### 8. RLHF (Reinforcement Learning from Human Feedback)
- Overview of alignment techniques
- Human feedback simulation demo

---

## 📘 Module 4: Building with LLMs
### 9. LangChain / LlamaIndex 101
- Chains, memory, and agents
- Building Q&A apps with RAG

### 10. LLM APIs in Production
- OpenAI, Cohere, HuggingFace Inference
- Handling rate limits, logging, observability

### 11. Chatbot + RAG Project
- Ingest PDF/text
- Add memory & tool use

---

## 📘 Module 5: Advanced Topics & Deployment
### 12. LLMOps: Serving & Scaling
- FastAPI, vLLM, Hugging Face Spaces, Modal
- Deploying local models with Ollama

### 13. Security, Bias & Ethics
- Prompt injection attacks
- Jailbreaks, red-teaming & safe responses

### 14. Build a Mini Language Model
- Train from scratch on a toy dataset
- Tokenization → model → sampling loop

---

## 🎓 Capstone Projects (Pick One)
- ✅ Chatbot for documents (PDF, CSV)
- ✅ Auto-tagging for customer support
- ✅ Custom-trained LoRA chatbot
- ✅ RAG-based search engine

---

## 🚀 Bonus Chapter: Becoming an LLM Engineer
- Must-have skills & GitHub project ideas
- Resume and interview tips
- Building your AI portfolio

---

*Built for developers, students, and tech teams ready to master LLMs in record time.*
</div>
  </div>