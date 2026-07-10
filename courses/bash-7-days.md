---
layout: course
title: "Bash in 7 Days — Hands-On"
permalink: /courses/bash-7-days/
course_track: "Bash"
description: "Shell scripting for real work: globs, pipes, scripts, and safe automation."
toc:
  - id: "day-1-navigation-files"
    label: "Day 1: Navigation & files"
  - id: "day-2-variables-quoting"
    label: "Day 2: Variables & quoting"
  - id: "day-3-pipes-filters"
    label: "Day 3: Pipes & filters"
  - id: "day-4-control-flow"
    label: "Day 4: Control flow"
  - id: "day-5-functions-set-euo"
    label: "Day 5: Functions & set -euo"
  - id: "day-6-json-http"
    label: "Day 6: JSON & HTTP"
  - id: "day-7-real-automation"
    label: "Day 7: Real automation"
  - id: "capstone"
    label: "Capstone project"
---

# Bash in 7 Days — Hands-On

Shell scripting for real work: globs, pipes, scripts, and safe automation.

## Why this language
{: #why-this-language }

Every server, container, and CI job speaks shell. Automate the boring glue.

## Setup (Day 0)
{: #setup-day-0 }

Any Linux/macOS terminal:
```bash
bash --version
mkdir bash-lab && cd bash-lab
```

---

## Day 1: Navigation & files
{: #day-1-navigation-files }

### What you'll learn

- cd/ls/cp/mv
- globs
- permissions

### Code along

```bash
#!/usr/bin/env bash
set -euo pipefail
echo "PWD=$PWD"
ls -la
```

### Your task

Script that creates `out/` and copies `*.txt` into it.

---

## Day 2: Variables & quoting
{: #day-2-variables-quoting }

### What you'll learn

- $VAR
- "$VAR"
- arrays

### Code along

```bash
name="Ada Lovelace"
echo "Hello, $name"
files=(a.txt b.txt)
echo "${files[0]}"
```

### Your task

Script taking a name arg; exit 1 if missing.

---

## Day 3: Pipes & filters
{: #day-3-pipes-filters }

### What you'll learn

- grep/sed/awk
- sort/uniq
- cut

### Code along

```bash
printf "b\na\nb\n" | sort | uniq -c
```

### Your task

From a fake log, top 5 IPs.

---

## Day 4: Control flow
{: #day-4-control-flow }

### What you'll learn

- if
- for
- while
- case

### Code along

```bash
for f in *.md; do echo "FILE=$f"; done
```

### Your task

Loop files; print size via `wc -c`.

---

## Day 5: Functions & set -euo
{: #day-5-functions-set-euo }

### What you'll learn

- functions
- pipefail
- trap

### Code along

```bash
die() { echo "$*" >&2; exit 1; }
need_cmd() { command -v "$1" >/dev/null || die "missing $1"; }
need_cmd curl
```

### Your task

Script that checks for git/curl/jq before running.

---

## Day 6: JSON & HTTP
{: #day-6-json-http }

### What you'll learn

- curl
- jq
- exit codes

### Code along

```bash
curl -s https://httpbin.org/uuid | jq -r .uuid
```

### Your task

Fetch UUID; write to `id.txt`; fail if empty.

---

## Day 7: Real automation
{: #day-7-real-automation }

### What you'll learn

- cron mindset
- logging
- idempotent scripts

### Code along

```bash
log() { echo "$(date -Is) $*"; }
log "start backup"
# rsync -a ./data/ ./backup/
```

### Your task

Idempotent backup script: copy `data/` → `backup/` only if source newer.


---

## Capstone project
{: #capstone }

Write a **project bootstrap script**: create dirs, check deps, write a `.env.example`, and print next steps. Use `set -euo pipefail` throughout.

## Related

- [Getting Started with Linux Shell](/blog/2026/07/10/getting-started-with-linux-shell/)
- [Docker getting started](/blog/2026/07/10/getting-started-with-docker/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
