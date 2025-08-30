# Snippets which will be useful

## Custom comparator 
Say you have been given task to sort elements based on diffrence between the input element and the number in the list
So write this oneliner and you can sort the element.

```
 Collections.sort(ls, 
        (n1, n2) -> Math.abs(n1 - x) - Math.abs(n2 - x));
```
### There is another method to compare the strings it is called compareTo()
```
string1.compareTo(string2)
```
#### Example 2: Using Comparator

```
import java.util.*;


class Person {
    String name;
    int age;

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public String toString() {
        return name + " (" + age + ")";
    }
}

public class TreeMapComparatorExample {
    public static void main(String[] args) {
        // Sort by name instead of age
        Comparator<Person> nameComparator = Comparator.comparing(p -> p.name);

        TreeMap<Person, String> map = new TreeMap<>(nameComparator);

        /*
        // Old school Comparator (anonymous class)
        Comparator<Person> nameComparator = new Comparator<Person>() {
            @Override
            public int compare(Person p1, Person p2) {
                return p1.name.compareTo(p2.name);
            }
        };
        */

        map.put(new Person("Alice", 30), "Doctor");
        map.put(new Person("Bob", 25), "Engineer");
        map.put(new Person("Charlie", 35), "Teacher");

        for (Map.Entry<Person, String> entry : map.entrySet()) {
            System.out.println(entry.getKey() + " -> " + entry.getValue());
        }
    }
}
```

#### Output (sorted by name):

```
Alice (30) -> Doctor
Bob (25) -> Engineer
Charlie (35) -> Teacher
```
### 📦 Arrays
```
int[] arr = new int[10];
Arrays.fill(arr, -1);
int[] copy = Arrays.copyOf(arr, arr.length);
int[] sub = Arrays.copyOfRange(arr, 2, 5);
```

### 📑 String
```
String s = "hello";
s.charAt(i);
s.substring(0, 3);
s.length();
s.equals("test");
s.toCharArray();
```
### 🧠 HashMap / HashSet
```
Map<Integer, Integer> map = new HashMap<>();
map.put(key, val);
map.getOrDefault(key, 0);
map.containsKey(key);
map.remove(key);

```
```

Set<Integer> set = new HashSet<>();
set.add(x);
set.contains(x);
set.remove(x);

```

### 🧮 PriorityQueue

```

PriorityQueue<Integer> pq = new PriorityQueue<>(); // min-heap
PriorityQueue<Integer> maxpq = new PriorityQueue<>(Collections.reverseOrder()); // max-heap
pq.offer(x);
pq.poll();
pq.peek();

```

### 🔃 2D Arrays

```

int[][] grid = new int[m][n];
for (int[] row : grid) Arrays.fill(row, -1);

```
### 🚀 Sorting

```

Arrays.sort(arr);
Collections.sort(list); // for List<Integer>

Arrays.sort(arr, (a, b) -> b - a); // Desc order for Integer[]

```
### 🔣 Character & ASCII

```

char c = 'a';
int idx = c - 'a';  // 0-based index
Character.isDigit(c);
Character.isLetter(c);

```

### 💡 Quick Math

```

Math.max(a, b);
Math.min(a, b);
Math.abs(x);
Math.pow(x, y);

```

### 🧪 Binary Search

```
int idx = Arrays.binarySearch(arr, target);

```

### 📚 Stack & Queue

```

Stack<Integer> stack = new Stack<>();
stack.push(x); stack.pop(); stack.peek();

```

```

Queue<Integer> q = new LinkedList<>();
q.offer(x); q.poll(); q.peek();

```

### 🔁 DFS / BFS Template
####  DFS

```

void dfs(int u) {
    visited[u] = true;
    for (int v : graph.get(u)) {
        if (!visited[v]) dfs(v);
    }
}

```

### BFS

```

Queue<Integer> q = new LinkedList<>();
q.offer(start);
while (!q.isEmpty()) {
    int cur = q.poll();
    for (int next : adj.get(cur)) {
        if (!visited[next]) {
            visited[next] = true;
            q.offer(next);
        }
    }
}


```