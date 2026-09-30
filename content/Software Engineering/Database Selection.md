---
title: Database Selection
tags: [software, databases, architecture, system-design]
draft: false
---
Choosing the right database is one of the most consequential architectural decisions in application development. A poor choice can lead to performance bottlenecks, scaling nightmares, and expensive migrations. This note provides a structured framework for evaluating and selecting a database engine.

## The Query-First Strategy

Before evaluating any specific product, write out your application's most critical, frequent, and expensive queries. Different database engines are physically optimized for different "shapes" of data retrieval:

| Query Shape           | Description                                        | Optimal Engine Type                     |
| :-------------------- | :------------------------------------------------- | :-------------------------------------- |
| **Point Lookups**     | Retrieving a single record by a unique key         | Key-Value stores (Redis, DynamoDB)      |
| **Complex Joins**     | Linking multiple normalized entities together      | Relational (PostgreSQL, MySQL)          |
| **Aggregations**      | Scanning large datasets for analytics (SUM, AVG)   | Columnar / OLAP (ClickHouse, BigQuery)  |
| **Vector Similarity** | Searching by semantic meaning / embedding distance | Vector DBs (Pinecone, Milvus, Weaviate) |
| **Graph Traversals**  | Exploring deep, multi-hop relationships            | Graph DBs (Neo4j, Amazon Neptune)       |
| **Time-Range Scans**  | Querying sequential data by time windows           | Time-Series DBs (InfluxDB, TimescaleDB) |

If you design your queries first, the database choice often becomes obvious based on which engine handles those specific operations most efficiently.

## Core Selection Criteria

Evaluate every candidate database against these fundamental dimensions:

### 1. Data Model and Structure
- **Structured data** with well-defined schemas and relationships &rarr; Relational (SQL).
- **Semi-structured / evolving schemas** (JSON-like documents) &rarr; Document stores.
- **Highly connected data** where relationships are first-class citizens &rarr; Graph databases.
- **Simple key-to-value mappings** &rarr; Key-Value stores.

### 2. Workload Pattern
- **Read-heavy:** Applications serving dashboards, search results, or content pages. Caching layers (Redis) and read replicas help here.
- **Write-heavy:** Logging pipelines, telemetry ingestion, IoT sensor streams. [[Database Indexing Strategies|LSM-tree based]] engines excel at sequential write throughput.
- **Mixed (OLTP):** Standard transactional applications (e-commerce, SaaS). Relational databases with B-tree indexes are the default.
- **Analytical (OLAP):** Business intelligence and reporting. Columnar stores scan and aggregate large datasets efficiently.

> Never run heavy analytical queries directly on your primary transactional database. This causes lock contention and API timeouts. Use a separate analytical store or read replica.

