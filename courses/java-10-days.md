---
layout: course
title: "Java in 10 Days — Hands-On"
permalink: /courses/java-10-days/
course_track: "Java"
description: "Modern Java: records, streams, exceptions, and a real console service — with the compiler errors explained."
toc:
  - id: "why-this-language"
    label: "Why this language"
  - id: "setup-day-0"
    label: "Setup (Day 0)"
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

Modern Java: records, streams, and a console app shaped like a real service — every day compiles and prints checkable output.

## Why this language
{: #why-this-language }

Java still runs an enormous share of the world's backend systems, and the language has changed a lot in the last decade — records, `var`, streams, and pattern matching make modern Java far more concise than the Java most tutorials still teach. This course uses the modern dialect throughout: you won't write a getter/setter/equals/hashCode block by hand once, because `record` does it for you, and that's exactly how you should write Java in 2026.

## Setup (Day 0)
{: #setup-day-0 }

You need JDK 17 or newer (for records and modern switch expressions).

```bash
java -version     # expect 17, 21, or newer
javac -version
mkdir java-lab && cd java-lab
```

Verify compile-and-run works end to end:

```bash
cat > Check.java <<'EOF'
public class Check {
    public static void main(String[] args) {
        System.out.println("Java is ready");
    }
}
EOF
java Check.java   # single-file source launch, no separate compile step needed
```

Expected: `Java is ready`. Modern `java` can run a single `.java` file directly without a manual `javac` step — that's what you'll use for Days 1–9. Delete `Check.java` before Day 1.

```bash
rm Check.java
```

**Checkpoint:** if `java -version` reports anything below 17, install a current JDK (Temurin/Adoptium is a solid free choice) before continuing — records and the switch-expression syntax used later will not compile on Java 11 or older.

---

## Day 1: Hello & javac
{: #day-1-hello-javac }

### Why this matters

Every Java program's entry point is `public static void main(String[] args)` inside a class whose name must match the filename. Getting the compile/run cycle solid — and knowing exactly what error you get when the class name and filename mismatch — avoids an hour of confusion later.

### Mental model

`java Main.java` (JDK 11+) compiles and runs in one step for quick scripts; `javac Main.java` then `java Main` is the traditional two-step (compile once, run many times) you'll use once programs span multiple files. The public class name **must** match the filename exactly, including case.

### Code along

```java
// Day01.java
public class Day01 {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");

        if (args.length == 0) {
            System.out.println("No arguments. Try: java Day01.java foo bar");
            return;
        }

        for (int i = 0; i < args.length; i++) {
            System.out.printf("arg[%d] = %s%n", i, args[i]);
        }
        System.out.println("Total args: " + args.length);
    }
}
```

Run:

```bash
java Day01.java foo bar
```

Expected output:

```
Hello, Java!
arg[0] = foo
arg[1] = bar
Total args: 2
```

### Common mistake

Naming the file `day01.java` (lowercase) while the class is `public class Day01`. Compilation fails with `error: class Day01 is public, should be declared in a file named Day01.java`. Java enforces this exact match for any `public` class — it's not a style suggestion, it's a hard rule the compiler checks. Rename the file to match the class exactly (case-sensitive) and it compiles.

### Your task

Print the arguments in reverse order, and separately print whichever argument is alphabetically first (skip this comparison gracefully — print a message instead — if zero or one argument was given).

**Check:** `java Day01.java banana apple cherry` prints the three args reversed (`cherry apple banana`) and separately identifies `apple` as alphabetically first.

---

## Day 2: Classes & objects
{: #day-2-classes-objects }

### Why this matters

Encapsulating state behind methods — never exposing a mutable field directly — is how you prevent a `BankAccount` balance from being set to an invalid value by code that has no business touching it directly. This is the core object-oriented discipline Java was built around.

### Mental model

`private` fields plus public methods is the default shape of a well-designed class: the class alone decides how its state can change. `final` on a field means it's assigned exactly once (in the constructor, or at declaration) and never reassigned — use it for anything that shouldn't change after construction.

### Code along

```java
// Day02.java
public class Day02 {
    static class BankAccount {
        private final String owner;
        private long balanceCents;

        BankAccount(String owner, long openingCents) {
            if (openingCents < 0) {
                throw new IllegalArgumentException("opening balance cannot be negative");
            }
            this.owner = owner;
            this.balanceCents = openingCents;
        }

        void deposit(long cents) {
            if (cents <= 0) throw new IllegalArgumentException("deposit must be positive");
            balanceCents += cents;
        }

        void withdraw(long cents) {
            if (cents > balanceCents) {
                throw new IllegalStateException(
                    "insufficient funds: have " + balanceCents + ", want " + cents);
            }
            balanceCents -= cents;
        }

        long balance() {
            return balanceCents;
        }

        String owner() {
            return owner;
        }
    }

    public static void main(String[] args) {
        BankAccount acct = new BankAccount("Ada", 10_000);
        acct.deposit(500);

        try {
            acct.withdraw(20_000);
        } catch (IllegalStateException e) {
            System.out.println("withdraw failed: " + e.getMessage());
        }

        System.out.println(acct.owner() + "'s balance: " + acct.balance() + " cents");
    }
}
```

Expected output:

```
withdraw failed: insufficient funds: have 10500, want 20000
Ada's balance: 10500 cents
```

### Common mistake

Making `balanceCents` package-private or public "just to make it easier to test," then having other code do `acct.balanceCents = -500` directly — bypassing every validation check in `deposit`/`withdraw`. The class compiles fine; the bug is a design mistake the compiler can't catch, because you removed the very protection `private` gives you. Keep fields `private` and, if tests genuinely need to inspect state, add a read-only accessor like `balance()` rather than widening field visibility.

### Your task

Add a `transferTo(BankAccount other, long cents)` method that withdraws from `this` and deposits into `other`, leaving both accounts unchanged if the withdrawal would fail (check before mutating either).

**Check:** transferring 300 from an account with 10500 to a fresh account with 0 leaves them at 10200 and 300; attempting to transfer more than available throws `IllegalStateException` and neither balance changes.

---

## Day 3: Records & immutability
{: #day-3-records-immutability }

### Why this matters

Plain data carriers — a `Point`, a `Money` amount, an API response shape — used to require 20+ lines of boilerplate (constructor, getters, `equals`, `hashCode`, `toString`) written by hand. `record` generates all of it correctly from a one-line declaration, and correctly is the key word: hand-written `equals`/`hashCode` pairs are a classic source of subtle bugs.

### Mental model

`record Point(int x, int y) {}` gives you a constructor, `x()`/`y()` accessors (not `getX()`/`getY()` — that's the old JavaBeans convention), plus value-based `equals`, `hashCode`, and `toString`, for free. Records are implicitly `final` and all fields are implicitly `final` too — a record is immutable by construction, which is exactly what you want for a value type.

### Code along

```java
// Day03.java
public class Day03 {
    record Money(long cents) {
        Money {
            if (cents < 0) throw new IllegalArgumentException("money cannot be negative");
        }

        Money plus(Money other) {
            return new Money(this.cents + other.cents);
        }

        String format() {
            return String.format("$%d.%02d", cents / 100, cents % 100);
        }
    }

    record Point(int x, int y) {}

    public static void main(String[] args) {
        Money price = new Money(1999);
        Money tax = new Money(160);
        Money total = price.plus(tax);
        System.out.println(total.format());

        Point a = new Point(1, 2);
        Point b = new Point(1, 2);
        Point c = new Point(3, 4);

        System.out.println("a equals b: " + a.equals(b));
        System.out.println("a equals c: " + a.equals(c));
        System.out.println("a: " + a);
    }
}
```

Expected output:

```
$21.59
a equals b: true
a equals c: false
a: Point[x=1, y=2]
```

### Common mistake

Trying `new Money(-500)` and expecting a compile error — records don't validate ranges by default, only shape. The compact constructor (`Money { if (cents < 0) ... }` — note: no parameter list, no `this.cents = cents`, that assignment happens automatically after the block) is where you add validation, and it's easy to forget entirely, leaving invalid values constructible. Always add a compact constructor with validation for any record whose fields have real invariants (non-negative, non-null, non-empty).

### Your task

Add a `record TemperatureReading(double celsius, String sensorId)` with a compact constructor rejecting `celsius` below -273.15 (absolute zero) and a `sensorId` that's null or blank, plus a method `fahrenheit()` converting the value.

**Check:** `new TemperatureReading(-300, "s1")` throws `IllegalArgumentException`; `new TemperatureReading(100, "s1").fahrenheit()` returns `212.0`.

---

## Day 4: Collections
{: #day-4-collections }

### Why this matters

`List`, `Map`, and `Set` from `java.util` are what you reach for constantly — no Java program of any real size avoids them. Knowing which one fits a given problem (ordered vs unordered, duplicates allowed vs not, key lookup vs iteration) is a daily decision.

### Mental model

`List` preserves insertion order and allows duplicates; `Set` rejects duplicates (by `equals`/`hashCode`); `Map` is key→value lookup. `List.of(...)`/`Map.of(...)` create **immutable** collections — calling `.add()` on them throws `UnsupportedOperationException`; use `new ArrayList<>(...)` when you need a mutable copy.

### Code along

```java
// Day04.java
import java.util.*;

public class Day04 {
    public static void main(String[] args) {
        String text = "the quick brown fox jumps over the lazy dog the fox runs";
        Map<String, Integer> freq = new HashMap<>();
        for (String word : text.split("\\s+")) {
            freq.merge(word, 1, Integer::sum);
        }

        List<Map.Entry<String, Integer>> sorted = new ArrayList<>(freq.entrySet());
        sorted.sort((a, b) -> {
            int byCount = b.getValue() - a.getValue();
            return byCount != 0 ? byCount : a.getKey().compareTo(b.getKey());
        });

        for (int i = 0; i < 3 && i < sorted.size(); i++) {
            var e = sorted.get(i);
            System.out.println(e.getKey() + ": " + e.getValue());
        }

        Set<String> uniqueWords = new HashSet<>(freq.keySet());
        System.out.println("Unique words: " + uniqueWords.size());
    }
}
```

Run: `java Day04.java`

Expected output:

```
the: 3
fox: 2
brown: 1
Unique words: 9
```

### Common mistake

Writing `freq.get(word) + 1` on a `HashMap<String, Integer>` when `word` isn't present yet — `get` returns `null` for a missing key, and `null + 1` throws `NullPointerException` (auto-unboxing `null` fails). The idiomatic fix is exactly the `merge` call above: `freq.merge(word, 1, Integer::sum)` inserts `1` if the key is absent, or applies `Integer::sum` to combine the existing value with `1` if present — one line, no null check needed. This is worth memorizing; you'll use `merge` constantly for counting.

### Your task

Write `List<String> wordsLongerThan(Map<String, Integer> freq, int minLength)` returning distinct words (from the map's keys) longer than `minLength`, sorted alphabetically.

**Check:** `wordsLongerThan(freq, 4)` on the sample text returns `["brown", "jumps"]` in that exact order — verify against the actual word list by hand before trusting your output.

---

## Day 5: Streams
{: #day-5-streams }

### Why this matters

The Streams API turns manual for-loop accumulation (a mutable list, a mutable running total, manual iteration) into a declarative pipeline: filter, transform, collect. Once you're fluent in it, most collection-processing code becomes shorter and less bug-prone than the equivalent loop.

### Mental model

A stream pipeline is lazy — nothing executes until a **terminal** operation (`.collect`, `.forEach`, `.count`, `.sum`) runs. Streams are single-use: calling a terminal operation twice on the same stream throws `IllegalStateException: stream has already been operated upon or closed` — build a fresh stream (`.stream()` again from the source collection) each time you need to reprocess.

### Code along

```java
// Day05.java
import java.util.*;
import java.util.stream.*;

public class Day05 {
    record User(String name, int age, boolean active, String email) {}

    public static void main(String[] args) {
        List<User> users = List.of(
            new User("Ada", 36, true, "ada@example.com"),
            new User("Lin", 17, true, "lin@example.com"),
            new User("Sam", 42, false, "sam@example.com"),
            new User("Kai", 29, true, "kai@example.com")
        );

        List<String> activeAdultEmails = users.stream()
            .filter(u -> u.active() && u.age() >= 18)
            .map(User::email)
            .sorted()
            .toList();
        System.out.println(activeAdultEmails);

        double averageAge = users.stream()
            .mapToInt(User::age)
            .average()
            .orElse(0);
        System.out.printf("Average age: %.1f%n", averageAge);

        Map<Boolean, List<User>> byActive = users.stream()
            .collect(Collectors.groupingBy(User::active));
        System.out.println("Active count: " + byActive.getOrDefault(true, List.of()).size());
    }
}
```

Expected output:

```
[ada@example.com, kai@example.com]
Average age: 31.0
Active count: 3
```

### Common mistake

Chaining `.map(User::email)` before `.filter(...)` — order matters in a stream pipeline just like in a series of pipe operations. Filtering after mapping to `String` means you've lost access to `.age()` and `.active()` on the mapped elements; the code won't even compile with the filter written against `User` methods on a stream of `String`. Read a pipeline top to bottom as "what type flows through this stage" — get the filtering (which needs the full object) done before the mapping (which narrows to just what you need).

### Your task

Write a stream pipeline computing the total character count across all active users' emails (hint: `mapToInt(u -> u.email().length())`, filtered to active only, then `.sum()`).

**Check:** for the sample data, the total is `17 + 17 + 17` = the summed lengths of `ada@example.com`, `lin@example.com`, `kai@example.com` — compute it by hand and confirm your pipeline matches.

---

## Day 6: Exceptions
{: #day-6-exceptions }

### Why this matters

Java forces you to think about failure at compile time for **checked** exceptions (like `IOException`) — you cannot silently ignore them, the compiler won't let the code compile until you catch or declare them. `try`-with-resources guarantees cleanup (closing files, connections) even when something throws midway through.

### Mental model

Checked exceptions (`IOException`, `SQLException`) must be caught or declared with `throws` in the method signature — the compiler enforces it. Unchecked exceptions (`RuntimeException` and subclasses like `IllegalArgumentException`) need no such declaration — use them for programmer errors (bad arguments, invalid state) rather than expected, recoverable conditions.

### Code along

```java
// Day06.java
import java.io.*;
import java.nio.file.*;

public class Day06 {
    static int countLines(String path) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(Path.of(path))) {
            int count = 0;
            while (reader.readLine() != null) count++;
            return count;
        }
    }

    public static void main(String[] args) throws IOException {
        Path sample = Path.of("sample.txt");
        Files.writeString(sample, "line one\nline two\nline three\n");

        int lines = countLines("sample.txt");
        System.out.println("Lines: " + lines);

        try {
            countLines("does-not-exist.txt");
        } catch (IOException e) {
            System.out.println("Expected failure: " + e.getMessage());
        }

        Files.deleteIfExists(sample);
    }
}
```

Expected output (the exact wording of the `IOException` message varies by OS):

```
Lines: 3
Expected failure: does-not-exist.txt
```

### Common mistake

Writing `catch (Exception e) {}` (an empty catch block, or `catch (Exception e) { e.printStackTrace(); }` with no further action) around a checked exception just to make the compiler stop complaining. This is one of the most common real-world Java anti-patterns: it silences the compiler's genuine warning that something can fail, and now the failure disappears silently at runtime too — the program continues in a broken state with zero indication anything went wrong. Handle the specific exception meaningfully, or declare `throws` and let it propagate to a caller that can.

### Your task

Add a custom checked exception `class TooManyLinesException extends Exception` and make `countLines` throw it if the file has more than 1000 lines (read fully, then check, then throw with a message including the actual count).

**Check:** running `countLines` against a generated 1001-line file throws `TooManyLinesException` with a message containing `1001`; the 3-line sample file still returns `3` without throwing.

---

## Day 7: Interfaces & polymorphism
{: #day-7-interfaces-polymorphism }

### Why this matters

Interfaces let you write one function that accepts anything satisfying a contract — a `List<Shape>` can hold circles, squares, and triangles, and `totalArea` doesn't need to know which. This is how Java achieves extensibility: new shapes can be added later without touching existing code.

### Mental model

A class must explicitly declare `implements InterfaceName` (unlike Go's implicit interfaces) — the relationship is stated, not inferred. Default methods (`default` on an interface method) let you add new methods to an interface later without breaking every existing implementer, as long as you provide a sensible default body.

### Code along

```java
// Day07.java
import java.util.*;

public class Day07 {
    interface Shape {
        double area();

        default String describe() {
            return String.format("area = %.2f", area());
        }
    }

    record Circle(double radius) implements Shape {
        public double area() { return Math.PI * radius * radius; }
    }

    record Rectangle(double width, double height) implements Shape {
        public double area() { return width * height; }

        @Override
        public String describe() {
            return String.format("%.2f x %.2f, area = %.2f", width, height, area());
        }
    }

    public static void main(String[] args) {
        List<Shape> shapes = List.of(new Circle(2), new Rectangle(3, 4));

        for (Shape s : shapes) {
            System.out.println(s.describe());
        }

        double total = shapes.stream().mapToDouble(Shape::area).sum();
        System.out.printf("Total area: %.2f%n", total);
    }
}
```

Expected output:

```
area = 12.57
3.00 x 4.00, area = 12.00
Total area: 24.57
```

### Common mistake

Forgetting `implements Shape` on `Rectangle` while still defining an `area()` method with a matching signature — unlike Go, Java requires the explicit `implements` declaration. Without it, `Rectangle` is just a record with an unrelated `area()` method; you cannot put it in a `List<Shape>` at all, and the compiler error is `incompatible types: Rectangle cannot be converted to Shape` at the point you try. The method signature matching is not enough — the contract must be declared.

### Your task

Add a `Triangle(double base, double height, double sideA, double sideB, double sideC)` record implementing `Shape` with `area() = 0.5 * base * height`, using the default `describe()`.

**Check:** adding a `Triangle(6, 4, 5, 5, 6)` to the `shapes` list makes `describe()` print `area = 12.00` for it via the default method, and `Total area` updates to `36.57`.

---

## Day 8: Packages & modules lite
{: #day-8-packages-modules-lite }

### Why this matters

Packages are how Java organizes code across files and prevents name collisions between unrelated classes named the same thing in different libraries. Getting the `package` declaration and matching directory structure right is required before any multi-file Java project compiles at all.

### Mental model

A class in `package com.example.util;` **must** physically live in a directory path `com/example/util/` relative to your source root — this isn't a convention the compiler merely prefers, it's a hard requirement `javac` enforces. `import` brings a class from another package into scope by its simple name; fully-qualified names (`com.example.util.Util.add(...)`) always work without any import.

### Code along

```bash
mkdir -p com/example
```

```java
// com/example/Util.java
package com.example;

public class Util {
    public static int add(int a, int b) {
        return a + b;
    }

    public static boolean isPalindrome(String s) {
        String clean = s.toLowerCase().replaceAll("[^a-z0-9]", "");
        return clean.equals(new StringBuilder(clean).reverse().toString());
    }
}
```

```java
// Day08.java (at the project root, alongside com/)
import com.example.Util;

public class Day08 {
    public static void main(String[] args) {
        System.out.println("2 + 3 = " + Util.add(2, 3));
        System.out.println("'racecar' palindrome: " + Util.isPalindrome("racecar"));
        System.out.println("'hello' palindrome: " + Util.isPalindrome("hello"));
        System.out.println("'A man a plan a canal Panama' palindrome: "
            + Util.isPalindrome("A man a plan a canal Panama"));
    }
}
```

Compile and run both files together:

```bash
javac com/example/Util.java Day08.java
java Day08
```

Expected output:

```
2 + 3 = 5
'racecar' palindrome: true
'hello' palindrome: false
'A man a plan a canal Panama' palindrome: true
```

### Common mistake

Putting `Util.java` in the project root instead of `com/example/` while it declares `package com.example;`. Compilation fails: `error: class Util is public, should be declared in a file named Util.java` is *not* the error you'd expect here — instead you get inconsistent, confusing behavior or, with strict tooling, `error: package com.example does not exist` from any file trying to import it. The package declaration and the physical directory path must always agree.

### Your task

Add `Util.wordCount(String s)` returning the number of whitespace-separated tokens, and a second package `com.example.text` containing a `TextStats` class that uses `Util.wordCount` (add an `import com.example.Util;` inside that new file, even though both are under `com.example.*`, since Java doesn't auto-import sibling packages).

**Check:** `javac` compiles all three files together with no errors, and calling `TextStats`'s method on `"the quick brown fox"` reports `4` words.

---

## Day 9: HTTP client
{: #day-9-http-client }

### Why this matters

`java.net.http.HttpClient` (built into the JDK since 11) means you can make real HTTP calls with zero external dependencies — no need to reach for a third-party library for something this fundamental. Every service-to-service call in a Java backend eventually goes through something like this.

### Mental model

Build an immutable `HttpRequest` with a builder, send it through an `HttpClient`, and choose a `BodyHandler` (`ofString()`, `ofByteArray()`, etc.) that determines how the response body is materialized. `client.send(...)` blocks the calling thread; `client.sendAsync(...)` returns a `CompletableFuture` for non-blocking use.

### Code along

This spins up a local `HttpServer` so the example is self-contained and doesn't depend on the network being up.

```java
// Day09.java
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.http.*;
import java.time.Duration;

public class Day09 {
    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(0), 0);
        server.createContext("/health", exchange -> {
            byte[] body = "{\"status\":\"up\"}".getBytes();
            exchange.getResponseHeaders().add("Content-Type", "application/json");
            exchange.sendResponseHeaders(200, body.length);
            exchange.getResponseBody().write(body);
            exchange.close();
        });
        server.start();
        int port = server.getAddress().getPort();

        HttpClient client = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(2))
            .build();

        HttpRequest request = HttpRequest.newBuilder(URI.create("http://localhost:" + port + "/health"))
            .GET()
            .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("Status: " + response.statusCode());
        System.out.println("Body: " + response.body());

        server.stop(0);
    }
}
```

Expected output:

```
Status: 200
Body: {"status":"up"}
```

### Common mistake

Forgetting that `client.send(...)` throws two checked exceptions (`IOException`, `InterruptedException`) and having `main` not declare `throws Exception` — the code simply won't compile: `unreported exception java.io.IOException; must be caught or declared to be thrown`. This is the checked-exceptions discipline from Day 6 showing up again: the compiler is telling you, correctly, that a network call can fail and you must decide what happens when it does, even in a quick example script.

### Your task

Add a `POST` request to a new `/echo` context on the same local server that reads the request body and returns it verbatim, then send a JSON body to it with `HttpRequest.BodyPublishers.ofString(...)` and print the echoed response.

**Check:** sending `{"msg":"hi"}` to `/echo` and printing the response body shows exactly `{"msg":"hi"}` back.

---

## Day 10: Mini service shape
{: #day-10-mini-service-shape }

### Why this matters

A REPL-style command loop — read a command, dispatch, respond — is the shape of every interactive tool and a useful stepping stone before wiring up a real HTTP layer. Building one forces you to think about state management and clean separation between "parse the command" and "execute the command."

### Mental model

A `Scanner` reading `System.in` line by line, paired with a `switch` on the first token of each line, is enough structure for a real command loop. Keep the command-parsing logic separate from the state-mutating logic (as separate methods) so you can unit-test the state logic without needing to simulate stdin.

### Code along

```java
// Day10.java
import java.util.*;

public class Day10 {
    record Todo(int id, String text, boolean done) {
        Todo markDone() { return new Todo(id, text, true); }
    }

    static class TodoService {
        private final List<Todo> todos = new ArrayList<>();
        private int nextId = 1;

        Todo add(String text) {
            Todo t = new Todo(nextId++, text, false);
            todos.add(t);
            return t;
        }

        boolean complete(int id) {
            for (int i = 0; i < todos.size(); i++) {
                if (todos.get(i).id() == id) {
                    todos.set(i, todos.get(i).markDone());
                    return true;
                }
            }
            return false;
        }

        List<Todo> all() {
            return List.copyOf(todos);
        }
    }

    public static void main(String[] args) {
        TodoService service = new TodoService();
        Scanner scanner = new Scanner(System.in);

        System.out.println("Commands: add <text> | done <id> | list | quit");
        while (scanner.hasNextLine()) {
            String line = scanner.nextLine().trim();
            if (line.isEmpty()) continue;
            String[] parts = line.split("\\s+", 2);
            String command = parts[0];

            switch (command) {
                case "add" -> {
                    if (parts.length < 2) System.out.println("usage: add <text>");
                    else System.out.println("added #" + service.add(parts[1]).id());
                }
                case "done" -> {
                    int id = Integer.parseInt(parts[1].trim());
                    System.out.println(service.complete(id) ? "done #" + id : "no such id: " + id);
                }
                case "list" -> {
                    for (Todo t : service.all()) {
                        System.out.println((t.done() ? "[x] " : "[ ] ") + t.id() + ": " + t.text());
                    }
                }
                case "quit" -> {
                    return;
                }
                default -> System.out.println("unknown command: " + command);
            }
        }
    }
}
```

Test it:

```bash
printf "add buy milk\nadd ship capstone\ndone 1\nlist\nquit\n" | java Day10.java
```

Expected output:

```
Commands: add <text> | done <id> | list | quit
added #1
added #2
done #1
[x] 1: buy milk
[ ] 2: ship capstone
```

### Common mistake

Calling `Integer.parseInt(parts[1].trim())` for `done` without a `try`/`catch`, then piping `done abc` into the program — `NumberFormatException: For input string: "abc"` crashes the whole loop instead of printing a clean error and continuing. Any time you parse user input in a loop meant to keep running, wrap the parse in `try`/`catch` and print an error instead of letting an uncaught exception kill the process.

### Your task

Wrap the `done` case's parsing in a `try`/`catch (NumberFormatException e)` printing `"invalid id: " + parts[1]` instead of crashing, and add a `remove <id>` command removing a todo by id.

**Check:** piping `done abc` into the program prints an `invalid id` message and the loop continues to process subsequent commands (verify by piping `done abc\nlist\nquit` and confirming `list` still runs).

---

## Capstone project
{: #capstone }

Build a **todo CLI with persistence**: records for the data model, packages for organization, and JSON file storage — checkable end to end via a scripted sequence of commands.

**Deliverable — file layout:**

```
todo-cli/
  com/example/todo/Todo.java          # record: id, text, done
  com/example/todo/TodoService.java   # add/complete/remove/list + load/save
  com/example/todo/TodoCli.java       # main(): command loop from Day 10, wired to persistence
  README.md
```

**Persistence requirement:** write your own minimal JSON serializer/deserializer for the `Todo` list (a simple line-based or hand-rolled JSON array is fine — no external library required, since the shape is fixed and simple: `[{"id":1,"text":"buy milk","done":false}, ...]`). Load on startup (empty list if the file doesn't exist yet), save after every mutating command (`add`, `done`, `remove`).

**Service requirements:** `add(text)`, `complete(id) -> boolean`, `remove(id) -> boolean`, `all() -> List<Todo>`, `load(path)`, `save(path)` — `load` on a missing file returns an empty service state without throwing.

**CLI requirements:** same command loop shape as Day 10 (`add`, `done`, `remove`, `list`, `quit`), reading from and writing to `todos.json` in the current directory on every mutation.

**Acceptance check:** run the CLI, `add` two todos, `done` one, `quit`; inspect `todos.json` and confirm it's valid JSON reflecting exactly those two todos with the correct `done` flags; restart the CLI and `list` — the same two todos with the same state should appear, proving persistence actually round-trips.

## Related

- [Kotlin in 10 Days](/courses/kotlin-10-days/)
- [C# in 10 Days](/courses/csharp-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
