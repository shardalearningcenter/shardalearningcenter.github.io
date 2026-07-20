---
layout: page
title: C++ STL stack, queue, deque, priority_queue for Competitive Programming
permalink: /cpp-stl/stack-queue/
---

# C++ STL `stack`, `queue`, `deque`, `priority_queue` for Competitive Programming

**Hub:** [C++ STL Home](/cpp-stl/) · **Prev:** [set](/cpp-stl/set/) · **Next:** [Algorithms](/cpp-stl/algorithms/)

These are the workhorses for BFS, DFS (iterative), monotonic stacks/deques, and Dijkstra / Top-K.

---

## 1. `stack` (LIFO)

```cpp
#include <stack>
stack<int> st;
st.push(1);
st.push(2);
cout << st.top() << "\n";  // 2
st.pop();                  // removes 2
cout << st.size() << " " << st.empty() << "\n";
```

**No iterators.** Only `top`, `push`, `pop`, `size`, `empty`.

### Pattern: Next Greater Element

```cpp
vector<int> nextGreater(vector<int>& a) {
    int n = a.size();
    vector<int> ans(n, -1);
    stack<int> st; // indices
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.top()] < a[i]) {
            ans[st.top()] = a[i];
            st.pop();
        }
        st.push(i);
    }
    return ans;
}
```

### Iterative DFS

```cpp
stack<int> st;
vector<int> vis(n, 0);
st.push(start);
while (!st.empty()) {
    int u = st.top(); st.pop();
    if (vis[u]) continue;
    vis[u] = 1;
    for (int v : g[u]) if (!vis[v]) st.push(v);
}
```

---

## 2. `queue` (FIFO)

```cpp
#include <queue>
queue<int> q;
q.push(1);
q.push(2);
cout << q.front() << "\n"; // 1
cout << q.back() << "\n";  // 2
q.pop();
```

### BFS Template

```cpp
vector<int> dist(n, -1);
queue<int> q;
dist[src] = 0;
q.push(src);
while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int v : g[u]) if (dist[v] == -1) {
        dist[v] = dist[u] + 1;
        q.push(v);
    }
}
```

---

## 3. `deque` (Double-Ended Queue)

```cpp
#include <deque>
deque<int> dq;
dq.push_back(1);
dq.push_front(0);
dq.pop_back();
dq.pop_front();
cout << dq.front() << " " << dq.back() << "\n";
dq[i];   // random access — yes!
```

Also usable like a vector (iterators, sort), but `vector` is usually preferred for pure arrays.

### Sliding Window Maximum (monotonic deque)

```cpp
vector<int> maxSlidingWindow(vector<int>& a, int k) {
    deque<int> dq; // indices, decreasing values
    vector<int> ans;
    for (int i = 0; i < (int)a.size(); i++) {
        while (!dq.empty() && dq.front() <= i - k) dq.pop_front();
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1) ans.push_back(a[dq.front()]);
    }
    return ans;
}
```

### 0-1 BFS

```cpp
deque<int> dq;
vector<int> dist(n, 1e9);
dist[src] = 0;
dq.push_front(src);
while (!dq.empty()) {
    int u = dq.front(); dq.pop_front();
    for (auto [v, w] : g[u]) { // w is 0 or 1
        if (dist[v] > dist[u] + w) {
            dist[v] = dist[u] + w;
            if (w == 0) dq.push_front(v);
            else dq.push_back(v);
        }
    }
}
```

---

## 4. `priority_queue` (Heap)

Default = **max-heap**.

```cpp
#include <queue>
priority_queue<int> pq;
pq.push(3);
pq.push(5);
pq.push(1);
cout << pq.top() << "\n"; // 5
pq.pop();
```

### Min-heap

```cpp
priority_queue<int, vector<int>, greater<int>> minpq;
minpq.push(3);
minpq.push(1);
cout << minpq.top() << "\n"; // 1
```

### Pairs (Dijkstra distances)

```cpp
// max-heap by first: pair<dist, node> with negative dist OR use greater
using Node = pair<long long, int>; // dist, vertex
priority_queue<Node, vector<Node>, greater<Node>> pq;
pq.push({0, src});
```

### Top-K elements

```cpp
priority_queue<int, vector<int>, greater<int>> pq; // min-heap size k
for (int x : a) {
    pq.push(x);
    if ((int)pq.size() > k) pq.pop();
}
// pq contains k largest; top is the k-th largest
```

---

## 5. Custom Comparator for Heap

```cpp
struct Cmp {
    bool operator()(const pair<int,int>& a, const pair<int,int>& b) const {
        return a.second > b.second; // min-heap by second
    }
};
priority_queue<pair<int,int>, vector<pair<int,int>>, Cmp> pq;
```

Remember: `priority_queue` comparator is like `sort` but inverted intuition — think “returns true if a has **lower priority** than b”.

---

## 6. Quick Choice Guide

| Need | Use |
|---|---|
| BFS | `queue` |
| DFS iterative / parentheses / NGE | `stack` |
| Insert/delete both ends / 0-1 BFS / sliding window | `deque` |
| Always need min or max quickly | `priority_queue` |
| Need delete arbitrary + min | `multiset` (not heap) |

---

## 7. Complexity

| Structure | Push | Pop | Peek |
|---|---|---|---|
| stack / queue / deque ends | O(1) | O(1) | O(1) |
| priority_queue | O(log n) | O(log n) | O(1) |

---

## 8. Mini Practice

1. BFS distances on an unweighted graph.  
2. Next greater element with a stack.  
3. Sliding window maximum with deque.  
4. Dijkstra with `priority_queue<pair<ll,int>, ..., greater<...>>`.  
5. Find k-th largest using a size-`k` min-heap.

---

**Prev:** [set](/cpp-stl/set/) · **Next:** [Algorithms](/cpp-stl/algorithms/) · [Hub](/cpp-stl/)