### 3. Consistency Requirements
This is governed by two foundational concepts: **[[#ACID vs BASE]]** and the **[[#The CAP Theorem]]**.

- **Strict consistency (ACID):** Required for financial transactions, inventory management, order processing. Choose a relational database.
- **Eventual consistency (BASE):** Acceptable for social feeds, recommendation caches, analytics counters. NoSQL databases trade consistency for availability and speed.

### 4. Scalability Model
- **Vertical scaling (scale up):** Adding more CPU, RAM, and disk to a single server. Simpler to manage but has a hard ceiling. Traditional RDBMS default to this model.
- **Horizontal scaling (scale out):** Distributing data across multiple nodes via sharding or replication. Required for web-scale applications. NoSQL and NewSQL databases are designed for this.

### 5. Operational Considerations
- **Managed vs. self-hosted:** Managed services (AWS RDS, Google Cloud SQL, MongoDB Atlas) reduce operational burden but increase vendor lock-in and cost.
- **Team expertise:** A highly scalable distributed database is worthless if the team cannot tune, monitor, and debug it. Factor in the learning curve.
- **Ecosystem and tooling:** ORM support, migration tools, monitoring dashboards, community size, and documentation quality all matter for long-term productivity.
- **Cost model:** Licensing, storage, compute, and I/O costs vary dramatically. Some cloud databases charge per-read/write operation, which can produce surprises at scale.

### 6. AI and Modern Workloads
With the rise of LLMs and Retrieval Augmented Generation (RAG), native vector search capability is increasingly important. Some relational databases (PostgreSQL via `pgvector`) now support this, while purpose-built vector databases offer more advanced features like metadata filtering and hybrid search.

---

## Theoretical Foundations

### ACID vs BASE

ACID and BASE represent two opposing philosophies for managing transactions and data integrity.

**ACID (Atomicity, Consistency, Isolation, Durability)** is the traditional model for relational databases. It prioritizes strict data integrity:

| Property | Meaning |
| :--- | :--- |
| **Atomicity** | Transactions are all-or-nothing. If any part fails, the entire transaction rolls back. |
| **Consistency** | The database transitions from one valid state to another, enforcing all defined rules and constraints. |
| **Isolation** | Concurrent transactions do not interfere with each other; they appear to execute sequentially. |
| **Durability** | Once a transaction is committed, it persists permanently, even after a system crash. |

**BASE (Basically Available, Soft-state, Eventually consistent)** is the model adopted by many NoSQL databases to achieve massive scale:

| Property | Meaning |
| :--- | :--- |
| **Basically Available** | The system guarantees a response for every request, though it may not be the most current data. |
| **Soft-state** | The system state may change over time without user input, as data propagates across nodes. |
| **Eventually Consistent** | All replicas will converge to the same state given enough time, but reads may temporarily return stale data. |

| Dimension | ACID | BASE |
| :--- | :--- | :--- |
| **Primary Goal** | Data integrity and correctness | Availability and scalability |
| **Consistency** | Immediate / Strong | Eventual |
| **Performance** | Can be slower due to strict locking | Generally faster and more scalable |
| **Typical Use** | Financial systems, ERP, inventory | Social networks, analytics, web apps |

### The CAP Theorem

The CAP theorem (Brewer's theorem) states that in a distributed data store, you can only simultaneously guarantee **two** of three properties:

- **Consistency (C):** Every read receives the most recent write. All nodes see the same data at the same time (linearizability).
- **Availability (A):** Every request receives a non-error response, without guarantee that it contains the most recent write.
- **Partition Tolerance (P):** The system continues to operate despite network failures that prevent nodes from communicating.

Since network partitions are **inevitable** in distributed systems, the real choice is between **CP** and **AP**:

- **CP (Consistency + Partition Tolerance):** Prioritizes correctness. During a partition, the system may refuse requests to prevent serving stale data. Examples: HBase, MongoDB (default config), Redis Cluster.
- **AP (Availability + Partition Tolerance):** Prioritizes uptime. During a partition, the system continues serving requests but may return stale data. Examples: Cassandra, DynamoDB, CouchDB.

> The term "Consistency" means different things in CAP vs. ACID. In CAP, it refers to linearizability (all nodes see the same data simultaneously). In ACID, it refers to the database satisfying all integrity constraints after a transaction.

---

## Indexing Strategies

The choice of underlying index structure directly impacts read/write performance. See [[Database Indexing Strategies]] for a deep dive.

| Index Type     | Read Speed                    | Write Speed                | Range Queries | Best For                                 |
| :------------- | :---------------------------- | :------------------------- | :------------ | :--------------------------------------- |
| **B-Tree**     | Excellent `O(log n)`          | Moderate (random I/O)      | Supported     | General RDBMS (PostgreSQL, MySQL)        |
| **LSM Tree**   | Moderate (read amplification) | Excellent (sequential I/O) | Supported     | Write-heavy / NoSQL (Cassandra, RocksDB) |
| **Hash Index** | Excellent `O(1)`              | Fast                       | Not supported | Caching, exact-match lookups (Redis)     |

---

## Architectural Patterns

### Polyglot Persistence

The "SQL vs. NoSQL" binary is outdated. Modern architectures often adopt **polyglot persistence**: using different databases for different parts of the same application, each chosen for its strengths.

**Example architecture:**
- **PostgreSQL** as the transactional source of truth for users, orders, and billing.
- **Redis** as an in-memory cache for session data and hot queries.
- **ClickHouse** for real-time analytics dashboards.
- **Pinecone** for vector similarity search powering a recommendation engine.

**Best practices for polyglot persistence:**
1. **Define data ownership** -- clearly designate which database is the source of truth for each entity.
2. **Use event-driven sync** -- use message queues (Kafka, RabbitMQ) or CDC (Change Data Capture) to keep stores synchronized.
3. **Plan for eventual consistency** -- strict ACID compliance across multiple databases is extremely difficult.
4. **Use abstraction layers** -- repository patterns or service APIs decouple application code from specific database implementations.

**When to avoid polyglot persistence:**
- Small teams or tight budgets (operational overhead is significant).
- Strict cross-entity ACID requirements.
- Early-stage MVPs (prioritize simplicity until bottlenecks are clear).

### Core + Specialized Pattern

The recommended modern approach for most robust applications:

1. **Core Transactional Layer:** A rock-solid relational database (typically PostgreSQL) for primary business entities and the source of truth.
2. **Specialized Serving Layers:** Add secondary databases only when the core database fails to meet specific latency or throughput SLAs:
   - Cache layer for sub-millisecond reads.
   - Analytical store for heavy aggregations.
   - Vector store for AI/ML features.

---

## Decision Checklist

Use this checklist when evaluating a database for a new project:

- [ ] Have I identified my most critical and expensive queries?
- [ ] Is my data structured, semi-structured, or graph-like?
- [ ] Is my workload read-heavy, write-heavy, or mixed?
- [ ] Do I need strict ACID consistency or can I tolerate eventual consistency?
- [ ] Do I need to scale horizontally (sharding) or will vertical scaling suffice?
- [ ] Do I need vector search or other AI-native capabilities?
- [ ] Does my team have the expertise to operate this database?
- [ ] Have I evaluated the total cost of ownership (licensing, cloud, ops)?
- [ ] Have I run a proof-of-concept with representative data volumes and simulated load?
- [ ] Am I choosing based on the physics of my data, not hype?

---

## Common Pitfalls

1. **Mixing OLTP and OLAP workloads** on a single database, causing lock contention.
2. **Choosing based on hype** rather than workload fit (e.g., adopting a distributed database for a small app).
3. **Underestimating operational complexity** of distributed databases.
4. **Premature optimization** -- using polyglot persistence before understanding actual bottlenecks.
5. **Ignoring migration cost** -- switching databases later is extremely expensive.

---

## Related Notes
- [[Database Types]] - Detailed comparison of relational, NoSQL, NewSQL, graph, and time-series databases.
- [[Database Indexing Strategies]] - B-Tree, LSM Tree, and Hash Index internals.
- [[Polyglot Programming]] - Multi-language application architectures.

---

*Sources:*
- *[Choosing the Right Database](https://medium.com/) - Medium*
- *[CAP Theorem Explained](https://www.ibm.com/topics/cap-theorem) - IBM*
- *[ACID vs BASE](https://aws.amazon.com/compare/the-difference-between-acid-and-base-database/) - AWS*
- *[ByteByteGo - Database Internals](https://bytebytego.com/) - ByteByteGo*
