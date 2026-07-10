---
layout: course
title: "TypeScript in 10 Days — Hands-On"
permalink: /courses/typescript-10-days/
course_track: "TypeScript"
description: "Typed JavaScript for real apps: types, narrowing, modules, async, and a small typed HTTP client you build and test yourself."
toc:
  - id: "why-this-language"
    label: "Why this language"
  - id: "setup-day-0"
    label: "Setup (Day 0)"
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

Typed JavaScript for real apps. Every day compiles, runs, and prints something you can check against an expected value — no hand-waving.

## Why this language
{: #why-this-language }

TypeScript is the default for serious frontend and Node backends in 2026. The type checker is not decoration — it turns a category of runtime crashes (`undefined is not a function`, wrong field names, `null` sneaking through) into compile-time errors you fix before you ship. The payoff compounds: refactors that would be terrifying in plain JavaScript become "change the type, follow the red squiggles" in TypeScript. That's the entire pitch, and it's why almost every serious JS codebase adopted it.

## Setup (Day 0)
{: #setup-day-0 }

You need Node 18+ (for built-in `fetch`) and a TypeScript toolchain. No bundler, no framework — just the compiler and a runner.

```bash
node -v                       # expect v18.x or higher
mkdir ts-lab && cd ts-lab
npm init -y
npm i -D typescript tsx @types/node
npx tsc --init --strict --target ES2022 --module NodeNext --moduleResolution NodeNext
```

Verify the install:

```bash
npx tsc -v                    # Version 5.x
npx tsx -e 'console.log(1 + 1)'   # prints 2
```

Create `src/day01.ts`, run it with `npx tsx src/day01.ts`. Every day below assumes that pattern — one file per day, `npx tsx src/dayNN.ts` to run it, `npx tsc --noEmit` to type-check the whole project without emitting `.js` files.

**Checkpoint:** if `npx tsc -v` fails with "command not found," the local install didn't happen — re-run `npm i -D typescript` from inside `ts-lab`, don't install it globally (versions drift between projects if you do).

---

## Day 1: Types & variables
{: #day-1-types-variables }

### Why this matters

TypeScript's type checker only helps you if you give it something to check. Annotations on function boundaries and object shapes are how you communicate intent to both the compiler and the next person reading your code — usually you, in six months.

### Mental model

The compiler infers types from values whenever it can (`let x = 5` is already `number`), so you annotate where inference can't reach: function parameters, and any variable declared before it's assigned a value. Over-annotating obvious locals (`const name: string = "Ada"`) is noise; TypeScript already knows.

### Code along

```ts
// src/day01.ts
type Person = { name: string; age: number };

function describe(p: Person): string {
  return `${p.name} is ${p.age} years old`;
}

const people: Person[] = [
  { name: "Ada", age: 30 },
  { name: "Grace", age: 45 },
];

for (const person of people) {
  console.log(describe(person));
}

const total = people.reduce((sum, p) => sum + p.age, 0);
console.log(`Total age: ${total}`);
```

Run it:

```bash
npx tsx src/day01.ts
# Ada is 30 years old
# Grace is 45 years old
# Total age: 75
```

### Common mistake

Writing `let score: number;` and using `score` before assignment. Under `strict` mode (which you enabled in setup), this is a compile error: `Variable 'score' is used before being assigned`. TypeScript is protecting you from a real JavaScript bug — reading `undefined` where you expected a number, then getting `NaN` three functions downstream with no idea why. Fix it by assigning a value at declaration or giving it a definite-assignment check only if you're certain (`score!`), which you should almost never need as a beginner.

### Your task

Add a third person to the `people` array, then write a function `oldest(people: Person[]): Person` that returns whoever has the highest `age`. Print the result.

**Check:** running the script prints `Grace is 45 years old` (or whichever name you gave the oldest age) as the last line, with no compiler errors from `npx tsc --noEmit`.

---

## Day 2: Interfaces & objects
{: #day-2-interfaces-objects }

### Why this matters

Real data — API responses, config, form input — arrives as objects with some fields required and some optional. `interface` is how you name that shape once and reuse it everywhere, instead of re-describing the same object in five function signatures and letting them drift apart.

### Mental model

TypeScript uses **structural typing**: an object satisfies an interface if it has the right shape, regardless of how it was constructed. There's no `implements` requirement for plain objects. `readonly` blocks reassignment of a property after creation — it does not deep-freeze nested objects.

### Code along

```ts
// src/day02.ts
interface BlogPost {
  readonly id: number;
  title: string;
  tags: string[];
  publishedAt?: string; // optional: ISO date string, or undefined if a draft
}

function summarize(post: BlogPost): string {
  const status = post.publishedAt ? `published ${post.publishedAt}` : "draft";
  return `#${post.id} "${post.title}" [${post.tags.join(", ")}] — ${status}`;
}

const posts: BlogPost[] = [
  { id: 1, title: "Hello TS", tags: ["intro"], publishedAt: "2026-01-05" },
  { id: 2, title: "Work in progress", tags: ["draft", "ts"] },
];

posts.forEach((p) => console.log(summarize(p)));

const drafts = posts.filter((p) => !p.publishedAt);
console.log(`Drafts: ${drafts.length}`);
```

Expected output:

```
#1 "Hello TS" [intro] — published 2026-01-05
#2 "Work in progress" [draft, ts] — draft
Drafts: 1
```

### Common mistake

Trying to mutate a `readonly` field: `posts[0].id = 99` fails to compile with `Cannot assign to 'id' because it is a read-only property`. Beginners sometimes "fix" this by removing `readonly` instead of asking whether the ID should ever change — usually it shouldn't, and the error was correct. The other classic mistake: forgetting the `?` on `publishedAt` and then writing `post.publishedAt.slice(0, 4)` everywhere, which crashes at runtime the first time a draft flows through — TypeScript would have flagged `post.publishedAt` as possibly `undefined` if you'd typed it optional and tried to call a method on it directly.

### Your task

Add a `comments: { author: string; text: string }[]` field to `BlogPost`. Write `commentCount(post: BlogPost): number` and a function `mostCommented(posts: BlogPost[]): BlogPost` (assume the array is non-empty).

**Check:** `npx tsc --noEmit` passes, and calling `mostCommented` on three posts with `[0, 3, 1]` comments respectively returns the post with 3.

---

## Day 3: Functions & unions
{: #day-3-functions-unions }

### Why this matters

Not every value has one type. An ID might be a number from your database or a string from a URL param; a parse result is either good data or an error. Union types let you say that precisely instead of lying with `any`, and **narrowing** is how the compiler proves which branch you're in.

### Mental model

A union type (`A | B`) means "one of these, you don't know which yet." Narrowing — `typeof`, `in`, equality checks, discriminant fields — is how you convince the compiler which member of the union you're holding at a given line, so it lets you use members specific to that type.

### Code along

```ts
// src/day03.ts
type Id = string | number;

function formatId(id: Id): string {
  if (typeof id === "string") {
    return id.toUpperCase();
  }
  return `N${id.toString().padStart(4, "0")}`;
}

type ParseResult =
  | { ok: true; value: number }
  | { ok: false; error: string };

function parseAge(input: string): ParseResult {
  const n = Number(input);
  if (!Number.isInteger(n) || n < 0 || n > 130) {
    return { ok: false, error: `"${input}" is not a valid age` };
  }
  return { ok: true, value: n };
}

console.log(formatId(7), formatId("abc"));

for (const input of ["42", "abc", "-5", "150"]) {
  const result = parseAge(input);
  if (result.ok) {
    console.log(`${input} -> valid: ${result.value}`);
  } else {
    console.log(`${input} -> invalid: ${result.error}`);
  }
}
```

Expected output:

```
N0007 ABC
42 -> valid: 42
abc -> invalid: "abc" is not a valid age
-5 -> invalid: "-5" is not a valid age
150 -> invalid: "150" is not a valid age
```

### Common mistake

Accessing `result.value` before checking `result.ok`. TypeScript rejects it: `Property 'value' does not exist on type '{ ok: false; error: string }'`. This looks annoying the first time, then becomes the exact reason you never ship a `Cannot read properties of undefined (reading 'value')` runtime crash in production — the compiler forces you to handle the `ok: false` branch before it lets you near `.value`. If you find yourself reaching for `result as any` to make the error go away, stop: you're deleting the safety net, not fixing the code.

### Your task

Write `parseStatus(input: string): { ok: true; status: "active" | "inactive" } | { ok: false; error: string }` that accepts only the literal strings `"active"` or `"inactive"` (case-insensitive) and errors on anything else.

**Check:** `parseStatus("ACTIVE")` returns `{ ok: true, status: "active" }`; `parseStatus("pending")` returns an object with `ok: false` and a non-empty `error` string. Print both cases.

---

## Day 4: Arrays & generics
{: #day-4-arrays-generics }

### Why this matters

`Array<any>` and hand-copied helper functions per type are how codebases rot. Generics let you write one `first`, one `groupBy`, one `pluck` that works correctly — and type-checked — across every shape of data you throw at it.

### Mental model

A generic function is a template: `<T>` is a placeholder filled in at the call site based on the argument you pass. `keyof T` gives you the union of a type's property names as a type, which is how you write functions that are safe against typos in field names.

### Code along

```ts
// src/day04.ts
function first<T>(xs: T[]): T | undefined {
  return xs[0];
}

function pluck<T, K extends keyof T>(rows: T[], key: K): T[K][] {
  return rows.map((row) => row[key]);
}

function groupBy<T, K extends string | number>(
  rows: T[],
  keyFn: (row: T) => K,
): Record<K, T[]> {
  const out = {} as Record<K, T[]>;
  for (const row of rows) {
    const k = keyFn(row);
    (out[k] ??= []).push(row);
  }
  return out;
}

type Score = { player: string; team: string; points: number };

const scores: Score[] = [
  { player: "Ada", team: "Red", points: 12 },
  { player: "Lin", team: "Blue", points: 9 },
  { player: "Sam", team: "Red", points: 7 },
];

console.log(first(scores)?.player);
console.log(pluck(scores, "points"));
console.log(groupBy(scores, (s) => s.team));
```

Expected output (formatting of the grouped object may wrap differently, values are what matter):

```
Ada
[ 12, 9, 7 ]
{ Red: [ { player: 'Ada', ... }, { player: 'Sam', ... } ], Blue: [ { player: 'Lin', ... } ] }
```

### Common mistake

Calling `pluck(scores, "poitns")` (typo). Because `K extends keyof T`, this is a compile error — `Argument of type '"poitns"' is not assignable to parameter of type ...` — instead of a silent `undefined` in every row at runtime, which is what you'd get in plain JavaScript. This is the single biggest argument for generics over `any[]`: the typo is caught at the call site, not discovered three weeks later when a report is wrong.

### Your task

Write `sumBy<T>(rows: T[], keyFn: (row: T) => number): number` and use it to compute total points per team from `groupBy`'s output (loop over the grouped object, sum each team's points with `sumBy`).

**Check:** printing the per-team totals gives `Red: 19` and `Blue: 9` for the sample data above.

---

## Day 5: Modules
{: #day-5-modules }

### Why this matters

One giant file compiles fine but doesn't scale past a few hundred lines: nothing stops one part of the code from silently depending on the internals of another. Modules with explicit `export`/`import` are the boundary that lets two files change independently as long as the exported contract holds.

### Mental model

`export` decides what's visible outside a file; everything else is private to that module by default (unlike classes, where you need explicit access modifiers — see Day 7). Named exports (`export const x`) are for multiple things per file; a `default` export is for "this file's one main thing." Prefer named exports — they survive renames and refactors in your editor better.

### Code along

```ts
// src/types.ts
export type Todo = { id: number; text: string; done: boolean };

// src/store.ts
import type { Todo } from "./types.ts";

export function createStore() {
  let todos: Todo[] = [];
  let nextId = 1;

  return {
    add(text: string): Todo {
      const todo: Todo = { id: nextId++, text, done: false };
      todos.push(todo);
      return todo;
    },
    complete(id: number): boolean {
      const todo = todos.find((t) => t.id === id);
      if (!todo) return false;
      todo.done = true;
      return true;
    },
    list(): Todo[] {
      return todos;
    },
  };
}

// src/day05.ts
import { createStore } from "./store.ts";

const store = createStore();
store.add("Write TypeScript notes");
const second = store.add("Ship the capstone");
store.complete(second.id);

for (const t of store.list()) {
  console.log(`[${t.done ? "x" : " "}] ${t.id}: ${t.text}`);
}
```

Expected output:

```
[ ] 1: Write TypeScript notes
[x] 2: Ship the capstone
```

### Common mistake

Importing with the wrong extension or path style and getting `Cannot find module './store' or its corresponding type declarations`. With `moduleResolution: NodeNext` (set in Day 0), relative imports need an explicit extension — `./store.ts` when running through `tsx`, or `./store.js` if you're importing compiled output. Mixing the two conventions across a project is the single most common "why won't this import" bug beginners hit.

### Your task

Add a `remove(id: number): boolean` method to the store and a `stats()` method returning `{ total: number; done: number }`. Keep `types.ts`, `store.ts`, and `day05.ts` as separate files — don't inline the store back into the day file.

**Check:** after adding two todos, completing one, and removing the other, `stats()` reports `{ total: 1, done: 1 }`.

---

## Day 6: Async & fetch
{: #day-6-async-fetch }

### Why this matters

Nearly everything useful — databases, APIs, files — is asynchronous. Untyped, un-awaited promises are where "it works on my machine" bugs come from: a response you assumed was ready but wasn't, an error swallowed because nobody `.catch()`'d it.

### Mental model

`async`/`await` is sequential-looking code over promises; the function pauses at `await` and resumes when the promise settles, without blocking anything else. Always check `res.ok` before trusting a response — `fetch` does **not** throw on HTTP 404/500, only on network failure. Always wrap awaited calls that can fail in `try`/`catch` or handle rejection explicitly.

### Code along

This spins up a real local server so the example runs offline and deterministically — no flaky third-party endpoint.

```ts
// src/day06.ts
import http, { type AddressInfo } from "node:http";

const server = http.createServer((req, res) => {
  res.setHeader("content-type", "application/json");
  if (req.url === "/health") {
    res.end(JSON.stringify({ status: "up", uptimeMs: 12345 }));
    return;
  }
  res.statusCode = 404;
  res.end(JSON.stringify({ error: "not found" }));
});

async function getJson<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`request to ${url} failed with status ${res.status}`);
  }
  return (await res.json()) as T;
}

