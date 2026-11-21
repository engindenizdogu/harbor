---
title: MapReduce Patterns
tags: [data-science, big-data, mapreduce, hadoop, distributed-computing, auto-captured]
draft: false
---
Most MapReduce jobs are variations of a few recurring patterns. This note shows the shuffle in detail, a runnable word count, and the standard patterns: combiners, inverted index, joins, top-N, matrix multiplication and skew handling. For the model itself, HDFS and YARN, see [[Hadoop and MapReduce]].

All code here was run locally. Hadoop Streaming scripts were tested with a Unix pipeline, and the other patterns with a small in-memory simulation that mimics the map, shuffle and reduce phases.

## The Shuffle in Detail
The shuffle is where most of a job's time and network traffic go.
1. **Map side:** each mapper writes its `(key, value)` output to a memory buffer. When the buffer fills, it is partitioned, sorted by key and spilled to local disk. Spill files are merged at the end.
2. **Partitioning:** a **partitioner** decides which reducer receives each key. The default is `hash(key) mod number_of_reducers`, so all values for a key reach the same reducer.
3. **Copy:** each reducer fetches its partition from every mapper over the network.
4. **Reduce side:** fetched data is merge-sorted, so the reducer sees keys in order, with all values of one key together.

Consequences:
- Everything with the same key lands on **one** reducer. A very common key makes one reducer much slower than the others (see Skew below).
- Output is sorted **within** each reducer, not globally, unless you use a range partitioner or a single reducer.
- Intermediate map output goes to local disk and the final output to HDFS, which is why MapReduce is slow for iterative work and why [[Apache Spark]] keeps data in memory.
- **Number of reducers:** too few means long, serial reducers. Too many means many tiny output files and overhead. It is set per job.

## Word Count with Hadoop Streaming
Hadoop Streaming lets any program that reads standard input and writes standard output act as mapper or reducer, with tab-separated `key<TAB>value` lines.

`mapper.py`:
```python
#!/usr/bin/env python3
import sys
for line in sys.stdin:
    for word in line.lower().split():
        print(f"{word}\t1")
```
`reducer.py`:
```python
#!/usr/bin/env python3
import sys
current, total = None, 0
for line in sys.stdin:                     # input arrives sorted by key
    word, count = line.rstrip("\n").split("\t")
    if word != current:
        if current is not None:
            print(f"{current}\t{total}")
        current, total = word, 0
    total += int(count)
if current is not None:
    print(f"{current}\t{total}")
```
Test it locally, with `sort` standing in for the shuffle:
```bash
cat in.txt | python3 mapper.py | sort | python3 reducer.py
```
For the input `the quick brown fox / the lazy dog / the fox` this prints `brown 1, dog 1, fox 2, lazy 1, quick 1, the 3`.

Note that, unlike the Java API, a streaming reducer receives a **flat sorted stream**, not grouped values. It must detect key changes itself, as above. On a cluster, the job is submitted with the `hadoop-streaming` jar, passing `-mapper`, `-reducer`, `-input` and `-output`.

**The same job in PySpark** (output identical):
```python
counts = (sc.textFile("in.txt").flatMap(lambda l: l.lower().split())
            .map(lambda w: (w, 1)).reduceByKey(lambda a, b: a + b))
```
Spark's `reduceByKey` already applies a combiner-style local aggregation before the shuffle. See [[PySpark Cheat Sheet]].

## Combiners
A **combiner** is a mini-reducer run on each mapper's output before the shuffle. It shrinks the data sent over the network.

Example: a word count over 1,000 lines (3,750 words in total). Without a combiner, 3,750 pairs cross the shuffle. With the reducer reused as combiner, only 24 do, and the final counts are identical.

Rules:
- The framework may run a combiner **zero, one or many times**, so the job must be correct without it.
- The operation must be **associative and commutative** (sum, count, min, max). The combiner's output type must match the reducer's input type.
- **Averages break this.** An average of averages is wrong. Emit `(sum, count)` pairs and divide in the reducer.
- **In-mapper combining** goes further: keep a dictionary inside the mapper, aggregate there, and emit once at the end. It saves more but uses mapper memory.

## Inverted Index
Maps each word to the documents containing it. It is the core of search indexing.
- **Map:** for each document, emit `(word, doc_id)` for each distinct word.
- **Reduce:** collect and sort the document ids for each word.

For three documents (`d1: the cat sat`, `d2: the dog sat`, `d3: a cat ran`) the output includes `cat: [d1, d3]`, `sat: [d1, d2]`, `the: [d1, d2]` and `ran: [d3]`.

