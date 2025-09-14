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

   

<!-- <div class="course-cards"> -->

<h1># 🧠 LLM Boot Camp Curriculum</h1>


<h2>## 📘 Module 1: Foundations of Large Language Models</h2>

<h3>### 1. What is a Language Model?</h3>
- Evolution from N-grams to Transformers
- Why "large" matters in modern AI

<h3>### 2. Transformers 101</h3>
- Self-attention mechanism
- Positional encoding & architecture
- Mini Transformer demo in PyTorch

---

<h2>## 📘 Module 2: Pre-trained LLMs – Under the Hood</h2>
<h3>### 3. Tokenization Deep Dive</h3>
- BPE, WordPiece, SentencePiece
- Tokenizer visualization & decoding

<h3>### 4. Exploring Popular LLMs</h3>
- GPT, LLaMA, Falcon, Mistral
- Model card reading and comparison

<h3>### 5. Embeddings & Representations</h3>
- Sentence and word embeddings
- Using OpenAI or Hugging Face APIs

---

<h2>## 📘 Module 3: Prompting & Fine-Tuning</h2>
<h3>### 6. Prompt Engineering Basics</h3>
- Zero, one, few-shot prompting
- Prompt hacks & real-world examples

<h3>### 7. Fine-Tuning vs LoRA</h3>
- Why and when to fine-tune
- Fine-tune with PEFT / LoRA on Hugging Face

<h3>### 8. RLHF (Reinforcement Learning from Human Feedback)</h3>
- Overview of alignment techniques
- Human feedback simulation demo

---

<h2>## 📘 Module 4: Building with LLMs</h2>
<h3>### 9. LangChain / LlamaIndex 101</h3>
- Chains, memory, and agents
- Building Q&A apps with RAG

<h3>### 10. LLM APIs in Production</h3>
- OpenAI, Cohere, HuggingFace Inference
- Handling rate limits, logging, observability

<h3>### 11. Chatbot + RAG Project</h3>
- Ingest PDF/text
- Add memory & tool use

---

<h2>## 📘 Module 5: Advanced Topics & Deployment</h2>
<h3>### 12. LLMOps: Serving & Scaling</h3>
- FastAPI, vLLM, Hugging Face Spaces, Modal
- Deploying local models with Ollama

<h3>### 13. Security, Bias & Ethics</h3>
- Prompt injection attacks
- Jailbreaks, red-teaming & safe responses

<h3>### 14. Build a Mini Language Model</h3>
- Train from scratch on a toy dataset
- Tokenization → model → sampling loop

---

<h2>## 🎓 Capstone Projects (Pick One)</h2>
- ✅ Chatbot for documents (PDF, CSV)
- ✅ Auto-tagging for customer support
- ✅ Custom-trained LoRA chatbot
- ✅ RAG-based search engine

---

<h2>## 🚀 Bonus Chapter: Becoming an LLM Engineer</h2>
- Must-have skills & GitHub project ideas
- Resume and interview tips
- Building your AI portfolio

---

*Built for developers, students, and tech teams ready to master LLMs in record time.*

</div>
  </div>