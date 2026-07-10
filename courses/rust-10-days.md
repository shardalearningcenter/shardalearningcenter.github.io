---
layout: course
title: "Rust in 10 Days — Hands-On"
permalink: /courses/rust-10-days/
course_track: "Rust"
description: "Ownership, structs, traits, and error handling — learn Rust by reading the compiler's errors, not by avoiding them."
toc:
  - id: "why-this-language"
    label: "Why this language"
  - id: "setup-day-0"
    label: "Setup (Day 0)"
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

Ownership, types, and a CLI. Rust's compiler is strict because it's catching bugs other languages let you ship — every error message here is explained, not skipped past.

## Why this language
{: #why-this-language }

Rust gives you C++-class performance without a garbage collector, and it does it by catching memory bugs (use-after-free, data races, null derefs) at compile time instead of at 3am in production. That's why it's become the default choice for CLIs, WASM, and performance-sensitive systems code. The tradeoff is a steeper learning curve up front — the borrow checker rejects code that "looks fine" until you understand why it isn't. This course leans into that: you'll hit real compiler errors and learn to read them, because that's the actual skill.

## Setup (Day 0)
{: #setup-day-0 }

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
rustc --version              # expect 1.75+
cargo new rust-lab && cd rust-lab
cargo run
```

Expected final output: `Hello, world!`. This confirms `rustc`, `cargo`, and the linker are all working — if `cargo run` fails at the linker step on Linux, install build essentials (`sudo apt install build-essential` on Debian/Ubuntu) and retry.

Each day below lives in `rust-lab/src/bin/dayNN.rs` (Cargo auto-discovers files in `src/bin/` as separate executables). Run a specific day with `cargo run --bin dayNN`. Create the `src/bin/` directory now:

```bash
mkdir -p src/bin
```

**Checkpoint:** `cargo run --bin day01` after creating `src/bin/day01.rs` with a `fn main() {}` should compile and exit with no output, confirming the multi-binary layout works before you write real code.

---

## Day 1: Hello & cargo
{: #day-1-hello-cargo }

### Why this matters

`cargo` is Rust's build tool, package manager, and test runner in one — you'll use it every single day you write Rust. Getting comfortable with `cargo run`, `cargo build`, and `cargo check` now saves confusion later.

### Mental model

`cargo check` type-checks without producing a binary — much faster than a full build, use it constantly while iterating. `cargo run` builds (if needed) and runs. There's no implicit "main file runs on save" — you always explicitly build or run.

### Code along

```rust
// src/bin/day01.rs
fn main() {
    let name = "Rust";
    let version = 2026;
    println!("Hello, {name}! Learning in {version}.");

    let args: Vec<String> = std::env::args().collect();
    println!("Binary path: {}", args[0]);
    if args.len() > 1 {
        println!("You passed {} extra argument(s): {:?}", args.len() - 1, &args[1..]);
    } else {
        println!("No extra arguments. Try: cargo run --bin day01 -- foo bar");
    }
}
```

Run it two ways:

```bash
cargo run --bin day01
cargo run --bin day01 -- foo bar
```

Expected output (second run):

```
Hello, Rust! Learning in 2026.
Binary path: target/debug/day01
You passed 2 extra argument(s): ["foo", "bar"]
```

### Common mistake

Running `cargo run --bin day01 foo bar` (forgetting the `--` separator) — Cargo tries to interpret `foo` as a Cargo subcommand/flag instead of passing it to your program, and you get `error: unexpected argument 'foo' found`. Everything after `--` goes to *your* binary; everything before it is for Cargo itself. This trips up everyone the first week.

### Your task

Print `args[0]` (the binary path) split on the OS path separator, showing just the filename (hint: `std::path::Path::new(&args[0]).file_name()`).

**Check:** running `cargo run --bin day01` prints just `day01` (or `day01.exe` on Windows) as the binary name, not the full path.

---

## Day 2: Ownership basics
{: #day-2-ownership-basics }

### Why this matters

Ownership is the one idea that makes Rust different from every mainstream language, and it's what lets the compiler guarantee memory safety without a garbage collector. Every confusing compiler error in your first weeks traces back to this one rule: a value has exactly one owner, and when the owner goes out of scope, the value is dropped.

### Mental model

Assigning a `String` (heap-allocated, owned data) to a new variable **moves** it — the old variable becomes invalid. Passing by `&reference` **borrows** it temporarily without taking ownership. `Copy` types (integers, `bool`, `char`) are duplicated instead of moved, which is why `let x = 5; let y = x;` leaves both `x` and `y` valid but the `String` equivalent does not.

### Code along

```rust
// src/bin/day02.rs
fn word_count(s: &str) -> usize {
    s.split_whitespace().count()
}

fn shout(s: String) -> String {
    s.to_uppercase()
}

fn main() {
    let greeting = String::from("hello there rust learner");

    // Borrowing: greeting is still usable after this call.
    println!("Word count: {}", word_count(&greeting));
    println!("Still have it: {greeting}");

    // Moving: passing `greeting` by value transfers ownership into `shout`.
    let loud = shout(greeting);
    println!("{loud}");

    // Uncommenting the next line would fail to compile:
    // println!("{greeting}"); // error[E0382]: borrow of moved value: `greeting`
}
```

Expected output:

```
Word count: 4
Still have it: hello there rust learner
HELLO THERE RUST LEARNER
```

### Common mistake

Uncommenting that last line and trying to use `greeting` after it was moved into `shout`. The compiler rejects it with `error[E0382]: borrow of moved value: 'greeting'`, and — this is the important part — it tells you exactly where the move happened (`value moved here`) and where you tried to use it afterward. Read that error message top to bottom; it's not vague, it's pointing at the two exact lines involved. The fix is almost always: borrow (`&greeting`) if you don't need ownership, or `.clone()` if you genuinely need two independent copies.

### Your task

Write `first_word(s: &str) -> &str` that returns a slice of the first word without allocating a new `String`. Call it on `greeting` both before and after `shout(greeting)` consumes it (adjust the order so the borrow happens first) and print the result each time.

**Check:** `first_word("hello there")` returns `"hello"`; the code compiles cleanly with `cargo check` because `first_word` only ever borrows, never takes ownership.

---

## Day 3: Structs & impl
{: #day-3-structs-impl }

### Why this matters

Structs plus `impl` blocks are how Rust organizes data and behavior together without classes or inheritance. Getting comfortable with `&self` vs `self` vs `&mut self` in method signatures is central to writing Rust that compiles on the first (or third) try.

### Mental model

`&self` borrows immutably (read-only method), `&mut self` borrows mutably (can modify fields), and `self` (no `&`) consumes the struct entirely — use that last one rarely, mainly for conversions. Associated functions (no `self` parameter, like `Rect::new(...)`) are Rust's equivalent of static factory methods.

### Code along

```rust
// src/bin/day03.rs
struct Rect {
    width: u32,
    height: u32,
}

impl Rect {
    fn new(width: u32, height: u32) -> Self {
        Rect { width, height }
    }

    fn area(&self) -> u32 {
        self.width * self.height
    }

    fn can_hold(&self, other: &Rect) -> bool {
        self.width >= other.width && self.height >= other.height
    }

    fn scale(&mut self, factor: u32) {
        self.width *= factor;
        self.height *= factor;
    }
}

fn main() {
    let mut a = Rect::new(10, 20);
    let b = Rect::new(5, 5);

    println!("a area: {}", a.area());
    println!("a can hold b: {}", a.can_hold(&b));
    println!("b can hold a: {}", b.can_hold(&a));

    a.scale(2);
    println!("a after scale: {}x{} (area {})", a.width, a.height, a.area());
}
```

Expected output:

```
a area: 200
a can hold b: true
b can hold a: false
a after scale: 20x40 (area 800)
```

### Common mistake

Calling `a.scale(2)` on an `a` declared with `let a = Rect::new(...)` (no `mut`). The compiler rejects it: `error[E0596]: cannot borrow 'a' as mutable, as it is not declared as mutable`, with a suggestion to add `mut`. This isn't Rust being pedantic — it's the compiler statically proving that nothing else could have expected `a` to stay constant, because you told it up front whether `a` was allowed to change.

### Your task

Add a method `aspect_ratio(&self) -> f64` returning `width as f64 / height as f64`, and a method `is_square(&self) -> bool`. Test both on `a` before and after scaling.

**Check:** `Rect::new(10, 20).aspect_ratio()` returns `0.5`; `Rect::new(7, 7).is_square()` returns `true`; scaling a rectangle uniformly (same factor on both dimensions) never changes its aspect ratio — verify this holds for `a` before/after `scale(2)`.

---

## Day 4: Enums & match
{: #day-4-enums-match }

### Why this matters

`Option` and `Result` are how Rust eliminates null pointer bugs and unchecked exceptions entirely — there is no `null` in Rust, and there's no exception that can silently skip your error handling. `match` forces you to handle every case, which is a feature, not friction.

### Mental model

`Option<T>` is `Some(value)` or `None` — use it for "might not have a value." `Result<T, E>` is `Ok(value)` or `Err(error)` — use it for "might fail, and here's why." `match` must be exhaustive: the compiler won't let you forget a variant, unlike a `switch` in most other languages.

### Code along

```rust
// src/bin/day04.rs
use std::env;

fn parse_int(s: &str) -> Result<i32, String> {
    s.trim()
        .parse::<i32>()
        .map_err(|_| format!("'{s}' is not a valid integer"))
}

fn sum_args(args: &[String]) -> Result<i32, String> {
    let mut total = 0;
    for arg in args {
        total += parse_int(arg)?; // `?` returns early on Err
    }
    Ok(total)
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();

    if args.is_empty() {
        println!("Usage: day04 <int> <int> ...");
        return;
    }

    match sum_args(&args) {
        Ok(total) => println!("Sum: {total}"),
        Err(e) => eprintln!("Error: {e}"),
    }
}
```

Run it two ways:

```bash
cargo run --bin day04 -- 3 4 5
cargo run --bin day04 -- 3 four 5
```

Expected output (first run): `Sum: 12`
Expected output (second run, to stderr): `Error: 'four' is not a valid integer`

### Common mistake

Calling `.unwrap()` on the `parse::<i32>()` result instead of handling the `Err` case: `s.parse::<i32>().unwrap()`. This compiles fine and works right up until someone passes a non-numeric argument, at which point the program **panics** — crashes with a stack trace — instead of printing a clean error. `unwrap()` is for cases you've already proven can't fail (or throwaway prototypes); production-shaped code propagates the error with `?` or handles it with `match`, as above.

### Your task

Add an `average_args(args: &[String]) -> Result<f64, String>` that reuses `parse_int` (via `?` inside a loop, then divides by count) and returns an error if `args` is empty (division by zero) before attempting the math.

**Check:** `average_args` on `["2", "4", "6"]` returns `Ok(4.0)`; on `[]` returns an `Err` with a message mentioning "empty," and on `["2", "x"]` propagates the parse error from `parse_int` unchanged.

---

## Day 5: Collections
{: #day-5-collections }

### Why this matters

`Vec` and `HashMap` are the two collections you'll reach for constantly. Understanding iterator chains (`map`, `filter`, `collect`) is what makes Rust data transformations concise instead of manual index-juggling loops.

### Mental model

`Vec<T>` is a growable array; `HashMap<K, V>` needs `K: Eq + Hash`. Iterators are lazy — nothing happens until you call a consuming method like `.collect()`, `.sum()`, or loop over them with `for`. `.collect()` needs to know the target type, which is why you often see `let v: Vec<_> = ...` or a type on the receiving `let`.

### Code along

```rust
// src/bin/day05.rs
use std::collections::HashMap;

fn word_frequency(text: &str) -> HashMap<String, u32> {
    let mut freq = HashMap::new();
    for word in text.to_lowercase().split_whitespace() {
        let clean: String = word.chars().filter(|c| c.is_alphabetic()).collect();
        if clean.is_empty() {
            continue;
        }
        *freq.entry(clean).or_insert(0) += 1;
    }
    freq
}

fn main() {
    let text = "the quick brown fox jumps over the lazy dog the fox runs";
    let freq = word_frequency(text);

    let mut sorted: Vec<(&String, &u32)> = freq.iter().collect();
    sorted.sort_by(|a, b| b.1.cmp(a.1).then(a.0.cmp(b.0)));

    for (word, count) in sorted.iter().take(3) {
        println!("{word}: {count}");
    }

    let squares: Vec<i32> = (1..=5).map(|x| x * x).collect();
    println!("{:?}", squares);
}
```

Expected output:

```
the: 3
fox: 2
brown: 1
[1, 4, 9, 16, 25]
```

(The third-place tie among count-1 words is broken alphabetically by the `.then(a.0.cmp(b.0))` — `brown` comes before `dog`, `jumps`, `lazy`, `over`, `runs`.)

### Common mistake

Writing `freq[word] += 1` on a fresh `HashMap` expecting Rust to auto-insert a default like some other languages do. This doesn't compile — `HashMap` doesn't implement `IndexMut` for insertion, only for reading an existing key (and indexing a *missing* key panics at runtime instead). The idiomatic pattern is `*freq.entry(word).or_insert(0) += 1`, which handles "insert 0 if missing, then increment" atomically and is worth memorizing — you'll write it constantly.

### Your task

Write `longest_words(freq: &HashMap<String, u32>, n: usize) -> Vec<&String>` returning the `n` longest keys (ties broken alphabetically), using `.iter()`, `.sorted_by`-style comparison via `.sort_by`, and `.take(n)`.

**Check:** on the sample text's frequency map, `longest_words(&freq, 1)` returns `["quick"]` or `["brown"]` — whichever your tie-break logic picks first — verify by hand which 5-letter words are actually the longest in that text before trusting the output.

---

## Day 6: Error handling ergonomics
{: #day-6-error-handling-ergonomics }

### Why this matters

Real programs touch files, networks, and user input — all of which fail. The `?` operator is what makes Rust's explicit error handling (no exceptions) actually pleasant to write instead of a `match` pyramid on every fallible call.

### Mental model

`?` on a `Result` either unwraps the `Ok` value and continues, or returns the `Err` immediately from the enclosing function — which must itself return a compatible `Result`. Custom error enums (implementing `std::error::Error` via `impl Display` + a marker) let one function's `Result` type represent multiple distinct failure reasons cleanly.

### Code along

```rust
// src/bin/day06.rs
use std::fmt;
use std::fs;

#[derive(Debug)]
enum ReportError {
    Io(std::io::Error),
    Empty,
}

impl fmt::Display for ReportError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            ReportError::Io(e) => write!(f, "I/O error: {e}"),
            ReportError::Empty => write!(f, "file is empty"),
        }
    }
}

