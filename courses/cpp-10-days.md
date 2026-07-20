---
layout: course
title: "C++ in 10 Days — Hands-On"
permalink: /courses/cpp-10-days/
course_track: "C++"
description: "RAII, the STL, and smart pointers — build a working C++20 CLI without the legacy maze."
toc:
  - id: "day-1-hello-build"
    label: "Day 1: Hello & build"
  - id: "day-2-types-references"
    label: "Day 2: Types & references"
  - id: "day-3-classes-raii"
    label: "Day 3: Classes & RAII"
  - id: "day-4-stl-vectors-algorithms"
    label: "Day 4: STL vectors & algorithms"
  - id: "day-5-maps-unordered_map"
    label: "Day 5: Maps & unordered_map"
  - id: "day-6-smart-pointers"
    label: "Day 6: Smart pointers"
  - id: "day-7-optional-variants-lite"
    label: "Day 7: Optional & variants lite"
  - id: "day-8-exceptions"
    label: "Day 8: Exceptions"
  - id: "day-9-headers-multi-file"
    label: "Day 9: Headers & multi-file"
  - id: "day-10-cli-tool"
    label: "Day 10: CLI tool"
  - id: "capstone"
    label: "Capstone project"
---

# C++ in 10 Days — Hands-On

RAII, the STL, and smart pointers — build a working C++20 CLI without the legacy maze.

