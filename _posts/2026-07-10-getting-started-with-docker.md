---
layout: post
title: "Getting Started with Docker"
date: 2026-07-10
description: "Images vs containers, a minimal Dockerfile, and a full build-run-inspect-cleanup cycle for a tiny Python API — the same one every time."
tags: [docker, getting-started]
---

Docker packages "it works on my machine" into something you can ship. For ML and APIs, that means: same Python, same system libraries, same entrypoint — on your laptop and in CI. This post takes you through the entire lifecycle once: build, run, verify, inspect, stop, and clean up — the part most tutorials skip.

## Concepts

| Term | Meaning |
|------|---------|
| **Image** | Immutable filesystem + metadata (the recipe result) |
| **Container** | A running (or stopped) instance of an image |
| **Dockerfile** | Instructions to build an image, executed top to bottom |
| **Layer** | Each Dockerfile instruction adds a cached layer; unchanged layers are reused on rebuild |
| **Volume** | Persistent data living outside the container's writable layer |

```bash
docker run --rm -it python:3.12-slim bash
# inside the container: python --version; exit
```

`--rm` deletes the container the moment it exits. `-it` gives you an interactive terminal attached to it.

## Mini project: build, run, verify, inspect, clean up

```bash
mkdir docker-hello && cd docker-hello

cat > requirements.txt <<'EOF'
fastapi
uvicorn[standard]
EOF

cat > main.py <<'EOF'
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}
EOF

cat > Dockerfile <<'EOF'
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

cat > .dockerignore <<'EOF'
.venv
__pycache__
*.pyc
.git
EOF
```

Dependencies are installed **before** `COPY . .` on purpose: editing `main.py` later won't bust the pip-install cache layer, so rebuilds stay fast.

```bash
docker build -t hello-api .
docker run -d --name hello --rm -p 8000:8000 hello-api

curl -s http://127.0.0.1:8000/health          # {"ok":true}
docker logs hello                              # confirms uvicorn actually started
docker exec -it hello bash -c "python --version"   # peek inside the running container

docker stop hello                              # --rm means this also deletes the container
docker ps -a                                   # confirm it's gone, not just stopped
```

Cleanup — useful once containers and images pile up:

```bash
docker images                 # see what's on disk
docker system prune -f        # removes stopped containers, dangling images, unused networks
```

`docker system prune` is destructive for anything not currently running or tagged as in-use — read what it says it will remove before you run it on a machine with work you care about.

## Habits that save pain

- Pin base images (`python:3.12.8-slim`) when reproducibility matters; `latest` silently changes under you.
- Put dependency installs before `COPY . .` (done above) so code edits don't bust the pip cache every time.
- Don't bake secrets into images — pass environment variables or mount secrets at runtime, since anything in a layer is recoverable from the image history.
- Prefer one process per container; if you need two processes, you probably need two containers plus `docker compose`, not a supervisor script.
- Always ship a `.dockerignore` — without one, `COPY . .` pulls in `.git`, `.venv`, and `node_modules`, bloating the build context and sometimes leaking history into the image.

## Common footguns

- **"permission denied" on `/var/run/docker.sock`** — on Linux, add your user to the `docker` group (`sudo usermod -aG docker $USER`, then log out/in) instead of prefixing every command with `sudo`.
- **"port is already allocated"** — something else is bound to `8000`; either stop it (`docker ps` to find the culprit) or map a different host port (`-p 8001:8000`).
- **Forgetting `--rm`** — stopped containers accumulate silently and eat disk; `docker ps -a` reveals them, `docker container prune` clears them.
- **Root by default** — containers run as root unless you add a `USER` instruction; fine for local learning, a real problem for anything internet-facing.
- **Rebuilding without noticing cache reuse** — if you change `requirements.txt`, Docker reruns `pip install`; if you only change `main.py`, it reuses the cached install layer. Confusing these two is a common "why is this taking so long" moment.

## You know you're done when…

- [ ] `docker build` finishes with no errors and `docker images` lists `hello-api`
- [ ] `curl http://127.0.0.1:8000/health` returns `{"ok":true}` while the container runs detached (`-d`)
- [ ] `docker logs hello` shows the uvicorn startup line, proving the process actually started (not just that the container exists)
- [ ] After `docker stop hello`, `docker ps -a` shows it gone (because of `--rm`), not lingering as "Exited"
- [ ] You have a `.dockerignore` so `.git` and `.venv` never enter the build context

## Next

[Getting Started with FastAPI](/2026/07/10/getting-started-with-fastapi/) — the API you just containerized, explained properly · wrap models behind HTTP after [LLM Mastery](/courses/llm-mastery/).
