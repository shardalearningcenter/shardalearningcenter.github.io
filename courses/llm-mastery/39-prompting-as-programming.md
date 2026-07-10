---
layout: course
title: "39. Prompting as Programming"
permalink: /courses/llm-mastery/39-prompting-as-programming/
course_track: "LLM Mastery"
description: "A prompt is source code for a fluent, literal interpreter with no compiler errors — only silent wrong answers."
level: Intermediate
toc:
  - id: "mental-model"
    label: "Mental model"
  - id: "worked-example"
    label: "Worked example"
  - id: "failure-modes"
    label: "Failure modes"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Intermediate · **Article 39/50** · Karpathy-style LLM course

Every prompting technique that actually works reduces to one move: turn a vague request into a spec. Treat the model like a very fast, very literal junior engineer who will do exactly what you wrote, not what you meant, and most "prompt engineering" tricks stop looking like magic and start looking like code review.

## Mental model
{: #mental-model }

Split every prompt into three roles, even when they're not visually separated: **instructions** (what to do, constraints, tone), **context** (the data to operate on — retrieved docs, conversation history, file contents), and a **format contract** (exactly what the output should look like, ideally something you can parse mechanically). Most prompt failures trace back to conflating these three: instructions buried inside a wall of context, a format described in prose instead of shown by example, constraints stated once and then silently violated three paragraphs later once the model's attention has moved on.

Chain-of-thought fits this frame too, once you stop treating it as a magic incantation. Asking the model to "think step by step" is useful precisely when the intermediate steps are things you can check — arithmetic, a chain of lookups, a plan you can inspect before it's executed. It's dead weight, and sometimes actively harmful, when there's nothing to verify and the reasoning trace is just more fluent text generated after the fact to justify whatever answer the model was already leaning toward. Ask whether you'd bother reading the reasoning trace before deciding whether to ask for one.

## Worked example
{: #worked-example }

Here's the pattern in code, not just advice. Give the model a schema-shaped contract, parse its output mechanically, and treat a parse failure as a bug to retry — the same way you'd treat a failed assertion, not as evidence the model is unusable.

```python
import json

SYSTEM = '''You are a JSON-only API. Given a support ticket, output exactly:
{"category": "billing"|"bug"|"feature_request", "urgent": true|false}
No prose. No markdown fences. JSON only.'''

def classify(ticket_text: str, llm_call, max_retries: int = 2) -> dict:
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": ticket_text},
    ]
    for attempt in range(max_retries + 1):
        raw = llm_call(messages)
        try:
            result = json.loads(raw)
            assert result["category"] in {"billing", "bug", "feature_request"}
            assert isinstance(result["urgent"], bool)
            return result
        except (json.JSONDecodeError, KeyError, AssertionError):
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user",
                "content": "That wasn't valid JSON matching the schema. Try again, JSON only."})
    raise ValueError(f"Model failed to produce valid output after {max_retries} retries")
```

Notice what's doing the work: not a clever turn of phrase, but a schema, a parser, and a retry loop that feeds the failure back as context. That's software engineering applied to a nondeterministic component — the same instinct as retrying a flaky network call, just with a more articulate flake.

## Failure modes
{: #failure-modes }

The recurring ways specs fail, roughly in order of how often they bite in production:

- **Buried requirements.** A constraint mentioned once, early, in a long system prompt gets outweighed by more recent or more repeated context — models are not immune to primacy and recency effects.
- **Conflicting instructions.** "Be concise" and "explain your reasoning step by step" fight each other; the model picks a winner you didn't choose.
- **Format described, not shown.** "Return a JSON object with fields X and Y" is worse than pasting one literal example. Show, don't just tell — models pattern-match examples far more reliably than they parse abstract descriptions.
- **Unvalidated output shipped straight through.** Any pipeline that takes model output and acts on it — writes to a database, sends an email, executes code — without the retry-and-validate loop above is one bad sample away from an incident.

## Exercise
{: #exercise }

Take this prompt: *"Summarize this article and make it good for social media."* Rewrite it as a tight spec with explicit fields for: input format, output format (with one concrete example), length constraint, tone constraint, and defined failure behavior (what the model should do if the article is too short to summarize meaningfully). Then write the Python validation function that would check your output format mechanically — if you can't write that function, your spec still isn't tight enough.


---

[← 38. Preferences: RLHF and DPO](/courses/llm-mastery/38-preference-rlhf-dpo/)  
[40. RAG: Retrieval-Augmented Generation →](/courses/llm-mastery/40-rag-retrieval/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
