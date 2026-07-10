---
layout: course
title: "Rust in 10 Days — Hands-On"
permalink: /courses/rust-10-days/
course_track: "Rust"
description: "Ownership, types, and a CLI — learn Rust by compiling through the errors."
toc:
  - id: "day-1-hello-cargo"
    label: "Day 1: Hello & cargo"
  - id: "day-2-ownership-basics"
    label: "Day 2: Ownership basics"
  - id: "day-3-structs-impl"
    label: "Day 3: Structs & impl"
  - id: "day-4-enums-match"
    label: "Day 4: Enums & match"
  - id: "day-5-collections"
    label: "Day 5: Collections"
  - id: "day-6-error-handling-ergonomics"
    label: "Day 6: Error handling ergonomics"
  - id: "day-7-traits"
    label: "Day 7: Traits"
  - id: "day-8-modules-crates"
    label: "Day 8: Modules & crates"
  - id: "day-9-testing"
    label: "Day 9: Testing"
  - id: "day-10-cli-with-clap-manual-argv-ok"
    label: "Day 10: CLI with clap (manual argv ok)"
  - id: "capstone"
    label: "Capstone project"
---

# Rust in 10 Days — Hands-On

Ownership, types, and a CLI — learn Rust by compiling through the errors.

## Why this language
{: #why-this-language }

Rust gives C++-class performance with memory safety. Hot for systems, WASM, and CLI tools.

## Setup (Day 0)
{: #setup-day-0 }

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustc --version
cargo new rust-lab && cd rust-lab
cargo run
```

---

## Day 1: Hello & cargo
{: #day-1-hello-cargo }

### What you'll learn

- `cargo new`
- `fn main`
- println!

### Code along

```rust
fn main() {
    let name = "Rust";
    println!("Hello, {name}!");
}
```

### Your task

Print your name and the current working directory hint via args later.

---

## Day 2: Ownership basics
{: #day-2-ownership-basics }

### What you'll learn

- Move vs copy
- `String` vs `&str`
- Borrowing

### Code along

```rust
fn len(s: &str) -> usize { s.len() }
fn main() {
    let s = String::from("hi");
    println!("{}", len(&s));
    println!("{s}"); // still usable
}
```

### Your task

Write functions that take `&String` vs `String` and explain the difference.

---

## Day 3: Structs & impl
{: #day-3-structs-impl }

### What you'll learn

- Structs
- Methods
- Associated fns

### Code along

```rust
struct Rect { w: u32, h: u32 }
impl Rect {
    fn area(&self) -> u32 { self.w * self.h }
}
fn main() { println!("{}", Rect { w: 3, h: 4 }.area()); }
```

### Your task

Add `can_hold(&self, other: &Rect) -> bool`.

---

## Day 4: Enums & match
{: #day-4-enums-match }

### What you'll learn

- `Option`
- `Result`
- Exhaustive match

### Code along

```rust
fn parse(s: &str) -> Result<i32, String> {
    s.parse().map_err(|_| format!("bad: {s}"))
}
fn main() {
    match parse("42") {
        Ok(n) => println!("{n}"),
        Err(e) => eprintln!("{e}"),
    }
}
```

### Your task

CLI that parses ints from args and sums them; print errors for bad args.

---

## Day 5: Collections
{: #day-5-collections }

### What you'll learn

- `Vec`
- `HashMap`
- Iterators

### Code along

```rust
use std::collections::HashMap;
fn main() {
    let mut m = HashMap::new();
    m.insert("a", 1);
    let v: Vec<_> = (1..5).map(|x| x * x).collect();
    println!("{:?} {:?}", m, v);
}
```

### Your task

Word count over a string → HashMap.

---

## Day 6: Error handling ergonomics
{: #day-6-error-handling-ergonomics }

### What you'll learn

- `?` operator
- `anyhow` optional
- Custom errors

### Code along

```rust
use std::fs;
fn read_n(path: &str) -> Result<usize, std::io::Error> {
    let s = fs::read_to_string(path)?;
    Ok(s.lines().count())
}
fn main() { println!("{:?}", read_n("Cargo.toml")); }
```

### Your task

Read a file and return line count; propagate IO errors with `?`.

---

## Day 7: Traits
{: #day-7-traits }

### What you'll learn

- `Display`
- Custom traits
- Generics bounds

### Code along

```rust
trait Summary { fn summarize(&self) -> String; }
struct Post { title: String }
impl Summary for Post {
    fn summarize(&self) -> String { format!("Post: {}", self.title) }
}
fn main() { println!("{}", Post { title: "Hi".into() }.summarize()); }
```

### Your task

Trait `Area` for Circle and Rect; print both via trait object or generics.

---

## Day 8: Modules & crates
{: #day-8-modules-crates }

### What you'll learn

- `mod`
- `use`
- lib vs bin

### Code along

```rust
// src/lib.rs
pub fn add(a: i32, b: i32) -> i32 { a + b }
// src/main.rs
use rust_lab::add;
fn main() { println!("{}", add(2, 3)); }
```

### Your task

Move helpers into `src/lib.rs` and call from `main`.

---

## Day 9: Testing
{: #day-9-testing }

### What you'll learn

- `#[test]`
- `cargo test`
- Assert macros

### Code along

```rust
pub fn add(a: i32, b: i32) -> i32 { a + b }
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn adds() { assert_eq!(add(2, 2), 4); }
}
```

### Your task

Tests for a `clamp(x, lo, hi)` function including edge cases.

---

## Day 10: CLI with clap (manual argv ok)
{: #day-10-cli-with-clap-manual-argv-ok }

### What you'll learn

- Args
- Subcommands mindset
- Exit codes

### Code along

```rust
fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    match args.as_slice() {
        [cmd, path] if cmd == "wc" => {
            let n = std::fs::read_to_string(path).unwrap().lines().count();
            println!("{n}");
        }
        _ => eprintln!("usage: wc <path>"),
    }
}
```

### Your task

Extend with `grep <pat> <path>` printing matching lines.


---

## Capstone project
{: #capstone }

Build a **todo CLI** in Rust: add/list/done stored in a JSON file, with `Result`-based error handling and tests for the store module.

## Related

- [C++ in 10 Days](/courses/cpp-10-days/)
- [Go in 10 Days](/courses/go-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
