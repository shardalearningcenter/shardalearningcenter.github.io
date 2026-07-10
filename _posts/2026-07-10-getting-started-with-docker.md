---
layout: post
title: "Getting Started with Docker"
date: 2026-07-10
description: "Images vs containers, a minimal Dockerfile, and how to ship a tiny Python API the same way every time."
tags: [docker, getting-started]
---

Docker packages “it works on my machine” into something you can ship. For ML and APIs, that means: same Python, same system libs, same entrypoint — on your laptop and in CI.

## Concepts

| Term | Meaning |
|------|---------|
| **Image** | Immutable filesystem + metadata (the recipe result) |
| **Container** | A running (or stopped) instance of an image |
| **Dockerfile** | Instructions to build an image |
| **Volume** | Persistent data outside the container filesystem |

```bash
docker run --rm -it python:3.12-slim bash
# inside: python --version; exit
```

`--rm` deletes the container when it exits. `-it` gives you an interactive terminal.

## Minimal Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t hello-api .
docker run --rm -p 8000:8000 hello-api
curl http://127.0.0.1:8000/health
```

## Habits that save pain

- Pin base images (`python:3.12.8-slim`) when reproducibility matters.
- Put dependency install before `COPY . .` so code edits do not bust the pip cache every time.
- Do not bake secrets into images; pass env vars or mount secrets at runtime.
- Prefer one process per container.

## Exercise

1. Create a 10-line FastAPI (or Flask) hello world.
2. Write a Dockerfile.
3. Build and run it; hit `/health` from the host.
4. Bonus: multi-stage build or a non-root `USER`.

## Next

[FastAPI getting started](/blog/2026/07/10/getting-started-with-fastapi/) · wrap models behind HTTP after [LLM Mastery](/courses/llm-mastery/).
