---
layout: page
title: C++ STL vector for Competitive Programming
permalink: /cpp-stl/vector/
---

# C++ STL `vector` for Competitive Programming

**Hub:** [C++ STL Home](/cpp-stl/) · **Next:** [Iterators](/cpp-stl/iterators/)

`vector` is a **dynamic array**. In contests it replaces raw arrays for almost everything: lists of numbers, adjacency lists for graphs, DP tables, and temporary buffers.

---

## 1. Include & Declare

```cpp
#include <vector>
using namespace std;

vector<int> a;                 // empty
vector<int> b(n);              // n zeros
vector<int> c(n, -1);          // n copies of -1
vector<int> d = {3, 1, 4};     // initializer list
vector<long long> e(n);        // use long long often in CP
```

**2D vector (matrix / grid / adj list):**

```cpp
vector<vector<int>> g(n);           // n empty rows (graph adj)
vector<vector<int>> mat(n, vector<int>(m, 0));  // n x m zeros
```

---

## 2. Size, Capacity, Empty

```cpp
a.size();      // number of elements (size_t)
a.empty();     // true if size == 0
a.clear();     // size becomes 0 (capacity may remain)
a.resize(k);   // change size; new elems = 0 (for int)
a.resize(k, x);// new elems = x
a.reserve(k);  // pre-allocate capacity (avoids realloc in loops)
```

**Contest tip:** If you know final size ≈ `n`, do `a.reserve(n)` or construct `vector<int> a(n)` then fill by index.

---

## 3. Access Elements

```cpp
a[i];        // no bounds check (fast) — use in contests
a.at(i);     // throws if out of range (slower; rarely used in CP)
a.front();   // a[0]
a.back();    // last element
a.data();    // pointer to underlying array (rare)
```

**Never** write `a[a.size()]` — that is out of bounds. Last index is `a.size() - 1`.

---

## 4. Add / Remove

```cpp
a.push_back(x);     // add at end — amortized O(1)
a.emplace_back(x);  // construct in place (often same as push for ints)
a.pop_back();       // remove last — O(1)
a.insert(a.begin() + i, x);   // insert at i — O(n)
a.erase(a.begin() + i);       // erase at i — O(n)
a.erase(a.begin() + L, a.begin() + R); // erase [L, R)
```

**Prefer `push_back` / index assignment over middle `insert`/`erase` in hot loops.**

---

## 5. Iterate

```cpp
for (int i = 0; i < (int)a.size(); i++) {
    cout << a[i] << " ";
}

for (int x : a) {          // range-for (copy)
    cout << x << " ";
}

for (int &x : a) {         // modify in place
    x *= 2;
}

for (auto it = a.begin(); it != a.end(); ++it) {
    cout << *it << " ";
}
```

Cast `a.size()` to `int` when comparing with `int i` to avoid unsigned bugs:

```cpp
for (int i = 0; i < (int)a.size(); i++) { ... }
```

---

## 6. Sort, Reverse, Unique

```cpp
#include <algorithm>

sort(a.begin(), a.end());                  // ascending
sort(a.begin(), a.end(), greater<int>());  // descending
reverse(a.begin(), a.end());

// remove duplicates (must sort first)
sort(a.begin(), a.end());
a.erase(unique(a.begin(), a.end()), a.end());
```

**Custom comparator (pair by second, then first):**

```cpp
vector<pair<int,int>> v = {{1,5},{2,3},{1,2}};
sort(v.begin(), v.end(), [](auto &p, auto &q){
    if (p.second != q.second) return p.second < q.second;
    return p.first < q.first;
});
```

---

## 7. Binary Search on a Sorted Vector

```cpp
sort(a.begin(), a.end());

bool ok = binary_search(a.begin(), a.end(), x);

// first index with value >= x
auto it = lower_bound(a.begin(), a.end(), x);
int idx = it - a.begin();   // n if not found / all smaller

// first index with value > x
auto it2 = upper_bound(a.begin(), a.end(), x);
```

**Count of `x`:**

```cpp
int cnt = upper_bound(a.begin(), a.end(), x) - lower_bound(a.begin(), a.end(), x);
```

More on this: [Algorithms](/cpp-stl/algorithms/)

---

## 8. Common CP Patterns

### Frequency with value compression

```cpp
vector<int> a = /* input */;
vector<int> b = a;
sort(b.begin(), b.end());
b.erase(unique(b.begin(), b.end()), b.end());
for (int &x : a) {
    x = lower_bound(b.begin(), b.end(), x) - b.begin(); // 0..k-1
}
```

### Prefix sums

```cpp
vector<long long> pref(n + 1, 0);
for (int i = 0; i < n; i++) pref[i + 1] = pref[i] + a[i];
// sum of [L, R] inclusive:
long long sum = pref[R + 1] - pref[L];
```

### Graph adjacency list

```cpp
int n, m;
cin >> n >> m;
vector<vector<int>> g(n);
for (int i = 0; i < m; i++) {
    int u, v;
    cin >> u >> v;
    --u; --v;              // if input is 1-indexed
    g[u].push_back(v);
    g[v].push_back(u);     // undirected
}
```

### Read `n` integers

```cpp
int n;
cin >> n;
vector<int> a(n);
for (int i = 0; i < n; i++) cin >> a[i];
```

---

## 9. Time Complexity Cheat Card

| Operation | Complexity |
|---|---|
| `a[i]`, `front`, `back` | O(1) |
| `push_back` / `pop_back` | amortized O(1) / O(1) |
| `insert` / `erase` middle | O(n) |
| `sort` | O(n log n) |
| `lower_bound` on sorted | O(log n) |

---

## 10. Mini Practice Tasks

1. Read `n` numbers, print them sorted unique.  
2. Build prefix sums; answer `q` range-sum queries.  
3. Store an undirected graph; print degrees of all nodes.  
4. Given sorted `a`, count occurrences of `x` with `lower_bound`/`upper_bound`.

---

**Prev:** [STL Hub](/cpp-stl/) · **Next:** [Iterators](/cpp-stl/iterators/)
