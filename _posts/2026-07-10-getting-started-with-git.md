---
layout: post
title: "Getting Started with Git (without the fear)"
date: 2026-07-10
description: "Five daily commands, a clear mental model, and a real merge conflict you create and resolve yourself — enough Git to stop being afraid of it."
tags: [git, getting-started]
---

Git is a time machine for your files. Most "Git anxiety" comes from never having deliberately broken something and fixed it. This post has you create a real merge conflict on purpose, resolve it, and confirm the history is sane — because that's the moment Git stops feeling like magic.

## Install and one-time setup

```bash
git --version
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

Skip the global config and your commits show up anonymously as whatever your OS username happens to be — annoying to fix retroactively across dozens of commits.

## Daily driver

```bash
git status                 # where am I?
git add -p                 # stage hunks intentionally, not blindly
git commit -m "message"    # snapshot with a why
git log --oneline -10      # recent history
git diff                   # unstaged changes
git diff --staged          # what will actually be committed
```

Commit messages: say **why**, not "update files." Future-you (and reviewers) need the reason, not a restatement of the diff.

## Mental model

```
working tree  →  staging area  →  commit (immutable snapshot)
     edit            git add           git commit
```

- A **branch** is a movable label pointing at a commit — nothing more exotic than that.
- `main` is a convention, not a special object; Git doesn't know it's "the important one."
- Remotes (`origin`) are other copies of the same commit graph, not a separate system.

## Mini project: create a merge conflict, then resolve it

Tutorials that avoid conflicts teach you to fear them. Do this instead — it's the single most useful 5 minutes you can spend learning Git.

```bash
mkdir git-practice && cd git-practice
git init -b main
echo "Headline: draft" > readme.txt
git add readme.txt
git commit -m "add readme with draft headline"

git switch -c feature-headline
echo "Headline: Hello World" > readme.txt
git commit -am "feature: rewrite headline for launch"

git switch main
echo "Headline: Welcome Friends" > readme.txt
git commit -am "main: rewrite headline for homepage"

git merge feature-headline
```

Git stops and reports `CONFLICT (content): Merge conflict in readme.txt`. Open the file — it now looks like this:

```
<<<<<<< HEAD
Headline: Welcome Friends
=======
Headline: Hello World
>>>>>>> feature-headline
```

Everything between `<<<<<<<` and `=======` is your current branch (`HEAD`); everything between `=======` and `>>>>>>>` is the branch you're merging in. Resolve it by editing the file down to what you actually want — say, `Headline: Welcome Friends (Hello World!)` — deleting the marker lines, then:

```bash
git add readme.txt
git commit --no-edit          # finishes the merge commit
git log --oneline --graph --all
```

The graph should show two branches converging into one merge commit. You created the exact situation every team hits weekly, and fixed it without panic.

## Undo without panic

| Situation | Safe move |
|-----------|-----------|
| Unstaged edits you hate | `git restore file` |
| Staged too much | `git restore --staged file` |
| Last commit message wrong | `git commit --amend` (only if not pushed) |
| Need a throwaway experiment | new branch; delete it later |
| "I think I deleted a commit" | `git reflog` — find the old `HEAD` position, then `git switch -c rescue-branch <sha>` |

`git reflog` is your safety net: Git keeps a log of where `HEAD` has pointed, even across resets and rebases, for about 90 days by default. Almost nothing is truly lost immediately.

## Common footguns

- **Force-pushing shared branches** — `git push --force` overwrites history your teammates already pulled. Use `--force-with-lease` if you must, and only on branches you own.
- **Detached HEAD confusion** — `git checkout <sha>` (not a branch) puts you in detached HEAD. Commits there are orphaned unless you `git switch -c <name>` before leaving.
- **Committing secrets or large binaries** — they live in history forever unless you rewrite it (`git filter-repo`), which is painful. `.gitignore` them before the first commit, not after.
- **Rebasing after pushing** — rewrites commit SHAs your collaborators already have, forcing them into confusing conflicts. Rebase local, unpublished work only.
- **`.gitignore` added too late** — adding a pattern doesn't untrack files already committed; you also need `git rm --cached <file>`.

## You know you're done when…

- [ ] `git log --oneline --graph --all` shows both branches merging into a single history
- [ ] You deliberately created and resolved a real merge conflict, not just avoided one
- [ ] `git status` is clean before you switch branches (no surprise stashing later)
- [ ] You can find a "lost" commit with `git reflog` without googling the command
- [ ] `user.name` / `user.email` are configured, so your commits aren't anonymous

## Next

Use Git on every course project. Pair with [Getting Started with the Linux Shell](/2026/07/10/getting-started-with-linux-shell/) so `git` and the terminal feel like one tool.
