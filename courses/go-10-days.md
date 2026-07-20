---
layout: course
title: "Go in 10 Days — Hands-On"
permalink: /courses/go-10-days/
course_track: "Go"
description: "Idiomatic Go: structs, interfaces, goroutines, and a real HTTP API — with the errors you'll hit along the way."
toc:
  - id: "why-this-language"
    label: "Why this language"
  - id: "setup-day-0"
    label: "Setup (Day 0)"
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

Idiomatic Go: packages, interfaces, concurrency, and a real HTTP API you build, test, and can `curl`.

## Why this language
{: #why-this-language }

Go is the language of cloud infrastructure — Docker, Kubernetes, Terraform are all written in it — because it compiles to a single static binary, starts instantly, and makes concurrency a first-class, approachable feature instead of an advanced topic. The language is deliberately small: no exceptions, no inheritance, no generics-heavy abstraction layers (generics exist but are used sparingly). That smallness is the point — a Go codebase written by ten different people tends to look like it was written by one disciplined person, because there's rarely more than one idiomatic way to do something.

## Setup (Day 0)
{: #setup-day-0 }

```bash
go version                          # expect go1.21 or higher
mkdir go-lab && cd go-lab
go mod init example.com/golab
```

Verify the toolchain builds and runs something:

```bash
cat > main.go <<'EOF'
package main
import "fmt"
func main() { fmt.Println("go is ready") }
EOF
go run main.go
```

Expected: `go is ready`. Delete this scratch `main.go` before Day 1 — each day below gets its own file under `cmd/dayNN/main.go`, which is idiomatic Go project layout (one `main` package per executable, under `cmd/`).

```bash
rm main.go
mkdir -p cmd
```

Run a given day with `go run ./cmd/dayNN`. **Checkpoint:** after creating `cmd/day01/main.go` with a minimal `package main; func main(){}`, `go run ./cmd/day01` should exit silently with no errors, confirming the layout is wired correctly.

---

## Day 1: Packages & fmt
{: #day-1-packages-fmt }

### Why this matters

Every Go file starts with a package declaration and every executable needs exactly one `func main()` in `package main`. Getting this — plus reading and printing values with `fmt` — solid on day one means every later day's compiler errors are about real logic, not boilerplate.

### Mental model

`:=` declares and infers type in one step; `var x int` declares with an explicit type and zero value if unassigned. Unused imports and unused local variables are **compile errors** in Go, not warnings — the compiler enforces tidiness so nobody argues about lint rules.

### Code along

```go
// cmd/day01/main.go
package main

import (
	"fmt"
	"os"
)

func main() {
	name := "Go"
	version := 1.22

	fmt.Printf("Hello, %s! (toolchain target %.2f)\n", name, version)

	args := os.Args[1:] // os.Args[0] is the binary path, always skip it
	if len(args) == 0 {
		fmt.Println("No arguments. Try: go run ./cmd/day01 foo bar")
		return
	}
	for i, arg := range args {
		fmt.Printf("arg[%d] = %s\n", i, arg)
	}
}
```

Run:

```bash
go run ./cmd/day01 foo bar
```

Expected output:

```
Hello, Go! (toolchain target 1.22)
arg[0] = foo
arg[1] = bar
```

### Common mistake

Importing `"os"` but forgetting to use it (or the reverse — using `os.Args` without importing `"os"`). Go gives a hard compile error either way: `imported and not used: "os"` or `undefined: os`. Unlike Python or JavaScript, there's no way to leave an unused import lying around "just in case" — this is intentional, and it's why `goimports`/`gofmt` (run `go fmt ./...` regularly) can safely auto-manage your import list without breaking anything.

### Your task

Print the arguments joined into a single sentence with `strings.Join`, and separately print the count using `len(args)`.

**Check:** `go run ./cmd/day01 buy milk` prints `arg[0] = buy` / `arg[1] = milk` as before, plus a line like `Joined: buy milk` and `Count: 2`.

---

## Day 2: Structs & methods
{: #day-2-structs-methods }

### Why this matters

Structs are Go's only way to group related data — there are no classes. Methods with pointer receivers vs value receivers is the single most important distinction to get right early: pick the wrong one and your mutations silently vanish.

### Mental model

A method with a value receiver (`func (u User) Method()`) operates on a **copy** — changes inside don't affect the original. A pointer receiver (`func (u *User) Method()`) operates on the real thing. Rule of thumb: if the method mutates state, use a pointer receiver; for consistency, once one method on a type uses a pointer receiver, make them all pointer receivers.

### Code along

```go
// cmd/day02/main.go
package main

import "fmt"

type BankAccount struct {
	Owner   string
	balance int // cents; unexported, package-private
}

func NewBankAccount(owner string, openingCents int) *BankAccount {
	return &BankAccount{Owner: owner, balance: openingCents}
}

func (a *BankAccount) Deposit(cents int) error {
	if cents <= 0 {
		return fmt.Errorf("deposit must be positive, got %d", cents)
	}
	a.balance += cents
	return nil
}

func (a *BankAccount) Withdraw(cents int) error {
	if cents > a.balance {
		return fmt.Errorf("insufficient funds: have %d, want %d", a.balance, cents)
	}
	a.balance -= cents
	return nil
}

func (a *BankAccount) Balance() int {
	return a.balance
}

func main() {
	acct := NewBankAccount("Ada", 10000)
	acct.Deposit(500)

	if err := acct.Withdraw(20000); err != nil {
		fmt.Println("withdraw failed:", err)
	}

	fmt.Printf("%s's balance: %d cents\n", acct.Owner, acct.Balance())
}
```

Expected output:

```
withdraw failed: insufficient funds: have 10500, want 20000
Ada's balance: 10500 cents
```

### Common mistake

Defining `Deposit` with a value receiver (`func (a BankAccount) Deposit(cents int)`) instead of a pointer receiver. The code compiles fine and runs with no error — that's what makes this dangerous. `a.balance += cents` modifies the *copy* passed into the method, and the original `acct` outside is completely unchanged after the call returns. You'd only notice when you print the balance later and it's wrong. Always use pointer receivers for methods that mutate.

### Your task

Add a `TransferTo(other *BankAccount, cents int) error` method that withdraws from the receiver and deposits into `other`, returning early with an error (and no state change to either account) if the withdrawal fails.

**Check:** transferring 300 cents from an account with 10500 to a fresh account with 0 leaves them at 10200 and 300 respectively; attempting to transfer more than the source has changes neither account's balance.

---

## Day 3: Interfaces
{: #day-3-interfaces }

### Why this matters

Go interfaces are satisfied implicitly — no `implements` keyword, no declared relationship between type and interface. This is what makes Go's standard library (`io.Reader`, `error`, `sort.Interface`) so composable: any type, from any package, automatically works with any interface it happens to match the shape of.

### Mental model

If a type has all the methods an interface requires, it satisfies that interface — full stop, no explicit declaration needed. This means you can define a small interface for exactly what *your* function needs, and any existing type (yours or from a third-party library) that happens to match just works, without that library needing to know your interface exists.

### Code along

```go
// cmd/day03/main.go
package main

import (
	"fmt"
	"math"
)

type Shape interface {
	Area() float64
	Perimeter() float64
}

type Circle struct {
	Radius float64
}

func (c Circle) Area() float64      { return math.Pi * c.Radius * c.Radius }
func (c Circle) Perimeter() float64 { return 2 * math.Pi * c.Radius }

type Rectangle struct {
	Width, Height float64
}

func (r Rectangle) Area() float64      { return r.Width * r.Height }
func (r Rectangle) Perimeter() float64 { return 2 * (r.Width + r.Height) }

func describe(s Shape) string {
	return fmt.Sprintf("area=%.2f perimeter=%.2f", s.Area(), s.Perimeter())
}

func main() {
	shapes := []Shape{
		Circle{Radius: 3},
		Rectangle{Width: 4, Height: 5},
	}
	for _, s := range shapes {
		fmt.Println(describe(s))
	}
}
```

Expected output:

```
area=28.27 perimeter=18.85
area=20.00 perimeter=38.00
```

### Common mistake

Defining `Area()` with a pointer receiver (`func (c *Circle) Area() float64`) but then trying to put a plain `Circle{}` value (not `&Circle{}`) into a `[]Shape`. The compile error is `Circle does not implement Shape (method Area has pointer receiver)` — a value type does not automatically satisfy an interface that only pointer-receiver methods implement, because the compiler can't silently take the address of a value stored in a slice for you in every context. Either use value receivers throughout (as above, for simple immutable-ish shapes) or consistently store pointers (`[]Shape{&Circle{...}}`).

### Your task

Add a `Triangle` type (base, height for `Area`; three side lengths for `Perimeter`) implementing `Shape`, and a function `totalArea(shapes []Shape) float64` summing all areas.

**Check:** adding a `Triangle{Base: 6, Height: 4, SideA: 5, SideB: 5, SideC: 6}` (area 12, perimeter 16) to the `shapes` slice makes `totalArea` return `60.27` (28.27 + 20.00 + 12.00) — verify by hand.

---

## Day 4: Slices & maps
{: #day-4-slices-maps }

### Why this matters

Slices and maps are Go's two workhorse collections. Understanding that slices share backing arrays (mutating one can affect another that overlaps) is one of the most common sources of subtle Go bugs — and one of the most common interview questions.

### Mental model

A slice is a view (pointer + length + capacity) into an underlying array — slicing an existing slice (`s[1:3]`) doesn't copy data, it shares memory with the original. `append` *may* allocate a new backing array if capacity is exceeded, or may not — never rely on whether it does. Maps have no guaranteed iteration order; sort keys explicitly if you need deterministic output.

### Code along

```go
// cmd/day04/main.go
package main

import (
	"fmt"
	"sort"
	"strings"
)

func wordFrequency(text string) map[string]int {
	freq := make(map[string]int)
	for _, word := range strings.Fields(strings.ToLower(text)) {
		freq[word]++
	}
	return freq
}

func topN(freq map[string]int, n int) []string {
	type pair struct {
		word  string
		count int
	}
	pairs := make([]pair, 0, len(freq))
	for w, c := range freq {
		pairs = append(pairs, pair{w, c})
	}
	sort.Slice(pairs, func(i, j int) bool {
		if pairs[i].count != pairs[j].count {
			return pairs[i].count > pairs[j].count
		}
		return pairs[i].word < pairs[j].word
	})
	result := make([]string, 0, n)
	for i := 0; i < n && i < len(pairs); i++ {
		result = append(result, fmt.Sprintf("%s:%d", pairs[i].word, pairs[i].count))
	}
	return result
}

func main() {
	text := "the quick brown fox jumps over the lazy dog the fox runs"
	freq := wordFrequency(text)
	fmt.Println(topN(freq, 3))
}
```

Expected output:

```
[the:3 fox:2 brown:1]
```

### Common mistake

Writing `freq[word] += 1` and assuming it panics or errors on a missing key — it doesn't. Go maps return the **zero value** for a missing key (`0` for `int`, `""` for `string`, `false` for `bool`), so `freq[word]++` on a brand-new word correctly starts it at 1. The actual common bug is the opposite assumption: forgetting that reading a missing key returns a zero value silently, and writing code that can't tell "key present with value 0" apart from "key absent" — when that distinction matters, check with the two-value form: `count, exists := freq[word]`.

### Your task

Write `averageWordLength(freq map[string]int) float64` — the average length of words weighted by frequency (a word appearing 3 times counts 3 times toward the average, not once).

**Check:** for the sample text, compute the expected value by hand (total characters across all word occurrences ÷ total word occurrences) and confirm your function's output matches to 2 decimal places.

---

## Day 5: Errors
{: #day-5-errors }

### Why this matters

Go has no exceptions — errors are ordinary return values, checked explicitly with `if err != nil`. This is verbose compared to `try`/`catch`, but it means every fallible call site is visible in the code, and nothing can fail silently past a forgotten `catch`.

### Mental model

By convention, error is always the **last** return value, and callers check it immediately after the call, before touching any other return value. `fmt.Errorf("...: %w", err)` wraps an error while preserving the original for `errors.Is`/`errors.As` — always prefer `%w` over `%v` when the underlying error might need to be inspected later.

### Code along

```go
// cmd/day05/main.go
package main

import (
	"errors"
	"fmt"
	"os"
)

var ErrNotFound = errors.New("record not found")

type Store struct {
	data map[string]string
}

func (s *Store) Get(key string) (string, error) {
	v, ok := s.data[key]
	if !ok {
		return "", fmt.Errorf("get %q: %w", key, ErrNotFound)
	}
	return v, nil
}

func loadConfig(path string) (map[string]string, error) {
	_, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("loading config from %s: %w", path, err)
	}
	return map[string]string{}, nil
}

func main() {
	store := &Store{data: map[string]string{"name": "Ada"}}

	if v, err := store.Get("name"); err == nil {
		fmt.Println("found:", v)
	}

	_, err := store.Get("missing")
	if errors.Is(err, ErrNotFound) {
		fmt.Println("expected miss:", err)
	}

	_, err = loadConfig("does-not-exist.json")
	if err != nil {
		fmt.Println("config error:", err)
	}
}
```

Expected output (the exact OS error text may vary slightly by platform):

```
found: Ada
expected miss: get "missing": record not found
config error: loading config from does-not-exist.json: open does-not-exist.json: no such file or directory
```

### Common mistake

Comparing wrapped errors with `==` instead of `errors.Is`: `if err == ErrNotFound` fails even when the underlying cause genuinely is `ErrNotFound`, because `fmt.Errorf("...: %w", err)` returns a **new** error value that wraps the original, not the original itself. `errors.Is` walks the wrap chain to find a match; plain `==` only checks the immediate value's identity. This is the single most common Go error-handling bug once a codebase starts wrapping errors for context (which it should).

### Your task

Add a `Delete(key string) error` method to `Store` that also returns `ErrNotFound` (wrapped with context) for a missing key, and a `main` block proving `errors.Is` correctly identifies both the `Get` and `Delete` misses as the same underlying `ErrNotFound`.

**Check:** `errors.Is(store.Delete("missing"), ErrNotFound)` prints `true`; after deleting an existing key, a subsequent `Get` on that key also returns an `ErrNotFound`-wrapped error.

---

## Day 6: Goroutines & channels
{: #day-6-goroutines-channels }

### Why this matters

Goroutines are Go's lightweight concurrency primitive — cheap enough to spawn thousands of them. Channels are how goroutines communicate safely without manual locks. Getting comfortable with the fan-out/collect pattern here is the foundation for every concurrent Go program you'll write.

### Mental model

`go f()` starts `f` running concurrently and returns immediately — it does **not** wait for `f` to finish. An unbuffered channel send blocks until a receiver is ready; use a buffered channel (`make(chan T, n)`) or `sync.WaitGroup` when you need to collect results from multiple goroutines without knowing exact timing.

### Code along

```go
// cmd/day06/main.go
package main

import (
	"fmt"
	"sync"
	"time"
)

func fetchWork(id int, results chan<- string, wg *sync.WaitGroup) {
	defer wg.Done()
	time.Sleep(time.Duration(id) * 10 * time.Millisecond) // simulate variable latency
	results <- fmt.Sprintf("worker %d done", id)
}

func main() {
	const numWorkers = 3
	results := make(chan string, numWorkers)
	var wg sync.WaitGroup

	start := time.Now()
	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		go fetchWork(i, results, &wg)
	}

	wg.Wait()
	close(results)

	var collected []string
	for r := range results {
		collected = append(collected, r)
	}

	fmt.Printf("collected %d results in %v\n", len(collected), time.Since(start).Round(10*time.Millisecond))
}
```

Expected output (exact duration varies, should be close to the slowest worker's delay, ~30ms, not the sum of all three):

```
collected 3 results in 30ms
```

### Common mistake

Forgetting `wg.Wait()` before `close(results)` and reading from the channel — `main()` returns as soon as its own goroutine finishes, potentially before any worker goroutine has sent a result, silently dropping all of them with **no error at all**. Go doesn't wait for background goroutines when `main` exits. This is the single most common concurrency bug for Go beginners: the program "works" (no crash) but produces incomplete or empty results, because nothing forced `main` to wait.

### Your task

Modify `fetchWork` so worker `2` simulates a failure (return an error string on the channel instead of a success message, don't panic). Update the collection loop to separate successes from failures and print counts of each.

**Check:** the output reports `2 succeeded, 1 failed` (or your chosen wording) after running, and the program still exits cleanly with no goroutine leak warnings (nothing hangs — `go run` should return to your shell promptly).

---

## Day 7: Testing
{: #day-7-testing }

### Why this matters

`go test` is built into the toolchain — no framework to install, no config to write. Table-driven tests are the idiomatic Go pattern for covering many input/output pairs concisely, and they're what you'll see in nearly every real Go codebase's test files.

### Mental model

Any file ending in `_test.go` is a test file, excluded from normal builds. `testing.T` gives you `t.Errorf` (report failure, keep running other checks in the same test) vs `t.Fatalf` (report and stop this test immediately) — prefer `Errorf` inside loops so one bad case doesn't hide others.

### Code along

```go
// internal/mathutil/clamp.go
package mathutil

func Clamp(x, lo, hi int) int {
	if x < lo {
		return lo
	}
	if x > hi {
		return hi
	}
	return x
}
```

```go
// internal/mathutil/clamp_test.go
package mathutil

import "testing"

func TestClamp(t *testing.T) {
	cases := []struct {
		name string
		x, lo, hi, want int
	}{
		{"within range", 5, 0, 10, 5},
		{"below range", -5, 0, 10, 0},
		{"above range", 15, 0, 10, 10},
		{"at lower boundary", 0, 0, 10, 0},
		{"at upper boundary", 10, 0, 10, 10},
		{"negative range", -100, -50, -10, -50},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			got := Clamp(tc.x, tc.lo, tc.hi)
			if got != tc.want {
				t.Errorf("Clamp(%d, %d, %d) = %d, want %d", tc.x, tc.lo, tc.hi, got, tc.want)
			}
		})
	}
}
```

Run:

```bash
go test ./internal/mathutil/...
go test -v ./internal/mathutil/...   # verbose: shows each subtest name
```

Expected output (with `-v`): six `--- PASS` lines, one per named case, then `PASS` and `ok`.

### Common mistake

Using `t.Fatalf` instead of `t.Errorf` inside the loop over `cases`. `Fatalf` stops the **entire** test function immediately, so if the first case fails, you never learn whether the other five would have passed or failed — you fix one case, re-run, and discover the next failure one at a time instead of seeing the full picture. Reserve `Fatalf` for setup failures (e.g., a file that must exist for the test to even make sense), and use `Errorf` for actual assertion failures inside a loop.

### Your task

Add a case to the table for `lo > hi` (an invalid range, e.g. `Clamp(5, 10, 0)`) and decide — then implement — what `Clamp` should do: return `x` unchanged, return `lo`, or panic. Document your choice with a comment and a matching test case.

**Check:** `go test -v ./internal/mathutil/...` shows 7 passing subtests including your new one, and the comment above `Clamp` explains the invalid-range behavior in one sentence.

---

## Day 8: HTTP server
{: #day-8-http-server }

### Why this matters

`net/http` in the standard library is production-capable with zero external dependencies — no framework required for a real API. Understanding `http.HandleFunc`, status codes, and JSON encoding/decoding is the core of virtually every Go backend service.

### Mental model

A handler is any function matching `func(w http.ResponseWriter, r *http.Request)`. Always set the status code (`w.WriteHeader(...)`) **before** writing the body — headers can't change after the first `Write` call. Decode request bodies with `json.NewDecoder(r.Body).Decode(&target)`; encode responses with `json.NewEncoder(w).Encode(value)`.

### Code along

```go
// cmd/day08/main.go
package main

import (
	"encoding/json"
	"log"
	"net/http"
)

type EchoRequest struct {
	Message string `json:"message"`
}

type EchoResponse struct {
	Echo   string `json:"echo"`
	Length int    `json:"length"`
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]bool{"ok": true})
}

func echoHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		json.NewEncoder(w).Encode(map[string]string{"error": "use POST"})
		return
	}

	var req EchoRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(map[string]string{"error": "invalid JSON body"})
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(EchoResponse{Echo: req.Message, Length: len(req.Message)})
}

func main() {
	http.HandleFunc("/health", healthHandler)
	http.HandleFunc("/echo", echoHandler)
	log.Println("listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
```

Run it, then in another terminal:

```bash
go run ./cmd/day08 &
curl -s localhost:8080/health
curl -s -X POST localhost:8080/echo -d '{"message":"hi"}'
curl -s -X POST localhost:8080/echo -d 'not json'
```

Expected responses, in order: `{"ok":true}`, `{"echo":"hi","length":2}`, `{"error":"invalid JSON body"}` (kill the background server afterward with `kill %1`).

### Common mistake

Calling `w.WriteHeader(http.StatusBadRequest)` **after** already calling `json.NewEncoder(w).Encode(...)` once. The first write to `w` implicitly sends a `200 OK` status if you haven't set one explicitly — once that happens, any later `WriteHeader` call is a no-op and Go logs `http: superfluous response.WriteHeader call`. Always decide and set your status code as the very first thing you do in each branch of a handler, before any `Encode`/`Write` call.

### Your task

Add a `POST /links` route that stores `{"url": "..."}` in an in-memory `map[string]string` (generate a short id, e.g. `fmt.Sprintf("%d", len(store)+1)`) and returns `{"code": "...", "url": "..."}`; add `GET /links/{code}` reading via `r.URL.Path` parsing to look it up, returning `404` with a JSON error body if the code isn't found.

**Check:** `curl -X POST localhost:8080/links -d '{"url":"https://example.com"}'` returns a JSON object with a `code`; `curl localhost:8080/links/<that code>` returns the same URL; `curl -i localhost:8080/links/doesnotexist` shows `HTTP/1.1 404` in the headers.

---

## Day 9: Context & timeouts
{: #day-9-context-timeouts }

### Why this matters

Every real server call needs a way to say "give up after N seconds" or "stop if the client disconnected" — otherwise one slow downstream dependency can pile up unbounded work and take your whole service down. `context.Context` is Go's standard mechanism for cancellation and deadlines, threaded explicitly through every function that might block.

### Mental model

`context.WithTimeout` returns a context that's automatically cancelled after the duration, plus a `cancel` function you must always call (typically via `defer`) to release resources even if the timeout never fires. `select` with `ctx.Done()` alongside your actual work is the pattern for making any blocking operation respect cancellation.

### Code along

```go
// cmd/day09/main.go
package main

import (
	"context"
	"fmt"
	"time"
)

func slowOperation(ctx context.Context, delay time.Duration) (string, error) {
	select {
	case <-time.After(delay):
		return "operation complete", nil
	case <-ctx.Done():
		return "", fmt.Errorf("operation cancelled: %w", ctx.Err())
	}
}

func main() {
	ctx1, cancel1 := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel1()

	result, err := slowOperation(ctx1, 20*time.Millisecond)
	fmt.Println("fast op:", result, err)

	ctx2, cancel2 := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel2()

	result, err = slowOperation(ctx2, 200*time.Millisecond)
	fmt.Println("slow op:", result, err)
}
```

Expected output (timing approximate, the important part is the second line has an error):

```
fast op: operation complete <nil>
slow op:  operation cancelled: context deadline exceeded
```

### Common mistake

Forgetting `defer cancel()` after `context.WithTimeout`. The context still times out fine on its own, but the resources associated with the timer aren't released until the timeout naturally elapses — in a long-running server handling many requests per second, each with its own context, this leaks timers and memory until the process's resource usage climbs steadily. `go vet` will actually flag this for you (`the cancel function is not used on all paths`) — always run `go vet ./...` and pay attention to it.

### Your task

Wrap the `/echo` handler from Day 8 with a context that times out after 2 seconds using `r.Context()` (every `http.Request` already carries a context tied to the client connection) combined with `context.WithTimeout`, and have the handler return a `504 Gateway Timeout` if a simulated slow step (`time.Sleep` or the `select` pattern above) exceeds it.

**Check:** a request that completes quickly still returns `200`; temporarily hardcoding a 3-second simulated delay makes the same request return `504` after roughly 2 seconds, not 3.

---

## Day 10: Small module layout
{: #day-10-small-module-layout }

### Why this matters

`cmd/` for binaries and `internal/` for private packages (unimportable from outside your module — enforced by the compiler, not just convention) is the standard layout for any Go project past a single file. Learning it now means your next real project starts organized instead of needing a painful restructure later.

### Mental model

Anything under `internal/` can only be imported by code inside the same module — the Go toolchain enforces this at compile time, so it's a real boundary, not a suggestion. `cmd/<name>/main.go` per executable keeps entry points thin; the actual logic lives in importable packages that both your binaries and your tests can reach.

### Code along

Restructure Day 8's server into this layout:

```
go-lab/
  cmd/api/main.go
  internal/store/store.go
  internal/store/store_test.go
```

```go
// internal/store/store.go
package store

import (
	"fmt"
	"sync"
)

type Link struct {
	Code string
	URL  string
}

type MemStore struct {
	mu   sync.Mutex
	data map[string]string
	next int
}

func New() *MemStore {
	return &MemStore{data: make(map[string]string)}
}

func (s *MemStore) Create(url string) Link {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.next++
	code := fmt.Sprintf("l%d", s.next)
	s.data[code] = url
	return Link{Code: code, URL: url}
}

func (s *MemStore) Get(code string) (Link, bool) {
	s.mu.Lock()
	defer s.mu.Unlock()
	url, ok := s.data[code]
	return Link{Code: code, URL: url}, ok
}
```

```go
// cmd/api/main.go
package main

import (
	"encoding/json"
	"log"
	"net/http"

	"example.com/golab/internal/store"
)

func main() {
	s := store.New()

	http.HandleFunc("/links", func(w http.ResponseWriter, r *http.Request) {
		var body struct{ URL string `json:"url"` }
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil || body.URL == "" {
			w.WriteHeader(http.StatusBadRequest)
			return
		}
		link := s.Create(body.URL)
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(link)
	})

	log.Println("listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
```

Run `go run ./cmd/api` and confirm `curl -X POST localhost:8080/links -d '{"url":"https://x.com"}'` returns `{"Code":"l1","URL":"https://x.com"}`.

### Common mistake

Trying to `import "example.com/golab/internal/store"` from a *different* module (e.g., a separate `go.mod` in another directory you're experimenting with). This fails to compile with `use of internal package example.com/golab/internal/store not allowed` — `internal/` isn't just a naming convention, the Go compiler actively enforces the boundary. This is a feature: it guarantees your internal packages can be refactored freely without worrying about breaking external consumers, because there can't be any.

### Your task

Add a `GET /links/{code}` handler (parse the code from `r.URL.Path`, e.g. `strings.TrimPrefix(r.URL.Path, "/links/")`) using `store.Get`, and write a table-driven test in `internal/store/store_test.go` covering: creating returns sequential codes (`l1`, `l2`, ...), getting an existing code returns `found=true` with the right URL, and getting an unknown code returns `found=false`.

**Check:** `go test ./internal/store/...` passes; `curl localhost:8080/links/l1` after creating one link returns that link's URL; `curl -i localhost:8080/links/nope` returns `404`.

---

## Capstone project
{: #capstone }

Build a **URL shortener API** in Go with the `cmd/`+`internal/` layout from Day 10, a thread-safe in-memory store with full test coverage, and a README with copy-pasteable `curl` commands that actually work.

**Deliverable — file layout:**

```
url-shortener/
  cmd/api/main.go
  internal/store/store.go
  internal/store/store_test.go
  internal/httpapi/handlers.go       # separate handlers from main() for testability
  internal/httpapi/handlers_test.go
  README.md
  go.mod
```

**API requirements:**
- `POST /links` `{"url": "..."}` → `201` `{"code": "...", "url": "..."}`. `400` on missing/empty `url`.
- `GET /links/{code}` → `302` redirect to the stored URL (use `http.Redirect`), or `404` with a JSON error body if unknown.
- `GET /links` → `200` with a JSON array of all stored links.

**Testing requirements:** unit tests for the store (concurrent-safety not required to test explicitly, but the store must use a `sync.Mutex` or `sync.RWMutex`) and HTTP-level tests for the handlers using `net/http/httptest` — at minimum: creating a link and then successfully redirecting via its code, and requesting an unknown code returning `404`.

**README requirements:** exact `go run` command to start the server, and 3+ `curl` commands with their expected output pasted alongside them.

**Acceptance check:** `go test ./...` passes with no failures; starting the server and running the README's exact `curl` commands produces output matching what the README documents, word for word on status codes and field names.

## Related

- [Golang Bootcamp](/courses/golang-bootcamp/)
- [Rust in 10 Days](/courses/rust-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
