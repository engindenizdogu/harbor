---
title: Database Types
tags: [software, databases, architecture, system-design]
draft: false
---
A comprehensive reference of major database categories, their data models, strengths, weaknesses, and ideal use cases. This note complements [[Database Selection]] by providing the detail needed to compare specific engine families.

---

## Relational Databases (RDBMS)

**Data Model:** Structured tables with rows and columns, linked by foreign keys. Enforces a rigid schema.

**Examples:** PostgreSQL, MySQL, MariaDB, SQL Server, Oracle, SQLite

**Strengths:**
- Full ACID compliance for transactional integrity.
- Mature ecosystem with decades of optimization, tooling, and community support.
- Standardized query language (SQL) with powerful join, aggregation, and window function capabilities.
- Strong support for complex, multi-table queries.
- PostgreSQL in particular has expanded to handle JSON (`jsonb`), full-text search, and vector embeddings (`pgvector`), narrowing the gap with specialized engines.

**Weaknesses:**
- Vertical scaling by default; horizontal scaling (sharding) is complex and often requires application-level logic.
- Schema rigidity can slow iteration in early-stage products with rapidly evolving data models.
- Not ideal for hierarchical or deeply nested data structures.

**Best for:** Financial systems, e-commerce, SaaS platforms, ERP/CRM, any application where data integrity and relational querying are paramount.

---

## Document Databases

**Data Model:** Semi-structured documents (typically JSON or BSON), stored in collections. Schema-flexible -- each document in a collection can have different fields.

**Examples:** MongoDB, Couchbase, Amazon DocumentDB, Firestore

**Strengths:**
- Flexible schema allows rapid iteration without migrations.
- Natural fit for hierarchical or nested data (e.g., a blog post with embedded comments).
- Built for horizontal scaling with native sharding.
- Developer-friendly; data shape often mirrors application objects directly.

**Weaknesses:**
- Limited join capabilities compared to relational databases. Denormalization is common, which can lead to data duplication and update anomalies.
- Eventual consistency by default in distributed configurations (though tunable).
- Complex cross-document transactions are possible but less performant than in RDBMS.

**Best for:** Content management systems, user profiles, product catalogs, mobile app backends, and applications with rapidly evolving schemas.

---

## Key-Value Stores

**Data Model:** Simple key-to-value mappings. The value is opaque to the database -- it can be a string, a serialized object, a list, or a hash.

**Examples:** Redis, Amazon DynamoDB, Memcached, etcd, Riak

**Strengths:**
- Extremely fast reads and writes, often sub-millisecond (especially in-memory stores like Redis).
- Simple API: `GET`, `SET`, `DELETE`.
- Highly scalable horizontally via consistent hashing.
- Redis extends the model with data structures (sorted sets, streams, pub/sub).

**Weaknesses:**
- No query language -- you can only retrieve data by its exact key.
- No support for complex queries, joins, or aggregations.
- In-memory stores (Redis, Memcached) are limited by available RAM unless configured for disk persistence.

**Best for:** Session management, caching, feature flags, rate limiting, leaderboards, real-time counters.

---

## Wide-Column Stores

**Data Model:** Data organized into rows and column families. Each row can have a different set of columns. Designed for sparse, distributed datasets.

**Examples:** Apache Cassandra, ScyllaDB, HBase, Google Bigtable

**Strengths:**
- Designed for massive horizontal scale across hundreds or thousands of nodes.
- High write throughput with tunable consistency.
- Excellent for time-series-like workloads with known access patterns.
- Cassandra offers masterless architecture with no single point of failure.

**Weaknesses:**
- Data modeling is query-driven and counterintuitive for developers used to relational design.
- Limited ad-hoc query capability; schema must be designed around specific access patterns upfront.
- Operational complexity is high.

**Best for:** IoT data at scale, messaging platforms, event logging, recommendation feeds, any workload requiring extreme write throughput across geographically distributed clusters.

---

## Graph Databases

**Data Model:** Nodes (entities) and edges (relationships), both of which can carry properties. Relationships are first-class citizens stored directly, not computed via joins.

**Examples:** Neo4j, Amazon Neptune, ArangoDB, JanusGraph

**Strengths:**
- Queries involving deep, multi-hop relationships (e.g., "friends of friends who liked X") are orders of magnitude faster than equivalent SQL joins.
- Intuitive data modeling for relationship-rich domains.
- Cypher (Neo4j) and Gremlin (TinkerPop) provide expressive graph query languages.

**Weaknesses:**
- Not suited for bulk analytical scans or simple CRUD workloads.
- Scaling horizontally is harder than in document or key-value stores.
- Smaller ecosystem and community compared to RDBMS or MongoDB.

