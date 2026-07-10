---
layout: course
title: "Kotlin in 10 Days — Hands-On"
permalink: /courses/kotlin-10-days/
course_track: "Kotlin"
description: "Concise JVM language: null-safety, data classes, coroutines intro, and a small script."
toc:
  - id: "day-1-hello-kotlin"
    label: "Day 1: Hello Kotlin"
  - id: "day-2-null-safety"
    label: "Day 2: Null safety"
  - id: "day-3-data-classes"
    label: "Day 3: Data classes"
  - id: "day-4-collections"
    label: "Day 4: Collections"
  - id: "day-5-functions-extensions"
    label: "Day 5: Functions & extensions"
  - id: "day-6-when-sealed"
    label: "Day 6: When & sealed"
  - id: "day-7-classes-interfaces"
    label: "Day 7: Classes & interfaces"
  - id: "day-8-file-io"
    label: "Day 8: File I/O"
  - id: "day-9-coroutines-intro"
    label: "Day 9: Coroutines intro"
  - id: "day-10-mini-cli"
    label: "Day 10: Mini CLI"
  - id: "capstone"
    label: "Capstone project"
---

# Kotlin in 10 Days — Hands-On

Concise JVM language: null-safety, data classes, coroutines intro, and a small script.

## Why this language
{: #why-this-language }

Kotlin is Android’s preferred language and a joy on the server (Ktor, Spring). Null-safety is built in.

## Setup (Day 0)
{: #setup-day-0 }

Install Kotlin compiler or use IntelliJ. Or:
```bash
sdk install kotlin   # if using SDKMAN
kotlinc -version
```

---

## Day 1: Hello Kotlin
{: #day-1-hello-kotlin }

### What you'll learn

- `fun main`
- val/var
- string templates

### Code along

```kotlin
fun main() {
  val name = "Kotlin"
  println("Hello, $name")
}
```

### Your task

Read a name from `readln()` and greet.

---

## Day 2: Null safety
{: #day-2-null-safety }

### What you'll learn

- `?`
- `?:`
- `?.`
- `!!` sparingly

### Code along

```kotlin
fun len(s: String?): Int = s?.length ?: 0
fun main() = println(len(null))
```

### Your task

Parse an Int from String?; return null on failure.

---

## Day 3: Data classes
{: #day-3-data-classes }

### What you'll learn

- `data class`
- copy
- destructuring

### Code along

```kotlin
data class User(val id: Int, val email: String)
fun main() {
  val u = User(1, "a@b.com")
  println(u.copy(email = "x@y.com"))
}
```

### Your task

Model Product; write a discounted copy helper.

---

## Day 4: Collections
{: #day-4-collections }

### What you'll learn

- listOf/mutableList
- map/filter
- groupBy

### Code along

```kotlin
val nums = listOf(1, 2, 3, 4)
println(nums.filter { it % 2 == 0 }.map { it * it })
```

### Your task

Group words by first letter.

---

## Day 5: Functions & extensions
{: #day-5-functions-extensions }

### What you'll learn

- Default args
- Named args
- Extension fns

### Code along

```kotlin
fun String.shout(): String = uppercase()
fun main() = println("hi".shout())
```

### Your task

Extension `List<Int>.median(): Double`.

---

## Day 6: When & sealed
{: #day-6-when-sealed }

### What you'll learn

- `when`
- sealed class/interface
- exhaustive

### Code along

```kotlin
sealed interface Result
data class Ok(val n: Int) : Result
data object Err : Result
fun show(r: Result) = when (r) {
  is Ok -> println(r.n)
  Err -> println("err")
}
```

### Your task

Sealed hierarchy for UI state: Loading/Ready/Error.

---

## Day 7: Classes & interfaces
{: #day-7-classes-interfaces }

### What you'll learn

- class
- interface
- object singleton

### Code along

```kotlin
interface Greeter { fun greet(): String }
class Person(val name: String) : Greeter {
  override fun greet() = "Hi $name"
}
```

### Your task

Implement a simple Repository interface with an in-memory object.

---

## Day 8: File I/O
{: #day-8-file-io }

### What you'll learn

- readText
- writeText
- use

### Code along

```kotlin
import java.io.File
fun main() {
  File("out.txt").writeText("hello")
  println(File("out.txt").readText())
}
```

### Your task

Append timestamped lines to a log file.

---

## Day 9: Coroutines intro
{: #day-9-coroutines-intro }

### What you'll learn

- `runBlocking`
- `launch`
- `delay`

### Code along

```kotlin
// needs kotlinx-coroutines
// runBlocking { launch { delay(100); println("hi") }; println("start") }
```

### Your task

If deps are hard, simulate with threads; else launch 3 jobs and join.

---

## Day 10: Mini CLI
{: #day-10-mini-cli }

### What you'll learn

- args
- when commands
- mutable state

### Code along

```kotlin
fun main(args: Array<String>) {
  when (args.getOrNull(0)) {
    "hello" -> println("hi ${args.getOrNull(1) ?: "world"}")
    else -> println("usage: hello <name>")
  }
}
```

### Your task

Todo CLI: add/list/done with a text file store.


---

## Capstone project
{: #capstone }

Build a **Kotlin todo CLI** with data classes, null-safe parsing, and file persistence. Optional: expose list via a tiny Ktor route.

## Related

- [Java in 10 Days](/courses/java-10-days/)
- [Swift in 10 Days](/courses/swift-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
