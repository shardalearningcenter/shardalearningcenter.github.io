---
layout: course
title: "48. Build Eval-Driven: A Practical Workflow"
permalink: /courses/llm-mastery/48-building-eval-driven/
course_track: "LLM Mastery"
description: "If you can't name the number that went up, you didn't improve the system — you changed vibes, and vibes don't survive new users."
level: Advanced
toc:
  - id: "mental-model"
    label: "Mental model"
  - id: "worked-example"
    label: "Worked example"
  - id: "failure-mode"
    label: "Failure mode"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 48/50** · Karpathy-style LLM course

A change to a prompt, a model version, a retriever, or a chunking strategy is a change to your system's behavior — exactly as much as a code change — and it deserves the same discipline: a regression suite you run before and after, so "this feels better" gets replaced by a number that either went up or didn't.

## Mental model
{: #mental-model }

Never ship a change to a non-trivial LLM pipeline based on a handful of demo runs that happened to look good. A workable structure has two tiers. A small **golden set** — tens to low hundreds of cases — with deterministic, mechanically checkable pass/fail criteria: exact match, regex, schema validity, a code test that actually runs the output. And a larger **sampled set** using a weaker deterministic signal, an LLM-judge or periodic human review, to catch the broader failure modes the golden set is too narrow to see. The golden set catches regressions fast and cheaply on every change; the sampled set catches the things you didn't think to write a golden case for.

Where do golden cases come from, in practice? The best source isn't imagination — it's production traces. Every time a real user hits an edge case that broke the system, that trace becomes a golden case, permanently, the same way a bug report becomes a regression test. A team that does this consistently ends up with a golden set that's a literal history of every mistake the system has ever made in front of a real user, which is a far better curriculum than anything you'd invent sitting at a whiteboard.

## Worked example
{: #worked-example }

```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class Case:
    input: str
    check: Callable[[str], bool]
    name: str

def run_eval(cases: list[Case], pipeline: Callable[[str], str]) -> dict:
    results = []
    for case in cases:
        output = pipeline(case.input)
        passed = case.check(output)
        results.append({"name": case.name, "passed": passed, "output": output})
    pass_rate = sum(r["passed"] for r in results) / len(results)
    return {"pass_rate": pass_rate, "results": results}

cases = [
    Case("What's 15% of 200?", lambda out: "30" in out, "tip_calc_basic"),
    Case("Refund policy for order #404?", lambda out: "order not found" in out.lower(),
         "handles_missing_order"),
]

before = run_eval(cases, old_pipeline)
after  = run_eval(cases, new_pipeline)
regressions = [b["name"] for b, a in zip(before["results"], after["results"])
               if b["passed"] and not a["passed"]]
print(f"pass rate: {before['pass_rate']:.2f} -> {after['pass_rate']:.2f}")
print("regressions:", regressions)
```

The whole value of this harness is the `regressions` list, not the aggregate pass rate. A prompt change that fixes three cases and silently breaks one specific edge case, `handles_missing_order`, can leave the aggregate rate flat or even improved — you'd ship it, and only discover the regression from an angry support ticket weeks later, if this harness didn't name it explicitly.

## Failure mode
{: #failure-mode }

Building the harness is necessary, not sufficient — three ways teams still fool themselves with one in hand:

- **Prompt-engineering directly against the golden set.** If you iterate by tweaking the prompt until the same fifty cases pass, you're overfitting exactly the way a model overfits a small training set (article 9) — the prompt gets brittle-good at your golden cases and no better, sometimes worse, at the real distribution of user inputs.
- **Noisy LLM-judges create false confidence.** An LLM-judge scoring "helpfulness" on a 1–5 scale has real variance run to run and real biases, favoring longer answers, favoring its own phrasing style. Treating a judge score of 4.2 vs 4.4 as a meaningful signal without checking judge-score variance across repeated runs is trusting noise.
- **Aggregate scores hide slice-level regressions.** A pass rate that stays flat can be masking a system that got much better at easy cases and much worse at a specific, important slice — non-English queries, edge-case account states. Always break results down by category, not just one headline number.

## Exercise
{: #exercise }

Extend the `cases` list above with three new cases for a FAQ bot you care about, at least one of which is deliberately designed to fail against the *current* pipeline — a known edge case it handles badly today. Run the harness, confirm your new case fails as expected, then make the smallest pipeline change that fixes it without appearing in the `regressions` list for any of the other cases. What does it mean, in this framework, if you can't find a fix that doesn't regress something else?


---

[← 47. Safety, Security, and Prompt Injection](/courses/llm-mastery/47-safety-security/)  
[49. Research Taste: How to Read Papers →](/courses/llm-mastery/49-research-taste/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
