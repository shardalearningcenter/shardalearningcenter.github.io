---
layout: page
title: C++ STL Algorithms for Competitive Programming
permalink: /cpp-stl/algorithms/
---

# C++ STL `<algorithm>` & `<numeric>` for Competitive Programming

**Hub:** [C++ STL Home](/cpp-stl/) · **Prev:** [stack / queue](/cpp-stl/stack-queue/) · **Next:** [string / pair](/cpp-stl/string-pair/)

Most contest code is: **put data in a `vector` → call algorithms**.

```cpp
#include <algorithm>
#include <numeric>
```

All ranges are **half-open**: `[first, last)`.

---

## 1. Sorting

```cpp
vector<int> a = {5, 1, 4, 2};

sort(a.begin(), a.end());                    // ascending
sort(a.begin(), a.end(), greater<int>());    // descending
stable_sort(a.begin(), a.end());             // keeps equal-element order

// custom
sort(a.begin(), a.end(), [](int x, int y){
    return x > y; // descending
});
```

**Sort pairs:**

```cpp
vector<pair<int,int>> v;
sort(v.begin(), v.end()); // first asc, then second asc
```

**Partial sort / nth element:**

```cpp
nth_element(a.begin(), a.begin() + k, a.end());
// a[k] is the element that would be at k after full sort
// left side <= a[k], right side >= a[k] (not fully sorted)
```

---

## 2. Binary Search Family

**Requires sorted ascending range** (or custom comp consistency).

```cpp
sort(a.begin(), a.end());

bool exists = binary_search(a.begin(), a.end(), x);

auto lo = lower_bound(a.begin(), a.end(), x); // first >= x
auto hi = upper_bound(a.begin(), a.end(), x); // first > x
int idx = lo - a.begin();
int count_x = hi - lo;
```

### Binary search on answer (pattern)

```cpp
long long lo = 0, hi = 1e18, ans = -1;
while (lo <= hi) {
    long long mid = lo + (hi - lo) / 2;
    if (check(mid)) { ans = mid; hi = mid - 1; } // minimize
    else lo = mid + 1;
}
```

---

## 3. Min / Max / Minmax

```cpp
int mn = *min_element(a.begin(), a.end());
int mx = *max_element(a.begin(), a.end());
int i_mn = min_element(a.begin(), a.end()) - a.begin();

cout << min(x, y) << " " << max(x, y) << "\n";
cout << min({a, b, c}) << "\n";
```

---

## 4. Fill, Assign, Swap, Reverse, Rotate

```cpp
fill(a.begin(), a.end(), 0);
fill(a.begin(), a.begin() + k, -1);

reverse(a.begin(), a.end());
rotate(a.begin(), a.begin() + k, a.end()); // left rotate by k

swap(a[i], a[j]);
swap(a, b); // swap whole containers
```

2D fill:

```cpp
vector<vector<int>> dp(n, vector<int>(m, INF));
```

---

## 5. Unique, Remove, Count, Find

```cpp
sort(a.begin(), a.end());
a.erase(unique(a.begin(), a.end()), a.end()); // sorted unique

int c = count(a.begin(), a.end(), x);
auto it = find(a.begin(), a.end(), x);
bool ok = (it != a.end());

// remove-erase idiom (unordered remove of value)
a.erase(remove(a.begin(), a.end(), x), a.end());
```

---

## 6. Permutations

```cpp
vector<int> p = {1, 2, 3};
sort(p.begin(), p.end());
do {
    // use p
} while (next_permutation(p.begin(), p.end()));
```

Generates all ascending permutations — `n!` must be tiny (`n ≤ 10` usually).

---

## 7. Merge / Set Operations on Sorted Ranges

```cpp
vector<int> a, b, c;
sort(a.begin(), a.end());
sort(b.begin(), b.end());

c.resize(a.size() + b.size());
auto it = set_intersection(a.begin(), a.end(), b.begin(), b.end(), c.begin());
c.resize(it - c.begin());

// also: set_union, set_difference, set_symmetric_difference, merge
```

---

## 8. `<numeric>` Gems

```cpp
#include <numeric>

long long sum = accumulate(a.begin(), a.end(), 0LL); // use 0LL !!
long long prod = accumulate(a.begin(), a.end(), 1LL, multiplies<long long>());

vector<long long> pref(n);
partial_sum(a.begin(), a.end(), pref.begin());

iota(a.begin(), a.end(), 0); // fill 0,1,2,...,n-1
```

**GCD / LCM (C++17):**

```cpp
#include <numeric>
int g = gcd(a, b);
long long l = lcm((long long)a, (long long)b); // watch overflow
```

---

## 9. `all_of` / `any_of` / `none_of`

```cpp
bool allPos = all_of(a.begin(), a.end(), [](int x){ return x > 0; });
bool anyNeg = any_of(a.begin(), a.end(), [](int x){ return x < 0; });
```

---

## 10. Must-Know Complexities

| Algorithm | Complexity |
|---|---|
| `sort` / `stable_sort` | O(n log n) |
| `lower_bound` / `upper_bound` / `binary_search` | O(log n) |
| `nth_element` | avg O(n) |
| `next_permutation` (one call) | O(n) |
| `accumulate` / `count` / `find` / `reverse` | O(n) |

---

## 11. Mini Practice

1. Sort + unique a vector of integers.  
2. Count occurrences of `x` with `lower_bound`/`upper_bound`.  
3. Use `nth_element` to find median.  
4. Generate all permutations of `{1,2,3,4}`.  
5. Prefix sums with `partial_sum` and answer range sums.

---

**Prev:** [stack / queue](/cpp-stl/stack-queue/) · **Next:** [string, pair, tuple](/cpp-stl/string-pair/) · [Hub](/cpp-stl/)
