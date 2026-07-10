---
layout: course
title: "SQL in 10 Days — Hands-On"
permalink: /courses/sql-10-days/
course_track: "SQL"
description: "Query fluency with SQLite: joins, windows, and a tiny analytics project."
toc:
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

Query fluency with SQLite: joins, windows, and a tiny analytics project.

## Why this language
{: #why-this-language }

Every backend and data role speaks SQL. Master it once; transfer everywhere.

## Setup (Day 0)
{: #setup-day-0 }

```bash
sqlite3 --version
sqlite3 learning.db
```
Or use any Postgres — dialect notes call out differences.

---

## Day 1: SELECT basics
{: #day-1-select-basics }

### What you'll learn

- SELECT/FROM/WHERE
- ORDER BY
- LIMIT

### Code along

```sql
SELECT id, title FROM posts WHERE published = 1 ORDER BY id DESC LIMIT 5;
```

### Your task

Create a `people(name, age)` table; insert 5 rows; query adults.

---

## Day 2: INSERT/UPDATE/DELETE
{: #day-2-insertupdatedelete }

### What you'll learn

- mutations
- transactions
- BEGIN/COMMIT

### Code along

```sql
BEGIN;
UPDATE people SET age = age + 1 WHERE name = 'Ada';
COMMIT;
```

### Your task

Transaction that inserts two related rows or rolls back.

---

## Day 3: JOINs
{: #day-3-joins }

### What you'll learn

- INNER
- LEFT
- ON

### Code along

```sql
SELECT u.name, p.title
FROM users u
JOIN posts p ON p.author_id = u.id;
```

### Your task

Blog schema: users/posts/comments; list comments with names.

---

## Day 4: GROUP BY
{: #day-4-group-by }

### What you'll learn

- COUNT/SUM
- HAVING
- aggregates

### Code along

```sql
SELECT author_id, COUNT(*) AS n FROM posts GROUP BY author_id HAVING n >= 2;
```

### Your task

Top 5 commenters.

---

## Day 5: Subqueries
{: #day-5-subqueries }

### What you'll learn

- IN
- EXISTS
- scalar subquery

### Code along

```sql
SELECT name FROM users u
WHERE EXISTS (SELECT 1 FROM posts p WHERE p.author_id = u.id);
```

### Your task

Users with zero posts via NOT EXISTS.

---

## Day 6: Indexes & EXPLAIN
{: #day-6-indexes-explain }

### What you'll learn

- CREATE INDEX
- EXPLAIN QUERY PLAN
- when indexes help

### Code along

```sql
CREATE INDEX idx_posts_author ON posts(author_id);
EXPLAIN QUERY PLAN SELECT * FROM posts WHERE author_id = 1;
```

### Your task

Add an index that speeds a slow filter you invent.

---

## Day 7: Window functions
{: #day-7-window-functions }

### What you'll learn

- ROW_NUMBER
- RANK
- SUM OVER

### Code along

```sql
SELECT title, author_id,
  ROW_NUMBER() OVER (PARTITION BY author_id ORDER BY id) AS rn
FROM posts;
```

### Your task

Running total of amounts by day.

---

## Day 8: CTEs
{: #day-8-ctes }

### What you'll learn

- WITH
- readable pipelines
- recursive peek

### Code along

```sql
WITH active AS (
  SELECT * FROM users WHERE active = 1
)
SELECT * FROM active;
```

### Your task

Rewrite a nested subquery as a CTE.

---

## Day 9: Views & constraints
{: #day-9-views-constraints }

### What you'll learn

- VIEW
- UNIQUE
- FOREIGN KEY
- CHECK

### Code along

```sql
CREATE VIEW post_counts AS
SELECT author_id, COUNT(*) AS n FROM posts GROUP BY author_id;
```

### Your task

Enforce FK from comments to posts; try a bad insert.

---

## Day 10: Analytics mini-project
{: #day-10-analytics-mini-project }

### What you'll learn

- star schema lite
- funnel query
- export

### Code along

```sql
-- events(user_id, event, ts)
-- count signup -> activate -> purchase
```

### Your task

Design events table; write a 3-step funnel count.


---

## Capstone project
{: #capstone }

Model a **SaaS metrics** SQLite DB (users, accounts, events). Write 5 reporting queries (DAU, top accounts, funnel, retention sketch) in a `queries.sql` file.

## Related

- [Getting Started with SQL](/blog/2026/07/10/getting-started-with-sql/)
- [Python in 10 Days](/courses/python-10-days/)

[All language tutorials](/courses/languages/) · [All courses](/courses/)
