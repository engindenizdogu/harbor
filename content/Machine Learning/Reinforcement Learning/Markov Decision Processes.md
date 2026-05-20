---
title: Markov Decision Processes
tags: [machine-learning, reinforcement-learning, math]
draft: false
---
A Markov Decision Process (MDP) provides a mathematical framework for modeling decision-making in situations where outcomes are partly random and partly under the control of a decision-maker.

## The Markov Property
A state $S_t$ is **Markov** if and only if:
$$P(S_{t+1} | S_t) = P(S_{t+1} | S_1, ..., S_t)$$
In other words, the future is independent of the past given the present. The current state captures all relevant information from the history.

## Formal Definition
An MDP is defined by a 5-tuple $(S, A, P, R, \gamma)$:
- **$S$**: A finite set of states.
- **$A$**: A finite set of actions.
- **$P$**: A state transition probability matrix $P(s'|s, a)$.
- **$R$**: A reward function $R(s, a)$.
- **$\gamma$**: A discount factor $\gamma \in [0, 1]$, which determines the importance of future rewards.

## Goal of an MDP
The goal is to find a **Policy** $\pi(a|s)$ that maximizes the **Expected Return** $G_t$:
$$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + ... = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$$

## Value Functions

### State-Value Function $V_\pi(s)$
The expected return starting from state $s$ and following policy $\pi$.
$$V_\pi(s) = E_\pi [G_t | S_t = s]$$

### Action-Value Function $Q_\pi(s, a)$
The expected return starting from state $s$, taking action $a$, and then following policy $\pi$.
$$Q_\pi(s, a) = E_\pi [G_t | S_t = s, A_t = a]$$

## The Bellman Equation
The fundamental recursive relationship for value functions:
$$V_\pi(s) = \sum_{a \in A} \pi(a|s) \sum_{s' \in S} P(s'|s, a) [R(s, a, s') + \gamma V_\pi(s')]$$

## See Also
- [[Reinforcement Learning]]
- [[Bellman Equations]]
- [[Dynamic Programming]]
