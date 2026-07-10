---
layout: course
title: "40. RAG: Retrieval-Augmented Generation"
permalink: /courses/llm-mastery/40-rag-retrieval/
course_track: "LLM Mastery"
description: "Weights are a stale, lossy compression of the internet. RAG bolts on a live, editable memory the model has to read at inference time."
level: Advanced
toc:
  - id: "mental-model"
    label: "Mental model"
  - id: "worked-example"
    label: "Worked example"
  - id: "hard-parts"
    label: "Hard parts"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 40/50** · Karpathy-style LLM course

Retrieval-Augmented Generation has one job: get the right few paragraphs in front of the model before it has to answer. Everything else — the vector database, the fancy re-ranker, the embedding-model leaderboard — is in service of that one job, and if it fails, no amount of generation quality downstream saves you.

## Mental model
{: #mental-model }

Think of the pipeline as a strict information bottleneck: `documents → retriever → top-k chunks → context window → model`. The model can only reason over what made it through that bottleneck. A more capable model cannot recover information that retrieval failed to surface — it can only produce a more fluent-sounding wrong answer, or, if you're lucky and it's well-calibrated, say it doesn't know. Debugging a bad RAG answer should *always* start by checking what actually got retrieved, before you touch the prompt or swap the generation model. Most "hallucination" complaints about RAG systems are retrieval failures wearing a generation-failure costume.

## Worked example
{: #worked-example }

Strip away the vector database and a RAG retriever is just: embed everything, then rank by similarity.

```python
import numpy as np

def embed(text: str) -> np.ndarray:
    # stand-in for a real embedding model call
    ...

def retrieve(query: str, chunks: list[str], k: int = 3) -> list[str]:
    q = embed(query)
    q = q / np.linalg.norm(q)
    scored = []
    for chunk in chunks:
        c = embed(chunk)
        c = c / np.linalg.norm(c)
        scored.append((float(q @ c), chunk))   # cosine similarity
    scored.sort(reverse=True)
    return [chunk for _, chunk in scored[:k]]

def answer(query: str, chunks: list[str], llm_call) -> str:
    top = retrieve(query, chunks)
    context = "\n---\n".join(f"[{i}] {c}" for i, c in enumerate(top))
    prompt = (
        f"Context:\n{context}\n\nQuestion: {query}\n"
        "Answer using only the context above. Cite chunk numbers. "
        "If the context doesn't contain the answer, say so."
    )
    return llm_call(prompt)
```

Every production RAG system is this function with more knobs: hybrid sparse+dense retrieval, re-ranking the top-k with a cross-encoder, query rewriting, metadata filters. But if this simple version returns the wrong chunks, none of those knobs matter yet.

## Hard parts
{: #hard-parts }

Three failure sources dominate in practice:

- **Chunking cuts sentences that matter in half.** A 512-token fixed-size chunker will happily split "the deadline is [CHUNK BOUNDARY] March 15th" across two chunks, and neither chunk alone answers the question. Overlapping windows and semantic, section-aware chunking mitigate this; nothing eliminates it entirely.
- **Lost in the middle.** Even with the right chunks retrieved, models attend unevenly across a long context — information at the very start or end is used more reliably than information buried in the middle. Stuffing in twenty "just in case" chunks instead of the best three often *hurts* accuracy, not helps it.
- **Confident wrong retrieval.** The retriever will sometimes return a chunk that's topically similar but factually about a different case, version, or time period — and the model will cite it fluently and confidently as if it were correct. This is arguably the most dangerous failure mode because it looks exactly like a well-grounded answer.
- **Embedding-model domain mismatch.** An embedding model trained mostly on general web text will place a legal contract clause and a casual blog sentence about the same topic surprisingly close together, and surprisingly far from a semantically identical clause phrased in denser legal language. If your domain has specialized vocabulary — legal, medical, your own internal codebase — the off-the-shelf embedding model's notion of "similar" may not match your notion of "relevant," and no amount of prompt tuning downstream fixes a retriever that's ranking the wrong things as close.

## Exercise
{: #exercise }

You have three chunks with cosine similarities to a query of 0.81, 0.79, and 0.42. The top two are near-duplicate paragraphs from two different, contradictory versions of a policy document — one from 2023, one from 2025 — and no date metadata was indexed. Design a concrete fix at the *indexing* stage (not the prompt stage) that would prevent this specific failure, and explain why fixing it at generation time, e.g. asking the model to "pick the most recent one," is a worse solution.


---

[← 39. Prompting as Programming](/courses/llm-mastery/39-prompting-as-programming/)  
[41. Agents and Tool Use →](/courses/llm-mastery/41-agents-tool-use/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
