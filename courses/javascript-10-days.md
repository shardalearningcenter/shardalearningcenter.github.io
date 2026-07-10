---
layout: course
title: "JavaScript in 10 Days — Hands-On"
permalink: /courses/javascript-10-days/
course_track: "JavaScript"
description: "Modern JS from the console to a small Node script — no framework required."
toc:
  - id: "day-1-values-control-flow"
    label: "Day 1: Values & control flow"
  - id: "day-2-functions-scope"
    label: "Day 2: Functions & scope"
  - id: "day-3-arrays-deep-dive"
    label: "Day 3: Arrays deep dive"
  - id: "day-4-objects-json"
    label: "Day 4: Objects & JSON"
  - id: "day-5-dom-basics"
    label: "Day 5: DOM basics"
  - id: "day-6-async-javascript"
    label: "Day 6: Async JavaScript"
  - id: "day-7-modules-in-node"
    label: "Day 7: Modules in Node"
  - id: "day-8-errors-debugging"
    label: "Day 8: Errors & debugging"
  - id: "day-9-local-storage-mini-app"
    label: "Day 9: Local storage mini-app"
  - id: "day-10-small-node-cli"
    label: "Day 10: Small Node CLI"
  - id: "capstone"
    label: "Capstone project"
---

# JavaScript in 10 Days — Hands-On

Modern JS from the console to a small Node script — no framework required.

## Why this language
{: #why-this-language }

JavaScript runs everywhere: browsers, Node, edge workers. Master the language before the frameworks.

## Setup (Day 0)
{: #setup-day-0 }

Browser: DevTools console. Node:
```bash
node -v
mkdir js-lab && cd js-lab
```

---

## Day 1: Values & control flow
{: #day-1-values-control-flow }

### What you'll learn

- Primitives
- `if`/`for`/`while`
- Template strings

### Code along

```js
const n = 5;
for (let i = 1; i <= n; i++) console.log(`#${i}`);
```

### Your task

FizzBuzz 1–50.

---

## Day 2: Functions & scope
{: #day-2-functions-scope }

### What you'll learn

- Declarations vs arrows
- Closures
- Default params

### Code along

```js
const makeCounter = () => { let n = 0; return () => ++n; };
const c = makeCounter();
console.log(c(), c());
```

### Your task

Write `once(fn)` that only runs `fn` the first time.

---

## Day 3: Arrays deep dive
{: #day-3-arrays-deep-dive }

### What you'll learn

- `map`/`filter`/`reduce`
- Spread
- Destructuring

### Code along

```js
const nums = [1, 2, 3, 4];
const sum = nums.reduce((a, b) => a + b, 0);
const [a, ...rest] = nums;
console.log(sum, a, rest);
```

### Your task

From a list of users, return emails of active adults.

---

## Day 4: Objects & JSON
{: #day-4-objects-json }

### What you'll learn

- Object literals
- `Object.keys`
- JSON parse/stringify

### Code along

```js
const user = { id: 1, name: "Riya" };
console.log(JSON.stringify(user, null, 2));
```

### Your task

Merge two config objects; later keys win.

---

## Day 5: DOM basics
{: #day-5-dom-basics }

### What you'll learn

- `querySelector`
- Events
- textContent

### Code along

```js
document.body.innerHTML = `<button id="b">Click</button><p id="o"></p>`;
document.getElementById("b").onclick = () => {
  document.getElementById("o").textContent = new Date().toISOString();
};
```

### Your task

Build a page with an input and a live character counter.

---

## Day 6: Async JavaScript
{: #day-6-async-javascript }

### What you'll learn

- Promises
- `async`/`await`
- `fetch`

### Code along

```js
const res = await fetch("https://httpbin.org/uuid");
const data = await res.json();
console.log(data.uuid);
```

### Your task

Parallel-fetch two URLs with `Promise.all` and print both.

---

## Day 7: Modules in Node
{: #day-7-modules-in-node }

### What you'll learn

- ESM `import`
- `package.json` type module
- Exports

### Code along

```js
// package.json: { "type": "module" }
export const shout = (s) => s.toUpperCase();
import { shout } from "./shout.js";
console.log(shout("hey"));
```

### Your task

Split a word-frequency script into modules.

---

## Day 8: Errors & debugging
{: #day-8-errors-debugging }

### What you'll learn

- `try`/`catch`
- Custom Error
- `console.table`

### Code along

```js
function parseAge(s) {
  const n = Number(s);
  if (!Number.isFinite(n)) throw new Error("bad age");
  return n;
}
try { console.log(parseAge("x")); } catch (e) { console.error(e.message); }
```

### Your task

Validate a form object; collect all errors, don’t stop at first.

---

## Day 9: Local storage mini-app
{: #day-9-local-storage-mini-app }

### What you'll learn

- `localStorage`
- Events
- Render lists

### Code along

```js
const KEY = "todos";
const load = () => JSON.parse(localStorage.getItem(KEY) ?? "[]");
const save = (xs) => localStorage.setItem(KEY, JSON.stringify(xs));
save([...load(), { text: "ship it", done: false }]);
console.log(load());
```

### Your task

Todo list UI that survives refresh.

---

## Day 10: Small Node CLI
{: #day-10-small-node-cli }

### What you'll learn

- `process.argv`
- `fs`
- Exit codes

### Code along

```js
import fs from "node:fs";
const file = process.argv[2];
if (!file) { console.error("usage: node wc.js <file>"); process.exit(1); }
const text = fs.readFileSync(file, "utf8");
console.log(text.trim().split(/\s+/).length);
```

### Your task

CLI that prints line/word/char counts like `wc`.


---

## Capstone project
{: #capstone }

Ship a **browser + Node** pair: a notes app in the browser (localStorage) and a Node script that imports/exports notes as JSON.

## Related

- [TypeScript in 10 Days](/courses/typescript-10-days/)
- [Getting Started with JavaScript](/blog/2026/07/10/getting-started-with-javascript/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
