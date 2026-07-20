---
layout: course
title: "Swift in 10 Days — Hands-On"
permalink: /courses/swift-10-days/
course_track: "Swift"
description: "Optionals, enums, and protocols — build a working Swift CLI, one concept at a time."
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

Optionals, enums, and protocols — build a working Swift CLI, one concept at a time.

## Why this language
{: #why-this-language }

Swift is the only realistic choice for shipping iOS/macOS apps, and it's increasingly usable server-side (Vapor) and on Linux. What makes it worth learning deliberately rather than picking up by osmosis is that its core safety features — optionals, value types, exhaustive `switch` — are designed to catch the same bugs Objective-C let through for two decades. This course treats it as a general-purpose language via the command line, no Xcode required, so the concepts transfer even if you never touch UIKit.

## Setup (Day 0)
{: #setup-day-0 }

On macOS, Xcode's command-line tools include the compiler. On Linux, install the toolchain from swift.org.

```bash
swift --version
mkdir SwiftLab && cd SwiftLab
swift package init --type executable
```

Each day's code below can also run directly as a script: save it as `day.swift` and run `swift day.swift`, no package needed, if you'd rather skip the package boilerplate while you're still on single files.

---

## Day 1: Hello Swift
{: #day-1-hello-swift }

### Why it matters

`let`/`var`, `print`, and string interpolation are the vocabulary every Swift file starts from — SwiftUI views, Vapor route handlers, and command-line scripts all sit on top of these same three things.

### Mental model

`let` binds a value once; `var` allows reassignment. This is stricter than it looks: for value types (structs, including `Int`, `String`, arrays), a `let` binding also makes the value's *contents* immutable, not just the reference — you can't call a mutating method on a `let` struct. String interpolation with `\(expression)` accepts any expression, not just identifiers, so `\(name.uppercased())` works exactly as you'd hope.

### Code along

```swift
import Foundation

let greeting = "Hello"
var visitCount = 0

let arguments = CommandLine.arguments
let target = arguments.count > 1 ? arguments[1] : "world"
visitCount += 1

print("\(greeting), \(target)!")
print("Visits this run: \(visitCount)")
print("Uppercased: \(target.uppercased())")
```

Run it with `swift day1.swift Ada` (or `swift run` inside the package, passing args after `--`). `CommandLine.arguments[0]` is always the program name/path, so real arguments start at index 1 — a detail that trips people up coming from languages where `argv[0]` is stripped for you.

### Common mistake

Declaring `let visitCount = 0` and then writing `visitCount += 1`, expecting it to work because "it's just a counter." Swift's compiler rejects this at compile time with "Left side of mutating operator isn't mutable" — decide up front whether a binding's value changes over its lifetime.

### Your task

Change the program to read a name from standard input with `readLine()` when no CLI argument is given. `readLine()` returns `String?` — handle the `nil` case (empty input / EOF) by printing an error to `FileHandle.standardError` and exiting via `exit(1)`.

**Check:** `echo "Ada" | swift day1.swift` prints `Hello, Ada!` and `Visits this run: 1`; `printf "" | swift day1.swift` (immediate EOF, `readLine()` returns `nil`) prints an error to stderr and `echo $?` afterward shows `1`.

---

## Day 2: Optionals
{: #day-2-optionals }

### Why it matters

Objective-C let any object pointer be `nil` with no compiler help; Swift's optionals make "this might not have a value" part of the type itself, so `nil`-related crashes get caught while you're typing, not when a user hits an edge case in production.

### Mental model

`String` and `String?` are different types — you cannot pass an optional where a non-optional is expected without unwrapping it first. `if let` and `guard let` both unwrap safely, binding a new non-optional constant only inside the scope where the value is confirmed present; `guard let` is preferred at the top of a function because it lets you exit early and keep the "happy path" unindented. `??` (nil-coalescing) supplies a default. Force-unwrap (`!`) skips all of that and crashes immediately if the value is `nil` — same trade-off as Kotlin's `!!`.

### Code along

```swift
func parseAge(_ input: String?) -> Int? {
    guard let trimmed = input?.trimmingCharacters(in: .whitespaces) else { return nil }
    return Int(trimmed)
}

func describe(_ input: String?) {
    if let age = parseAge(input) {
        print("You are \(age) years old.")
    } else {
        print("Could not read an age from '\(input ?? "nil")'.")
    }
}

describe("34")
describe("  41  ")
describe("banana")
describe(nil)
```

`Int("banana")` returning `nil` instead of throwing is exactly the same pattern as Kotlin's `toIntOrNull()` — Swift's standard library leans on optionals for "this parse might fail" everywhere, not exceptions.

### Common mistake

Force-unwrapping the result of `Int(someString)` — `let age = Int(input)!` — because "the input always looks like a number in testing." The moment a genuinely malformed string reaches that line in production, the process crashes with no recoverable error. Reserve `!` for cases where `nil` would represent an actual programming bug you already ruled out a few lines earlier, never for parsing external input.

### Your task

Write `func readConfigValue(_ config: [String: String], key: String) -> Int?` that looks up `key` in a dictionary and parses the value as `Int`, returning `nil` if the key is missing or the value isn't numeric. Test with `["port": "8080", "timeout": "abc"]`, printing both results with `?? -1` as the fallback.

**Check:** `readConfigValue(config, key: "port") ?? -1` prints `8080`; `readConfigValue(config, key: "timeout") ?? -1` prints `-1`; `readConfigValue(config, key: "missing") ?? -1` also prints `-1`, covering both failure reasons (bad value and missing key) with the same fallback.

---

## Day 3: Structs & methods
{: #day-3-structs-methods }

### Why it matters

Most Swift APIs — including nearly everything in the standard library and SwiftUI — are structs, not classes. Understanding value semantics (copies, not shared references) up front prevents a specific class of bug where mutating what you think is "the same object" somewhere else silently doesn't affect the original.

### Mental model

A `struct` is a value type: assigning it to a new variable or passing it to a function copies the value (Swift optimizes this under the hood, but the observable behavior is "independent copies"). Methods that change a struct's own properties must be marked `mutating`, and you can only call a `mutating` method on a `var`, never a `let` — that's the compiler enforcing the "value types are copied" model from Day 1.

### Code along

```swift
struct BankAccount {
    let owner: String
    private(set) var balanceCents: Int = 0

    mutating func deposit(_ cents: Int) {
        precondition(cents > 0, "deposit amount must be positive")
        balanceCents += cents
    }

    mutating func withdraw(_ cents: Int) -> Bool {
        guard cents > 0, cents <= balanceCents else { return false }
        balanceCents -= cents
        return true
    }
}

var account = BankAccount(owner: "Ada")
account.deposit(5000)
let ok = account.withdraw(2000)
let tooMuch = account.withdraw(10000)

print("Balance: \(account.balanceCents) cents")
print("First withdrawal succeeded: \(ok)")
print("Second withdrawal succeeded: \(tooMuch)")

var copy = account
copy.deposit(100)
print("Original balance: \(account.balanceCents), copy balance: \(copy.balanceCents)")
```

That last block is the whole lesson: mutating `copy` after assignment never touches `account` — they're independent values, not two references to the same object.

### Common mistake

Declaring an account as `let account = BankAccount(...)` and then calling `account.deposit(...)`, expecting it to work because `deposit` only changes a property, not the whole struct. It won't compile — `deposit` is `mutating`, and mutating methods require a `var` binding. This is Swift telling you, correctly, that reassigning any property of a `let` struct is disallowed.

### Your task

Add a `struct Transaction { let kind: String; let cents: Int }` and a `private var history: [Transaction] = []` to `BankAccount`, appending an entry on every successful deposit/withdrawal. Add `func printStatement()` that prints each transaction and the running balance after it.

**Check:** for the exact sequence in the code above (`deposit(5000)`, `withdraw(2000)` succeeds, `withdraw(10000)` fails), `printStatement()` prints exactly **two** entries, not three — the failed `10000` withdrawal must not appear in history — and the running balance shown after the second entry is `3000`, matching `account.balanceCents`.

---

## Day 4: Enums
{: #day-4-enums }

### Why it matters

Swift enums with associated values are how the language represents "one of a fixed set of shapes, each carrying its own data" — API responses, parse results, navigation destinations. Combined with exhaustive `switch`, they give you the same compiler-enforced completeness as Kotlin's sealed classes, in a lighter-weight form.

### Mental model

An enum case can carry associated values of different types per case: `case ok(Int)` and `case err(String)` are structurally different, unlike a class hierarchy where every subtype shares a base shape. `switch` over an enum without a `default` must cover every case — the compiler checks this regardless of whether the `switch` is used as an expression or a statement, which is actually stricter (in a good way) than Kotlin's `when`.

### Code along

```swift
enum FetchResult {
    case ok(Int)
    case err(String)
}

func describe(_ result: FetchResult) -> String {
    switch result {
    case .ok(let value):
        return "Got value: \(value)"
    case .err(let message):
        return "Failed: \(message)"
    }
}

enum HTTPMethod: String {
    case get = "GET"
    case post = "POST"
    case delete = "DELETE"
}

let results: [FetchResult] = [.ok(42), .err("timeout"), .ok(0)]
for r in results {
    print(describe(r))
}

for method in [HTTPMethod.get, .post, .delete] {
    print("\(method) -> \(method.rawValue)")
}
```

`HTTPMethod` is a `String`-backed enum — useful whenever you need a fixed set of values that also has a natural textual representation, like methods, statuses, or currency codes.

### Common mistake

Adding a new case to an enum (say, `case redirect(String)` to `FetchResult`) and forgetting that every exhaustive `switch` over it elsewhere in the codebase now fails to compile until updated. That's a feature, not a bug — it's the compiler doing the work of finding every place that needs updating for you — but if you "fix" it by adding a blanket `default:` case just to make it compile, you've thrown away exactly that safety net.

### Your task

Add a third case `case redirect(String)` to `FetchResult` (carrying a URL) and update `describe` to handle it without adding a `default` branch — let the compiler guide you to every spot that needs a change.

**Check:** before updating `describe`, `swift day4.swift` fails to compile with an error naming `switch must be exhaustive`; after adding the `.redirect(let url)` case, `describe(.redirect("https://example.com"))` returns a string containing `https://example.com`, and adding `.redirect("https://example.com")` to `results` prints that line alongside the existing two.

---

## Day 5: Collections
{: #day-5-collections }

### Why it matters

`Array`, `Dictionary`, and `Set`, combined with `map`/`filter`/`reduce`, cover the vast majority of everyday data shuffling — the same three collection types show up whether you're processing JSON, table rows, or UI model data.

### Mental model

`Array` preserves order and allows duplicates; `Set` has no order and no duplicates (elements must be `Hashable`); `Dictionary` maps unique keys to values. Like Swift structs generally, all three are value types with copy-on-write — assigning one to a new variable is "free" until you mutate one of the copies, at which point it actually copies the storage.

### Code along

```swift
let words = ["swift", "kotlin", "go", "rust", "swift", "python", "go", "go"]

var counts: [String: Int] = [:]
for word in words {
    counts[word, default: 0] += 1
}

let sortedByCount = counts.sorted { $0.value > $1.value }
print("Frequency:")
for (word, count) in sortedByCount {
    print("  \(word) -> \(count)")
}

let byFirstLetter = Dictionary(grouping: Set(words)) { $0.first! }
print("Grouped by first letter: \(byFirstLetter)")

let longWordsUppercased = Set(words).filter { $0.count > 3 }.map { $0.uppercased() }
print("Long words, uppercased: \(longWordsUppercased.sorted())")
```

`counts[word, default: 0] += 1` is the idiomatic word-counter one-liner — it reads a current value or `0` if absent, and writes back in the same expression, no manual `if let` needed.

### Common mistake

Iterating a `Dictionary` and assuming a stable order across runs — Swift dictionaries make no ordering guarantee, so code that "worked" printing keys in insertion order during testing can print a different order tomorrow. If order matters, sort explicitly (as `sorted(by:)` does above) rather than relying on iteration order.

### Your task

Given `let sentence = "the quick brown fox jumps over the lazy dog the fox runs"`, split it on whitespace, then print: the top 3 most frequent words with counts, and a `[Int: [String]]` grouping distinct words by their length.

**Check:** the frequency ranking starts `the -> 3`, `fox -> 2` (everything else ties at count 1, so the third entry is unpredictable — that's expected). The length dictionary has exactly three keys, `3`, `4`, and `5`; key `3` contains `{the, fox, dog}`, key `4` contains `{over, lazy, runs}`, key `5` contains `{quick, brown, jumps}` — check membership, not array order, since `Set` (used for `distinct` here) makes no ordering guarantee.

---

## Day 6: Protocols
{: #day-6-protocols }

### Why it matters

Protocols are Swift's interfaces, and protocol-oriented design (favoring composition of small protocols over deep class hierarchies) is the idiom the language and its standard library are built around — `Equatable`, `Comparable`, and `Codable` are all protocols you'll conform your own types to constantly.

### Mental model

A `protocol` declares required properties/methods; `struct`s, `enum`s, and `class`es can all conform. Protocol extensions let you provide a default implementation once, inherited by every conforming type that doesn't override it — this is how you get shared behavior without inheritance.

### Code along

```swift
protocol Shape {
    var area: Double { get }
    var perimeter: Double { get }
}

extension Shape {
    var description: String {
        "area=\(String(format: "%.2f", area)), perimeter=\(String(format: "%.2f", perimeter))"
    }
}

struct Circle: Shape {
    let radius: Double
    var area: Double { .pi * radius * radius }
    var perimeter: Double { 2 * .pi * radius }
}

struct Rectangle: Shape {
    let width: Double
    let height: Double
    var area: Double { width * height }
    var perimeter: Double { 2 * (width + height) }
}

let shapes: [Shape] = [Circle(radius: 3), Rectangle(width: 4, height: 5)]
for shape in shapes {
    print(shape.description)
}
```

`description` is defined once in the protocol extension and used by both `Circle` and `Rectangle` without either type writing a line of formatting code — that's the payoff of protocol-oriented design over copy-pasted helper methods.

### Common mistake

Declaring a protocol requirement as a `let`-style read-only property (`var area: Double { get }`) and then trying to conform with a stored `var` that you expected callers to mutate directly. `{ get }` only requires a getter — conforming types are free to implement it as computed (as above) or as a plain stored property; either satisfies the protocol, but callers of the protocol type can never *set* it, only read it, regardless of how the concrete type implements storage.

### Your task

Add a new type `struct Triangle: Shape` (base and height only, area = `0.5 * base * height`; for perimeter, assume equilateral and use `3 * base`), add it to the `shapes` array, and confirm `description` works with zero additional code in the protocol extension.

**Check:** `Triangle(base: 4, height: 3).description` prints `area=6.00, perimeter=12.00` — computed entirely from the protocol extension you didn't touch, using only the `area`/`perimeter` you implemented on `Triangle` itself.

---

## Day 7: Error handling
{: #day-7-error-handling }

### Why it matters

`throws`/`try`/`do-catch` is how Swift represents "this operation can fail in a specific, typed way" for things optionals aren't expressive enough for — you often need to know *why* something failed, not just that it did.

### Mental model

A function marked `throws` can `throw` any value conforming to `Error` (usually an `enum`); callers must handle it with `try` inside a `do { } catch { }` block, or propagate it further by marking the calling function `throws` too. Unlike optionals, the error carries information about *what* went wrong, which you pattern-match on in the `catch` clause.

### Code along

```swift
enum ValidationError: Error, CustomStringConvertible {
    case empty
    case tooLong(limit: Int)

    var description: String {
        switch self {
        case .empty: return "value must not be empty"
        case .tooLong(let limit): return "value exceeds \(limit) characters"
        }
    }
}

func validateUsername(_ name: String) throws -> String {
    if name.isEmpty { throw ValidationError.empty }
    if name.count > 20 { throw ValidationError.tooLong(limit: 20) }
    return name
}

let candidates = ["ada", "", String(repeating: "x", count: 30)]
for candidate in candidates {
    do {
        let valid = try validateUsername(candidate)
        print("Valid: \(valid)")
    } catch let error as ValidationError {
        print("Rejected '\(candidate)': \(error)")
    } catch {
        print("Unexpected error: \(error)")
    }
}
```

Catching `ValidationError` specifically (before the generic fallback `catch`) lets you handle known failure modes distinctly from anything unforeseen — always order `catch` clauses from most specific to least.

### Common mistake

Using `try!` to skip error handling because "this call can't realistically fail here." `try!` crashes the process immediately if it's wrong, exactly like force-unwrapping an optional — appropriate only for truly programmer-error conditions (a malformed literal you wrote yourself), never for anything touching a file, network, or user input.

### Your task

Add a case `case containsWhitespace` to `ValidationError`, thrown when the username contains a space, and update `validateUsername` and its `description` to handle it. Test with `"ada lovelace"` as one of the candidates.

**Check:** the loop's output for `"ada lovelace"` reads `Rejected 'ada lovelace': ...` with your `containsWhitespace` message (mentioning "whitespace" or "space") — and it's caught by the specific `catch let error as ValidationError` clause, not the generic fallback `catch`, proving the new case really is a `ValidationError`.

---

## Day 8: Closures
{: #day-8-closures }

### Why it matters

Closures are how Swift passes "a piece of behavior" as a value — sorting comparators, completion handlers, SwiftUI button actions. Trailing closure syntax is everywhere in idiomatic Swift, so reading it fluently is non-negotiable.

### Mental model

A closure captures variables from its surrounding scope by reference (for `var`) — if you mutate a captured variable after creating the closure, the closure sees the updated value the next time it runs, not a frozen snapshot from creation time. Trailing closure syntax lets the last closure argument move outside the parentheses: `sorted(by: { $0 < $1 })` becomes `sorted { $0 < $1 }`.

### Code along

```swift
func makeCounter() -> () -> Int {
    var count = 0
    return {
        count += 1
        return count
    }
}

let counterA = makeCounter()
let counterB = makeCounter()
print(counterA(), counterA(), counterA())
print(counterB())

let numbers = [5, 3, 8, 1, 9]
let sortedDescending = numbers.sorted { $0 > $1 }
let squaresOfEven = numbers.filter { $0 % 2 == 0 }.map { $0 * $0 }

print("Descending: \(sortedDescending)")
print("Squares of evens: \(squaresOfEven)")
```

`counterA` and `counterB` each capture their *own* independent `count` variable from separate calls to `makeCounter()` — printing `counterA()` three times gives `1 2 3` while `counterB()` still starts fresh at `1`, which is the clearest demonstration that captures are per-closure-instance, not shared globally.

### Common mistake

Capturing `self` strongly inside a closure stored as a property (common in completion handlers), creating a retain cycle where the object keeps the closure alive and the closure keeps the object alive, so neither is ever deallocated. The fix, once you get to class-based code with stored closures, is `[weak self]` in the capture list — worth knowing about now even though today's exercises use only value types and local closures where it doesn't yet bite.

### Your task

Implement `func once(_ action: @escaping () -> Void) -> () -> Void` that returns a closure wrapping `action`, guaranteeing `action` runs on only the *first* call, doing nothing on subsequent calls. Verify by wrapping a closure that prints `"ran!"`, calling the wrapped version three times, and confirming the message prints exactly once.

**Check:** `let runOnce = once { print("ran!") }; runOnce(); runOnce(); runOnce()` prints `ran!` exactly **one** time total, not three.

---

## Day 9: Async basics
{: #day-9-async-basics }

### Why it matters

Modern Swift concurrency (`async`/`await`, introduced in Swift 5.5) replaced a decade of nested completion-handler callbacks with code that reads top-to-bottom, while still being non-blocking under the hood — essential for anything that talks to the network or disk without freezing the UI thread.

### Mental model

An `async` function can suspend at each `await` point without blocking the thread it's running on, similar in spirit to Kotlin's `suspend`. `Task { }` starts new concurrent work from synchronous code — it's the bridge, analogous to `launch` in Kotlin coroutines. `Task.sleep(for:)` suspends without blocking, the async equivalent of avoiding `Thread.sleep`.

### Code along

```swift
import Foundation

func fetchPrice(item: String, delayMs: UInt64) async -> Int {
    try? await Task.sleep(nanoseconds: delayMs * 1_000_000)
    return item.count * 100
}

@main
struct Demo {
    static func main() async {
        let start = Date()

        async let apple = fetchPrice(item: "apple", delayMs: 300)
        async let kiwi = fetchPrice(item: "kiwi", delayMs: 500)
        async let fig = fetchPrice(item: "fig", delayMs: 200)

        let results = await [apple, kiwi, fig]
        let elapsed = Date().timeIntervalSince(start) * 1000

        print("Prices: \(results)")
        print("Elapsed: \(Int(elapsed))ms")
    }
}
```

Save this as `Sources/SwiftLab/main.swift` in the package from Day 0 (the `@main` attribute needs a proper executable target) and run `swift run`. `async let` starts all three fetches concurrently; if elapsed lands near 500ms rather than 1000ms, you've confirmed they actually overlapped instead of running one after another.

### Common mistake

Writing three separate `await fetchPrice(...)` calls in sequence instead of using `async let`. `await` on its own does **not** imply concurrency — `let a = await fetchPrice(...)` followed by `let b = await fetchPrice(...)` runs strictly one after the other, each fully finishing before the next starts. `async let` is specifically what launches them in parallel; forgetting this is the single most common Swift-concurrency performance bug.

### Your task

Add a fourth item and change `fetchPrice` so it throws `URLError(.timedOut)` when `item == "kiwi"`. Wrap the `await` for `kiwi` in a `do/catch` (or use `try?` and handle `nil`) so one failure doesn't cancel the other two `async let` bindings, and print `"kiwi failed"` in that case.

**Check:** the run prints `500` (apple's price, `"apple".count * 100`), `300` (fig's price), and `kiwi failed` — all three lines appear despite kiwi throwing, proving the other two `async let` bindings were never cancelled by the failure.

---

## Day 10: CLI tool
{: #day-10-cli-tool }

### Why it matters

`CommandLine.arguments` plus `FileManager` is the entire toolkit behind most small Swift command-line utilities — no third-party dependency needed until you want polished flag parsing (that's what `swift-argument-parser` is for, once you outgrow manual handling).

### Mental model

Treat `CommandLine.arguments` as a plain `[String]` you parse yourself: dispatch on the first real argument, read the rest positionally, and use `exit(code)` to signal success/failure to whatever invoked your process. Persistent state has to go through the filesystem (`FileManager`, `String(contentsOf:)`, `write(to:)`) since each invocation is a fresh process with no memory of the last one.

### Code along

```swift
import Foundation

let storeURL = URL(fileURLWithPath: "todos.txt")

func loadTodos() -> [String] {
    guard let contents = try? String(contentsOf: storeURL, encoding: .utf8) else { return [] }
    return contents.split(separator: "\n").map(String.init).filter { !$0.isEmpty }
}

func saveTodos(_ todos: [String]) {
    let text = todos.joined(separator: "\n")
    try? text.write(to: storeURL, atomically: true, encoding: .utf8)
}

var todos = loadTodos()
let args = CommandLine.arguments

switch args.count > 1 ? args[1] : nil {
case "add":
    let text = args.dropFirst(2).joined(separator: " ")
    if text.isEmpty {
        FileHandle.standardError.write("usage: add <text>\n".data(using: .utf8)!)
        exit(1)
    }
    todos.append("[ ] \(text)")
    saveTodos(todos)
    print("Added: \(text)")
case "list":
    if todos.isEmpty { print("No todos yet.") }
    for (i, todo) in todos.enumerated() { print("\(i): \(todo)") }
case "done":
    guard args.count > 2, let index = Int(args[2]), todos.indices.contains(index) else {
        FileHandle.standardError.write("usage: done <index>\n".data(using: .utf8)!)
        exit(1)
    }
    todos[index] = todos[index].replacingOccurrences(of: "[ ]", with: "[x]")
    saveTodos(todos)
    print("Marked done: \(todos[index])")
default:
    print("usage: add <text> | list | done <index>")
}
```

Build with `swift build` and run `.build/debug/SwiftLab add "write course"`, `.build/debug/SwiftLab list`, `.build/debug/SwiftLab done 0` — note `args[1]` is the first *real* argument since `args[0]` is always the executable path.

### Common mistake

Using `args.dropFirst(2).joined(separator: " ")` incorrectly as `args[2]` when the todo text contains multiple words. `add write the swift course` arrives as five separate elements in `CommandLine.arguments` because the shell splits on whitespace before your program runs — grabbing only `args[2]` silently drops everything after the first word.

### Your task

Add a `remove <index>` command that deletes a todo and re-saves, shifting later indices down.

**Check:** add three todos, remove index `1`, then run `list` — it shows exactly two entries, `0` and `1`, holding the original 1st and 3rd todos renumbered (not the original indices `0` and `2`).

---

## Capstone project
{: #capstone }

Build a **Swift todo CLI** that pulls together the whole week:

- `struct Todo: Codable` with `id`, `text`, `done` — JSON persistence via `Codable` instead of the plain-text format from Day 10.
- `enum CliError: Error` for bad commands/arguments, surfaced through `do/catch` at the top level — Day 7.
- A `TodoStore` protocol with an in-memory conformance for tests and a file-backed conformance for real runs — Day 6.
- Commands dispatched on `CommandLine.arguments`, covering `add`, `list`, `done`, `remove` — Day 10.

Stretch goal: make `loadTodos`/`saveTodos` `async` and use `async let` to load todos while simultaneously validating the store file's existence, printing a warning if the file was missing on first run — small, but it forces you to actually use Day 9's concurrency instead of just reading about it.

**Acceptance check:** running `add`, `add`, `done 0`, `remove 1`, `list` against a fresh store shows exactly one todo, marked done, at index `0`; the persisted JSON file (`cat todos.json`) round-trips cleanly through a second `list` invocation in a brand-new process, proving `Codable` persistence — not in-memory state — is what's driving the output.

## Related

- [Kotlin in 10 Days](/courses/kotlin-10-days/)
- [TypeScript in 10 Days](/courses/typescript-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
