---
layout: post
title: "Getting Started with Git (without the fear)"
date: 2026-07-10
description: "Five daily commands, a clear mental model, and one practice repo — enough Git to ship course projects."
tags: [git, getting-started]
---

Git is a time machine for your files. Most “Git anxiety” comes from treating it as magic. Learn five commands deeply, then add the rest when you need them.

## Daily driver

```bash
git status                 # where am I?
git add -p                 # stage hunks intentionally
git commit -m "message"    # snapshot with a why
git log --oneline -10      # recent history
git diff                   # unstaged changes
git diff --staged          # what will be committed
```

Commit messages: say **why**, not “update files.”

## Mental model

```
working tree  →  staging area  →  commit (immutable snapshot)
     edit            git add           git commit
```

- A **branch** is a movable label pointing at a commit.
- `main` is just a convention, not a special object.
- Remotes (`origin`) are other copies of the same graph.

```bash
git branch feature-x
git switch feature-x       # or: git checkout -b feature-x
# ... edit, commit ...
git switch main
git merge feature-x
```

## Undo without panic

| Situation | Safe move |
|-----------|-----------|
| Unstaged edits you hate | `git checkout -- file` or `git restore file` |
| Staged too much | `git restore --staged file` |
| Last commit message wrong | `git commit --amend` (only if not pushed) |
| Need a throwaway experiment | new branch; delete later |

Never rewrite history that others already pulled unless your team agrees.

## Exercise

```bash
mkdir git-practice && cd git-practice
git init
echo "v1" > readme.txt && git add readme.txt && git commit -m "add readme"
echo "v2" >> readme.txt && git commit -am "note v2"
git switch -c experiment
echo "spike" > spike.txt && git add spike.txt && git commit -m "try spike"
git switch main
git merge experiment
git log --oneline --graph
```

## Next

Use Git on every course project. Pair with [Linux shell](/blog/2026/07/10/getting-started-with-linux-shell/) so `git` and the terminal feel like one tool.
