---
layout: course
title: "Swift in 10 Days — Hands-On"
permalink: /courses/swift-10-days/
course_track: "Swift"
description: "Modern Swift for Apple platforms and beyond — types, optionals, and a small CLI."
toc:
  - id: "day-1-hello-swift"
    label: "Day 1: Hello Swift"
  - id: "day-2-optionals"
    label: "Day 2: Optionals"
  - id: "day-3-structs-methods"
    label: "Day 3: Structs & methods"
  - id: "day-4-enums"
    label: "Day 4: Enums"
  - id: "day-5-collections"
    label: "Day 5: Collections"
  - id: "day-6-protocols"
    label: "Day 6: Protocols"
  - id: "day-7-error-handling"
    label: "Day 7: Error handling"
  - id: "day-8-closures"
    label: "Day 8: Closures"
  - id: "day-9-async-basics"
    label: "Day 9: Async basics"
  - id: "day-10-cli-tool"
    label: "Day 10: CLI tool"
  - id: "capstone"
    label: "Capstone project"
---

# Swift in 10 Days — Hands-On

Modern Swift for Apple platforms and beyond — types, optionals, and a small CLI.

## Why this language
{: #why-this-language }

Swift is the language of iOS/macOS apps, with growing server-side use. Clear syntax and strong safety.

## Setup (Day 0)
{: #setup-day-0 }

On macOS: Xcode or `swift` toolchain. On Linux: install Swift.org toolchain.
```bash
swift --version
mkdir SwiftLab && cd SwiftLab
swift package init --type executable
```

---

## Day 1: Hello Swift
{: #day-1-hello-swift }

### What you'll learn

- let/var
- print
- string interpolation

### Code along

```swift
let name = "Swift"
print("Hello, \(name)")
```

### Your task

Read a line and greet.

---

## Day 2: Optionals
{: #day-2-optionals }

### What you'll learn

- `?`
- `if let`
- `guard let`
- nil coalescing

### Code along

```swift
func len(_ s: String?) -> Int { s?.count ?? 0 }
print(len(nil))
```

### Your task

Parse Int from String?; print message on failure.

---

## Day 3: Structs & methods
{: #day-3-structs-methods }

### What you'll learn

- struct
- mutating
- methods

### Code along

```swift
struct Counter {
  private(set) var n = 0
  mutating func tick() { n += 1 }
}
```

### Your task

BankAccount struct with deposit/withdraw.

---

## Day 4: Enums
{: #day-4-enums }

### What you'll learn

- associated values
- switch
- exhaustive

### Code along

```swift
enum Result { case ok(Int); case err(String) }
func show(_ r: Result) {
  switch r {
  case .ok(let n): print(n)
  case .err(let e): print(e)
  }
}
```

### Your task

Enum for HTTP method; print raw description.

---

## Day 5: Collections
{: #day-5-collections }

### What you'll learn

- Array/Dict/Set
- map/filter
- for-in

### Code along

```swift
let nums = [1, 2, 3, 4]
print(nums.filter { $0 % 2 == 0 }.map { $0 * $0 })
```

### Your task

Word frequency dictionary.

---

## Day 6: Protocols
{: #day-6-protocols }

### What you'll learn

- protocol
- conformance
- extensions

### Code along

```swift
protocol Greeter { func greet() -> String }
struct Person: Greeter {
  var name: String
  func greet() -> String { "Hi \(name)" }
}
```

### Your task

Protocol Area for Circle and Rect.

---

## Day 7: Error handling
{: #day-7-error-handling }

### What you'll learn

- `throws`
- `try`
- `do/catch`

### Code along

```swift
enum ParseError: Error { case bad }
func parse(_ s: String) throws -> Int {
  guard let n = Int(s) else { throw ParseError.bad }
  return n
}
```

### Your task

Read a file and throw on missing path.

---

## Day 8: Closures
{: #day-8-closures }

### What you'll learn

- trailing closures
- capture
- sorted(by:)

### Code along

```swift
let xs = [3, 1, 2].sorted { $0 < $1 }
print(xs)
```

### Your task

Implement `once` using a closure flag.

---

## Day 9: Async basics
{: #day-9-async-basics }

### What you'll learn

- async/await intro
- Task
- URLSession sketch

### Code along

```swift
// async func load() async throws -> String { ... }
print("learn URLSession when on Apple platforms")
```

### Your task

Write an async function that sleeps and returns a string (Task.sleep).

---

## Day 10: CLI tool
{: #day-10-cli-tool }

### What you'll learn

- CommandLine.arguments
- FileManager
- exit

### Code along

```swift
let args = CommandLine.arguments
guard args.count > 1 else { fputs("usage\n", stderr); exit(1); }
print(args[1])
```

### Your task

wc-like line counter for a file path arg.


---

## Capstone project
{: #capstone }

Build a **Swift todo CLI** with Codable JSON persistence, enums for commands, and clear error messages.

## Related

- [Kotlin in 10 Days](/courses/kotlin-10-days/)
- [TypeScript in 10 Days](/courses/typescript-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
