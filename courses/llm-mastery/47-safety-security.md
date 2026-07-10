---
layout: course
title: "47. Safety, Security, and Prompt Injection"
permalink: /courses/llm-mastery/47-safety-security/
course_track: "LLM Mastery"
description: "Untrusted text in the context window is a control-plane attack."
level: Advanced
toc:
  - id: "prompt-injection"
    label: "Prompt injection"
  - id: "defenses"
    label: "Defenses"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 47/50** · Karpathy-style LLM course

Untrusted text in the context window is a control-plane attack.

## Prompt injection
{: #prompt-injection }

Retrieved docs or user content says: “Ignore previous instructions…” The model might obey.

## Defenses
{: #defenses }

Separation of instructions vs data, least-privilege tools, output filters, human approvals for risky actions.

## Exercise
{: #exercise }

Write an attack string against a naive “summarize this email and send reply” agent.


---

[← 46. Diffusion vs Autoregressive: Two Generative Religions](/courses/llm-mastery/46-diffusion-vs-ar/)  
[48. Build Eval-Driven: A Practical Workflow →](/courses/llm-mastery/48-building-eval-driven/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
