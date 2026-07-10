---
layout: course
title: "42. Hallucinations: Why They Happen"
permalink: /courses/llm-mastery/42-hallucinations/
course_track: "LLM Mastery"
description: "Sampling from a prior over text is not querying a database."
level: Advanced
toc:
  - id: "cause"
    label: "Cause"
  - id: "mitigations"
    label: "Mitigations"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 42/50** · Karpathy-style LLM course

Sampling from a prior over text is not querying a database.

## Cause
{: #cause }

The objective doesn’t require truth — only plausible continuation. If evidence isn’t in context/weights, fluent falsehoods appear.

## Mitigations
{: #mitigations }

RAG, tools, calibration prompts, abstention, verification agents, smaller claims.

## Exercise
{: #exercise }

Give an example where higher temperature increases hallucination risk and why.


---

[← 41. Agents and Tool Use](/courses/llm-mastery/41-agents-tool-use/)  
[43. Interpretability: Looking Inside →](/courses/llm-mastery/43-interpretability-basics/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
