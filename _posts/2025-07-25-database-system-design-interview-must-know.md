---
layout: post
title: "Database questions must know for system design interview"
date: 2025-07-25
---
# Databse questions must know for system design interview


## 🎯 Scenario:

You’re designing and maintaining a backend for a high-traffic Google service (e.g., YouTube comment system, Google Maps review store, etc.). Millions of reads and writes per day. Your task is to optimize database performance, both read-heavy and write-heavy use cases.



## 🟢 Interviewer starts: Basic Level Questions



### 🔹 Q1. What do you mean by database fine-tuning?

A: Database fine-tuning is the process of improving the performance of a database system by optimizing queries, indexes, schema design, configuration settings, and hardware resources to minimize latency and maximize throughput.

### 🔹 Q2. What’s the first thing you’d do if a query is running slow?

A: First, I’d analyze the query execution plan using tools like EXPLAIN (MySQL/PostgreSQL) to understand how the database is interpreting the query. This helps identify full table scans, missing indexes, or costly operations like sorts or joins.

## 🟡 Interviewer follows up to dig deeper

### 🔹 Q3. What if the execution plan shows a full table scan? What would you do?

A: I’d check if the columns in the WHERE clause are indexed. If not, adding an appropriate index can help. I’d also consider whether the query could be rewritten to be more efficient, e.g., breaking large JOINs or using materialized views.

### 🔹 Q4. How do indexes improve performance, and when can they hurt it?

A: Indexes speed up read operations by allowing faster lookups. However, they can hurt write performance since the database must update indexes on every insert, update, or delete. Over-indexing can also increase memory usage.

### 🔹 Q5. In a write-heavy system, how would you optimize?

A: In write-heavy scenarios, I’d minimize indexes, batch writes, and consider techniques like write-ahead logging or in-memory queues (e.g., Kafka) to decouple writes. I’d also partition data (sharding) to distribute load.



### 🔹 Q6. Would you denormalize the schema to improve performance? When?

A: Yes, especially in read-heavy systems. Denormalization avoids expensive JOINs and reduces query complexity. However, it increases redundancy and risk of data inconsistency, so I’d only do it with strong data update strategies in place.



## 🔴 Interviewer gets technical and scenario-driven



### 🔹 Q7. Your service has a 99th percentile query latency of 1.2s. Business wants it < 500ms. What are your steps?

A:

Analyze slow queries via logs or APM tools.

Use EXPLAIN to check for suboptimal plans.

Add/adjust indexes.

Cache expensive queries in Redis/Memcached.

Add pagination for large result sets.

If still slow, consider query restructuring or denormalization.



### 🔹 Q8. You added an index and the query slowed down. Why might that happen?

A: Possible reasons:

Query planner misjudged index selectivity.

Index is not covering (doesn’t include all needed columns).

Index maintenance overhead on frequent writes.

Query became CPU-bound due to sorting/index lookup.



### 🔹 Q9. How would you design indexes for a composite query with WHERE clauses on (user_id, status) and ORDER BY created_at DESC?



A: I’d use a composite index on (user_id, status, created_at DESC) to match both the filter and sort. Index order matters — filters first, sort last.



### 🔹 Q10. How do you detect and prevent deadlocks in a DB under load?

A:

Use proper transaction ordering.

Keep transactions short.

Use lower isolation levels if acceptable.

Add monitoring for deadlock events via DB logs.

Detect circular locks via profiling tools.



### 🔹 Q11. How does connection pooling help with performance?

A: It reuses existing DB connections instead of constantly opening/closing new ones, reducing latency and CPU cost. Helps manage concurrent requests efficiently.



## 🔵 Interviewer shifts to scaling & high availability



### 🔹 Q12. How would you scale a database handling 10M+ requests per day?

A:

Read Replicas for load balancing.

Sharding (horizontal partitioning).

Caching layer (e.g., Redis) for frequently accessed data.

Use of CDNs where applicable.

Load testing to find bottlenecks.



### 🔹 Q13. What’s the difference between vertical and horizontal scaling in DB context?

A:

Vertical scaling: Upgrading server (CPU, RAM, SSD).

Horizontal scaling: Adding more database nodes (e.g., sharding, replicas).

 Horizontal scaling improves fault tolerance and better handles concurrent load.



### 🔹 Q14. When would you choose a NoSQL database over a relational DB?

A: When the schema is dynamic, data is hierarchical, consistency is relaxed (eventual OK), or for high-speed writes and scale — e.g., user activity logs, product catalogs.



### 🔹 Q15. How do you ensure high availability and failover in production DBs?

A:

Use master-slave replication.

Auto failover with tools like Patroni (PostgreSQL), MHA.

Backup strategies (daily, hourly).

Heartbeat & health checks.

Region-level redundancy for disaster recovery.



## ✅ Bonus Twist from Interviewer:

“Great. Let’s say your app still faces 5% slow requests despite all these. What now?”

A:

Profile application code for bottlenecks outside DB.

Analyze thread contention or network latency.

Check for N+1 queries or unoptimized ORMs.

Consider async processing for background tasks.

Review hardware limits or OS-level I/O issues.



## 🧠 Tips for You:

Always measure before optimizing.

Database fine-tuning is both an art and a science — stay data-driven.

Be clear in trade-offs: performance vs. consistency vs. availability.