async function main() {
  await new Promise<void>((resolve) => server.listen(0, resolve));
  const { port } = server.address() as AddressInfo;
  const base = `http://localhost:${port}`;

  const health = await getJson<{ status: string; uptimeMs: number }>(`${base}/health`);
  console.log("health:", health);

  try {
    await getJson(`${base}/missing`);
  } catch (err) {
    console.log("expected failure:", (err as Error).message);
  }
}

main()
  .catch((err) => console.error("unexpected error:", err))
  .finally(() => server.close());
```

Expected output:

```
health: { status: 'up', uptimeMs: 12345 }
expected failure: request to http://localhost:PORT/missing failed with status 404
```

### Common mistake

Calling `server.address()` before `listen()`'s callback fires — it returns `null` and destructuring it throws `Cannot read properties of null (reading 'port')`. This is a real race condition, not a TypeScript quirk: the server isn't bound to a port until the callback runs, which is exactly why the code above `await`s a promise wrapping `listen()` instead of calling `address()` right after starting it.

### Your task

Add a `/echo` route that reads the request body and echoes it back as JSON (`req.on("data", ...)` / `req.on("end", ...)`, or use `for await (const chunk of req)`). From `main`, POST a JSON body to it with `fetch(url, { method: "POST", body: JSON.stringify(...) })` and print the echoed result.

**Check:** the printed echoed object deep-equals the object you sent.

---

## Day 7: Classes & OOP lite
{: #day-7-classes-oop-lite }

### Why this matters

Classes bundle state and the operations that keep it valid in one place. A `BankAccount` that only exposes `deposit`/`withdraw` — never a raw mutable `balance` — is how you prevent "someone set balance to -500 directly" bugs by construction, not by convention.

### Mental model

`private` fields are enforced by the compiler (and, with the `#` syntax, by the runtime too) — external code literally cannot reference them. `implements` says "this class's public shape matches that interface"; unlike interfaces on plain objects, classes can also `extends` one parent for shared behavior.

