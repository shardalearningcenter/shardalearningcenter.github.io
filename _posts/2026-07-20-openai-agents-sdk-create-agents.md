---
layout: post
title: "How to Use the OpenAI Agents SDK to Create Agents (Hands-On)"
date: 2026-07-20
tags: [AI, LLM, OpenAI, Agents, Python, SDK]
---

# How to Use the OpenAI Agents SDK to Create Agents (Hands-On)

Build real agents with the official **OpenAI Agents SDK** (`openai-agents`) — the lightweight, production-oriented framework that replaced Swarm. You will create a single agent, add tools, then orchestrate specialists with handoffs.

**Docs:** [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)  
**Related on this site:** [LLM Bootcamp](/llm-bootcamp/) · [AI LLM Roadmap](/2026/07/20/ai-llm-developer-roadmap.html) · [Build first LLM apps](/2026/07/21/build-your-first-llm-apps-python-rag.html)

---

## What the SDK Gives You

A small set of primitives:

| Primitive | Job |
|---|---|
| `Agent` | LLM + instructions + tools + handoffs |
| `Runner` | Runs the agent loop (tool calls, handoffs) |
| `function_tool` | Turn any Python function into a tool |
| Handoffs | Route work to specialist agents |
| Tracing | Debug runs in the OpenAI dashboard |

Provider-agnostic at the edges, but this guide uses the OpenAI API.

---

## 1. Setup (5 minutes)

```bash
mkdir openai-agents-lab
cd openai-agents-lab
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install openai-agents
```

Set your API key:

```powershell
# PowerShell
$env:OPENAI_API_KEY = "sk-..."
```

```bash
# macOS / Linux
export OPENAI_API_KEY=sk-...
```

Never commit the key. Use env vars or a secrets manager.

---

## 2. Hello World Agent

Create `01_hello_agent.py`:

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. Keep answers short.",
)

result = Runner.run_sync(
    agent,
    "Write a haiku about recursion in programming.",
)
print(result.final_output)
```

Run:

```bash
python 01_hello_agent.py
```

**Async version** (preferred in servers / FastAPI):

```python
import asyncio
from agents import Agent, Runner

agent = Agent(
    name="History Tutor",
    instructions="You answer history questions clearly and concisely.",
)

