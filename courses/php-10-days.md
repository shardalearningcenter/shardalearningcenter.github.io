---
layout: course
title: "PHP in 10 Days — Hands-On"
permalink: /courses/php-10-days/
course_track: "PHP"
description: "Types, Composer, and PDO — build a working PHP JSON API, one concept at a time."
toc:
  - id: "day-1-hello-php"
    label: "Day 1: Hello PHP"
  - id: "day-2-types-functions"
    label: "Day 2: Types & functions"
  - id: "day-3-arrays"
    label: "Day 3: Arrays"
  - id: "day-4-classes"
    label: "Day 4: Classes"
  - id: "day-5-composer"
    label: "Day 5: Composer"
  - id: "day-6-exceptions"
    label: "Day 6: Exceptions"
  - id: "day-7-files-json"
    label: "Day 7: Files & JSON"
  - id: "day-8-built-in-server"
    label: "Day 8: Built-in server"
  - id: "day-9-pdo-lite"
    label: "Day 9: PDO lite"
  - id: "day-10-mini-json-api"
    label: "Day 10: Mini JSON API"
  - id: "capstone"
    label: "Capstone project"
---

# PHP in 10 Days — Hands-On

Types, Composer, and PDO — build a working PHP JSON API, one concept at a time.

## Why this language
{: #why-this-language }

PHP still powers a huge share of the web, and the language most people learned five or ten years ago is not the language PHP 8 actually is: scalar type hints, `strict_types`, named arguments, and constructor property promotion make modern PHP a genuinely typed, fast language — Composer replaced the old copy-paste-a-library era with proper dependency management and autoloading. This course builds a small JSON API without a framework, so the mechanics (routing, JSON, persistence) aren't hidden behind Laravel or Symfony conventions.

## Setup (Day 0)
{: #setup-day-0 }

```bash
php -v   # 8.1 or newer
mkdir php-lab && cd php-lab
```

Every day's script runs directly with `php filename.php` from the terminal — no server needed until Day 8.

---

## Day 1: Hello PHP
{: #day-1-hello-php }

### Why it matters

`<?php`, `echo`, and variables are the absolute floor every PHP file is built on — even in a full framework, request handlers ultimately bottom out in this same syntax.

### Mental model

Every PHP variable starts with `$` and doesn't need a declared type unless you're writing a typed function signature. Double-quoted strings interpolate variables directly (`"Hello, $name"`); single-quoted strings don't interpolate at all — pick double quotes whenever you need a variable or escape sequence inside the string, single quotes for pure literal text.

### Code along

```php
<?php
$greeting = "Hello";
$visitCount = 0;

$target = $argv[1] ?? "world";
$visitCount += 1;

echo "$greeting, $target!\n";
echo "Visits this run: $visitCount\n";
echo "Uppercased: " . strtoupper($target) . "\n";
```

Run with `php hello.php Ada`. `$argv[0]` is always the script's own path (same convention as C's `argv`), so real arguments start at `$argv[1]` — and `??` (null coalescing) is the safe way to read an index that might not exist, instead of triggering an "undefined array key" warning.

### Common mistake

Writing `'Hello, $name'` with single quotes and getting the literal text `$name` printed instead of its value. Single-quoted strings only interpolate nothing — not variables, not `\n` — switch to double quotes (or use `.` concatenation) whenever interpolation is needed.

### Your task

Change the script to read a name from standard input via `trim(fgets(STDIN))` when no CLI argument is given. Print an error to `STDERR` (via `fwrite(STDERR, ...)`) and call `exit(1)` if the input is empty after trimming.

**Check:** `echo "Ada" | php hello.php` prints `Hello, Ada!` and `Visits this run: 1`; `printf "" | php hello.php` prints an error to stderr and `echo $?` afterward shows `1`.

---

## Day 2: Types & functions
{: #day-2-types-functions }

### Why it matters

Scalar type hints plus `declare(strict_types=1)` are what turned PHP from "anything coerces into anything" into a language where a function signature is an actual, enforced contract — this single `declare` line at the top of a file is one of the highest-value habits you can build.

### Mental model

Without `strict_types`, PHP coerces arguments to match a type hint where possible (a numeric string quietly becomes an `int`); with `declare(strict_types=1)`, a type mismatch throws a `TypeError` instead of silently coercing — you want the error, because silent coercion is exactly how subtle bugs creep into loosely-typed codebases. Return types (`: int`, `: ?string`) are checked the same way. `?Type` (nullable) means the value can be that type or `null`.

### Code along

```php
<?php
declare(strict_types=1);

function add(int $a, int $b): int
{
    return $a + $b;
}

function clamp(float $value, float $lo, float $hi): float
{
    if ($value < $lo) return $lo;
    if ($value > $hi) return $hi;
    return $value;
}

function greet(string $name = "friend", bool $loud = false): string
{
    $base = "Hello, $name";
    return $loud ? strtoupper($base) . "!" : $base;
}

echo add(2, 3), "\n";
echo clamp(15.5, 0.0, 10.0), "\n";
echo greet(), "\n";
echo greet(loud: true), "\n";
```

`greet(loud: true)` uses a named argument (PHP 8+) to skip `$name` entirely and supply only `$loud` — the same trick as Kotlin/Swift default+named parameters, and it reads far more clearly than a positional call with a placeholder.

### Common mistake

Calling `add("2", 3)` under `declare(strict_types=1)` expecting PHP to helpfully convert the string `"2"` to an `int` the way it would without strict types — instead it throws `TypeError: add(): Argument #1 ($a) must be of type int, string given`. That's the entire point of enabling strict types: catch a caller passing the wrong type at the exact call site, instead of a numeric string silently propagating through several functions before something breaks.

### Your task

Write `function percentageOf(int $value, int $total): float` that returns `$value` as a percentage of `$total`, throwing a `DivisionByZeroError` (via `throw new DivisionByZeroError(...)`, or just letting PHP raise it) when `$total === 0`. Call it with both a normal case and a zero-total case wrapped in `try`/`catch` (Day 6 covers this properly, but get a first look now).

**Check:** `percentageOf(25, 100)` returns `25.0`; wrapping `percentageOf(5, 0)` in `try`/`catch (DivisionByZeroError $e)` catches it cleanly — the script doesn't crash with an uncaught error.

---

## Day 3: Arrays
{: #day-3-arrays }

### Why it matters

PHP's `array` does double duty as both a list and a hash map — the same type backs `$list = [1, 2, 3]` and `$map = ["a" => 1, "b" => 2]` — so knowing the associative-array idioms (`foreach ($map as $key => $value)`, `array_map`/`array_filter`) covers most day-to-day data shuffling.

### Mental model

A plain PHP array is an *ordered* map under the hood — even a "list" like `[1, 2, 3]` has implicit integer keys `0, 1, 2`, which is why `foreach` always gives you insertion order regardless of whether keys are integers or strings. `array_map`, `array_filter`, and `array_reduce` mirror the same map/filter/reduce operations you've seen in every other language in this series, just as free functions rather than methods.

### Code along

```php
<?php
declare(strict_types=1);

$words = ["php", "ruby", "go", "rust", "php", "swift", "go", "go"];

$counts = [];
foreach ($words as $word) {
    $counts[$word] = ($counts[$word] ?? 0) + 1;
}

arsort($counts);
foreach ($counts as $word => $count) {
    echo "$word -> $count\n";
}

$distinct = array_unique($words);
$longWords = array_filter($distinct, fn($w) => strlen($w) > 3);
$uppercased = array_map('strtoupper', $longWords);
echo implode(", ", $uppercased), "\n";
```

`arsort($counts)` sorts the associative array by value, descending, while preserving the key => value association — plain `sort()` would renumber the keys and lose the word each count belonged to, which is a very easy mistake to make.

### Common mistake

Calling `sort($counts)` on an associative array when you meant `arsort` or `asort`. `sort()` re-indexes the array with fresh integer keys `0, 1, 2, ...` and discards the original string keys entirely — you lose the mapping from word to count, ending up with a plain list of numbers with no idea which word each one came from.

### Your task

Given `$sentence = "the quick brown fox jumps over the lazy dog the fox runs"`, split it with `explode(" ", $sentence)`, then build and print: the top 3 most frequent words with counts (using `arsort` and `array_slice`), and an associative array grouping distinct words by length.

**Check:** the frequency ranking starts `the -> 3`, `fox -> 2` (everything else ties at `1`). The length-grouped array has exactly three keys, `3`, `4`, and `5` — key `3` holds `["the", "fox", "dog"]`, key `4` holds `["over", "lazy", "runs"]`, key `5` holds `["quick", "brown", "jumps"]`.

---

## Day 4: Classes
{: #day-4-classes }

### Why it matters

Constructor property promotion (PHP 8+) collapses what used to be five lines of boilerplate (declare property, declare constructor parameter, assign it) into one line per property — modern PHP classes read almost as compactly as Kotlin data classes or C# records for the common case.

### Mental model

`public function __construct(public string $name)` simultaneously declares the `$name` property, accepts it as a constructor parameter, and assigns it — no separate `$this->name = $name;` line needed. `readonly` properties (PHP 8.1+) can be set once (typically in the constructor) and never reassigned afterward, giving you Kotlin-`val`-like immutability on individual properties.

### Code along

```php
<?php
declare(strict_types=1);

class BankAccount
{
    private int $balanceCents;

    public function __construct(
        public readonly string $owner,
        int $openingCents = 0
    ) {
        $this->balanceCents = $openingCents;
    }

    public function deposit(int $cents): void
    {
        if ($cents <= 0) {
            throw new InvalidArgumentException("deposit must be positive");
        }
        $this->balanceCents += $cents;
    }

    public function withdraw(int $cents): bool
    {
        if ($cents <= 0 || $cents > $this->balanceCents) {
            return false;
        }
        $this->balanceCents -= $cents;
        return true;
    }

    public function balance(): int
    {
        return $this->balanceCents;
    }
}

$account = new BankAccount("Ada", 5000);
$account->deposit(2000);
var_dump($account->withdraw(1000));
var_dump($account->withdraw(999999));
echo "Balance: {$account->balance()} cents\n";
```

`$this->balanceCents` is deliberately *not* promoted in the constructor signature — it needs custom logic (defaulting from `$openingCents`) rather than a direct 1:1 assignment, which is exactly when you fall back to declaring it separately and assigning it in the constructor body.

### Common mistake

Marking a property `public` (promoted or not) when it holds internal state that should only change through validated methods — `public int $balanceCents` would let any calling code do `$account->balanceCents = -999999;` directly, bypassing `deposit`/`withdraw` entirely. Keep mutable internal state `private` (or `protected`), and expose controlled mutation only through methods.

### Your task

Add a `private array $history = []` to `BankAccount`, appending a short string (e.g. `"deposit 2000"`) on every successful deposit/withdrawal, and a `public function statement(): void` that echoes each entry with the running balance after it.

**Check:** for the exact sequence in the code above (opening `5000`, `deposit(2000)` → `7000`, `withdraw(1000)` succeeds → `6000`, `withdraw(999999)` fails), `statement()` echoes exactly **two** entries (the failed withdrawal excluded), and the balance shown after the second entry is `6000`, matching `$account->balance()`.

---

## Day 5: Composer
{: #day-5-composer }

### Why it matters

Composer's PSR-4 autoloading means you never write a manual `require` for every class file again — organize your code into namespaced directories, and `require "vendor/autoload.php"` makes every class available by its fully-qualified name, exactly like `import` in most other modern languages.

### Mental model

`composer.json`'s `autoload.psr-4` maps a namespace prefix to a directory: `"Lab\\": "src/"` means the class `Lab\Math\Add` is expected to live at `src/Math/Add.php`. Composer generates `vendor/autoload.php`, which registers an autoloader that resolves any `Lab\...` class reference to the right file on demand — you stop thinking about file paths and just `use` the namespace you need.

### Code along

`composer.json`:

```json
{
    "name": "lab/php",
    "autoload": {
        "psr-4": { "Lab\\": "src/" }
    }
}
```

`src/Math/Calculator.php`:

```php
<?php
declare(strict_types=1);

namespace Lab\Math;

class Calculator
{
    public function add(int $a, int $b): int
    {
        return $a + $b;
    }

    public function average(array $numbers): float
    {
        if (empty($numbers)) {
            throw new \InvalidArgumentException("cannot average an empty list");
        }
        return array_sum($numbers) / count($numbers);
    }
}
```

`main.php`:

```php
<?php
declare(strict_types=1);

require __DIR__ . "/vendor/autoload.php";

use Lab\Math\Calculator;

$calc = new Calculator();
echo $calc->add(2, 3), "\n";
echo $calc->average([4, 8, 6, 5]), "\n";
```

Run `composer dump-autoload` (generates `vendor/autoload.php` from the mapping above without needing any actual dependency yet), then `php main.php`. The directory `src/Math/` matching the namespace `Lab\Math` is not a coincidence — PSR-4 requires that structural correspondence.

### Common mistake

Adding a new class file under `src/` and getting a "class not found" error, even though the namespace and `use` statement look correct. This almost always means the autoloader's cached mapping is stale or the file/folder path doesn't exactly match the namespace — run `composer dump-autoload` again after adding new files, and double-check the directory structure mirrors the namespace exactly (case matters on Linux filesystems).

### Your task

Add a second class `Lab\Text\WordCounter` with a method `count(string $text): array` returning a word-frequency associative array (reusing Day 3's technique), require it from `main.php` via `use Lab\Text\WordCounter`, and print the result for a short test sentence.

**Check:** `(new WordCounter())->count("go go php")` returns an associative array equal to `["go" => 2, "php" => 1]` — no `composer dump-autoload` errors, and no manual `require` of `WordCounter.php` needed in `main.php` beyond the `use` statement.

---

## Day 6: Exceptions
{: #day-6-exceptions }

### Why it matters

`try`/`catch`/`throw` is PHP's mechanism for recoverable, typed failure — and PHP's exception hierarchy (`Throwable` at the root, with `Error` and `Exception` as the two main branches) is worth understanding so you catch the right thing instead of a catch-all that hides real bugs.

### Mental model

`throw` raises any object implementing `Throwable` — typically a subclass of the built-in `Exception` or a custom one you define. `catch (SpecificException $e)` catches only that type (and subclasses); order multiple `catch` blocks from most specific to least specific, since PHP checks them in order and uses the first match. `finally` runs regardless of whether an exception was thrown or caught, same role as Ruby's `ensure` or Java/C#'s `finally`.

### Code along

```php
<?php
declare(strict_types=1);

class ParseError extends \RuntimeException {}

function parseStrictInt(string $text): int
{
    if (!preg_match('/^-?\d+$/', trim($text))) {
        throw new ParseError("not a valid integer: '$text'");
    }
    return (int) trim($text);
}

$inputs = ["42", "-7", "banana", "12abc"];

foreach ($inputs as $text) {
    try {
        $value = parseStrictInt($text);
        echo "$text -> $value\n";
    } catch (ParseError $e) {
        fwrite(STDERR, "skipped: {$e->getMessage()}\n");
    } finally {
        echo "  (checked '$text')\n";
    }
}
```

`preg_match` here rejects `"12abc"` outright — unlike PHP's own loose `(int)` cast, which would silently truncate `"12abc"` to `12` with no warning, exactly the kind of implicit coercion `strict_types` and careful validation are meant to guard against.

### Common mistake

Casting with `(int) $text` directly on unvalidated input and trusting the result, instead of validating first. `(int) "12abc"` is `12`, `(int) "abc"` is `0`, and `(int) ""` is also `0` — the cast never throws, so a genuinely malformed value silently becomes a plausible-looking number instead of a caught error. Validate the *format* first (as `parseStrictInt` does with a regex) whenever a bad number could be indistinguishable from a real `0`.

### Your task

Add a second custom exception `class RangeError extends \RuntimeException {}`, and extend `parseStrictInt` into a new function `parsePercentage(string $text): int` that throws `ParseError` for non-numeric input and `RangeError` if the parsed integer is outside `0..100`. Handle both distinctly in a loop over a handful of test inputs.

**Check:** `parsePercentage("50")` returns `50`; `parsePercentage("banana")` throws `ParseError`; `parsePercentage("150")` throws `RangeError`, not `ParseError` — two distinct `catch` blocks each fire for their own input.

---

## Day 7: Files & JSON
{: #day-7-files-json }

### Why it matters

JSON is the lingua franca between PHP backends and everything else — `json_encode`/`json_decode` plus `JSON_THROW_ON_ERROR` is the modern, safe way to serialize and parse it without silently swallowing malformed input.

### Mental model

`json_encode($data)` turns a PHP array/object into a JSON string; `json_decode($json, true)` parses it back into an associative array (the `true` flag; omit it and you get `stdClass` objects instead). By default, both functions return `false`/`null` on failure instead of throwing — passing `JSON_THROW_ON_ERROR` makes them throw a `JsonException` instead, which you almost always want, the same way `strict_types` turns silent coercion into a loud error.

### Code along

```php
<?php
declare(strict_types=1);

$data = ["ok" => true, "createdAt" => date("Y-m-d")];

file_put_contents(
    "out.json",
    json_encode($data, JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR)
);

$raw = file_get_contents("out.json");
if ($raw === false) {
    throw new RuntimeException("could not read out.json");
}

$parsed = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
echo "ok field: ", var_export($parsed["ok"], true), "\n";
echo "createdAt field: {$parsed['createdAt']}\n";
```

`JSON_THROW_ON_ERROR` on the `json_decode` call means a corrupted `out.json` (say, someone truncated it mid-write) throws a catchable `JsonException` right at the parse line, instead of returning `null` and letting `$parsed["ok"]` fail later with a confusing "trying to access array offset on null" warning.

### Common mistake

Checking `json_decode($raw)` for truthiness to detect failure — `json_decode("false")` legitimately returns the boolean `false` for valid JSON input, which looks identical to a decode failure if you're checking with `if (!$parsed)`. Use `JSON_THROW_ON_ERROR` (catch `JsonException`) or explicitly check `json_last_error() === JSON_ERROR_NONE` instead of testing the decoded value's truthiness.

### Your task

Write a function `function readJsonFile(string $path): array` that reads and decodes a JSON file, throwing a clear custom exception if the file is missing (`file_get_contents` returns `false`) or the JSON is malformed (`JsonException` from `JSON_THROW_ON_ERROR`), and demonstrate both failure paths with two different bad inputs.

**Check:** `readJsonFile("missing.json")` throws with a message mentioning the file wasn't found; `printf "not json" > bad.json` then `readJsonFile("bad.json")` throws a `JsonException`; `readJsonFile("out.json")` (a valid file from Day 7's code-along) returns an array with the same `ok` and `createdAt` keys you wrote.

---

## Day 8: Built-in server
{: #day-8-built-in-server }

### Why it matters

`php -S` starts a real HTTP server backed by a router script with zero configuration — exactly enough to build and test a small API locally without installing Apache/Nginx/FPM, and it's what most PHP tutorials (including this one) use for local development.

### Mental model

`php -S host:port router.php` routes every incoming request through `router.php` first. Returning `false` from the router tells the built-in server "serve this as a static file instead" (useful for assets); returning `true` (or nothing) means the router itself already sent the full response. `$_SERVER["REQUEST_URI"]` and `$_SERVER["REQUEST_METHOD"]` are the superglobals you read to implement routing by hand.

### Code along

`router.php`:

```php
<?php
declare(strict_types=1);

header("Content-Type: application/json");

$path = parse_url($_SERVER["REQUEST_URI"], PHP_URL_PATH);

if ($path === "/health") {
    echo json_encode(["ok" => true]);
    return true;
}

if ($path === "/time") {
    echo json_encode(["now" => date("c")]);
    return true;
}

http_response_code(404);
echo json_encode(["error" => "not found", "path" => $path]);
return true;
```

Start it with `php -S localhost:8000 router.php`, then hit it from another terminal: `curl http://localhost:8000/health`, `curl http://localhost:8000/time`, `curl http://localhost:8000/nope`.

### Common mistake

Forgetting `header("Content-Type: application/json")` and being surprised when a browser or strict HTTP client treats the response as plain text/HTML instead of JSON — PHP defaults to `text/html` unless you explicitly set the content type, even though the body you echoed is valid JSON.

### Your task

Add a `/echo` route that only accepts `POST` (return HTTP 405 for any other method via `http_response_code(405)`), reads the raw request body with `file_get_contents("php://input")`, and echoes it back inside `{"received": <body>}`.

**Check:** `curl -X POST http://localhost:8000/echo -d 'hello there'` prints `{"received":"hello there"}`; `curl -w '%{http_code}' http://localhost:8000/echo` (a plain `GET`) prints `405`, not the echoed body.

---

## Day 9: PDO lite
{: #day-9-pdo-lite }

### Why it matters

PDO is PHP's database-agnostic abstraction — the same prepared-statement API works whether you're talking to SQLite, MySQL, or Postgres, and prepared statements (as opposed to string-interpolated SQL) are the single most important habit for avoiding SQL injection.

### Mental model

`$pdo->prepare($sql)` parses a parameterized SQL statement once; `$stmt->execute([$value1, $value2])` binds actual values and runs it, with the driver handling all escaping — you should almost never see raw user input concatenated directly into an SQL string. `PDO::ERRMODE_EXCEPTION` makes database errors throw `PDOException` instead of silently returning `false`, which you want for the exact same reason `JSON_THROW_ON_ERROR` and `strict_types` are worth turning on.

### Code along

```php
<?php
declare(strict_types=1);

$pdo = new PDO("sqlite::memory:");
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$pdo->exec("CREATE TABLE todos (id INTEGER PRIMARY KEY, text TEXT NOT NULL, done INTEGER DEFAULT 0)");

$insert = $pdo->prepare("INSERT INTO todos (text) VALUES (?)");
$insert->execute(["write PHP course"]);
$insert->execute(["ship it"]);

$pdo->prepare("UPDATE todos SET done = 1 WHERE id = ?")->execute([1]);

$rows = $pdo->query("SELECT id, text, done FROM todos ORDER BY id")->fetchAll(PDO::FETCH_ASSOC);
foreach ($rows as $row) {
    $mark = $row["done"] ? "x" : " ";
    echo "[$mark] {$row['id']}: {$row['text']}\n";
}
```

`sqlite::memory:` gives you a fresh in-memory database per script run — perfect for examples and tests, since there's no leftover file to clean up between runs, but remember it disappears the moment the script ends.

### Common mistake

Building SQL by string concatenation — `"SELECT * FROM todos WHERE text = '" . $userInput . "'"` — instead of a parameterized query. Any `$userInput` containing a stray quote breaks the query at best, and at worst lets an attacker inject arbitrary SQL if that input ever comes from outside your own code (a form field, a query parameter). Prepared statements with `?` placeholders and `execute([...])` are not an optional style preference — treat string-concatenated SQL as a bug every time you see it.

### Your task

Add a `find(PDO $pdo, string $query): array` function that does a `LIKE '%...%'` search over the `text` column using a prepared statement (not string concatenation), and demonstrate it finding `"ship it"` with the query `"ship"`.

**Check:** `find($pdo, "ship")` returns exactly one row, the `"ship it"` todo; `find($pdo, "xyz")` (no match) returns an empty array, not an error.

---

## Day 10: Mini JSON API
{: #day-10-mini-json-api }

### Why it matters

Combining `php -S` routing, JSON encode/decode, and file or database persistence is the complete shape of a small production API — everything before today was one ingredient; this is the dish.

### Mental model

Read the request method and body, validate/parse the JSON, do the corresponding store operation, and write back a JSON response with an appropriate status code — that request/response cycle, repeated per route, is what a framework's routing layer automates for you once you've outgrown hand-rolling it.

### Code along

`router.php`:

```php
<?php
declare(strict_types=1);

header("Content-Type: application/json");

const STORE_PATH = __DIR__ . "/todos.json";

function loadTodos(): array
{
    if (!file_exists(STORE_PATH)) return [];
    $raw = file_get_contents(STORE_PATH);
    return $raw === false || $raw === "" ? [] : json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
}

function saveTodos(array $todos): void
{
    file_put_contents(STORE_PATH, json_encode($todos, JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR));
}

$method = $_SERVER["REQUEST_METHOD"];
$path = parse_url($_SERVER["REQUEST_URI"], PHP_URL_PATH);

if ($path !== "/todos") {
    http_response_code(404);
    echo json_encode(["error" => "not found"]);
    return true;
}

$todos = loadTodos();

if ($method === "GET") {
    echo json_encode($todos);
} elseif ($method === "POST") {
    $body = json_decode(file_get_contents("php://input"), true, 512, JSON_THROW_ON_ERROR);
    if (!isset($body["text"]) || trim((string) $body["text"]) === "") {
        http_response_code(400);
        echo json_encode(["error" => "text is required"]);
        return true;
    }
    $todos[] = ["id" => count($todos) + 1, "text" => $body["text"], "done" => false];
    saveTodos($todos);
    http_response_code(201);
    echo json_encode(end($todos));
} else {
    http_response_code(405);
    echo json_encode(["error" => "method not allowed"]);
}

return true;
```

Start with `php -S localhost:8000 router.php`. Test with `curl http://localhost:8000/todos`, `curl -X POST http://localhost:8000/todos -d '{"text":"buy milk"}'`, then `curl http://localhost:8000/todos` again to see the addition persisted across requests via the JSON file.

### Common mistake

Reading `count($todos) + 1` as an "ID" scheme that stays correct after deletions — if you later add a `DELETE` route without also fixing ID assignment, two todos can end up sharing an ID, or the count-based ID can collide with an existing one. This toy scheme is fine for `add`-only demos; a real implementation should track the highest ID ever issued (or use a proper database auto-increment) rather than deriving the next ID from the current count.

### Your task

Add a `DELETE /todos/{id}`-shaped route — since the built-in router doesn't parse path segments for you, match on a prefix like `/todos/` and parse the trailing numeric segment yourself — that removes the matching todo and re-saves, returning `404` if no todo has that ID.

**Check:** after two `POST`s (ids `1` and `2`), `curl -X DELETE http://localhost:8000/todos/1 -w '%{http_code}'` prints `200` (or whatever success code you chose) and a follow-up `GET /todos` shows only id `2`; `curl -X DELETE http://localhost:8000/todos/99 -w '%{http_code}'` prints `404`.

---

## Capstone project
{: #capstone }

Ship a **PHP todo JSON API** that draws on the full week:

- `class Todo` with constructor property promotion for `id`/`text`/`done` — Day 4.
- Composer-autoloaded namespaces (`Lab\Todo\...`) instead of one flat script — Day 5.
- A `TodoStore` interface with a JSON-file implementation (Day 7) and, as a stretch, a SQLite/PDO implementation (Day 9) behind the same interface.
- Custom exceptions (`StoreError`, `ValidationError`) caught distinctly at the router level, each mapped to the right HTTP status code — Day 6.
- Routes for `GET/POST/DELETE /todos` served through `php -S` — Days 8 and 10.

Document the exact `php -S localhost:PORT router.php` command and a couple of `curl` examples in a `README.md` so a reviewer can run it in under a minute.

**Acceptance check:** `POST /todos`, `POST /todos`, `DELETE /todos/1`, `GET /todos` against a freshly-started server shows exactly one remaining todo (id `2`); pointing `TodoStore` at a hand-corrupted JSON file makes the router return a mapped HTTP error status (not a raw PHP warning or a blank 500 page).

## Related

- [SQL in 10 Days](/courses/sql-10-days/)
- [JavaScript in 10 Days](/courses/javascript-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
