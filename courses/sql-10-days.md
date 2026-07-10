---
layout: course
title: "SQL in 10 Days — Hands-On"
permalink: /courses/sql-10-days/
course_track: "SQL"
description: "Joins, aggregates, window functions, and CTEs in SQLite — build query fluency by running real queries against real data, not syntax diagrams."
toc:
  - id: "why-this-language"
    label: "Why this language"
  - id: "setup-day-0"
    label: "Setup (Day 0)"
  - id: "day-1-select-basics"
    label: "Day 1: SELECT basics"
  - id: "day-2-insertupdatedelete"
    label: "Day 2: INSERT/UPDATE/DELETE"
  - id: "day-3-joins"
    label: "Day 3: JOINs"
  - id: "day-4-group-by"
    label: "Day 4: GROUP BY"
  - id: "day-5-subqueries"
    label: "Day 5: Subqueries"
  - id: "day-6-indexes-explain"
    label: "Day 6: Indexes & EXPLAIN"
  - id: "day-7-window-functions"
    label: "Day 7: Window functions"
  - id: "day-8-ctes"
    label: "Day 8: CTEs"
  - id: "day-9-views-constraints"
    label: "Day 9: Views & constraints"
  - id: "day-10-analytics-mini-project"
    label: "Day 10: Analytics mini-project"
  - id: "capstone"
    label: "Capstone project"
---

# SQL in 10 Days — Hands-On

Joins, aggregates, window functions, and CTEs — all run against one small SQLite database that grows day by day. Every query below produces an exact, checkable result against the seed data in Day 0.

