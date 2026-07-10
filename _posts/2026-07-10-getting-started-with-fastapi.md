---
layout: post
title: "Getting Started with FastAPI"
date: 2026-07-10
description: "Health checks, Pydantic validation, and a POST echo — wrap models and scripts behind a clean HTTP API."
tags: [fastapi, python, getting-started]
---

FastAPI is a pleasant way to wrap models and scripts behind HTTP. Auto docs, type hints, and Pydantic validation make it a strong default for LLM demos and internal tools.

## Install and hello

```bash
pip install fastapi uvicorn
```

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Hello API")

@app.get("/health")
def health():
    return {"ok": True}

class EchoIn(BaseModel):
    message: str

@app.post("/echo")
def echo(body: EchoIn):
    return {"you_said": body.message}
```

```bash
uvicorn main:app --reload --port 8000
# open http://127.0.0.1:8000/docs
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/echo \
  -H 'content-type: application/json' \
  -d '{"message":"hi"}'
```

## Why it fits AI work

| Need | FastAPI habit |
|------|----------------|
| Validate inputs | Pydantic models |
| Long model calls | background tasks or a job queue later |
| Ship consistently | [Docker](/blog/2026/07/10/getting-started-with-docker/) + uvicorn |
| Explore API | `/docs` (Swagger) while developing |

Keep inference code in a plain Python module; the route should be thin: validate → call → return.

## Exercise

1. Add `POST /predict` that accepts `{"text": "..."}` and returns `{"n_chars": N, "n_words": M}`.
2. Reject empty `text` with a 422 (Pydantic `min_length=1`).
3. Containerize it with the Docker getting-started guide.

## Next

Serve a tiny model after [LLM Mastery](/courses/llm-mastery/) (quantization & serving in art. 44). For product UIs, pair with [JavaScript](/blog/2026/07/10/getting-started-with-javascript/).
