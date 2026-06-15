---
title: World Models
tags: [machine-learning, reinforcement-learning, deep-learning]
draft: false
---

A world model is an AI system’s internal, causal representation of an environment. It allows an agent to simulate future states, predict the consequences of its actions, and plan accordingly without executing those actions in the real world.

It typically relies on three core components:
* **The Encoder:** Compresses high-dimensional sensory inputs into a latent representation: $s_t = E(x_t)$.
* **The Transition Model:** Predicts the next latent state based on the current state and a specific action: $s_{t+1} = T(s_t, a_t)$.
* **The Decoder/Reward Model:** Translates the predicted state back into an observation or reward signal.

## World Models vs. SOTA LLMs

LLMs are advanced autoregressive sequence predictors. Their primary objective is predicting the next token: $P(x_{t+1} | x_1, \dots, x_t)$. They lack a grounded, causal simulator.

| Feature | SOTA LLMs | True World Models |
| :--- | :--- | :--- |
| **Paradigm** | Reactive Execution (Trial-and-error) | Proactive Simulation (Forward-planning) |
| **State Representation** | Linguistic tokens (text/code) | Continuous latent variables representing states |
| **Mechanism** | Semantic Proximity (Statistical correlations) | Causal Dynamics (Mathematical first principles) |
| **Handling Novelty** | Struggles with out-of-distribution variables | Calculates outcomes based on simulation rules |

### The "Breaking Glass" Example

* **LLM:** Knows a dropped glass breaks because words like "throw," "glass," and "shatter" are statistically correlated in its training data (Semantic Proximity).
* **World Model:** Instantiates properties (mass, brittleness, force, gravity) and simulates the trajectory and impact to calculate structural failure (Causal Dynamics).

## World Models for Software and Coding

Software is a mathematical environment with its own "physics." A codebase possesses:
* **State:** Variables in memory, abstract syntax trees.
* **Action:** Executing a function, making a system call.
* **Transition Dynamics:** The strict, deterministic rules of the compiler/interpreter.

Instead of predicting the next most likely line of code (like an LLM), a Code World Model simulates the code's execution. It predicts changes in memory allocation or type-checker passes *before* the code is actually run, allowing for rigorous, autonomous software engineering.

## Handling Stochasticity and Chance Nodes

Real-world environments and complex games involve hidden information and randomness. World models handle this via Probabilistic Code and Monte Carlo Tree Search (MCTS).

* **Probabilistic Transitions:** The model defines a probability distribution over all possible next states: $P(s_{t+1} | s_t, a_t)$ (see [[Markov Decision Processes]]).
* **Decision Nodes:** Points in the search tree where the agent chooses an action to maximize expected reward.
* **Chance Nodes:** Points where the environment executes randomness. The model *samples* these nodes repeatedly during rollouts.
* **Expected Value:** By running thousands of simulations and averaging the outcomes of the chance nodes, the agent learns the true mathematical risk of an action.
* **Information Set MCTS (ISMCTS):** Used for hidden information (e.g., fog of war, opponent's cards). The model randomly samples a plausible starting state based on current observations and simulates forward.

---

## Key Resources & Reading List

### Foundational Theory

* **"World Models" (2018)** by David Ha and Jürgen Schmidhuber: The bedrock paper popularizing the term, detailing the VMC (Vision, Memory, Controller) architecture.
* **"A Path Towards Autonomous Machine Intelligence" (2022)** by Yann LeCun: Introduces the Joint Embedding Predictive Architecture (JEPA), emphasizing the need for abstract continuous latent space prediction.

### Applied to Code and Agents

* **"Generating Code World Models with Large Language Models Guided by Monte Carlo Tree Search" (NeurIPS 2024):** Explores how LLMs can synthesize discrete code to act as deterministic simulators.
* **"Code World Models for General Game Playing" (Google DeepMind, ICLR 2026):** Details the use of LLMs to generate full simulators for unknown environments, including the practical application of ISMCTS for chance nodes.
