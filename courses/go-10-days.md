---
layout: course
title: "Go in 10 Days — Hands-On"
permalink: /courses/go-10-days/
course_track: "Go"
description: "Idiomatic Go: packages, interfaces, concurrency, and a tiny HTTP API."
toc:
  - id: "day-1-packages-fmt"
    label: "Day 1: Packages & fmt"
  - id: "day-2-structs-methods"
    label: "Day 2: Structs & methods"
  - id: "day-3-interfaces"
    label: "Day 3: Interfaces"
  - id: "day-4-slices-maps"
    label: "Day 4: Slices & maps"
  - id: "day-5-errors"
    label: "Day 5: Errors"
  - id: "day-6-goroutines-channels"
    label: "Day 6: Goroutines & channels"
  - id: "day-7-testing"
    label: "Day 7: Testing"
  - id: "day-8-http-server"
    label: "Day 8: HTTP server"
  - id: "day-9-context-timeouts"
    label: "Day 9: Context & timeouts"
  - id: "day-10-small-module-layout"
    label: "Day 10: Small module layout"
  - id: "capstone"
    label: "Capstone project"
---

# Go in 10 Days — Hands-On

Idiomatic Go: packages, interfaces, concurrency, and a tiny HTTP API.

## Why this language
{: #why-this-language }

Go is the language of cloud services, CLIs, and Kubernetes-adjacent tooling. Simple, fast to ship.

## Setup (Day 0)
{: #setup-day-0 }

```bash
go version   # 1.21+
mkdir go-lab && cd go-lab
go mod init example.com/golab
```

---

## Day 1: Packages & fmt
{: #day-1-packages-fmt }

### What you'll learn

- `package main`
- go run
- Variables

### Code along

```go
package main
import "fmt"
func main() {
  name := "Go"
  fmt.Printf("Hello, %s\n", name)
}
```

### Your task

Print args from `os.Args`.

---

## Day 2: Structs & methods
{: #day-2-structs-methods }

### What you'll learn

- Structs
- Pointers
- Methods

### Code along

```go
type User struct{ Name string; Age int }
func (u User) Greet() string { return "Hi " + u.Name }
func main() { fmt.Println(User{"Ada", 36}.Greet()) }
```

### Your task

BankAccount with Deposit/Withdraw methods.

---

## Day 3: Interfaces
{: #day-3-interfaces }

### What you'll learn

- Implicit interfaces
- error
- io.Reader mindset

### Code along

```go
type Speaker interface{ Speak() string }
type Dog struct{}
func (Dog) Speak() string { return "woof" }
func say(s Speaker) { fmt.Println(s.Speak()) }
func main() { say(Dog{}) }
```

### Your task

Shape interface with Area(); Circle and Rect.

---

## Day 4: Slices & maps
{: #day-4-slices-maps }

### What you'll learn

- Append
- Range
- Maps

### Code along

```go
m := map[string]int{"a": 1}
m["b"] = 2
for k, v := range m { fmt.Println(k, v) }
```

### Your task

Word frequency counter over a string.

---

## Day 5: Errors
{: #day-5-errors }

### What you'll learn

- `error` values
- Wrapping
- sentinel errors

### Code along

```go
func parse(s string) (int, error) {
  var n int
  _, err := fmt.Sscanf(s, "%d", &n)
  return n, err
}
```

### Your task

Read a file; return wrapped errors with `%w`.

---

## Day 6: Goroutines & channels
{: #day-6-goroutines-channels }

### What you'll learn

- go keyword
- chan
- select intro

### Code along

```go
ch := make(chan string)
go func() { ch <- "ping" }()
fmt.Println(<-ch)
```

### Your task

Fan-out: 3 goroutines fetch fake work; collect results.

---

## Day 7: Testing
{: #day-7-testing }

### What you'll learn

- `_test.go`
- table tests
- go test

### Code along

```go
func Add(a, b int) int { return a + b }
// add_test.go
func TestAdd(t *testing.T) {
  if Add(2, 3) != 5 { t.Fatal("nope") }
}
```

### Your task

Table-driven tests for a Clamp function.

---

## Day 8: HTTP server
{: #day-8-http-server }

### What you'll learn

- net/http
- handlers
- JSON

### Code along

```go
http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
  w.Write([]byte(`{"ok":true}`))
})
log.Fatal(http.ListenAndServe(":8080", nil))
```

### Your task

Add POST /echo that returns the JSON body.

---

## Day 9: Context & timeouts
{: #day-9-context-timeouts }

### What you'll learn

- context.Context
- WithTimeout
- Cancel

### Code along

```go
ctx, cancel := context.WithTimeout(context.Background(), time.Second)
defer cancel()
select {
case <-time.After(2 * time.Second):
case <-ctx.Done():
  fmt.Println(ctx.Err())
}
```

### Your task

HTTP handler that respects request context cancellation.

---

## Day 10: Small module layout
{: #day-10-small-module-layout }

### What you'll learn

- internal/
- cmd/
- go test ./...

### Code along

```go
// layout: cmd/api/main.go + internal/store/store.go
package store
type Mem struct{ data map[string]string }
func New() *Mem { return &Mem{data: map[string]string{}} }
```

### Your task

Split yesterday’s API into cmd + internal packages.


---

## Capstone project
{: #capstone }

Build a **URL shortener API** in Go: in-memory store, POST create, GET redirect, tests for the store, README with curl examples. Then compare with the [Golang Bootcamp](/courses/golang-bootcamp/).

## Related

- [Golang Bootcamp](/courses/golang-bootcamp/)
- [Rust in 10 Days](/courses/rust-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
