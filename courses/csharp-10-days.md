---
layout: course
title: "C# in 10 Days — Hands-On"
permalink: /courses/csharp-10-days/
course_track: "C#"
description: "Modern C# and .NET: records, LINQ, async, and a minimal web API sketch."
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

Modern C# and .NET: records, LINQ, async, and a minimal web API sketch.

## Why this language
{: #why-this-language }

C#/.NET is hot for enterprise APIs, game tooling (Unity), and cross-platform backends.

## Setup (Day 0)
{: #setup-day-0 }

Install [.NET SDK](https://dotnet.microsoft.com/):
```bash
dotnet --version
dotnet new console -n CsLab && cd CsLab
dotnet run
```

---

## Day 1: Hello & SDK
{: #day-1-hello-sdk }

### What you'll learn

- top-level statements
- dotnet run
- strings

### Code along

```csharp
Console.WriteLine($"Hello C#");
```

### Your task

Print args from `args`.

---

## Day 2: Types & classes
{: #day-2-types-classes }

### What you'll learn

- class
- props
- methods

### Code along

```csharp
class User {
  public required string Name { get; init; }
  public string Greet() => $"Hi {Name}";
}
```

### Your task

BankAccount with deposit/withdraw.

---

## Day 3: Records
{: #day-3-records }

### What you'll learn

- record
- with
- equality

### Code along

```csharp
record Point(int X, int Y);
var p = new Point(1, 2) with { X = 3 };
Console.WriteLine(p);
```

### Your task

Money record with Plus method.

---

## Day 4: LINQ
{: #day-4-linq }

### What you'll learn

- Where/Select
- GroupBy
- ToList

### Code along

```csharp
var xs = new[] { 1, 2, 3, 4 };
var ys = xs.Where(n => n % 2 == 0).Select(n => n * n).ToList();
Console.WriteLine(string.Join(",", ys));
```

### Your task

From users, select active emails.

---

## Day 5: Collections
{: #day-5-collections }

### What you'll learn

- List/Dict
- foreach
- span mindset

### Code along

```csharp
var m = new Dictionary<string, int>();
m["a"] = 1;
foreach (var (k, v) in m) Console.WriteLine($"{k}={v}");
```

### Your task

Word frequency counter.

---

## Day 6: Async/await
{: #day-6-asyncawait }

### What you'll learn

- Task
- HttpClient
- await

### Code along

```csharp
using var http = new HttpClient();
var s = await http.GetStringAsync("https://httpbin.org/uuid");
Console.WriteLine(s);
```

### Your task

Fetch two URLs concurrently with Task.WhenAll.

---

## Day 7: Exceptions & nullability
{: #day-7-exceptions-nullability }

### What you'll learn

- nullable refs
- try/catch
- pattern matching

### Code along

```csharp
string? s = null;
Console.WriteLine(s?.Length ?? 0);
```

### Your task

Parse int; return null on failure using int?.

---

## Day 8: Interfaces & DI mindset
{: #day-8-interfaces-di-mindset }

### What you'll learn

- interface
- impl
- ctor inject sketch

### Code along

```csharp
interface IClock { DateTime UtcNow { get; } }
class SystemClock : IClock { public DateTime UtcNow => DateTime.UtcNow; }
```

### Your task

ITodoStore interface + in-memory implementation.

---

## Day 9: Minimal API peek
{: #day-9-minimal-api-peek }

### What you'll learn

- WebApplication
- MapGet
- JSON

### Code along

```csharp
// dotnet new web -n ApiLab
// app.MapGet("/health", () => Results.Ok(new { ok = true }));
```

### Your task

Add POST /echo that returns the body.

---

## Day 10: Files & CLI
{: #day-10-files-cli }

### What you'll learn

- File.ReadAllText
- args
- exit codes

### Code along

```csharp
if (args.Length == 0) { Console.Error.WriteLine("usage"); return 1; }
var text = File.ReadAllText(args[0]);
Console.WriteLine(text.Split().Length);
```

### Your task

wc-like tool with line/word/char counts.


---

## Capstone project
{: #capstone }

Build a **.NET todo API**: minimal APIs, in-memory store behind an interface, and a few integration-style tests or curl script.

## Related

- [Java in 10 Days](/courses/java-10-days/)
- [TypeScript in 10 Days](/courses/typescript-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