## Why this language
{: #why-this-language }

SQL is the one language nearly every backend, data, and analytics role still speaks daily, and it hasn't meaningfully changed in decades — the SQL you learn this week still works in ten years. The hard part isn't the syntax (SELECT/FROM/WHERE is five minutes of memorization); it's the relational thinking underneath: joins, aggregation, and set logic. This course uses SQLite because it needs zero setup, but every query here is standard ANSI SQL that transfers directly to Postgres, MySQL, or a data warehouse — dialect notes are called out where they matter.

## Setup (Day 0)
{: #setup-day-0 }

```bash
sqlite3 --version   # expect 3.x
sqlite3 learning.db
```

Paste this schema and seed data at the `sqlite3>` prompt (or save it as `seed.sql` and run `sqlite3 learning.db < seed.sql`). It's the dataset every day below queries — nothing is dropped between days.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES users(id),
    title TEXT NOT NULL,
    published INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES posts(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    body TEXT NOT NULL,
    created_at TEXT NOT NULL
);

INSERT INTO users (id, name, email, active) VALUES
    (1, 'Ada', 'ada@example.com', 1),
    (2, 'Grace', 'grace@example.com', 1),
    (3, 'Linus', 'linus@example.com', 0),
    (4, 'Margaret', 'margaret@example.com', 1);

INSERT INTO posts (id, author_id, title, published) VALUES
    (1, 1, 'Hello World', 1),
    (2, 1, 'Draft Post', 0),
    (3, 2, 'Compilers 101', 1),
    (4, 2, 'Second Post', 1),
    (5, 4, 'Software Engineering', 1);

INSERT INTO comments (id, post_id, user_id, body, created_at) VALUES
    (1, 1, 2, 'Nice!', '2026-01-01'),
    (2, 1, 4, 'Great read', '2026-01-02'),
    (3, 3, 1, 'Interesting', '2026-01-03'),
    (4, 3, 4, '+1', '2026-01-04'),
    (5, 4, 1, 'Thanks', '2026-01-05');
```

**Checkpoint:** run `SELECT COUNT(*) FROM users;` and confirm it prints `4`. If you get a "no such table" error, the schema block above didn't run — re-paste it before continuing.

---

## Day 1: SELECT basics
{: #day-1-select-basics }

### Why it matters

Every query you'll ever write is a variation on `SELECT ... FROM ... WHERE ... ORDER BY ... LIMIT`. Get the *order of execution* right in your head now — `FROM`/`WHERE` filter rows before `SELECT` picks columns, and `ORDER BY`/`LIMIT` happen last — and every weirder query later stops being mysterious.

### Mental model

SQL reads like English but *executes* almost backwards: SQLite first figures out which table (`FROM`), then which rows (`WHERE`), then which columns (`SELECT`), then sorts (`ORDER BY`), then trims (`LIMIT`). This is why you can't reference a column alias from `SELECT` inside the same query's `WHERE` clause — `WHERE` runs before `SELECT` has created that alias.

### Code along

```sql
SELECT id, title
FROM posts
WHERE published = 1
ORDER BY id DESC
LIMIT 3;
```

Expected output:

```
5|Software Engineering
4|Second Post
3|Compilers 101
```

(Post `2`, "Draft Post", is excluded — `published = 0` — and post `1` falls outside the `LIMIT 3` once sorted newest-first.)

### Common mistake

Writing `WHERE published = 1 ORDER BY published_at LIMIT 3` and expecting `LIMIT` to run *before* the sort — thinking "give me any 3, then sort them." SQLite (and every SQL engine) always sorts the *entire* filtered result set first, then takes the top rows from that sorted set. There's no such thing as "sort these 3 rows I already picked" unless you explicitly nest it in a subquery.

### Your task

Write a query returning the `name` and `email` of every `active = 1` user, sorted alphabetically by `name`.

**Check:** the output is exactly `Ada|ada@example.com`, `Grace|grace@example.com`, `Margaret|margaret@example.com` in that order — Linus is excluded (`active = 0`).

---

## Day 2: INSERT/UPDATE/DELETE
{: #day-2-insertupdatedelete }

### Why it matters

Reads are half of SQL; writes are the other half, and they're the half that can silently corrupt data if you forget a `WHERE` clause. Transactions (`BEGIN`/`COMMIT`/`ROLLBACK`) exist so that a multi-step write either fully happens or fully doesn't — no half-finished state visible to anyone else.

### Mental model

`UPDATE table SET col = val` with **no `WHERE`** updates *every row in the table* — this is the SQL equivalent of `rm -rf` with no path. Always write and verify the `WHERE` clause as a `SELECT` first, then swap `SELECT *` for the mutation once you've confirmed it targets the right rows. A transaction groups statements so `ROLLBACK` can undo all of them if any check fails partway through.

### Code along

```sql
SELECT * FROM posts WHERE author_id = 1;  -- verify the target set first

BEGIN;
INSERT INTO posts (id, author_id, title, published) VALUES (6, 3, 'Linus Draft', 0);
UPDATE users SET active = 1 WHERE id = 3;
COMMIT;

SELECT name, active FROM users WHERE id = 3;
```

Expected output (last query): `Linus|1`

### Common mistake

Running `DELETE FROM comments WHERE post_id = 1` inside a `BEGIN` block, getting distracted, and leaving the transaction open in another terminal tab. SQLite locks the database file for writes until you `COMMIT` or `ROLLBACK` — a second connection trying to write will hang or fail with `database is locked`. Always finish (commit or rollback) a transaction in the same breath you started it; don't leave one open across a coffee break.

### Your task

Inside one transaction: insert a new post `(7, 2, 'Rolled Back Post', 0)`, then deliberately `ROLLBACK` instead of `COMMIT`.

**Check:** `SELECT COUNT(*) FROM posts;` still returns `5` afterward — the rollback fully undid the insert, proving the transaction boundary actually worked.

---

## Day 3: JOINs
{: #day-3-joins }

### Why it matters

Real data lives in multiple tables on purpose — a `users` table shouldn't repeat a name on every comment row. `JOIN` is how you reassemble that normalized data back into one readable result, and it's the single most-used SQL feature in any real application.

### Mental model

`INNER JOIN` (or bare `JOIN`) keeps only rows that match on *both* sides — a user with zero comments disappears entirely. `LEFT JOIN` keeps every row from the left table regardless of a match, filling unmatched right-side columns with `NULL` — this is the join you want when the *absence* of a match is the interesting answer (Day 3's task).

### Code along

```sql
SELECT u.name AS commenter, p.title, c.body
FROM comments c
JOIN posts p ON p.id = c.post_id
JOIN users u ON u.id = c.user_id
ORDER BY c.id;
```

Expected output:

```
Grace|Hello World|Nice!
Margaret|Hello World|Great read
Ada|Compilers 101|Interesting
Margaret|Compilers 101|+1
Ada|Second Post|Thanks
```

### Common mistake

Writing `JOIN posts p ON p.author_id = u.id` when `u` (the `users` alias) hasn't been introduced yet in the `FROM` clause above it. SQLite evaluates joins top-to-bottom in the order you write them, so an `ON` clause can only reference aliases already declared *earlier* in the same query — `no such column: u.id` if you jump the gun. Chain joins in the order the aliases become available.

### Your task

Use a `LEFT JOIN` from `users` to `posts` to find every user who has written zero posts.

**Check:** the query returns exactly one row: `Linus` (with `NULL` in the joined `posts` columns) — every other user has at least one post.

---

## Day 4: GROUP BY
{: #day-4-group-by }

### Why it matters

"How many X per Y" is one of the most common business questions, and `GROUP BY` plus an aggregate (`COUNT`, `SUM`, `AVG`) is the entire answer. `HAVING` is the `WHERE` that runs *after* grouping — that distinction trips up almost everyone the first time.

### Mental model

`WHERE` filters rows *before* grouping happens; `HAVING` filters *groups* after aggregation. You can't write `WHERE COUNT(*) >= 2` — `COUNT(*)` doesn't exist yet at the point `WHERE` runs — but `HAVING COUNT(*) >= 2` works because grouping has already happened by then.

### Code along

```sql
SELECT u.name AS commenter, COUNT(*) AS n
FROM comments c
JOIN users u ON u.id = c.user_id
GROUP BY u.id
HAVING n >= 2
ORDER BY n DESC;
```

Expected output:

```
Ada|2
Margaret|2
```

(Grace commented once — excluded by `HAVING n >= 2`.)

### Common mistake

Writing `WHERE COUNT(*) >= 2` instead of `HAVING`, and getting `misuse of aggregate function COUNT()`. SQLite is telling you, correctly, that aggregate functions don't have a value yet at the `WHERE` stage — grouping and aggregation happen *after* the row-filtering `WHERE` clause, so there's nothing to compare yet. If you're filtering on an aggregate result, it's always `HAVING`.

### Your task

Write a query showing each post's `id`, `title`, and comment count (including posts with **zero** comments — hint: `LEFT JOIN` and `COUNT(c.id)`, not `COUNT(*)`, so unmatched rows count as `0` not `1`).

**Check:** posts `2` and `5` show `0`; post `1` and `3` show `2`; post `4` shows `1` — five rows total, none dropped.

---

## Day 5: Subqueries
{: #day-5-subqueries }

### Why it matters

Sometimes a filter depends on a separate query's result — "users who have posted" isn't a column, it's a relationship you have to compute. `EXISTS`, `IN`, and scalar subqueries are three ways to embed one query's answer inside another's `WHERE` clause.

### Mental model

`EXISTS (subquery)` only cares whether the subquery returns *any* row — it's a yes/no check and stops scanning as soon as it finds one match, which usually makes it faster than `IN` for existence checks. `IN (subquery)` compares against the actual *values* the subquery returns, which is the right tool when you're matching specific IDs rather than asking "does anything match."

### Code along

```sql
SELECT name FROM users u
WHERE EXISTS (SELECT 1 FROM posts p WHERE p.author_id = u.id);
```

Expected output: `Ada`, `Grace`, `Margaret` (three rows — Linus has no posts).

### Common mistake

Trying `WHERE id NOT IN (SELECT author_id FROM posts)` expecting the mirror image of the query above, but a **single `NULL`** anywhere in `posts.author_id` silently breaks it — `NOT IN` against a list containing `NULL` returns `NULL` (not `true`) for every comparison, so the whole `WHERE` clause matches zero rows, with no error at all. `NOT EXISTS` doesn't have this trap because it never compares values directly:

```sql
SELECT name FROM users u
WHERE NOT EXISTS (SELECT 1 FROM posts p WHERE p.author_id = u.id);
```

Prefer `NOT EXISTS` over `NOT IN` whenever the subquery's column could ever contain `NULL` — which, in practice, means prefer it by default.

### Your task

Write a query listing each user's name alongside their **total published post count**, using a scalar subquery in the `SELECT` list: `(SELECT COUNT(*) FROM posts p WHERE p.author_id = u.id AND p.published = 1)`.

**Check:** `Ada|1`, `Grace|2`, `Linus|0`, `Margaret|1` — four rows, one per user, in whatever order `users` returns them without an `ORDER BY`.

---

## Day 6: Indexes & EXPLAIN
{: #day-6-indexes-explain }

### Why it matters

Every query above has run instantly because the tables are tiny. At real scale, the difference between a query that finishes in 2ms and one that takes 2 minutes is almost always: is there an index on the column being filtered or joined on? `EXPLAIN QUERY PLAN` shows you the truth instead of a guess.

### Mental model

Without an index, filtering `WHERE author_id = 2` means SQLite reads *every row* in the table and checks each one — a **SCAN**. An index on `author_id` lets it jump straight to matching rows — a **SEARCH**. Indexes speed up reads but cost a little on every write (the index has to be updated too), so you index columns you filter/join on often, not every column reflexively.

### Code along

```sql
EXPLAIN QUERY PLAN
SELECT * FROM posts WHERE author_id = 2;
```

Expected output (before adding an index): a plan mentioning `SCAN posts`.

```sql
CREATE INDEX idx_posts_author ON posts(author_id);

EXPLAIN QUERY PLAN
SELECT * FROM posts WHERE author_id = 2;
```

Expected output (after): a plan mentioning `SEARCH posts USING INDEX idx_posts_author (author_id=?)`.

### Common mistake

Adding an index on `comments(user_id)` and then querying `WHERE LOWER(user_id) = 2` (or any expression wrapped around the indexed column) and being confused why `EXPLAIN QUERY PLAN` still shows a `SCAN`. An index on a raw column only speeds up comparisons against that *exact* column — wrapping it in a function means SQLite has to compute that function for every row before it can compare, defeating the index. If you need to filter on an expression regularly, index the expression itself (`CREATE INDEX ... ON table(LOWER(col))`).

### Your task

Create an index on `comments(post_id)`, then run `EXPLAIN QUERY PLAN SELECT * FROM comments WHERE post_id = 3;` before and after.

**Check:** the plan changes from mentioning `SCAN comments` to mentioning `SEARCH comments USING INDEX ... (post_id=?)` — you should be able to point at the exact word that changed.

---

## Day 7: Window functions
{: #day-7-window-functions }

### Why it matters

"Running total," "rank within group," and "compare this row to the previous row" all used to require self-joins or app-side loops. Window functions compute these *without collapsing rows the way `GROUP BY` does* — you keep every row and add a computed column alongside it.

### Mental model

`GROUP BY` merges rows into one row per group; `OVER (...)` keeps every row but computes a value *relative to a window* of related rows. `PARTITION BY` resets the calculation per group (like a mini `GROUP BY` inside the window); `ORDER BY` inside `OVER` controls both the running order **and** the default frame (`RANGE UNBOUNDED PRECEDING`) — without it, aggregates like `SUM(...) OVER (...)` compute the grand total for the whole partition on every row instead of a running total.

### Code along

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    amount_cents INTEGER NOT NULL,
    order_date TEXT NOT NULL
);

INSERT INTO orders (id, user_id, amount_cents, order_date) VALUES
    (1, 1, 1000, '2026-02-01'),
    (2, 2, 1500, '2026-02-01'),
    (3, 1, 2000, '2026-02-02'),
    (4, 4, 500,  '2026-02-02'),
    (5, 2, 3000, '2026-02-03'),
    (6, 1, 1200, '2026-02-03');

SELECT id, order_date, amount_cents,
    SUM(amount_cents) OVER (ORDER BY id) AS running_total
FROM orders;
```

Expected output:

```
1|2026-02-01|1000|1000
2|2026-02-01|1500|2500
3|2026-02-02|2000|4500
4|2026-02-02|500|5000
5|2026-02-03|3000|8000
6|2026-02-03|1200|9200
```

### Common mistake

Writing `SUM(amount_cents) OVER (PARTITION BY user_id)` and expecting a running total per user, but omitting `ORDER BY` inside `OVER`. Without an `ORDER BY`, every row in the partition sees the *entire* partition as its frame — you get each user's grand total repeated on every one of their rows, not a running total. The fix is `OVER (PARTITION BY user_id ORDER BY id)` — adding the `ORDER BY` is what turns "total" into "running total."

### Your task

Add `ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY id) AS order_seq` as a second computed column to the query above.

**Check:** user `1`'s three orders (ids 1, 3, 6) show `order_seq` `1, 2, 3`; user `2`'s two orders (ids 2, 5) show `1, 2`; user `4`'s one order shows `1`.

---

## Day 8: CTEs
{: #day-8-ctes }

### Why it matters

`WITH name AS (...)` (a Common Table Expression) names a subquery so the rest of your query reads top-to-bottom like a pipeline instead of a nested Russian doll of parentheses. Recursive CTEs go further — they can generate sequences or walk hierarchies (org charts, category trees) that a single flat query can't express.

### Mental model

A CTE is a subquery with a name, scoped to just the one statement that follows it — think of it as a temporary, disposable view. A **recursive** CTE has two parts unioned together: a base case (the starting row(s)) and a recursive case that references the CTE's own name, repeating until the recursive part produces no new rows.

### Code along

```sql
WITH active_authors AS (
    SELECT DISTINCT author_id FROM posts WHERE published = 1
)
SELECT u.name FROM users u
JOIN active_authors a ON a.author_id = u.id
ORDER BY u.name;
```

Expected output: `Ada`, `Grace`, `Margaret`.

Recursive CTE — generate a small number sequence:

```sql
WITH RECURSIVE counter(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM counter WHERE n < 5
)
SELECT n FROM counter;
```

Expected output: `1`, `2`, `3`, `4`, `5` (five rows).

### Common mistake

Writing the recursive case without a terminating condition — `SELECT n + 1 FROM counter` with no `WHERE n < 5` guard. SQLite will keep unioning new rows forever (or until it hits the default recursion limit and errors out), because nothing ever tells the recursive term to stop producing rows. Always put the stopping condition directly in the recursive `SELECT`'s `WHERE` clause, not as an afterthought `LIMIT` on the final query — `LIMIT` alone doesn't stop the CTE from generating rows internally.

### Your task

Rewrite the Day 4 "posts with zero comments" idea as a CTE: `WITH comment_counts AS (SELECT post_id, COUNT(*) AS n FROM comments GROUP BY post_id)`, then `SELECT` post titles from `posts LEFT JOIN comment_counts` where the count is `0` or missing.

**Check:** returns exactly `Draft Post` and `Software Engineering` (posts `2` and `5`) — the same two posts Day 4's `LEFT JOIN`/`COUNT(c.id)` version found, confirming both approaches agree.

---

## Day 9: Views & constraints
{: #day-9-views-constraints }

### Why it matters

A `VIEW` saves a query under a name so you (and everyone else on the team) stop copy-pasting the same five-join monster. Constraints (`UNIQUE`, `FOREIGN KEY`, `CHECK`) push data-integrity rules into the database itself, so a bug in application code can't silently create orphaned or impossible rows.

### Mental model

A view is a stored `SELECT`, re-run fresh every time you query it — it doesn't cache data, so it's always current but not inherently faster. Foreign keys need enforcement turned on explicitly in SQLite (`PRAGMA foreign_keys = ON;` — it defaults to *off* for backward compatibility, unlike Postgres/MySQL where it's always on).

### Code along

```sql
CREATE VIEW post_engagement AS
SELECT p.id, p.title, COUNT(c.id) AS comment_count
FROM posts p
LEFT JOIN comments c ON c.post_id = p.id
GROUP BY p.id;

SELECT * FROM post_engagement WHERE comment_count = 0;
```

Expected output: `2|Draft Post|0` and `5|Software Engineering|0`.

```sql
PRAGMA foreign_keys = ON;
INSERT INTO comments (id, post_id, user_id, body, created_at)
VALUES (99, 999, 1, 'orphan comment', '2026-03-01');
```

Expected error: `FOREIGN KEY constraint failed` — post `999` doesn't exist, and with enforcement on, SQLite refuses the insert outright.

### Common mistake

Defining the `REFERENCES posts(id)` foreign key in the schema (as Day 0 did) but never running `PRAGMA foreign_keys = ON;` — then being surprised the "orphan comment" insert above *succeeds* silently instead of erroring. SQLite parses and stores foreign key definitions regardless, but only *enforces* them when that pragma is set, and it must be set on every new connection (it's not a permanent database setting) — a script that opens a fresh connection without the pragma has no enforcement, even against a schema that looks fully constrained.

### Your task

Add a `CHECK` constraint (`CHECK (published IN (0, 1))`) if it were missing, then try `UPDATE posts SET published = 2 WHERE id = 1;` against a table that has it.

**Check:** the update fails with an error mentioning `CHECK constraint failed`, and `SELECT published FROM posts WHERE id = 1;` still shows the original value `1`, proving the failed write changed nothing.

---

## Day 10: Analytics mini-project
{: #day-10-analytics-mini-project }

### Why it matters

Funnel analysis — "how many people who signed up also activated, and how many of those purchased" — is the single most common analytics query in any product company. It's `GROUP BY` and conditional aggregation applied to event data, and once you can write one funnel query, you can write all of them.

### Mental model

Model each user action as one row in an `events` table (`user_id`, `event`, `ts`) rather than one column per event — this "long" format is what lets you add a new event type later without an `ALTER TABLE`. Count funnel steps with conditional aggregation: `COUNT(DISTINCT CASE WHEN event = 'signup' THEN user_id END)` counts *users*, not raw event rows, which matters if someone can fire the same event twice.

### Code along

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    event TEXT NOT NULL,
    ts TEXT NOT NULL
);

INSERT INTO events (user_id, event, ts) VALUES
    (1, 'signup',   '2026-03-01'), (2, 'signup',   '2026-03-01'),
    (3, 'signup',   '2026-03-01'), (4, 'signup',   '2026-03-02'),
    (1, 'activate', '2026-03-01'), (2, 'activate', '2026-03-02'),
    (3, 'activate', '2026-03-02'),
    (1, 'purchase',  '2026-03-02'), (2, 'purchase', '2026-03-03');

SELECT
    COUNT(DISTINCT CASE WHEN event = 'signup'   THEN user_id END) AS signups,
    COUNT(DISTINCT CASE WHEN event = 'activate' THEN user_id END) AS activated,
    COUNT(DISTINCT CASE WHEN event = 'purchase' THEN user_id END) AS purchased
FROM events;
```

Expected output: `4|3|2` — 4 users signed up, 3 activated, 2 purchased.

### Common mistake

Using `COUNT(CASE WHEN event = 'signup' THEN user_id END)` (no `DISTINCT`) when a user's client accidentally fires the `signup` event twice due to a retry. That double-fire inflates the signup count to `5` even though only 4 distinct users actually signed up — the funnel's top of the mouth looks bigger than reality, and every downstream conversion rate you compute from it is quietly wrong. Conditional *counts* of events and conditional counts of *distinct users* answer different questions — pick deliberately.

### Your task

Compute the activation rate (`activated / signups`) and purchase rate (`purchased / activated`) as percentages, rounded to one decimal, using the counts above (hint: `CAST(x AS REAL) / y * 100`, and watch for integer division truncating to `0`).

**Check:** activation rate is `75.0` (3/4), purchase rate is `66.7` (2/3, rounded) — if you get `0` for either, you divided two integers without casting one to `REAL` first.

---

## Capstone project
{: #capstone }

Build a small **SaaS metrics database** modeling `users`, `accounts` (an account can have many users), and `events`, then write five reporting queries in a `queries.sql` file:

1. **DAU** — distinct users with at least one event, grouped by day.
2. **Top accounts** — the 5 accounts with the most events in the last 7 days of your seed data.
3. **Signup → activation → purchase funnel** — reusing Day 10's conditional-count pattern.
4. **Week-2 retention** — of users who signed up in week 1, what percentage had any event in week 2 (hint: two CTEs — `week1_signups` and `week2_active` — then a `LEFT JOIN` and a percentage).
5. **Running revenue total** — a window-function running total over a `purchase` event's associated `amount_cents` (add that column to `events`, or a separate `purchases` table if you prefer a cleaner schema).

**Acceptance check:** every query in `queries.sql` runs against your seed data with `sqlite3 metrics.db < queries.sql` without error, and you can explain out loud — for each one — which day's technique it reuses (join, group by, subquery, window function, or CTE).

## Related

- [Getting Started with SQL](/blog/2026/07/10/getting-started-with-sql/)
- [Python in 10 Days](/courses/python-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
