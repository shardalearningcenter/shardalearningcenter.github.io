---
layout: page
title: C++ STL Iterators for Competitive Programming
permalink: /cpp-stl/iterators/
---

# C++ STL Iterators for Competitive Programming

**Hub:** [C++ STL Home](/cpp-stl/) · **Prev:** [vector](/cpp-stl/vector/) · **Next:** [map](/cpp-stl/map/)

Iterators are **pointers into a container**. Almost every STL algorithm takes a half-open range `[begin, end)`.

```text
[ begin , end )
   ↑        ↑
 first    one-past-last
```

---

## 1. Basic Usage

```cpp
vector<int> a = {10, 20, 30, 40};

auto it = a.begin();   // points to 10
cout << *it << "\n";   // 10
++it;                  // now 20
it = a.end();          // past-the-end — do NOT dereference
```

```cpp
a.begin();   // first element
a.end();     // one past last
a.rbegin();  // reverse: last element
a.rend();    // reverse past-the-end
a.cbegin();  // const begin
a.cend();
```

---

## 2. Iterator → Index

On **random-access** containers (`vector`, `deque`, string):

```cpp
int idx = it - a.begin();
// or
int idx = (int)distance(a.begin(), it);
```

On `map`/`set`, `distance` is **O(n)** — prefer `lower_bound` style APIs instead of converting to index.

---

## 3. Loop Patterns

```cpp
for (auto it = a.begin(); it != a.end(); ++it) {
    cout << *it << " ";
}

// erase while iterating (vector)
for (auto it = a.begin(); it != a.end(); ) {
    if (*it % 2 == 0) it = a.erase(it);  // erase returns next
    else ++it;
}
```

**Wrong (undefined behavior):**

```cpp
a.erase(it);
++it;   // it is invalid after erase
```

---

## 4. Insert / Erase with Iterators

```cpp
vector<int> a = {1, 2, 4};
a.insert(a.begin() + 2, 3);           // {1,2,3,4}
a.erase(a.begin() + 1);               // {1,3,4}
a.erase(a.begin(), a.begin() + 2);    // erase prefix
```

**`map` / `set`:**

```cpp
map<int,int> mp = {{1,10},{2,20},{3,30}};
auto it = mp.find(2);
if (it != mp.end()) mp.erase(it);     // O(log n), safe
```

---

## 5. `next` / `prev` (C++11)

```cpp
#include <iterator>

auto it = a.begin();
auto it2 = next(it);      // it+1 without changing it
auto it3 = next(it, 2);   // it+2
auto it4 = prev(a.end()); // last element
```

Useful for `set`/`map` where `it + 1` is **not** allowed:

```cpp
set<int> s = {1, 3, 5, 7};
auto it = s.lower_bound(4); // 5
if (it != s.begin()) {
    auto pit = prev(it);    // 3
}
```

---

## 6. Reverse Iterators

```cpp
vector<int> a = {1, 2, 3, 4};
for (auto it = a.rbegin(); it != a.rend(); ++it) {
    cout << *it << " ";  // 4 3 2 1
}
```

Convert reverse → forward:

```cpp
auto rit = a.rbegin();
auto fit = rit.base(); // careful: base() points one past the reversed element
```

In CP, reverse with `reverse(a.begin(), a.end())` or loop indices is often clearer.

---

## 7. Iterator Categories (What Matters in Contests)

| Category | Examples | `it+k`? | Used for |
|---|---|---|---|
| Random access | `vector`, `deque`, `string` | Yes | binary search, indexing |
| Bidirectional | `list`, `set`, `map` | No (`++`/`--` only) | ordered trees |
| Forward | some others | `++` only | rare in CP |

**Rule:**  
`lower_bound(a.begin(), a.end(), x)` needs random access **or** you use the container member:

```cpp
auto it = s.lower_bound(x);   // set/map member — O(log n)
```

---

## 8. Algorithms Are Iterator-Based

```cpp
sort(a.begin(), a.end());
reverse(a.begin(), a.end());
fill(a.begin(), a.end(), 0);
min_element(a.begin(), a.end());
max_element(a.begin(), a.end());
accumulate(a.begin(), a.end(), 0LL);
```

Half-open ranges:

```cpp
// process indices [L, R] inclusive on vector:
sort(a.begin() + L, a.begin() + R + 1);
```

---

## 9. Invalidation Rules (Avoid WA / Runtime Error)

| Container | When iterators invalidate |
|---|---|
| `vector` | insert/erase at/before position; reallocation on `push_back` if capacity grows |
| `deque` | insert/erase in middle; ends safer for push/pop |
| `list` / `set` / `map` | only erased element(s); others stay valid |
| `unordered_*` | rehash may invalidate all |

**Safe pattern after `push_back` on vector:** do not keep old iterators/pointers across a growing `push_back` loop unless you `reserve` first.

```cpp
vector<int> a;
a.reserve(n);
for (int i = 0; i < n; i++) a.push_back(i);
```

---

## 10. Mini Practice

1. Erase all even numbers from a `vector` using the erase-return pattern.  
2. On a `set`, find predecessor of `x` with `lower_bound` + `prev`.  
3. Sort only the subarray `a[L..R]` using iterators.

---

**Prev:** [vector](/cpp-stl/vector/) · **Next:** [map & unordered_map](/cpp-stl/map/) · [Hub](/cpp-stl/)
