---
layout: course
title: "41. Agents and Tool Use"
permalink: /courses/llm-mastery/41-agents-tool-use/
course_track: "LLM Mastery"
description: "An agent is a language model in a while loop with permission to act. The loop is simple; the permissions are where it gets dangerous."
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

> **Level:** Advanced · **Article 41/50** · Karpathy-style LLM course

Strip away the branding and an "agent" is a for-loop: the model produces a structured action, your code executes it, the result goes back into context, repeat until the model says it's done. The interesting engineering isn't the loop — it's everything that stops the loop from doing something you'll regret.

## Mental model
{: #mental-model }

The canonical shape (ReAct and its many descendants):

```
loop:
  model sees: system prompt + tool schemas + conversation + prior observations
  model emits: either a final answer, or a structured tool call {name, arguments}
  if tool call: runtime validates arguments against schema, executes, appends result as an "observation"
  else: return final answer
```

The load-bearing design decision is that tool calls are **structured** — JSON matching a schema — not free-form natural language that you then try to parse. Treat the tool interface exactly like an API contract, because that's what it is. The model is a caller you don't fully control, which means your schema validation is not a nice-to-have; it's the boundary between "the model asked for something" and "the model did something."

Design tools around idempotency wherever you can — a `create_ticket` call the model retries after a timeout should not silently create two tickets. Traditional distributed-systems engineering already solved this class of problem (idempotency keys, at-least-once delivery with dedup); agent loops inherit exactly the same retry-and-partial-failure hazards, just with a less predictable caller deciding when to retry.

## Worked example
{: #worked-example }

```python
import json

TOOLS = {
    "search": lambda args: f"3 results for '{args['query']}'",
    "calculator": lambda args: str(eval(args["expression"], {"__builtins__": {}})),
}

TOOL_SCHEMAS = {
    "search": {"query": str},
    "calculator": {"expression": str},
}

def validate(name: str, args: dict) -> bool:
    schema = TOOL_SCHEMAS.get(name)
    if schema is None:
        return False
    return all(isinstance(args.get(k), t) for k, t in schema.items())

def run_agent(user_msg: str, llm_call, max_steps: int = 6) -> str:
    messages = [{"role": "user", "content": user_msg}]
    for step in range(max_steps):
        response = llm_call(messages, tools=list(TOOLS))
        if response.get("final_answer") is not None:
            return response["final_answer"]

        name, args = response["tool"], response["arguments"]
        if not validate(name, args):
            observation = f"ERROR: invalid arguments for tool '{name}'"
        else:
            observation = TOOLS[name](args)

        messages.append({"role": "assistant", "content": json.dumps(response)})
        messages.append({"role": "tool", "content": observation})
    return "Agent exceeded max_steps without a final answer."
```

Three things earning their keep here that a demo would skip: `max_steps` (a hard ceiling, not a suggestion), `validate()` running before execution (not trusting the model's arguments to match the schema just because they usually do), and errors going back into context as observations rather than crashing the loop — the model gets a chance to recover from its own mistake, the same way you'd want a junior engineer to see a failing test rather than have the process silently die.

## Failure mode
{: #failure-mode }

Three ways this goes wrong in production, each corresponding to a guard above:

- **No termination condition.** Without `max_steps`, a model that gets a confusing observation can loop forever, calling the same tool with slight variations, burning tokens and money with no forward progress.
- **Hallucinated arguments.** Models confidently emit plausible-looking arguments that don't match reality — a file path that doesn't exist, a parameter name close to but not exactly the schema's. Skip validation and you execute garbage as if it were intentional.
- **Cascading trust.** Once a bad observation enters context — a tool returned wrong data, or a hallucinated call "succeeded" with fabricated output — every subsequent step reasons on top of it as ground truth. One bad link early in the chain corrupts everything downstream, which is why sandboxing risky tools (code exec, spending money, sending messages) behind human approval matters more than making the loop smarter.

## Exercise
{: #exercise }

The `calculator` tool above calls Python's `eval` on the model's `expression` string. Write an input the model could plausibly be tricked into emitting — via a prompt-injected observation from `search`, say — that would do something the tool's author never intended. Then rewrite `calculator` so that no input, however adversarial, can escape simple arithmetic. What's the general principle behind your fix, and does it depend at all on the model's intentions being good?


---

[← 40. RAG: Retrieval-Augmented Generation](/courses/llm-mastery/40-rag-retrieval/)  
[42. Hallucinations: Why They Happen →](/courses/llm-mastery/42-hallucinations/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