async def main():
    result = await Runner.run(
        agent,
        "When did the Roman Empire fall?",
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

### What matters
- `name` — label for tracing / handoffs  
- `instructions` — system-style behavior  
- `Runner.run` / `run_sync` — executes the agent loop  
- `result.final_output` — the answer you show users  

---

## 3. Give the Agent Tools

Tools let the model call your Python code (search, DB, calculator, APIs).

Create `02_tools.py`:

```python
import asyncio
from agents import Agent, Runner, function_tool

@function_tool
def history_fun_fact() -> str:
    """Return a short surprising history fact."""
    return "Sharks are older than trees."

@function_tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers exactly."""
    return a + b

agent = Agent(
    name="Tool Tutor",
    instructions=(
        "Answer clearly. "
        "Use history_fun_fact for history curiosities. "
        "Use add_numbers for arithmetic — never guess math."
    ),
    tools=[history_fun_fact, add_numbers],
)

async def main():
    result = await Runner.run(
        agent,
        "Tell me one surprising ancient-life fact, then compute 19.5 + 22.25.",
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

### Tool tips
- Write a **clear docstring** — the model uses it to decide when to call the tool  
- Type hints become the tool schema  
- Keep tools small and deterministic when possible  

---

## 4. Multi-Agent Handoffs (Triage → Specialists)

Pattern: a **triage agent** routes to specialists.

Create `03_handoffs.py`:

```python
import asyncio
from agents import Agent, Runner

history_tutor = Agent(
    name="History Tutor",
    handoff_description="Specialist for historical questions",
    instructions="Answer history questions clearly and concisely.",
)

math_tutor = Agent(
    name="Math Tutor",
    handoff_description="Specialist for math questions",
    instructions="Explain math step by step with a short worked example.",
)

triage = Agent(
    name="Homework Triage",
    instructions="Route each homework question to the right specialist.",
    handoffs=[history_tutor, math_tutor],
)

async def main():
    result = await Runner.run(
        triage,
        "Who was the first president of the United States?",
    )
    print(result.final_output)
    print("Answered by:", result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())
```

### Handoffs vs “agents as tools”

| Pattern | Who stays in control? | Use when |
|---|---|---|
| **Handoffs** | Specialist takes over | Clear domains (math vs history) |
| **Agents as tools** | Manager stays in control | Manager must merge multiple specialist outputs |

Start with handoffs — shortest path for routing.

---

## 5. Structured Output (Optional but Powerful)

Ask the agent to return typed data with Pydantic:

```python
from pydantic import BaseModel
from agents import Agent, Runner

class Ticket(BaseModel):
    priority: str
    category: str
    summary: str

agent = Agent(
    name="Support Sorter",
    instructions="Classify the support message.",
    output_type=Ticket,
)

result = Runner.run_sync(
    agent,
    "My payment failed twice and I need this fixed today.",
)
print(result.final_output)          # Ticket object
print(result.final_output.priority)
```

Great for APIs: validate → store → respond.

---

## 6. Multi-Turn Conversations

For a second turn, pass prior context back:

```python
import asyncio
from agents import Agent, Runner

agent = Agent(
    name="Coach",
    instructions="You are a concise coding coach.",
)

async def main():
    r1 = await Runner.run(agent, "I am learning Python.")
    print("Turn 1:", r1.final_output)

    r2 = await Runner.run(
        agent,
        "What should I learn next?",
        # continue from previous turn:
        input=r1.to_input_list() + [
            {"role": "user", "content": "What should I learn next?"}
        ],
    )
    # Simpler approach often shown in docs:
    # pass result.to_input_list() merged with the new user message
    print("Turn 2:", r2.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

Practical pattern:

```python
result = await Runner.run(agent, "Hi, I am Sam.")
next_input = result.to_input_list() + [
    {"role": "user", "content": "Remind me of my name and give one tip."}
]
result2 = await Runner.run(agent, next_input)
print(result2.final_output)
```

For longer apps, use SDK **sessions** or OpenAI server-managed `conversation_id` / `previous_response_id` (see [Running agents](https://openai.github.io/openai-agents-python/running_agents/)).

---

## 7. Mini Project — Support Desk Agent

Build a tiny support desk with tools + triage.

`04_support_desk.py`:

```python
import asyncio
from agents import Agent, Runner, function_tool

ORDERS = {
    "A100": {"status": "shipped", "eta_days": 2},
    "A200": {"status": "processing", "eta_days": 5},
}

@function_tool
def lookup_order(order_id: str) -> str:
    """Look up an order status by id like A100."""
    order = ORDERS.get(order_id.upper())
    if not order:
        return f"No order found for {order_id}"
    return f"Order {order_id}: status={order['status']}, eta_days={order['eta_days']}"

@function_tool
def refund_policy() -> str:
    """Return the refund policy summary."""
    return "Refunds within 30 days of purchase. Digital goods: 14 days."

orders_agent = Agent(
    name="Orders Agent",
    handoff_description="Handles shipping and order status questions",
    instructions="Use lookup_order for status. Be concise.",
    tools=[lookup_order],
)

policy_agent = Agent(
    name="Policy Agent",
    handoff_description="Handles refund and policy questions",
    instructions="Use refund_policy. Do not invent legal terms.",
    tools=[refund_policy],
)

desk = Agent(
    name="Support Desk",
    instructions=(
        "You are the front desk. "
        "Hand off order/shipping questions to Orders Agent. "
        "Hand off refund/policy questions to Policy Agent."
    ),
    handoffs=[orders_agent, policy_agent],
)

async def main():
    questions = [
        "Where is order A100?",
        "What is your refund window?",
        "Status for A999 please",
    ]
    for q in questions:
        result = await Runner.run(desk, q)
        print("\nQ:", q)
        print("A:", result.final_output)
        print("via:", result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())
```

### Stretch ideas
- Add a `create_ticket(summary: str)` tool that appends to `tickets.json`  
- Wrap with FastAPI (`POST /ask`)  
- Log `result.last_agent.name` for analytics  

---

## 8. Debug with Traces

Every run can appear in the OpenAI **Trace viewer** (dashboard). Use it to see:

- Which tools were called  
- Handoff decisions  
- Latency / errors  

When something feels “random,” open the trace before rewriting prompts.

---

## 9. Common Pitfalls

| Problem | Fix |
|---|---|
| `OPENAI_API_KEY` missing | Set env var in the same terminal session |
| Tool never called | Improve docstring + instructions (“use X when…”) |
| Wrong specialist | Strengthen `handoff_description` + triage instructions |
| Hallucinated facts | Force tools for lookups; forbid guessing in instructions |
| Sync in async server | Use `await Runner.run` inside FastAPI routes |

---

## 10. How This Maps to Jobs

| Skill shown | Interview signal |
|---|---|
| Single agent + `Runner` | Can ship GenAI features |
| `function_tool` | Tool-calling / function calling |
| Handoffs | Multi-agent orchestration |
| Structured `output_type` | Production API design |
| Traces | Debuggability / LLMOps mindset |

Pair this with your [Document Knowledge Assistant capstone](/2026/07/23/advanced-document-knowledge-assistant-rag-project.html) (RAG) for a strong portfolio combo: **RAG + Agents SDK**.

---

## Checklist

- [ ] Installed `openai-agents` and set `OPENAI_API_KEY`  
- [ ] Ran hello-world with `Runner.run_sync`  
- [ ] Added at least one `@function_tool`  
- [ ] Built a triage agent with 2 handoffs  
- [ ] Inspected a run in the Trace viewer  
- [ ] (Bonus) Support desk mini project works  

---

## Next Steps

- Official quickstart: [openai.github.io/openai-agents-python/quickstart](https://openai.github.io/openai-agents-python/quickstart/)  
- Tools guide: [Tools](https://openai.github.io/openai-agents-python/tools/)  
- JS/TS twin: [`@openai/agents`](https://github.com/openai/openai-agents-js)  
- On this site: [LLM Bootcamp](/llm-bootcamp/) · [Prompting → Fine-tuning → LLMOps](/2026/07/22/prompting-to-finetuning-llmops-career.html)

---

*Start with one agent. Add one tool. Then add one handoff. That is how agent systems stay understandable.*
