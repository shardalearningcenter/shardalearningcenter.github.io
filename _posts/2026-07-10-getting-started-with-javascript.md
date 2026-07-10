---
layout: post
title: "Getting Started with JavaScript"
date: 2026-07-10
description: "Variables, async/await, and a persistent todo app built with vanilla JS and localStorage — no framework, no build step, fully checkable."
tags: [javascript, getting-started]
---

JavaScript runs in the browser and on the server (Node). Start in the browser console (`F12` → Console), then move to a file once a snippet outgrows one line. This post ends with a small app that actually persists data across page reloads — the clearest way to prove your code did what you think it did.

## Essentials

```javascript
const name = "Sharda";     // prefer const
let count = 0;             // when a value must change

const add = (a, b) => a + b;

const nums = [1, 2, 3, 4];
const evens = nums.filter((n) => n % 2 === 0);
const doubled = nums.map((n) => n * 2);

const { id, role } = { id: 1, role: "student" };   // destructuring
const label = `user #${id} (${role})`;              // template literal
```

Always use `===`/`!==`, never `==`/`!=`. Loose equality coerces types in ways that surprise you (`"0" == false` is `true`).

## Async without tears

```javascript
async function load() {
  const res = await fetch("https://httpbin.org/get");
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return await res.json();
}

load().then(console.log).catch(console.error);
```

`async`/`await` and Promises are the same idea: "do this when the network returns," written to read top-to-bottom instead of nested in callbacks. The one rule that prevents most bugs: every Promise needs either an `await`, a `.then()`, or an explicit `.catch()` — an unhandled one ("floating promise") fails silently and you find out in production.

## Mini project: a todo app that survives a page reload

DOM manipulation and `localStorage` together, with zero dependencies and zero build step. Save this as `todo.html` and open it directly in a browser.

```html
<!DOCTYPE html>
<html>
<head><title>Todos</title></head>
<body>
  <input id="task" placeholder="New task" />
  <button id="add">Add</button>
  <ul id="list"></ul>

  <script>
    const KEY = "todos-v1";
    const load = () => JSON.parse(localStorage.getItem(KEY) || "[]");
    const save = (todos) => localStorage.setItem(KEY, JSON.stringify(todos));

    function render() {
      const list = document.getElementById("list");
      list.innerHTML = "";
      load().forEach((todo, i) => {
        const li = document.createElement("li");
        li.textContent = todo + " ";

        const del = document.createElement("button");
        del.textContent = "x";
        del.onclick = () => {
          const todos = load();
          todos.splice(i, 1);
          save(todos);
          render();
        };

        li.appendChild(del);
        list.appendChild(li);
      });
    }

    document.getElementById("add").onclick = () => {
      const input = document.getElementById("task");
      const value = input.value.trim();
      if (!value) return;
      const todos = load();
      todos.push(value);
      save(todos);
      input.value = "";
      render();
    };

    render();
  </script>
</body>
</html>
```

Test it end to end, in this order:

1. Open `todo.html`, add three tasks — they appear immediately.
2. **Refresh the page.** All three should still be there. This is the real test: it proves data persisted in `localStorage`, not just in a JavaScript variable that resets on reload.
3. Delete the middle task. Confirm it removed *that one*, not its neighbor — an easy off-by-one bug in `splice(i, 1)` if `i` were computed wrong.
4. Open DevTools → Application → Local Storage and inspect the raw JSON string yourself.

Extend it: add an "edit" button, or a "clear completed" button using `.filter()` instead of `.splice()`.

## Common footguns

- **`==` vs `===`** — covered above, but it's the single most common source of "why is this true when it shouldn't be" bugs.
- **Losing `this` in callbacks** — a plain `function` used as an event handler gets its own `this`; an arrow function captures the surrounding scope's `this`. The todo app above uses arrow functions for exactly this reason.
- **`var` vs `let`/`const`** — `var` is function-scoped and hoists, causing loop-variable bugs (`for (var i ...)` inside async callbacks all seeing the final `i`). Default to `const`, use `let` only when reassigning, and avoid `var` entirely.
- **Floating promises** — calling an `async` function without `await` or `.catch()` swallows errors silently. Lint rules like `no-floating-promises` exist specifically for this.
- **Mutating arrays you're about to render from** — `todos.push(...)` then forgetting to `save()` before `render()` leaves the UI and storage out of sync; the app above always saves, then renders.
- **`NaN !== NaN`** — the one value that isn't equal to itself; use `Number.isNaN(x)` to check, never `x === NaN`.

## You know you're done when…

- [ ] Adding a task updates the list immediately with no page reload
- [ ] Reloading the browser keeps your todos — proof `localStorage` persisted, not just in-memory state
- [ ] Deleting one todo removes exactly that item, not a neighbor
- [ ] DevTools → Console shows zero errors during the whole flow
- [ ] You can explain why the delete handler uses an arrow function rather than a plain `function`

## Next

Frontends often call Python backends — see [Getting Started with FastAPI](/2026/07/10/getting-started-with-fastapi/). For AI product UIs, keep JS thin and put model logic on the server.
