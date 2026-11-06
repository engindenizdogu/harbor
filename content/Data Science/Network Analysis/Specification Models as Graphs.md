---
title: Specification Models as Graphs
tags: [data-science, graph, network-analysis, intermediate-representation, consistency-checking, mbse, auto-captured]
draft: false
---
A structured specification (a system model, a schema, a configuration) can be converted into a graph so that graph tools can find problems a human reviewer would miss. This note covers the pipeline pattern, the graph construction choices that mattered, and which checks paid off. The running example is a system model exported as XMI (see [[Model-Based Systems Engineering]]).

## Pipeline Pattern

```mermaid
flowchart LR
    X["Spec file (XML)"] --> P["Adapter parser"]
    P --> I["Intermediate graph schema"]
    I --> L["Optional LLM enrichment"]
    L --> G["Graph builder"]
    I --> G
    G --> M["GNN analysis"]
    G --> R["Rule checks"]
    M --> V["Visuals and review list"]
    R --> V
```

- **Adapter:** a parser that knows one input format (here, namespace-aware XPath over XML) and nothing else.
- **Intermediate representation (IR):** a unified, format-independent schema that sits between inputs and analysis. A minimal graph IR is `Node{id, type, attrs}` and `Edge{src, dst, type, attrs}`.
- **Why an IR:** everything after the adapter is format-independent, so supporting a new input format means writing one new parser and nothing else. This is the classic adapter pattern combined with a compiler-style IR.
- **LLM enrichment (optional):** normalize names, infer missing relations, or tag types. Treat its output as suggestions to verify.
- **Graph builder:** NetworkX for rules, PyTorch Geometric `Data` for [[Graph Neural Networks]].

## Graph Construction Choices

| Choice | Reason |
| ------ | ------ |
| Use a multigraph (NetworkX `MultiDiGraph`) | Two elements can share several relation types, such as a message and a connector between the same two classes, and rule checks depend on those types |
| Give containment ("owned by") its own relation and treat it as context | It records where an element lives but is not a semantic relation between elements |
| Keep both edge directions when feeding a GCN | `GCNConv` passes messages only along an edge, so a one-way edge leaves the source blind to its target |
| Omit a wrapper root node | A root linked to everything joins all views through one node and hides disconnected components |

## Why Explicit Structure Beats a Flat Export

Example: the same model analyzed two ways.

| Metric | Flattened export | Adapter-built graph |
| ------ | ---------------- | ------------------- |
| Nodes | 6,035 | 110 |
| Edges | 539 | 249 (113 relationships + 102 containment + 34 derived) |
| Isolated nodes | 5,529 | 0 |
| Connected components | 5,567 | 6 (largest 37) |
| Average degree | 0.18 | 4.00 |
| Density | 0.00003 | 0.0367 |
| Relation types | n/a | 19 |

About 96% of the flattened nodes were library elements. Derived edges covered operation calls, interaction participants, parameter types, and instances. Fewer but connected nodes gave about 22 times the average degree: making structure explicit mattered more than the choice of model.

## Rule-Based Consistency Checks

Rules run on the graph need no training, and every finding is explainable.

| Category | Checks |
| -------- | ------ |
| Connectivity | Disconnected parts; orphan elements |
| Naming | Duplicate elements or inconsistent spelling under the same owner; placeholder names ending in a number; unnamed elements |
| Cycles | Cyclic dependencies through Include, Dependency, Usage, Generalization, or Extend |
| Use cases | Actor without a use case; use case without an actor; use case with no behavior of the same name |
| Operations | Operation never called; message sent to a class that does not declare the operation; interactions disagreeing on who calls an operation |
| Deployment | Component without an artifact; artifact not deployed; dependency crossing layers; layers disagreeing |
| Control flow | Decision node with one way out (a merge modeled as a decision); decision branch without a guard or with a vague guard; join modeled as a fork |

One caution from hand review: a use case that is included by another needs no actor of its own, so the naive "use case without actor" rule gave false alarms until it was refined.

On the 110-node example the rules produced **32 findings**, more than the GNN surfaced.

## General Lesson

Build the graph, run simple rules first, then use ML to prioritize where a reviewer should look. Predictions are prompts for review, not corrections. The evaluation of the ML step on this graph is in [[Graph Neural Networks]].

## Sources
- NetworkX documentation: [MultiDiGraph](https://networkx.org/documentation/stable/reference/classes/multidigraph.html)
- Statistics and findings come from the author's analysis of one example model.

*Verification: the pipeline description and rule list reflect the author's own work; the NetworkX link points to the documentation page and was not re-fetched.*

## Related Notes
- [[Model-Based Systems Engineering]] - What the specification models and XMI are.
- [[Graph Neural Networks]] - Node-type classification and link prediction on the graph.
- [[Network Analysis Tools]] - NetworkX for building and inspecting graphs.
- [[Centrality Measures]] - Structural scores that could complement rule checks.
