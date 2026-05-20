---
title: Q-Learning
tags: [machine-learning, reinforcement-learning, algorithms]
draft: false
---
Q-Learning is an **Off-Policy, Model-Free** Temporal Difference (TD) learning algorithm used to find the optimal action-selection policy for any given MDP.

## The Core Idea
The goal of Q-learning is to learn the **Optimal Action-Value Function** $Q^*(s, a)$, which represents the maximum expected future reward for taking action $a$ in state $s$.

## The Update Rule
The Q-values are updated iteratively using the **Bellman Equation** as an update target:

$$Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha [R_{t+1} + \gamma \max_{a} Q(S_{t+1}, a) - Q(S_t, A_t)]$$

Where:
- $\alpha$: The learning rate.
- $\gamma$: The discount factor.
- $R_{t+1} + \gamma \max_{a} Q(S_{t+1}, a)$: The **TD Target** (the estimated future value).
- $R_{t+1} + \gamma \max_{a} Q(S_{t+1}, a) - Q(S_t, A_t)$: The **TD Error**.

## Key Characteristics

### Off-Policy Learning
Q-Learning is "Off-Policy" because it updates the Q-value based on the *greedy* action (the maximum possible Q-value in the next state), even if the agent actually took a different (e.g., exploratory) action.

### Convergence
Under the assumption of infinite exploration and a decaying learning rate, Q-Learning is guaranteed to converge to the optimal $Q^*$ values for finite state and action spaces.

## Q-Table
In its simplest form, Q-learning maintains a table (the **Q-Table**) where rows represent states and columns represent actions. This works well for environments with small, discrete state spaces but fails in high-dimensional or continuous spaces.

## Deep Q-Learning
To handle complex environments (like Atari games), the Q-table is replaced with a Neural Network (a **Deep Q-Network** or DQN) that approximates the Q-values.

## See Also
- [[Reinforcement Learning]]
- [[Deep Reinforcement Learning]]
- [[SARSA]] - The on-policy counterpart to Q-Learning.
