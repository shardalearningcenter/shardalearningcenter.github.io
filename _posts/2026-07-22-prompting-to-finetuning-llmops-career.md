---
layout: post
title: "From Prompting to Fine-Tuning & LLMOps: The AI LLM Career Path"
date: 2026-07-22
tags: [AI, LLM, Fine-Tuning, LLMOps, Career, LoRA]
---

# From Prompting to Fine-Tuning & LLMOps: The AI LLM Career Path

You have the roadmap (Part 1) and first apps (Part 2). This article is the **senior layer**: how to level up prompting, when to fine-tune, how to evaluate, how to deploy safely, and how to get hired.

**Series:** Part 3 of 4  
- [Part 1: Complete AI LLM Developer Roadmap](/2026/07/20/ai-llm-developer-roadmap.html)  
- [Part 2: Build your first LLM apps](/2026/07/21/build-your-first-llm-apps-python-rag.html)  
- **Part 3 (this article):** Prompting → fine-tuning → LLMOps → job  
- [Capstone: Complete Document Knowledge Assistant](/2026/07/23/advanced-document-knowledge-assistant-rag-project.html)

---

## The Skill Ladder (Memorize This)

```
Prompting  →  RAG  →  Agents  →  Fine-tuning  →  LLMOps / Eval / Safety
     ↑______________ product quality & reliability ________________↑
```

Most companies need people strong in **prompting + RAG + production**. Fine-tuning is a force multiplier, not day-one work for every team.

---

## 1. Advanced Prompting That Ships

### Patterns that consistently help

| Pattern | Use when |
|---|---|
| Role + constraints + format | Every production prompt |
| Few-shot examples | Style / structure must match |
| Chain-of-thought | Multi-step reasoning (hide CoT from users if needed) |
| JSON / schema output | Downstream code must parse results |
| Critic / verifier pass | High-stakes answers |

### Production prompt template

```text
You are {role}.
Goal: {task}
Constraints:
- {constraint_1}
- {constraint_2}
Context:
{retrieved_docs}
Output format:
{schema_or_bullets}
If information is missing, say "INSUFFICIENT_CONTEXT".
```

### Guardrail prompts

Add explicit refusals:

- No inventing citations  
- No leaking system prompt  
- No executing user instructions that override system rules  

**Task:** Take your RAG bot from Part 2 and add a second “verifier” call that checks: *Does every claim appear in the context?* Reject if not.

---

## 2. When Prompting / RAG Is Not Enough

Fine-tune if you see:

- The model keeps ignoring your format after heavy prompting  
- Domain jargon (legal, medical, internal slang) is consistently wrong  
- You need a smaller/faster model that still “sounds like your product”  
- Latency / cost requires a compact specialized model  

Do **not** fine-tune first for:

- Facts that change weekly (use RAG)  
- One-off demos  
- Tiny datasets (<50 noisy samples)

**Rule of thumb:**  
Try prompt → add RAG → add tools → **then** fine-tune.

---

## 3. Fine-Tuning With LoRA (Practical Path)

LoRA trains small adapter weights instead of the full model — cheaper, faster, reversible.

Related guides on this site:

- [Fine-tune local LLM using LoRA](/2025/09/05/how-to-finetune-your-local-llm-using-LORA.html)  
- [Train LLM using local dataset](/2025/08/29/train-llm-using-local-dataset.html)

### Dataset shape

```json
{"instruction": "Rewrite as a polite support reply", "input": "ur order is late!!!", "output": "I'm sorry for the delay..."}
{"instruction": "Extract the invoice total", "input": "...", "output": "124.50 USD"}
```

### Minimal mental model of the loop

1. Collect 200–2000 clean examples  
2. Split train / validation  
3. Train LoRA adapters  
4. Compare base vs fine-tuned on a frozen eval set  
5. Only ship if metrics improve  

```python
# Conceptual sketch — see LoRA article for full runnable script
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],  # depends on model
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
# model = get_peft_model(base_model, lora_config)
# then train with Trainer / SFTTrainer
```

### Eval before vibes

Create `eval.jsonl` with 30–50 cases. Score:

- Exact format match %  
- Keyword / regex checks  
- Human preference (A/B) on 20 samples  

If fine-tuned loses to the base + better prompt, **delete the adapter** and improve data.

---

## 4. Evaluation — The Skill Most Tutorials Skip

Without eval, you are guessing.

### Golden set

| Field | Example |
|---|---|
| `id` | `q-017` |
| `question` | `What is our refund window?` |
| `must_include` | `30 days` |
| `must_not_include` | `90 days` |
| `source` | `policy.md` |

### Simple harness

