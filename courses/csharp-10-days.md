---
layout: course
title: "C# in 10 Days — Hands-On"
permalink: /courses/csharp-10-days/
course_track: "C#"
description: "Records, LINQ, and async/await — build a working .NET console app, one concept at a time."
toc:
  - id: "day-1-hello-sdk"
    label: "Day 1: Hello & SDK"
  - id: "day-2-types-classes"
    label: "Day 2: Types & classes"
  - id: "day-3-records"
    label: "Day 3: Records"
  - id: "day-4-linq"
    label: "Day 4: LINQ"
  - id: "day-5-collections"
    label: "Day 5: Collections"
  - id: "day-6-asyncawait"
    label: "Day 6: Async/await"
  - id: "day-7-exceptions-nullability"
    label: "Day 7: Exceptions & nullability"
  - id: "day-8-interfaces-di-mindset"
    label: "Day 8: Interfaces & DI mindset"
  - id: "day-9-minimal-api-peek"
    label: "Day 9: Minimal API peek"
  - id: "day-10-files-cli"
    label: "Day 10: Files & CLI"
  - id: "capstone"
    label: "Capstone project"
---

# C# in 10 Days — Hands-On

Records, LINQ, and async/await — build a working .NET console app, one concept at a time.

## Why this language
{: #why-this-language }

C# and .NET run a huge share of enterprise backends, and the modern toolchain (`dotnet` CLI, cross-platform runtime, C# 12) has little in common with the Windows-only, XML-config-heavy .NET of a decade ago. LINQ turned collection processing into a first-class, composable query language before most other mainstream languages caught up, and `async`/`await` in C# is the design a lot of other languages' async syntax was directly modeled on. This course treats C# as a general backend/CLI language — no Visual Studio, no ASP.NET MVC ceremony, just the `dotnet` CLI.

## Setup (Day 0)
{: #setup-day-0 }

Install the [.NET SDK](https://dotnet.microsoft.com/):

```bash
dotnet --version
dotnet new console -o CsLab && cd CsLab
dotnet run
```

Every day below replaces the contents of `Program.cs` in this project. Re-run with `dotnet run` after each edit — no separate compile step needed during development.

---

## Day 1: Hello & SDK
{: #day-1-hello-sdk }

### Why it matters

Top-level statements (no `class Program { static void Main }` boilerplate needed since C# 9/10) are how nearly all modern C# sample code and small tools are written now — knowing this is the current idiom, not a shortcut you'll "graduate out of," matters for reading real projects.

### Mental model

A top-level `Program.cs` file's statements run in order as if they were the body of `Main`, and `args` (the string array of CLI arguments) is available automatically without declaring a `Main` method yourself. String interpolation (`$"text {expr}"`) is the idiomatic replacement for `string.Format` or concatenation — any expression can go inside the braces.

### Code along

```csharp
string greeting = "Hello";
int visitCount = 0;

string target = args.Length > 0 ? args[0] : "world";
visitCount += 1;

Console.WriteLine($"{greeting}, {target}!");
Console.WriteLine($"Visits this run: {visitCount}");
Console.WriteLine($"Uppercased: {target.ToUpper()}");
```

Run with `dotnet run -- Ada` (the `--` separates `dotnet run`'s own flags from your program's `args`). Forgetting the `--` is the most common reason a first argument mysteriously "disappears" — `dotnet run Ada` tries to interpret `Ada` as a `dotnet` option instead of passing it through.

### Common mistake

Running `dotnet run Ada` (no `--`) and being confused when `args.Length` is `0`. The `dotnet` CLI needs the `--` separator to know where its own arguments end and your program's begin — this is a `dotnet run` quirk, not a C# language issue, but it trips up almost everyone the first time.

### Your task

Change the program to read a name via `Console.ReadLine()` when no argument is supplied. `ReadLine()` returns `string?` (nullable) — handle a `null`/empty result by printing to `Console.Error` and exiting with `Environment.Exit(1)`.

**Check:** `echo "Ada" | dotnet run` prints `Hello, Ada!` and `Visits this run: 1`; `printf "" | dotnet run` (immediate EOF, `ReadLine()` returns `null`) prints an error to stderr and `echo $?` afterward shows `1`.

---

## Day 2: Types & classes
{: #day-2-types-classes }

### Why it matters

Classes with properties and methods are the backbone of typical C# code (records, covered tomorrow, are for a narrower "immutable data" case) — getting comfortable with auto-properties, `required` members, and expression-bodied methods now pays off in every class you write afterward.

### Mental model

`public string Name { get; init; }` is an auto-property: the compiler generates the backing field for you; `init` (not `set`) means it can only be assigned during object construction (via object-initializer syntax), giving you effectively-immutable properties without a constructor. `required` (C# 11+) forces callers to supply that property at construction time, turning "forgot to set an important field" into a compile error.

### Code along

```csharp
class User
{
    public required string Name { get; init; }
    public required string Email { get; init; }
    public int LoginCount { get; private set; } = 0;

    public string Greet() => $"Hi {Name}";

    public void RecordLogin() => LoginCount++;
}

var user = new User { Name = "Ada", Email = "ada@example.com" };
Console.WriteLine(user.Greet());

user.RecordLogin();
user.RecordLogin();
Console.WriteLine($"Logins: {user.LoginCount}");
```

`LoginCount` has a `private set`, so code outside the class can read it freely but can't assign it directly (`user.LoginCount = 99;` won't compile) — only `RecordLogin()` is allowed to change it, which is how you protect an invariant without hiding the value entirely.

### Common mistake

Marking a property `required` but giving it no way to be validated — `required string Email` still accepts an empty string, since `required` only enforces "was a value supplied," not "was it a *good* value." If you need real validation (non-empty, correct format), do it in a constructor or an `init`-accessor body, not by relying on `required` alone.

### Your task

Write a `BankAccount` class with `required string Owner { get; init; }`, a private `set`-only `Balance` property, and `Deposit(int cents)` / `bool Withdraw(int cents)` methods (the latter returns `false` on insufficient funds without changing the balance). Construct one and demonstrate both a successful and a failed withdrawal.

**Check:** starting from a `0`-balance account, `Deposit(5000)` then `Withdraw(2000)` returns `true` and leaves `Balance` at `3000`; a subsequent `Withdraw(10000)` returns `false` and `Balance` stays `3000`, unchanged.

---

## Day 3: Records
{: #day-3-records }

### Why it matters

Most data you pass between layers — API request/response shapes, event payloads — doesn't need class-style identity or mutability; `record` gives you value equality, a readable `ToString()`, and non-destructive updates (`with`) for free, exactly the same motivation as Kotlin's `data class`.

### Mental model

A `record` (positional syntax: `record Point(int X, int Y);`) is compared by value: two records with equal properties are `==`-equal, unlike ordinary classes which compare by reference by default. `with { Property = newValue }` returns a new record with one or more properties changed, leaving the original untouched — this is the C# equivalent of Kotlin's `copy()`.

### Code along

```csharp
record Point(int X, int Y);
record Money(int Cents, string Currency)
{
    public Money Plus(Money other)
    {
        if (Currency != other.Currency)
            throw new InvalidOperationException("currency mismatch");
        return this with { Cents = Cents + other.Cents };
    }
}

var origin = new Point(0, 0);
var moved = origin with { X = 3 };

Console.WriteLine(origin);
Console.WriteLine(moved);
Console.WriteLine($"Equal? {origin == moved}");

var price = new Money(500, "USD");
var tax = new Money(45, "USD");
var total = price.Plus(tax);
Console.WriteLine($"Total: {total}");
```

`origin == moved` prints `False` — despite the friendly name "record," equality is genuinely structural, computed from every property, not reference identity.

### Common mistake

Assuming `with` mutates the original record in place, then being surprised the original still shows its old values later in the same method. `origin with { X = 3 }` always returns a brand-new record; if you don't capture it in a variable (as `moved` does above), the modified version is discarded immediately. This is the same "copy, don't mutate" trap as Kotlin's `copy()`.

### Your task

Add a method `Money Minus(Money other)` to the `Money` record (throwing on currency mismatch, same as `Plus`), and write a small check that `price.Plus(tax).Minus(tax) == price` evaluates to `true` — confirming record value equality works the way you expect after a round trip of operations.

**Check:** with `price = new Money(500, "USD")` and `tax = new Money(45, "USD")`, `price.Plus(tax)` is `Money(545, "USD")`, and `price.Plus(tax).Minus(tax) == price` prints `True` — the round trip lands back on a record that's value-equal to the original, not merely similar.

---

## Day 4: LINQ
{: #day-4-linq }

### Why it matters

LINQ turns "loop, filter, accumulate" into a declarative pipeline that reads as a description of the result you want, not the steps to get there — and because it operates over any `IEnumerable<T>`, the exact same syntax works on in-memory lists, database queries (via EF Core), and XML.

### Mental model

Most LINQ methods (`Where`, `Select`, `OrderBy`, `GroupBy`) are **lazy** — they build up a query plan but don't actually run it until you enumerate the result (with `foreach`, `.ToList()`, `.First()`, etc.). That laziness is powerful (you can compose filters before deciding to execute) but also a common source of bugs if you expect a query variable to have already "run."

### Code along

```csharp
record Order(int Id, string Customer, decimal Amount, bool Shipped);

var orders = new List<Order>
{
    new(1, "Ada", 42.50m, true),
    new(2, "Grace", 15.00m, false),
    new(3, "Ada", 8.75m, true),
    new(4, "Linus", 99.99m, true),
    new(5, "Grace", 20.00m, true),
};

var shippedTotalsByCustomer = orders
    .Where(o => o.Shipped)
    .GroupBy(o => o.Customer)
    .Select(g => new { Customer = g.Key, Total = g.Sum(o => o.Amount) })
    .OrderByDescending(g => g.Total);

foreach (var row in shippedTotalsByCustomer)
{
    Console.WriteLine($"{row.Customer}: {row.Total:C}");
}

bool anyUnshipped = orders.Any(o => !o.Shipped);
Console.WriteLine($"Any unshipped orders? {anyUnshipped}");
```

`Sum(o => o.Amount)` inside `Select` runs once per group as the outer `GroupBy` is enumerated — the whole pipeline only actually executes when the `foreach` starts pulling results, which is worth watching for in the debugger if the order of operations ever seems surprising.

### Common mistake

Calling `.Where(...)` and then examining `orders.Count` (the *original* list's count) instead of the filtered query's count, expecting the source list to have shrunk. LINQ query methods never mutate the source collection — `Where` returns a new lazy sequence; if you need the filtered count, call `.Count()` on the query result itself, not on `orders`.

### Your task

Given `orders` above, write a LINQ query returning the single customer with the highest total amount across *all* orders (shipped or not), and a second query listing customers who have at least one unshipped order, sorted alphabetically.

**Check:** the highest-total customer is `Linus` (`99.99`, from a single order — more than Ada's combined `51.25` across two orders); the unshipped-order list contains exactly one name, `Grace` (order `2` is her only unshipped one).

---

## Day 5: Collections
{: #day-5-collections }

### Why it matters

`List<T>` and `Dictionary<TKey, TValue>` cover the overwhelming majority of everyday data structures in C# — knowing their complexity characteristics and the idiomatic iteration patterns (`foreach` with tuple deconstruction for dictionaries) is table stakes before LINQ makes it look effortless.

### Mental model

`List<T>` is a resizable array — indexing is O(1), `Add` is amortized O(1). `Dictionary<TKey, TValue>` is a hash table — lookups, inserts, and deletes are average O(1). Deconstructing a `KeyValuePair<K, V>` as `foreach (var (key, value) in dict)` is cleaner than `.Key`/`.Value` access everywhere, and works because `KeyValuePair` provides a `Deconstruct` method.

### Code along

```csharp
var words = new List<string> { "csharp", "kotlin", "go", "rust", "csharp", "swift", "go", "go" };

var counts = new Dictionary<string, int>();
foreach (var word in words)
{
    counts[word] = counts.GetValueOrDefault(word, 0) + 1;
}

foreach (var (word, count) in counts.OrderByDescending(kv => kv.Value))
{
    Console.WriteLine($"{word} -> {count}");
}

var byFirstLetter = words.Distinct()
    .GroupBy(w => w[0])
    .ToDictionary(g => g.Key, g => g.ToList());

foreach (var (letter, group) in byFirstLetter)
{
    Console.WriteLine($"{letter}: {string.Join(", ", group)}");
}
```

`GetValueOrDefault(word, 0)` avoids a `KeyNotFoundException` on the first sighting of any word — it's the C# equivalent of Kotlin's `map[key, default]` pattern from Day 4 of that course.

### Common mistake

Indexing a `Dictionary` with `counts[word]` to *read* a possibly-missing key, which throws `KeyNotFoundException` instead of returning a default — unlike `List<T>` indexing out of range (which throws `IndexOutOfRangeException`, at least a clear signal), a missing dictionary key error can be easy to miss in a stack trace if you weren't expecting it. Use `GetValueOrDefault`, `TryGetValue`, or `ContainsKey` first when the key might not exist.

### Your task

Given the same `words` list, compute the top 3 most frequent words with counts, and a `Dictionary<int, List<string>>` grouping distinct words by their length, printed in ascending order of length.

**Check:** the frequency ranking starts `go -> 3`, `csharp -> 2` (kotlin/rust/swift all tie at count `1`, so the third slot is unpredictable). Printed ascending by length: `2: go`, `4: rust`, `5: swift`, `6: csharp, kotlin` — four length groups total.

---

## Day 6: Async/await
{: #day-6-asyncawait }

### Why it matters

Nearly every real-world I/O operation in .NET — HTTP calls, database queries, file access — exposes an `async` API, and C#'s `async`/`await` (which several other languages' async syntax was modeled on) is how you write non-blocking code that still reads top-to-bottom instead of nested callbacks.

### Mental model

An `async Task<T>` method can `await` other async operations, suspending without blocking the calling thread while the awaited operation completes. `Task.WhenAll(...)` runs multiple tasks concurrently and completes when all of them do — critically different from awaiting each one in sequence, which runs them one after another.

### Code along

```csharp
using System.Diagnostics;

async Task<int> FetchPriceAsync(string item, int delayMs)
{
    await Task.Delay(delayMs);
    return item.Length * 100;
}

var stopwatch = Stopwatch.StartNew();

var appleTask = FetchPriceAsync("apple", 300);
var kiwiTask = FetchPriceAsync("kiwi", 500);
var figTask = FetchPriceAsync("fig", 200);

var prices = await Task.WhenAll(appleTask, kiwiTask, figTask);
stopwatch.Stop();

Console.WriteLine($"Prices: {string.Join(", ", prices)}");
Console.WriteLine($"Elapsed: {stopwatch.ElapsedMilliseconds}ms");
```

Starting all three `Task`s before awaiting any of them (rather than `await`-ing each call immediately) is what makes this concurrent — if elapsed time lands near 500ms rather than 1000ms, they genuinely overlapped.

### Common mistake

Writing `var applePrice = await FetchPriceAsync("apple", 300);` immediately followed by `var kiwiPrice = await FetchPriceAsync("kiwi", 500);` — each `await` here fully completes before the next call even starts, running strictly sequentially despite "using async." Starting the tasks first (assigning the `Task<T>` without awaiting), then awaiting them together via `Task.WhenAll`, is what actually gets you concurrency.

### Your task

Make `FetchPriceAsync` throw an `InvalidOperationException` when `item == "kiwi"`. Replace `Task.WhenAll` with individual `try/catch` around each `await` (or catch around the `WhenAll` call and inspect `Task.Exception`) so a kiwi failure doesn't prevent apple and fig's prices from being reported.

**Check:** the run prints apple's price `500` (`"apple".Length * 100`) and fig's price `300`, plus a caught-error message for kiwi — all three tasks report *something*, and `stopwatch.ElapsedMilliseconds` stays near `500`, not `1000`, proving the failure didn't block the other two from running concurrently.

---

## Day 7: Exceptions & nullability
{: #day-7-exceptions-nullability }

### Why it matters

Nullable reference types (enabled by default in modern .NET project templates) bring compile-time "this might be null" warnings to C#'s reference types, closing most of the gap with languages like Kotlin/Swift that had null safety from day one — combined with `try`/`catch`, that covers the two main ways C# code communicates "something's missing or wrong."

### Mental model

With nullable reference types enabled, `string` means "never null" and `string?` means "might be null" — the compiler warns (not errors, by default) when you dereference a `string?` without a null check. `??` (null-coalescing) supplies a default; `?.` chains safely; pattern matching (`is int n`) both checks a condition and binds a variable in one expression.

### Code along

```csharp
#nullable enable

int? ParseAge(string? input)
{
    if (input is null) return null;
    return int.TryParse(input.Trim(), out int result) ? result : null;
}

void Describe(string? input)
{
    int? age = ParseAge(input);
    string message = age is int a ? $"You are {a} years old." : $"Could not read an age from '{input ?? "null"}'.";
    Console.WriteLine(message);
}

Describe("34");
Describe("  41  ");
Describe("banana");
Describe(null);
```

`int.TryParse` follows the same "never throw, signal failure via a bool" pattern as Kotlin's `toIntOrNull()` and Swift's `Int(text)` — idiomatic parsing in every one of these languages avoids exceptions for routine, expected failures.

### Common mistake

Using the null-forgiving operator (`input!.Trim()`) to silence a nullable-warning instead of actually handling the null case, then hitting a real `NullReferenceException` the first time `input` is genuinely null at runtime. `!` only suppresses the *compiler warning* — it has zero effect at runtime, so it's purely a promise to the compiler that you were wrong to make if the value turns out to be null after all.

### Your task

Write `int? ReadConfigValue(Dictionary<string, string> config, string key)` that looks up `key` and parses the value as an `int`, returning `null` if the key is missing or unparsable. Test with a dictionary containing `"port"` (a valid number) and `"timeout"` (not a number), printing both results with `?? -1` as a fallback.

**Check:** with `{"port": "8080", "timeout": "abc"}`, `ReadConfigValue(config, "port") ?? -1` prints `8080`, and `ReadConfigValue(config, "timeout") ?? -1` prints `-1`.

---

## Day 8: Interfaces & DI mindset
{: #day-8-interfaces-di-mindset }

### Why it matters

Interfaces plus constructor injection are the foundation of testable .NET code — nearly every ASP.NET Core project is built around registering interface implementations in a DI container so production code and test code can swap dependencies without touching the classes that use them.

### Mental model

An `interface` declares a contract with no implementation; a class implementing it provides the behavior. Constructor injection means a class receives its dependencies (as interface types) through its constructor rather than constructing them itself — the class doesn't know or care whether it's talking to a real database or an in-memory fake, only that it satisfies the interface.

### Code along

```csharp
interface IClock
{
    DateTime UtcNow { get; }
}

class SystemClock : IClock
{
    public DateTime UtcNow => DateTime.UtcNow;
}

class FixedClock : IClock
{
    public DateTime UtcNow { get; }
    public FixedClock(DateTime fixedTime) => UtcNow = fixedTime;
}

interface ITodoStore
{
    void Add(string text);
    IReadOnlyList<string> All();
}

class InMemoryTodoStore : ITodoStore
{
    private readonly List<string> _items = new();
    private readonly IClock _clock;

    public InMemoryTodoStore(IClock clock) => _clock = clock;

    public void Add(string text) => _items.Add($"{_clock.UtcNow:O} {text}");

    public IReadOnlyList<string> All() => _items;
}

ITodoStore store = new InMemoryTodoStore(new FixedClock(new DateTime(2026, 1, 1)));
store.Add("write C# course");
store.Add("ship it");

foreach (var item in store.All())
{
    Console.WriteLine(item);
}
```

Passing `new FixedClock(...)` instead of `new SystemClock()` in a test gives you deterministic timestamps to assert against — that's the entire practical payoff of routing time through `IClock` instead of calling `DateTime.UtcNow` directly inside `InMemoryTodoStore`.

### Common mistake

Having `InMemoryTodoStore` construct its own `SystemClock` internally (`private readonly IClock _clock = new SystemClock();`) instead of receiving it through the constructor. It compiles and runs fine, but now every test using `InMemoryTodoStore` is stuck with real, non-deterministic timestamps — you've silently closed off the exact seam (constructor injection) that would have let you substitute `FixedClock` for testing.

### Your task

Add `bool Remove(string text)` to `ITodoStore` and implement it in `InMemoryTodoStore`. Write a small check using `FixedClock` that adds two todos, removes one by exact text match, and confirms `All()` returns exactly the remaining one.

**Check:** after adding `"write C# course"` and `"ship it"`, `Remove("write C# course")` returns `true` and `All()` afterward has `Count == 1`, containing only the `"ship it"` entry; calling `Remove("never added")` returns `false` and leaves `All()` unchanged.

---

## Day 9: Minimal API peek
{: #day-9-minimal-api-peek }

### Why it matters

ASP.NET Core's Minimal APIs strip away controller-class ceremony for small services — a handful of `MapGet`/`MapPost` calls is often all a microservice or internal tool needs, and it's the fastest on-ramp to seeing how the interfaces from Day 8 plug into a real web app via dependency injection.

### Mental model

`WebApplication.CreateBuilder(args)` sets up configuration, DI container, and logging; `builder.Services.AddSingleton<T>()` (or `AddScoped`/`AddTransient`) registers implementations so route handlers can just *ask* for an interface as a parameter and the framework supplies it — the same pattern as Day 8's constructor injection, now wired automatically per request.

### Code along

Create a web project instead of a console one: `dotnet new web -o ApiLab && cd ApiLab`, then replace `Program.cs`:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddSingleton<ITodoStore, InMemoryTodoStore>();
builder.Services.AddSingleton<IClock, SystemClock>();

var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new { ok = true }));

app.MapGet("/todos", (ITodoStore store) => Results.Ok(store.All()));

app.MapPost("/todos", (ITodoStore store, TodoRequest request) =>
{
    store.Add(request.Text);
    return Results.Created("/todos", request);
});

app.Run();

record TodoRequest(string Text);

interface IClock { DateTime UtcNow { get; } }
class SystemClock : IClock { public DateTime UtcNow => DateTime.UtcNow; }

interface ITodoStore
{
    void Add(string text);
    IReadOnlyList<string> All();
}

class InMemoryTodoStore : ITodoStore
{
    private readonly List<string> _items = new();
    private readonly IClock _clock;
    public InMemoryTodoStore(IClock clock) => _clock = clock;
    public void Add(string text) => _items.Add($"{_clock.UtcNow:O} {text}");
    public IReadOnlyList<string> All() => _items;
}
```

Run with `dotnet run` and hit it from another terminal: `curl http://localhost:5000/health`, `curl -X POST http://localhost:5000/todos -H "Content-Type: application/json" -d '{"Text":"buy milk"}'`, then `curl http://localhost:5000/todos` (check the console output for the actual bound port).

### Common mistake

Registering a store with `AddSingleton` and then being surprised that data persists across requests but resets on every app restart — `AddSingleton` means one shared instance for the whole app's lifetime, not "saved to disk." For anything that needs to survive a restart, you need real persistence (a file or database), which is exactly what Day 10 covers.

### Your task

Add `DELETE /todos/{index}` that removes a todo by its position in the list, returning `404` via `Results.NotFound()` if the index is out of range, and `204` via `Results.NoContent()` on success.

**Check:** after `POST`-ing two todos, `curl -X DELETE http://localhost:5000/todos/0 -w '%{http_code}'` prints `204`, and a follow-up `GET /todos` shows only the second todo remaining; `curl -X DELETE http://localhost:5000/todos/9 -w '%{http_code}'` (out of range) prints `404`.

---

## Day 10: Files & CLI
{: #day-10-files-cli }

### Why it matters

`File.ReadAllText`/`WriteAllText` plus exit codes are how a console tool persists state between runs and reports success/failure to whatever invoked it (a script, a CI job) — the same shape as the file-backed CLIs in every other language in this series, now in C#.

### Mental model

`File.ReadAllText(path)` throws `FileNotFoundException` if the path doesn't exist — check `File.Exists(path)` first, or catch the exception, depending on whether a missing file is an expected case (first run) or a genuine error. `Environment.Exit(code)` (or simply `return code;` from a top-level `Main`) sets the process exit code the OS/shell sees.

### Code along

```csharp
string storePath = "todos.txt";

List<string> LoadTodos() =>
    File.Exists(storePath) ? File.ReadAllLines(storePath).Where(l => !string.IsNullOrWhiteSpace(l)).ToList() : new List<string>();

void SaveTodos(List<string> todos) => File.WriteAllLines(storePath, todos);

var todos = LoadTodos();

if (args.Length == 0)
{
    Console.Error.WriteLine("usage: add <text> | list | done <index>");
    return 1;
}

switch (args[0])
{
    case "add":
        string text = string.Join(" ", args.Skip(1));
        if (string.IsNullOrWhiteSpace(text))
        {
            Console.Error.WriteLine("usage: add <text>");
            return 1;
        }
        todos.Add($"[ ] {text}");
        SaveTodos(todos);
        Console.WriteLine($"Added: {text}");
        break;

    case "list":
        if (todos.Count == 0) Console.WriteLine("No todos yet.");
        for (int i = 0; i < todos.Count; i++) Console.WriteLine($"{i}: {todos[i]}");
        break;

    case "done":
        if (args.Length < 2 || !int.TryParse(args[1], out int index) || index < 0 || index >= todos.Count)
        {
            Console.Error.WriteLine("usage: done <index>");
            return 1;
        }
        todos[index] = todos[index].Replace("[ ]", "[x]");
        SaveTodos(todos);
        Console.WriteLine($"Marked done: {todos[index]}");
        break;

    default:
        Console.WriteLine("usage: add <text> | list | done <index>");
        break;
}

return 0;
```

Top-level statements support `return <int>;` at the end to set the process exit code directly — build with `dotnet build -c Release`, then run the published binary repeatedly to see persistence across separate process invocations, exactly as with the other languages' CLI days.

### Common mistake

Writing `args[1]` for the todo text when the text has multiple words (`add write the csharp course`), instead of `string.Join(" ", args.Skip(1))`. The shell splits arguments on whitespace before your program ever runs, so `args` here is five separate elements, not one string — always decide explicitly whether trailing arguments should be joined.

### Your task

Add a `remove <index>` command that deletes a todo and re-saves the file, shifting later indices down.

**Check:** add three todos, remove index `1`, then run `list` — it shows exactly two entries, `0` and `1`, holding the original 1st and 3rd todos renumbered.

---

## Capstone project
{: #capstone }

Ship a **.NET todo API** combining the whole week:

- `record Todo(int Id, string Text, bool Done)` for the data shape — Day 3.
- `ITodoStore` interface with an in-memory implementation for tests and a file-backed (JSON via `System.Text.Json`) implementation for real runs, wired through constructor injection — Day 8.
- Minimal API routes `GET /todos`, `POST /todos`, `DELETE /todos/{id}` registered via DI in `Program.cs` — Day 9.
- LINQ used for any filtering/sorting the API exposes (e.g., `?done=true` query filtering) — Day 4.
- `async` handlers if your store does real file I/O, using `Task.WhenAll` where more than one independent operation can overlap — Day 6.

Write a short `curl`-based smoke-test script (or a couple of `dotnet test`-style checks) exercising add/list/delete against a running instance, and note in a README exactly which `dotnet` commands build and run the project.

**Acceptance check:** the smoke-test script, run against a freshly-started `dotnet run` instance, adds two todos, lists them, deletes one, and lists again showing exactly one remaining — all via `curl`, with expected HTTP status codes (`201`/`200`/`204`) asserted at each step, not just eyeballed.

## Related

- [Java in 10 Days](/courses/java-10-days/)
- [TypeScript in 10 Days](/courses/typescript-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
