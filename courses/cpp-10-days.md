---
layout: course
title: "C++ in 10 Days — Hands-On"
permalink: /courses/cpp-10-days/
course_track: "C++"
description: "Modern C++17/20 essentials: RAII, STL, and a small CLI — without the legacy maze."
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

Modern C++17/20 essentials: RAII, STL, and a small CLI — without the legacy maze.

## Why this language
{: #why-this-language }

C++ still owns games, HFT-adjacent systems, browsers, and embedded. Learn modern C++, not 1998 C++.

## Setup (Day 0)
{: #setup-day-0 }

```bash
g++ --version   # or clang++
mkdir cpp-lab && cd cpp-lab
```
Compile: `g++ -std=c++20 -O2 main.cpp -o main && ./main`

---

## Day 1: Hello & build
{: #day-1-hello-build }

### What you'll learn

- main
- iostream
- compile flags

### Code along

```cpp
#include <iostream>
int main() {
  std::cout << "Hello C++\n";
}
```

### Your task

Print argv.

---

## Day 2: Types & references
{: #day-2-types-references }

### What you'll learn

- auto
- refs
- const

### Code along

```cpp
void add1(int& x) { x += 1; }
int main() { int n = 1; add1(n); std::cout << n; }
```

### Your task

Swap two ints via references.

---

## Day 3: Classes & RAII
{: #day-3-classes-raii }

### What you'll learn

- ctor/dtor
- rule of zero
- private

### Code along

```cpp
class Counter {
  int n_ = 0;
public:
  void tick() { ++n_; }
  int get() const { return n_; }
};
```

### Your task

BankAccount class with deposit/withdraw.

---

## Day 4: STL vectors & algorithms
{: #day-4-stl-vectors-algorithms }

### What you'll learn

- vector
- range-for
- sort

### Code along

```cpp
#include <vector>
#include <algorithm>
std::vector<int> v{3,1,2};
std::sort(v.begin(), v.end());
```

### Your task

Remove duplicates from a sorted vector.

---

## Day 5: Maps & unordered_map
{: #day-5-maps-unordered_map }

### What you'll learn

- map
- count words
- structured bindings

### Code along

```cpp
#include <unordered_map>
#include <string>
std::unordered_map<std::string,int> m;
m["a"]++;
```

### Your task

Word count over stdin lines.

---

## Day 6: Smart pointers
{: #day-6-smart-pointers }

### What you'll learn

- unique_ptr
- shared_ptr
- make_unique

### Code along

```cpp
#include <memory>
auto p = std::make_unique<int>(42);
std::cout << *p;
```

### Your task

Factory returning unique_ptr to a Shape hierarchy.

---

## Day 7: Optional & variants lite
{: #day-7-optional-variants-lite }

### What you'll learn

- optional
- nullopt
- value_or

### Code along

```cpp
#include <optional>
std::optional<int> parse(const std::string& s) {
  try { return std::stoi(s); } catch (...) { return std::nullopt; }
}
```

### Your task

Parse many args; skip bad ones.

---

## Day 8: Exceptions
{: #day-8-exceptions }

### What you'll learn

- try/catch
- what()
- RAII + exceptions

### Code along

```cpp
try { throw std::runtime_error("boom"); }
catch (const std::exception& e) { std::cerr << e.what(); }
```

### Your task

File open wrapper that throws on failure.

---

## Day 9: Headers & multi-file
{: #day-9-headers-multi-file }

### What you'll learn

- header guards / #pragma once
- cpp files
- link

### Code along

```cpp
// add.h
#pragma once
int add(int a, int b);
// add.cpp
int add(int a, int b) { return a + b; }
```

### Your task

Split a project into main.cpp + util.h/cpp; compile both.

---

## Day 10: CLI tool
{: #day-10-cli-tool }

### What you'll learn

- fstream
- stringstream
- exit codes

### Code along

```cpp
#include <fstream>
#include <string>
int main(int argc, char** argv) {
  if (argc < 2) return 1;
  std::ifstream in(argv[1]);
  std::string line; int n = 0;
  while (std::getline(in, line)) ++n;
  std::cout << n << "\n";
}
```

### Your task

Add word and char counts.


---

## Capstone project
{: #capstone }

Build a **C++ todo CLI** using vector + file persistence, with a clean class boundary and C++20 compile flags documented in README.

## Related

- [Rust in 10 Days](/courses/rust-10-days/)
- [Zig in 7 Days](/courses/zig-7-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
