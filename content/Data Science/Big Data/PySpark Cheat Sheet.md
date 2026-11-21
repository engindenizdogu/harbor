---
title: PySpark Cheat Sheet
tags: [data-science, big-data, spark, pyspark, dataframe, auto-captured]
draft: false
---
A working reference for the PySpark API, organized by task. Every snippet was run in local mode (PySpark 4.3.0, Java 17, Python 3.13) on small example data. For architecture, RDDs and lazy evaluation, see [[Apache Spark]]. Official reference: [PySpark API documentation](https://spark.apache.org/docs/latest/api/python/index.html).

## Setup
```bash
pip install pyspark pandas pyarrow
```
```python
from pyspark.sql import SparkSession, functions as F, Window

spark = (SparkSession.builder
         .master("local[*]")                      # all local cores; omit on a real cluster
         .appName("example")
         .config("spark.sql.shuffle.partitions", "8")
         .getOrCreate())
```
- **Java is required** (JDK 17 worked). PySpark starts a JVM behind the Python API.
- **Workers use their own Python.** Spark launches worker processes with whatever `python3` is on the path, not necessarily your virtual environment. If a UDF fails with `ModuleNotFoundError` for a package you installed, set `PYSPARK_PYTHON` to the environment's interpreter before starting.
- **pyarrow:** in my setup even a plain Python UDF failed in the worker until `pyarrow` was available, so install it.
- **pandas versions:** the pandas API on Spark (below) failed to import with pandas 3.1 and worked with pandas 2.3. Pin `pandas<3` if you use it.

## Data Model in One Minute
- A **DataFrame** is a distributed table with a schema, like a pandas DataFrame that is split into partitions across machines.
- **Transformations** (`select`, `filter`, `join`, ...) are lazy: they only build a plan. **Actions** (`show`, `count`, `collect`, `write`) run it.
- The **Catalyst optimizer** rewrites the plan, so the order you write operations in is not the order they run.
- DataFrames are immutable: every operation returns a new one.

## Creating DataFrames
```python
rows = [("A","tug",12.5,3), ("A","cargo",8.1,5), ("B","tug",14.0,2),
        ("B","cargo",9.7,None), ("C","ferry",18.2,7), ("C","tug",11.0,1)]
df = spark.createDataFrame(rows, ["port","type","speed","trips"])
df.printSchema()      # port: string, type: string, speed: double, trips: long
df.show()             # first 20 rows, truncated columns
df.count(); df.columns; df.dtypes
```
- `spark.createDataFrame(pandas_df)` converts a pandas DataFrame, and `df.toPandas()` collects a Spark one back. `toPandas()` pulls everything to the driver, so use it only on small results.
- Python `int` is inferred as `long`. Set an explicit schema when types matter (see Reading and Writing).

## Selecting, Filtering, Adding Columns
```python
out = (df.select("port", "type", (F.col("speed") * 1.852).alias("kmh"))
         .filter(F.col("kmh") > 20)
         .withColumn("fast", F.when(F.col("kmh") > 30, "yes").otherwise("no")))
```
| Task | Code |
|---|---|
| Choose columns | `df.select("a", F.col("b"))` |
| Filter rows | `df.filter(F.col("x") > 5)` or `df.where("x > 5")` |
| Add or replace a column | `df.withColumn("c", expr)` |
| Rename | `df.withColumnRenamed("old", "new")` |
| Drop columns | `df.drop("a")` |
| Distinct | `df.distinct()`, `df.dropDuplicates(["a"])` |
| Sort | `df.orderBy(F.desc("x"))` |
| Cast | `F.col("x").cast("int")` |
| Conditional | `F.when(cond, a).otherwise(b)` |
| String matching | `F.col("s").like("A%")`, `.rlike(regex)`, `.isin(["a","b"])` |

Use `F.col("name")` for expressions. Plain Python operators such as `df.speed * 2` also work, but `F.col` avoids ambiguity after joins.

## Aggregation
```python
df.groupBy("port").agg(
    F.count("*").alias("n"),
    F.avg("speed").alias("avg_speed"),
    F.sum("trips").alias("trips")).orderBy("port").show()
```
Result: port A has n = 2, average speed 10.3, 8 trips; B has 11.85 and 2 trips (the null counts as nothing in the sum); C has 14.6 and 8 trips. Aggregates ignore nulls, but `count("*")` counts every row.

Other useful aggregates: `F.min`, `F.max`, `F.countDistinct`, `F.collect_list`, `F.collect_set`, `F.stddev`, `F.percentile_approx`.

## Missing Values
```python
df.na.fill({"trips": 0})      # fill by column
df.dropna()                   # drop any row with a null: 5 of 6 rows remain here
df.dropna(subset=["trips"])
df.filter(F.col("trips").isNull())
```
Comparing with `== None` does not work in Spark. Use `isNull()` and `isNotNull()`.

## Joins
```python
ports = spark.createDataFrame([("A","Newark"), ("B","Brooklyn"), ("D","Staten Island")], ["port","name"])

df.join(ports, "port", "left")                 # keeps C, with name = NULL
df.join(F.broadcast(ports), "port", "inner")   # only A and B rows
```
- Join types: `inner` (default), `left`, `right`, `outer`, `left_semi` (keep left rows that have a match), `left_anti` (keep left rows with no match).
- Joining on a column name (`"port"`) keeps one copy of the key. Joining on an expression (`df.a == other.a`) keeps both, which causes ambiguous-column errors later.
- **Broadcast joins:** `F.broadcast(small_df)` ships the small table to every executor, which avoids shuffling the big one. The physical plan shows `BroadcastHashJoin` when it works.

## Window Functions
```python
w = Window.partitionBy("port").orderBy(F.desc("speed"))
df.withColumn("rank", F.row_number().over(w)) \
  .withColumn("prev",  F.lag("speed").over(w))
```
In this data, the fastest vessel in each port gets rank 1 with `prev` = null, and the next gets rank 2 with `prev` equal to the first one's speed.
- Ranking: `row_number`, `rank`, `dense_rank`. Neighbors: `lag`, `lead`. Running totals: `F.sum("x").over(w.rowsBetween(Window.unboundedPreceding, Window.currentRow))`.
- A window with no `partitionBy` moves all data into one partition and is slow on large tables.

## Spark SQL
```python
df.createOrReplaceTempView("vessels")
spark.sql("SELECT port, MAX(speed) AS m FROM vessels GROUP BY port ORDER BY port").show()
```
SQL and the DataFrame API compile to the same plan, so choose by readability. Views are visible only inside the session.

## User-Defined Functions
```python
from pyspark.sql.functions import udf, pandas_udf
import pandas as pd

@udf("string")
def size(s):                       # runs row by row in Python
    return "fast" if s and s > 12 else "slow"

@pandas_udf("double")
def knots_to_kmh(s: pd.Series) -> pd.Series:   # runs on batches of rows
    return s * 1.852

df.withColumn("cls", size("speed")).withColumn("kmh", knots_to_kmh("speed"))
```
- Python UDFs are opaque to the optimizer and slower than built-in functions. Prefer `pyspark.sql.functions` whenever one exists.
- **Pandas UDFs** process a batch at a time through Arrow, so they are much faster than row-by-row UDFs.

## Reading and Writing
```python
df.write.mode("overwrite").partitionBy("port").parquet("out/p")
spark.read.parquet("out/p")

from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
schema = StructType([StructField("port", StringType()), StructField("type", StringType()),
                     StructField("speed", DoubleType()), StructField("trips", IntegerType())])
spark.read.schema(schema).option("header", True).csv("data/*.csv")
df.write.mode("overwrite").option("header", True).csv("out/c")
```
- **Parquet** is the default choice for analytics: columnar, compressed, and it stores the schema. The output above is a folder, not a file, with a `_SUCCESS` marker and one subfolder per partition value (`port=A`, `port=B`, `port=C`).
- **Partition columns move.** When Parquet is read back, the partition column (`port`) appears as the **last** column.
- **CSV:** `inferSchema=True` needs an extra pass over the data, and an explicit schema is faster and safer.
- **Write modes:** `append`, `overwrite`, `ignore`, `error` (default).
- Other formats: `.json(...)`, `.orc(...)`, `.format("delta")` (with the Delta library), and `.jdbc(...)`.

## Partitions, Caching, and Performance
```python
df.rdd.getNumPartitions()          # 2 in local[2]
df.repartition(4)                  # full shuffle to 4 partitions
df.repartition(4).coalesce(2)      # merge down to 2 without a full shuffle
df.cache(); df.count()             # cache fills on the first action
df.unpersist()
df.groupBy("port").count().explain()
```
- **Shuffles are the main cost.** `groupBy`, `join` and `repartition` redistribute data across the network. The plan shows them as `Exchange`.
- `repartition(n)` can increase or decrease partitions with a shuffle. `coalesce(n)` only decreases, without a full shuffle.
- `spark.sql.shuffle.partitions` (default 200) sets the partition count after a shuffle. It is far too high for small data and may be too low for huge data.
- **Cache** a DataFrame only if you reuse it several times. `df.is_cached` confirms it.
- **Adaptive Query Execution** appears in plans as `AdaptiveSparkPlan` and adjusts partition counts and join strategies at run time.
- **Read `explain()`:** look for `Exchange` (shuffle), `BroadcastHashJoin` (good for small tables), and `Filter`/`Project` pushed down to the scan.
- **Avoid `collect()`** on big data. It pulls every row into the driver's memory.

## MLlib Pipelines
```python
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

train, test = sdf.randomSplit([0.7, 0.3], seed=42)
pipe = Pipeline(stages=[
    VectorAssembler(inputCols=feature_cols, outputCol="raw"),
    StandardScaler(inputCol="raw", outputCol="features"),
    LogisticRegression(featuresCol="features", labelCol="label")])
model = pipe.fit(train)
ev = BinaryClassificationEvaluator(labelCol="label", metricName="areaUnderROC")
ev.evaluate(model.transform(test))
```
- MLlib estimators expect **one vector column** of features, which `VectorAssembler` builds from many columns. Categorical columns go through `StringIndexer` and `OneHotEncoder` first.
- A `Pipeline` chains the steps so the same transformations apply at training and prediction time.
- **Result** on the breast cancer dataset (569 rows, 30 features): test AUC 0.986.

**Cross-validation and tuning:**
```python
lr = pipe.getStages()[-1]
grid = (ParamGridBuilder().addGrid(lr.regParam, [0.0, 0.1])
                          .addGrid(lr.elasticNetParam, [0.0, 1.0]).build())
cv = CrossValidator(estimator=pipe, estimatorParamMaps=grid, evaluator=ev, numFolds=3, seed=1).fit(train)
```
Average cross-validated AUC for (`regParam`, `elasticNetParam`): (0, 0) = 0.994, (0, 1) = 0.994, (0.1, 0) = 0.996, (0.1, 1) = 0.987. The best model (0.1, 0) scored 0.988 on the test set. `elasticNetParam=1.0` means a pure L1 penalty, and 0.0 means pure L2. See [[Regularization]].

### Feature selection in Spark
```python
from pyspark.ml.feature import VarianceThresholdSelector, UnivariateFeatureSelector

VarianceThresholdSelector(featuresCol="features", outputCol="v", varianceThreshold=1.0).fit(asm)
(UnivariateFeatureSelector(featuresCol="features", labelCol="label", outputCol="sel")
   .setFeatureType("continuous").setLabelType("categorical")
   .setSelectionMode("numTopFeatures").setSelectionThreshold(5))
```
- `VarianceThresholdSelector` kept 10 of the 30 raw (unscaled) features at threshold 1.0, because variance depends on scale.
- L1 selection: a `LogisticRegression` with `elasticNetParam=1.0` and `regParam=0.05` on standardized features kept 4 non-zero coefficients out of 30 (`model.coefficients`).
- `UnivariateFeatureSelector` takes its feature and label types through setters, not constructor arguments (the constructor raised a `TypeError` for `featureType`).
- **Verify it before trusting it.** In my run, `numTopFeatures=5` returned the first five columns (`mean_radius` through `mean_smoothness`), while scikit-learn's F-test ranks `worst concave points`, `worst perimeter` and `mean concave points` at the top. I did not find the cause. Compare against a known ranking (for example scikit-learn's `f_classif`) on your own data. `ChiSqSelector` treats every distinct value of a feature as a category, so on continuous data its picks are not comparable with the chi-square scores in [[Feature Selection Methods]] either.

