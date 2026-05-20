---
title: Reinforcement Learning
tags: [machine-learning, reinforcement-learning, foundations]
draft: false
---
Reinforcement Learning (RL) is the science of decision-making. It involves an **Agent** learning to behave in an **Environment** by performing **Actions** and seeing the results as **Rewards**.

## The Agent-Environment Loop

The interaction between the agent and the environment is typically modeled as a discrete-time process:
1. At each time step $t$, the agent receives the current **State** $S_t$.
2. The agent selects an **Action** $A_t$.
3. The environment transition to a new state $S_{t+1}$ and provides a **Reward** $R_{t+1}$.
4. The cycle repeats.

### Key Components

| Component                | Description                                                                                          |
| :----------------------- | :--------------------------------------------------------------------------------------------------- |
| **Agent**                | The decision-maker that learns which actions to take.                                                |
| **Environment**          | Everything outside the agent that the agent interacts with.                                          |
| **Policy ($\pi$)**       | A mapping from states to actions (the agent's "strategy").                                           |
| **Reward Signal ($R$)**  | A scalar value defining the goal of the RL problem.                                                  |
| **Value Function ($V$)** | The total amount of reward an agent can expect to accumulate over the future, starting from a state. |
| **Model**                | (Optional) The agent's representation of how the environment behaves (transitions and rewards).      |

## Core Challenges

### Exploration vs. Exploitation
- **Exploration**: Trying new actions to discover more about the environment.
- **Exploitation**: Using current knowledge to take actions that yield the highest known reward.
- *Balance*: Common strategies include $\epsilon$-greedy, where the agent explores with probability $\epsilon$ and exploits otherwise.

### Credit Assignment Problem
The difficulty of determining which specific action in a long sequence was responsible for an eventual reward (e.g., in a game of Chess, which move led to the win?).

### Delayed Reward
Rewards may not be immediate. An agent might have to take several "bad" actions in the short term to reach a high-reward state in the future.

## Types of RL

- **Model-Based**: The agent tries to learn a model of the environment and uses it to plan.
- **Model-Free**: The agent learns purely from experience without building an internal model of transitions (e.g., Q-Learning).
- **On-Policy**: The agent learns about the policy it is currently following.
- **Off-Policy**: The agent learns about an optimal policy while following a different exploratory policy.

## See Also
- [[Reinforcement Learning MOC]]
- [[Markov Decision Processes]]
- [[Dynamic Programming]]
- [[Deep Reinforcement Learning]]

*Source: [Sutton & Barto - Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html)*
