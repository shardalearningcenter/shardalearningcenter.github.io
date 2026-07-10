---
layout: post
title: "Getting Started with SQL"
date: 2026-07-10
description: "SELECT, JOIN, GROUP BY, and a blog schema exercise — the SQL every engineer needs."
tags: [sql, getting-started]
---

SQL is how you ask structured questions of tables. Whether you use Postgres, SQLite, or a warehouse, the core verbs stay the same.

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

Joins:

```sql
SELECT u.name, p.title
FROM users u
JOIN posts p ON p.author_id = u.id
WHERE u.active = TRUE;
```

Mutations (use carefully in production):

```sql
INSERT INTO posts (author_id, title, body) VALUES (1, 'Hello', '...');
UPDATE posts SET published = TRUE WHERE id = 42;
DELETE FROM comments WHERE id = 7;
```

## Mental model

- Tables ≈ spreadsheets with types and constraints
- Rows ≈ records; columns ≈ fields
- `JOIN` stitches tables on keys
- `GROUP BY` collapses rows into buckets; `HAVING` filters buckets

Prefer explicit `JOIN ... ON` over old comma-style joins.

## Exercise: blog schema

Design three tables:

1. `users(id, name, email)`
2. `posts(id, author_id, title, body, created_at)`
3. `comments(id, post_id, user_id, body, created_at)`

Then write:

- All comments on a given post with commenter names
- Top 5 commenters by comment count
- Posts with zero comments (`LEFT JOIN` + `WHERE comments.id IS NULL`)

Use SQLite locally if you want zero setup: `sqlite3 blog.db`.

## Next

APIs often wrap SQL — [FastAPI](/blog/2026/07/10/getting-started-with-fastapi/). RAG systems sometimes store metadata in SQL and vectors elsewhere — see [LLM Mastery art. 40](/courses/llm-mastery/40-rag-retrieval/).
