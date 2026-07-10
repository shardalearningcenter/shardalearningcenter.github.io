---
layout: course
title: "41. Agents and Tool Use"
permalink: /courses/llm-mastery/41-agents-tool-use/
course_track: "LLM Mastery"
description: "Let the model call functions. Keep a tight loop and verify."
level: Advanced
toc:
  - id: "loop"
    label: "Loop"
  - id: "safety"
    label: "Safety"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 41/50** · Karpathy-style LLM course

Let the model call functions. Keep a tight loop and verify.

## Loop
{: #loop }

```
observe → think → act(tool) → observe → …
```

Tools: search, code exec, DB, browser. The model emits structured calls; your runtime executes.

## Safety
{: #safety }

Sandbox code. Rate-limit. Never trust free-form shell. Log everything.

## Exercise
{: #exercise }

Design 3 tools for a “repo assistant” and specify their schemas.


---

[← 40. RAG: Retrieval-Augmented Generation](/courses/llm-mastery/40-rag-retrieval/)  
[42. Hallucinations: Why They Happen →](/courses/llm-mastery/42-hallucinations/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