impl From<std::io::Error> for ReportError {
    fn from(e: std::io::Error) -> Self {
        ReportError::Io(e)
    }
}

fn line_report(path: &str) -> Result<(usize, usize), ReportError> {
    let contents = fs::read_to_string(path)?; // io::Error auto-converts via From
    if contents.trim().is_empty() {
        return Err(ReportError::Empty);
    }
    let lines = contents.lines().count();
    let non_empty = contents.lines().filter(|l| !l.trim().is_empty()).count();
    Ok((lines, non_empty))
}

fn main() {
    match line_report("Cargo.toml") {
        Ok((total, non_empty)) => println!("{total} lines, {non_empty} non-empty"),
        Err(e) => eprintln!("Error: {e}"),
    }

    match line_report("does-not-exist.txt") {
        Ok(_) => unreachable!(),
        Err(e) => println!("Expected failure: {e}"),
    }
}
```

Expected output (line counts will vary by your `Cargo.toml`, the second line is exact):

```
9 lines, 8 non-empty
Expected failure: I/O error: No such file or directory (os error 2)
```

### Common mistake

Forgetting the `impl From<std::io::Error> for ReportError` and expecting `?` to "just work" anyway. Without it, `?` on `fs::read_to_string(path)?` fails to compile: `error[E0277]: '?' couldn't convert the error to 'ReportError'`. The `?` operator relies on `From` conversions to bridge a lower-level error type into your function's error type — this is the mechanism, not magic, and every custom error enum wrapping standard library errors needs these `impl From` blocks.

