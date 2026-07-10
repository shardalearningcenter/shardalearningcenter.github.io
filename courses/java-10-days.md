---
layout: course
title: "Java in 10 Days — Hands-On"
permalink: /courses/java-10-days/
course_track: "Java"
description: "Modern Java: records, streams, and a tiny REST-shaped console app."
toc:
  - id: "day-1-hello-javac"
    label: "Day 1: Hello & javac"
  - id: "day-2-classes-objects"
    label: "Day 2: Classes & objects"
  - id: "day-3-records-immutability"
    label: "Day 3: Records & immutability"
  - id: "day-4-collections"
    label: "Day 4: Collections"
  - id: "day-5-streams"
    label: "Day 5: Streams"
  - id: "day-6-exceptions"
    label: "Day 6: Exceptions"
  - id: "day-7-interfaces-polymorphism"
    label: "Day 7: Interfaces & polymorphism"
  - id: "day-8-packages-modules-lite"
    label: "Day 8: Packages & modules lite"
  - id: "day-9-http-client"
    label: "Day 9: HTTP client"
  - id: "day-10-mini-service-shape"
    label: "Day 10: Mini service shape"
  - id: "capstone"
    label: "Capstone project"
---

# Java in 10 Days — Hands-On

Modern Java: records, streams, and a tiny REST-shaped console app.

## Why this language
{: #why-this-language }

Java still powers enterprise backends, Android-adjacent ecosystems, and huge codebases. Learn the modern dialect.

## Setup (Day 0)
{: #setup-day-0 }

Install JDK 17+.
```bash
java -version
javac -version
mkdir java-lab && cd java-lab
```

---

## Day 1: Hello & javac
{: #day-1-hello-javac }

### What you'll learn

- class/main
- compile/run
- vars

### Code along

```java
public class Main {
  public static void main(String[] args) {
    System.out.println("Hello Java");
  }
}
```

### Your task

Print all command-line args.

---

## Day 2: Classes & objects
{: #day-2-classes-objects }

### What you'll learn

- Fields
- Constructors
- Methods

### Code along

```java
class User {
  final String name;
  User(String name) { this.name = name; }
  String greet() { return "Hi " + name; }
}
```

### Your task

BankAccount with deposit/withdraw.

---

## Day 3: Records & immutability
{: #day-3-records-immutability }

### What you'll learn

- `record`
- equals/hashCode
- Compact ctor

### Code along

```java
record Point(int x, int y) {}
void demo() { System.out.println(new Point(1, 2)); }
```

### Your task

Record `Money(long cents)` with a method `plus`.

---

## Day 4: Collections
{: #day-4-collections }

### What you'll learn

- List/Map/Set
- Generics
- for-each

### Code along

```java
var nums = List.of(1, 2, 3);
var m = new HashMap<String, Integer>();
m.put("a", 1);
```

### Your task

Word count with HashMap.

---

## Day 5: Streams
{: #day-5-streams }

### What you'll learn

- map/filter/collect
- Optional
- method refs

### Code along

```java
var out = List.of(1,2,3,4).stream().filter(n -> n % 2 == 0).map(n -> n * n).toList();
System.out.println(out);
```

### Your task

From List<User>, collect emails of active users.

---

## Day 6: Exceptions
{: #day-6-exceptions }

### What you'll learn

- checked vs unchecked
- try-with-resources
- custom

### Code along

```java
try (var r = new java.io.FileReader("a.txt")) {
  // ...
} catch (java.io.IOException e) {
  System.err.println(e.getMessage());
}
```

### Your task

Read a file line count with try-with-resources.

---

## Day 7: Interfaces & polymorphism
{: #day-7-interfaces-polymorphism }

### What you'll learn

- interface
- default methods
- implements

### Code along

```java
interface Greeter { String greet(); }
record Person(String name) implements Greeter {
  public String greet() { return "Hi " + name; }
}
```

### Your task

Shape interface; Circle/Rect implementations.

---

## Day 8: Packages & modules lite
{: #day-8-packages-modules-lite }

### What you'll learn

- package decl
- classpath
- jar mindset

### Code along

```java
// com/example/Util.java
package com.example;
public class Util { public static int add(int a, int b) { return a + b; } }
```

### Your task

Split Main and Util into packages; compile both.

---

## Day 9: HTTP client
{: #day-9-http-client }

### What you'll learn

- HttpClient
- URI
- JSON string handling

### Code along

```java
var client = java.net.http.HttpClient.newHttpClient();
var req = java.net.http.HttpRequest.newBuilder(java.net.URI.create("https://httpbin.org/get")).GET().build();
var res = client.send(req, java.net.http.HttpResponse.BodyHandlers.ofString());
System.out.println(res.statusCode());
```

### Your task

GET a URL and print status + first 200 chars of body.

---

## Day 10: Mini service shape
{: #day-10-mini-service-shape }

### What you'll learn

- Router-by-hand
- DTO records
- Main loop

### Code along

```java
// Console "API": commands add/list for todos in memory
var todos = new java.util.ArrayList<String>();
todos.add("learn java");
System.out.println(todos);
```

### Your task

REPL: `add <text>`, `list`, `quit` for todos.


---

## Capstone project
{: #capstone }

Build a **todo CLI** with records, packages, and file persistence (JSON or CSV). Optional: expose the same store behind a tiny HTTP server.

## Related

- [Kotlin in 10 Days](/courses/kotlin-10-days/)
- [C# in 10 Days](/courses/csharp-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