## Structured Streaming
```python
q = (spark.readStream.format("rate").option("rowsPerSecond", 20).load()   # test source
       .withWatermark("timestamp", "10 seconds")
       .groupBy(F.window("timestamp", "2 seconds")).count()
       .writeStream.outputMode("update").format("memory").queryName("agg").start())
spark.sql("SELECT * FROM agg").show()
q.stop()
```
- A streaming DataFrame uses the same API as a batch one, with `readStream` and `writeStream`. Real sources include Kafka, files and sockets (see [[Stream Processing and Event Streaming]]).
- The built-in `rate` source and `memory` sink are for testing. After 6 seconds this query held 7 rows (one per 2-second window).
- **Output modes:** `append` (only finalized rows), `update` (changed rows), `complete` (whole result table).
- A **watermark** says how late data may arrive, so Spark can drop old window state. Without it, state grows forever.
- For a full streaming example with Kafka and monitoring, see [[Correlation Drift Monitoring with Spark]].

## Pandas API on Spark
```python
import pyspark.pandas as ps
psdf = ps.DataFrame({"port": ["A","A","B"], "speed": [12.5, 8.1, 14.0]})
psdf.groupby("port")["speed"].mean()      # pandas syntax, runs distributed
sdf = psdf.to_spark()                      # to a Spark DataFrame
psdf2 = sdf.pandas_api()                   # and back
```
It gives pandas-style code on distributed data, which eases migration. Operations that depend on global row order or index can be slow, so for new code the native DataFrame API is usually faster.

## Common Pitfalls
- **Nulls in comparisons:** `null == x` is null, not false. Filter with `isNull()` and handle nulls explicitly.
- **Column name clashes after a join:** join on names, or alias the DataFrames.
- **Too many small files:** many output partitions make slow reads. Reduce with `coalesce` before writing.
- **Skew:** one hot key in a join or `groupBy` makes one task much slower than the rest, which shows up in the Spark UI.
- **Python UDF overuse:** replace with built-in functions or pandas UDFs.
- **Random splits are not stable** across different data layouts. Use a `seed`, and for exact reproducibility save the split.

## Related Notes
- [[Apache Spark]]: architecture, RDDs, and lazy evaluation.
- [[Distributed Machine Learning and Graph Processing]]: MLlib and GraphX in context.
- [[Stream Processing and Event Streaming]]: Kafka, Flink and streaming concepts.
- [[Hadoop and MapReduce]]: the model Spark replaced for most workloads.
