---
layout: post
title: "Getting Started with the Linux Shell"
date: 2026-07-10
description: "pwd, pipes, and permissions — then generate a fake access log and build a real analysis pipeline against it, footguns included."
tags: [linux, shell, getting-started]
---

The shell is how you talk to the machine without a mouse. Every serious ML and backend workflow eventually lands here: datasets, logs, Docker, SSH, CI. This post ends with you generating fake log data and writing pipelines that answer real questions about it — the same shape of work you'll do against production logs.

## Survival kit

```bash
pwd                 # where am I?
ls -la               # what is here, including dotfiles?
cd path              # move
mkdir -p a/b         # create nested dirs in one shot
cp src dst && mv old new
rm -i file           # interactive delete (safer while learning)
less file            # paginated view, quit with q
head -n 20 file
tail -f log.txt      # follow a growing log
```

Find and search:

```bash
grep -n "ERROR" app.log
grep -R "TODO" . --include="*.py"
find . -name "*.csv"
```

Two habits worth building immediately: use `Tab` for completion (fewer typos, faster) and `Ctrl+R` to search command history instead of retyping. `man <command>` or `<command> --help` beats guessing flags from memory.

## Pipes, redirection, and exit codes

Programs read stdin and write stdout; chaining them is the entire philosophy of the shell:

```bash
cat access.log | grep " 500 " | awk '{print $1}' | sort | uniq -c | sort -nr | head
```

| Operator | Meaning |
|----------|---------|
| `\|` | pipe stdout → next command's stdin |
| `>` | overwrite file |
| `>>` | append |
| `2>` | redirect stderr |
| `&&` | run next command only if previous succeeded |
| `;` | run next command regardless |

Every command leaves an **exit code** in `$?` — `0` means success, anything else means failure. Scripts that ignore this silently continue after real errors.

```bash
grep "ERROR" app.log
echo $?              # 0 if found, 1 if not found, 2 if app.log doesn't exist
```

## Paths, permissions, and the environment

- `.` current dir, `..` parent, `~` home
- `chmod +x script.sh && ./script.sh` — the executable bit, not the file extension, controls whether it runs
- `chmod 644 file` (owner read/write, everyone else read) vs `chmod 600` (owner-only) — numeric modes are `owner-group-other`, each digit a sum of read(4)+write(2)+execute(1)
- `echo $PATH` — the ordered list of directories the shell searches for commands; `which python3` tells you exactly which binary will run, which matters when you have both a system Python and a venv Python

## Mini project: build a log analysis pipeline

Generate a synthetic access log with real (pseudo-random) variation, then answer three questions about it with pipelines — no sample output is given here on purpose; you run it and read your own numbers.

```bash
for i in $(seq 1 40); do
  ip="10.0.0.$(( RANDOM % 5 + 1 ))"
  if (( RANDOM % 5 == 0 )); then status=500; else status=200; fi
  echo "$ip GET /page$(( RANDOM % 4 )) $status"
done > toy.log

wc -l toy.log                                                   # should print 40
```

Now answer three questions:

```bash
# 1. Which IP hit the server most?
awk '{print $1}' toy.log | sort | uniq -c | sort -nr | head -5

# 2. What's the status code breakdown?
awk '{print $3}' toy.log | sort | uniq -c

# 3. How many 500s happened total?
grep -c " 500$" toy.log
```

Re-run the generator loop and the pipelines again — because it uses `$RANDOM`, your numbers will differ each time, which is the point: you're checking that the *pipeline logic* is correct, not memorizing one output. Cross-check by hand: add up the counts from question 2 and confirm they sum to 40.

## Common footguns

- **Unquoted variables** — `rm -rf $DIR/*` silently becomes `rm -rf /*` if `$DIR` is empty or unset. Always quote: `rm -rf "$DIR"/*`, and set `set -u` in scripts to error on unset variables.
- **Parsing `ls` output** — filenames with spaces or newlines break naive `for f in $(ls)` loops. Use `find . -print0 | xargs -0` or a glob (`for f in *.csv`) instead.
- **Forgetting `set -e`** — without it, a failing command in a script doesn't stop the script; later commands run against a broken state.
- **`source script.sh` vs `./script.sh`** — sourcing runs in your *current* shell (env var changes persist); executing runs in a subshell (they don't). Mixing these up is why "but I exported it!" doesn't always work.
- **Trusting PATH order blindly** — `which python3` before debugging "wrong version" complaints; a stale `/usr/local/bin` entry ahead of your venv is a classic trap.

## You know you're done when…

- [ ] `toy.log` contains exactly 40 lines after the generator loop
- [ ] All three analysis pipelines run with no errors and the status-code counts sum to 40
- [ ] You can explain why `rm -rf "$DIR"/*` (quoted) is safer than the unquoted version
- [ ] `echo $?` immediately after a command tells you pass/fail without re-running anything
- [ ] `which <command>` points to the binary you actually expect

## Next

[Getting Started with Docker](/2026/07/10/getting-started-with-docker/) packages the environment you just learned to navigate. [Getting Started with Git](/2026/07/10/getting-started-with-git/) version-controls the scripts you write in the shell.
