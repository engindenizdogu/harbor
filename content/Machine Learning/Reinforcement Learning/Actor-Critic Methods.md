---
title: Actor-Critic Methods
tags: [machine-learning, reinforcement-learning, policy-gradient, actor-critic, auto-captured]
draft: false
---
Reinforcement learning methods split into those that learn a **policy** (how to act), those that learn a **value** (how good a situation is), and **actor-critic** methods that learn both. The critic turns the sparse, delayed reward into a dense learning signal for the actor.

## Policy, Value, or Both

| | Policy (actor) | Value (critic) | Actor-critic |
| - | -------------- | -------------- | ------------ |
| Intuition | Instinct, reflex | Deliberate judgment | Acts and is judged |
| Learns | State to action | State (or state-action pair) to value | Both |
| Example algorithms | REINFORCE | Q-learning | A2C, TRPO, PPO |
| Weakness | Noisy and slow: only the final outcome guides it | No explicit policy; awkward for continuous or numerous actions | Two things to train |

## What "Reinforce" Means

A policy $\pi(a \mid s; \theta)$ is a parametrized function that gives the probability of each action. To reinforce an action is to make it **more likely in that state** by gradient ascent on expected reward:

$$\theta \leftarrow \theta + \alpha \cdot \text{signal} \cdot \nabla_\theta \log \pi(a \mid s; \theta)$$

- $\nabla_\theta \log \pi(a \mid s)$ is the direction that makes that action more probable.
- The **signal** says how good the action turned out to be: positive raises its probability, negative lowers it.
- $\alpha$ is the learning rate.

This has the same form as maximum likelihood, $\theta \leftarrow \theta + \alpha \nabla_\theta \log P(\text{label} \mid x)$, where the signal is implicitly 1 for the labeled answer. In RL there is no label, so the signal says how good the action was and can be negative. What differs between methods is the signal.

## Why Add a Critic

- With **no critic**, the signal is the full return after the action. It is unbiased but has high variance, because it mixes in the luck of everything that happens later, and it must wait for the episode to end.
- With a **critic**, the signal is the TD error (or advantage) $\delta = r + \gamma V(s') - V(s)$, available at every step with much less noise. See [[Temporal Difference Learning]].
- Both learn at once: the critic is trained so that $V(s)$ matches $r + \gamma V(s')$, and the actor reinforces actions using the same error.

**Example (chess).** The critic produces the 50% to 70% estimate after a capture, and the actor is the part that chooses the capture. The change in the critic's estimate is the signal that makes the actor repeat that kind of move.

## Algorithms

| Method | Learns | Signal | Distinguishing idea |
| ------ | ------ | ------ | ------------------- |
| REINFORCE | Policy | Full return | Simple and unbiased but high variance; waits for the episode end. Subtracting a baseline such as $V(s)$ leads to actor-critic |
| Q-learning | $Q(s, a)$ | TD error | Off-policy; acts greedily with some exploration. See [[Q-Learning]] |
| A2C (advantage actor-critic) | Policy and $V$ | Advantage, about $r + \gamma V(s') - V(s)$ | Lower variance than REINFORCE |
| TRPO | Policy and $V$ | Advantage | A KL-divergence trust region limits each policy update so one big step cannot wreck the policy |
| PPO | Policy and $V$ | Clipped advantage | Clips the ratio $\pi_{new} / \pi_{old}$ to $[1-\epsilon, 1+\epsilon]$: a simpler way to keep updates small; the usual optimizer in RLHF for language models |

The **advantage** is how much better an action was than the state's average. Example of PPO clipping with $\epsilon = 0.2$: if the old policy gave an action probability 0.10 and the advantage is positive, raising it to 0.15 gives a ratio of 1.5, which is clipped to 1.2, so larger increases stop being rewarded.

REINFORCE, A2C, TRPO, and PPO are **on-policy** (they learn from the policy's own experience); Q-learning is **off-policy**. In practice the lineage runs from REINFORCE, to adding a critic (A2C), to constraining updates (TRPO), to simplifying the constraint (PPO).

## Where This Appears

- **AlphaZero:** one network outputs a policy and a value together, the same idea in a single network. See [[AlphaZero]].
- **Learning from human preferences:** the paper optimizes its learned reward with A2C (Atari) and TRPO (simulated robotics). The learned reward predictor is **not** a value function: it gives an immediate per-step reward learned from comparisons, while a value is the expected future reward under a policy. See [[Deep Reinforcement Learning from Human Preferences]].
- **RLHF for language models:** PPO is the typical optimizer in the RL step. See [[Reinforcement Learning from Human Feedback]].

## Related Notes
- [[Deep Reinforcement Learning]] - Neural-network versions of these methods.
- [[Temporal Difference Learning]] - The error signal the critic computes.
- [[Reinforcement Learning]] - Agent, environment, and reward basics.

*Sources: [Sutton & Barto, Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html); [TRPO](https://arxiv.org/abs/1502.05477) (Schulman et al., 2015); [PPO](https://arxiv.org/abs/1707.06347) (Schulman et al., 2017); [A3C/A2C](https://arxiv.org/abs/1602.01783) (Mnih et al., 2016). Lecture material places REINFORCE, Q-learning, and PPO as the policy, value, and actor-critic examples, and the human-preferences paper uses A2C and TRPO. The algorithm descriptions and formulas are standard formulations written from general knowledge, not copied from the papers. Please check the sources.*
