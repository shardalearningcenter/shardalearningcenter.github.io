---
layout: course
title: "Bash in 7 Days — Hands-On"
permalink: /courses/bash-7-days/
course_track: "Bash"
description: "Globs, pipes, quoting, and safe automation — learn shell scripting by triggering its classic footguns on purpose, so production never does."
toc:
  - id: "why-this-language"
    label: "Why this language"
  - id: "setup-day-0"
    label: "Setup (Day 0)"
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

Quoting bugs and unset-variable typos are the two things that make shell scripts unreliable — and both are fixable habits, not bad luck. Seven days, one script per day, one deliberate footgun per day so you recognize it instantly in production.

## Why this language
{: #why-this-language }

Every Linux server, container entrypoint, and CI job runs through a shell whether you write one line of Bash or a thousand — you can't opt out of it, so it's worth doing well. Bash's reputation for being fragile is mostly about a handful of specific habits (unquoted variables, ignoring exit codes, no `set -e`) that this course deliberately breaks on purpose so you feel the failure once and never repeat it. By Day 7 you'll write scripts that fail loudly and immediately instead of limping along with corrupted state.

## Setup (Day 0)
{: #setup-day-0 }

```bash
bash --version    # expect 5.x (macOS ships 3.2 — install a newer one via brew if so)
mkdir bash-lab && cd bash-lab
```

Every script below starts with the same header — get used to typing it:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

**Checkpoint:** save a file `day00.sh` containing just that header plus `echo "ready"`, run `chmod +x day00.sh && ./day00.sh`, and confirm it prints `ready` with exit code `0` (`echo $?` right after).

---

## Day 1: Navigation & files
{: #day-1-navigation-files }

### Why it matters

Globs (`*.txt`) and safe file operations are the first thing any script does, and the most common early bug — a glob that matches nothing — is completely silent unless you know to guard for it. Getting this right on Day 1 prevents a whole category of "the script ran but did nothing" incidents later.

### Mental model

When a glob like `*.txt` matches nothing, Bash (by default) leaves the pattern **unexpanded** — your loop variable literally becomes the string `*.txt`, not an empty list. That's why every glob loop needs an existence check (`[ -e "$f" ] || continue`) unless you've turned on `shopt -s nullglob` to make non-matching globs expand to nothing instead.

### Code along

```bash
mkdir -p out
for f in *.txt; do
    [ -e "$f" ] || continue
    cp "$f" out/
    echo "copied $f"
done
ls out
```

Set up two sample files first, then run the script above:

```bash
printf "sample a\n" > a.txt
printf "sample b\n" > b.txt
printf "not this one\n" > notes.md
```

Expected output:

```
copied a.txt
copied b.txt
a.txt
b.txt
```

### Common mistake

Deleting the `[ -e "$f" ] || continue` guard and running the loop in an empty directory (no `.txt` files at all). `*.txt` doesn't match anything, so `f` becomes the literal string `*.txt`, and `cp "*.txt" out/` fails with `cp: cannot stat '*.txt': No such file or directory` — a real error, but a confusing one, because it looks like a copy bug when the actual problem is an unguarded glob that never matched a real file.

### Your task

Extend the script to also write a manifest: after copying, create `out/manifest.txt` listing one copied filename per line, and print the total count copied.

**Check:** with the two sample files above, `out/manifest.txt` contains exactly `a.txt` and `b.txt` (one per line), and the script prints `Copied 2 file(s)`.

---

## Day 2: Variables & quoting
{: #day-2-variables-quoting }

### Why it matters

Unquoted variables are the single most common source of "works on my machine, breaks on a filename with a space" bugs in shell scripts. Seeing word-splitting happen on purpose, once, makes the `"$var"` habit permanent.

### Mental model

`$var` unquoted goes through **word splitting** (on spaces/tabs/newlines) and **glob expansion** *after* substitution — so a variable holding `"Ada Lovelace"` unquoted becomes two separate words to whatever command receives it. `"$var"` quoted is always exactly one word, no matter what's inside it. Arrays follow the same rule: `"${arr[@]}"` (quoted) preserves each element as one word each; `${arr[@]}` (unquoted) re-splits every element on whitespace.

### Code along

```bash
name="Ada Lovelace"
printf 'quoted:   [%s]\n' "$name"
printf 'unquoted: [%s]\n' $name
```

Expected output:

```
quoted:   [Ada Lovelace]
unquoted: [Ada]
unquoted: [Lovelace]
```

(`printf` repeats its format string for every remaining argument — the unquoted `$name` arrived as *two* arguments, `Ada` and `Lovelace`, so the format line printed twice.)

```bash
files=(a.txt b.txt "with space.txt")
echo "${files[0]}"
echo "${#files[@]}"
for f in "${files[@]}"; do
    echo "file: $f"
done
```

Expected output: `a.txt`, then `3`, then three `file: ...` lines, the last one reading `file: with space.txt` as a single line.

### Common mistake

Writing the loop as `for f in ${files[@]}; do` (no quotes around the array expansion). `"with space.txt"` — one array element — gets word-split back into two loop iterations, `with` and `space.txt`, silently turning a 3-element array into a 4-iteration loop. This is the exact same bug as the `printf` example above, just inside a `for` instead — always quote `"${arr[@]}"`.

### Your task

Write a script that takes a name as `$1`, and if it's missing, prints `usage: greet.sh <name>` to stderr and exits `1` without printing a greeting.

**Check:** `./greet.sh` (no args) prints the usage line to stderr and `echo $?` afterward shows `1`; `./greet.sh "Ada Lovelace"` prints `Hello, Ada Lovelace!` as one line, proving `"$1"` was quoted correctly through the whole script.

---

## Day 3: Pipes & filters
{: #day-3-pipes-filters }

### Why it matters

`sort | uniq -c | sort -rn | head` is one of the most-repeated pipelines in operations work — "what are the top N things in this log file" — and once you've built it by hand once, you'll recognize the shape everywhere.

### Mental model

`uniq -c` only collapses **adjacent** duplicate lines — it has no idea two non-adjacent lines are "the same," which is exactly why it always comes after `sort`, never before. Each stage of a pipeline runs concurrently on the *stream*, not sequentially on a fully-materialized result — that's what makes pipelines fast even on huge files, but it also means every stage needs the sort order it expects to already be true when data reaches it.

### Code along

```bash
cat <<'EOF' > access.log
10.0.0.1 GET /home
10.0.0.2 GET /about
10.0.0.1 GET /home
10.0.0.3 GET /contact
10.0.0.1 GET /pricing
10.0.0.2 GET /home
EOF

awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -3
```

Expected output (leading whitespace before the counts is normal `uniq -c` padding and may vary slightly by system — the numbers and order won't):

```
3 10.0.0.1
2 10.0.0.2
1 10.0.0.3
```

### Common mistake

Skipping the middle `sort` and running `awk '{print $1}' access.log | uniq -c` directly. `10.0.0.1` appears on lines 1, 3, and 5 — not adjacent to each other — so `uniq -c` only merges immediate neighbors and reports six separate `1 <ip>` rows instead of three correctly-merged counts. The output looks plausible (it's not an error, just wrong), which is what makes this bug dangerous: nothing crashes, the numbers are just silently incorrect.

### Your task

Using `cut -d' ' -f3` (the requested path, third field) instead of `$1`, find the single most-requested path in `access.log` and its count.

**Check:** the result is `3 /home` — `/home` appears on lines 1, 3, and 6.

---

## Day 4: Control flow
{: #day-4-control-flow }

### Why it matters

`if`, `for`, `while`, and `case` are how a script makes decisions instead of just running a fixed list of commands. `case` in particular replaces long `if/elif` chains for pattern-matching on a single value — file extensions, subcommands, anything with a closed set of shapes.

### Mental model

`[ ... ]` (POSIX test) and `[[ ... ]]` (Bash-only extended test) look similar but aren't identical — inside `[[ ]]`, `<` and `>` compare strings safely; inside `[ ]`, those same characters are **file redirection operators**, not comparisons, which is a classic silent trap. `case` matches patterns top-to-bottom and stops at the first match — order your patterns from most-specific to the catch-all `*)`.

### Code along

```bash
printf "Hello\n" > a.md
printf "Hi\n" > b.md

for f in *.md; do
    if [ -f "$f" ]; then
        size=$(wc -c < "$f")
        echo "$f: $size bytes"
    fi
done
```

Expected output:

```
a.md: 6 bytes
b.md: 3 bytes
```

```bash
classify() {
    case "$1" in
        *.md)  echo "markdown" ;;
        *.txt) echo "text" ;;
        *)     echo "unknown" ;;
    esac
}
classify a.md
classify a.txt
classify a.bin
```

Expected output: `markdown`, `text`, `unknown`.

### Common mistake

Writing `if [ "$size" > 100 ]` to check whether a file is larger than 100 bytes. Inside single `[ ]`, `>` is **file redirection**, not "greater than" — this silently creates (or truncates) a file literally named `100` in the current directory, and the condition itself almost always evaluates true regardless of `$size`'s value, because `[ "$size" ]` alone (ignoring the redirection) just checks "is this string non-empty." The fix is `[ "$size" -gt 100 ]` for numeric comparison inside `[ ]`, or switch to `[[ "$size" > 100 ]]` — which does do string comparison correctly, but still isn't the numeric check you want here.

### Your task

Write a `while read` loop over `access.log` (from Day 3) that counts how many lines contain `/home`, using `[[ "$line" == *"/home"* ]]` inside the loop body.

**Check:** the count printed is `3` — lines 1, 3, and 6 of `access.log` contain `/home`.

---

## Day 5: Functions & set -euo
{: #day-5-functions-set-euo }

### Why it matters

`set -euo pipefail` turns Bash from "keep going and hope" into "stop the instant something's wrong" — and functions like `die`/`need_cmd` are the standard pattern for failing with a clear message instead of a cryptic one three commands later.

### Mental model

`-e` exits on any command's non-zero exit status (with exceptions: conditions in `if`/`while`/`&&`/`||` are allowed to "fail" without triggering it — that's the whole point of a condition). `-u` turns referencing an *unset* variable into a hard error instead of silently substituting an empty string. `-o pipefail` makes a pipeline's exit status the *last non-zero* status among all its stages, not just the final command's — without it, `false | true` reports success, hiding a real failure upstream.

### Code along

```bash
#!/usr/bin/env bash
set -euo pipefail

die() { echo "error: $*" >&2; exit 1; }
need_cmd() { command -v "$1" >/dev/null 2>&1 || die "missing required command: $1"; }

tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT

need_cmd bash
need_cmd curl
echo "working in $tmpfile" > "$tmpfile"
cat "$tmpfile"
need_cmd nonexistent-tool-xyz
echo "all good"   # never reached
```

Expected output:

```
working in /tmp/tmp.XXXXXXXXXX
error: missing required command: nonexistent-tool-xyz
```

The script exits `1` right after the error line — `echo "all good"` never runs — and the temp file is gone afterward (`trap ... EXIT` ran during the `die`'s `exit 1`, not just on a clean exit).

### Common mistake

Assuming `set -u` will catch every unset variable everywhere, including inside a default-value expansion like `${MAYBE_UNSET:-fallback}`. That specific syntax is designed to be safe *even with `-u` on* — it's the correct way to give a variable a default without tripping the strict-mode check. The actual trap is the opposite direction: forgetting `-u` entirely on an older script and having a typo'd variable name (`$HOEM` instead of `$HOME`) silently evaluate to an empty string instead of erroring — `rm -rf "$HOEM/cache"` with an unset, empty `$HOEM` becomes `rm -rf /cache`, not a no-op. `set -u` exists specifically to turn that into an immediate `bash: HOEM: unbound variable` instead.

### Your task

Add a `need_cmd jq` call before `need_cmd nonexistent-tool-xyz`, and reorder so all `need_cmd` checks run *before* any real work — confirm the script now fails fast on the first missing dependency without writing to `$tmpfile` at all.

**Check:** if `jq` is installed but `nonexistent-tool-xyz` isn't, the script still fails on the fake tool with the same `error: missing required command: nonexistent-tool-xyz` message, and `tmpfile`'s content-writing line never executes (add a `echo unreachable-marker` right after it to confirm — that marker should never print).

---

## Day 6: JSON & HTTP
{: #day-6-json-http }

### Why it matters

Shell scripts talk to HTTP APIs constantly in CI and ops tooling, and `curl | jq` is the standard combination for "fetch JSON, pull one field out of it." Getting the flags right (`-s`, `-f`, `-r`) is what separates a script that fails loudly from one that silently writes garbage.

### Mental model

`curl -s` suppresses the progress meter (not errors); `curl -f` makes curl itself return a non-zero exit code on HTTP 4xx/5xx instead of printing the error page's body as if it were your data — without `-f`, a broken endpoint looks like a successful response containing HTML. `jq -r` outputs a JSON string's raw text; without `-r`, you get the value still wrapped in quotes (valid JSON, wrong for anything expecting plain text).

### Code along

```bash
curl -sf https://httpbin.org/uuid | jq -r .uuid
```

Expected output: a bare UUID like `3fa85f64-5717-4562-b3fc-2c963f66afa6` (the exact value differs every run — check the *shape*, not the value: `grep -Eq '^[0-9a-f-]{36}$'`).

### Common mistake

Dropping `-r` and running `curl -sf https://httpbin.org/uuid | jq .uuid > id.txt`. `id.txt` ends up containing `"3fa85f64-5717-4562-b3fc-2c963f66afa6"` — with the quote characters literally in the file — because `jq` without `-r` always prints valid *JSON*, and a JSON string is quoted by definition. Anything downstream expecting a bare UUID (a filename, a URL path segment, a comparison against a plain string) breaks in a confusing way, because the value *looks* right when you `cat` it but comparisons like `[ "$id" == "$expected" ]` silently fail.

### Your task

Write a script that fetches the UUID, writes it to `id.txt`, and fails with a clear stderr message and exit `1` if the response is empty or doesn't match a UUID shape (use the `grep -Eq` check from above).

**Check:** on success, `cat id.txt` shows exactly one line matching `^[0-9a-f-]{36}$`; temporarily pointing the script at a bad URL (like `https://httpbin.org/status/500`) makes it print a clear error to stderr and exit `1` instead of writing a bad `id.txt`.

---

## Day 7: Real automation
{: #day-7-real-automation }

### Why it matters

A script that's safe to run twice (or a hundred times, from cron, unattended) is what "automation" actually means — a one-off script you have to remember to run carefully is just a chore with extra syntax. Idempotency and logging are what separate the two.

### Mental model

**Idempotent** means "running it again, with no new input, produces no new effect" — a backup script that logs `"nothing new, skipping"` on a second run (because nothing changed) is idempotent; one that blindly re-copies everything every time is wasteful but at least not *wrong*. A naive timestamp check (`[ "$src" -nt "$marker" ]`) only tells you a directory's own entries changed (something added or removed directly inside it) — it does **not** detect a file's *contents* changing in place, which is why production tools like `rsync -a` compare each file's own mtime/size, not just the containing directory's.

### Code along

```bash
log() { printf '%s %s\n' "$(date -Is)" "$*"; }

backup() {
    local src=$1 dst=$2
    mkdir -p "$dst"
    if [ ! -e "$dst/.last_backup" ] || [ "$src" -nt "$dst/.last_backup" ]; then
        log "backing up $src -> $dst"
        cp -a "$src"/. "$dst"/
        touch "$dst/.last_backup"
    else
        log "nothing new, skipping"
    fi
}

mkdir -p data && echo "v1" > data/file.txt
backup data backup
backup data backup   # run again immediately, nothing changed
```

Expected output (timestamps will differ on your machine):

```
2026-07-10T12:00:00+00:00 backing up data -> backup
2026-07-10T12:00:00+00:00 nothing new, skipping
```

### Common mistake

Running `backup` a *third* time right after touching a new file inside `data/` (`touch data/new.txt`) and expecting the "nothing new" branch — but `mkdir -p "$dst"` was only called once implicitly at the top, and if `$dst` (`backup/`) already existed from the first run without a trailing `.last_backup` check being current, the naive `-nt` comparison against the *directory's* mtime does correctly catch a newly added file (directory mtime changes on add/remove) — but would **not** catch `echo "v2" > data/file.txt` overwriting existing content in place, since that only changes `file.txt`'s own mtime, not `data/`'s. Test both cases yourself: add a file (detected) versus edit an existing file's content (missed) — this gap is exactly why real backup tools don't rely on directory timestamps alone.

### Your task

Fix the idempotency gap: change the check to compare **every file's** mtime against the marker (`find "$src" -newer "$dst/.last_backup" -print -quit` — prints one path if anything is newer, nothing otherwise) instead of just the directory's own timestamp.

**Check:** after the fixed script's first two runs (matching the log output above), run `echo "v2" > data/file.txt` then `backup data backup` a third time — it now logs `backing up data -> backup` again, correctly detecting the in-place content change that the naive version above would have missed.

---

## Capstone project
{: #capstone }

Write a **project bootstrap script** (`bootstrap.sh`) you'd actually hand a new teammate on day one:

- `set -euo pipefail` at the top, `die`/`need_cmd` helpers from Day 5.
- Checks for `git`, `curl`, and `jq` up front — fails fast, before creating anything, if any are missing.
- Creates a standard directory layout (`src/`, `tests/`, `docs/`) idempotently — `mkdir -p`, so re-running never errors on "already exists."
- Writes a `.env.example` file only if one doesn't already exist (never overwrites a teammate's real `.env` if they accidentally point the script at it).
- Logs every step with the Day 7 `log()` helper, and prints a final "Next steps" block listing 2–3 concrete commands to run next.

**Acceptance check:** running `./bootstrap.sh` twice in a row is silent-safe — the second run makes zero changes (no errors, no duplicate content in `.env.example`), and `echo $?` is `0` both times. Deleting one directory (say `tests/`) and running a third time recreates only that directory, leaving the others untouched.

## Related

- [Getting Started with Linux Shell](/blog/2026/07/10/getting-started-with-linux-shell/)
- [Docker getting started](/blog/2026/07/10/getting-started-with-docker/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
