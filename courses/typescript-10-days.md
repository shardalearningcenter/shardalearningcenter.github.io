---
layout: course
title: "TypeScript in 10 Days — Hands-On"
permalink: /courses/typescript-10-days/
course_track: "TypeScript"
description: "Typed JavaScript for real apps: types, modules, async, and a small API client."
toc:
  - id: "day-1-types-variables"
    label: "Day 1: Types & variables"
  - id: "day-2-interfaces-objects"
    label: "Day 2: Interfaces & objects"
  - id: "day-3-functions-unions"
    label: "Day 3: Functions & unions"
  - id: "day-4-arrays-generics"
    label: "Day 4: Arrays & generics"
  - id: "day-5-modules"
    label: "Day 5: Modules"
  - id: "day-6-async-fetch"
    label: "Day 6: Async & fetch"
  - id: "day-7-classes-oop-lite"
    label: "Day 7: Classes & OOP lite"
  - id: "day-8-utility-types"
    label: "Day 8: Utility types"
  - id: "day-9-strict-mode-habits"
    label: "Day 9: Strict mode habits"
  - id: "day-10-mini-cli-tool"
    label: "Day 10: Mini CLI tool"
  - id: "capstone"
    label: "Capstone project"
---

# TypeScript in 10 Days — Hands-On

Typed JavaScript for real apps: types, modules, async, and a small API client.

## Why this language
{: #why-this-language }

TypeScript is the default for serious frontend and Node backends. Types catch bugs before runtime and make refactors safe.

## Setup (Day 0)
{: #setup-day-0 }

```bash
node -v          # 18+
npm init -y
npm i -D typescript tsx @types/node
npx tsc --init
```
Create `src/day01.ts` and run with `npx tsx src/day01.ts`.

---

## Day 1: Types & variables
{: #day-1-types-variables }

### What you'll learn

- `string`/`number`/`boolean`
- Type annotations
- `const` vs `let`

### Code along

```ts
const name: string = "Ada";
let score: number = 42;
console.log(`${name} scored ${score}`);
```

### Your task

Make a `Person` type with `name` and `age`, print a greeting.

**Pro tip:** Prefer `const` until you need reassignment.

---

## Day 2: Interfaces & objects
{: #day-2-interfaces-objects }

### What you'll learn

- `interface`
- Optional props
- Readonly

### Code along

```ts
interface User { id: number; email: string; active?: boolean }
const u: User = { id: 1, email: "a@b.com" };
console.log(u.email);
```

### Your task

Model a `BlogPost` with title, tags[], and optional publishedAt.

---

## Day 3: Functions & unions
{: #day-3-functions-unions }

### What you'll learn

- Param/return types
- Union types
- Type narrowing

### Code along

```ts
type Id = string | number;
function label(id: Id): string {
  return typeof id === "string" ? id.toUpperCase() : `N${id}`;
}
console.log(label(7), label("abc"));
```

### Your task

Write `parseStatus(s: string): "ok" | "err"` that validates input.

---

## Day 4: Arrays & generics
{: #day-4-arrays-generics }

### What you'll learn

- Typed arrays
- Generic functions
- `Record`

### Code along

```ts
function first<T>(xs: T[]): T | undefined { return xs[0]; }
console.log(first([10, 20]));
const scores: Record<string, number> = { alice: 9 };
```

### Your task

Implement `pluck<T, K extends keyof T>(rows: T[], key: K): T[K][]`.

---

## Day 5: Modules
{: #day-5-modules }

### What you'll learn

- `export`/`import`
- Default vs named
- Project layout

### Code along

```ts
// math.ts
export const add = (a: number, b: number) => a + b;

// main.ts
import { add } from "./math";
console.log(add(2, 3));
```

### Your task

Split a todo app into `types.ts`, `store.ts`, and `main.ts`.

---

## Day 6: Async & fetch
{: #day-6-async-fetch }

### What you'll learn

- `async`/`await`
- `Promise`
- Error handling

### Code along

```ts
async function getJson(url: string) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(String(res.status));
  return res.json();
}
getJson("https://httpbin.org/get").then(console.log);
```

### Your task

Fetch JSON and print one nested field; handle network errors.

---

## Day 7: Classes & OOP lite
{: #day-7-classes-oop-lite }

### What you'll learn

- Classes
- Access modifiers
- Implements

### Code along

```ts
interface Greeter { greet(): string }
class Person implements Greeter {
  constructor(private name: string) {}
  greet() { return `Hi ${this.name}`; }
}
console.log(new Person("Sam").greet());
```

### Your task

Build a `BankAccount` with deposit/withdraw and a private balance.

---

## Day 8: Utility types
{: #day-8-utility-types }

### What you'll learn

- `Partial`
- `Pick`
- `Omit`
- `Readonly`

### Code along

```ts
type User = { id: number; name: string; email: string };
type UserUpdate = Partial<Omit<User, "id">>;
const patch: UserUpdate = { email: "x@y.com" };
console.log(patch);
```

### Your task

Design create/update DTOs for a Product using utility types.

---

## Day 9: Strict mode habits
{: #day-9-strict-mode-habits }

### What you'll learn

- `strictNullChecks`
- Exhaustive switches
- Never

### Code along

```ts
type Shape = { kind: "circle"; r: number } | { kind: "square"; s: number };
function area(s: Shape): number {
  switch (s.kind) {
    case "circle": return Math.PI * s.r ** 2;
    case "square": return s.s ** 2;
  }
}
```

### Your task

Add a `triangle` variant and make the compiler force you to handle it.

---

## Day 10: Mini CLI tool
{: #day-10-mini-cli-tool }

### What you'll learn

- `process.argv`
- File I/O with `fs`
- JSON

### Code along

```ts
import fs from "node:fs";
const path = process.argv[2] ?? "data.json";
const data = JSON.parse(fs.readFileSync(path, "utf8"));
console.log(Object.keys(data));
```

### Your task

CLI that counts keys in a JSON file and writes a summary.md.


---

## Capstone project
{: #capstone }

Build a typed **URL shortener client**: types for API responses, `fetch` wrapper, CLI to create/list links, and a README with example commands.

## Related

- [Getting Started with JavaScript](/blog/2026/07/10/getting-started-with-javascript/)
- [JavaScript in 10 Days](/courses/javascript-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
