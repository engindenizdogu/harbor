---
title: Bayesian Networks
---
# Bayesian Networks

| Type                          |
| ----------------------------- |
| Probabilistic Graphical Model |

A Bayesian Network is a **Directed Acyclic Graph (DAG)** that represents the joint probability distribution of a set of random variables.
- **Nodes:** Represent random variables (can be discrete or continuous).
- **Edges:** Directed arrows represent causal influences or conditional dependencies.
- **Local Markov Property:** Each node is conditionally independent of its non-descendants given its parents.

---

# Key Components and Calculus
The power of Bayesian Networks lies in their ability to factorize a complex joint distribution into smaller, local conditional distributions.
### Factorization
The joint probability of all variables $X_1, ..., X_n$ is the product of the probability of each node given its parents:

$$P(X_1, ..., X_n) = \prod_{i=1}^{n} P(X_i | Parents(X_i))$$

### Conditional Probability Tables (CPTs)

For discrete variables, each node has an associated CPT. This table quantifies the effects the parents have on the child node. If a node has no parents, the table simply contains its prior probabilities.

---
# d-Separation and Independence
**d-separation** (directed separation) is a criterion used to determine if two sets of variables are independent given a third set. There are three fundamental structures (triplets) that define the flow of influence:
1. **Causal Chains ($X \rightarrow Y \rightarrow Z$):** $X$ and $Z$ are independent **only if** $Y$ is observed.
2. **Common Cause ($X \leftarrow Y \rightarrow Z$):** $X$ and $Z$ are independent **only if** $Y$ is observed (e.g., $Y$ is the flu, $X$ and $Z$ are different symptoms).
3. **Common Effect / V-Structure ($X \rightarrow Y \leftarrow Z$):** $X$ and $Z$ are **independent** by default, but become **dependent** if $Y$ (or its descendant) is observed. This is known as "explaining away."

---

# Real-Life Scenarios for Graphical Models
Graphical models are used in fields where variables have complex interdependencies.
### Medical Diagnosis
- **Scenario:** Predicting the likelihood of a disease based on symptoms and test results.
- **Structure:** Nodes represent "Smoking," "Lung Cancer," "Cough," and "X-ray result." A Bayesian network can calculate the probability of cancer given a positive X-ray and a history of smoking.

### Spam Filtering
- **Scenario:** Determining if an email is spam based on the presence of certain words.
- **Structure:** A "Naive Bayes" model (a simple form of PGM) uses a central "Spam/Not Spam" node that influences the probability of seeing words like "Winner," "Offer," or "Meeting."

### Fault Diagnosis in Engineering
- **Scenario:** Identifying which component failed in a complex system (like a car engine or a power grid).
- **Structure:** Nodes represent different components (battery, alternator, spark plugs) and observable signals (lights flickering, engine not starting).

### Genetics and Bioinformatics
- **Scenario:** Modeling the inheritance of traits or the interaction between different genes.
- **Structure:** Pedigree charts are essentially Bayesian networks where nodes are individuals and edges represent the passing of genetic material from parents to offspring.