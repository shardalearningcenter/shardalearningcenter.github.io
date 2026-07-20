---
layout: course
title: "JavaScript in 10 Days — Hands-On"
permalink: /courses/javascript-10-days/
course_track: "JavaScript"
description: "Modern JS from the console to a small Node CLI — closures, arrays, async, and the errors you'll actually hit, explained."
toc:
  - id: "why-this-language"
    label: "Why this language"
  - id: "setup-day-0"
    label: "Setup (Day 0)"
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

Modern JS, no framework: the language itself, the runtime quirks that trip people up, and enough Node to ship a real CLI.

## Why this language
{: #why-this-language }

JavaScript is the only language that runs natively in every browser, and it's also a first-class server language via Node. That combination means the concepts in this course — closures, `this`, promises, prototypes — carry directly into React, Vue, Express, and every framework built on top of them. Learn the language before you learn a framework's opinions about the language; it makes the frameworks' error messages make sense instead of feeling like magic.

## Setup (Day 0)
{: #setup-day-0 }

Two runtimes, one language: your browser's DevTools console for DOM days, Node for everything else.

```bash
node -v                 # expect v18.x or higher (need built-in fetch)
mkdir js-lab && cd js-lab
npm init -y
```

Verify Node works and check strict-mode behavior (Node modules are strict by default, browser `<script>` tags are not unless you opt in):

```bash
node -e 'console.log(1 + 1)'   # prints 2
```

Each day's file goes in `js-lab/dayNN.mjs` (the `.mjs` extension turns on ES module syntax — `import`/`export` — without editing `package.json`). Run with `node dayNN.mjs`. Days involving the DOM (Day 5, part of Day 9) use a plain `index.html` you open in a browser instead — those days say so explicitly.

**Checkpoint:** if `import`/`export` throws `SyntaxError: Cannot use import statement outside a module`, you saved the file as `.js` instead of `.mjs`, or you're running it directly with `node day07.js` when it needs the module flag. Rename to `.mjs` and re-run.

---

## Day 1: Values & control flow
{: #day-1-values-control-flow }

### Why this matters

Every program is values, decisions, and repetition. Get comfortable with JavaScript's specific rules here — especially around equality and truthiness — because they differ from most other languages and cause real bugs if you assume otherwise.

### Mental model

Use `===`/`!==`, never `==`/`!=` — the loose operators coerce types in surprising ways (`"" == 0` is `true`; `null == undefined` is `true` but `null == 0` is `false`). Falsy values are exactly: `false`, `0`, `""`, `null`, `undefined`, `NaN` — everything else, including `"0"` and `[]`, is truthy.

### Code along

```js
// day01.mjs
function fizzbuzz(n) {
  const lines = [];
  for (let i = 1; i <= n; i++) {
    if (i % 15 === 0) lines.push("FizzBuzz");
    else if (i % 3 === 0) lines.push("Fizz");
    else if (i % 5 === 0) lines.push("Buzz");
    else lines.push(String(i));
  }
  return lines;
}

const result = fizzbuzz(20);
console.log(result.join(" "));
console.log(`Fizz count: ${result.filter((l) => l === "Fizz").length}`);
```

Run:

```bash
node day01.mjs
```

Expected output:

```
1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz 16 17 Fizz 19 Buzz
Fizz count: 4
```

### Common mistake

Checking divisibility with `i % 15 == 0` after `else if (i % 3 === 0)` **first** — order matters. If the `% 3` check runs before `% 15`, every multiple of 15 prints `"Fizz"` and never reaches the `FizzBuzz` branch, because `15 % 3 === 0` is also true and the `else if` chain stops at the first match. This is a logic bug, not a syntax error — it runs fine and prints wrong data, which is the most dangerous kind of bug because nothing tells you it's wrong.

### Your task

Modify `fizzbuzz` to also push `"Buzz3"` for multiples of 3 that are also odd numbers not divisible by 5 (i.e., a fourth category layered on top). Decide the correct order of your `if` checks and justify it in a comment.

**Check:** running for `n = 20` still produces exactly one label per number (no number falls through to the plain-number case if it matches your new rule), and you can point to why your check order is correct.

---

## Day 2: Functions & scope
{: #day-2-functions-scope }

### Why this matters

Closures are how JavaScript remembers state without classes — every debounce function, every event handler with private state, every memoization cache is a closure. If closures feel like magic, most of the ecosystem's code will feel like magic too.

### Mental model

A closure is a function bundled with the variables from its enclosing scope at the time it was created — not copies of the values, but live references. Each call to an outer function creates a **new** scope, so two counters from `makeCounter()` never share state.

### Code along

```js
// day02.mjs
function makeCounter(start = 0) {
  let count = start;
  return {
    increment: () => ++count,
    decrement: () => --count,
    value: () => count,
  };
}

function once(fn) {
  let called = false;
  let result;
  return (...args) => {
    if (!called) {
      result = fn(...args);
      called = true;
    }
    return result;
  };
}

const a = makeCounter();
const b = makeCounter(100);
console.log(a.increment(), a.increment(), b.increment());
console.log("a:", a.value(), "b:", b.value());

let sideEffects = 0;
const init = once(() => {
  sideEffects++;
  return "initialized";
});
console.log(init(), init(), init());
console.log("side effects ran:", sideEffects, "times");
```

Expected output:

```
1 2 101
a: 2 b: 101
initialized initialized initialized
side effects ran: 1 times
```

### Common mistake

Building an array of closures inside a `for` loop using `var` instead of `let`: `for (var i = 0; i < 3; i++) fns.push(() => i)` — every closure captures the **same** `i`, and after the loop finishes, all three functions return `3`. `let` fixes this because it creates a fresh binding per iteration. This is the single most common closure bug and the main reason `var` is considered legacy — always use `let`/`const`.

### Your task

Write `memoize(fn)` that caches results by argument (assume a single numeric argument, use a `Map`) so repeated calls with the same input don't recompute. Test it by wrapping a function that increments a counter each time it actually runs, and confirm the counter only increases on new inputs.

**Check:** calling the memoized function with `5, 5, 5, 7` increments the underlying counter exactly twice (once for `5`, once for `7`), even though the function was called four times.

---

## Day 3: Arrays deep dive
{: #day-3-arrays-deep-dive }

### Why this matters

`map`/`filter`/`reduce` plus destructuring are how you transform data in JavaScript without writing manual index-tracking loops that are easy to get off-by-one wrong. This is the vocabulary of every data-shaping task you'll do — API responses, form data, CSV rows.

### Mental model

`map` transforms each element 1:1, `filter` keeps a subset, `reduce` folds everything into one value — chain them left to right and read them as a pipeline. None of the three mutate the original array; they return new ones. Destructuring (`const [a, ...rest] = arr`) and spread (`[...a, ...b]`) are how you avoid manual indexing entirely.

### Code along

```js
// day03.mjs
const users = [
  { name: "Ada", age: 36, active: true, email: "ada@example.com" },
  { name: "Lin", age: 17, active: true, email: "lin@example.com" },
  { name: "Sam", age: 42, active: false, email: "sam@example.com" },
  { name: "Kai", age: 29, active: true, email: "kai@example.com" },
];

function activeAdultEmails(users) {
  return users
    .filter((u) => u.active && u.age >= 18)
    .map((u) => u.email);
}

console.log(activeAdultEmails(users));

const totalAge = users.reduce((sum, u) => sum + u.age, 0);
console.log("Average age:", (totalAge / users.length).toFixed(1));

const [first, ...rest] = users;
console.log("First user:", first.name, "| Remaining:", rest.length);
```

Expected output:

```
[ 'ada@example.com', 'kai@example.com' ]
Average age: 31.0
First user: Ada | Remaining: 3
```

### Common mistake

Writing `.filter(u => u.active && u.age >= 18)` but forgetting parentheses when returning an object literal from an arrow function elsewhere: `.map(u => { name: u.name })` does **not** return `{ name: u.name }` — the `{` is parsed as a function body, `name: u.name` becomes a useless labeled statement, and the arrow function returns `undefined`. The fix is to wrap the object in parentheses: `.map(u => ({ name: u.name }))`. This exact mistake produces an array of `undefined`s with no error thrown — check your output, don't assume.

### Your task

Write `topEarners(products, n)` that, given `[{ name, priceCents }]`, returns the `n` most expensive product names, using `sort` (careful: `sort` mutates — copy the array first with `[...products]`) and `slice`.

**Check:** given 5 products with distinct prices, `topEarners(products, 2)` returns exactly the two highest-priced names in descending order, and the original `products` array's order is unchanged after the call.

---

## Day 4: Objects & JSON
{: #day-4-objects-json }

### Why this matters

JSON is the universal data interchange format — APIs, config files, local storage all speak it. Knowing exactly what survives a `JSON.stringify`/`JSON.parse` round-trip (and what silently doesn't) saves you from bugs that only show up after data has been serialized and reloaded.

### Mental model

`JSON.stringify` drops `undefined` values, functions, and `Symbol` keys entirely; it converts `Date` objects to ISO strings (one-way — parsing back gives you a plain string, not a `Date`). `Object.keys`/`values`/`entries` only see a plain object's own enumerable properties, not inherited ones.

### Code along

```js
// day04.mjs
function mergeConfig(base, override) {
  return { ...base, ...override };
}

const defaults = { timeout: 5000, retries: 3, debug: false };
const userConfig = { retries: 5, debug: true };

const merged = mergeConfig(defaults, userConfig);
console.log(merged);
console.log(JSON.stringify(merged, null, 2));

const withExtras = {
  ...merged,
  createdAt: new Date("2026-01-01T00:00:00Z"),
  callback: () => "ignored",
  missing: undefined,
};

console.log(JSON.stringify(withExtras));
```

Expected output:

```
{ timeout: 5000, retries: 5, debug: true }
{
  "timeout": 5000,
  "retries": 5,
  "debug": true
}
{"timeout":5000,"retries":5,"debug":true,"createdAt":"2026-01-01T00:00:00.000Z"}
```

Note: `callback` and `missing` are simply absent from the final JSON string — not `null`, not an error, just gone.

### Common mistake

Assuming `JSON.parse(JSON.stringify(obj))` is a safe deep clone for anything containing a `Date`, `Map`, `Set`, or function — it isn't. The round trip turns `Date` objects into plain strings permanently; parsing the result back gives you a string where you expect a `Date`, and calling `.getFullYear()` on it throws `TypeError: date.getFullYear is not a function`. For real deep cloning of complex objects, use `structuredClone(obj)` (built into Node 17+ and browsers), which preserves `Date`, `Map`, and `Set` correctly.

### Your task

Write `deepMerge(base, override)` that merges nested objects recursively (plain `{ ...base, ...override }` only merges one level deep — a nested object in `override` fully replaces the one in `base` instead of merging with it). Test with a config that has a nested `{ database: { host, port } }` where you only override `port`.

**Check:** after `deepMerge`, `result.database.host` still has the base value and `result.database.port` has the override value — a plain spread merge would have lost `host`.

---

## Day 5: DOM basics
{: #day-5-dom-basics }

### Why this matters

Every frontend framework is, underneath, generating and updating DOM nodes. Manipulating the DOM by hand once — selecting elements, wiring events, reading/writing text — demystifies what React/Vue/Svelte are automating for you.

### Mental model

The DOM is a live tree; `querySelector`/`getElementById` find nodes, event listeners react to user actions, and `textContent`/`value` read or write what's displayed. Nothing re-renders automatically — if data changes, you must explicitly update the DOM to reflect it.

### Code along

This day runs in a browser, not Node. Save as `day05.html` and open it directly (double-click, or `open day05.html` / drag into a browser tab).

```html
<!-- day05.html -->
<!DOCTYPE html>
<html>
<body>
  <input id="text" placeholder="Type something..." />
  <p id="counter">0 characters</p>
  <p id="reversed"></p>

  <script>
    const input = document.getElementById("text");
    const counter = document.getElementById("counter");
    const reversed = document.getElementById("reversed");

    input.addEventListener("input", () => {
      const value = input.value;
      counter.textContent = `${value.length} characters`;
      reversed.textContent = [...value].reverse().join("");
    });
  </script>
</body>
</html>
```

Open it, type "hello" into the input, and confirm the page shows `5 characters` and `olleh`.

### Common mistake

Putting the `<script>` tag in `<head>` and calling `document.getElementById` before the elements below it exist in the DOM yet — `getElementById` returns `null`, and calling `.addEventListener` on `null` throws `Cannot read properties of null (reading 'addEventListener')`. Fix by placing scripts at the end of `<body>` (as above) or wrapping the code in a `DOMContentLoaded` listener: `document.addEventListener("DOMContentLoaded", () => { ... })`.

### Your task

Add a button that clears the input and resets both `counter` and `reversed` to their initial states, and disable the button whenever the input is already empty (`button.disabled = value.length === 0`).

**Check:** typing text enables the button; clicking it empties the input, resets the counter text to `0 characters`, clears the reversed text, and the button becomes disabled again.

---

## Day 6: Async JavaScript
{: #day-6-async-javascript }

### Why this matters

Real programs wait on things — network responses, timers, file reads. Promises and `async`/`await` are how JavaScript expresses "this will finish later" without blocking the single thread everything else runs on.

### Mental model

`await` only pauses the `async` function it's inside — the rest of the program keeps running. `Promise.all` runs promises concurrently and waits for all of them; if you `await` one at a time in sequence instead, you're accidentally serializing work that could have run in parallel.

### Code along

Run in Node — this spins up a local server so there's no dependency on the network being up.

```js
// day06.mjs
import http from "node:http";

const server = http.createServer((req, res) => {
  const delayMs = req.url === "/slow" ? 200 : 20;
  setTimeout(() => {
    res.setHeader("content-type", "application/json");
    res.end(JSON.stringify({ path: req.url, delayMs }));
  }, delayMs);
});

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url} -> ${res.status}`);
  return res.json();
}

await new Promise((resolve) => server.listen(0, resolve));
const base = `http://localhost:${server.address().port}`;

const start = Date.now();
const [fast, slow] = await Promise.all([
  fetchJson(`${base}/fast`),
  fetchJson(`${base}/slow`),
]);
console.log("parallel took ~", Date.now() - start, "ms");
console.log(fast, slow);

server.close();
```

Expected output (timing will vary but should be close to the slower request, ~200ms, not the sum of both):

```
parallel took ~ 200 ms
{ path: '/fast', delayMs: 20 } { path: '/slow', delayMs: 200 }
```

### Common mistake

Writing `const fast = await fetchJson(url1); const slow = await fetchJson(url2);` instead of `Promise.all`. Both work and produce the same values, but the sequential version takes roughly `20 + 200 = 220ms` because the second request doesn't even start until the first fully finishes — a real performance bug that's invisible in code review unless you know to look for consecutive unrelated `await`s that could run concurrently.

### Your task

Add a third endpoint `/flaky` that responds with a `500` status half the time (`Math.random() < 0.5`). Write `fetchWithRetry(url, attempts = 3)` that retries on failure and throws only after exhausting attempts.

**Check:** run the script several times; it should eventually always print a successful `/flaky` response within 3 attempts (statistically, failing all 3 is 1-in-8 — run it a few times and confirm you see both an immediate success and at least one retry-then-success in different runs).

---

## Day 7: Modules in Node
{: #day-7-modules-in-node }

### Why this matters

Splitting code into modules with a clear public surface (`export`) is what makes a codebase navigable past a few hundred lines. It's also a prerequisite for testing — you can't unit-test a function that's trapped as an unexported closure in a 500-line file.

### Mental model

ESM (`import`/`export`) is the modern standard, distinct from Node's older CommonJS (`require`/`module.exports`) — don't mix them in one file. A module's top-level code runs exactly once, the first time it's imported, no matter how many other files import it afterward.

### Code along

```js
// wordcount.mjs
export function wordFrequency(text) {
  const words = text.toLowerCase().match(/[a-z']+/g) ?? [];
  const freq = {};
  for (const w of words) {
    freq[w] = (freq[w] ?? 0) + 1;
  }
  return freq;
}

export function topWords(freq, n) {
  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, n);
}

// day07.mjs
import { wordFrequency, topWords } from "./wordcount.mjs";

const text = "the quick brown fox jumps over the lazy dog the fox runs";
const freq = wordFrequency(text);
console.log(freq);
console.log(topWords(freq, 2));
```

Expected output:

```
{ the: 3, quick: 1, brown: 1, fox: 2, jumps: 1, over: 1, lazy: 1, dog: 1, runs: 1 }
[ [ 'the', 3 ], [ 'fox', 2 ] ]
```

### Common mistake

Forgetting the `.mjs` (or matching `package.json` `"type": "module"`) and getting `SyntaxError: Unexpected token 'export'`. Node decides how to parse a file (CommonJS vs ESM) before running it, based on extension/package.json — there's no in-file way to declare "this is an ES module" the way some other languages allow.

### Your task

Add a third function `wordLengthHistogram(freq)` returning `{ [length]: count }` — how many distinct words have each length. Import it alongside the other two into `day07.mjs` and print it for the sample text.

**Check:** for the sample text, the histogram shows `3` for length matching `"the"`, `"fox"`, `"dog"`, `"the"` (dedupe by distinct word, not occurrence) — verify your counts by hand against the word list before trusting the output.

---

## Day 8: Errors & debugging
{: #day-8-errors-debugging }

### Why this matters

Production code fails in ways your happy-path tests never anticipated: malformed input, network timeouts, unexpected `null`. Structured error handling — custom error types, collecting all validation errors instead of stopping at the first — is what separates a debuggable failure from a cryptic crash.

### Mental model

`throw` anywhere inside a `try` jumps straight to the nearest `catch`, skipping everything in between — including cleanup code, unless it's in a `finally` block. Custom error classes (`extends Error`) let `catch` blocks distinguish "expected, handled" errors from genuine bugs using `instanceof`.

### Code along

```js
// day08.mjs
class ValidationError extends Error {
  constructor(errors) {
    super(`validation failed: ${errors.join("; ")}`);
    this.name = "ValidationError";
    this.errors = errors;
  }
}

function validateForm(form) {
  const errors = [];
  if (!form.email?.includes("@")) errors.push("email must contain @");
  if (typeof form.age !== "number" || form.age < 0) errors.push("age must be a non-negative number");
  if (!form.name || form.name.trim().length === 0) errors.push("name is required");

  if (errors.length > 0) throw new ValidationError(errors);
  return { ...form, name: form.name.trim() };
}

const inputs = [
  { name: "Ada", email: "ada@example.com", age: 30 },
  { name: "", email: "not-an-email", age: -5 },
];

for (const input of inputs) {
  try {
    const clean = validateForm(input);
    console.log("valid:", clean);
  } catch (err) {
    if (err instanceof ValidationError) {
      console.log("invalid:", err.errors);
    } else {
      throw err; // unexpected bug, don't swallow it
    }
  }
}
```

Expected output:

```
valid: { name: 'Ada', email: 'ada@example.com', age: 30 }
invalid: [ 'email must contain @', 'age must be a non-negative number', 'name is required' ]
```

### Common mistake

Writing `if (errors.length > 0) throw errors;` (throwing a plain array or string instead of an `Error` subclass). `catch (err)` still catches it, but `err.stack` doesn't exist, `err instanceof Error` is `false`, and any logging/monitoring tool that expects `.message` shows `undefined`. Always throw `Error` instances (or subclasses) — never raw strings, objects, or arrays.

### Your task

Add a `passwordStrength(password)` check to the same form (require length ≥ 8, at least one digit) that contributes its own message to the `errors` array rather than throwing separately — validation should still collect **all** problems in one pass, not stop at the first field.

**Check:** a form with a bad email, a 4-character password, and a valid name/age reports exactly two errors (email and password), not one.

---

## Day 9: Local storage mini-app
{: #day-9-local-storage-mini-app }

### Why this matters

`localStorage` is the simplest form of client-side persistence — no backend, no database, data survives a page refresh. It's how you build a genuinely useful toy app (a todo list that doesn't forget your todos) with nothing but the browser.

### Mental model

`localStorage` only stores strings — you must `JSON.stringify` on the way in and `JSON.parse` on the way out. It's synchronous and per-origin (same protocol+domain+port); it persists until explicitly cleared, surviving tab closes and browser restarts.

### Code along

Save as `day09.html`, open in a browser.

```html
<!-- day09.html -->
<!DOCTYPE html>
<html>
<body>
  <input id="new-todo" placeholder="What needs doing?" />
  <button id="add-btn">Add</button>
  <ul id="list"></ul>

  <script>
    const KEY = "todos-v1";
    const load = () => JSON.parse(localStorage.getItem(KEY) ?? "[]");
    const save = (todos) => localStorage.setItem(KEY, JSON.stringify(todos));

    function render() {
      const list = document.getElementById("list");
      list.innerHTML = "";
      for (const todo of load()) {
        const li = document.createElement("li");
        li.textContent = todo.text;
        if (todo.done) li.style.textDecoration = "line-through";
        li.addEventListener("click", () => {
          const todos = load().map((t) =>
            t.id === todo.id ? { ...t, done: !t.done } : t
          );
          save(todos);
          render();
        });
        list.appendChild(li);
      }
    }

    document.getElementById("add-btn").addEventListener("click", () => {
      const input = document.getElementById("new-todo");
      const text = input.value.trim();
      if (!text) return;
      const todos = load();
      todos.push({ id: Date.now(), text, done: false });
      save(todos);
      input.value = "";
      render();
    });

    render();
  </script>
</body>
</html>
```

Add a few todos, click one to toggle it (strikethrough), refresh the page — they're still there.

### Common mistake

Calling `render()` after mutating the array returned by `load()` directly (`load().push(...)`) instead of calling `save()` — `localStorage` is not a live reference to a JS array; `load()` deserializes a fresh copy every time, so mutating that copy and forgetting to `save()` it back is a silent no-op that looks correct until you refresh and the "added" todo is gone.

### Your task

Add a delete button per item (a small "×" that removes just that todo) and a "Clear completed" button that removes every `done: true` todo in one click.

**Check:** after adding 3 todos, marking 1 done, and clicking "Clear completed," exactly 2 todos remain, and refreshing the page still shows those same 2.

---

## Day 10: Small Node CLI
{: #day-10-small-node-cli }

### Why this matters

`wc`, `grep`, `ls` — the small composable CLIs that make Unix pleasant to use are just programs that read args, do one thing, and print predictable output. Writing your own is the fastest way to internalize argument parsing, exit codes, and stdin/file handling.

### Mental model

Exit code `0` means success, anything else means failure — scripts and CI pipelines check this, not your console output. `process.argv.slice(2)` is your actual argument list; validate it and fail loudly and immediately if it's wrong, rather than limping forward with bad data.

### Code along

```js
// wc.mjs
import fs from "node:fs";

const file = process.argv[2];
if (!file) {
  console.error("usage: node wc.mjs <file>");
  process.exit(1);
}

let text;
try {
  text = fs.readFileSync(file, "utf8");
} catch (err) {
  console.error(`cannot read ${file}: ${err.message}`);
  process.exit(1);
}

const lines = text.split("\n").length - (text.endsWith("\n") ? 1 : 0);
const words = text.trim().split(/\s+/).filter(Boolean).length;
const chars = text.length;

console.log(`${lines}\t${words}\t${chars}\t${file}`);
```

Test it:

```bash
printf "hello world\nsecond line\n" > sample.txt
node wc.mjs sample.txt
```

Expected output:

```
2	4	24	sample.txt
```

(2 lines, 4 words, 24 characters including newlines — verify the character count against your actual file with `wc -c sample.txt` if you're on macOS/Linux.)

### Common mistake

Computing line count as `text.split("\n").length` without adjusting for a trailing newline. A file ending in `\n` (the Unix convention, and what most editors write) produces one extra empty string after the final split, overcounting lines by one. This is exactly the kind of off-by-one that only shows up when you check your output against a known-good tool like the real `wc` — always verify against ground truth, don't trust that code "looks right."

### Your task

Add a `-l`, `-w`, or `-c` flag (mimicking real `wc`) that prints only that one count instead of all three, e.g. `node wc.mjs -w sample.txt` prints just `4`.

**Check:** `node wc.mjs -l sample.txt`, `-w`, and `-c` each print a single bare number matching the corresponding column from the no-flag output above.

---

## Capstone project
{: #capstone }

Ship a **notes app** that works in two environments sharing one data format: a browser page using `localStorage`, and a Node script that can import/export the same notes as JSON — proving your data model is portable, not tied to one runtime.

**Deliverable — file layout:**

```
notes-app/
  notes.html      # browser UI: add/edit/delete notes, persisted to localStorage
  notes-cli.mjs   # node CLI: export (localStorage-shaped JSON -> file), import (file -> printed notes), stats
  README.md       # exact commands + expected output
```

**Shared data shape:** `{ id: number, title: string, body: string, updatedAt: string (ISO) }[]`.

**Browser requirements:** add a note (title + body), edit an existing note's body, delete a note, and see the list persist across a page refresh (same `localStorage` key convention as Day 9).

**CLI requirements:**
- `node notes-cli.mjs export <localStorage-json-file> <output.json>` — reads a JSON file (you manually copy the value from DevTools → Application → Local Storage into a file for this exercise), validates it matches the shared shape, and writes a pretty-printed copy.
- `node notes-cli.mjs stats <notes.json>` — prints total note count and the title of the most recently updated note.

**Acceptance check:** create 3 notes in the browser, copy the `localStorage` value into `raw.json`, run `export raw.json clean.json` and confirm `clean.json` is valid, indented JSON with exactly 3 entries; run `stats clean.json` and confirm it correctly identifies the most recently edited note after you edit one of the three in the browser and re-export.

## Related

- [TypeScript in 10 Days](/courses/typescript-10-days/)
- [Getting Started with JavaScript](/blog/2026/07/10/getting-started-with-javascript/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
