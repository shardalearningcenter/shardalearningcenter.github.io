---
layout: course
title: "Ruby in 10 Days — Hands-On"
permalink: /courses/ruby-10-days/
course_track: "Ruby"
description: "Blocks, Enumerable, and modules — build a working Ruby CLI, one concept at a time."
toc:
  - id: "day-1-hello-ruby"
    label: "Day 1: Hello Ruby"
  - id: "day-2-arrays-hashes"
    label: "Day 2: Arrays & hashes"
  - id: "day-3-methods-blocks"
    label: "Day 3: Methods & blocks"
  - id: "day-4-enumerable"
    label: "Day 4: Enumerable"
  - id: "day-5-classes"
    label: "Day 5: Classes"
  - id: "day-6-modules-mixins"
    label: "Day 6: Modules & mixins"
  - id: "day-7-file-io"
    label: "Day 7: File I/O"
  - id: "day-8-exceptions"
    label: "Day 8: Exceptions"
  - id: "day-9-gems-bundler"
    label: "Day 9: Gems & Bundler"
  - id: "day-10-tiny-web-sketch"
    label: "Day 10: Tiny web sketch"
  - id: "capstone"
    label: "Capstone project"
---

# Ruby in 10 Days — Hands-On

Blocks, Enumerable, and modules — build a working Ruby CLI, one concept at a time.

