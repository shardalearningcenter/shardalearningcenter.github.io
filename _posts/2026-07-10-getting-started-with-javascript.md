---
layout: post
title: "Getting Started with JavaScript"
date: 2026-07-10
description: "Variables, functions, async/await, and a tiny fetch demo — JS for the browser and Node."
tags: [javascript, getting-started]
---

JavaScript runs in the browser and on the server (Node). Start in the browser console (`F12` → Console), then move to a file when the snippet grows.

## Essentials

```javascript
const name = "Sharda";     // prefer const
let count = 0;             // when it must change

const add = (a, b) => a + b;

const nums = [1, 2, 3, 4];
const evens = nums.filter((n) => n % 2 === 0);
const doubled = nums.map((n) => n * 2);
```

Objects and JSON:

```javascript
const user = { id: 1, role: "student" };
console.log(user.role);
console.log(JSON.stringify(user));
```

## Async without tears

```javascript
async function load() {
  const res = await fetch("https://httpbin.org/get");
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  return data;
}

load().then(console.log).catch(console.error);
```

Promises and `async/await` are the same idea: “do this when the network returns.”

## Tiny page

```html
<!DOCTYPE html>
<html>
  <body>
    <button id="go">Fetch</button>
    <pre id="out"></pre>
    <script>
      document.getElementById("go").onclick = async () => {
        const res = await fetch("https://httpbin.org/get");
        const data = await res.json();
        document.getElementById("out").textContent = JSON.stringify(data, null, 2);
      };
    </script>
  </body>
</html>
```

Open the file in a browser and click the button.

## Exercise

Add a second button that `POST`s JSON to `https://httpbin.org/post` and prints the echoed body.

## Next

Frontends often call Python backends — see [FastAPI](/blog/2026/07/10/getting-started-with-fastapi/). For AI product UIs, keep JS thin and put model logic on the server.
