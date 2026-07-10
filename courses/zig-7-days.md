---
layout: course
title: "Zig in 7 Days — Hands-On"
permalink: /courses/zig-7-days/
course_track: "Zig"
description: "Explicit allocators, error unions, and comptime — learn Zig by reading its compile-time errors and leak reports, not by avoiding them."
toc:
  - id: "why-this-language"
    label: "Why this language"
  - id: "setup-day-0"
    label: "Setup (Day 0)"
  - id: "day-1-hello-zig"
    label: "Day 1: Hello Zig"
  - id: "day-2-types-errors"
    label: "Day 2: Types & errors"
  - id: "day-3-allocators"
    label: "Day 3: Allocators"
  - id: "day-4-structs"
    label: "Day 4: Structs"
  - id: "day-5-comptime-peek"
    label: "Day 5: Comptime peek"
  - id: "day-6-files"
    label: "Day 6: Files"
  - id: "day-7-cli-tool"
    label: "Day 7: CLI tool"
  - id: "capstone"
    label: "Capstone project"
---

# Zig in 7 Days — Hands-On

No hidden allocations, no hidden control flow. Every day below is one file you run directly with `zig run` — by Day 7 you'll have a working grep-lite CLI.

## Why this language
{: #why-this-language }

Zig's pitch is simple: C-level control with none of C's footguns left implicit. There's no garbage collector and no hidden allocations — every function that allocates takes an `Allocator` argument explicitly, so you can always see, by reading a signature, whether a call might touch the heap. Error handling is a first-class type (`!T`) instead of exceptions or `errno`, so the compiler forces you to acknowledge failure paths. It's a smaller, stricter language than Rust with a much smaller learning curve — this course gets you from zero to a working CLI in a week.

## Setup (Day 0)
{: #setup-day-0 }

```bash
# https://ziglang.org/download/
zig version              # expect 0.13.0 or newer
mkdir zig-lab && cd zig-lab
```

No `build.zig` needed for this course — every day is a single file run directly:

```bash
zig run day01.zig
zig run day01.zig -- foo bar   # everything after -- becomes the program's own argv
```

**Checkpoint:** create `day00.zig` with just `pub fn main() void {}` and run `zig run day00.zig`. It should compile in under a second and print nothing — confirming your toolchain works before Day 1's real code.

---

## Day 1: Hello Zig
{: #day-1-hello-zig }

### Why it matters

`std.debug.print` and command-line arguments are the first thing every Zig program touches, and they immediately introduce the two ideas that define the language: explicit allocators (arguments need one to read) and `!void` return types (allocation can fail, so `main` must be allowed to propagate an error).

### Mental model

`std.process.argsAlloc` needs an allocator because argv has to be copied into memory your program owns — nothing in Zig allocates behind your back. A function declared `pub fn main() !void` can use `try` on any call that returns an error union; a function declared `void` cannot, full stop. `defer` schedules cleanup that runs when the enclosing scope exits, in reverse order of registration — it's how you pair every allocation with its cleanup right next to where the allocation happened.

### Code along

```zig
// day01.zig
const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const args = try std.process.argsAlloc(allocator);
    defer std.process.argsFree(allocator, args);

    std.debug.print("Hello, Zig! Learning in 2026.\n", .{});
    if (args.len > 1) {
        std.debug.print("You passed {d} extra argument(s):\n", .{args.len - 1});
        for (args[1..]) |arg| {
            std.debug.print("  {s}\n", .{arg});
        }
    } else {
        std.debug.print("No extra arguments. Try: zig run day01.zig -- foo bar\n", .{});
    }
}
```

Run it two ways:

```bash
zig run day01.zig
zig run day01.zig -- foo bar
```

Expected output (second run):

```
Hello, Zig! Learning in 2026.
You passed 2 extra argument(s):
  foo
  bar
```

### Common mistake

Running `zig run day01.zig foo bar` (forgetting the `--` separator). Without it, Zig tries to treat `foo` as another *source file* to compile alongside `day01.zig`, and fails with an error about an unrecognized or missing file — not your program's own argument-handling logic at all. Everything after `--` goes to your program; everything before it is for the `zig` command itself, exactly like `cargo run --bin x -- args`.

### Your task

Change the "no extra arguments" branch to instead read a line from stdin (`std.io.getStdIn().reader()`, `readUntilDelimiterAlloc` on `'\n'`) and print `"You said: <line>"`.

**Check:** running `echo "hi there" | zig run day01.zig` prints `You said: hi there` — confirming stdin reading works when no argv arguments are present.

---

## Day 2: Types & errors
{: #day-2-types-errors }

### Why it matters

Zig has no exceptions and no `null` pointer surprises — both "this might fail" and "this might be absent" are encoded directly in the type (`!T` and `?T`). Reading a function's signature tells you everything about what can go wrong, which is the entire point.

### Mental model

An **error set** (`error{ Empty, NotANumber }`) is a closed list of named failure reasons — think of it as a small enum reserved for errors. `!T` means "either an error from some error set, or a value of type `T`." `catch` handles the error case inline (supplying a default or running a block); `try` is shorthand for "catch, and if it's an error, return it immediately from the current function" — which only compiles if the current function's return type can carry that error.

### Code along

```zig
// day02.zig
const std = @import("std");

const ParseError = error{ Empty, NotANumber };

fn parsePositive(s: []const u8) ParseError!u32 {
    if (s.len == 0) return ParseError.Empty;
    return std.fmt.parseInt(u32, s, 10) catch return ParseError.NotANumber;
}

pub fn main() void {
    const inputs = [_][]const u8{ "42", "", "abc" };
    for (inputs) |input| {
        const result = parsePositive(input) catch |err| {
            std.debug.print("'{s}' failed: {s}\n", .{ input, @errorName(err) });
            continue;
        };
        std.debug.print("'{s}' -> {d}\n", .{ input, result });
    }
}
```

Expected output:

```
'42' -> 42
'' failed: Empty
'abc' failed: NotANumber
```

### Common mistake

Trying `const n = try parsePositive("42");` inside `main` when `main` is declared `pub fn main() void` (as it correctly is above, since this version handles the error with `catch`, not `try`). Swap in a bare `try` there and the compiler rejects it: the error union `parsePositive` can return has nowhere to go, because `void` can't carry an error. The fix is always one of two things — change the function's own return type to `!void` so the error can propagate further up, or handle it locally with `catch`, exactly as Day 2's working version does.

### Your task

Add a third error case: `TooLarge`, returned when the parsed number exceeds `1000`. Update the `inputs` array to include `"5000"` and confirm it prints `'5000' failed: TooLarge`.

**Check:** all four inputs (`"42"`, `""`, `"abc"`, `"5000"`) print, in order: a success line, then three failure lines naming `Empty`, `NotANumber`, and `TooLarge` respectively.

---

## Day 3: Allocators
{: #day-3-allocators }

### Why it matters

Every dynamically-sized collection in Zig — `ArrayList`, `HashMap`, a file's contents read into memory — needs an allocator passed explicitly. There's no default heap hiding behind the scenes; you choose the allocator, and in debug builds `GeneralPurposeAllocator` will actively tell you if you forget to free something.

### Mental model

`GeneralPurposeAllocator` wraps the system allocator with **leak detection** in debug builds — every `alloc` it hasn't seen a matching `free` for by the time `deinit()` runs gets reported. `ArrayList(T).init(allocator)` starts empty and grows as you `.append()`; `.deinit()` frees its backing memory. The pattern is always: allocate, `defer` the matching cleanup on the very next line, then use the value in between — write the `defer` before you forget it's needed.

### Code along

```zig
// day03.zig
const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var list = std.ArrayList(i32).init(allocator);
    defer list.deinit();

    for (1..6) |i| {
        try list.append(@intCast(i * i));
    }

    std.debug.print("Squares: {any}\n", .{list.items});

    var total: i32 = 0;
    for (list.items) |n| total += n;
    std.debug.print("Sum: {d}\n", .{total});
}
```

Expected output:

```
Squares: { 1, 4, 9, 16, 25 }
Sum: 55
```

### Common mistake

Deleting the `defer list.deinit();` line to "clean up the code" since the program still runs and prints correctly either way. In a debug build, `gpa.deinit()` returns `.leak` and `GeneralPurposeAllocator` prints something like `error(gpa): memory address 0x... leaked` to stderr right before exit — the leak is real, it just doesn't crash anything, because the OS reclaims all memory when the process exits regardless. This is exactly the class of bug that's silent in short-lived CLI tools and fatal in long-running servers; the leak detector exists so you catch it in the CLI tool, before it becomes the server bug.

### Your task

Change `ArrayList(i32)` to `ArrayList([]const u8)` holding the words of a sentence (split with `std.mem.splitScalar(u8, sentence, ' ')`, appending each `it.next()` result), and print `list.items.len` followed by each word on its own line.

**Check:** for `"the quick brown fox"`, prints `4` followed by exactly four lines: `the`, `quick`, `brown`, `fox`.

---

## Day 4: Structs
{: #day-4-structs }

### Why it matters

Zig has no classes or inheritance — just `struct` plus plain functions that take the struct as their first parameter. Whether a method can mutate its receiver is visible directly in the signature (`self: Rect` vs `self: *Rect`), not buried in a `mutable` keyword you have to remember to add.

### Mental model

`self: Rect` (by value) means the method gets a copy and can't affect the caller's original. `self: *Rect` (by pointer) means the method can mutate the real thing — and critically, you can only call a `*Rect`-receiver method on a variable declared `var`, never `const`, because a `const` value has no guarantee it's even mutable in memory.

### Code along

```zig
// day04.zig
const std = @import("std");

const Rect = struct {
    width: f64,
    height: f64,

    fn area(self: Rect) f64 {
        return self.width * self.height;
    }

    fn scale(self: *Rect, factor: f64) void {
        self.width *= factor;
        self.height *= factor;
    }
};

pub fn main() void {
    var r = Rect{ .width = 10, .height = 20 };
    std.debug.print("area: {d}\n", .{r.area()});
    r.scale(2);
    std.debug.print("after scale: {d}x{d} area={d}\n", .{ r.width, r.height, r.area() });
}
```

Expected output:

```
area: 200
after scale: 20x40 area=800
```

### Common mistake

Declaring `const r = Rect{ .width = 10, .height = 20 };` instead of `var r = ...`, then calling `r.scale(2)`. The compiler rejects it — something like `error: cannot assign to constant` or a type mismatch pointing at `scale` wanting `*Rect` but receiving `*const Rect`. This is the same category of guarantee Rust's borrow checker makes: the compiler statically knows nothing declared `const` can be handed to a function that mutates through a pointer, so it refuses before the mistake ever runs.

### Your task

Add a method `fn isSquare(self: Rect) bool` returning `self.width == self.height`, and a method `fn aspectRatio(self: Rect) f64` returning `self.width / self.height`. Print both for `r` before and after `scale(2)`.

**Check:** `aspectRatio` returns `0.5` both before and after scaling (uniform scaling never changes aspect ratio); `isSquare` returns `false` in both cases for a 10×20 (later 20×40) rectangle.

---

## Day 5: Comptime peek
{: #day-5-comptime-peek }

### Why it matters

`comptime` is Zig's answer to generics — instead of a separate generics syntax, a function parameter can simply be a `type`, evaluated and specialized entirely at compile time. There's no runtime cost and no separate "generic" language feature to learn; it's the same language, just evaluated earlier.

### Mental model

`comptime T: type` means the compiler must know `T` while compiling, not while running — you can't pass a runtime-computed type. Each distinct `T` you call `max` with generates its own specialized copy of the function at compile time (monomorphization), the same mechanism Rust generics and C++ templates use, just with plain function syntax instead of angle brackets.

### Code along

```zig
// day05.zig
const std = @import("std");

fn max(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

fn Pair(comptime T: type) type {
    return struct {
        first: T,
        second: T,
    };
}

pub fn main() void {
    std.debug.print("max i32: {d}\n", .{max(i32, 3, 7)});
    std.debug.print("max f64: {d}\n", .{max(f64, 2.5, 1.5)});

    const p = Pair(i32){ .first = 1, .second = 2 };
    std.debug.print("pair: {d}, {d}\n", .{ p.first, p.second });
}
```

Expected output:

```
max i32: 7
max f64: 2.5
pair: 1, 2
```

### Common mistake

Calling `max(i32, 3, 7.5)` — mixing an integer literal with a floating-point one while `T` is pinned to `i32`. This fails at compile time with something like `error: expected type 'i32', found 'comptime_float'`: `7.5` isn't a whole number, so it can't coerce into `i32` the way `3` (a `comptime_int`) can. `comptime` catches this before your program ever runs, unlike a dynamically-typed language where `max(3, 7.5)` would silently succeed and quietly hand back a type you didn't expect.

### Your task

Write `fn Pair3(comptime T: type) type` returning a struct with three fields (`first`, `second`, `third`) of type `T`, plus a method `fn sum(self: @This()) T` (only implement `sum` for numeric `T` — try it with `i32`). Construct one with values `1, 2, 3` and print `sum()`.

**Check:** `sum()` on a `Pair3(i32){ .first = 1, .second = 2, .third = 3 }` prints `6`.

---

## Day 6: Files
{: #day-6-files }

### Why it matters

`std.fs.cwd().readFileAlloc` is how nearly every real Zig CLI tool reads input — and because it returns an error union, the compiler forces you to decide what happens when the file doesn't exist, instead of finding out from a crash report.

### Mental model

`readFileAlloc` needs a max-size argument as a safety cap — it refuses to read a file larger than you told it to expect, rather than silently allocating gigabytes because someone pointed it at the wrong path. The returned slice is heap memory *you* now own — pair it with `defer allocator.free(contents)` immediately, the same discipline as Day 3's `ArrayList`.

### Code along

```bash
printf "line one\nline two\nline three\n" > sample.txt
```

```zig
// day06.zig
const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const contents = try std.fs.cwd().readFileAlloc(allocator, "sample.txt", 1024 * 1024);
    defer allocator.free(contents);

    var lines: usize = 0;
    for (contents) |c| {
        if (c == '\n') lines += 1;
    }
    std.debug.print("{d} lines, {d} bytes\n", .{ lines, contents.len });
}
```

Expected output: `3 lines, 27 bytes`

### Common mistake

Running `zig run day06.zig` from a directory that doesn't have `sample.txt` yet. Because `main` is `!void` and nothing `catch`es the `readFileAlloc` call, the error propagates all the way out and Zig prints an unhandled-error trace ending in something like `error: FileNotFound` plus a stack of source locations — not a graceful message. That's the correct behavior for a quick script, but a real CLI tool should `catch` file errors near the entry point and print something a user (not a developer) can act on.

### Your task

Wrap the `readFileAlloc` call in a `catch |err|` that prints `"could not read sample.txt: {s}"` with `@errorName(err)` and exits via `std.process.exit(1)` instead of letting the raw error trace through.

**Check:** renaming `sample.txt` temporarily and re-running prints your clean one-line message (not a stack trace), and `echo $?` after it shows `1`.

---

## Day 7: CLI tool
{: #day-7-cli-tool }

### Why it matters

A real CLI dispatches on a subcommand and validates its own arguments — the same shape as Day 1's argument handling, Day 2's error unions, and Day 6's file reading, combined into one program. This is the shape every one of Zig's own tools (`zig fmt`, `zig build`) shares underneath.

### Mental model

Slices don't support `==` for content comparison — `args[1] == "wc"` compares whether two slices point at the *same memory*, not whether their contents match, and will almost always be `false` even when the text looks identical. `std.mem.eql(u8, a, b)` is the actual content comparison you want, every time you're comparing `[]const u8`.

### Code along

```zig
// day07.zig
const std = @import("std");

fn countLines(allocator: std.mem.Allocator, path: []const u8) !usize {
    const contents = try std.fs.cwd().readFileAlloc(allocator, path, 1024 * 1024);
    defer allocator.free(contents);
    var lines: usize = 0;
    for (contents) |c| {
        if (c == '\n') lines += 1;
    }
    return lines;
}

fn grep(allocator: std.mem.Allocator, pattern: []const u8, path: []const u8) !void {
    const contents = try std.fs.cwd().readFileAlloc(allocator, path, 1024 * 1024);
    defer allocator.free(contents);
    var it = std.mem.splitScalar(u8, contents, '\n');
    var lineNum: usize = 0;
    while (it.next()) |line| {
        lineNum += 1;
        if (std.mem.indexOf(u8, line, pattern) != null) {
            std.debug.print("{d}:{s}\n", .{ lineNum, line });
        }
    }
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const args = try std.process.argsAlloc(allocator);
    defer std.process.argsFree(allocator, args);

    if (args.len == 3 and std.mem.eql(u8, args[1], "wc")) {
        const n = try countLines(allocator, args[2]);
        std.debug.print("{d}\n", .{n});
    } else if (args.len == 4 and std.mem.eql(u8, args[1], "grep")) {
        try grep(allocator, args[2], args[3]);
    } else {
        std.debug.print("usage: day07 wc <path> | day07 grep <pattern> <path>\n", .{});
        std.process.exit(1);
    }
}
```

Test it:

```bash
printf "fn main() void {}\n// TODO: cleanup\nconst x = 1;\n" > sample.zig
zig run day07.zig -- wc sample.zig
zig run day07.zig -- grep TODO sample.zig
```

Expected output:

```
3
2:// TODO: cleanup
```

### Common mistake

Writing the dispatch check as `if (args[1] == "wc")` instead of `std.mem.eql(u8, args[1], "wc")`. This *compiles* — slices support `==` syntactically — but it compares slice identity (pointer and length), not text content, so it evaluates `false` for essentially any two independently-created strings, even ones that read identically. The visible symptom is worse than a compile error: every subcommand silently falls through to the `usage` branch, and it looks like your program simply doesn't recognize any command you type.

### Your task

Add a `lines <n> <path>` subcommand that prints just the first `n` lines (split on `'\n'` with `splitScalar`, take the first `n` with a counter, `break` once reached).

**Check:** `zig run day07.zig -- lines 2 sample.zig` prints exactly the first two lines from the test file above (`fn main() void {}` and `// TODO: cleanup`), nothing more.

---

## Capstone project
{: #capstone }

Build a **grep-lite CLI** combining every day above: explicit allocator threaded through every function, `!T` error unions with real `catch` handling at the boundary (not raw propagation to a stack trace), and a small `struct` to hold parsed options.

**Deliverable:**

```
grep-lite/
  main.zig       # parses argv, dispatches, owns the allocator
  README.md      # exact commands + expected output
```

**Requirements:**
- `struct Options { pattern: []const u8, path: []const u8, ignore_case: bool }` built from argv (support a `-i` flag anywhere in the args, case-insensitive via `std.ascii.eqlIgnoreCase` per byte or lowercasing both sides before `indexOf`).
- Clean error messages (via `catch`) for: missing arguments, file not found, pattern not found in file (exit `1`, not a crash, in all three cases).
- No leaks: run under `zig build -Doptimize=Debug` and confirm `GeneralPurposeAllocator` reports zero leaked addresses on every code path, including the error paths.

**Acceptance check:** `grep-lite -i TODO sample.zig` finds a `// todo:` line regardless of case; `grep-lite MISSING sample.zig` prints a clean "not found" message and exits `1`; `grep-lite PATTERN missing-file.txt` prints a clean "file not found" message and exits `1` — no raw error traces in any of the three cases.

## Related

- [Rust in 10 Days](/courses/rust-10-days/)
- [C++ in 10 Days](/courses/cpp-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
