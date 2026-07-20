# Docs rewrite plan — kill the AI slop

**Site:** `shaardalearningcenter.github.io`  
**Goal:** Every public doc should read like a careful teacher (Karpathy / Cloud docs), not a generated outline.

## What’s wrong now

| Symptom | Example |
|---------|---------|
| Outline pretending to be a lesson | 4 short sections, no worked failure |
| Bullet lists with no “why” | “Learn ownership” with 8 lines of code |
| Marketing filler | “most practical”, “master”, “journey” |
| Duplicate titles / thin exercises | “Write one sentence…” with no check |
| Same skeleton every page | learn → code → task, zero depth |

## Quality bar (non-negotiable)

Every lesson/article must include:

1. **One clear claim** in the first screen (what you will be able to do).
2. **Mental model** — diagram-in-words or numbered steps; not vibes.
3. **Worked example** — full code that runs; shapes/types called out.
4. **Failure mode** — what breaks, how you see it, how you fix it.
5. **Exercise with a check** — concrete output or test, not “try it.”
6. **No filler** — ban: “in today’s world”, “powerful tool”, “dive deep”, “leverage”, “robust”, “seamless”, “unlock”.

**Length targets**

- LLM Mastery article: ~800–1,800 words (or equivalent code+prose density).
- Language day: ~400–800 words with 1–2 runnable snippets + debug note.
- Getting-started blog: ~600–1,200 words; one mini-project end-to-end.

**Voice:** Direct, slightly opinionated, first-principles. Prefer “do this / don’t do that” over adjectives.

## Priority order

| Phase | Scope | Why first |
|------:|-------|-----------|
| **P0** | LLM Mastery hub + articles **01–10** | Foundations; most linked |
| **P1** | LLM Mastery **11–27** (neural → tiny GPT) | Core of the course |
| **P2** | LLM Mastery **28–50** (systems → capstone) | Completes the path |
| **P3** | Language tracks (TS/JS/Rust/Go/Java first, then rest) | High traffic hub |
| **P4** | Getting-started blogs (8) | Entry points from Google |
| **P5** | Older bootcamps (Python/LLM/Go) — strip emoji, rewrite modules | Legacy pages |

## Execution method

1. Keep permalinks and TOC ids stable where possible (SEO).
2. Rewrite bodies in `courses/llm-mastery/*.md` and language course files.
3. Update generators only after content quality is proven (generators must not re-slop).
4. Publish in commits per phase so the live site improves continuously.

## Progress

| Phase | Status |
|------|--------|
| P0 LLM 01–10 | Done (rewritten in depth) |
| P1 LLM 11–27 | Done |
| P2 LLM 28–50 | Done |
| P3 Language tracks | Done (14 courses + hub) |
| P4 Getting-started blogs | Done (8 + 2 announcements) |
| P5 Legacy bootcamps (emoji pages) | Pending — next pass |

Generators `generate_llm_mastery.py` and `generate_language_tutorials.py` now **refuse to run** so they cannot overwrite hand-written docs.
