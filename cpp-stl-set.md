---
layout: page
title: C++ STL set, multiset and unordered_set for Competitive Programming
permalink: /cpp-stl/set/
---

# C++ STL `set`, `multiset` & `unordered_set` for Competitive Programming

**Hub:** [C++ STL Home](/cpp-stl/) · **Prev:** [map](/cpp-stl/map/) · **Next:** [stack / queue](/cpp-stl/stack-queue/)

Sets store **keys only** (no separate value). Use them for unique elements, ordered queries, and sliding “currently active” values.

| Container | Duplicates | Ordered | Typical use |
|---|---|---|---|
| `set` | No | Yes | unique + order |
| `multiset` | Yes | Yes | keep duplicates sorted |
| `unordered_set` | No | No | existence checks |

---

## 1. `set` Basics

```cpp
#include <set>
using namespace std;

set<int> s;
s.insert(3);
s.insert(1);
s.insert(3);          // ignored
s.emplace(2);

cout << s.size() << "\n";          // 3 → {1,2,3}
cout << *s.begin() << "\n";        // minimum
cout << *s.rbegin() << "\n";       // maximum

s.erase(2);                        // erase by value
auto it = s.find(1);
if (it != s.end()) s.erase(it);
```

```cpp
if (s.count(x)) { ... }            // 0 or 1
if (s.find(x) != s.end()) { ... }
```

---

## 2. Ordered Queries

```cpp
set<int> s = {1, 3, 5, 7, 9};

auto it = s.lower_bound(4);   // >= 4 → 5
auto it2 = s.upper_bound(5);  // > 5 → 7

// predecessor of x (largest < x) — or <= with lower_bound tricks
auto it3 = s.lower_bound(x);
if (it3 == s.begin()) { /* no smaller */ }
else {
    --it3;  // now < x if x not present; <= if present and we used upper_bound
}
```

**Largest ≤ x:**

```cpp
auto it = s.upper_bound(x);
if (it == s.begin()) { /* none */ }
else {
    --it; // *it <= x
}
```

---

## 3. Iterate

```cpp
for (int x : s) cout << x << " ";

for (auto it = s.begin(); it != s.end(); ++it) {
    cout << *it << " ";
}
```

Erase while iterating:

```cpp
for (auto it = s.begin(); it != s.end(); ) {
    if (*it % 2 == 0) it = s.erase(it);
    else ++it;
}
```

---

## 4. `multiset` (Duplicates Allowed)

```cpp
#include <set>
multiset<int> ms;
ms.insert(5);
ms.insert(5);
ms.insert(2);   // {2,5,5}

cout << ms.count(5) << "\n";  // 2 — O(k + log n) to count all
```

### Critical: `erase(value)` vs `erase(iterator)`

```cpp
ms.erase(5);           // erases ALL 5s — often a bug in CP
ms.erase(ms.find(5));  // erases ONE 5 — what you usually want
```

---

## 5. `unordered_set`

```cpp
#include <unordered_set>
unordered_set<int> us;
us.insert(10);
if (us.count(10)) { ... }
us.erase(10);
```

Great for “have I seen this?” in O(1) average.

```cpp
unordered_set<int> seen;
for (int x : a) {
    if (seen.count(x)) { /* duplicate */ }
    seen.insert(x);
}
```

---

## 6. Custom Comparator

```cpp
struct Cmp {
    bool operator()(const pair<int,int>& a, const pair<int,int>& b) const {
        if (a.first != b.first) return a.first > b.first; // desc by first
        return a.second < b.second;
    }
};

set<pair<int,int>, Cmp> s;
```

Or with `greater`:

```cpp
set<int, greater<int>> s;  // descending order
```

---

## 7. CP Patterns

### Maintain current window extremes

```cpp
multiset<int> window;
// add x
window.insert(x);
// remove one x
window.erase(window.find(x));
// min / max
int mn = *window.begin();
int mx = *window.rbegin();
```

### Mex (minimum excluded non-negative)

Often use `set` of missing numbers, or boolean array if `n` small.

```cpp
set<int> missing;
for (int i = 0; i <= n + 1; i++) missing.insert(i);
// when value v appears:
if (missing.count(v)) missing.erase(v);
int mex = *missing.begin();
```

### Unique elements from stream

```cpp
set<int> s(a.begin(), a.end());
vector<int> uniq(s.begin(), s.end()); // sorted unique
```

(Usually `sort` + `unique` on `vector` is faster.)

---

## 8. Complexity

| Op | `set` / `multiset` | `unordered_set` |
|---|---|---|
| insert / erase / find | O(log n) | avg O(1) |
| min / max | O(1) via begin/rbegin | N/A (scan) |
| lower_bound | O(log n) | N/A |

---

## 9. Mini Practice

1. Insert `n` numbers into a `set`; print min and max after each insert.  
2. Use `multiset` for a sliding window of size `k`; print min each step.  
3. Find predecessor of `x` safely.  
4. Demonstrate the `multiset.erase(value)` bug and fix it.

---

**Prev:** [map](/cpp-stl/map/) · **Next:** [stack, queue, deque, priority_queue](/cpp-stl/stack-queue/) · [Hub](/cpp-stl/)
