---
layout: page
title: C++ STL map and unordered_map for Competitive Programming
permalink: /cpp-stl/map/
---

# C++ STL `map` & `unordered_map` for Competitive Programming

**Hub:** [C++ STL Home](/cpp-stl/) · **Prev:** [Iterators](/cpp-stl/iterators/) · **Next:** [set](/cpp-stl/set/)

Use maps when you need **key → value** association: frequencies, memoization, coordinate labels, graph compressions.

| | `map` | `unordered_map` |
|---|---|---|
| Order | Sorted by key | No order |
| Find / insert / erase | O(log n) | avg O(1), worst O(n) |
| Implementation | Balanced BST (usually RB-tree) | Hash table |
| When to use | Need order / `lower_bound` | Pure frequency / existence |
| Custom keys | Needs `operator<` | Needs hash + equality |

---

## 1. `map` Basics

```cpp
#include <map>
using namespace std;

map<string, int> mp;
mp["apple"] = 3;
mp["banana"] = 5;

cout << mp["apple"] << "\n";     // 3
cout << mp["cherry"] << "\n";    // inserts cherry→0, prints 0  ← careful!
```

**Safe read without insert:**

```cpp
if (mp.count("cherry")) { ... }           // 0 or 1 for map
if (mp.find("cherry") != mp.end()) { ... }

// C++20: mp.contains("cherry")
```

Prefer `find`/`count` when you must not create keys accidentally.

---

## 2. Insert, Erase, Iterate

```cpp
mp.insert({1, 10});
mp.emplace(2, 20);
mp.erase(1);                 // erase by key
auto it = mp.find(2);
if (it != mp.end()) mp.erase(it);

for (auto &[k, v] : mp) {    // structured bindings (C++17)
    cout << k << " " << v << "\n";
}

// older style
for (auto it = mp.begin(); it != mp.end(); ++it) {
    cout << it->first << " " << it->second << "\n";
}
```

Iteration is **ascending by key**.

---

## 3. Frequency Counting (Classic)

```cpp
vector<int> a = {1, 2, 1, 3, 2, 1};
map<int, int> freq;
for (int x : a) freq[x]++;

for (auto [x, c] : freq) cout << x << " appears " << c << "\n";
```

Faster when order not needed:

```cpp
unordered_map<int, int> freq;
for (int x : a) freq[x]++;
```

---

## 4. Ordered Queries on `map`

```cpp
map<int, int> mp = {{1,10},{3,30},{5,50},{7,70}};

auto it = mp.lower_bound(4);  // first key >= 4 → 5
auto it2 = mp.upper_bound(5); // first key > 5 → 7

// largest key <= x
auto it3 = mp.upper_bound(x);
if (it3 == mp.begin()) { /* none */ }
else {
    --it3;  // now key <= x
}
```

Same idea works on `set`.

---

## 5. `unordered_map`

```cpp
#include <unordered_map>

unordered_map<int, int> um;
um.reserve(n * 2);   // optional: reduce rehashing
um.max_load_factor(0.7);

um[42] = 1;
if (um.find(42) != um.end()) { ... }
```

**Custom hash for `pair` (common need):**

```cpp
struct PairHash {
    size_t operator()(const pair<int,int>& p) const noexcept {
        return (size_t)p.first * 1000003u + (size_t)p.second;
    }
};

unordered_map<pair<int,int>, int, PairHash> um;
```

For contests, many people use `map<pair<int,int>,int>` if `n` is small enough (O(log n) is fine).

---

## 6. `map` vs Array / Vector

If keys are `1..n` or dense `0..n-1`, use `vector`, not map:

```cpp
vector<int> freq(n + 1, 0);
freq[x]++;   // O(1)
```

Use map when keys are sparse / huge / strings.

---

## 7. CP Patterns

### Memoization (DP with map)

```cpp
map<pair<int,int>, long long> memo;
long long dp(int i, int j) {
    if (...) return base;
    auto key = make_pair(i, j);
    if (memo.count(key)) return memo[key];
    return memo[key] = /* compute */;
}
```

### Coordinate compression helper

Often better with `vector` + sort + unique + `lower_bound` ([vector article](/cpp-stl/vector/)). Use `map` only if convenient:

```cpp
map<int, int> comp;
vector<int> vals = /* all coordinates */;
sort(vals.begin(), vals.end());
vals.erase(unique(vals.begin(), vals.end()), vals.end());
for (int i = 0; i < (int)vals.size(); i++) comp[vals[i]] = i;
```

### Grouping anagrams / strings

```cpp
map<string, vector<string>> groups;
for (auto &s : words) {
    string key = s;
    sort(key.begin(), key.end());
    groups[key].push_back(s);
}
```

---

## 8. Multimap

```cpp
#include <map>
multimap<int, int> mm;  // duplicate keys allowed
mm.insert({1, 10});
mm.insert({1, 20});
auto r = mm.equal_range(1); // all values with key 1
```

Rare in CP compared to `map<int, vector<int>>`.

---

## 9. Complexity & Pitfalls

| Pitfall | Fix |
|---|---|
| `mp[x]` creates 0 | Use `find` / `count` for checks |
| `unordered_map` TLE / hack | Use `map`, or better hash, or `vector` |
| Iterating huge map each query | Wrong structure — rethink |
| Using map for `1..n` keys | Use `vector` |

---

## 10. Mini Practice

1. Count character frequencies in a string with `map<char,int>`.  
2. Read `n` pairs `(k,v)`; print keys in sorted order with sums of values.  
3. Implement “largest key ≤ x” with `upper_bound` + decrement.  
4. Rewrite a frequency problem with both `map` and `unordered_map`; compare.

---

**Prev:** [Iterators](/cpp-stl/iterators/) · **Next:** [set & multiset](/cpp-stl/set/) · [Hub](/cpp-stl/)
