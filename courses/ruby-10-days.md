---
layout: course
title: "Ruby in 10 Days — Hands-On"
permalink: /courses/ruby-10-days/
course_track: "Ruby"
description: "Elegant Ruby for scripts and web — blocks, Enumerable, and a tiny Sinatra-shaped app."
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

Elegant Ruby for scripts and web — blocks, Enumerable, and a tiny Sinatra-shaped app.

## Why this language
{: #why-this-language }

Ruby remains beloved for developer happiness, DevOps scripts, and Rails ecosystems.

## Setup (Day 0)
{: #setup-day-0 }

```bash
ruby -v
gem install bundler
mkdir ruby-lab && cd ruby-lab
```

---

## Day 1: Hello Ruby
{: #day-1-hello-ruby }

### What you'll learn

- puts
- vars
- string interp

### Code along

```ruby
name = "Ruby"
puts "Hello, #{name}"
```

### Your task

Read name from STDIN and greet.

---

## Day 2: Arrays & hashes
{: #day-2-arrays-hashes }

### What you'll learn

- []
- each
- symbols

### Code along

```ruby
h = { a: 1, b: 2 }
h.each { |k, v| puts "#{k}=#{v}" }
```

### Your task

Word count hash.

---

## Day 3: Methods & blocks
{: #day-3-methods-blocks }

### What you'll learn

- def
- yield
- blocks

### Code along

```ruby
def twice
  yield
  yield
end
twice { puts "hi" }
```

### Your task

Implement `once` with a block.

---

## Day 4: Enumerable
{: #day-4-enumerable }

### What you'll learn

- map/select/reduce
- grep
- sort_by

### Code along

```ruby
puts [1,2,3,4].select(&:even?).map { |n| n * n }
```

### Your task

Group words by length.

---

## Day 5: Classes
{: #day-5-classes }

### What you'll learn

- initialize
- attr_reader
- instance methods

### Code along

```ruby
class User
  attr_reader :name
  def initialize(name) = @name = name
  def greet = "Hi #{@name}"
end
```

### Your task

BankAccount class.

---

## Day 6: Modules & mixins
{: #day-6-modules-mixins }

### What you'll learn

- module
- include
- extend

### Code along

```ruby
module Greeter
  def greet = "Hi"
end
class Person
  include Greeter
end
```

### Your task

Mixin for logging timestamps.

---

## Day 7: File I/O
{: #day-7-file-io }

### What you'll learn

- File.read
- File.write
- each_line

### Code along

```ruby
File.write("out.txt", "hello")
puts File.read("out.txt")
```

### Your task

Count lines in a file path from ARGV.

---

## Day 8: Exceptions
{: #day-8-exceptions }

### What you'll learn

- begin/rescue
- raise
- ensure

### Code along

```ruby
begin
  Integer("x")
rescue ArgumentError => e
  warn e.message
end
```

### Your task

Validate a hash of form fields; collect errors.

---

## Day 9: Gems & Bundler
{: #day-9-gems-bundler }

### What you'll learn

- Gemfile
- bundle exec
- require

### Code along

```ruby
# Gemfile
# source "https://rubygems.org"
# gem "json"
```

### Your task

Create Gemfile; require json; pretty-print a hash.

---

## Day 10: Tiny web sketch
{: #day-10-tiny-web-sketch }

### What you'll learn

- WEBrick or Sinatra
- routes
- JSON

### Code along

```ruby
require "webrick"
server = WEBrick::HTTPServer.new(Port: 8000)
server.mount_proc("/health") { |_req, res| res.body = '{"ok":true}' }
trap("INT") { server.shutdown }
server.start
```

### Your task

Add /echo POST that returns body.


---

## Capstone project
{: #capstone }

Build a **Ruby todo CLI** with JSON persistence, then optionally wrap list/add in WEBrick routes.

## Related

- [Python in 10 Days](/courses/python-10-days/)
- [PHP in 10 Days](/courses/php-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
