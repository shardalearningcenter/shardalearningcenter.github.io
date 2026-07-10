---
layout: post
title: "Getting Started with Python (the useful parts)"
date: 2026-07-10
description: "Install, venv, core types, and a tiny word-count project — the Python you need before ML and LLMs."
tags: [python, getting-started]
---

Python is the glue language of modern AI. You do not need every language feature. You need a clean environment, a few data structures, and the habit of writing small scripts that touch real files.

## Install and isolate

```bash
python3 --version          # aim for 3.10+
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install numpy
```

One project → one virtualenv. Never `pip install` into the system Python for learning work.

## Core ideas in one screen

| Idea | Why it matters |
|------|----------------|
| Everything is an object | `type(x)`, `dir(x)` teach you the language |
| Lists / dicts / sets | 90% of day-one data work |
| Functions are first-class | Pass them, return them, use them in `map` |
| `with` for resources | Files and connections close correctly |
| Comprehensions | Compact transforms without ceremony |

```python
from collections import Counter

def top_words(path: str, n: int = 20) -> list[tuple[str, int]]:
    text = open(path, encoding="utf-8").read().lower()
    words = [w.strip(".,!?;:\"'()[]") for w in text.split()]
    words = [w for w in words if w]
    return Counter(words).most_common(n)

if __name__ == "__main__":
    for word, count in top_words("notes.txt"):
        print(f"{count:4d}  {word}")
```

## Tiny project

1. Save the script above as `wordcount.py`.
2. Drop any text file next to it as `notes.txt`.
3. Run `python wordcount.py`.
4. Extend it: ignore stopwords (`the`, `a`, `and`), or print a CSV.

## Common footguns

- Mixing tabs and spaces → use an editor that shows whitespace.
- Mutable default args (`def f(x=[])`) → use `None` and create inside.
- Catching bare `Exception` everywhere → catch what you can fix.

## Next

- [Python in 10 Days](/courses/python-10-days/) — structured sprint
- [Getting Started with PyTorch](/blog/2026/07/10/getting-started-with-pytorch/) — tensors next
- [LLM Mastery](/courses/llm-mastery/) — when you want language models from first principles
