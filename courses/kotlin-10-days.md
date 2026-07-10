---
layout: course
title: "Kotlin in 10 Days — Hands-On"
permalink: /courses/kotlin-10-days/
course_track: "Kotlin"
description: "Null safety, data classes, and coroutines — build a working Kotlin CLI, one concept at a time."
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
    label: "Day 6: When & sealed classes"
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

Null safety, data classes, and coroutines — build a working Kotlin CLI, one concept at a time.

## Why this language
{: #why-this-language }

Kotlin is the default language for Android and a first-class option on the JVM server side (Ktor, Spring Boot supports it natively). The reason it displaced Java in both places isn't syntax sugar — it's that the type system tracks nullability, so a whole class of `NullPointerException` crashes becomes a compile error instead of a 2 a.m. page. If you already know Java, C#, or TypeScript, most of Kotlin will feel familiar; the parts that don't (null safety, `when` exhaustiveness, coroutines) are exactly the parts worth ten days of focused practice.

## Setup (Day 0)
{: #setup-day-0 }

Install the compiler directly, or through SDKMAN if you manage multiple JVM tools:

```bash
sdk install kotlin        # via SDKMAN, or brew install kotlin
kotlinc -version
mkdir kotlin-lab && cd kotlin-lab
```

You don't need IntelliJ for this course — `kotlinc file.kt -include-runtime -d app.jar && java -jar app.jar` works fine, or run scripts directly with `kotlinc -script file.kts`. Each day below is a single file you can compile and run in under a second.

---

## Day 1: Hello Kotlin
{: #day-1-hello-kotlin }

### Why it matters

Every Kotlin program — Android activity, Ktor route, or Gradle build script — starts from the same three ideas you'll use today: a top-level `fun main`, the `val`/`var` distinction, and string templates. Get these automatic and everything else reads naturally.

### Mental model

`val` is not "constant" in the sense of compile-time constant — it means *this reference can't be reassigned* after initialization, similar to `final` in Java or `const` for a binding (not the value) in JavaScript. `var` allows reassignment. Default to `val`; reach for `var` only when you have a real reason to mutate. String templates (`"$name"` or `"${expr}"`) replace concatenation — use the bare `$name` form for a single identifier and braces when you need an expression, a property, or a method call.

### Code along

```kotlin
fun main(args: Array<String>) {
    val greeting = "Hello"
    var visitCount = 0

    val target = if (args.isNotEmpty()) args[0] else "world"
    visitCount += 1

    println("$greeting, $target!")
    println("Visits this run: $visitCount")
    println("Uppercased: ${target.uppercase()}")
}
```

Compile and run it with `kotlinc hello.kt -include-runtime -d hello.jar && java -jar hello.jar Ada`. You should see three lines, the last one showing `${target.uppercase()}` evaluated, not printed literally — that's the tell that you understand template syntax versus plain string interpolation typos.

### Common mistake

Writing `val visitCount = 0` and then trying `visitCount += 1` two lines later. The compiler rejects it with "Val cannot be reassigned" — this is the language working as intended, not a bug. The fix is to decide up front whether the variable's identity changes over its lifetime; if it does, it's a `var`.

### Your task

Extend the program so that if no command-line argument is given, it reads a name from `readln()` instead of defaulting to `"world"`. Print an error to `System.err` and exit with a non-zero status via `kotlin.system.exitProcess(1)` if the input is blank after trimming.

**Check:** piping `echo "" | java -jar hello.jar` (blank input, no args) prints an error to stderr and `echo $?` afterward shows a non-zero code; piping `echo "Ada" | java -jar hello.jar` prints `Hello, Ada!` followed by `Visits this run: 1`.

---

## Day 2: Null safety
{: #day-2-null-safety }

### Why it matters

`NullPointerException` was called Tony Hoare's "billion-dollar mistake" for a reason — it's the single most common crash in Java-shaped codebases. Kotlin doesn't remove null; it makes nullability part of the type, so the compiler forces you to handle the absent case *before* you ship, not after a crash report.

### Mental model

`String` and `String?` are different types. A `String` is guaranteed non-null by the compiler; a `String?` might hold a value or `null`, and you can't call methods on it directly. Three operators bridge the gap: `?.` (safe call — returns null instead of throwing if the receiver is null), `?:` (Elvis — supplies a default when the left side is null), and `!!` (not-null assertion — throws `NullPointerException` immediately if the value is null, i.e., you're telling the compiler "trust me" and taking the crash risk back on yourself).

### Code along

```kotlin
fun parseAge(input: String?): Int? {
    return input?.trim()?.toIntOrNull()
}

fun describe(input: String?) {
    val age = parseAge(input)
    val message = age?.let { "You are $it years old." } ?: "Could not read an age from '$input'."
    println(message)
}

fun main() {
    describe("34")
    describe("  41  ")
    describe("banana")
    describe(null)
}
```

`toIntOrNull()` is the idiomatic parse: it returns `Int?`, never throws, and chains cleanly with `?.`. Run this and notice the last two calls fail gracefully into the Elvis default instead of crashing — that's the entire point of the exercise.

### Common mistake

Reaching for `!!` to silence a compiler error instead of actually handling the null case. `input!!.trim()` compiles, looks fine in a code review, and then blows up in production the first time `input` is genuinely null — you've reintroduced the exact bug Kotlin was designed to prevent. Use `!!` only when null there would be a real programming bug you *want* to crash loudly on (e.g., a value you just null-checked three lines above), never on external input.

### Your task

Write `fun readConfigValue(config: Map<String, String>, key: String): Int?` that looks up `key`, and if present, parses it as an `Int` (returning `null` on a bad number, not throwing). Test it with a map containing `"port" to "8080"` and `"timeout" to "abc"`, printing both results with a default of `-1` via Elvis when the result is null.

**Check:** with `mapOf("port" to "8080", "timeout" to "abc")`, `readConfigValue(config, "port") ?: -1` prints `8080`, and `readConfigValue(config, "timeout") ?: -1` prints `-1` (the parse failed, so the Elvis default kicked in).

---

## Day 3: Data classes
{: #day-3-data-classes }

### Why it matters

Most of a real codebase is plumbing data between layers — DTOs, API payloads, database rows. In Java that means hand-writing (or generating) `equals`, `hashCode`, and `toString` for every one of them. Kotlin's `data class` generates all three plus a `copy()` function, which is why Kotlin code has noticeably less boilerplate than the Java it replaced.

### Mental model

A `data class` is defined by its *properties*, not its identity: two instances with equal properties are `==` equal, print readably via `toString()`, and can be destructured into individual variables. `copy()` returns a new instance with one or more properties changed, leaving the original untouched — this is how you do "update" without mutation.

### Code along

```kotlin
data class Product(val id: Int, val name: String, val priceCents: Int)

fun applyDiscount(product: Product, percentOff: Int): Product {
    val newPrice = product.priceCents * (100 - percentOff) / 100
    return product.copy(priceCents = newPrice)
}

fun main() {
    val mug = Product(1, "Mug", 1200)
    val discounted = applyDiscount(mug, 25)

    println(mug)
    println(discounted)
    println("Same object? ${mug === discounted}")
    println("Equal by value? ${mug == discounted}")

    val (id, name, price) = discounted
    println("Destructured: id=$id name=$name price=$price")
}
```

`mug === discounted` checks reference identity and is `false`; `mug == discounted` checks structural equality via the generated `equals()` and is also `false` here because the price differs — that distinction between `===` and `==` is the whole lesson.

### Common mistake

Putting a mutable `var` property in a data class and then using instances as `HashMap` keys or storing them in a `HashSet`. `hashCode()` is computed from the properties at insertion time; if you mutate the property afterward, the hash changes but the bucket doesn't — the object becomes unfindable in the collection even though it's still "in" it. Keep data class properties `val`; model changes with `copy()` instead of mutation.

### Your task

Model `data class Order(val id: Int, val item: String, val quantity: Int, val unitPriceCents: Int)`. Write `fun total(order: Order): Int` returning `quantity * unitPriceCents`, and `fun rush(order: Order): Order` that returns a copy with quantity set to 1 and a comment printed showing the two orders are `!=` but share the same `id`.

**Check:** for `Order(1, "Mug", 3, 500)`, `total(order)` returns `1500`; `rush(order)` returns `Order(1, "Mug", 1, 500)` with `total(rush(order)) == 500`; `order != rush(order)` is `true` while `order.id == rush(order).id` is `true`.

---

## Day 4: Collections
{: #day-4-collections }

### Why it matters

Filtering, transforming, and grouping lists is what most business logic actually is once you strip away the framework code. Kotlin's collection operations chain into pipelines that read like a description of the transformation, replacing loops full of accumulator variables and off-by-one bugs.

### Mental model

`listOf(...)` returns a read-only `List` — the reference can't add or remove elements, though the underlying data could still be mutable if aliased elsewhere, so treat it as an API contract, not a guarantee of immutability. `mutableListOf(...)` gives you `add`/`remove`. Chained operations like `.filter { }.map { }` each produce a **new** list; nothing is mutated in place, and none of them touch the original.

### Code along

```kotlin
fun main() {
    val words = listOf("kotlin", "java", "go", "rust", "kotlin", "swift", "go", "go")

    val counts: Map<String, Int> = words.groupingBy { it }.eachCount()
    val sortedByCount = counts.entries.sortedByDescending { it.value }

    println("Frequency:")
    for ((word, count) in sortedByCount) {
        println("  $word -> $count")
    }

    val byFirstLetter = words.distinct().groupBy { it.first() }
    println("Grouped by first letter: $byFirstLetter")

    val longWords = words.distinct().filter { it.length > 3 }.map { it.uppercase() }
    println("Long words, uppercased: $longWords")
}
```

`groupingBy { it }.eachCount()` is the idiomatic word-frequency counter — it's a single pass, no manual `mutableMapOf` with `getOrDefault` bookkeeping.

### Common mistake

Writing `words.filter { ... }` and expecting `words` itself to shrink. It doesn't — `filter` returns a new list and the original is untouched. Bugs from this usually show up as "I filtered the list but the old items are still there," because the code kept using the original reference instead of the filtered result.

### Your task

Given `val sentence = "the quick brown fox jumps over the lazy dog the fox runs"`, split it into words, then produce: (1) the top 3 most frequent words with counts, (2) a `Map<Int, List<String>>` grouping distinct words by length. Print both.

**Check:** the frequency ranking starts `the -> 3`, `fox -> 2` (both unambiguous — everything else ties at count 1); the length map has exactly three keys, `3`, `4`, and `5`, each holding 3 words — key `3` is `[the, fox, dog]`, key `4` is `[over, lazy, runs]`, key `5` is `[quick, brown, jumps]`.

---

## Day 5: Functions & extensions
{: #day-5-functions-extensions }

### Why it matters

Default and named arguments eliminate the overload explosion you'd otherwise write to handle "give me this parameter, or a sensible default." Extension functions let you add methods to types you don't own — `String`, `List`, even Android's `View` — without inheritance or wrapper classes, which is why idiomatic Kotlin code reads as if the standard library anticipated your exact need.

### Mental model

An extension function is ordinary syntax sugar: `fun String.shout()` compiles to a static function taking a `String` as its first (hidden) parameter, called with `receiver.shout()`. Because of that, extension resolution is **static** — determined by the *declared* type at the call site at compile time, not by runtime polymorphism. That matters when a member function and an extension function share a signature: the member always wins.

### Code along

```kotlin
fun String.isPalindrome(): Boolean {
    val cleaned = this.lowercase().filter { it.isLetterOrDigit() }
    return cleaned == cleaned.reversed()
}

fun List<Int>.median(): Double {
    require(isNotEmpty()) { "median() of an empty list is undefined" }
    val sorted = sorted()
    val mid = sorted.size / 2
    return if (sorted.size % 2 == 1) sorted[mid].toDouble()
           else (sorted[mid - 1] + sorted[mid]) / 2.0

}

fun greet(name: String = "friend", loud: Boolean = false): String {
    val base = "Hello, $name"
    return if (loud) base.uppercase() + "!" else base
}

fun main() {
    println("Was it a car or a cat I saw".isPalindrome())
    println("racecar".isPalindrome())
    println(listOf(7, 1, 3, 9).median())

    println(greet())
    println(greet("Ada"))
    println(greet(loud = true))
}
```

Notice `greet(loud = true)` skips `name` entirely by using a named argument — this is what replaces Java-style method overloading for optional parameters.

### Common mistake

Assuming an extension function can override behavior for subtypes the way a virtual method would. It can't: extension resolution uses the static type of the expression, so if you write `fun Animal.speak() = "..."` and separately `fun Dog.speak() = "woof"`, calling `speak()` on a variable declared as `Animal` (even holding a `Dog` at runtime) always calls the `Animal` version. Extensions are for adding capabilities, not for polymorphic dispatch — use interfaces and real methods when you need that.

### Your task

Write `fun String.wordCount(): Int` and `fun String.titleCase(): String` (capitalize the first letter of every word, lowercase the rest). Then write a function `fun summarize(text: String, maxWords: Int = 10): String` with a default parameter that truncates `text` to `maxWords` words and appends `"..."` if it was longer.

**Check:** `"hello world".wordCount()` returns `2`; `"HELLO world".titleCase()` returns `"Hello World"`; `summarize("the quick brown fox jumps", maxWords = 3)` returns `"the quick brown..."`; `summarize("hi there")` (5 words, under the default of 10) returns `"hi there"` unchanged, with no trailing `"..."`.

---

## Day 6: When & sealed classes
{: #day-6-when-sealed }

### Why it matters

State machines — UI screens, parser results, network responses — have a fixed, known set of shapes. `sealed` plus `when` gives you a compiler-checked guarantee that you've handled every one of them, so adding a new state later causes a compile error everywhere you forgot to update, instead of a silent runtime gap.

### Mental model

A `sealed` class or interface restricts all direct subtypes to the same file or module, so the compiler knows the *complete* list of possibilities. A `when` expression (one whose result is used — assigned, returned, or passed as an argument) over a sealed type must be exhaustive: leave out a case and it won't compile, no `else` required. A `when` used as a *statement* (result discarded) is **not** checked for exhaustiveness — this asymmetry is worth memorizing.

### Code along

```kotlin
sealed interface UiState
data object Loading : UiState
data class Ready(val items: List<String>) : UiState
data class Error(val message: String) : UiState

fun render(state: UiState): String = when (state) {
    Loading -> "Loading..."
    is Ready -> if (state.items.isEmpty()) "No items." else "Items: ${state.items.joinToString(", ")}"
    is Error -> "Error: ${state.message}"
}

fun main() {
    val states = listOf(
        Loading,
        Ready(listOf("apples", "bread")),
        Ready(emptyList()),
        Error("timeout")
    )
    states.forEach { println(render(it)) }
}
```

Try commenting out the `is Error` branch: `render` no longer compiles, because it's a `when` **expression** returning `String`. That immediate feedback loop is the payoff for using sealed types.

### Common mistake

Adding a new subtype to a sealed hierarchy (say, `data object Empty : UiState`) and expecting every `when` in the codebase to flag it automatically. It only does if the `when` is used as an expression. A `when (state) { Loading -> ...; is Ready -> ... }` used purely for its side effects (a statement, nothing returned or assigned) compiles fine even with a missing branch — the new case is silently ignored at runtime. When exhaustiveness matters, force expression form, e.g. by assigning the result to `Unit` or returning it, or add an explicit `else -> error("unhandled state")`.

### Your task

Add a fourth state `data object Empty : UiState` to the hierarchy above. Update `render` to handle it, confirm the compiler complains before you do, then write a second function `fun isTerminal(state: UiState): Boolean` that returns `true` only for `Ready` and `Error` (not `Loading` or `Empty`), using exhaustive `when`.

**Check:** before you add the `Empty` branch to `render`, `kotlinc` fails to compile with an error naming `'when' expression must be exhaustive`; after fixing it, `isTerminal(Empty)` and `isTerminal(Loading)` both return `false`, while `isTerminal(Ready(emptyList()))` and `isTerminal(Error("x"))` both return `true`.

---

## Day 7: Classes & interfaces
{: #day-7-classes-interfaces }

### Why it matters

Interfaces plus `object` singletons are how Kotlin achieves dependency-injection-friendly design without a heavyweight framework: define a seam (an interface), swap implementations for tests versus production, and use `object` when you genuinely need exactly one instance app-wide.

### Mental model

`object` declares a class *and* creates its single instance in the same statement — Kotlin handles thread-safe lazy initialization for you, which is what the classic Java singleton pattern (double-checked locking, static holder class) exists to hand-roll. An `interface` can declare abstract members and even provide default implementations; a `class` implementing it must supply the abstract ones with `override`.

### Code along

```kotlin
data class Todo(val id: Int, val text: String, val done: Boolean = false)

interface TodoRepository {
    fun add(text: String): Todo
    fun all(): List<Todo>
    fun complete(id: Int): Boolean
}

object InMemoryTodoRepository : TodoRepository {
    private val items = mutableListOf<Todo>()
    private var nextId = 1

    override fun add(text: String): Todo {
        val todo = Todo(nextId++, text)
        items.add(todo)
        return todo
    }

    override fun all(): List<Todo> = items.toList()

    override fun complete(id: Int): Boolean {
        val index = items.indexOfFirst { it.id == id }
        if (index == -1) return false
        items[index] = items[index].copy(done = true)
        return true
    }
}

fun main() {
    val repo: TodoRepository = InMemoryTodoRepository
    repo.add("Write Kotlin course")
    repo.add("Ship it")
    repo.complete(1)

    repo.all().forEach { println("[${if (it.done) "x" else " "}] ${it.id} ${it.text}") }
}
```

Declaring `repo` as the interface type, not `InMemoryTodoRepository`, is deliberate — every call site only depends on the contract, so swapping in a database-backed implementation later touches one line.

### Common mistake

Using an `object` for storage that should be scoped per-request or per-test. Because an `object` is a genuine process-wide singleton on the JVM, state added in one unit test (`repo.add(...)`) is still there when the next test runs, unless you explicitly reset it — a classic source of "tests pass alone, fail together" flakiness. For anything with a lifecycle shorter than the whole process, use a regular `class` you instantiate fresh, not `object`.

### Your task

Add `fun findByText(query: String): List<Todo>` to `TodoRepository` and implement it in `InMemoryTodoRepository` with a case-insensitive substring match. Then write a small `class InMemoryTodoRepositoryTest` style `main` block that adds three todos, calls `findByText("ship")`, and asserts (via `require`) exactly one match comes back.

**Check:** after adding `"Write course"`, `"Ship it"`, and `"Ship the docs"`, `findByText("ship")` (lowercase query) returns a list of size `2` (both "Ship" todos match case-insensitively); the `require` assertion for a size-`2` result passes silently, and changing it to expect size `1` makes `require` throw `IllegalArgumentException` with your message.

---

## Day 8: File I/O
{: #day-8-file-io }

### Why it matters

Reading config, writing logs, and persisting small amounts of state to disk is unavoidable outside of pure algorithm exercises. `use { }` is Kotlin's answer to Java's try-with-resources: it guarantees a `Closeable` (a file handle, a stream) gets closed even if the block throws, which is the difference between a program that leaks file descriptors under load and one that doesn't.

### Mental model

`File(path)` just builds a path object — it does nothing on disk and doesn't throw if the file is missing; only an actual read/write operation touches the filesystem and can fail. `readText()`/`writeText()` are whole-file convenience methods, fine for small files; for anything that might not fit comfortably in memory, use `bufferedWriter()`/`bufferedReader()` inside `use { }` so you stream instead of buffering the entire file as one string.

### Code along

```kotlin
import java.io.File
import java.time.Instant

fun appendLog(path: String, message: String) {
    File(path).also { it.parentFile?.mkdirs() }
        .bufferedWriter().use { writer ->
            // Overwrites; see task for append mode.
            writer.appendLine("${Instant.now()} $message")
        }
}

fun main() {
    val logPath = "activity.log"

    appendLog(logPath, "server started")
    appendLog(logPath, "request handled")
    appendLog(logPath, "server stopped")

    val file = File(logPath)
    println("Log has ${file.readLines().size} lines:")
    file.readLines().forEach { println("  $it") }
}
```

Run this twice and check the line count — with `bufferedWriter()` opened in default (truncate) mode, each run overwrites the file, so you'll always see 3 lines, not a growing count. That's intentional groundwork for the task below.

### Common mistake

Calling `File(path).readText()` on a file that doesn't exist and being surprised by a `FileNotFoundException` deep in a stack trace instead of a clear error at the call site. `File` objects are cheap and don't validate existence at construction — always check `file.exists()` (or catch the specific `IOException`) before assuming a read will succeed, especially for paths built from user input or CLI arguments.

### Your task

Fix `appendLog` so it genuinely appends across runs instead of truncating — use `File(path).appendText(...)` or open the writer with `FileWriter(path, /* append = */ true)`. Then write a `main` that calls it 3 times in a loop, reads the file back, and prints `"Total lines: N"` where `N` grows by 3 every time you run the program.

**Check:** delete `activity.log` if it exists, then run the program three separate times (three separate `java -jar` invocations) — it prints `Total lines: 3`, then `Total lines: 6`, then `Total lines: 9`, proving the file genuinely accumulates across process runs instead of resetting.

---

## Day 9: Coroutines intro
{: #day-9-coroutines-intro }

### Why it matters

Android and Ktor both lean on coroutines instead of raw threads because an OS thread costs roughly a megabyte of stack and a context switch; a suspended coroutine costs a small heap object. That difference is why a Ktor server can hold tens of thousands of concurrent connections that would fall over immediately with one thread each.

### Mental model

A `suspend` function can pause and resume without blocking the underlying thread — think of it as a function that can be "put on hold" instead of one that ties up a whole thread while waiting. `runBlocking` is the bridge from ordinary blocking code (like `main`) into that suspend world — use it at the outermost layer only. Inside a coroutine scope, `launch { }` starts a new concurrent child job; `delay(ms)` suspends without blocking, unlike `Thread.sleep(ms)`, which blocks the real thread and defeats the entire point.

### Code along

This needs the `kotlinx-coroutines-core` artifact on the classpath. The fastest way to run it standalone:

```bash
curl -L -o coroutines.jar \
  https://repo1.maven.org/maven2/org/jetbrains/kotlinx/kotlinx-coroutines-core-jvm/1.8.1/kotlinx-coroutines-core-jvm-1.8.1.jar
kotlinc coroutines_demo.kt -include-runtime -cp coroutines.jar -d demo.jar
java -cp "demo.jar:coroutines.jar" MainKt
```

`coroutines_demo.kt`:

```kotlin
import kotlinx.coroutines.*
import kotlin.system.measureTimeMillis

suspend fun fetchPrice(item: String, delayMs: Long): Int {
    delay(delayMs)
    return item.length * 100
}

fun main() = runBlocking {
    val elapsed = measureTimeMillis {
        val a = launch { println("apple: ${fetchPrice("apple", 300)}") }
        val b = launch { println("kiwi: ${fetchPrice("kiwi", 500)}") }
        val c = launch { println("fig: ${fetchPrice("fig", 200)}") }
        joinAll(a, b, c)
    }
    println("Total elapsed: ${elapsed}ms")
}
```

If the three jobs truly ran concurrently, elapsed time should land near 500ms (the slowest one), not 1000ms (the sum) — that's the number to check.

### Common mistake

Swapping `delay(ms)` for `Thread.sleep(ms)` inside a coroutine "because it's simpler." `Thread.sleep` blocks the actual OS thread the coroutine is running on, so if you're on a shared dispatcher, other coroutines scheduled on that thread stall too — you lose concurrency silently, and the elapsed-time check above will jump back up toward the sum of delays. Always suspend with `delay`, never block with `sleep`, inside coroutine code.

### Your task

Modify the demo so `fetchPrice` occasionally "fails" (throw an exception when `item == "kiwi"`), wrap each `launch` body in a `try/catch` that prints `"failed: $item"` instead of crashing the whole `runBlocking`, and confirm the other two jobs still complete and print their prices.

**Check:** the output contains `apple: 500`, `fig: 300`, and `failed: kiwi` (in some interleaved order — concurrency doesn't guarantee ordering), and `Total elapsed` stays near `500ms`, not `1000ms` — proving apple and fig still ran concurrently with the failing kiwi job instead of one failure stalling the others.

---

## Day 10: Mini CLI
{: #day-10-mini-cli }

### Why it matters

Almost every CLI tool you'll ever write — linters, migration scripts, deploy helpers — has the same shape: parse `args`, dispatch on a command word, mutate some state, report a result. Getting comfortable with that shape in a small program means you're not starting from scratch on the next one.

### Mental model

`args: Array<String>` is exactly what the OS handed your process — no flag parsing, no validation, done for you. `when (args.getOrNull(0))` dispatches on the first token safely (returns `null`, not an exception, past the end of the array), and each branch is free to read further args with its own `getOrNull` calls. Treat this like a tiny router: one entry point, exhaustive-ish branches, a clear "unknown command" fallback.

### Code along

```kotlin
import java.io.File

private val storePath = "todos.txt"

fun loadTodos(): List<String> =
    File(storePath).let { if (it.exists()) it.readLines().filter { line -> line.isNotBlank() } else emptyList() }

fun saveTodos(todos: List<String>) {
    File(storePath).writeText(todos.joinToString("\n"))
}

fun main(args: Array<String>) {
    val todos = loadTodos().toMutableList()

    when (args.getOrNull(0)) {
        "add" -> {
            val text = args.drop(1).joinToString(" ")
            if (text.isBlank()) {
                System.err.println("usage: add <text>")
                return
            }
            todos.add("[ ] $text")
            saveTodos(todos)
            println("Added: $text")
        }
        "list" -> {
            if (todos.isEmpty()) println("No todos yet.")
            todos.forEachIndexed { i, t -> println("$i: $t") }
        }
        "done" -> {
            val index = args.getOrNull(1)?.toIntOrNull()
            if (index == null || index !in todos.indices) {
                System.err.println("usage: done <index>")
                return
            }
            todos[index] = todos[index].replace("[ ]", "[x]")
            saveTodos(todos)
            println("Marked done: ${todos[index]}")
        }
        else -> println("usage: add <text> | list | done <index>")
    }
}
```

Build once with `kotlinc todo.kt -include-runtime -d todo.jar`, then run `java -jar todo.jar add "write course"`, `java -jar todo.jar list`, and `java -jar todo.jar done 0` — each invocation is a fresh process, so persistence has to happen through the file, not memory. That's a deliberate constraint, not an oversight.

### Common mistake

Forgetting that `args.drop(1).joinToString(" ")` is needed (not just `args[1]`) when the todo text itself contains spaces — `add write the kotlin course` arrives as five separate array elements, not one string, because the shell splits on whitespace before your program ever sees it. Always decide explicitly whether a command's trailing args should be joined or treated as a list.

### Your task

Add a `"remove <index>"` command that deletes a todo entirely (not just marks it done) and re-saves the file, shifting remaining indices down.

**Check:** add three todos, remove index `1`, then run `list` — it shows exactly two entries, `0` and `1`, holding the original 1st and 3rd todos' text (renumbered, not the original indices `0` and `2`).

---

## Capstone project
{: #capstone }

Combine everything into a **Kotlin todo CLI** you'd be comfortable showing in an interview:

- `data class Todo(val id: Int, val text: String, val done: Boolean = false)` — Day 3.
- A `TodoRepository` interface with an in-memory implementation for tests and a file-backed implementation for real use — Day 7.
- `sealed interface CliResult` (`Ok(message)` / `Failed(reason)`) returned from each command handler, rendered exhaustively — Day 6.
- Persistence via `File(...).use { }` with proper append/overwrite semantics — Day 8.
- Commands dispatched through `when` over `args.getOrNull(0)`, supporting `add`, `list`, `done`, `remove` — Day 10.

Stretch goal: expose `list` and `add` as HTTP routes with a minimal Ktor server, reusing the same `TodoRepository` you already wrote — the interface boundary from Day 7 is what makes that swap a small diff instead of a rewrite.

**Acceptance check:** running `add`, `add`, `done 0`, `remove 1`, `list` in sequence against a fresh store shows exactly one todo, marked done, at index `0` — and you can point at which day's concept (data class, sealed result, repository interface, file persistence, or dispatch) each line of `main` came from.

## Related

- [Java in 10 Days](/courses/java-10-days/)
- [Swift in 10 Days](/courses/swift-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
