---
layout: page
title: C++ STL Competitive Programming Cheatsheet
permalink: /cpp-stl/cp-cheatsheet/
---

# C++ STL Competitive Programming Cheatsheet

**Hub:** [C++ STL Home](/cpp-stl/) · All detailed pages linked below.

Quick lookup for contests. For depth, open the article.

---

## Articles Index

1. [vector](/cpp-stl/vector/)  
2. [Iterators](/cpp-stl/iterators/)  
3. [map & unordered_map](/cpp-stl/map/)  
4. [set, multiset, unordered_set](/cpp-stl/set/)  
5. [stack, queue, deque, priority_queue](/cpp-stl/stack-queue/)  
6. [Algorithms](/cpp-stl/algorithms/)  
7. [string, pair, tuple](/cpp-stl/string-pair/)  
8. **This cheatsheet**

---

## Fast I/O Template

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T = 1;
    // cin >> T;
    while (T--) {
        // solve
    }
    return 0;
}
```

Portable includes if `bits/stdc++.h` unavailable:

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <deque>
#include <unordered_map>
#include <unordered_set>
#include <numeric>
#include <cmath>
```

---

## Complexity Table

| Container / Algo | Key cost |
|---|---|
| `vector` index / push_back | O(1) / amort. O(1) |
| `sort` | O(n log n) |
| `lower_bound` on vector | O(log n) |
| `set` / `map` ops | O(log n) |
| `unordered_*` ops | avg O(1) |
| `priority_queue` push/pop | O(log n) |
| BFS / DFS | O(n + m) |

---

## Snippets

### Read vector

```cpp
int n; cin >> n;
vector<int> a(n);
for (int i = 0; i < n; i++) cin >> a[i];
```

### Sort unique

```cpp
sort(a.begin(), a.end());
a.erase(unique(a.begin(), a.end()), a.end());
```

### Prefix sum

```cpp
vector<long long> pref(n + 1);
for (int i = 0; i < n; i++) pref[i + 1] = pref[i] + a[i];
```

### Frequency

```cpp
map<int,int> freq;
for (int x : a) freq[x]++;
```

### Graph

```cpp
vector<vector<int>> g(n);
g[u].push_back(v);
```

### BFS

```cpp
queue<int> q;
vector<int> dist(n, -1);
dist[s] = 0; q.push(s);
while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int v : g[u]) if (dist[v] < 0) {
        dist[v] = dist[u] + 1;
        q.push(v);
    }
}
```

### Min-heap Dijkstra

```cpp
using P = pair<long long,int>;
priority_queue<P, vector<P>, greater<P>> pq;
```

### Lower / upper bound count

```cpp
int cnt = upper_bound(a.begin(), a.end(), x) - lower_bound(a.begin(), a.end(), x);
```

### Multiset erase one

```cpp
ms.erase(ms.find(x)); // NOT ms.erase(x)
```

### Coordinate compression

```cpp
vector<int> b = a;
sort(b.begin(), b.end());
b.erase(unique(b.begin(), b.end()), b.end());
for (int &x : a) x = lower_bound(b.begin(), b.end(), x) - b.begin();
```

### Directions (grid)

```cpp
int dx[4] = {1, -1, 0, 0};
int dy[4] = {0, 0, 1, -1};
```

### Infinity

```cpp
const int INF = 1e9;
const long long LINF = 1e18;
```

---

## Choose the Right Tool

| Problem need | Tool |
|---|---|
| Dynamic array / adj list | `vector` |
| Sorted unique + predecessor | `set` |
| Key → value + order | `map` |
| Frequency only | `unordered_map` / array |
| BFS | `queue` |
| Sliding window max | `deque` |
| Top-K / Dijkstra | `priority_queue` |
| Sort + binary search | `vector` + `<algorithm>` |

---

## Debug Tips

```cpp
#ifdef LOCAL
#define dbg(x) cerr << #x << " = " << (x) << "\n"
#else
#define dbg(x)
#endif
```

Print vector:

```cpp
for (int x : a) cerr << x << " ";
cerr << "\n";
```

---

## Practice Checklist

- [ ] `vector` + sort + unique + lower_bound  
- [ ] prefix sums  
- [ ] graph BFS / DFS  
- [ ] `map` frequency  
- [ ] `set` predecessor / successor  
- [ ] monotonic stack / deque  
- [ ] `priority_queue` min-heap  
- [ ] `next_permutation` on small n  
- [ ] string `substr` / `find`  

---

**Back to hub:** [C++ STL for Competitive Programming](/cpp-stl/)
