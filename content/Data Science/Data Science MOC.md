---
title: Data Science MOC
tags: [data, moc]
draft: false
---
Map of Contents

## Notes
- [[CRISP-DM]] - ![[Pasted image 20260425190426.png]] Source: [CRISP-DM: das Standard-Vorgehensmodell für Data Mining](https...

## Statistics
- [[Correlation Coefficients]] - Pearson, Spearman, and Kendall, when each fits, and why zero correlation is not independence. Related: [[Exploratory Data Analysis]].
- [[Statistical Inference Basics]] - p-values, confidence intervals, t-tests with worked examples, business decisions, and Bayesian credible intervals. Related: [[1. Probability]].
- [[Autoregressive Models]] - AR, MA, ARMA, ARIMA, order identification with ACF/PACF, AIC/BIC/HQC and LRT, parameter fitting, and forecasting. Related: [[Correlation Coefficients]].
- [[Stationarity and Unit Roots]] - Weak stationarity, types of non-stationarity, ADF and KPSS, spurious regression, and fixes.
- [[ARMA and ARIMA Models]] - Lag operator, invertibility, differencing, special cases, and a worked order-identification example.
- [[Vector Autoregression]] - Multivariate AR, Granger causality, impulse responses, cointegration and VECM.

## Network Analysis
Read in this order: node importance first, then two-mode networks.
- [[Centrality Measures]] - Degree, closeness, betweenness, eigenvector, Katz, and PageRank, with a worked example and when to use each. Related: [[Distributed Machine Learning and Graph Processing]].
- [[Bipartite Networks]] - Two-mode graphs, biadjacency matrices, one-mode projections and weighting, co-occurrence matrices, and centrality across two node sets. Related: [[Recommendation Systems]].
- [[Network Analysis Tools]] - NetworkX for analysis, Gephi for visual exploration, Graphviz for static diagrams.
- [[Graph Neural Networks]] - Message passing, GCN, GraphSAGE, and GAT; learned alternatives to hand-made centrality.

## Simulation
- [[Agent-Based Modeling]] - Emergence from simple agent rules, Schelling's segregation model, how it differs from LLM agent systems, and the Mesa framework. Related: [[Network Analysis Tools]], [[Agents MOC]].

## Big Data Technologies
Read in this order: foundations, storage and batch compute, then streaming, plumbing, and analytics.
- [[Big Data Fundamentals and Architecture]] - The four Vs, layered architecture, storage options, CAP trade-offs, and responsible use. Related: [[Database Types]], [[Database Selection]].
- [[Hadoop and MapReduce]] - HDFS, YARN, the map-shuffle-reduce model, and the Hadoop ecosystem.
- [[Apache Spark]] - In-memory engine: RDDs, DataFrames, lineage, and how it differs from MapReduce.
- [[Stream Processing and Event Streaming]] - Batch vs. stream, Kafka, Storm, Flink, Spark Streaming, and cloud services.
- [[Big Data Integration and Orchestration]] - NiFi, Kafka, Flume, Airflow, and Oozie for ingestion and scheduling.
- [[Distributed Machine Learning and Graph Processing]] - Mahout, MLlib, Giraph, GraphX, and Neo4j.
- [[Correlation Drift Monitoring with Spark]] - Worked predictive-maintenance example: batch correlation matrix, sliding-window streaming correlation, and alerting pitfalls.
- [[Ray]] - Python-first task and actor runtime for distributed ML, tuning, RL, and serving; compared with Spark.

## External Resources & Data
- [[Wikimedia Commons]] - Massive open-source media repository; useful for visual datasets and public domain assets.

---
## To Research / Inbox
