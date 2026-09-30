---
title: Database Indexing Strategies
tags: [software, databases, performance, internals]
draft: false
---
Indexes are the primary mechanism databases use to avoid full table scans and locate data efficiently. The choice of index structure has profound implications for read latency, write throughput, and the types of queries a database can serve efficiently. This note covers the three foundational indexing strategies.

---

## B-Tree (Balanced Tree)

The standard index for most relational databases. Designed to minimize disk I/O by keeping data sorted in a balanced, hierarchical tree structure.

### How It Works
- Data is organized into **nodes** (pages, typically 4-16 KB).
- **Internal nodes** act as a sorted routing map, guiding the search down the tree.
- **Leaf nodes** contain the actual data (or pointers to data rows on disk).
- The tree is always balanced: every path from root to leaf has the same length, guaranteeing predictable `O(log n)` lookup time.
- Updates happen **in-place**: when a value changes, the database modifies the existing node directly. If a node becomes full on insert, it is **split** and the tree rebalances.

### Performance Characteristics
- **Reads:** Excellent. `O(log n)` for both point lookups and range queries. The sorted structure makes `BETWEEN`, `>`, `<`, and `ORDER BY` operations highly efficient.
- **Writes:** Moderate. In-place updates can cause **random disk I/O** (seeking to the specific page). Node splits and rebalancing add overhead. Write-ahead logs (WAL) are used for crash recovery, adding sequential write cost.

### Used By
PostgreSQL, MySQL (InnoDB), SQL Server, Oracle, SQLite.

---

## LSM Tree (Log-Structured Merge Tree)

Optimized for high-velocity write throughput. Transforms random writes into sequential, append-only operations.

### How It Works
1. Incoming writes are first buffered in an in-memory sorted structure called a **memtable** (typically a red-black tree or skip list).
2. When the memtable reaches a threshold size, it is **flushed** to disk as an immutable **SSTable** (Sorted String Table).
3. Over time, multiple SSTables accumulate on disk. Background **compaction** processes periodically merge overlapping SSTables, removing deleted/overwritten entries and consolidating data.

### Performance Characteristics
- **Writes:** Excellent. All writes go to the memtable (memory), then are flushed as sequential disk writes. This avoids the random I/O penalty of B-trees, achieving significantly higher write throughput.
- **Reads:** Slower than B-trees. A read may need to check the memtable, then potentially multiple SSTables on disk to find the most recent version of a key. This is called **read amplification**.
- **Mitigation:** **Bloom filters** (probabilistic data structures) are attached to each SSTable to quickly determine if a key is definitely *not* in that file, skipping unnecessary disk reads.

### Write Amplification vs. Read Amplification
LSM trees trade **write amplification** (data is rewritten multiple times during compaction) for sequential I/O. The amplification factor depends on the compaction strategy:
- **Size-tiered compaction:** Groups similarly-sized SSTables. Lower write amplification, higher space amplification.
- **Leveled compaction:** Organizes SSTables into levels with size limits. Higher write amplification, better read performance, lower space amplification.

### Used By
Apache Cassandra, RocksDB, LevelDB, ScyllaDB, HBase, CockroachDB (storage layer), InfluxDB.

---

## Hash Index

The simplest and fastest index for exact-match lookups. Not suitable for range queries.

### How It Works
- A **hash function** takes a key and maps it directly to a **bucket** (a location in a hash table or a file offset).
- Retrieval is direct: compute the hash, go to the bucket, retrieve the value. No tree traversal needed.
- **Collisions** (two keys mapping to the same bucket) are handled via chaining (linked lists) or open addressing.

### Performance Characteristics
- **Reads:** Extremely fast -- `O(1)` average case for exact-match lookups.
- **Writes:** Fast for inserts and updates to existing keys.
- **Range Queries:** **Not supported.** Hash functions deliberately scramble key ordering to distribute them uniformly. There is no way to find "all keys between A and B" without scanning the entire table.

### Used By
Redis (internal hash tables), Memcached, PostgreSQL (hash index type, rarely used in practice), Bitcask (Riak's storage engine).

---

## Comparison Table

| Feature | B-Tree | LSM Tree | Hash Index |
| :--- | :--- | :--- | :--- |
| **Read Performance** | Excellent `O(log n)` | Moderate (read amplification) | Excellent `O(1)` |
| **Write Performance** | Moderate (random I/O) | Excellent (sequential I/O) | Fast |
| **Range Queries** | Efficient (sorted data) | Supported | Not supported |
| **Space Efficiency** | Good | Varies (compaction dependent) | Good |
| **Concurrency** | Good (page-level locking) | Excellent (append-only) | Moderate |
| **Primary Use Case** | General RDBMS workloads | Write-heavy / NoSQL | Caching, exact lookups |

---

## How to Choose

- **Use B-Trees** when you need a general-purpose index supporting mixed read/write workloads with range queries (the default for most SQL databases).
- **Use LSM Trees** when your primary bottleneck is write throughput (log ingestion, event sourcing, time-series data). Accept the trade-off of higher read latency.
- **Use Hash Indexes** when you exclusively perform exact-match lookups on a unique key and never need range scans or sorting.

---

## Related Notes
- [[Database Selection]] - Framework for choosing the right database.
- [[Database Types]] - Comparison of major database categories.
- [[Dynamic Programming]] - Subproblem optimization, a related algorithmic concept.

---

*Sources:*
- *[Designing Data-Intensive Applications](https://dataintensive.net/) - Martin Kleppmann (Chapter 3: Storage and Retrieval)*
- *[ByteByteGo - Database Indexing](https://bytebytego.com/) - ByteByteGo*
- *[LSM Tree Explained](https://dev.to/) - Dev.to*
