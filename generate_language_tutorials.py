#!/usr/bin/env python3
"""Generate hands-on multi-day tutorials for hot programming languages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COURSES = ROOT / "courses"
POSTS = ROOT / "_posts"


def slugify(label: str) -> str:
    s = re.sub(r"[^\w\s-]", "", label.lower())
    return re.sub(r"[-\s]+", "-", s).strip("-")


def day(n: int, title: str, learn: list[str], code: str, lang: str, task: str, tip: str = "") -> dict:
    return {
        "n": n,
        "title": title,
        "learn": learn,
        "code": code.strip("\n"),
        "lang": lang,
        "task": task,
        "tip": tip,
    }


def render_course(
    slug: str,
    title: str,
    track: str,
    blurb: str,
    why: str,
    setup: str,
    days: list[dict],
    capstone: str,
    related: list[tuple[str, str]],
) -> str:
    toc_lines = []
    body_parts = []
    for d in days:
        sid = f"day-{d['n']}-{slugify(d['title'])}"
        toc_lines.append(f'  - id: "{sid}"\n    label: "Day {d["n"]}: {d["title"]}"')
        learn = "\n".join(f"- {x}" for x in d["learn"])
        tip = f"\n\n**Pro tip:** {d['tip']}" if d["tip"] else ""
        body_parts.append(
            f"""## Day {d['n']}: {d['title']}
{{: #{sid} }}

### What you'll learn

{learn}

### Code along

```{d['lang']}
{d['code']}
```

### Your task

{d['task']}{tip}
"""
        )

    toc_yaml = "\n".join(toc_lines)
    related_md = "\n".join(f"- [{a}]({b})" for a, b in related)
    days_body = "\n---\n\n".join(body_parts)

    return f"""---
layout: course
title: "{title}"
permalink: /courses/{slug}/
course_track: "{track}"
description: "{blurb}"
toc:
{toc_yaml}
  - id: "capstone"
    label: "Capstone project"
---

# {title}

{blurb}

## Why this language
{{: #why-this-language }}

{why}

## Setup (Day 0)
{{: #setup-day-0 }}

{setup}

---

{days_body}

---

## Capstone project
{{: #capstone }}

{capstone}

## Related

{related_md}

[All language tutorials](/courses/languages/) · [All courses](/courses/)
"""


# ---------------------------------------------------------------------------
# Language curricula
# ---------------------------------------------------------------------------

LANGS: list[dict] = []


def add(**kwargs):
    LANGS.append(kwargs)


add(
    slug="typescript-10-days",
    title="TypeScript in 10 Days — Hands-On",
    track="TypeScript",
    blurb="Typed JavaScript for real apps: types, modules, async, and a small API client.",
    why="TypeScript is the default for serious frontend and Node backends. Types catch bugs before runtime and make refactors safe.",
    setup="""```bash
node -v          # 18+
npm init -y
npm i -D typescript tsx @types/node
npx tsc --init
```
Create `src/day01.ts` and run with `npx tsx src/day01.ts`.""",
    days=[
        day(1, "Types & variables", ["`string`/`number`/`boolean`", "Type annotations", "`const` vs `let`"],
            'const name: string = "Ada";\nlet score: number = 42;\nconsole.log(`${name} scored ${score}`);',
            "ts", "Make a `Person` type with `name` and `age`, print a greeting.", "Prefer `const` until you need reassignment."),
        day(2, "Interfaces & objects", ["`interface`", "Optional props", "Readonly"],
            'interface User { id: number; email: string; active?: boolean }\nconst u: User = { id: 1, email: "a@b.com" };\nconsole.log(u.email);',
            "ts", "Model a `BlogPost` with title, tags[], and optional publishedAt."),
        day(3, "Functions & unions", ["Param/return types", "Union types", "Type narrowing"],
            'type Id = string | number;\nfunction label(id: Id): string {\n  return typeof id === "string" ? id.toUpperCase() : `N${id}`;\n}\nconsole.log(label(7), label("abc"));',
            "ts", "Write `parseStatus(s: string): \"ok\" | \"err\"` that validates input."),
        day(4, "Arrays & generics", ["Typed arrays", "Generic functions", "`Record`"],
            'function first<T>(xs: T[]): T | undefined { return xs[0]; }\nconsole.log(first([10, 20]));\nconst scores: Record<string, number> = { alice: 9 };',
            "ts", "Implement `pluck<T, K extends keyof T>(rows: T[], key: K): T[K][]`."),
        day(5, "Modules", ["`export`/`import`", "Default vs named", "Project layout"],
            '// math.ts\nexport const add = (a: number, b: number) => a + b;\n\n// main.ts\nimport { add } from "./math";\nconsole.log(add(2, 3));',
            "ts", "Split a todo app into `types.ts`, `store.ts`, and `main.ts`."),
        day(6, "Async & fetch", ["`async`/`await`", "`Promise`", "Error handling"],
            'async function getJson(url: string) {\n  const res = await fetch(url);\n  if (!res.ok) throw new Error(String(res.status));\n  return res.json();\n}\ngetJson("https://httpbin.org/get").then(console.log);',
            "ts", "Fetch JSON and print one nested field; handle network errors."),
        day(7, "Classes & OOP lite", ["Classes", "Access modifiers", "Implements"],
            'interface Greeter { greet(): string }\nclass Person implements Greeter {\n  constructor(private name: string) {}\n  greet() { return `Hi ${this.name}`; }\n}\nconsole.log(new Person("Sam").greet());',
            "ts", "Build a `BankAccount` with deposit/withdraw and a private balance."),
        day(8, "Utility types", ["`Partial`", "`Pick`", "`Omit`", "`Readonly`"],
            'type User = { id: number; name: string; email: string };\ntype UserUpdate = Partial<Omit<User, "id">>;\nconst patch: UserUpdate = { email: "x@y.com" };\nconsole.log(patch);',
            "ts", "Design create/update DTOs for a Product using utility types."),
        day(9, "Strict mode habits", ["`strictNullChecks`", "Exhaustive switches", "Never"],
            'type Shape = { kind: "circle"; r: number } | { kind: "square"; s: number };\nfunction area(s: Shape): number {\n  switch (s.kind) {\n    case "circle": return Math.PI * s.r ** 2;\n    case "square": return s.s ** 2;\n  }\n}',
            "ts", "Add a `triangle` variant and make the compiler force you to handle it."),
        day(10, "Mini CLI tool", ["`process.argv`", "File I/O with `fs`", "JSON"],
            'import fs from "node:fs";\nconst path = process.argv[2] ?? "data.json";\nconst data = JSON.parse(fs.readFileSync(path, "utf8"));\nconsole.log(Object.keys(data));',
            "ts", "CLI that counts keys in a JSON file and writes a summary.md."),
    ],
    capstone="Build a typed **URL shortener client**: types for API responses, `fetch` wrapper, CLI to create/list links, and a README with example commands.",
    related=[("Getting Started with JavaScript", "/blog/2026/07/10/getting-started-with-javascript/"), ("JavaScript in 10 Days", "/courses/javascript-10-days/")],
)

add(
    slug="javascript-10-days",
    title="JavaScript in 10 Days — Hands-On",
    track="JavaScript",
    blurb="Modern JS from the console to a small Node script — no framework required.",
    why="JavaScript runs everywhere: browsers, Node, edge workers. Master the language before the frameworks.",
    setup="""Browser: DevTools console. Node:
```bash
node -v
mkdir js-lab && cd js-lab
```""",
    days=[
        day(1, "Values & control flow", ["Primitives", "`if`/`for`/`while`", "Template strings"],
            'const n = 5;\nfor (let i = 1; i <= n; i++) console.log(`#${i}`);',
            "js", "FizzBuzz 1–50."),
        day(2, "Functions & scope", ["Declarations vs arrows", "Closures", "Default params"],
            'const makeCounter = () => { let n = 0; return () => ++n; };\nconst c = makeCounter();\nconsole.log(c(), c());',
            "js", "Write `once(fn)` that only runs `fn` the first time."),
        day(3, "Arrays deep dive", ["`map`/`filter`/`reduce`", "Spread", "Destructuring"],
            'const nums = [1, 2, 3, 4];\nconst sum = nums.reduce((a, b) => a + b, 0);\nconst [a, ...rest] = nums;\nconsole.log(sum, a, rest);',
            "js", "From a list of users, return emails of active adults."),
        day(4, "Objects & JSON", ["Object literals", "`Object.keys`", "JSON parse/stringify"],
            'const user = { id: 1, name: "Riya" };\nconsole.log(JSON.stringify(user, null, 2));',
            "js", "Merge two config objects; later keys win."),
        day(5, "DOM basics", ["`querySelector`", "Events", "textContent"],
            'document.body.innerHTML = `<button id="b">Click</button><p id="o"></p>`;\ndocument.getElementById("b").onclick = () => {\n  document.getElementById("o").textContent = new Date().toISOString();\n};',
            "js", "Build a page with an input and a live character counter."),
        day(6, "Async JavaScript", ["Promises", "`async`/`await`", "`fetch`"],
            'const res = await fetch("https://httpbin.org/uuid");\nconst data = await res.json();\nconsole.log(data.uuid);',
            "js", "Parallel-fetch two URLs with `Promise.all` and print both."),
        day(7, "Modules in Node", ["ESM `import`", "`package.json` type module", "Exports"],
            '// package.json: { "type": "module" }\nexport const shout = (s) => s.toUpperCase();\nimport { shout } from "./shout.js";\nconsole.log(shout("hey"));',
            "js", "Split a word-frequency script into modules."),
        day(8, "Errors & debugging", ["`try`/`catch`", "Custom Error", "`console.table`"],
            'function parseAge(s) {\n  const n = Number(s);\n  if (!Number.isFinite(n)) throw new Error("bad age");\n  return n;\n}\ntry { console.log(parseAge("x")); } catch (e) { console.error(e.message); }',
            "js", "Validate a form object; collect all errors, don’t stop at first."),
        day(9, "Local storage mini-app", ["`localStorage`", "Events", "Render lists"],
            'const KEY = "todos";\nconst load = () => JSON.parse(localStorage.getItem(KEY) ?? "[]");\nconst save = (xs) => localStorage.setItem(KEY, JSON.stringify(xs));\nsave([...load(), { text: "ship it", done: false }]);\nconsole.log(load());',
            "js", "Todo list UI that survives refresh."),
        day(10, "Small Node CLI", ["`process.argv`", "`fs`", "Exit codes"],
            'import fs from "node:fs";\nconst file = process.argv[2];\nif (!file) { console.error("usage: node wc.js <file>"); process.exit(1); }\nconst text = fs.readFileSync(file, "utf8");\nconsole.log(text.trim().split(/\\s+/).length);',
            "js", "CLI that prints line/word/char counts like `wc`."),
    ],
    capstone="Ship a **browser + Node** pair: a notes app in the browser (localStorage) and a Node script that imports/exports notes as JSON.",
    related=[("TypeScript in 10 Days", "/courses/typescript-10-days/"), ("Getting Started with JavaScript", "/blog/2026/07/10/getting-started-with-javascript/")],
)

add(
    slug="rust-10-days",
    title="Rust in 10 Days — Hands-On",
    track="Rust",
    blurb="Ownership, types, and a CLI — learn Rust by compiling through the errors.",
    why="Rust gives C++-class performance with memory safety. Hot for systems, WASM, and CLI tools.",
    setup="""```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustc --version
cargo new rust-lab && cd rust-lab
cargo run
```""",
    days=[
        day(1, "Hello & cargo", ["`cargo new`", "`fn main`", "println!"],
            'fn main() {\n    let name = "Rust";\n    println!("Hello, {name}!");\n}',
            "rust", "Print your name and the current working directory hint via args later."),
        day(2, "Ownership basics", ["Move vs copy", "`String` vs `&str`", "Borrowing"],
            'fn len(s: &str) -> usize { s.len() }\nfn main() {\n    let s = String::from("hi");\n    println!("{}", len(&s));\n    println!("{s}"); // still usable\n}',
            "rust", "Write functions that take `&String` vs `String` and explain the difference."),
        day(3, "Structs & impl", ["Structs", "Methods", "Associated fns"],
            'struct Rect { w: u32, h: u32 }\nimpl Rect {\n    fn area(&self) -> u32 { self.w * self.h }\n}\nfn main() { println!("{}", Rect { w: 3, h: 4 }.area()); }',
            "rust", "Add `can_hold(&self, other: &Rect) -> bool`."),
        day(4, "Enums & match", ["`Option`", "`Result`", "Exhaustive match"],
            'fn parse(s: &str) -> Result<i32, String> {\n    s.parse().map_err(|_| format!("bad: {s}"))\n}\nfn main() {\n    match parse("42") {\n        Ok(n) => println!("{n}"),\n        Err(e) => eprintln!("{e}"),\n    }\n}',
            "rust", "CLI that parses ints from args and sums them; print errors for bad args."),
        day(5, "Collections", ["`Vec`", "`HashMap`", "Iterators"],
            'use std::collections::HashMap;\nfn main() {\n    let mut m = HashMap::new();\n    m.insert("a", 1);\n    let v: Vec<_> = (1..5).map(|x| x * x).collect();\n    println!("{:?} {:?}", m, v);\n}',
            "rust", "Word count over a string → HashMap."),
        day(6, "Error handling ergonomics", ["`?` operator", "`anyhow` optional", "Custom errors"],
            'use std::fs;\nfn read_n(path: &str) -> Result<usize, std::io::Error> {\n    let s = fs::read_to_string(path)?;\n    Ok(s.lines().count())\n}\nfn main() { println!("{:?}", read_n("Cargo.toml")); }',
            "rust", "Read a file and return line count; propagate IO errors with `?`."),
        day(7, "Traits", ["`Display`", "Custom traits", "Generics bounds"],
            'trait Summary { fn summarize(&self) -> String; }\nstruct Post { title: String }\nimpl Summary for Post {\n    fn summarize(&self) -> String { format!("Post: {}", self.title) }\n}\nfn main() { println!("{}", Post { title: "Hi".into() }.summarize()); }',
            "rust", "Trait `Area` for Circle and Rect; print both via trait object or generics."),
        day(8, "Modules & crates", ["`mod`", "`use`", "lib vs bin"],
            '// src/lib.rs\npub fn add(a: i32, b: i32) -> i32 { a + b }\n// src/main.rs\nuse rust_lab::add;\nfn main() { println!("{}", add(2, 3)); }',
            "rust", "Move helpers into `src/lib.rs` and call from `main`."),
        day(9, "Testing", ["`#[test]`", "`cargo test`", "Assert macros"],
            'pub fn add(a: i32, b: i32) -> i32 { a + b }\n#[cfg(test)]\nmod tests {\n    use super::*;\n    #[test]\n    fn adds() { assert_eq!(add(2, 2), 4); }\n}',
            "rust", "Tests for a `clamp(x, lo, hi)` function including edge cases."),
        day(10, "CLI with clap (manual argv ok)", ["Args", "Subcommands mindset", "Exit codes"],
            'fn main() {\n    let args: Vec<String> = std::env::args().skip(1).collect();\n    match args.as_slice() {\n        [cmd, path] if cmd == "wc" => {\n            let n = std::fs::read_to_string(path).unwrap().lines().count();\n            println!("{n}");\n        }\n        _ => eprintln!("usage: wc <path>"),\n    }\n}',
            "rust", "Extend with `grep <pat> <path>` printing matching lines."),
    ],
    capstone="Build a **todo CLI** in Rust: add/list/done stored in a JSON file, with `Result`-based error handling and tests for the store module.",
    related=[("C++ in 10 Days", "/courses/cpp-10-days/"), ("Go in 10 Days", "/courses/go-10-days/")],
)

add(
    slug="go-10-days",
    title="Go in 10 Days — Hands-On",
    track="Go",
    blurb="Idiomatic Go: packages, interfaces, concurrency, and a tiny HTTP API.",
    why="Go is the language of cloud services, CLIs, and Kubernetes-adjacent tooling. Simple, fast to ship.",
    setup="""```bash
go version   # 1.21+
mkdir go-lab && cd go-lab
go mod init example.com/golab
```""",
    days=[
        day(1, "Packages & fmt", ["`package main`", "go run", "Variables"],
            'package main\nimport "fmt"\nfunc main() {\n  name := "Go"\n  fmt.Printf("Hello, %s\\n", name)\n}',
            "go", "Print args from `os.Args`."),
        day(2, "Structs & methods", ["Structs", "Pointers", "Methods"],
            'type User struct{ Name string; Age int }\nfunc (u User) Greet() string { return "Hi " + u.Name }\nfunc main() { fmt.Println(User{"Ada", 36}.Greet()) }',
            "go", "BankAccount with Deposit/Withdraw methods."),
        day(3, "Interfaces", ["Implicit interfaces", "error", "io.Reader mindset"],
            'type Speaker interface{ Speak() string }\ntype Dog struct{}\nfunc (Dog) Speak() string { return "woof" }\nfunc say(s Speaker) { fmt.Println(s.Speak()) }\nfunc main() { say(Dog{}) }',
            "go", "Shape interface with Area(); Circle and Rect."),
        day(4, "Slices & maps", ["Append", "Range", "Maps"],
            'm := map[string]int{"a": 1}\nm["b"] = 2\nfor k, v := range m { fmt.Println(k, v) }',
            "go", "Word frequency counter over a string."),
        day(5, "Errors", ["`error` values", "Wrapping", "sentinel errors"],
            'func parse(s string) (int, error) {\n  var n int\n  _, err := fmt.Sscanf(s, "%d", &n)\n  return n, err\n}',
            "go", "Read a file; return wrapped errors with `%w`."),
        day(6, "Goroutines & channels", ["go keyword", "chan", "select intro"],
            'ch := make(chan string)\ngo func() { ch <- "ping" }()\nfmt.Println(<-ch)',
            "go", "Fan-out: 3 goroutines fetch fake work; collect results."),
        day(7, "Testing", ["`_test.go`", "table tests", "go test"],
            'func Add(a, b int) int { return a + b }\n// add_test.go\nfunc TestAdd(t *testing.T) {\n  if Add(2, 3) != 5 { t.Fatal("nope") }\n}',
            "go", "Table-driven tests for a Clamp function."),
        day(8, "HTTP server", ["net/http", "handlers", "JSON"],
            'http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {\n  w.Write([]byte(`{"ok":true}`))\n})\nlog.Fatal(http.ListenAndServe(":8080", nil))',
            "go", "Add POST /echo that returns the JSON body."),
        day(9, "Context & timeouts", ["context.Context", "WithTimeout", "Cancel"],
            'ctx, cancel := context.WithTimeout(context.Background(), time.Second)\ndefer cancel()\nselect {\ncase <-time.After(2 * time.Second):\ncase <-ctx.Done():\n  fmt.Println(ctx.Err())\n}',
            "go", "HTTP handler that respects request context cancellation."),
        day(10, "Small module layout", ["internal/", "cmd/", "go test ./..."],
            '// layout: cmd/api/main.go + internal/store/store.go\npackage store\ntype Mem struct{ data map[string]string }\nfunc New() *Mem { return &Mem{data: map[string]string{}} }',
            "go", "Split yesterday’s API into cmd + internal packages."),
    ],
    capstone="Build a **URL shortener API** in Go: in-memory store, POST create, GET redirect, tests for the store, README with curl examples. Then compare with the [Golang Bootcamp](/courses/golang-bootcamp/).",
    related=[("Golang Bootcamp", "/courses/golang-bootcamp/"), ("Rust in 10 Days", "/courses/rust-10-days/")],
)

add(
    slug="java-10-days",
    title="Java in 10 Days — Hands-On",
    track="Java",
    blurb="Modern Java: records, streams, and a tiny REST-shaped console app.",
    why="Java still powers enterprise backends, Android-adjacent ecosystems, and huge codebases. Learn the modern dialect.",
    setup="""Install JDK 17+.
```bash
java -version
javac -version
mkdir java-lab && cd java-lab
```""",
    days=[
        day(1, "Hello & javac", ["class/main", "compile/run", "vars"],
            'public class Main {\n  public static void main(String[] args) {\n    System.out.println("Hello Java");\n  }\n}',
            "java", "Print all command-line args."),
        day(2, "Classes & objects", ["Fields", "Constructors", "Methods"],
            'class User {\n  final String name;\n  User(String name) { this.name = name; }\n  String greet() { return "Hi " + name; }\n}',
            "java", "BankAccount with deposit/withdraw."),
        day(3, "Records & immutability", ["`record`", "equals/hashCode", "Compact ctor"],
            'record Point(int x, int y) {}\nvoid demo() { System.out.println(new Point(1, 2)); }',
            "java", "Record `Money(long cents)` with a method `plus`."),
        day(4, "Collections", ["List/Map/Set", "Generics", "for-each"],
            'var nums = List.of(1, 2, 3);\nvar m = new HashMap<String, Integer>();\nm.put("a", 1);',
            "java", "Word count with HashMap."),
        day(5, "Streams", ["map/filter/collect", "Optional", "method refs"],
            'var out = List.of(1,2,3,4).stream().filter(n -> n % 2 == 0).map(n -> n * n).toList();\nSystem.out.println(out);',
            "java", "From List<User>, collect emails of active users."),
        day(6, "Exceptions", ["checked vs unchecked", "try-with-resources", "custom"],
            'try (var r = new java.io.FileReader("a.txt")) {\n  // ...\n} catch (java.io.IOException e) {\n  System.err.println(e.getMessage());\n}',
            "java", "Read a file line count with try-with-resources."),
        day(7, "Interfaces & polymorphism", ["interface", "default methods", "implements"],
            'interface Greeter { String greet(); }\nrecord Person(String name) implements Greeter {\n  public String greet() { return "Hi " + name; }\n}',
            "java", "Shape interface; Circle/Rect implementations."),
        day(8, "Packages & modules lite", ["package decl", "classpath", "jar mindset"],
            '// com/example/Util.java\npackage com.example;\npublic class Util { public static int add(int a, int b) { return a + b; } }',
            "java", "Split Main and Util into packages; compile both."),
        day(9, "HTTP client", ["HttpClient", "URI", "JSON string handling"],
            'var client = java.net.http.HttpClient.newHttpClient();\nvar req = java.net.http.HttpRequest.newBuilder(java.net.URI.create("https://httpbin.org/get")).GET().build();\nvar res = client.send(req, java.net.http.HttpResponse.BodyHandlers.ofString());\nSystem.out.println(res.statusCode());',
            "java", "GET a URL and print status + first 200 chars of body."),
        day(10, "Mini service shape", ["Router-by-hand", "DTO records", "Main loop"],
            '// Console "API": commands add/list for todos in memory\nvar todos = new java.util.ArrayList<String>();\ntodos.add("learn java");\nSystem.out.println(todos);',
            "java", "REPL: `add <text>`, `list`, `quit` for todos."),
    ],
    capstone="Build a **todo CLI** with records, packages, and file persistence (JSON or CSV). Optional: expose the same store behind a tiny HTTP server.",
    related=[("Kotlin in 10 Days", "/courses/kotlin-10-days/"), ("C# in 10 Days", "/courses/csharp-10-days/")],
)

add(
    slug="kotlin-10-days",
    title="Kotlin in 10 Days — Hands-On",
    track="Kotlin",
    blurb="Concise JVM language: null-safety, data classes, coroutines intro, and a small script.",
    why="Kotlin is Android’s preferred language and a joy on the server (Ktor, Spring). Null-safety is built in.",
    setup="""Install Kotlin compiler or use IntelliJ. Or:
```bash
sdk install kotlin   # if using SDKMAN
kotlinc -version
```""",
    days=[
        day(1, "Hello Kotlin", ["`fun main`", "val/var", "string templates"],
            'fun main() {\n  val name = "Kotlin"\n  println("Hello, $name")\n}',
            "kotlin", "Read a name from `readln()` and greet."),
        day(2, "Null safety", ["`?`", "`?:`", "`?.`", "`!!` sparingly"],
            'fun len(s: String?): Int = s?.length ?: 0\nfun main() = println(len(null))',
            "kotlin", "Parse an Int from String?; return null on failure."),
        day(3, "Data classes", ["`data class`", "copy", "destructuring"],
            'data class User(val id: Int, val email: String)\nfun main() {\n  val u = User(1, "a@b.com")\n  println(u.copy(email = "x@y.com"))\n}',
            "kotlin", "Model Product; write a discounted copy helper."),
        day(4, "Collections", ["listOf/mutableList", "map/filter", "groupBy"],
            'val nums = listOf(1, 2, 3, 4)\nprintln(nums.filter { it % 2 == 0 }.map { it * it })',
            "kotlin", "Group words by first letter."),
        day(5, "Functions & extensions", ["Default args", "Named args", "Extension fns"],
            'fun String.shout(): String = uppercase()\nfun main() = println("hi".shout())',
            "kotlin", "Extension `List<Int>.median(): Double`."),
        day(6, "When & sealed", ["`when`", "sealed class/interface", "exhaustive"],
            'sealed interface Result\ndata class Ok(val n: Int) : Result\ndata object Err : Result\nfun show(r: Result) = when (r) {\n  is Ok -> println(r.n)\n  Err -> println("err")\n}',
            "kotlin", "Sealed hierarchy for UI state: Loading/Ready/Error."),
        day(7, "Classes & interfaces", ["class", "interface", "object singleton"],
            'interface Greeter { fun greet(): String }\nclass Person(val name: String) : Greeter {\n  override fun greet() = "Hi $name"\n}',
            "kotlin", "Implement a simple Repository interface with an in-memory object."),
        day(8, "File I/O", ["readText", "writeText", "use"],
            'import java.io.File\nfun main() {\n  File("out.txt").writeText("hello")\n  println(File("out.txt").readText())\n}',
            "kotlin", "Append timestamped lines to a log file."),
        day(9, "Coroutines intro", ["`runBlocking`", "`launch`", "`delay`"],
            '// needs kotlinx-coroutines\n// runBlocking { launch { delay(100); println("hi") }; println("start") }',
            "kotlin", "If deps are hard, simulate with threads; else launch 3 jobs and join."),
        day(10, "Mini CLI", ["args", "when commands", "mutable state"],
            'fun main(args: Array<String>) {\n  when (args.getOrNull(0)) {\n    "hello" -> println("hi ${args.getOrNull(1) ?: "world"}")\n    else -> println("usage: hello <name>")\n  }\n}',
            "kotlin", "Todo CLI: add/list/done with a text file store."),
    ],
    capstone="Build a **Kotlin todo CLI** with data classes, null-safe parsing, and file persistence. Optional: expose list via a tiny Ktor route.",
    related=[("Java in 10 Days", "/courses/java-10-days/"), ("Swift in 10 Days", "/courses/swift-10-days/")],
)

add(
    slug="swift-10-days",
    title="Swift in 10 Days — Hands-On",
    track="Swift",
    blurb="Modern Swift for Apple platforms and beyond — types, optionals, and a small CLI.",
    why="Swift is the language of iOS/macOS apps, with growing server-side use. Clear syntax and strong safety.",
    setup="""On macOS: Xcode or `swift` toolchain. On Linux: install Swift.org toolchain.
```bash
swift --version
mkdir SwiftLab && cd SwiftLab
swift package init --type executable
```""",
    days=[
        day(1, "Hello Swift", ["let/var", "print", "string interpolation"],
            'let name = "Swift"\nprint("Hello, \\(name)")',
            "swift", "Read a line and greet."),
        day(2, "Optionals", ["`?`", "`if let`", "`guard let`", "nil coalescing"],
            'func len(_ s: String?) -> Int { s?.count ?? 0 }\nprint(len(nil))',
            "swift", "Parse Int from String?; print message on failure."),
        day(3, "Structs & methods", ["struct", "mutating", "methods"],
            'struct Counter {\n  private(set) var n = 0\n  mutating func tick() { n += 1 }\n}',
            "swift", "BankAccount struct with deposit/withdraw."),
        day(4, "Enums", ["associated values", "switch", "exhaustive"],
            'enum Result { case ok(Int); case err(String) }\nfunc show(_ r: Result) {\n  switch r {\n  case .ok(let n): print(n)\n  case .err(let e): print(e)\n  }\n}',
            "swift", "Enum for HTTP method; print raw description."),
        day(5, "Collections", ["Array/Dict/Set", "map/filter", "for-in"],
            'let nums = [1, 2, 3, 4]\nprint(nums.filter { $0 % 2 == 0 }.map { $0 * $0 })',
            "swift", "Word frequency dictionary."),
        day(6, "Protocols", ["protocol", "conformance", "extensions"],
            'protocol Greeter { func greet() -> String }\nstruct Person: Greeter {\n  var name: String\n  func greet() -> String { "Hi \\(name)" }\n}',
            "swift", "Protocol Area for Circle and Rect."),
        day(7, "Error handling", ["`throws`", "`try`", "`do/catch`"],
            'enum ParseError: Error { case bad }\nfunc parse(_ s: String) throws -> Int {\n  guard let n = Int(s) else { throw ParseError.bad }\n  return n\n}',
            "swift", "Read a file and throw on missing path."),
        day(8, "Closures", ["trailing closures", "capture", "sorted(by:)"],
            'let xs = [3, 1, 2].sorted { $0 < $1 }\nprint(xs)',
            "swift", "Implement `once` using a closure flag."),
        day(9, "Async basics", ["async/await intro", "Task", "URLSession sketch"],
            '// async func load() async throws -> String { ... }\nprint("learn URLSession when on Apple platforms")',
            "swift", "Write an async function that sleeps and returns a string (Task.sleep)."),
        day(10, "CLI tool", ["CommandLine.arguments", "FileManager", "exit"],
            'let args = CommandLine.arguments\nguard args.count > 1 else { fputs("usage\\n", stderr); exit(1); }\nprint(args[1])',
            "swift", "wc-like line counter for a file path arg."),
    ],
    capstone="Build a **Swift todo CLI** with Codable JSON persistence, enums for commands, and clear error messages.",
    related=[("Kotlin in 10 Days", "/courses/kotlin-10-days/"), ("TypeScript in 10 Days", "/courses/typescript-10-days/")],
)

add(
    slug="cpp-10-days",
    title="C++ in 10 Days — Hands-On",
    track="C++",
    blurb="Modern C++17/20 essentials: RAII, STL, and a small CLI — without the legacy maze.",
    why="C++ still owns games, HFT-adjacent systems, browsers, and embedded. Learn modern C++, not 1998 C++.",
    setup="""```bash
g++ --version   # or clang++
mkdir cpp-lab && cd cpp-lab
```
Compile: `g++ -std=c++20 -O2 main.cpp -o main && ./main`""",
    days=[
        day(1, "Hello & build", ["main", "iostream", "compile flags"],
            '#include <iostream>\nint main() {\n  std::cout << "Hello C++\\n";\n}',
            "cpp", "Print argv."),
        day(2, "Types & references", ["auto", "refs", "const"],
            'void add1(int& x) { x += 1; }\nint main() { int n = 1; add1(n); std::cout << n; }',
            "cpp", "Swap two ints via references."),
        day(3, "Classes & RAII", ["ctor/dtor", "rule of zero", "private"],
            'class Counter {\n  int n_ = 0;\npublic:\n  void tick() { ++n_; }\n  int get() const { return n_; }\n};',
            "cpp", "BankAccount class with deposit/withdraw."),
        day(4, "STL vectors & algorithms", ["vector", "range-for", "sort"],
            '#include <vector>\n#include <algorithm>\nstd::vector<int> v{3,1,2};\nstd::sort(v.begin(), v.end());',
            "cpp", "Remove duplicates from a sorted vector."),
        day(5, "Maps & unordered_map", ["map", "count words", "structured bindings"],
            '#include <unordered_map>\n#include <string>\nstd::unordered_map<std::string,int> m;\nm["a"]++;',
            "cpp", "Word count over stdin lines."),
        day(6, "Smart pointers", ["unique_ptr", "shared_ptr", "make_unique"],
            '#include <memory>\nauto p = std::make_unique<int>(42);\nstd::cout << *p;',
            "cpp", "Factory returning unique_ptr to a Shape hierarchy."),
        day(7, "Optional & variants lite", ["optional", "nullopt", "value_or"],
            '#include <optional>\nstd::optional<int> parse(const std::string& s) {\n  try { return std::stoi(s); } catch (...) { return std::nullopt; }\n}',
            "cpp", "Parse many args; skip bad ones."),
        day(8, "Exceptions", ["try/catch", "what()", "RAII + exceptions"],
            'try { throw std::runtime_error("boom"); }\ncatch (const std::exception& e) { std::cerr << e.what(); }',
            "cpp", "File open wrapper that throws on failure."),
        day(9, "Headers & multi-file", ["header guards / #pragma once", "cpp files", "link"],
            '// add.h\n#pragma once\nint add(int a, int b);\n// add.cpp\nint add(int a, int b) { return a + b; }',
            "cpp", "Split a project into main.cpp + util.h/cpp; compile both."),
        day(10, "CLI tool", ["fstream", "stringstream", "exit codes"],
            '#include <fstream>\n#include <string>\nint main(int argc, char** argv) {\n  if (argc < 2) return 1;\n  std::ifstream in(argv[1]);\n  std::string line; int n = 0;\n  while (std::getline(in, line)) ++n;\n  std::cout << n << "\\n";\n}',
            "cpp", "Add word and char counts."),
    ],
    capstone="Build a **C++ todo CLI** using vector + file persistence, with a clean class boundary and C++20 compile flags documented in README.",
    related=[("Rust in 10 Days", "/courses/rust-10-days/"), ("Zig in 7 Days", "/courses/zig-7-days/")],
)

add(
    slug="csharp-10-days",
    title="C# in 10 Days — Hands-On",
    track="C#",
    blurb="Modern C# and .NET: records, LINQ, async, and a minimal web API sketch.",
    why="C#/.NET is hot for enterprise APIs, game tooling (Unity), and cross-platform backends.",
    setup="""Install [.NET SDK](https://dotnet.microsoft.com/):
```bash
dotnet --version
dotnet new console -n CsLab && cd CsLab
dotnet run
```""",
    days=[
        day(1, "Hello & SDK", ["top-level statements", "dotnet run", "strings"],
            'Console.WriteLine($"Hello C#");',
            "csharp", "Print args from `args`."),
        day(2, "Types & classes", ["class", "props", "methods"],
            'class User {\n  public required string Name { get; init; }\n  public string Greet() => $"Hi {Name}";\n}',
            "csharp", "BankAccount with deposit/withdraw."),
        day(3, "Records", ["record", "with", "equality"],
            'record Point(int X, int Y);\nvar p = new Point(1, 2) with { X = 3 };\nConsole.WriteLine(p);',
            "csharp", "Money record with Plus method."),
        day(4, "LINQ", ["Where/Select", "GroupBy", "ToList"],
            'var xs = new[] { 1, 2, 3, 4 };\nvar ys = xs.Where(n => n % 2 == 0).Select(n => n * n).ToList();\nConsole.WriteLine(string.Join(",", ys));',
            "csharp", "From users, select active emails."),
        day(5, "Collections", ["List/Dict", "foreach", "span mindset"],
            'var m = new Dictionary<string, int>();\nm["a"] = 1;\nforeach (var (k, v) in m) Console.WriteLine($"{k}={v}");',
            "csharp", "Word frequency counter."),
        day(6, "Async/await", ["Task", "HttpClient", "await"],
            'using var http = new HttpClient();\nvar s = await http.GetStringAsync("https://httpbin.org/uuid");\nConsole.WriteLine(s);',
            "csharp", "Fetch two URLs concurrently with Task.WhenAll."),
        day(7, "Exceptions & nullability", ["nullable refs", "try/catch", "pattern matching"],
            'string? s = null;\nConsole.WriteLine(s?.Length ?? 0);',
            "csharp", "Parse int; return null on failure using int?."),
        day(8, "Interfaces & DI mindset", ["interface", "impl", "ctor inject sketch"],
            'interface IClock { DateTime UtcNow { get; } }\nclass SystemClock : IClock { public DateTime UtcNow => DateTime.UtcNow; }',
            "csharp", "ITodoStore interface + in-memory implementation."),
        day(9, "Minimal API peek", ["WebApplication", "MapGet", "JSON"],
            '// dotnet new web -n ApiLab\n// app.MapGet("/health", () => Results.Ok(new { ok = true }));',
            "csharp", "Add POST /echo that returns the body."),
        day(10, "Files & CLI", ["File.ReadAllText", "args", "exit codes"],
            'if (args.Length == 0) { Console.Error.WriteLine("usage"); return 1; }\nvar text = File.ReadAllText(args[0]);\nConsole.WriteLine(text.Split().Length);',
            "csharp", "wc-like tool with line/word/char counts."),
    ],
    capstone="Build a **.NET todo API**: minimal APIs, in-memory store behind an interface, and a few integration-style tests or curl script.",
    related=[("Java in 10 Days", "/courses/java-10-days/"), ("TypeScript in 10 Days", "/courses/typescript-10-days/")],
)

add(
    slug="ruby-10-days",
    title="Ruby in 10 Days — Hands-On",
    track="Ruby",
    blurb="Elegant Ruby for scripts and web — blocks, Enumerable, and a tiny Sinatra-shaped app.",
    why="Ruby remains beloved for developer happiness, DevOps scripts, and Rails ecosystems.",
    setup="""```bash
ruby -v
gem install bundler
mkdir ruby-lab && cd ruby-lab
```""",
    days=[
        day(1, "Hello Ruby", ["puts", "vars", "string interp"],
            'name = "Ruby"\nputs "Hello, #{name}"',
            "ruby", "Read name from STDIN and greet."),
        day(2, "Arrays & hashes", ["[]", "each", "symbols"],
            'h = { a: 1, b: 2 }\nh.each { |k, v| puts "#{k}=#{v}" }',
            "ruby", "Word count hash."),
        day(3, "Methods & blocks", ["def", "yield", "blocks"],
            'def twice\n  yield\n  yield\nend\ntwice { puts "hi" }',
            "ruby", "Implement `once` with a block."),
        day(4, "Enumerable", ["map/select/reduce", "grep", "sort_by"],
            'puts [1,2,3,4].select(&:even?).map { |n| n * n }',
            "ruby", "Group words by length."),
        day(5, "Classes", ["initialize", "attr_reader", "instance methods"],
            'class User\n  attr_reader :name\n  def initialize(name) = @name = name\n  def greet = "Hi #{@name}"\nend',
            "ruby", "BankAccount class."),
        day(6, "Modules & mixins", ["module", "include", "extend"],
            'module Greeter\n  def greet = "Hi"\nend\nclass Person\n  include Greeter\nend',
            "ruby", "Mixin for logging timestamps."),
        day(7, "File I/O", ["File.read", "File.write", "each_line"],
            'File.write("out.txt", "hello")\nputs File.read("out.txt")',
            "ruby", "Count lines in a file path from ARGV."),
        day(8, "Exceptions", ["begin/rescue", "raise", "ensure"],
            'begin\n  Integer("x")\nrescue ArgumentError => e\n  warn e.message\nend',
            "ruby", "Validate a hash of form fields; collect errors."),
        day(9, "Gems & Bundler", ["Gemfile", "bundle exec", "require"],
            '# Gemfile\n# source "https://rubygems.org"\n# gem "json"',
            "ruby", "Create Gemfile; require json; pretty-print a hash."),
        day(10, "Tiny web sketch", ["WEBrick or Sinatra", "routes", "JSON"],
            'require "webrick"\nserver = WEBrick::HTTPServer.new(Port: 8000)\nserver.mount_proc("/health") { |_req, res| res.body = \'{"ok":true}\' }\ntrap("INT") { server.shutdown }\nserver.start',
            "ruby", "Add /echo POST that returns body."),
    ],
    capstone="Build a **Ruby todo CLI** with JSON persistence, then optionally wrap list/add in WEBrick routes.",
    related=[("Python in 10 Days", "/courses/python-10-days/"), ("PHP in 10 Days", "/courses/php-10-days/")],
)

add(
    slug="php-10-days",
    title="PHP in 10 Days — Hands-On",
    track="PHP",
    blurb="Modern PHP 8: types, Composer, and a tiny JSON API without a heavy framework.",
    why="PHP still runs a huge share of the web. Modern PHP is typed, fast, and pleasant with Composer.",
    setup="""```bash
php -v   # 8.1+
mkdir php-lab && cd php-lab
```""",
    days=[
        day(1, "Hello PHP", ["<?php", "echo", "vars"],
            '<?php\n$name = "PHP";\necho "Hello, $name\\n";',
            "php", "Print CLI args from `$argv`."),
        day(2, "Types & functions", ["type hints", "return types", "strict_types"],
            '<?php\ndeclare(strict_types=1);\nfunction add(int $a, int $b): int { return $a + $b; }\necho add(2, 3);',
            "php", "Write `clamp(float $x, float $lo, float $hi): float`."),
        day(3, "Arrays", ["lists", "assoc", "foreach"],
            '<?php\n$m = ["a" => 1, "b" => 2];\nforeach ($m as $k => $v) echo "$k=$v\\n";',
            "php", "Word frequency array."),
        day(4, "Classes", ["constructor", "props", "methods"],
            '<?php\nclass User {\n  public function __construct(public string $name) {}\n  public function greet(): string { return "Hi {$this->name}"; }\n}',
            "php", "BankAccount class."),
        day(5, "Composer", ["composer.json", "autoload", "vendor"],
            '{\n  "name": "lab/php",\n  "autoload": { "psr-4": { "Lab\\\\": "src/" } }\n}',
            "php", "PSR-4 class Lab\\\\Math\\\\Add and require vendor/autoload.php."),
        day(6, "Exceptions", ["try/catch", "throw", "custom"],
            '<?php\ntry {\n  throw new RuntimeException("boom");\n} catch (Throwable $e) {\n  fwrite(STDERR, $e->getMessage());\n}',
            "php", "Parse int helper that throws on bad input."),
        day(7, "Files & JSON", ["file_get_contents", "json_encode", "JSON_THROW_ON_ERROR"],
            '<?php\n$data = ["ok" => true];\nfile_put_contents("out.json", json_encode($data, JSON_PRETTY_PRINT));',
            "php", "Read JSON file into array; print a field."),
        day(8, "Built-in server", ["php -S", "router script", "superglobals"],
            '<?php\n// router.php\nif ($_SERVER["REQUEST_URI"] === "/health") {\n  header("Content-Type: application/json");\n  echo json_encode(["ok" => true]);\n  return true;\n}\nreturn false;',
            "php", "`php -S localhost:8000 router.php` and hit /health."),
        day(9, "PDO lite", ["SQLite PDO", "prepare", "execute"],
            '<?php\n$pdo = new PDO("sqlite::memory:");\n$pdo->exec("CREATE TABLE t(id INTEGER PRIMARY KEY, name TEXT)");\n$pdo->prepare("INSERT INTO t(name) VALUES (?)")->execute(["Ada"]);',
            "php", "Create todos table; insert and list rows."),
        day(10, "Mini JSON API", ["POST body", "status codes", "routing"],
            '<?php\n// extend router: POST /todos reads php://input JSON and appends to file store',
            "php", "Implement GET/POST /todos with a JSON file store."),
    ],
    capstone="Ship a **PHP todo JSON API** on the built-in server with Composer autoload, typed classes, and SQLite or file persistence.",
    related=[("SQL in 10 Days", "/courses/sql-10-days/"), ("JavaScript in 10 Days", "/courses/javascript-10-days/")],
)

add(
    slug="sql-10-days",
    title="SQL in 10 Days — Hands-On",
    track="SQL",
    blurb="Query fluency with SQLite: joins, windows, and a tiny analytics project.",
    why="Every backend and data role speaks SQL. Master it once; transfer everywhere.",
    setup="""```bash
sqlite3 --version
sqlite3 learning.db
```
Or use any Postgres — dialect notes call out differences.""",
    days=[
        day(1, "SELECT basics", ["SELECT/FROM/WHERE", "ORDER BY", "LIMIT"],
            'SELECT id, title FROM posts WHERE published = 1 ORDER BY id DESC LIMIT 5;',
            "sql", "Create a `people(name, age)` table; insert 5 rows; query adults."),
        day(2, "INSERT/UPDATE/DELETE", ["mutations", "transactions", "BEGIN/COMMIT"],
            "BEGIN;\nUPDATE people SET age = age + 1 WHERE name = 'Ada';\nCOMMIT;",
            "sql", "Transaction that inserts two related rows or rolls back."),
        day(3, "JOINs", ["INNER", "LEFT", "ON"],
            "SELECT u.name, p.title\nFROM users u\nJOIN posts p ON p.author_id = u.id;",
            "sql", "Blog schema: users/posts/comments; list comments with names."),
        day(4, "GROUP BY", ["COUNT/SUM", "HAVING", "aggregates"],
            "SELECT author_id, COUNT(*) AS n FROM posts GROUP BY author_id HAVING n >= 2;",
            "sql", "Top 5 commenters."),
        day(5, "Subqueries", ["IN", "EXISTS", "scalar subquery"],
            "SELECT name FROM users u\nWHERE EXISTS (SELECT 1 FROM posts p WHERE p.author_id = u.id);",
            "sql", "Users with zero posts via NOT EXISTS."),
        day(6, "Indexes & EXPLAIN", ["CREATE INDEX", "EXPLAIN QUERY PLAN", "when indexes help"],
            "CREATE INDEX idx_posts_author ON posts(author_id);\nEXPLAIN QUERY PLAN SELECT * FROM posts WHERE author_id = 1;",
            "sql", "Add an index that speeds a slow filter you invent."),
        day(7, "Window functions", ["ROW_NUMBER", "RANK", "SUM OVER"],
            "SELECT title, author_id,\n  ROW_NUMBER() OVER (PARTITION BY author_id ORDER BY id) AS rn\nFROM posts;",
            "sql", "Running total of amounts by day."),
        day(8, "CTEs", ["WITH", "readable pipelines", "recursive peek"],
            "WITH active AS (\n  SELECT * FROM users WHERE active = 1\n)\nSELECT * FROM active;",
            "sql", "Rewrite a nested subquery as a CTE."),
        day(9, "Views & constraints", ["VIEW", "UNIQUE", "FOREIGN KEY", "CHECK"],
            "CREATE VIEW post_counts AS\nSELECT author_id, COUNT(*) AS n FROM posts GROUP BY author_id;",
            "sql", "Enforce FK from comments to posts; try a bad insert."),
        day(10, "Analytics mini-project", ["star schema lite", "funnel query", "export"],
            "-- events(user_id, event, ts)\n-- count signup -> activate -> purchase",
            "sql", "Design events table; write a 3-step funnel count."),
    ],
    capstone="Model a **SaaS metrics** SQLite DB (users, accounts, events). Write 5 reporting queries (DAU, top accounts, funnel, retention sketch) in a `queries.sql` file.",
    related=[("Getting Started with SQL", "/blog/2026/07/10/getting-started-with-sql/"), ("Python in 10 Days", "/courses/python-10-days/")],
)

add(
    slug="zig-7-days",
    title="Zig in 7 Days — Hands-On",
    track="Zig",
    blurb="A rising systems language: explicit allocators, comptime, and a tiny CLI.",
    why="Zig is hot among systems programmers who want C interop without C footguns. Great for tooling and WASM.",
    setup="""Install from https://ziglang.org/
```bash
zig version
mkdir zig-lab && cd zig-lab
zig init-exe
zig build run
```""",
    days=[
        day(1, "Hello Zig", ["pub fn main", "print", "build"],
            'const std = @import("std");\npub fn main() void {\n    std.debug.print("Hello Zig\\n", .{});\n}',
            "zig", "Print a number and a string."),
        day(2, "Types & errors", ["u32/i32", "error unions", "`try`/`catch`"],
            'fn parse() !u32 { return 42; }\npub fn main() void {\n    const n = parse() catch 0;\n    _ = n;\n}',
            "zig", "Function that returns error on bad input string length."),
        day(3, "Allocators", ["page_allocator", "ArrayList", "defer"],
            'var gpa = std.heap.GeneralPurposeAllocator(.{}){};\ndefer _ = gpa.deinit();\nconst a = gpa.allocator();',
            "zig", "Build a dynamic list of integers and print them."),
        day(4, "Structs", ["struct", "methods", "fields"],
            'const Point = struct { x: i32, y: i32 };\nvar p = Point{ .x = 1, .y = 2 };\n_ = p;',
            "zig", "Rect with area method."),
        day(5, "Comptime peek", ["comptime", "inline", "type params lite"],
            'fn max(comptime T: type, a: T, b: T) T {\n    return if (a > b) a else b;\n}',
            "zig", "Comptime max for i32 and f64 calls."),
        day(6, "Files", ["cwd", "readFileAlloc", "write"],
            '// use std.fs.cwd().readFileAlloc(allocator, path, max)\nstd.debug.print("read a file next\\n", .{});',
            "zig", "Line-count a file path from args."),
        day(7, "CLI tool", ["args", "exit", "build.zig mindset"],
            'var it = try std.process.argsWithAllocator(allocator);\ndefer it.deinit();\n_ = it.skip();',
            "zig", "wc-like tool: lines for a path argument."),
    ],
    capstone="Build a **Zig grep-lite**: read a file, print lines containing a pattern, with explicit allocator and error handling.",
    related=[("Rust in 10 Days", "/courses/rust-10-days/"), ("C++ in 10 Days", "/courses/cpp-10-days/")],
)

add(
    slug="bash-7-days",
    title="Bash in 7 Days — Hands-On",
    track="Bash",
    blurb="Shell scripting for real work: globs, pipes, scripts, and safe automation.",
    why="Every server, container, and CI job speaks shell. Automate the boring glue.",
    setup="""Any Linux/macOS terminal:
```bash
bash --version
mkdir bash-lab && cd bash-lab
```""",
    days=[
        day(1, "Navigation & files", ["cd/ls/cp/mv", "globs", "permissions"],
            '#!/usr/bin/env bash\nset -euo pipefail\necho "PWD=$PWD"\nls -la',
            "bash", "Script that creates `out/` and copies `*.txt` into it."),
        day(2, "Variables & quoting", ["$VAR", "\"$VAR\"", "arrays"],
            'name="Ada Lovelace"\necho "Hello, $name"\nfiles=(a.txt b.txt)\necho "${files[0]}"',
            "bash", "Script taking a name arg; exit 1 if missing."),
        day(3, "Pipes & filters", ["grep/sed/awk", "sort/uniq", "cut"],
            'printf "b\\na\\nb\\n" | sort | uniq -c',
            "bash", "From a fake log, top 5 IPs."),
        day(4, "Control flow", ["if", "for", "while", "case"],
            'for f in *.md; do echo "FILE=$f"; done',
            "bash", "Loop files; print size via `wc -c`."),
        day(5, "Functions & set -euo", ["functions", "pipefail", "trap"],
            'die() { echo "$*" >&2; exit 1; }\nneed_cmd() { command -v "$1" >/dev/null || die "missing $1"; }\nneed_cmd curl',
            "bash", "Script that checks for git/curl/jq before running."),
        day(6, "JSON & HTTP", ["curl", "jq", "exit codes"],
            'curl -s https://httpbin.org/uuid | jq -r .uuid',
            "bash", "Fetch UUID; write to `id.txt`; fail if empty."),
        day(7, "Real automation", ["cron mindset", "logging", "idempotent scripts"],
            'log() { echo "$(date -Is) $*"; }\nlog "start backup"\n# rsync -a ./data/ ./backup/',
            "bash", "Idempotent backup script: copy `data/` → `backup/` only if source newer."),
    ],
    capstone="Write a **project bootstrap script**: create dirs, check deps, write a `.env.example`, and print next steps. Use `set -euo pipefail` throughout.",
    related=[("Getting Started with Linux Shell", "/blog/2026/07/10/getting-started-with-linux-shell/"), ("Docker getting started", "/blog/2026/07/10/getting-started-with-docker/")],
)


def write_hub(langs: list[dict]) -> None:
    cards = []
    toc = []
    for L in langs:
        slug = L["slug"]
        title = L["title"]
        days = len(L["days"])
        toc.append(f'  - id: "{slug}"\n    label: "{L["track"]} ({days} days)"')
        cards.append(
            f"""### {L['track']}
{{: #{slug} }}

**[{title}](/courses/{slug}/)** — {L['blurb']}

"""
        )

    hub = f"""---
layout: course
title: "Hot Languages — Hands-On Tutorials"
permalink: /courses/languages/
course_track: "Languages"
description: "Hands-on multi-day tutorials for TypeScript, JavaScript, Rust, Go, Java, Kotlin, Swift, C++, C#, Ruby, PHP, SQL, Zig, and Bash."
toc:
  - id: "how-to-use"
    label: "How to use"
{chr(10).join(toc)}
  - id: "also-on-site"
    label: "Also on this site"
---

# Hot languages — hands-on tutorials

Pick a language. Type every example. Ship the capstone. No slide decks.

## How to use
{{: #how-to-use }}

1. One day ≈ 45–90 minutes.
2. Do the **task** before peeking at solutions online.
3. Keep a single repo `language-lab/` with a folder per language.
4. After the sprint, build something you’d show in an interview.

{"".join(cards)}

## Also on this site
{{: #also-on-site }}

- [Python in 10 Days](/courses/python-10-days/) (already published)
- [Python Bootcamp](/courses/python-bootcamp/)
- [Golang Bootcamp](/courses/golang-bootcamp/)
- [LLM Mastery](/courses/llm-mastery/)
- Getting started blogs: [Python](/blog/2026/07/10/getting-started-with-python/), [Git](/blog/2026/07/10/getting-started-with-git/), [Docker](/blog/2026/07/10/getting-started-with-docker/), [PyTorch](/blog/2026/07/10/getting-started-with-pytorch/), [FastAPI](/blog/2026/07/10/getting-started-with-fastapi/)

[All courses](/courses/)
"""
    (COURSES / "languages.md").write_text(hub, encoding="utf-8")


def main() -> None:
    write_hub(LANGS)
    for L in LANGS:
        path = COURSES / f"{L['slug']}.md"
        text = render_course(
            slug=L["slug"],
            title=L["title"],
            track=L["track"],
            blurb=L["blurb"],
            why=L["why"],
            setup=L["setup"],
            days=L["days"],
            capstone=L["capstone"],
            related=L["related"],
        )
        path.write_text(text, encoding="utf-8")
        print("wrote", path.relative_to(ROOT))

    post = POSTS / "2026-07-10-hot-language-hands-on-tutorials.md"
    links = "\n".join(
        f"- [{L['track']}](/courses/{L['slug']}/) — {len(L['days'])} days"
        for L in LANGS
    )
    post.write_text(
        f"""---
layout: post
title: "Hot language hands-on tutorials (TypeScript, Rust, Go, and more)"
date: 2026-07-10
description: "Multi-day hands-on courses for the languages teams actually hire for — plus SQL, Zig, and Bash."
tags: [languages, tutorials, getting-started]
---

We published a full **[Languages hub](/courses/languages/)** with hands-on sprints:

{links}

- [Python in 10 Days](/courses/python-10-days/) (already on the site)

Each course has daily code-alongs, a concrete task, and a capstone. Start at the hub and pick one language this week.
""",
        encoding="utf-8",
    )
    print("wrote", post.relative_to(ROOT))
    print(f"DONE {len(LANGS)} language courses")


if __name__ == "__main__":
    main()
