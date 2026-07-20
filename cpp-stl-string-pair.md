---
layout: page
title: C++ STL string, pair and tuple for Competitive Programming
permalink: /cpp-stl/string-pair/
---

# C++ STL `string`, `pair` & `tuple` for Competitive Programming

**Hub:** [C++ STL Home](/cpp-stl/) · **Prev:** [Algorithms](/cpp-stl/algorithms/) · **Next:** [CP Cheatsheet](/cpp-stl/cp-cheatsheet/)

---

## 1. `string` Basics

```cpp
#include <string>
using namespace std;

string s = "abcd";
s.size(); s.length();
s.empty();
s[i];                 // char
s.front(); s.back();
s += 'e';             // append char
s += "fg";            // append string
s.push_back('h');
s.pop_back();
```

### Substring & search

```cpp
string t = s.substr(1, 2);      // from idx 1, length 2 → "bc"
string u = s.substr(2);         // from idx 2 to end

auto pos = s.find("bc");        // size_t; npos if missing
if (pos != string::npos) { ... }

s.find('a');
s.rfind('a');                   // last occurrence
```

### Compare & modify

```cpp
s == t;
s < t;                          // lexicographical
s.compare(t);

s.insert(2, "XY");
s.erase(2, 3);                  // idx, length
s.replace(1, 2, "ZZ");
s.clear();
```

### Convert

```cpp
string num = to_string(42);
int x = stoi("42");
long long y = stoll("1234567890123");
double z = stod("3.14");
```

### Iterate

```cpp
for (char c : s) { ... }
for (char &c : s) c = toupper(c); // need <cctype>
```

### Read full line

```cpp
string line;
getline(cin, line);
```

After `cin >> n;` remember leftover newline:

```cpp
int n; cin >> n;
string s; getline(cin, s); // may read empty
getline(cin, s);           // actual line
```

---

## 2. String CP Patterns

### Frequency of characters

```cpp
vector<int> freq(26, 0);
for (char c : s) if (islower(c)) freq[c - 'a']++;
```

### Palindrome check

```cpp
bool isPal = true;
for (int i = 0, j = (int)s.size() - 1; i < j; i++, j--)
    if (s[i] != s[j]) { isPal = false; break; }
```

### Sort characters

```cpp
sort(s.begin(), s.end());
```

### Sliding window on string / two pointers  
(Use indices; `string` behaves like `vector<char>`.)

---

## 3. `pair`

```cpp
#include <utility>

pair<int, int> p = {1, 2};
pair<int, int> q = make_pair(3, 4);
cout << p.first << " " << p.second << "\n";

p = {5, 6};
swap(p.first, p.second);
```

### Comparison (default)

Compares `first`, then `second`:

```cpp
pair<int,int> a = {1, 5}, b = {1, 3};
// b < a is true
```

### Vector of pairs

```cpp
vector<pair<int,int>> v;
v.push_back({i, a[i]});
sort(v.begin(), v.end());
```

### Structured bindings (C++17)

```cpp
for (auto [idx, val] : v) {
    cout << idx << " " << val << "\n";
}
```

### As map key

```cpp
map<pair<int,int>, int> mp;
mp[{1, 2}] = 10;
```

---

## 4. `tie` for Unpacking

```cpp
int x, y;
tie(x, y) = p;          // from pair
tie(x, y) = {10, 20};

// ignore one field
tie(x, ignore) = p;
```

Useful in Dijkstra / sorting swaps:

```cpp
int a = 3, b = 1;
if (tie(a) > tie(b)) { ... } // rarely needed; prefer direct compare
```

---

## 5. `tuple`

```cpp
#include <tuple>

tuple<int,int,int> t = {1, 2, 3};
auto t2 = make_tuple(1, 2, string("x"));

cout << get<0>(t) << "\n";
auto [a, b, c] = t;     // C++17

tuple<int,int,string> u;
u = {1, 2, "hi"};
```

Sort by multiple keys:

```cpp
vector<tuple<int,int,int>> v; // (priority, time, id)
sort(v.begin(), v.end());     // lexicographical on all fields
```

---

## 6. When to Use What

| Need | Prefer |
|---|---|
| Two related ints | `pair<int,int>` |
| Three+ fields | `tuple` or a `struct` |
| Named clarity | `struct` with fields |
| String processing | `string` |
| Fixed alphabet counts | `array`/`vector` size 26 |

In longer codes, a small `struct` beats deep `tuple` nesting for readability.

```cpp
struct Edge {
    int to;
    int w;
};
vector<vector<Edge>> g;
```

---

## 7. Mini Practice

1. Count vowels in a string.  
2. Check if two strings are anagrams (`sort` both).  
3. Store array indices as `pair<value,index>` and sort.  
4. Use `tuple<dist, node, parent>` in a BFS variant.  
5. Parse integers from a line with `stringstream` (bonus).

```cpp
#include <sstream>
string line = "10 20 30";
stringstream ss(line);
int x;
while (ss >> x) { /* use x */ }
```

---

**Prev:** [Algorithms](/cpp-stl/algorithms/) · **Next:** [CP Cheatsheet](/cpp-stl/cp-cheatsheet/) · [Hub](/cpp-stl/)
