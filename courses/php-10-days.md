---
layout: course
title: "PHP in 10 Days — Hands-On"
permalink: /courses/php-10-days/
course_track: "PHP"
description: "Modern PHP 8: types, Composer, and a tiny JSON API without a heavy framework."
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

Modern PHP 8: types, Composer, and a tiny JSON API without a heavy framework.

## Why this language
{: #why-this-language }

PHP still runs a huge share of the web. Modern PHP is typed, fast, and pleasant with Composer.

## Setup (Day 0)
{: #setup-day-0 }

```bash
php -v   # 8.1+
mkdir php-lab && cd php-lab
```

---

## Day 1: Hello PHP
{: #day-1-hello-php }

### What you'll learn

- <?php
- echo
- vars

### Code along

```php
<?php
$name = "PHP";
echo "Hello, $name\n";
```

### Your task

Print CLI args from `$argv`.

---

## Day 2: Types & functions
{: #day-2-types-functions }

### What you'll learn

- type hints
- return types
- strict_types

### Code along

```php
<?php
declare(strict_types=1);
function add(int $a, int $b): int { return $a + $b; }
echo add(2, 3);
```

### Your task

Write `clamp(float $x, float $lo, float $hi): float`.

---

## Day 3: Arrays
{: #day-3-arrays }

### What you'll learn

- lists
- assoc
- foreach

### Code along

```php
<?php
$m = ["a" => 1, "b" => 2];
foreach ($m as $k => $v) echo "$k=$v\n";
```

### Your task

Word frequency array.

---

## Day 4: Classes
{: #day-4-classes }

### What you'll learn

- constructor
- props
- methods

### Code along

```php
<?php
class User {
  public function __construct(public string $name) {}
  public function greet(): string { return "Hi {$this->name}"; }
}
```

### Your task

BankAccount class.

---

## Day 5: Composer
{: #day-5-composer }

### What you'll learn

- composer.json
- autoload
- vendor

### Code along

```php
{
  "name": "lab/php",
  "autoload": { "psr-4": { "Lab\\": "src/" } }
}
```

### Your task

PSR-4 class Lab\\Math\\Add and require vendor/autoload.php.

---

## Day 6: Exceptions
{: #day-6-exceptions }

### What you'll learn

- try/catch
- throw
- custom

### Code along

```php
<?php
try {
  throw new RuntimeException("boom");
} catch (Throwable $e) {
  fwrite(STDERR, $e->getMessage());
}
```

### Your task

Parse int helper that throws on bad input.

---

## Day 7: Files & JSON
{: #day-7-files-json }

### What you'll learn

- file_get_contents
- json_encode
- JSON_THROW_ON_ERROR

### Code along

```php
<?php
$data = ["ok" => true];
file_put_contents("out.json", json_encode($data, JSON_PRETTY_PRINT));
```

### Your task

Read JSON file into array; print a field.

---

## Day 8: Built-in server
{: #day-8-built-in-server }

### What you'll learn

- php -S
- router script
- superglobals

### Code along

```php
<?php
// router.php
if ($_SERVER["REQUEST_URI"] === "/health") {
  header("Content-Type: application/json");
  echo json_encode(["ok" => true]);
  return true;
}
return false;
```

### Your task

`php -S localhost:8000 router.php` and hit /health.

---

## Day 9: PDO lite
{: #day-9-pdo-lite }

### What you'll learn

- SQLite PDO
- prepare
- execute

### Code along

```php
<?php
$pdo = new PDO("sqlite::memory:");
$pdo->exec("CREATE TABLE t(id INTEGER PRIMARY KEY, name TEXT)");
$pdo->prepare("INSERT INTO t(name) VALUES (?)")->execute(["Ada"]);
```

### Your task

Create todos table; insert and list rows.

---

## Day 10: Mini JSON API
{: #day-10-mini-json-api }

### What you'll learn

- POST body
- status codes
- routing

### Code along

```php
<?php
// extend router: POST /todos reads php://input JSON and appends to file store
```

### Your task

Implement GET/POST /todos with a JSON file store.


---

## Capstone project
{: #capstone }

Ship a **PHP todo JSON API** on the built-in server with Composer autoload, typed classes, and SQLite or file persistence.

## Related

- [SQL in 10 Days](/courses/sql-10-days/)
- [JavaScript in 10 Days](/courses/javascript-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
