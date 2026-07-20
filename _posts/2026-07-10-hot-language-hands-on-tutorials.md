---
layout: post
title: "Hot language hands-on tutorials (TypeScript, Rust, Go, and more)"
date: 2026-07-10
description: "Multi-day hands-on courses for the languages teams actually hire for, each with a daily task and a capstone — plus SQL, Zig, and Bash."
tags: [languages, tutorials, getting-started]
---

We published a full **[Languages hub](/courses/languages/)** with hands-on, day-by-day sprints — not reference manuals you skim once and forget, but courses built around a task you complete each day.

## What "hands-on" actually means

Every course in the hub follows the same structure: a short code-along that introduces the day's concept, a concrete task you complete yourself using that concept, and a capstone project at the end that forces you to combine everything from the earlier days. There's no day that's just "read about generics" with nothing to run afterward — if a day doesn't produce code you executed and checked, it's not in the course.

As an example, [Go in 10 Days](/courses/go-10-days/) spends day one on goroutines and channels conceptually, then has you build a small concurrent worker pool that fetches a list of URLs in parallel and reports which ones failed — a task that only "works" if you actually understood the concurrency primitives, not just read about them.

## The full list

- [TypeScript](/courses/typescript-10-days/) — 10 days
- [JavaScript](/courses/javascript-10-days/) — 10 days
- [Rust](/courses/rust-10-days/) — 10 days
- [Go](/courses/go-10-days/) — 10 days
- [Java](/courses/java-10-days/) — 10 days
- [Kotlin](/courses/kotlin-10-days/) — 10 days
- [Swift](/courses/swift-10-days/) — 10 days
- [C++](/courses/cpp-10-days/) — 10 days
- [C#](/courses/csharp-10-days/) — 10 days
- [Ruby](/courses/ruby-10-days/) — 10 days
- [PHP](/courses/php-10-days/) — 10 days
- [SQL](/courses/sql-10-days/) — 10 days
- [Zig](/courses/zig-7-days/) — 7 days
- [Bash](/courses/bash-7-days/) — 7 days
- [Python in 10 Days](/courses/python-10-days/) — already on the site

## How to actually pick one

Don't pick based on hype alone — match the language to what you're trying to build next:

| If you're aiming at | Start with |
|---|---|
| Frontend or full-stack web work | TypeScript, then JavaScript if you skipped it |
| Systems, performance-critical services | Rust or Go |
| Backend services at a large company | Java, Kotlin, or C# |
| iOS/macOS apps | Swift |
| Data plumbing, scripting, gluing tools together | Bash, SQL |
| Embedded or resource-constrained targets | Zig or C++ |

If you genuinely don't know, Go or TypeScript are the safest defaults — both have large hiring markets, both are approachable in under two weeks, and both show up constantly in the backend/frontend split that most teams use.

## Common footguns when learning a new language this way

- **Course-hopping instead of finishing** — starting three 10-day courses in the same week means finishing none of them; the daily tasks build on each other, and losing the thread halfway through is worse than not starting.
- **Copy-pasting the code-along instead of typing it** — you'll pass the day's task without understanding it, then stall on the capstone, which deliberately doesn't hand you the pattern.
- **Skipping the capstone** — it's the only part of each course that tests whether you can combine ideas from multiple days, which is the actual skill you're building, not any single day's syntax.
- **Treating 10 days as "fluent"** — these courses get you to "can read the language, can build something small and working, knows where to look next." That's the honest bar; real fluency takes shipping real code over months, not a sprint.
- **Ignoring the language's own tooling** — every course leans on the language's standard formatter/linter/test runner (`gofmt`, `cargo test`, `rustfmt`, etc.) rather than fighting it; skipping that step means fighting style debates with yourself for months afterward.

## You know a course is actually done when…

- [ ] You completed the capstone without re-reading the day-by-day code-alongs from scratch
- [ ] You can write the "hello world" equivalent from memory, with correct syntax, no lookup
- [ ] You know the language's standard way to run tests and format code, and have actually run both at least once
- [ ] You can explain the one or two concepts that felt hardest on day one, in your own words, without the course's explanation in front of you
- [ ] You've pushed the capstone to a Git repo — see [Getting Started with Git](/2026/07/10/getting-started-with-git/) if that step itself is the unfamiliar part

Each course has daily code-alongs, a concrete task, and a capstone. Start at the [hub](/courses/languages/) and pick one language this week.