### Code along

```ts
// src/day07.ts
interface Account {
  deposit(amount: number): void;
  withdraw(amount: number): void;
  readonly balance: number;
}

class InsufficientFundsError extends Error {
  constructor(requested: number, available: number) {
    super(`cannot withdraw ${requested}, only ${available} available`);
    this.name = "InsufficientFundsError";
  }
}

class BankAccount implements Account {
  #balance: number;

  constructor(openingBalance = 0) {
    if (openingBalance < 0) throw new Error("opening balance cannot be negative");
    this.#balance = openingBalance;
  }

  get balance(): number {
    return this.#balance;
  }

  deposit(amount: number): void {
    if (amount <= 0) throw new Error("deposit must be positive");
    this.#balance += amount;
  }

  withdraw(amount: number): void {
    if (amount > this.#balance) {
      throw new InsufficientFundsError(amount, this.#balance);
    }
    this.#balance -= amount;
  }
}

const acct = new BankAccount(100);
acct.deposit(50);
acct.withdraw(30);
console.log(`Balance: ${acct.balance}`);

try {
  acct.withdraw(1000);
} catch (err) {
  if (err instanceof InsufficientFundsError) {
    console.log(`Caught: ${err.message}`);
  }
}
```

Expected output:

```
Balance: 120
Caught: cannot withdraw 1000, only 120 available
```

