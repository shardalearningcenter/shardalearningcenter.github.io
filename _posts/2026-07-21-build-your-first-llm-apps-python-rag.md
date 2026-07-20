---
layout: post
title: "Build Your First LLM Apps with Python: Chat, Summarize, RAG & Agents"
date: 2026-07-21
tags: [AI, LLM, Python, RAG, LangChain, Projects]
---

# Build Your First LLM Apps with Python: Chat, Summarize, RAG & Agents

This is the **hands-on** companion to the roadmap. You will build four small but real LLM apps you can put on GitHub.

**Series:** Part 2 of 4  
- [Part 1: Complete AI LLM Developer Roadmap](/2026/07/20/ai-llm-developer-roadmap.html)  
- **Part 2 (this article):** Build chat, summarize, RAG, agents  
- [Part 3: Prompting → fine-tuning → LLMOps](/2026/07/22/prompting-to-finetuning-llmops-career.html)  
- [Capstone: Complete Document Knowledge Assistant](/2026/07/23/advanced-document-knowledge-assistant-rag-project.html)

---

## What You'll Build

| # | App | Skills unlocked |
|---|---|---|
| 1 | Chat wrapper CLI | API / local model calls |
| 2 | Document summarizer | Prompt design + chunking |
| 3 | Notes RAG bot | Embeddings + retrieval |
| 4 | Mini tool agent | Function calling / tools |

**Time:** ~1 weekend per app if you already know basic Python.

---

## Setup (Do This Once)

```bash
mkdir llm-first-apps
cd llm-first-apps
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install transformers sentencepiece torch \
  sentence-transformers chromadb fastapi uvicorn \
  streamlit pypdf
```

**Two paths:**

- **Local / free:** Hugging Face models + Ollama (no paid key)  
- **Hosted:** OpenAI / Groq / Gemini when you want stronger quality  

This article leans **local-first** so anyone can follow.

---

## App 1 — Chat Wrapper CLI

### Goal

A tiny CLI that sends a user message to a local instruction model and prints the reply.

```python
# chat_cli.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)

def chat(user_text: str, max_new_tokens: int = 64) -> str:
    prompt = f"Answer clearly and briefly: {user_text}"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    while True:
        q = input("You: ").strip()
        if q.lower() in {"exit", "quit"}:
            break
        print("Bot:", chat(q))
```

### Task

1. Add a `--system` flag that prepends a custom personality  
2. Log every Q&A to `chat_log.jsonl`  
3. Swap `flan-t5-small` for a stronger local model via Ollama when ready  

---

## App 2 — Document Summarizer

### Goal

Summarize long text without blowing the context window — by **chunking**.

```python
# summarize.py
from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
)

def chunk_text(text: str, max_chars: int = 1500):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks

def summarize_long(text: str) -> str:
    parts = []
    for i, chunk in enumerate(chunk_text(text), 1):
        out = summarizer(chunk, max_length=120, min_length=30, do_sample=False)
        parts.append(out[0]["summary_text"])
        print(f"Chunk {i} done")
    # second pass: summarize the summaries
    joined = " ".join(parts)
    final = summarizer(joined, max_length=160, min_length=40, do_sample=False)
    return final[0]["summary_text"]

if __name__ == "__main__":
    with open("article.txt", "r", encoding="utf-8") as f:
        text = f.read()
    print(summarize_long(text))
```

Related reading: [How LLM works and summarizes input](/2025/09/13/how--llm-works-summarizes-the-document.html)

### Task

- Accept a PDF path with `pypdf`  
- Print word count before / after  
- Save summary to `summary.md`

---

## App 3 — Notes RAG Bot (The Job Skill)

### Goal

Ask questions over your own Markdown notes and get answers grounded in retrieved chunks.

### Step A — Index notes

```python
# build_index.py
from pathlib import Path
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

NOTES_DIR = Path("notes")
DB_DIR = "chroma_notes"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

embedder = SentenceTransformer(EMBED_MODEL)
client = PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection("notes")

def chunk(text: str, size: int = 500, overlap: int = 50):
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i : i + size])
        i += size - overlap
    return chunks

docs, ids, metas = [], [], []
idx = 0
for path in NOTES_DIR.glob("**/*.md"):
    text = path.read_text(encoding="utf-8")
    for c in chunk(text):
        docs.append(c)
        ids.append(f"doc-{idx}")
        metas.append({"source": str(path)})
        idx += 1

embeddings = embedder.encode(docs).tolist()
collection.add(documents=docs, embeddings=embeddings, ids=ids, metadatas=metas)
print(f"Indexed {len(docs)} chunks from {NOTES_DIR}")
```

### Step B — Ask questions