**Best for:** Social networks, recommendation engines, fraud detection, knowledge graphs, network topology analysis, identity and access management.

---

## Time-Series Databases

**Data Model:** Optimized for data points indexed by timestamps. Stores measurements sequentially and supports efficient time-range queries and rollups.

**Examples:** InfluxDB, TimescaleDB (PostgreSQL extension), QuestDB, Prometheus

**Strengths:**
- Purpose-built for extremely high write (ingest) throughput of timestamped data.
- Efficient compression and downsampling of time-series data.
- Native support for time-windowed aggregations (`avg over last 5 minutes`).
- Automatic data retention policies (e.g., delete data older than 90 days).

**Weaknesses:**
- Not general-purpose; poor fit for non-temporal queries or complex relational logic.
- Limited transaction support.

**Best for:** Infrastructure monitoring (CPU, memory, network metrics), IoT sensor data, financial market tick data, application performance management (APM).

---

## NewSQL Databases

**Data Model:** Relational (SQL interface) but built on a distributed, horizontally scalable architecture. Aims to combine the best of RDBMS and NoSQL.

**Examples:** CockroachDB, Google Spanner, TiDB, YugabyteDB

**Strengths:**
- Full ACID compliance with horizontal scalability -- the "holy grail" that traditional RDBMS and NoSQL each sacrifice one side of.
- Standard SQL interface, making migration from traditional RDBMS easier.
- Designed for global distribution with strong consistency (Spanner uses TrueTime; CockroachDB uses hybrid logical clocks).

**Weaknesses:**
- Higher latency per-transaction compared to a local, single-node RDBMS due to distributed consensus overhead.
- Relatively newer ecosystem; less battle-tested community tooling.
- Can be expensive, especially managed offerings.

**Best for:** High-traffic, globally distributed applications that require both ACID transactions and horizontal scalability (e.g., global financial platforms, multi-region SaaS).

---

## Vector Databases

**Data Model:** Stores high-dimensional vector embeddings and supports efficient approximate nearest neighbor (ANN) search.

**Examples:** Pinecone, Milvus, Weaviate, Qdrant, Chroma, PostgreSQL (`pgvector`)

**Strengths:**
- Purpose-built for semantic similarity search, enabling queries like "find items most similar to this embedding."
- Critical infrastructure for LLM-powered applications, particularly Retrieval Augmented Generation (RAG).
- Support metadata filtering and hybrid search (combining vector similarity with traditional filters).

**Weaknesses:**
- Not a general-purpose database; intended as a specialized layer alongside a primary store.
- ANN search is approximate, not exact -- accuracy depends on the index algorithm (HNSW, IVF, etc.).
- Rapidly evolving space with shifting best practices.

**Best for:** Semantic search, recommendation engines, RAG pipelines for LLMs, image/audio similarity, anomaly detection.

---

## Summary Comparison

| Type            | Data Model                 | Consistency   | Scaling            | Query Complexity  | Maturity  |
| :-------------- | :------------------------- | :------------ | :----------------- | :---------------- | :-------- |
| **Relational**  | Tables, Rows, Foreign Keys | Strong (ACID) | Vertical (default) | Very High (SQL)   | Very High |
| **Document**    | JSON/BSON Documents        | Tunable       | Horizontal         | Moderate          | High      |
| **Key-Value**   | Key &rarr; Value           | Tunable       | Horizontal         | Very Low          | High      |
| **Wide-Column** | Row + Column Families      | Tunable       | Horizontal         | Low-Moderate      | High      |
| **Graph**       | Nodes + Edges              | Varies        | Moderate           | High (traversals) | Moderate  |
| **Time-Series** | Timestamped Points         | Varies        | Horizontal         | Moderate (time)   | Moderate  |
| **NewSQL**      | Tables (distributed)       | Strong (ACID) | Horizontal         | Very High (SQL)   | Growing   |
| **Vector**      | Embeddings                 | Varies        | Horizontal         | Specialized (ANN) | Early     |

---

## Related Notes
- [[Database Selection]] - Framework for choosing the right database for your application.
- [[Database Indexing Strategies]] - B-Tree, LSM Tree, and Hash Index internals.

---

*Sources:*
- *[Database Types Comparison](https://www.splunk.com/en_us/blog/learn/database-types.html) - Splunk*
- *[SQL vs NoSQL](https://www.datacamp.com/blog/sql-vs-nosql-databases) - DataCamp*
- *[When to Use Graph Databases](https://neo4j.com/use-cases/) - Neo4j*