### Common mistake

Trying `acct.#balance` from outside the class: `Property '#balance' is not accessible outside class 'BankAccount' because it has a private identifier`. This is different from the older `private` keyword, which is compile-time only — `(acct as any).balance` could still sneak past it at runtime. The `#` syntax is enforced by the JavaScript engine itself, which is why you should prefer it for anything that must never be bypassed.

### Your task

Add a `transferTo(other: BankAccount, amount: number): void` method that withdraws from `this` and deposits into `other`, rolling back (no state change) if the deposit somehow fails.

**Check:** transferring 40 from an account with balance 120 to a fresh account with balance 0 leaves the source at 80 and the destination at 40; transferring more than the source balance throws `InsufficientFundsError` and leaves both balances unchanged.

---

## Day 8: Utility types
{: #day-8-utility-types }

### Why this matters

Create and update DTOs are almost always subsets or variations of your main model — you don't send an `id` when creating, and updates are usually partial. Utility types derive those variants from one source of truth instead of you maintaining three near-identical hand-written types that quietly drift apart.

### Mental model

`Partial<T>` makes every field optional. `Pick<T, K>` keeps only the listed keys; `Omit<T, K>` keeps everything except the listed keys. Combine them: `Partial<Omit<T, "id">>` is "everything but the id, all optional" — the classic update-DTO shape.

### Code along

```ts
// src/day08.ts
type Product = {
  id: number;
  name: string;
  priceCents: number;
  description: string;
};

type ProductCreate = Omit<Product, "id">;
type ProductUpdate = Partial<Omit<Product, "id">>;

let nextId = 1;
const products: Product[] = [];

function createProduct(input: ProductCreate): Product {
  const product: Product = { id: nextId++, ...input };
  products.push(product);
  return product;
}

function updateProduct(id: number, patch: ProductUpdate): Product | undefined {
  const product = products.find((p) => p.id === id);
  if (!product) return undefined;
  Object.assign(product, patch);
  return product;
}

const p1 = createProduct({ name: "Mug", priceCents: 999, description: "Ceramic mug" });
console.log(p1);

updateProduct(p1.id, { priceCents: 899 });
console.log(products[0]);
```

Expected output:

```
{ id: 1, name: 'Mug', priceCents: 999, description: 'Ceramic mug' }
{ id: 1, name: 'Mug', priceCents: 899, description: 'Ceramic mug' }
```

### Common mistake

Writing `createProduct({ id: 5, name: "Mug", ... })` — passing an `id` where `ProductCreate` (which is `Omit<Product, "id">`) forbids it. The error is `Object literal may only specify known properties, and 'id' does not exist in type 'ProductCreate'`. This is the type system catching a real bug: the caller shouldn't be picking IDs, the store should — if you find yourself wanting to pass one, the create function's contract is probably wrong, not the caller.

### Your task

Add `Readonly<Product>` for a `getProduct(id: number): Readonly<Product> | undefined` function that returns data callers can read but not mutate through the returned reference.

**Check:** `npx tsc --noEmit` rejects `getProduct(1)!.priceCents = 1` with a read-only assignment error, while `updateProduct` (which doesn't go through `getProduct`) still works.

---

## Day 9: Strict mode habits
{: #day-9-strict-mode-habits }

### Why this matters

The most dangerous TypeScript bug is the one that compiles: a discriminated union where you forgot to handle one variant, and the function silently returns `undefined` instead of erroring. Exhaustiveness checking turns "I forgot a case" into a compile failure the moment you add a new variant anywhere in the codebase.

### Mental model

`never` is the type of "a value that can't exist." If, after a `switch` handles every known variant, TypeScript still thinks a value could reach a default branch, that value's type there is `never` — assign it to a parameter typed `never` and the compiler flags any missed case as an error, at the exact place you forgot to handle it.

### Code along

```ts
// src/day09.ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "rectangle"; width: number; height: number };

function assertNever(x: never): never {
  throw new Error(`Unhandled shape variant: ${JSON.stringify(x)}`);
}

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
    case "rectangle":
      return shape.width * shape.height;
    default:
      return assertNever(shape);
  }
}

const shapes: Shape[] = [
  { kind: "circle", radius: 2 },
  { kind: "square", side: 3 },
  { kind: "rectangle", width: 4, height: 5 },
];

for (const s of shapes) {
  console.log(`${s.kind}: ${area(s).toFixed(2)}`);
}
```

Expected output:

```
circle: 12.57
square: 9.00
rectangle: 20.00
```

### Common mistake

Adding a new variant — say `{ kind: "triangle"; base: number; height: number }` — to the `Shape` union but forgetting to add a `case` for it. Without `assertNever` in the `default` branch, the function would silently return `undefined` for triangles and you'd find out in production when a report shows `NaN` totals. With `assertNever(shape)` in `default`, the compiler immediately errors at that line: `Argument of type '{ kind: "triangle"; ... }' is not assignable to parameter of type 'never'` — pointing you straight at the missing case, at compile time, before it ships.

### Your task

Add the `triangle` variant above, watch `npx tsc --noEmit` fail on the `assertNever` line, then add the missing `case` to fix it.

**Check:** after adding both the variant and its `case`, `npx tsc --noEmit` passes and `area({ kind: "triangle", base: 6, height: 4 })` prints `12.00`.

---

## Day 10: Mini CLI tool
{: #day-10-mini-cli-tool }

### Why this matters

Every real project eventually needs a small script: migrate data, summarize a log, check a file. Being able to write a typed CLI in ten minutes — args in, validated data, useful output — is a skill you'll use weekly, not a toy exercise.

### Mental model

`process.argv` is `[nodePath, scriptPath, ...userArgs]` — always slice off the first two. Validate input immediately and exit with a non-zero code and a clear message on bad input; a CLI that crashes with a raw stack trace on bad args is a CLI nobody trusts.

### Code along

```ts
// src/day10.ts
import fs from "node:fs";

function usageAndExit(message: string): never {
  console.error(`Error: ${message}`);
  console.error("Usage: tsx src/day10.ts <path-to-json-file>");
  process.exit(1);
}

function main(): void {
  const path = process.argv[2];
  if (!path) usageAndExit("missing file path");

  if (!fs.existsSync(path)) usageAndExit(`file not found: ${path}`);

  const raw = fs.readFileSync(path, "utf8");
  let data: unknown;
  try {
    data = JSON.parse(raw);
  } catch {
    usageAndExit(`${path} is not valid JSON`);
  }

  if (typeof data !== "object" || data === null || Array.isArray(data)) {
    usageAndExit("expected a JSON object at the top level");
  }

  const keys = Object.keys(data as object);
  const summary = {
    file: path,
    keyCount: keys.length,
    keys: keys.sort(),
  };

  const outPath = "summary.md";
  const lines = [
    `# Summary of ${path}`,
    ``,
    `- Keys: ${summary.keyCount}`,
    ...summary.keys.map((k) => `  - ${k}`),
  ];
  fs.writeFileSync(outPath, lines.join("\n") + "\n");
  console.log(`Wrote ${outPath} (${summary.keyCount} keys)`);
}

main();
```

Test it:

```bash
echo '{"name": "Ada", "age": 30, "active": true}' > sample.json
npx tsx src/day10.ts sample.json
cat summary.md
```

Expected:

```
Wrote summary.md (3 keys)
```

...and `summary.md` lists `active`, `age`, `name` (sorted) under a `# Summary of sample.json` heading.

### Common mistake

Forgetting `process.exit(1)` after printing an error and letting `main()` continue with `data` as `undefined`, which then throws an unrelated, confusing `TypeError` a few lines later instead of your clear message. `usageAndExit`'s return type `never` exists precisely so the compiler can (in later, more advanced patterns) help verify control flow doesn't fall through — get comfortable writing small "exit helpers" like this rather than scattering raw `process.exit()` calls everywhere.

### Your task

Add a second optional argument: `tsx src/day10.ts sample.json --key=age` prints just that key's value (or errors if the key doesn't exist) instead of writing the full summary.

**Check:** `npx tsx src/day10.ts sample.json --key=age` prints `30`; `npx tsx src/day10.ts sample.json --key=missing` exits non-zero with a clear error and does not touch `summary.md`.

---

## Capstone project
{: #capstone }

Build a **typed URL shortener client** against a server you also write. This is checkable end to end, not vibes.

**Deliverable — file layout:**

```
url-shortener/
  src/server.ts     # node:http server, in-memory store
  src/client.ts      # typed fetch wrapper: create(), get(), list()
  src/cli.ts         # `create <url>`, `list`, `get <code>` commands
  README.md          # exact commands + expected output
```

**Server requirements:**
- `POST /links` with body `{ "url": string }` → `201` with `{ code: string, url: string }`. Reject missing/malformed `url` with `400`.
- `GET /links/:code` → `200` with the stored `{ code, url }`, or `404` if unknown.
- `GET /links` → `200` with an array of all `{ code, url }` entries.

**Client requirements (`src/client.ts`):** typed functions `createLink(url: string): Promise<Link>`, `getLink(code: string): Promise<Link | null>`, `listLinks(): Promise<Link[]>`, each throwing a descriptive `Error` on non-2xx responses other than the documented 404-as-null case.

**CLI requirements:** running `npx tsx src/cli.ts create https://example.com` prints the generated short code; `npx tsx src/cli.ts get <code>` prints the original URL; `npx tsx src/cli.ts list` prints all links, one per line.

**Acceptance check:** start the server, then run all three CLI commands in sequence and confirm the code printed by `create` is the same one accepted by `get`, and that `list` shows exactly the links you created — no more, no fewer. `npx tsc --noEmit` must pass with zero errors across all three files.

## Related

- [Getting Started with JavaScript](/blog/2026/07/10/getting-started-with-javascript/)
- [JavaScript in 10 Days](/courses/javascript-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