## Joins
### Reduce-side join
Works for any two datasets, however large.
- **Map:** emit `(join_key, (source_tag, record))`, where the tag says which dataset the record came from.
- **Reduce:** for each key, split the values by tag and emit the cross product.

Example: users (`u1 Ana, u2 Bo`) joined with orders (`o1/u1/30, o2/u2/15, o3/u1/12, o4/u3/99`) gives `(u1, Ana, o1, 30)`, `(u1, Ana, o3, 12)` and `(u2, Bo, o2, 15)`. Order `o4` has no matching user and drops out, which is an **inner join**. Emitting unmatched records gives outer joins.

The whole shuffle carries both datasets, which makes it expensive. A refinement called **secondary sort** guarantees the smaller dataset arrives first, so the reducer need not buffer it.

### Map-side (broadcast) join
If one dataset is small, load it into memory in every mapper (Hadoop's distributed cache) and join while mapping. There is **no shuffle and no reduce phase**, so it is much faster. Spark's `F.broadcast()` does the same thing.

## Top-N
Find the $N$ largest values (or most frequent words, or highest scores).
- **Map and combine:** each mapper keeps only its **local top $N$** and emits those.
- **Reduce:** a **single reducer** merges the local lists and keeps the global top $N$.

On 100 shuffled numbers with $N=3$, only 9 values (3 per mapper across 3 mappers) reached the reducer instead of 100, and the answer was `[100, 99, 98]`. This works because any global top-$N$ item must also be in its own mapper's top $N$. The single reducer is not a bottleneck, since it only sees $N \times$ mappers records.

## Matrix Multiplication
For $C = A \times B$, element $C_{ik}=\sum_j A_{ij}B_{jk}$. A one-pass version:
- **Map:** each $A_{ij}$ is sent to every output cell in its row, `((i, k), ("A", j, value))` for all $k$. Each $B_{jk}$ is sent to every output cell in its column, `((i, k), ("B", j, value))` for all $i$.
- **Reduce:** for each cell $(i,k)$, pair values by $j$, multiply and sum.

Checked on $\begin{pmatrix}1&2\\3&4\end{pmatrix}\times\begin{pmatrix}5&6\\7&8\end{pmatrix}$, the job returned $\begin{pmatrix}19&22\\43&50\end{pmatrix}$, which is correct. Each input element is replicated many times, so for large dense matrices a two-pass version or a different tool is better. For sparse data, MapReduce is a natural fit.

## Data Skew and Salting
When one key dominates, one reducer gets most of the data and the whole job waits for it.

In a test with 10,000 records, of which 9,000 had the key `hot`, and 4 reducers, the reducer loads were `[249, 251, 249, 9251]`: one reducer did over 90% of the work.

**Salting:** append a random suffix to the hot key (`hot#0` through `hot#3`) in the mapper, so it is split into several keys. A second small step strips the suffix and merges the partial totals. After salting, loads were `[249, 4757, 249, 4745]` and the merged total for `hot` was still correct (9,000).

The split is uneven because the four salted keys happened to hash to only two of the four reducers. Salting reduces the worst load but does not guarantee balance, so use enough salts. Other fixes: a custom partitioner, a combiner (often removes most of the skew for aggregations), and handling the hot key in a separate map-side join.

## Failure Handling and Speculation
- **Task failure:** a failed map or reduce task is re-run on another node, up to a retry limit. Because tasks are deterministic and map outputs are stored, no other work is lost.
- **Speculative execution:** if a task is much slower than its peers (a **straggler**), the framework starts a duplicate on another node and keeps whichever finishes first. Turn it off for tasks with side effects, such as writing to an external database.
- **Idempotent output:** each task writes to a temporary location, and only successful attempts are committed to the final output directory.

## Practical Tuning
- **Combiners first:** the cheapest way to cut shuffle volume.
- **Compress** intermediate map output to reduce network traffic.
- **Avoid many small files:** each file creates at least one map task, and small files overload the NameNode. Combine inputs or use sequence files or Parquet.
- **Right-size splits:** by default one map task per HDFS block (commonly 128 MB).
- **Pick the right tool:** iterative algorithms (machine learning, graph algorithms) and interactive queries run much faster on [[Apache Spark]] or similar engines. MapReduce remains reasonable for large one-pass batch jobs.

## Related Notes
- [[Hadoop and MapReduce]]: the model, HDFS and YARN.
- [[Apache Spark]]: in-memory successor.
- [[PySpark Cheat Sheet]]: the same patterns with DataFrames.
- [[Big Data Fundamentals and Architecture]]: where batch processing fits.
