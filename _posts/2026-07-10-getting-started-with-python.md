---
layout: post
title: "Getting Started with Python (the useful parts)"
date: 2026-07-10
description: "Install a clean venv, learn the data structures that matter, then build a real argparse CLI tool end to end — the Python you need before ML and LLMs."
tags: [python, getting-started]
---

Python is the glue language of modern AI, but you do not need every language feature to be productive. You need a clean environment, a handful of data structures, and the habit of writing small scripts that touch real files and take real arguments. This post gets you there with one tool you build, run, and extend yourself — not a wall of syntax you'll forget by Friday.

## Install and isolate

```bash
python3 --version          # aim for 3.10+
python3 -m venv .venv
source .venv/bin/activate  # Windows (PowerShell): .venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"   # confirm it points inside .venv
pip install --upgrade pip
```

Two things trip up almost everyone new to Python:

- On Ubuntu/Debian the command is `python3`, not `python`, until you activate a venv (which usually symlinks `python` for you). If `python` is "not found," check that first.
- `python -c "import sys; print(sys.executable)"` is your sanity check. If it prints a system path instead of something ending in `.venv/bin/python`, your venv isn't active — and any `pip install` you run next pollutes the wrong environment.

One project → one virtualenv. Never `pip install` into the system Python for learning work; it turns into unremovable clutter within a month.

## Core ideas in one screen

| Idea | Why it matters |
|------|----------------|
| Everything is an object | `type(x)`, `dir(x)` teach you the language |
| Lists / dicts / sets | 90% of day-one data work |
| Functions are first-class | Pass them, return them, use them in `map`/`filter` |
| `with` for resources | Files and connections close correctly, even on error |
| Comprehensions | Compact transforms without a `for`-loop wrapper |

```python
from pathlib import Path

# list comprehension: transform + filter in one line
lengths = [len(w) for w in "a longer sentence here".split() if len(w) > 3]

# dict comprehension: build lookups fast
by_len = {w: len(w) for w in ["cat", "elephant", "ox"]}

# `with` guarantees the file handle closes even if read() raises
text = Path("notes.txt").read_text(encoding="utf-8") if Path("notes.txt").exists() else ""
```

## Mini project: a real CLI tool, not a toy snippet

Most "getting started" posts show you a script you run once. Build a small command-line tool instead — it forces you to touch arguments, files, and error paths, which is where Python actually gets used.

```python
#!/usr/bin/env python3
"""wordcount.py - rank word frequency across one or more text files."""
import argparse
import re
from collections import Counter
from pathlib import Path

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
    "to", "of", "in", "on", "for", "it", "this", "that",
}


def read_words(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8").lower()
    return re.findall(r"[a-z']+", text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Count word frequency in text files.")
    parser.add_argument("files", nargs="+", type=Path, help="one or more text files")
    parser.add_argument("-n", "--top", type=int, default=10, help="how many words to show")
    parser.add_argument("--no-stopwords", action="store_true", help="drop common stopwords")
    args = parser.parse_args()

    counts: Counter[str] = Counter()
    for path in args.files:
        if not path.exists():
            raise SystemExit(f"error: {path} does not exist")
        counts.update(read_words(path))

    if args.no_stopwords:
        for word in STOPWORDS:
            counts.pop(word, None)

    for word, n in counts.most_common(args.top):
        print(f"{n:5d}  {word}")


if __name__ == "__main__":
    main()
```

Run it end to end:

```bash
printf "the quick brown fox jumps over the lazy dog. the dog barks at the fox.\n" > notes.txt
python wordcount.py notes.txt
python wordcount.py notes.txt --no-stopwords -n 5
python wordcount.py missing.txt      # exercises the error path — should exit cleanly, not traceback
```

The first run shows `the` at the top with count 4. The second, with stopwords stripped, promotes `dog` and `fox` (count 2 each) to the top. The third should print your `SystemExit` message and exit with a non-zero code — try `echo $?` right after to confirm.

Extend it yourself: add a `--min-length` flag, or read from stdin when no files are given (`if not sys.stdin.isatty(): ...`).

## Common footguns

- **Mutable default arguments** — `def f(x=[])` reuses the *same* list across every call. Use `def f(x=None): x = x or []`.
- **Bare `except:`** — swallows `KeyboardInterrupt` and typos alike. Catch the specific exception you can actually handle.
- **`range(len(x))` instead of `enumerate(x)`** — works, but hides intent and invites off-by-one bugs.
- **Comparing floats with `==`** — `0.1 + 0.2 == 0.3` is `False`. Use `math.isclose()`.
- **Forgetting `.lower()` before comparing strings** — silent case-mismatch bugs that "work on my test data."
- **Mixing tabs and spaces** — Python 3 raises `TabError`; configure your editor to show whitespace and insert spaces only.

## You know you're done when…

- [ ] `python -c "import sys; print(sys.executable)"` prints a path inside `.venv`, not your system Python
- [ ] `python wordcount.py notes.txt` runs with no traceback and prints ranked counts
- [ ] `--no-stopwords` visibly changes which words rank highest
- [ ] `python wordcount.py missing.txt` fails with your error message, not a raw `FileNotFoundError` traceback
- [ ] You can explain, without looking it up, why `def f(x=[])` is a bug

## Next

- [Python in 10 Days](/courses/python-10-days/) — structured sprint
- [Getting Started with PyTorch](/2026/07/10/getting-started-with-pytorch/) — tensors next
- [Getting Started with FastAPI](/2026/07/10/getting-started-with-fastapi/) — wrap scripts like this one behind HTTP
- [LLM Mastery](/courses/llm-mastery/) — when you want language models from first principles
