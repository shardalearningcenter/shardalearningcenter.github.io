---
layout: course
title: "40. RAG: Retrieval-Augmented Generation"
permalink: /courses/llm-mastery/40-rag-retrieval/
course_track: "LLM Mastery"
description: "Don’t stuff the world into weights. Fetch evidence at runtime."
level: Advanced
toc:
  - id: "pipeline"
    label: "Pipeline"
  - id: "hard-parts"
    label: "Hard parts"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 40/50** · Karpathy-style LLM course

Don’t stuff the world into weights. Fetch evidence at runtime.

## Pipeline
{: #pipeline }

1. Index docs as embeddings
2. Retrieve top-k chunks for a query
3. Stuff into context with citations
4. Generate answer grounded in chunks

## Hard parts
{: #hard-parts }

Chunking, recall vs precision, stale indexes, citation faithfulness.

## Exercise
{: #exercise }

When is RAG better than finetuning? When is it worse?


---

[← 39. Prompting as Programming](/courses/llm-mastery/39-prompting-as-programming/)  
[41. Agents and Tool Use →](/courses/llm-mastery/41-agents-tool-use/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