### Your task

Add a `ReportError::TooLarge(usize)` variant for files over 1000 lines, checked after reading. Update `Display` to handle it with a message including the actual line count.

**Check:** running `line_report` against a generated file with 1001+ lines (`for i in $(seq 1 1001); do echo "line $i"; done > big.txt`) returns `Err(ReportError::TooLarge(1001))`, and the printed message includes `1001`.

---

## Day 7: Traits
{: #day-7-traits }

### Why this matters

Traits are Rust's answer to interfaces — they let you write one function that works across any type satisfying a contract, without inheritance. `impl Trait for Type` is how you retrofit shared behavior onto types you didn't design together.

### Mental model

A trait defines method signatures; `impl TraitName for TypeName` provides them. Generic functions with trait bounds (`fn describe<T: Summary>(item: &T)`) are checked and monomorphized at compile time — zero runtime cost, unlike interfaces in most garbage-collected languages.

### Code along

```rust
// src/bin/day07.rs
trait Area {
    fn area(&self) -> f64;
    fn describe(&self) -> String {
        format!("area = {:.2}", self.area()) // default method
    }
}

struct Circle {
    radius: f64,
}

struct Square {
    side: f64,
}

impl Area for Circle {
    fn area(&self) -> f64 {
        std::f64::consts::PI * self.radius * self.radius
    }
}

impl Area for Square {
    fn area(&self) -> f64 {
        self.side * self.side
    }
}

fn total_area(shapes: &[Box<dyn Area>]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}

fn main() {
    let shapes: Vec<Box<dyn Area>> = vec![
        Box::new(Circle { radius: 2.0 }),
        Box::new(Square { side: 3.0 }),
    ];

    for shape in &shapes {
        println!("{}", shape.describe());
    }
    println!("Total: {:.2}", total_area(&shapes));
}
```

Expected output:

```
area = 12.57
area = 9.00
Total: 21.57
```

### Common mistake

Trying `let shapes: Vec<Area> = vec![...]` without `Box<dyn Area>`. Traits aren't sized types on their own — the compiler doesn't know how much stack space a "some type implementing `Area`" needs, since `Circle` and `Square` are different sizes. The error is `error[E0277]: the size for values of type 'dyn Area' cannot be known at compilation time`, and the fix is exactly what's shown above: put trait objects behind a `Box` (heap allocation, fixed-size pointer) when you need a collection of mixed concrete types sharing one trait.

### Your task

Add a `Rectangle { width: f64, height: f64 }` implementing `Area`, and override `describe` for `Rectangle` specifically to include its dimensions (e.g. `"3.00 x 4.00, area = 12.00"`) instead of using the default.

**Check:** printing all four shapes (circle, square, and two rectangles) shows the rectangle's custom `describe` format while circle and square still use the default, and `total_area` correctly sums all four.

---

## Day 8: Modules & crates
{: #day-8-modules-crates }

### Why this matters

`mod` and a `lib.rs`/`main.rs` split is how you separate a reusable library from its command-line entry point — the same pattern real Rust projects use to keep business logic testable independently of I/O.

### Mental model

A binary crate has `src/main.rs` as its entry point; a library crate has `src/lib.rs`. A project can have both simultaneously — `main.rs` becomes a thin wrapper that calls into the library, which is exactly what makes the library's functions independently unit-testable (Day 9).

### Code along

Convert `rust-lab` to also expose a library. Add to `Cargo.toml` if not already inferred (Cargo auto-detects `src/lib.rs`):

```rust
// src/lib.rs
pub mod store {
    use std::collections::HashMap;

    pub struct KeyValueStore {
        data: HashMap<String, String>,
    }

    impl KeyValueStore {
        pub fn new() -> Self {
            KeyValueStore { data: HashMap::new() }
        }

        pub fn set(&mut self, key: &str, value: &str) {
            self.data.insert(key.to_string(), value.to_string());
        }

        pub fn get(&self, key: &str) -> Option<&String> {
            self.data.get(key)
        }

        pub fn len(&self) -> usize {
            self.data.len()
        }
    }
}
```

```rust
// src/bin/day08.rs
use rust_lab::store::KeyValueStore;

fn main() {
    let mut store = KeyValueStore::new();
    store.set("name", "Ada");
    store.set("lang", "Rust");

    match store.get("name") {
        Some(v) => println!("name = {v}"),
        None => println!("name not found"),
    }
    match store.get("missing") {
        Some(v) => println!("missing = {v}"),
        None => println!("missing key correctly returned None"),
    }
    println!("store has {} entries", store.len());
}
```

Expected output:

```
name = Ada
missing key correctly returned None
store has 2 entries
```

### Common mistake

Forgetting `pub` on either the module, the struct, or its methods, then getting `error[E0603]: module 'store' is private` or `error[E0616]: field 'data' of struct 'KeyValueStore' is private` from `src/bin/day08.rs`. Rust's default visibility is private — you opt into exposing things with `pub`, one layer at a time (module, then type, then each method/field you want external code to reach). This is intentional: it forces you to design a deliberate public API instead of accidentally exposing internals.

### Your task

Add a `remove(&mut self, key: &str) -> Option<String>` method to `KeyValueStore` that removes and returns the old value if present.

**Check:** after `set("a", "1")`, `remove("a")` returns `Some("1".to_string())` and a subsequent `get("a")` returns `None`; `remove("never-set")` returns `None` without panicking.

---

## Day 9: Testing
{: #day-9-testing }

### Why this matters

`cargo test` runs alongside your normal code with zero external test framework setup — there's no excuse not to test in Rust. Table-style tests covering edge cases (empty input, boundary values) are what catch the bugs that "looks right" code review misses.

### Mental model

`#[test]` marks a function as a test case; `#[cfg(test)]` on a `mod tests` block means that module only compiles when running `cargo test`, not in normal builds — zero cost in production binaries. `assert_eq!`/`assert!` panic (failing the test) with a clear diff when the condition doesn't hold.

### Code along

```rust
// src/lib.rs (add to the existing file, outside the store module)
pub fn clamp(x: i32, lo: i32, hi: i32) -> i32 {
    if lo > hi {
        panic!("invalid range: lo ({lo}) > hi ({hi})");
    }
    x.max(lo).min(hi)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn clamps_within_range_unchanged() {
        assert_eq!(clamp(5, 0, 10), 5);
    }

    #[test]
    fn clamps_below_range() {
        assert_eq!(clamp(-5, 0, 10), 0);
    }

    #[test]
    fn clamps_above_range() {
        assert_eq!(clamp(15, 0, 10), 10);
    }

    #[test]
    fn boundary_values_are_unchanged() {
        assert_eq!(clamp(0, 0, 10), 0);
        assert_eq!(clamp(10, 0, 10), 10);
    }

    #[test]
    #[should_panic(expected = "invalid range")]
    fn invalid_range_panics() {
        clamp(5, 10, 0);
    }
}
```

Run:

```bash
cargo test
```

Expected output: `test result: ok. 5 passed; 0 failed; ...` (function names may print in a different order — that's normal, `cargo test` doesn't guarantee execution order).

### Common mistake

Writing `assert_eq!(clamp(5, 0, 10), "5")` — comparing an `i32` against a string literal. This fails to compile, not just to run: `error[E0308]: mismatched types`. This is actually a gift compared to dynamically typed languages, where the equivalent mistake would silently return `false` from an equality check (`5 == "5"`) instead of erroring, and you'd have a test that passes for the wrong reason or fails with no explanation.

### Your task

Add a test proving `clamp`'s behavior when `lo == hi` (every input should clamp to that single value), and a test with negative bounds (`clamp(-100, -50, -10)`).

**Check:** `cargo test` shows 7 total passing tests (5 original + your 2 new ones), and you can explain out loud why each of your two new tests exercises a case the original 5 didn't cover.

---

## Day 10: CLI with clap (manual argv ok)
{: #day-10-cli-with-clap-manual-argv-ok }

### Why this matters

Every real Rust CLI tool — `cargo` itself included — parses subcommands and flags. Whether you use `clap` (the ecosystem standard) or roll it by hand, understanding the pattern (dispatch on the first argument, validate the rest) is what makes a CLI predictable to use and to extend.

### Mental model

Match on `args.as_slice()` with slice patterns to dispatch subcommands cleanly — Rust's pattern matching on slices (`[cmd, path]`, `[cmd, pat, path]`) is more expressive than manual `if args.len() == 2` checks and reads like a spec of your CLI's grammar.

### Code along

```rust
// src/bin/day10.rs
use std::fs;

fn cmd_wc(path: &str) {
    match fs::read_to_string(path) {
        Ok(text) => println!("{}", text.lines().count()),
        Err(e) => eprintln!("error reading {path}: {e}"),
    }
}

fn cmd_grep(pattern: &str, path: &str) {
    match fs::read_to_string(path) {
        Ok(text) => {
            for (i, line) in text.lines().enumerate() {
                if line.contains(pattern) {
                    println!("{}:{}", i + 1, line);
                }
            }
        }
        Err(e) => eprintln!("error reading {path}: {e}"),
    }
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();

    match args.as_slice() {
        [cmd, path] if cmd == "wc" => cmd_wc(path),
        [cmd, pattern, path] if cmd == "grep" => cmd_grep(pattern, path),
        _ => {
            eprintln!("usage:");
            eprintln!("  day10 wc <path>");
            eprintln!("  day10 grep <pattern> <path>");
            std::process::exit(1);
        }
    }
}
```

Test it:

```bash
printf "fn main() {}\n// TODO: cleanup\nlet x = 1;\n" > sample.rs
cargo run --bin day10 -- wc sample.rs
cargo run --bin day10 -- grep TODO sample.rs
```

Expected output:

```
3
2:// TODO: cleanup
```

### Common mistake

Forgetting the `if cmd == "wc"` guard on the pattern and matching `[cmd, path]` unconditionally — then `grep` (three args) never matches the two-arg pattern anyway, but a typo'd subcommand like `day10 xx sample.rs` silently runs `cmd_wc` on `sample.rs` as if it were the `wc` command, because the pattern only checks *shape* (two elements), not the actual subcommand name. Slice patterns match structure; you still need explicit guards (`if cmd == "..."`) to check content.

### Your task

Add a `lines <n> <path>` subcommand that prints just the first `n` lines of the file (parse `n` with `.parse::<usize>()`, handling a bad number with a clear error rather than a panic).

**Check:** `day10 lines 2 sample.rs` prints exactly the first two lines from the test file above; `day10 lines abc sample.rs` prints a clear error to stderr and exits non-zero, without panicking (no `thread 'main' panicked` text in the output).

---

## Capstone project
{: #capstone }

Build a **todo CLI** backed by a JSON file, with a properly separated library (`src/lib.rs`) and binary (`src/main.rs`), full `Result`-based error handling, and unit tests for the store — no `unwrap()` outside of tests.

**Deliverable — file layout:**

```
todo-cli/
  src/lib.rs      # TodoStore: add/complete/remove/list, load/save to JSON
  src/main.rs     # CLI: add <text>, done <id>, rm <id>, list
  Cargo.toml       # add `serde`, `serde_json` as dependencies
  README.md        # exact commands + expected output
```

**Library requirements (`src/lib.rs`):**
- `struct Todo { id: u32, text: String, done: bool }` deriving `Serialize`/`Deserialize`.
- `TodoStore::load(path: &str) -> Result<TodoStore, TodoError>` — returns an empty store (not an error) if the file doesn't exist yet; returns an error for genuinely malformed JSON.
- `add`, `complete(id) -> Result<(), TodoError>`, `remove(id) -> Result<(), TodoError>` (error on unknown id for the latter two), `list() -> &[Todo]`, `save(&self, path: &str) -> Result<(), TodoError>`.
- A custom `TodoError` enum (`Io`, `Parse`, `NotFound(u32)`) implementing `Display`.

**CLI requirements (`src/main.rs`):** `todo-cli add "buy milk"`, `todo-cli done 1`, `todo-cli rm 2`, `todo-cli list` — each loads the store from `todos.json`, performs the action, saves, and prints either the result or a clear error to stderr with a non-zero exit code.

**Test requirements:** at least 6 unit tests in `src/lib.rs` covering: adding assigns sequential ids, completing an unknown id errors, removing an unknown id errors, `load` on a missing file returns an empty store (not an error), `load` on malformed JSON returns an error, and a full add→complete→save→load round-trip preserves state.

**Acceptance check:** `cargo test` passes all tests; running `add`, `done`, `list` in sequence against a fresh `todos.json` shows the expected todo marked done in the final `list` output, and `cat todos.json` shows valid, matching JSON.

## Related

- [C++ in 10 Days](/courses/cpp-10-days/)
- [Go in 10 Days](/courses/go-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
