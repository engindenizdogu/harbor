---
title: 05.2026 - LLM Caching & Recursive Language Models (RLMs)
tags:
  - projects
  - portfolio
  - nlp
  - llm
draft: false
---
> A production-grade Python research system implementing a Two-Stage Semantic Cache ("Dragnet & Sniper") for autonomous LLM workflows, achieving massive cost reductions.

## Quick Facts
- **Context:** CS 800 Special Problems in CS (Spring 2026, In Progress)
- **Tech Stack:** Python, FAISS, Anthropic Claude, Hugging Face (Qwen3 Embeddings/Reranker)
- **Links:** None available

## Overview and Problem
High-volume, multi-step LLM agents are often economically unviable due to redundant generative workloads and API costs. This project solves this by creating a hybrid local/cloud semantic caching architecture that safely stores and reuses verified answers without hallucination drift.

## What I Built
- **Engineered** a "Dragnet & Sniper" two-stage semantic cache using FAISS and cross-encoder relevance gates to prevent catastrophic cache collisions.
- **Implemented** an autonomous workflow with SemanticCacheController that handles document retrieval, synthesis, grounding, and persistent storage.
- **Designed** a robust provenance system that grounds every cached entry against source chunks and verifies it with a secondary LLM.
- **Automated** knowledge extraction to decompose synthesized answers into queryable `(subject, relation, object)` triples for an emergent knowledge graph.
- **Built** a dynamic routing system to dispatch tasks efficiently between executor-class (Claude 3.5 Sonnet) and evaluator-class (Claude 3.5 Haiku) models.

## Key Results and Impact
- Achieved a massive 96.7% cost reduction on redundant generative workloads without sacrificing accuracy.
- Established a rigorous empirical benchmark repository targeting long-context suites like RULER v2, NoLiMa, LongBench v2, and LegalBench.
- Improved subsequent hit latency using local CPU-bound model infrastructure.

## Core Learnings
- Demonstrated that semantic caching paired with strict provenance checks and corpus-scoped isolation allows safe, reproducible answer reuse in complex workflows.

---
*Related:* [[Projects MOC]]