## Why this language
{: #why-this-language }

C++ still owns games, browsers, HFT-adjacent systems, and embedded firmware, because nothing else gives you both manual control over memory layout and zero-cost abstractions at the same time. The catch is that "C++" spans thirty years of accumulated features, and a lot of tutorials teach the 1998 subset. This course sticks to modern C++17/20 idioms — RAII, `std::vector` over raw arrays, smart pointers over raw `new`/`delete` — because that's the C++ you'll actually be expected to write in a codebase started this decade.

## Setup (Day 0)
{: #setup-day-0 }

```bash
g++ --version   # or clang++ --version
mkdir cpp-lab && cd cpp-lab
```

Compile and run every example below with:

```bash
g++ -std=c++20 -Wall -Wextra -O2 main.cpp -o main && ./main
```

`-Wall -Wextra` surfaces mistakes (unused variables, sign comparisons) that the compiler will happily let slide by default — leave these flags on for the whole course.

---

## Day 1: Hello & build
{: #day-1-hello-build }

### Why it matters

Getting from source to a running binary — `main`, `iostream`, and the compile command itself — is the first wall for C++ beginners coming from interpreted languages. Once the compile-and-run loop is muscle memory, everything else in this course is just new syntax inside the same loop.

### Mental model

`int main()` returning `0` tells the OS "success"; any nonzero return is a failure code the calling shell or script can check. `std::cout` is a stream you write to with `<<`, not a function you call — that's why chained `<<` works (`std::cout << a << b`) the way chained `.method()` calls work in other languages. `argc`/`argv` are the C-style argument count and array — `argv[0]` is the program's own invocation path, real arguments start at `argv[1]`.

### Code along

```cpp
#include <iostream>

int main(int argc, char** argv) {
    std::cout << "Hello, C++!\n";
    std::cout << "Received " << argc - 1 << " argument(s):\n";
    for (int i = 1; i < argc; ++i) {
        std::cout << "  [" << i << "] " << argv[i] << "\n";
    }
    return 0;
}
```

Run `./main Ada Lovelace` and confirm the loop prints both names with correct indices — `argc` is the *total* count including the program name, which is why the loop starts at `1` and the visible count is `argc - 1`.

### Common mistake

Forgetting `\n` (or `std::endl`) and being confused when multiple `std::cout` calls print on the same line with no separation — `std::cout` doesn't add newlines for you between statements, unlike `println` in some other languages. `std::endl` also flushes the output buffer, which matters (and costs a little performance) when you're debugging interleaved output; `\n` alone is usually enough and slightly faster in tight loops.

### Your task

Extend the program to print `"no arguments given"` when `argc == 1`, and to print the arguments in reverse order when the first argument is exactly `"--reverse"` (excluding that flag itself from the printed list).

**Check:** `./main` (no args) prints exactly `no arguments given`; `./main --reverse Ada Lovelace` prints `Lovelace` then `Ada`, in that order, with `--reverse` itself never appearing in the printed list.

---

## Day 2: Types & references
{: #day-2-types-references }

### Why it matters

References are how C++ lets a function modify a caller's variable without the syntax noise of explicit pointers — understanding when you're looking at a reference versus a copy is the difference between code that behaves as expected and code with silent, expensive copies of large objects.

### Mental model

`int& x` in a parameter list means `x` is an alias for the caller's variable, not a new copy — writes through it are visible to the caller. Plain `int x` is a copy; changes inside the function are invisible outside it. `const T&` is the idiom for "let me look at this large object without copying it and without letting me modify it" — use it for any parameter bigger than a machine word that you don't need to mutate. `auto` infers the type from the initializer, useful for verbose iterator/template types, but don't let it hide a type you genuinely need to think about (like an unexpected copy versus reference).

### Code along

```cpp
#include <iostream>
#include <string>

void increment(int& x) {
    x += 1;
}

void swapValues(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

std::string shout(const std::string& text) {
    std::string result = text;
    for (char& c : result) c = static_cast<char>(std::toupper(c));
    return result;
}

int main() {
    int n = 10;
    increment(n);
    std::cout << "n after increment: " << n << "\n";

    int a = 1, b = 2;
    swapValues(a, b);
    std::cout << "a=" << a << " b=" << b << "\n";

    std::string message = "hello";
    std::cout << shout(message) << " (original unchanged: " << message << ")\n";
}
```

`shout` takes its parameter by `const&` (no copy on the way in) but builds and returns a fresh `std::string` rather than mutating the caller's — the "original unchanged" line in the output confirms it.

### Common mistake

Passing large objects (`std::string`, `std::vector`, custom structs) by value into functions that never need to modify them: `void printAll(std::vector<int> v)` silently copies the entire vector on every call. Write `const std::vector<int>&` instead unless you specifically need an independent copy inside the function — this single habit is one of the biggest, easiest performance wins in everyday C++.

### Your task

Write `void clampInPlace(int& value, int lo, int hi)` that clamps `value` into `[lo, hi]` by reference (no return value), and `int clamp(int value, int lo, int hi)` that does the same thing but returns a new value, leaving the argument untouched. Call both on the same variable and print the results to show the difference.

**Check:** starting from `int v = 150;`, calling `clampInPlace(v, 0, 100)` changes `v` itself to `100`. Separately, starting from `int w = 150;`, calling `int result = clamp(w, 0, 100);` leaves `w` still `150` while `result` is `100` — same math, opposite mutation behavior.

---

## Day 3: Classes & RAII
{: #day-3-classes-raii }

### Why it matters

RAII (Resource Acquisition Is Initialization) is the single idea that replaces manual `malloc`/`free` and `new`/`delete` discipline with the compiler automatically calling destructors when objects go out of scope — it's why modern C++ can be memory-safe-by-construction for the common cases without a garbage collector.

### Mental model

A constructor acquires a resource (opens a file, allocates memory); the destructor releases it, and the compiler guarantees the destructor runs when the object's scope ends — normal return, early return, or exception, it doesn't matter. "Rule of zero" means: if your class doesn't manage a raw resource directly, don't write a destructor, copy constructor, or assignment operator at all — let the compiler-generated ones (which just RAII-delegate to your members) do the job.

### Code along

```cpp
#include <iostream>

class Counter {
    int count_ = 0;

public:
    void tick() { ++count_; }
    int value() const { return count_; }
};

class ScopedLogger {
    std::string name_;

public:
    explicit ScopedLogger(std::string name) : name_(std::move(name)) {
        std::cout << "[enter] " << name_ << "\n";
    }
    ~ScopedLogger() {
        std::cout << "[exit]  " << name_ << "\n";
    }
};

void doWork() {
    ScopedLogger log("doWork");
    Counter c;
    c.tick();
    c.tick();
    std::cout << "count = " << c.value() << "\n";
}

int main() {
    doWork();
    std::cout << "back in main\n";
}
```

Run this and read the output order: `[enter] doWork`, `count = 2`, `[exit] doWork`, `back in main` — the destructor fires automatically the instant `doWork` returns, with zero manual cleanup code at the call site.

### Common mistake

Writing a class that owns a raw resource (a raw pointer from `new`, a file descriptor from a C API) and forgetting the destructor entirely, "because it worked in testing." It leaks every single resource the moment the object goes out of scope, silently, with no crash to alert you — leaks only show up later as memory growth or "too many open files" under sustained load. If a class touches a raw resource directly, it needs RAII (a destructor, and correct copy/move semantics); if it only holds other RAII types (`std::string`, `std::vector`, smart pointers) as members, rule of zero applies and you write nothing extra.

### Your task

Write a `class BankAccount` with a private `int balanceCents_`, a constructor taking the opening balance, and `deposit(int cents)` / `bool withdraw(int cents)` methods (the latter returns `false` and changes nothing on insufficient funds). Add a destructor that prints the final balance when the account goes out of scope, and confirm it fires by creating one inside a nested `{ }` block in `main`.

**Check:** inside a nested block, construct with opening balance `1000`, `deposit(500)` (balance `1500`), then `withdraw(2000)` (returns `false`, balance still `1500`) — the destructor's printed final balance is `1500`, and that print appears *before* whatever you print immediately after the closing `}` of the nested block, proving the destructor really ran at scope exit, not at program exit.

---

## Day 4: STL vectors & algorithms
{: #day-4-stl-vectors-algorithms }

### Why it matters

`std::vector` is the default container for "a sequence of things" in modern C++ — it manages its own memory (RAII again), grows as needed, and pairs with `<algorithm>` functions like `std::sort` that are both more expressive and typically faster than a hand-rolled loop, because the standard library implementations are heavily tuned.

### Mental model

A `vector` owns a contiguous, heap-allocated buffer that it resizes (usually by doubling) as elements are added — indexing is O(1), like an array, but `push_back` is amortized O(1), not always-O(1), because of occasional reallocation. Range-based `for (auto& x : v)` iterates by reference when you write `auto&` (so mutations stick) versus by value with plain `auto` (a copy per element). Algorithms like `std::sort(v.begin(), v.end())` take iterator *ranges*, not the container itself — that's what lets the same `std::sort` work on vectors, arrays, and deques alike.

### Code along

```cpp
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> scores{72, 95, 88, 60, 95, 72, 100};

    std::sort(scores.begin(), scores.end());
    std::cout << "sorted: ";
    for (int s : scores) std::cout << s << " ";
    std::cout << "\n";

    auto last = std::unique(scores.begin(), scores.end());
    scores.erase(last, scores.end());
    std::cout << "deduplicated: ";
    for (int s : scores) std::cout << s << " ";
    std::cout << "\n";

    int total = 0;
    for (int s : scores) total += s;
    double average = static_cast<double>(total) / static_cast<double>(scores.size());
    std::cout << "average: " << average << "\n";

    auto passing = std::count_if(scores.begin(), scores.end(), [](int s) { return s >= 70; });
    std::cout << "passing count: " << passing << "\n";
}
```

`std::unique` only removes *adjacent* duplicates — that's why the vector must be sorted first; running `unique` on an unsorted range silently leaves non-adjacent duplicates in place, which is a very common bug.

### Common mistake

Calling `std::unique` on an unsorted vector and expecting all duplicates gone. `std::unique` collapses only consecutive equal runs and returns an iterator marking the new logical end — everything from there to the old end is leftover garbage that must be removed with `erase`, exactly as shown above. Skipping the `erase` step is the second half of this same mistake: `unique` alone doesn't shrink the vector's size.

### Your task

Given `std::vector<int> temps{68, 72, 75, 75, 68, 90, 61, 90}`, compute and print the minimum, maximum, and median (sort a copy first) without using any third-party library — only `<algorithm>` and `<vector>`.

**Check:** sorted, `temps` is `61 68 68 72 75 75 90 90` — minimum is `61`, maximum is `90`, and the median (average of the two middle values in this 8-element set) is `73.5` (the average of `72` and `75`).

---

## Day 5: Maps & unordered_map
{: #day-5-maps-unordered_map }

### Why it matters

Counting, grouping, and looking up "value for this key" is everywhere in real code, and `std::unordered_map` (hash map, average O(1) lookup) versus `std::map` (sorted, O(log n), red-black tree) is a decision you'll make on nearly every project — knowing which one and why matters more than memorizing the API.

### Mental model

`unordered_map` gives no ordering guarantee but is faster on average for pure lookups; `map` keeps keys sorted (useful if you need ordered iteration or range queries) at the cost of slower operations. `m[key]` on either type **inserts** a default-constructed value if `key` isn't present yet — a read-looking expression that can silently write. Structured bindings (`auto [key, value] : m`) make iterating pairs readable without `.first`/`.second` noise.

### Code along

```cpp
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

int main() {
    std::vector<std::string> words{"cpp", "rust", "go", "cpp", "zig", "go", "go"};

    std::unordered_map<std::string, int> counts;
    for (const auto& word : words) {
        counts[word]++;
    }

    for (const auto& [word, count] : counts) {
        std::cout << word << " -> " << count << "\n";
    }

    if (auto it = counts.find("go"); it != counts.end()) {
        std::cout << "'go' seen " << it->second << " time(s)\n";
    }

    if (counts.find("java") == counts.end()) {
        std::cout << "'java' was never seen\n";
    }
}
```

`counts[word]++` is the idiomatic counter increment — the first time a word appears, `counts[word]` default-constructs to `0` and then increments to `1`, no manual "does this key exist yet" check needed.

### Common mistake

Using `m[key]` to *check* whether a key exists (`if (m[key] == someDefault)`), which silently inserts `key` with a default value if it wasn't already there — you end up mutating the map just by asking a question about it. Use `m.find(key) != m.end()` or `m.count(key) > 0` (or `m.contains(key)` in C++20) for lookups where you don't want an insertion side effect.

### Your task

Given the same `words` vector, use `std::unordered_map<std::string, std::vector<int>>` to record the *positions* (indices) each word appears at, then print each word alongside its list of positions.

**Check:** for `{"cpp", "rust", "go", "cpp", "zig", "go", "go"}`, `positions["go"]` is `[2, 5, 6]`, `positions["cpp"]` is `[0, 3]`, `positions["rust"]` is `[1]`, and `positions["zig"]` is `[4]`.

---

## Day 6: Smart pointers
{: #day-6-smart-pointers }

### Why it matters

Smart pointers apply RAII to heap allocation itself — `std::unique_ptr` and `std::shared_ptr` mean you almost never write a bare `delete`, which eliminates the two classic C++ bugs: forgetting to free memory, and freeing it twice.

### Mental model

`std::unique_ptr<T>` owns its object exclusively — it can't be copied, only moved, so ownership transfer is explicit in the type system. `std::shared_ptr<T>` allows multiple owners via reference counting; the object is destroyed when the last `shared_ptr` to it goes away. Default to `unique_ptr`; reach for `shared_ptr` only when you genuinely need multiple independent owners (rare in well-structured code — often a sign ownership could be clarified instead).

### Code along

```cpp
#include <iostream>
#include <memory>
#include <vector>

struct Shape {
    virtual double area() const = 0;
    virtual ~Shape() = default;
};

struct Circle : Shape {
    double radius;
    explicit Circle(double r) : radius(r) {}
    double area() const override { return 3.14159265 * radius * radius; }
};

struct Rectangle : Shape {
    double width, height;
    Rectangle(double w, double h) : width(w), height(h) {}
    double area() const override { return width * height; }
};

std::unique_ptr<Shape> makeShape(const std::string& kind) {
    if (kind == "circle") return std::make_unique<Circle>(3.0);
    if (kind == "rectangle") return std::make_unique<Rectangle>(4.0, 5.0);
    return nullptr;
}

int main() {
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(makeShape("circle"));
    shapes.push_back(makeShape("rectangle"));

    for (const auto& shape : shapes) {
        std::cout << "area = " << shape->area() << "\n";
    }
}
```

`std::vector<std::unique_ptr<Shape>>` is the idiomatic way to store a heterogeneous collection of polymorphic objects — each `unique_ptr` owns exactly one `Shape`-derived object, and when the vector is destroyed, every owned object is destroyed with it, no manual cleanup loop required.

### Common mistake

Writing `Shape* raw = shape.get();` and then calling `delete raw;` manually somewhere, "just to be safe." `get()` returns a non-owning observer pointer specifically so you *don't* manage its lifetime — deleting it yourself while the `unique_ptr` still exists causes a double-free the moment the `unique_ptr` also destructs, undefined behavior that may not crash immediately, making it far worse than an obvious bug.

### Your task

Add a third shape `Triangle` (base and height, area = `0.5 * base * height`) to the hierarchy, extend `makeShape` to construct it for `"triangle"`, and write a function `double totalArea(const std::vector<std::unique_ptr<Shape>>& shapes)` that sums the areas without taking ownership of anything.

**Check:** with the existing `circle` (radius 3.0, area ≈ `28.27`) and `rectangle` (4×5, area `20.0`) plus a `Triangle(6.0, 4.0)` (area `12.0`), `totalArea(shapes)` returns approximately `60.27` — the sum of all three, computed independently of `totalArea` ever taking ownership (the vector's `unique_ptr`s are untouched afterward).

---

## Day 7: Optional & variants lite
{: #day-7-optional-variants-lite }

### Why it matters

`std::optional<T>` gives C++ a type-safe "might not have a value" without resorting to sentinel values (`-1`, `nullptr` for non-pointer types) or out-parameters — the same job `Int?` does in Kotlin/Swift, now natively available since C++17.

### Mental model

`std::optional<T>` either holds a `T` or is empty (`std::nullopt`) — check with `has_value()` or `if (opt)`, access with `*opt`/`opt->member`, or provide a default with `opt.value_or(fallback)`. Accessing an empty optional with `*opt` is undefined behavior (unlike Kotlin/Swift, which throw or require unwrapping) — always check first, or use `.value()` which throws `std::bad_optional_access` if you want a safety net that fails loudly instead of silently.

### Code along

```cpp
#include <iostream>
#include <optional>
#include <string>
#include <vector>

std::optional<int> parseInt(const std::string& text) {
    try {
        size_t consumed = 0;
        int value = std::stoi(text, &consumed);
        if (consumed != text.size()) return std::nullopt;  // trailing garbage like "12abc"
        return value;
    } catch (const std::exception&) {
        return std::nullopt;
    }
}

int main() {
    std::vector<std::string> inputs{"42", "-7", "banana", "12abc", "0"};

    int sum = 0;
    int skipped = 0;
    for (const auto& text : inputs) {
        if (auto value = parseInt(text)) {
            std::cout << text << " -> " << *value << "\n";
            sum += *value;
        } else {
            std::cout << text << " -> (skipped, not a valid integer)\n";
            ++skipped;
        }
    }
    std::cout << "sum: " << sum << ", skipped: " << skipped << "\n";
}
```

`std::stoi` normally throws on malformed input but silently ignores *trailing* garbage (`std::stoi("12abc")` returns `12` with no error) — the `consumed` out-parameter is how you detect and reject that case, which the code above deliberately does.

### Common mistake

Writing `int value = *parseInt(text);` directly without checking `has_value()` first, assuming "the input always parses in my testing." The moment `text` is genuinely unparseable, dereferencing an empty `optional` is undefined behavior — it might crash, might silently read garbage, might appear to work until a build flag changes. Always check with `if (auto value = ...)` or use `.value_or(default)` when a fallback makes sense.

### Your task

Write `std::optional<double> average(const std::vector<int>& values)` that returns `std::nullopt` for an empty vector instead of dividing by zero, and demonstrate it with both an empty and a non-empty vector, printing `"no data"` for the empty case via `.value_or` logic of your choosing.

**Check:** `average({})` is empty (`has_value()` is `false`), and printing it with your `"no data"` fallback shows exactly that string; `average({2, 4, 6})` returns `4.0`.

---

## Day 8: Exceptions
{: #day-8-exceptions }

### Why it matters

Exceptions are how C++ separates "this operation failed" from the normal return value channel, and — critically — they interact with RAII: an exception propagating out of a scope still runs every destructor along the way, so resources acquired earlier in a function are cleaned up correctly even when you throw partway through.

### Mental model

`throw` raises an exception object (convention: derive from `std::exception` so callers can catch generically via `const std::exception&` and call `.what()`); `try`/`catch` blocks handle it at whatever level chooses to. Catch by `const Type&`, never by value (avoids an extra copy and, for polymorphic exception types, avoids losing the derived type through slicing). Uncaught exceptions terminate the program via `std::terminate` — always have at least a top-level catch-all in `main` for anything you can't otherwise recover from.

### Code along

```cpp
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

class FileError : public std::runtime_error {
public:
    explicit FileError(const std::string& path)
        : std::runtime_error("could not open file: " + path) {}
};

std::string readWholeFile(const std::string& path) {
    std::ifstream in(path);
    if (!in) throw FileError(path);

    std::string contents((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    return contents;
}

int main() {
    try {
        std::string data = readWholeFile("does-not-exist.txt");
        std::cout << "read " << data.size() << " bytes\n";
    } catch (const FileError& e) {
        std::cerr << "handled: " << e.what() << "\n";
    } catch (const std::exception& e) {
        std::cerr << "unexpected: " << e.what() << "\n";
    }

    std::cout << "program continues normally\n";
}
```

Run this as-is (the file genuinely doesn't exist) and confirm you get the "handled:" message followed by "program continues normally" — the exception didn't terminate the process because something caught it at the right level.

### Common mistake

Catching `const std::exception& e` by writing `catch (std::exception e)` (by value) instead. Besides the unnecessary copy, if the actual thrown object is a derived type like `FileError`, catching by value "slices" it down to just the `std::exception` base — you lose any derived-class members or overridden behavior beyond what the base defines. Always catch exceptions by `const Type&`.

### Your task

Add a second custom exception `class ParseError : public std::runtime_error` and a function `int readNumberFromFile(const std::string& path)` that reads the file's contents (reusing `readWholeFile`) and throws `ParseError` if the trimmed contents aren't a valid integer. Handle both `FileError` and `ParseError` distinctly in `main`, printing a different message for each.

**Check:** `printf "42" > num.txt` then `readNumberFromFile("num.txt")` returns `42`; `printf "abc" > bad.txt` then `readNumberFromFile("bad.txt")` throws `ParseError` (caught and printed distinctly from a `FileError`); `readNumberFromFile("missing.txt")` throws `FileError`, not `ParseError` — two different messages for two different `catch` clauses.

---

## Day 9: Headers & multi-file
{: #day-9-headers-multi-file }

### Why it matters

Every real C++ project is more than one file — separating declarations (headers) from definitions (`.cpp` files) is how the language supports independent compilation and reasonable build times, and header guards are the mechanism that keeps a header from breaking the build when it's (correctly) included from multiple places.

### Mental model

A header declares *what exists* (function signatures, class definitions); a `.cpp` file defines *how it works* (function bodies). `#pragma once` (or classic `#ifndef`/`#define` guards) prevents the compiler from processing the same header's contents twice in one translation unit, which would otherwise cause "redefinition" errors the moment two included headers both pull in a third common header. The linker is what stitches separately compiled `.cpp` files (object files) together into one executable — that's why you compile multiple `.cpp` files in a single `g++` invocation, or as separate objects linked afterward.

### Code along

`stats.h`:

```cpp
#pragma once
#include <vector>

double mean(const std::vector<int>& values);
double stddev(const std::vector<int>& values);
```

`stats.cpp`:

```cpp
#include "stats.h"
#include <cmath>
#include <numeric>

double mean(const std::vector<int>& values) {
    if (values.empty()) return 0.0;
    double sum = std::accumulate(values.begin(), values.end(), 0.0);
    return sum / static_cast<double>(values.size());
}

double stddev(const std::vector<int>& values) {
    if (values.size() < 2) return 0.0;
    double m = mean(values);
    double variance = 0.0;
    for (int v : values) variance += (v - m) * (v - m);
    variance /= static_cast<double>(values.size() - 1);
    return std::sqrt(variance);
}
```

`main.cpp`:

```cpp
#include "stats.h"
#include <iostream>
#include <vector>

int main() {
    std::vector<int> samples{4, 8, 6, 5, 3, 7};
    std::cout << "mean: " << mean(samples) << "\n";
    std::cout << "stddev: " << stddev(samples) << "\n";
}
```

Compile all three together in one command: `g++ -std=c++20 -Wall -Wextra main.cpp stats.cpp -o main && ./main`. Notice `main.cpp` never sees the *implementation* of `mean`/`stddev` — only the declarations from `stats.h` — yet linking resolves the calls correctly.

### Common mistake

Putting a non-`inline` function's full *definition* (body) directly in a header instead of just its declaration. If that header is included by more than one `.cpp` file in the same build, the linker sees the same function defined twice across different translation units and fails with a "multiple definition" error — headers declare, `.cpp` files define, and `#pragma once` alone doesn't fix a definition-in-header problem because it only guards against double-inclusion *within a single translation unit*, not across separate ones.

### Your task

Split `main.cpp` above so that a new `formatting.h`/`formatting.cpp` pair provides `std::string formatStats(double mean, double stddev)` returning a one-line summary string, called from `main`. Compile all four files together and confirm it links and runs.

**Check:** `g++ -std=c++20 -Wall -Wextra main.cpp stats.cpp formatting.cpp -o main && ./main` links with zero errors and prints a line containing `5.5` (the mean of `{4, 8, 6, 5, 3, 7}`) and a stddev near `1.87` (`sqrt(3.5)`), sourced entirely from `formatStats`, not a raw `std::cout <<` in `main`.

---

## Day 10: CLI tool
{: #day-10-cli-tool }

### Why it matters

Reading a file, counting lines/words, and reporting via exit codes is the shape of dozens of real Unix tools (`wc`, `grep`, linters) — building a small one yourself is the fastest way to get comfortable with `fstream`, `argv`, and the convention that `0` means success and nonzero means "something went wrong, and here's roughly what."

### Mental model

`std::ifstream` opens a file for reading; check it in a boolean context (`if (!in)`) to detect open failures before you try to read. `std::getline(in, line)` returns the stream itself, which is implicitly convertible to a bool that's false once the stream is exhausted or hits an error — that's what makes `while (std::getline(in, line))` the idiomatic line-reading loop. Exit codes: `return 0` for success, nonzero (by convention, `1` for generic failure) for anything a caller script should treat as an error.

### Code along

```cpp
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "usage: " << argv[0] << " <path>\n";
        return 1;
    }

    std::ifstream in(argv[1]);
    if (!in) {
        std::cerr << "error: could not open '" << argv[1] << "'\n";
        return 1;
    }

    long lineCount = 0;
    long wordCount = 0;
    long charCount = 0;
    std::string line;

    while (std::getline(in, line)) {
        ++lineCount;
        charCount += static_cast<long>(line.size()) + 1;  // +1 for the newline getline strips

        std::istringstream words(line);
        std::string word;
        while (words >> word) ++wordCount;
    }

    std::cout << "lines: " << lineCount << "\n";
    std::cout << "words: " << wordCount << "\n";
    std::cout << "chars: " << charCount << "\n";
    return 0;
}
```

Run it against its own source: `./main main.cpp` — the numbers should roughly match what `wc main.cpp` reports (small discrepancies are expected since a real `wc` counts bytes/characters slightly differently around the final line and encoding).

### Common mistake

Forgetting to check `argc < 2` before touching `argv[1]`, then reading past the end of the `argv` array when the tool is run with no arguments — accessing `argv[1]` when `argc == 1` is undefined behavior, not a clean crash you can rely on. Always validate `argc` first, and return a nonzero exit code with a `usage:` message on `std::cerr` (not `std::cout` — errors belong on stderr so they don't pollute piped output).

### Your task

Add a `-l`-only mode: when invoked as `./main -l <path>`, print only the line count (no labels, just the number) so the output is script-friendly, e.g. usable as `count=$(./main -l file.txt)`. Keep the full three-line output as the default when `-l` isn't passed.

**Check:** `./main -l main.cpp` prints a single bare number with no labels, matching exactly the number that appears after `lines:` when you run `./main main.cpp` (no `-l`) on the same file.

---

## Capstone project
{: #capstone }

Build a **C++ todo CLI** that exercises the whole week:

- `class Todo` with RAII-clean member data, stored in a `std::vector<Todo>` — Days 3–4.
- `std::unordered_map<int, size_t>` mapping todo IDs to their vector index for O(1) lookups by ID — Day 5.
- File persistence via `std::ifstream`/`std::ofstream`, with a custom exception type thrown on unreadable/corrupt store files, caught at the top level in `main` — Days 8–9.
- `std::optional<Todo>` returned from a `findById` lookup instead of a sentinel or pointer — Day 7.
- Commands (`add`, `list`, `done`, `remove`) dispatched from `argv`, split across `main.cpp` + a `todo_store.h`/`.cpp` pair — Days 9–10.

Document your exact C++20 compile command (`g++ -std=c++20 ...`) in a short `README.md` alongside the code — a project that only builds if you remember an unwritten flag isn't done yet.

**Acceptance check:** running `add`, `add`, `done 0`, `remove 1`, `list` in sequence against a fresh store shows exactly one todo, marked done, at ID `0`; pointing the store loader at a corrupted file (`printf "not json" > todos.dat`) triggers your custom exception, caught cleanly at the top of `main` with a readable message — no raw `std::terminate` crash.

## Related

- [Rust in 10 Days](/courses/rust-10-days/)
- [Zig in 7 Days](/courses/zig-7-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
