---
layout: post
title: "Getting Started with FastAPI"
date: 2026-07-10
description: "Build a real in-memory notes API — GET, POST, DELETE, validation errors, 404s — and check every response code with curl, not vibes."
tags: [fastapi, python, getting-started]
---

FastAPI is a pleasant way to wrap models and scripts behind HTTP. Auto docs, type hints, and Pydantic validation make it a strong default for LLM demos and internal tools. This post builds a small but real API with four routes and deliberately exercises its error paths — a 404 and a 422 you trigger yourself, not just the happy path.

## Install

```bash
pip install fastapi uvicorn
```

## Mini project: a notes API with real validation and error handling

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Notes API")


class Note(BaseModel):
    id: int
    text: str


class NoteIn(BaseModel):
    text: str = Field(min_length=1, max_length=500)


notes: dict[int, Note] = {}
next_id = 1


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/notes")
def list_notes():
    return list(notes.values())


@app.post("/notes", status_code=201)
def create_note(body: NoteIn):
    global next_id
    note = Note(id=next_id, text=body.text)
    notes[next_id] = note
    next_id += 1
    return note


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="note not found")
    return notes[note_id]


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="note not found")
    del notes[note_id]
```

Run it and open the auto-generated docs:

```bash
uvicorn main:app --reload --port 8000
# open http://127.0.0.1:8000/docs
```

Now exercise every path with `curl`, including the two that should fail on purpose:

```bash
curl -s http://127.0.0.1:8000/health
# {"ok":true}

curl -s -X POST http://127.0.0.1:8000/notes \
  -H 'content-type: application/json' -d '{"text":"buy milk"}'
# {"id":1,"text":"buy milk"}  — check the HTTP status too:

curl -s -o /dev/null -w "%{http_code}\n" -X POST http://127.0.0.1:8000/notes \
  -H 'content-type: application/json' -d '{"text":"buy eggs"}'
# 201, not the default 200 — because of status_code=201 on the route

curl -s http://127.0.0.1:8000/notes
# [{"id":1,...},{"id":2,...}]

curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/notes/999
# 404 — an id that was never created

curl -s -X POST http://127.0.0.1:8000/notes \
  -H 'content-type: application/json' -d '{"text":""}' \
  -o /dev/null -w "%{http_code}\n"
# 422 — Pydantic's min_length=1 rejected it before your code ever ran

curl -s -X DELETE http://127.0.0.1:8000/notes/1 -o /dev/null -w "%{http_code}\n"
# 204
```

If any of those status codes don't match, that's the bug to chase — the point of writing them down is having something concrete to check against, not "it looked like it worked in the docs UI."

## Why it fits AI work

| Need | FastAPI habit |
|------|----------------|
| Validate inputs before they hit your model | Pydantic models (the `NoteIn` pattern above) |
| Long model calls | background tasks or a job queue, not a blocking route |
| Ship consistently | [Docker](/2026/07/10/getting-started-with-docker/) + uvicorn |
| Explore the API while building | `/docs` (Swagger UI) — try requests directly from the browser |

Keep inference or business logic in a plain Python module; the route itself should stay thin: validate → call → return.

## Common footguns

- **In-memory state isn't persistence** — the `notes` dict resets to empty every time `uvicorn --reload` restarts (which it does automatically on file changes). This is fine for learning; for anything real, back it with the SQLite schema from [Getting Started with SQL](/2026/07/10/getting-started-with-sql/).
- **Blocking code inside `async def`** — a synchronous call like `time.sleep()` or heavy file I/O inside an `async def` route blocks the *entire* event loop, stalling every other request. Use a plain `def` route for sync work (FastAPI runs it in a thread pool automatically) or `await` a genuinely async call.
- **Forgetting the default status code** — routes return `200` unless you set `status_code=` explicitly; a `POST` that creates a resource should return `201`, a `DELETE` typically `204`.
- **Trusting raw `dict`/`request.json()` instead of Pydantic** — skips validation entirely, so malformed input reaches your business logic instead of failing fast with a clear `422`.
- **CORS errors when calling from a browser on a different origin** — add `CORSMiddleware` explicitly; FastAPI doesn't allow cross-origin requests by default, on purpose.
- **Leaving `--reload` on outside development** — it watches the filesystem and restarts the process, which is convenient locally and inappropriate (and slower) in production.

## You know you're done when…

- [ ] `GET /health` returns `{"ok": true}` with status `200`
- [ ] `POST /notes` with a valid body returns status `201` and an incrementing `id`
- [ ] `GET /notes/999` (an id that doesn't exist) returns `404`, not a `500` or an empty `200`
- [ ] `POST /notes` with `{"text": ""}` returns `422` because of Pydantic's `min_length`
- [ ] You can explain why restarting `uvicorn --reload` wipes your notes, and what you'd change to make them survive a restart

## Next

Serve a tiny model after [LLM Mastery](/courses/llm-mastery/) (quantization & serving in article 44). For product UIs, pair with [Getting Started with JavaScript](/2026/07/10/getting-started-with-javascript/).
