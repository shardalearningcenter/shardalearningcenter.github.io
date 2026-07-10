---
layout: post
title: "Getting Started with SQL"
date: 2026-07-10
description: "SELECT, JOIN, GROUP BY, and a real blog schema you build in SQLite with sample data — verify every query against rows you can count by hand."
tags: [sql, getting-started]
---

SQL is how you ask structured questions of tables. Whether you use Postgres, SQLite, or a warehouse, the core verbs stay the same. This post has you build a tiny blog schema, load real sample rows, and run queries whose output you can verify by counting the `INSERT`s yourself — no trust required.

## Core verbs

```sql
SELECT id, title
FROM posts
WHERE published = TRUE
ORDER BY created_at DESC
LIMIT 10;
```

Aggregations:

```sql
SELECT author_id, COUNT(*) AS n_posts
FROM posts
GROUP BY author_id
HAVING COUNT(*) >= 3
ORDER BY n_posts DESC;
```

Joins — always explicit, never a bare comma:

```sql
SELECT u.name, p.title
FROM users u
JOIN posts p ON p.author_id = u.id
WHERE u.active = TRUE;
```

Mutations (use carefully in production):

```sql
INSERT INTO posts (author_id, title) VALUES (1, 'Hello');
UPDATE posts SET published = TRUE WHERE id = 42;
DELETE FROM comments WHERE id = 7;
```

## Mental model

- Tables ≈ spreadsheets with types and constraints.
- Rows ≈ records; columns ≈ fields.
- `JOIN` stitches tables together on matching keys.
- `GROUP BY` collapses rows into buckets; `HAVING` filters *buckets*, `WHERE` filters *rows before* grouping.

## Mini project: a blog schema with data you can verify

Use SQLite for zero setup — one binary, one file, no server.

```bash
sqlite3 blog.db
```

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE
);

CREATE TABLE posts (
  id INTEGER PRIMARY KEY,
  author_id INTEGER NOT NULL REFERENCES users(id),
  title TEXT NOT NULL
);

CREATE TABLE comments (
  id INTEGER PRIMARY KEY,
  post_id INTEGER NOT NULL REFERENCES posts(id),
  user_id INTEGER NOT NULL REFERENCES users(id),
  body TEXT NOT NULL
);

INSERT INTO users (name, email) VALUES
  ('Asha', 'asha@example.com'),
  ('Ravi', 'ravi@example.com'),
  ('Meera', 'meera@example.com');

INSERT INTO posts (author_id, title) VALUES
  (1, 'Hello SQL'),
  (1, 'Joins Explained'),
  (2, 'Why Indexes Matter');

INSERT INTO comments (post_id, user_id, body) VALUES
  (1, 2, 'Great intro!'),
  (1, 3, 'Finally makes sense'),
  (2, 3, 'More examples please');
```

Now run three queries and verify each against the `INSERT`s above before trusting the output:

```sql
-- 1. All comments on post 1, with commenter names
SELECT c.body, u.name AS commenter
FROM comments c
JOIN users u ON u.id = c.user_id
WHERE c.post_id = 1;
-- expect exactly 2 rows: Ravi's and Meera's comments on 'Hello SQL'

-- 2. Top commenters by comment count
SELECT u.name, COUNT(*) AS n_comments
FROM comments c
JOIN users u ON u.id = c.user_id
GROUP BY u.name
ORDER BY n_comments DESC;
-- expect Meera first with 2 (she commented on posts 1 and 2), Ravi with 1

-- 3. Posts with zero comments
SELECT p.title
FROM posts p
LEFT JOIN comments c ON c.post_id = p.id
WHERE c.id IS NULL;
-- expect exactly 'Why Indexes Matter' (post 3 has no comments above)
```

If your output doesn't match the comments in each query, re-count the `INSERT` statements — that mismatch is the whole point of the exercise: SQL results are always derivable by hand from small data, so "it looks right" is never good enough.

## Common footguns

- **`WHERE x = NULL` never matches anything** — `NULL` isn't equal to anything, including itself. Use `WHERE x IS NULL` / `IS NOT NULL`.
- **SQLite is lenient about `GROUP BY`** — it lets you `SELECT` a non-aggregated, non-grouped column without erroring (many other databases reject this outright). The value you get back is essentially arbitrary; only select columns that are either grouped or aggregated.
- **Missing `ON` clause → cartesian join** — `FROM a, b` without a join condition returns every combination of rows from both tables, which silently explodes result size on real data.
- **`LEFT JOIN` + `WHERE` on the right table's column (not `IS NULL`)** — turns your outer join back into an inner join by accident, because `WHERE comments.body = 'x'` filters out the `NULL` rows the `LEFT JOIN` produced.
- **`SELECT *` in application code** — breaks silently when someone adds or reorders a column; name the columns you actually use.
- **No index on a foreign key** — joins on `author_id` or `post_id` do a full table scan once your tables grow past a few thousand rows; `CREATE INDEX idx_posts_author ON posts(author_id);` fixes it.

## You know you're done when…

- [ ] `sqlite3 blog.db ".tables"` lists `users`, `posts`, and `comments`
- [ ] All three exercise queries return exactly the row counts predicted in the comments above
- [ ] You can explain why `WHERE comments.id IS NULL` after a `LEFT JOIN` finds posts with no comments — and why `WHERE comments.id = NULL` would return nothing at all
- [ ] Every join in your queries uses explicit `JOIN ... ON`, never a bare comma
- [ ] You can name one column in this schema that would benefit from an index, and why

## Next

APIs often wrap SQL — see [Getting Started with FastAPI](/2026/07/10/getting-started-with-fastapi/). RAG systems sometimes store metadata in SQL and vectors elsewhere — see [LLM Mastery art. 40](/courses/llm-mastery/40-rag-retrieval/).
