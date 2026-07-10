---
layout: post
title: "Getting Started with the Linux Shell"
date: 2026-07-10
description: "pwd, pipes, grep, and curl — the shell survival kit for developers and ML engineers."
tags: [linux, shell, getting-started]
---

The shell is how you talk to the machine without a mouse. Every serious ML and backend workflow eventually lands here: datasets, logs, Docker, SSH, CI.

## Survival kit

```bash
pwd                 # where am I?
ls -la              # what is here?
cd path             # move
mkdir -p a/b        # create dirs
cp src dst && mv old new
rm -i file          # interactive delete (safer while learning)
cat file | less     # view
head -n 20 file
tail -f log.txt     # follow a growing log
```

Find and search:

```bash
grep -n "ERROR" app.log
grep -R "TODO" . --include="*.py"
find . -name "*.csv"
```

Network peek:

```bash
curl -I https://example.com
curl -s https://httpbin.org/json | head
```

## Pipes and redirection

Programs read stdin and write stdout. Chain them:

```bash
cat access.log | grep " 500 " | awk '{print $1}' | sort | uniq -c | sort -nr | head
```

| Operator | Meaning |
|----------|---------|
| `\|` | pipe stdout → next stdin |
| `>` | overwrite file |
| `>>` | append |
| `2>` | redirect stderr |

## Paths and permissions

- `.` current, `..` parent, `~` home
- `chmod +x script.sh` then `./script.sh`
- Prefer absolute paths in scripts you will run from cron or CI

## Exercise

Invent a tiny log format (`IP METHOD PATH STATUS`), write 20 lines to `toy.log`, then write a one-liner that prints the top 5 IPs by request count.

## Next

[Docker](/blog/2026/07/10/getting-started-with-docker/) packages the environment you just learned to navigate. [Git](/blog/2026/07/10/getting-started-with-git/) version-controls the scripts you write in the shell.