## Why this language
{: #why-this-language }

Ruby is still the language behind a large share of DevOps tooling (Chef, Vagrant, Homebrew's older internals) and, through Rails, a huge number of production web apps — and it's worth learning on its own merits, not just as "the Rails language." Blocks and `Enumerable` are Ruby's signature feature: almost every collection operation reads as a short, composable pipeline, and once you're fluent in them, picking up Rails-specific conventions later is a much smaller jump.

## Setup (Day 0)
{: #setup-day-0 }

```bash
ruby -v
gem install bundler
mkdir ruby-lab && cd ruby-lab
```

Every snippet below runs directly with `ruby filename.rb` — no build step, no project scaffolding needed until Day 9.

---

## Day 1: Hello Ruby
{: #day-1-hello-ruby }

### Why it matters

`puts`, variable assignment, and string interpolation are what every single Ruby file starts from — scripts, Rake tasks, Rails controllers all sit on top of the exact same fundamentals you're using today.

### Mental model

Ruby variables aren't declared with a type or a keyword — assignment (`name = "Ruby"`) both creates and binds the variable. Everything is an object, including integers and `nil`, which is why methods like `.upcase` work directly on a string literal. String interpolation only works inside double-quoted strings (`"#{expr}"`); single-quoted strings are literal and won't interpolate — a distinction that trips up people coming from languages where quote style is purely cosmetic.

### Code along

```ruby
greeting = "Hello"
visit_count = 0

target = ARGV[0] || "world"
visit_count += 1

puts "#{greeting}, #{target}!"
puts "Visits this run: #{visit_count}"
puts "Uppercased: #{target.upcase}"
```

Run with `ruby hello.rb Ada`. `ARGV` is a plain array of the arguments after the script name — unlike C-family languages, there's no `argv[0]` slot for the program name to skip past.

### Common mistake

Writing `'Hello, #{name}'` with single quotes and being confused when it prints the literal text `#{name}` instead of the interpolated value. Single-quoted strings in Ruby do almost no escape processing at all — switch to double quotes any time you need interpolation or escape sequences like `\n`.

### Your task

Change the script to fall back to `gets.chomp` (reading a line from standard input) when no `ARGV[0]` is given, instead of defaulting to `"world"`. Print a friendly error and `exit 1` if the input is empty after `.strip`.

**Check:** `echo "Ada" | ruby hello.rb` prints `Hello, Ada!` and `Visits this run: 1`; `printf "" | ruby hello.rb` (empty input) prints a friendly error and `echo $?` afterward shows `1`.

---

## Day 2: Arrays & hashes
{: #day-2-arrays-hashes }

### Why it matters

Arrays and hashes are Ruby's two workhorse collections, and symbols (`:key`, as opposed to `"key"` strings) as hash keys are idiomatic Ruby you'll see in essentially every codebase — knowing why symbols are preferred for keys (and when they're not appropriate) is a small but constant habit.

### Mental model

A `Hash` in modern Ruby preserves *insertion order* when you iterate it — this is a language guarantee, not an implementation detail, unlike several other languages where hash/dictionary order is unspecified. Symbols (`:name`) are immutable, interned identifiers — comparing two `:name` symbols is an identity check under the hood, faster than comparing two separate string objects with equal contents, which is why they're the default choice for hash keys that represent fixed, known field names.

### Code along

```ruby
person = { name: "Ada", age: 36, active: true }

person.each { |key, value| puts "#{key} = #{value}" }

puts person[:name]
puts person.key?(:email)

numbers = [3, 1, 4, 1, 5, 9, 2, 6]
puts numbers.first(3).inspect
puts numbers.last(2).inspect
puts numbers.sort.inspect
puts numbers.uniq.inspect
```

`person.each { |key, value| ... }` destructures each key/value pair directly into block parameters — this pattern (`{ |a, b| ... }`) shows up constantly once you start using `Enumerable` methods tomorrow.

### Common mistake

Mixing `:name` (symbol) and `"name"` (string) as hash keys and expecting `person["name"]` to find what was stored as `person[name: ...]`. Symbols and strings are different objects and different keys — `{ name: "Ada" }[:name]` works, `{ name: "Ada" }["name"]` returns `nil`. Pick one key style per hash and stay consistent; symbols are the idiomatic default for fixed field names.

### Your task

Given a sentence split into words, build a `Hash` mapping each distinct word to how many times it appears (a manual word-count, without using `tally` yet — that's tomorrow's shortcut), then print the three most frequent words.

**Check:** using `"the quick brown fox jumps over the lazy dog the fox runs"`, the printed top words start `the -> 3`, `fox -> 2` — every remaining word ties at count `1`, so only those first two entries are guaranteed in a specific order.

---

## Day 3: Methods & blocks
{: #day-3-methods-blocks }

### Why it matters

Blocks are the mechanism behind essentially every Ruby idiom that looks like a built-in language feature but is actually just a method call — `3.times { }`, `each`, `map` — and `yield` is how you write your own methods that accept a block the same way.

### Mental model

A block is an anonymous chunk of code passed to a method, invoked inside that method via `yield` (with or without arguments). `yield` can be called multiple times, zero times, or conditionally — the method controls exactly when and how often the block runs, which is the core idea behind patterns like "run this, but also do setup/teardown around it" (a precursor to Ruby's `ensure`, covered on Day 8).

### Code along

```ruby
def twice
  yield
  yield
end

def with_timing
  start = Time.now
  result = yield
  elapsed = ((Time.now - start) * 1000).round(2)
  puts "took #{elapsed}ms"
  result
end

def once
  ran = false
  -> {
    return if ran
    ran = true
    yield
  }
end

twice { puts "hi" }

with_timing { sleep(0.05); puts "work done" }

action = once { puts "ran!" }
action.call
action.call
action.call
```

`once` returns a lambda that closes over the local `ran` flag — calling the returned lambda multiple times demonstrates the flag persisting across calls, since the lambda and `ran` share the same enclosing scope.

### Common mistake

Defining a method with `yield` but calling it with no block at all — `twice` (no braces) instead of `twice { ... }` — which raises `LocalJumpError: no block given`. If a method should tolerate being called without a block, guard with `yield if block_given?` rather than assuming a block is always present.

### Your task

Write a method `def retry_times(n)` that calls the given block up to `n` times, stopping as soon as the block returns a truthy value (returning that value), or returning `nil` if all `n` attempts return falsy. Demonstrate it with a block that "succeeds" only on its third call (track attempts in a counter outside the block).

**Check:** `retry_times(5) { attempts += 1; attempts == 3 ? "success" : false }` returns `"success"`, and `attempts` ends at exactly `3` — not `5` — proving `retry_times` stopped immediately once the block succeeded instead of always running all `n` attempts.

---

## Day 4: Enumerable
{: #day-4-enumerable }

### Why it matters

`Enumerable` (`map`, `select`, `reduce`, `sort_by`, `group_by`, `tally`) is the module that makes Ruby collection code so compact — instead of writing a loop with an accumulator variable for every transformation, you compose a handful of well-named methods, and the intent reads directly from the method names.

### Mental model

Every `Enumerable` method returns a *new* collection (or a single value for `reduce`/`sum`) — none of them mutate the receiver. `sort_by { |x| key }` sorts by a computed key without you writing a custom comparator; `group_by { |x| key }` partitions elements into a `Hash` of `key => [elements]`; `tally` is the shortcut for "count occurrences of each element" that Day 2's manual hash-building was building up to.

### Code along

```ruby
words = %w[ruby python go rust ruby swift go go]

counts = words.tally
counts.sort_by { |_word, count| -count }.each do |word, count|
  puts "#{word} -> #{count}"
end

by_length = words.uniq.group_by(&:length)
puts by_length.inspect

total_letters = words.sum(&:length)
puts "total letters across distinct words: #{words.uniq.sum(&:length)}, total: #{total_letters}"

evens_squared = (1..10).select(&:even?).map { |n| n**2 }
puts evens_squared.inspect
```

`&:length` and `&:even?` convert a symbol into a block via `Symbol#to_proc` — `words.uniq.group_by(&:length)` is shorthand for `words.uniq.group_by { |w| w.length }`, and you'll see this `&:method_name` shorthand constantly in real Ruby code.

### Common mistake

Calling `words.sort_by { |word, count| -count }` on the *array* `words` (a flat list of strings) as if it were already the tallied pairs, forgetting to call `.tally` first — this either raises an error or silently produces nonsense, depending on the exact method, because `sort_by`'s block receives one array element at a time, not a key/value pair, unless the receiver is already a hash-like structure of pairs.

### Your task

Given `sentence = "the quick brown fox jumps over the lazy dog the fox runs"`, split it into words, then use `Enumerable` methods (no manual loops with accumulator variables) to print: the top 3 most frequent words with counts, and a hash grouping distinct words by length.

**Check:** the frequency output starts `the -> 3`, `fox -> 2` (everything else ties at `1`). The length hash has exactly three keys, `3`, `4`, and `5` — key `3` is `["the", "fox", "dog"]`, key `4` is `["over", "lazy", "runs"]`, key `5` is `["quick", "brown", "jumps"]`, in that order (`uniq` preserves first-occurrence order, and `group_by` preserves it within each key).

---

## Day 5: Classes
{: #day-5-classes }

### Why it matters

Classes with `initialize`, `attr_reader`/`attr_accessor`, and plain instance methods are how you model anything with both data and behavior in Ruby — understanding the difference between exposing a getter (`attr_reader`) and exposing a getter *and* setter (`attr_accessor`) is a small habit that protects your invariants.

### Mental model

`initialize` is the constructor, called automatically by `ClassName.new(...)`. `attr_reader :name` generates a read-only getter method; `attr_accessor :name` generates both a getter and a setter — choose `attr_reader` by default and only add a setter (or a custom method) when external mutation is genuinely intended and safe.

### Code along

```ruby
class BankAccount
  attr_reader :owner, :balance_cents

  def initialize(owner, opening_cents = 0)
    @owner = owner
    @balance_cents = opening_cents
  end

  def deposit(cents)
    raise ArgumentError, "deposit must be positive" unless cents > 0
    @balance_cents += cents
  end

  def withdraw(cents)
    return false if cents <= 0 || cents > @balance_cents
    @balance_cents -= cents
    true
  end

  def to_s
    "#{@owner}: #{@balance_cents} cents"
  end
end

account = BankAccount.new("Ada", 5000)
account.deposit(2000)
puts account.withdraw(1000)
puts account.withdraw(999_999)
puts account
```

Overriding `to_s` is what makes `puts account` print a readable summary instead of Ruby's default `#<BankAccount:0x...>` object-id representation — worth doing on almost any class you expect to print or log.

### Common mistake

Using `attr_accessor :balance_cents` instead of `attr_reader` "for convenience," which lets any code anywhere do `account.balance_cents = 999_999_999` directly, completely bypassing `deposit`/`withdraw` and any validation they perform. Expose mutation only through methods that can enforce your invariants — a public setter for internal state defeats the purpose of having those methods at all.

### Your task

Add a `@history` array to `BankAccount`, recording a short string for every deposit/withdrawal (e.g. `"deposit 2000"`), and a `def statement` method that prints each entry followed by the running balance after it.

**Check:** for the exact sequence in the code above (opening `5000`, `deposit(2000)` → `7000`, `withdraw(1000)` succeeds → `6000`, `withdraw(999_999)` fails), `statement` prints exactly **two** entries (the failed withdrawal must not appear), and the balance shown after the second entry is `6000`, matching `account.balance_cents`.

---

## Day 6: Modules & mixins
{: #day-6-modules-mixins }

### Why it matters

Ruby doesn't have multiple inheritance, but `module` plus `include` gives you the practical equivalent — shared behavior mixed into unrelated classes — which is how the standard library itself adds `Enumerable` and `Comparable` to your own classes with almost no code on your part.

### Mental model

A `module` groups methods and constants without being instantiable on its own. `include SomeModule` inserts the module into a class's ancestor chain, so its instance methods become available on instances of that class as if they'd been defined there directly. `extend SomeModule` does the analogous thing but adds the methods as *class-level* (singleton) methods instead of instance methods — a subtle but important distinction.

### Code along

```ruby
module Loggable
  def log(message)
    puts "[#{self.class}] #{Time.now.strftime('%H:%M:%S')} #{message}"
  end
end

module Describable
  def describe
    "#{self.class.name} with #{instance_variables.length} attribute(s)"
  end
end

class Task
  include Loggable
  include Describable

  def initialize(title)
    @title = title
    log("created: #{title}")
  end
end

task = Task.new("Write Ruby course")
puts task.describe
task.log("marked complete")
```

`self.class` inside `Loggable#log` refers to whatever class actually included the module (`Task`, here) — the module's code stays generic and reusable across any class that includes it, which is the entire point of a mixin over copy-pasting the method into each class.

### Common mistake

Reaching for a deep class hierarchy (`class SpecialTask < Task < BaseTask`) to share behavior that's really orthogonal — logging, comparability, serializability — rather than mixing in a focused module. Deep inheritance chains couple unrelated concerns together and make it hard to reuse just *one* piece of behavior elsewhere; small, focused modules included where needed are the more idiomatic Ruby answer.

### Your task

Write a module `Timestamped` providing `def touch` that sets `@updated_at = Time.now` and `def updated_at` returning it, mix it into `Task`, and confirm `updated_at` changes after calling `touch` on an instance.

**Check:** immediately after `Task.new(...)`, `task.updated_at` is `nil` (nothing has called `touch` yet); calling `task.touch` then `task.updated_at` returns a real `Time` that's later than the object's creation time; calling `sleep(1); task.touch` again produces a strictly later `updated_at` than the first call.

---

## Day 7: File I/O
{: #day-7-file-io }

### Why it matters

Reading and writing files is a constant in real scripts — config loading, log processing, simple data persistence — and Ruby's `File` API has both convenient whole-file methods and streaming ones; knowing when to reach for each avoids loading gigabyte files entirely into memory by accident.

### Mental model

`File.write`/`File.read` are whole-file convenience methods, fine for small files. `File.open(path, mode) { |f| ... }` (block form) guarantees the file handle is closed automatically when the block ends, even if an exception is raised inside — Ruby's equivalent of Kotlin's `use { }` or Swift's automatic `Closeable` cleanup, just via block scoping instead of a language keyword.

### Code along

```ruby
LOG_PATH = "activity.log"

def append_log(message)
  File.open(LOG_PATH, "a") do |file|
    file.puts("#{Time.now.strftime('%Y-%m-%d %H:%M:%S')} #{message}")
  end
end

append_log("server started")
append_log("request handled")
append_log("server stopped")

lines = File.readlines(LOG_PATH)
puts "Log has #{lines.size} lines:"
lines.each { |line| print "  #{line}" }
```

The `"a"` mode is append, not the default (truncating) write mode — run the script twice and the line count should grow by 3 each time, confirming append semantics rather than overwrite.

### Common mistake

Opening a file with `File.open(path, "w")` (or plain `File.write`) when you actually meant to append, and being confused why previous runs' data disappeared. `"w"` truncates the file to empty before writing; `"a"` appends to the end. This single-character mode difference is responsible for a lot of "where did my data go" bug reports.

### Your task

Add a method `def tail_log(n)` that prints only the last `n` lines of the log file (use `File.readlines(LOG_PATH).last(n)`), and call it after appending 5 new entries to show just the most recent 3.

**Check:** append 5 new entries in one run (say `"event 1"` through `"event 5"`), then `tail_log(3)` prints exactly `"event 3"`, `"event 4"`, and `"event 5"` — the last 3 of the 5 you just added, not the first 3 and not all 5.

---

## Day 8: Exceptions
{: #day-8-exceptions }

### Why it matters

`begin`/`rescue`/`ensure` is how Ruby represents recoverable failure, and `ensure` in particular guarantees cleanup code runs whether the block succeeded, failed, or even returned early — critical for anything holding a resource (files, network connections, locks) that must be released no matter what.

### Mental model

`rescue SpecificError => e` catches only that error class (and subclasses); a bare `rescue` without a class catches `StandardError` and its descendants — deliberately *not* every possible exception (some, like `SystemExit`, are meant to propagate). `ensure` runs after the `begin` block completes or raises, always, similar to `finally` in Java/C#/JavaScript. `raise` re-throws or throws a new exception, optionally with a custom message or exception class.

### Code along

```ruby
class ValidationError < StandardError; end

def validate_fields(fields)
  errors = []
  errors << "name is required" if fields[:name].to_s.strip.empty?
  errors << "age must be a positive number" unless fields[:age].to_i > 0
  raise ValidationError, errors.join(", ") unless errors.empty?
  true
end

[
  { name: "Ada", age: "34" },
  { name: "", age: "34" },
  { name: "Grace", age: "-5" }
].each do |fields|
  begin
    validate_fields(fields)
    puts "#{fields.inspect} -> valid"
  rescue ValidationError => e
    puts "#{fields.inspect} -> invalid: #{e.message}"
  ensure
    puts "  (checked at #{Time.now.strftime('%H:%M:%S')})"
  end
end
```

The `ensure` block runs for every iteration regardless of whether `validate_fields` raised — that's the detail worth confirming by reading the output line-by-line rather than skimming it.

### Common mistake

Using a bare `rescue` (or `rescue Exception`) around a large block of code "to be safe," which swallows programming errors like `NoMethodError` from a typo alongside genuine, expected failures — you lose the crash report that would have told you about a real bug. Rescue the specific exception classes you actually expect and know how to handle; let everything else propagate so it's visible.

### Your task

Extend `validate_fields` to also reject an `:age` field that isn't numeric at all (e.g. `"old"`) with a clear message ("age must be a number"), distinct from the "must be positive" case, and add a test hash that triggers it.

**Check:** `validate_fields(name: "Grace", age: "old")` raises `ValidationError` with a message containing `"age must be a number"` — a different message than `validate_fields(name: "Grace", age: "-5")`'s `"age must be a positive number"`, proving the two failure modes are now distinguishable.

---

## Day 9: Gems & Bundler
{: #day-9-gems-bundler }

### Why it matters

Almost no real Ruby project has zero dependencies — Bundler pins exact gem versions in a `Gemfile.lock`, which is what makes "works on my machine" reproducible across teammates and CI, instead of everyone silently running slightly different library versions.

### Mental model

`Gemfile` declares which gems and version constraints your project needs; `bundle install` resolves and locks exact versions into `Gemfile.lock`; `bundle exec` runs a command using exactly the gems your lockfile specifies, rather than whatever happens to be globally installed — always prefer `bundle exec ruby script.rb` over a bare `ruby script.rb` once a project has a `Gemfile`.

### Code along

`Gemfile`:

```ruby
source "https://rubygems.org"

gem "json"
```

Then run:

```bash
bundle install
```

`use_gems.rb`:

```ruby
require "json"

data = {
  name: "Ruby Lab",
  gems: ["json"],
  created_at: Time.now.strftime("%Y-%m-%d")
}

puts JSON.pretty_generate(data)

parsed = JSON.parse(JSON.generate(data))
puts "Round-tripped name: #{parsed['name']}"
```

Run with `bundle exec ruby use_gems.rb`. `json` ships with modern Ruby's standard library already, so this example works even without Bundler — the point is the *workflow* (`Gemfile` → `bundle install` → `bundle exec`), which is identical for a gem that genuinely isn't bundled, like `httparty` or `rspec`.

### Common mistake

Committing a `Gemfile` but not `Gemfile.lock` to version control, or editing `Gemfile.lock` by hand. The lockfile is what pins exact resolved versions for every teammate and every CI run — without it, `bundle install` re-resolves versions each time and you lose the entire reproducibility guarantee Bundler exists to provide. Always commit the lockfile for applications (libraries/gems are the one exception, by convention).

### Your task

Add `gem "rspec"` to the `Gemfile`, run `bundle install`, then write a one-file spec (`spec/sample_spec.rb`) testing the `BankAccount` class from Day 5 — at minimum, a deposit increases the balance and a withdrawal beyond the balance returns `false` without changing it. Run it with `bundle exec rspec`.

**Check:** `bundle exec rspec` reports `2 examples, 0 failures` (or more, if you added extras) — and deliberately breaking `withdraw` (e.g. removing the balance check) makes that same command report a failure with a clear diff, proving the spec actually exercises the behavior instead of trivially passing.

---

## Day 10: Tiny web sketch
{: #day-10-tiny-web-sketch }

### Why it matters

Standing up a minimal HTTP server without a full framework demystifies what Rails/Sinatra actually do underneath — routing a request path to a handler and writing a response body — which makes debugging real framework behavior later far less mysterious.

### Mental model

`WEBrick::HTTPServer` (Ruby's standard-library HTTP server, fine for local tools and learning, not for production traffic) lets you `mount_proc(path) { |req, res| ... }` to handle a specific route. `req.request_method` tells you GET vs POST vs DELETE; `res.body =` sets the response, and `res.status =` sets the HTTP status code — everything a real framework's routing layer does, just written out explicitly.

### Code along

```ruby
require "webrick"
require "json"

todos = []

server = WEBrick::HTTPServer.new(Port: 8000)

server.mount_proc("/health") do |_req, res|
  res["Content-Type"] = "application/json"
  res.body = { ok: true }.to_json
end

server.mount_proc("/todos") do |req, res|
  res["Content-Type"] = "application/json"
  case req.request_method
  when "GET"
    res.body = todos.to_json
  when "POST"
    body = JSON.parse(req.body)
    todos << body["text"]
    res.status = 201
    res.body = { added: body["text"] }.to_json
  else
    res.status = 405
    res.body = { error: "method not allowed" }.to_json
  end
end

trap("INT") { server.shutdown }
puts "Listening on http://localhost:8000"
server.start
```

Start it with `ruby server.rb`, then from another terminal: `curl http://localhost:8000/health`, `curl -X POST http://localhost:8000/todos -d '{"text":"buy milk"}'`, `curl http://localhost:8000/todos`.

### Common mistake

Forgetting `trap("INT") { server.shutdown }` and then having to kill the process forcefully (or leave it occupying the port) every time you want to stop it during development — `Ctrl-C` without a registered `INT` handler doesn't let WEBrick clean up its listening socket gracefully, which can leave the port briefly unusable for the next run.

### Your task

Add a `DELETE /todos/:index`-style route (WEBrick's basic `mount_proc` doesn't parse path parameters for you, so match on a prefix like `/todos/` and parse the trailing segment yourself) that removes a todo by position, returning `404` if the index is invalid.

**Check:** after two `POST`s, `curl -X DELETE http://localhost:8000/todos/0 -w '%{http_code}'` succeeds and a follow-up `GET /todos` shows only the second todo remaining; `curl -X DELETE http://localhost:8000/todos/9 -w '%{http_code}'` (out of range) prints `404`.

---

## Capstone project
{: #capstone }

Build a **Ruby todo CLI** that draws on the whole week:

- `class Todo` with `attr_reader` for `id`/`text`/`done` and a method to toggle completion — Day 5.
- A `Persistence` module mixed into your store class, handling `File.open(..., "a")`/`File.readlines` so the storage logic isn't tangled with the todo logic itself — Days 6–7.
- `begin/rescue/ensure` around file operations, with a custom `StoreError` raised on a corrupt or unreadable store file — Day 8.
- `Enumerable` used for any listing/filtering (`todos.select(&:done)`, `todos.group_by(&:done)`) instead of manual loops — Day 4.
- A `Gemfile` even if the only dependency is `json`, run via `bundle exec` — Day 9.

Stretch goal: wrap `list`/`add` in the WEBrick sketch from Day 10, reusing your `Todo` class and store unchanged — if Day 6's module boundary is clean, this should be a small addition, not a rewrite.

**Acceptance check:** `bundle exec ruby cli.rb add "write course"`, `bundle exec ruby cli.rb done 0`, `bundle exec ruby cli.rb list` (three separate process invocations) shows one todo marked done — proving the `Persistence` module's file-backed store, not in-memory state, is carrying data across runs; corrupting the store file by hand and re-running raises your `StoreError` with a readable message instead of a raw `JSON::ParserError`.

## Related

- [Python in 10 Days](/courses/python-10-days/)
- [PHP in 10 Days](/courses/php-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