```python
# ask_rag.py
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

DB_DIR = "chroma_notes"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GEN_MODEL = "google/flan-t5-base"

embedder = SentenceTransformer(EMBED_MODEL)
client = PersistentClient(path=DB_DIR)
collection = client.get_collection("notes")

tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(GEN_MODEL)

def retrieve(query: str, k: int = 3):
    q_emb = embedder.encode([query]).tolist()
    res = collection.query(query_embeddings=q_emb, n_results=k)
    return res["documents"][0], res["metadatas"][0]

def answer(query: str) -> str:
    docs, metas = retrieve(query)
    context = "\n\n".join(docs)
    prompt = (
        "Answer using ONLY the context. If unknown, say 'I don't know'.\n\n"
        f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    )
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    out = model.generate(**inputs, max_new_tokens=128)
    text = tokenizer.decode(out[0], skip_special_tokens=True)
    sources = ", ".join(sorted({m["source"] for m in metas}))
    return f"{text}\n\nSources: {sources}"

if __name__ == "__main__":
    q = input("Question: ")
    print(answer(q))
```

### Why this matters

Interviewers love RAG because it shows you understand **grounding**, **retrieval**, and **hallucination control** — not just calling ChatGPT.

### Task

1. Put 5+ Markdown notes in `notes/`  
2. Index them  
3. Ask 10 questions; mark answers as correct / wrong / “I don’t know”  
4. Add Streamlit UI with a text box + answer panel  

---

## App 4 — Mini Tool Agent

### Goal

Let the model call tools (calculator + notes search) instead of guessing.

```python
# mini_agent.py
import re
from ask_rag import answer as rag_answer  # reuse App 3

def calculator(expr: str) -> str:
    # intentionally tiny & safe
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expr):
        return "Invalid expression"
    try:
        return str(eval(expr, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"

TOOLS = {
    "calculator": calculator,
    "notes_search": rag_answer,
}

SYSTEM = """You are a helpful agent.
If you need a tool, reply EXACTLY in this format:
TOOL: <name>
INPUT: <input>
Otherwise answer the user normally.
Available tools: calculator, notes_search
"""

def parse_tool_call(text: str):
    m = re.search(r"TOOL:\s*(\w+)\s*INPUT:\s*(.+)", text, re.S)
    if not m:
        return None
    return m.group(1).strip(), m.group(2).strip()

def run_agent(user: str, llm_fn):
    # llm_fn is your chat() from App 1 or an API call
    draft = llm_fn(SYSTEM + "\nUser: " + user)
    parsed = parse_tool_call(draft)
    if not parsed:
        return draft
    name, tool_input = parsed
    if name not in TOOLS:
        return f"Unknown tool: {name}"
    tool_result = TOOLS[name](tool_input)
    final = llm_fn(
        SYSTEM
        + f"\nUser: {user}\nTool {name} returned: {tool_result}\n"
        + "Give the final answer to the user."
    )
    return final
```

### Task

- Add a third tool: `get_time` returning local time  
- Limit the agent to **one** tool call (no infinite loops)  
- Log every tool call for debugging  

Related: [Local multi-chain agent with LangChain](/2025/09/02/create-local-multi-chain-agent-with-langchain.html)

---

## FastAPI Wrapper (Bonus — Looks Senior)

Expose App 3 as an HTTP API:

```python
# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from ask_rag import answer

app = FastAPI(title="Notes RAG API")

class AskRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(req: AskRequest):
    return {"answer": answer(req.question)}
```

Run:

```bash
uvicorn api:app --reload
```

Test with:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is RAG?\"}"
```

---

## Portfolio Checklist

Before you move to Part 3, your GitHub repo should include:

- [ ] `README.md` with screenshots / sample Q&A  
- [ ] `requirements.txt`  
- [ ] Sample `notes/` folder  
- [ ] One eval file: 10 questions + expected keywords  
- [ ] Short Loom / GIF demo (optional but powerful)

---

## Common Bugs (And Fixes)

| Problem | Fix |
|---|---|
| Model downloads forever | Use smaller models first (`flan-t5-small`) |
| RAG answers ignore docs | Lower temperature; strengthen “use ONLY context” |
| Empty retrieval | Check chunk size; verify index actually ran |
| CUDA / torch errors on Windows | Start with CPU; upgrade later |
| Agent loops forever | Cap steps at 1–3 |

---

## What’s Next

Part 3 covers the career ladder after first apps: advanced prompting, LoRA fine-tuning, evaluation, security, and LLMOps so you can interview with confidence.

→ [Part 3: From Prompting to Fine-Tuning & LLMOps](/2026/07/22/prompting-to-finetuning-llmops-career.html)

Curriculum hub: [LLM Bootcamp](/llm-bootcamp/)

---

*Ship apps. Measure quality. Repeat. That is how LLM developers actually grow.*
