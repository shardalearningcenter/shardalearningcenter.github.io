---
layout: page
title: C++ STL for Competitive Programming
permalink: /cpp-stl/
---

<style>
.stl-wrap { max-width: 920px; margin: 0 auto; padding: 1rem; line-height: 1.65; }
.stl-wrap h1 { margin-bottom: 0.4rem; }
.stl-lead { color: #444; margin-bottom: 1.5rem; }
.stl-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0 2rem;
}
.stl-card {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 1rem 1.1rem;
  background: #fff;
  box-shadow: 2px 2px 8px rgba(0,0,0,0.04);
}
.stl-card a { font-weight: 700; font-size: 1.1rem; color: #0a66c2; text-decoration: none; }
.stl-card a:hover { text-decoration: underline; }
.stl-card p { margin: 0.45rem 0 0; color: #555; font-size: 0.95rem; }
.stl-table { width: 100%; border-collapse: collapse; margin: 1rem 0 2rem; }
.stl-table th, .stl-table td { border: 1px solid #ddd; padding: 0.55rem 0.7rem; text-align: left; }
.stl-table th { background: #f3f6fa; }
.stl-note { background: #f7fafc; border-left: 4px solid #0a66c2; padding: 0.8rem 1rem; margin: 1.2rem 0; }
</style>

<div class="stl-wrap">

# C++ STL for Competitive Programming

<p class="stl-lead">
One hub for the Standard Template Library topics you actually need in contests (Codeforces, AtCoder, LeetCode, CodeChef).
Start here — every article is linked below.
</p>

## All Articles (Sub Pages)

<div class="stl-grid">
  <div class="stl-card">
    <a href="/cpp-stl/vector/">1. vector</a>
    <p>Dynamic arrays, indexing, push/pop, resize, sort, 2D vectors — the #1 CP container.</p>
  </div>
  <div class="stl-card">
    <a href="/cpp-stl/iterators/">2. Iterators</a>
    <p>begin/end, next/prev, erase/insert safely, reverse iterators, iterator categories.</p>
  </div>
  <div class="stl-card">
    <a href="/cpp-stl/map/">3. map &amp; unordered_map</a>
    <p>Ordered trees vs hash maps, frequency counting, coordinate compression helpers.</p>
  </div>
  <div class="stl-card">
    <a href="/cpp-stl/set/">4. set, multiset &amp; unordered_set</a>
    <p>Unique values, ordered sets, lower_bound tricks, multiset erase pitfalls.</p>
  </div>
  <div class="stl-card">
    <a href="/cpp-stl/stack-queue/">5. stack, queue, deque, priority_queue</a>
    <p>BFS/DFS helpers, sliding window deque, heaps for Top-K and Dijkstra.</p>
  </div>
  <div class="stl-card">
    <a href="/cpp-stl/algorithms/">6. Algorithms (&lt;algorithm&gt;)</a>
    <p>sort, stable_sort, lower/upper_bound, binary_search, next_permutation, accumulate.</p>
  </div>
  <div class="stl-card">
    <a href="/cpp-stl/string-pair/">7. string, pair &amp; tuple</a>
    <p>String ops, substr, pair keys in maps, structured bindings, tie.</p>
  </div>
  <div class="stl-card">
    <a href="/cpp-stl/cp-cheatsheet/">8. CP Cheatsheet</a>
    <p>Fast I/O template, complexity table, must-know snippets in one page.</p>
  </div>
</div>

## Suggested Learning Order

1. [vector](/cpp-stl/vector/) → 2. [iterators](/cpp-stl/iterators/) → 3. [algorithms](/cpp-stl/algorithms/)  
4. [map](/cpp-stl/map/) → 5. [set](/cpp-stl/set/) → 6. [stack / queue / heap](/cpp-stl/stack-queue/)  
7. [string / pair](/cpp-stl/string-pair/) → 8. [cheatsheet](/cpp-stl/cp-cheatsheet/)

## Complexity at a Glance

<table class="stl-table">
  <thead>
    <tr><th>Container</th><th>Find</th><th>Insert</th><th>Erase</th><th>Ordered?</th></tr>
  </thead>
  <tbody>
    <tr><td><code>vector</code></td><td>O(n)</td><td>amortized O(1) back</td><td>O(n) middle</td><td>No (you sort)</td></tr>
    <tr><td><code>deque</code></td><td>O(n)</td><td>O(1) ends</td><td>O(n) middle</td><td>No</td></tr>
    <tr><td><code>list</code></td><td>O(n)</td><td>O(1) known pos</td><td>O(1) known pos</td><td>No</td></tr>
    <tr><td><code>set</code> / <code>map</code></td><td>O(log n)</td><td>O(log n)</td><td>O(log n)</td><td>Yes</td></tr>
    <tr><td><code>unordered_set</code> / <code>unordered_map</code></td><td>avg O(1)</td><td>avg O(1)</td><td>avg O(1)</td><td>No</td></tr>
    <tr><td><code>priority_queue</code></td><td>top O(1)</td><td>O(log n)</td><td>O(log n) pop</td><td>Heap order</td></tr>
  </tbody>
</table>

<div class="stl-note">
<strong>Contest tip:</strong> Prefer <code>vector</code> + sort + two pointers / binary search first.
Reach for <code>map</code>/<code>set</code> when you need dynamic ordered queries; use <code>unordered_*</code> for pure frequency / existence when order does not matter.
</div>

## Headers You Almost Always Need

```cpp
#include <bits/stdc++.h>
using namespace std;
```

Or the portable set:

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <unordered_map>
#include <set>
#include <unordered_set>
#include <queue>
#include <stack>
#include <deque>
#include <algorithm>
#include <numeric>
#include <utility>
```

## Related on This Site

- [C Getting Started — Hands On](/c-getting-started/)  
- [DSA Cheatsheet](/dsa-cheatsheet/)  
- [Courses](/courses/)  
- [Blog](/blog/)

---

*Practice each container with 5–10 small problems. Speed in contests comes from muscle memory, not memorizing every member function.*

</div>