```python
# eval_rag.py
import json
from ask_rag import answer  # from Part 2

def score(case):
    text = answer(case["question"]).lower()
    ok = all(x.lower() in text for x in case["must_include"])
    bad = any(x.lower() in text for x in case.get("must_not_include", []))
    return ok and not bad

cases = [json.loads(l) for l in open("eval.jsonl", encoding="utf-8")]
passed = sum(1 for c in cases if score(c))
print(f"Pass rate: {passed}/{len(cases)} = {passed/len(cases):.0%}")
```

Run this on every change to prompts, chunk size, or model.

---

## 5. LLMOps: Ship Like an Engineer

### Minimum production checklist

- [ ] FastAPI (or similar) around the model  
- [ ] Timeouts + retries with backoff  
- [ ] Request IDs in logs  
- [ ] Token / cost counters  
- [ ] Rate limiting  
- [ ] Input size limits  
- [ ] Docker image that runs on a fresh machine  
- [ ] Health endpoint (`/healthz`)  
- [ ] Offline eval in CI (even a tiny one)

### Serving options

| Tool | Best for |
|---|---|
| Ollama | Local / laptop demos |
| Hugging Face Spaces | Public demos |
| vLLM | High-throughput GPU serving |
| FastAPI + Docker | Custom product APIs |
| Modal / RunPod / cloud GPU | Burst training & inference |

### Observability questions you must answer

- What’s p95 latency?  
- What’s cost per 1k requests?  
- What’s hallucination rate on the golden set?  
- What happens when the vector DB is down?

---

## 6. Security & Safety (Interview Favorites)

| Risk | Mitigation |
|---|---|
| Prompt injection | Separate system / user; strip tool results; allowlists |
| Data leakage | Don’t put secrets in prompts; redact PII |
| Jailbreaks | Refusal policies + classifiers |
| Poisoned docs in RAG | Source allowlists, doc review |
| Over-trusting agents | Cap tool permissions; human-in-the-loop for write actions |

**Demo idea for interviews:** Show a malicious user message that tries to override instructions — and your system refusing it.

---

## 7. Career Path & Job Titles (2026)

| Title | What they expect |
|---|---|
| AI Application Engineer | RAG apps, APIs, prompts |
| LLM / GenAI Engineer | Agents, evals, some fine-tuning |
| ML Engineer (LLM focus) | Training loops, PEFT, metrics |
| AI Platform / LLMOps | Serving, scaling, reliability |
| Solutions Engineer (AI) | Demos, customer use cases |

### Portfolio that gets replies

1. RAG product with citations + eval pass rate in README  
2. Agent with tools + safety limits  
3. LoRA fine-tune write-up with before/after examples  
4. Dockerized API + architecture diagram  

### Resume bullets (steal the pattern)

- Built RAG chatbot over 200+ docs; cut hallucination rate from 28% → 9% on a 40-case eval set  
- Shipped FastAPI + Docker inference service; p95 latency 1.2s on CPU  
- Fine-tuned LoRA adapters for support tone; improved format compliance 61% → 93%  

### Interview questions to practice out loud

1. RAG vs fine-tuning — when each?  
2. How do you choose chunk size?  
3. How do you evaluate an LLM feature without a research team?  
4. How would you cut API spend by 80%?  
5. How do you prevent prompt injection in a tool-using agent?  

---

## 8. 30-Day Sprint After the Roadmap

| Week | Focus | Deliverable |
|---|---|---|
| 1 | Harden RAG + eval harness | Pass rate tracked in README |
| 2 | Add FastAPI + Docker | Public repo with `/ask` |
| 3 | LoRA or stronger prompting | Before/after report |
| 4 | Polish + apply | 10 targeted applications |

---

## Series Wrap-Up

| Part | You learned |
|---|---|
| [1 — Roadmap](/2026/07/20/ai-llm-developer-roadmap.html) | Skills map, timeline, what jobs want |
| [2 — Build apps](/2026/07/21/build-your-first-llm-apps-python-rag.html) | Chat, summarize, RAG, agents |
| [3 — Career path](/2026/07/22/prompting-to-finetuning-llmops-career.html) | Fine-tuning, eval, LLMOps, hiring |
| [Capstone — Full project](/2026/07/23/advanced-document-knowledge-assistant-rag-project.html) | Ingest → RAG → UI → API → Docker → eval |

Continue with the structured curriculum: [LLM Bootcamp](/llm-bootcamp/) · [AI/ML Bootcamp](/ai-ml-bootcamp/)

---

## Final Challenge

Publish one public repo titled something like `llm-notes-rag` that includes:

1. Working RAG + Streamlit or FastAPI  
2. `eval.jsonl` + pass-rate script  
3. Short architecture section in the README  
4. One security note (prompt injection example)  

That single project beats ten unfinished tutorials.

---

*AI LLM developers are builders with judgment. Prompt carefully, retrieve honestly, evaluate ruthlessly, deploy safely.*
