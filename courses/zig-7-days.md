---
layout: course
title: "Zig in 7 Days — Hands-On"
permalink: /courses/zig-7-days/
course_track: "Zig"
description: "A rising systems language: explicit allocators, comptime, and a tiny CLI."
toc:
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

A rising systems language: explicit allocators, comptime, and a tiny CLI.

## Why this language
{: #why-this-language }

Zig is hot among systems programmers who want C interop without C footguns. Great for tooling and WASM.

## Setup (Day 0)
{: #setup-day-0 }

Install from https://ziglang.org/
```bash
zig version
mkdir zig-lab && cd zig-lab
zig init-exe
zig build run
```

---

## Day 1: Hello Zig
{: #day-1-hello-zig }

### What you'll learn

- pub fn main
- print
- build

### Code along

```zig
const std = @import("std");
pub fn main() void {
    std.debug.print("Hello Zig\n", .{});
}
```

### Your task

Print a number and a string.

---

## Day 2: Types & errors
{: #day-2-types-errors }

### What you'll learn

- u32/i32
- error unions
- `try`/`catch`

### Code along

```zig
fn parse() !u32 { return 42; }
pub fn main() void {
    const n = parse() catch 0;
    _ = n;
}
```

### Your task

Function that returns error on bad input string length.

---

## Day 3: Allocators
{: #day-3-allocators }

### What you'll learn

- page_allocator
- ArrayList
- defer

### Code along

```zig
var gpa = std.heap.GeneralPurposeAllocator(.{}){};
defer _ = gpa.deinit();
const a = gpa.allocator();
```

### Your task

Build a dynamic list of integers and print them.

---

## Day 4: Structs
{: #day-4-structs }

### What you'll learn

- struct
- methods
- fields

### Code along

```zig
const Point = struct { x: i32, y: i32 };
var p = Point{ .x = 1, .y = 2 };
_ = p;
```

### Your task

Rect with area method.

---

## Day 5: Comptime peek
{: #day-5-comptime-peek }

### What you'll learn

- comptime
- inline
- type params lite

### Code along

```zig
fn max(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}
```

### Your task

Comptime max for i32 and f64 calls.

---

## Day 6: Files
{: #day-6-files }

### What you'll learn

- cwd
- readFileAlloc
- write

### Code along

```zig
// use std.fs.cwd().readFileAlloc(allocator, path, max)
std.debug.print("read a file next\n", .{});
```

### Your task

Line-count a file path from args.

---

## Day 7: CLI tool
{: #day-7-cli-tool }

### What you'll learn

- args
- exit
- build.zig mindset

### Code along

```zig
var it = try std.process.argsWithAllocator(allocator);
defer it.deinit();
_ = it.skip();
```

### Your task

wc-like tool: lines for a path argument.


---

## Capstone project
{: #capstone }

Build a **Zig grep-lite**: read a file, print lines containing a pattern, with explicit allocator and error handling.

## Related

- [Rust in 10 Days](/courses/rust-10-days/)
- [C++ in 10 Days](/courses/cpp-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
