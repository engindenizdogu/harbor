---
title: Deep Reinforcement Learning
tags: [machine-learning, reinforcement-learning, deep-learning]
draft: false
---
Deep Reinforcement Learning (DRL) combines **Reinforcement Learning** with **Deep Learning**. It uses Neural Networks to approximate functions in RL, allowing agents to solve tasks with high-dimensional state spaces (like pixels or sensor readings).

## Why Deep Learning?
In many real-world problems, the state space is too large for a traditional **Q-Table**. For example, in an Atari game, the "state" is the pixel buffer ($210 \times 160$ pixels), resulting in $256^{210 \times 160}$ possible states. Deep Learning allows us to map these high-dimensional inputs to actions or values.

## Key Architectures

### 1. Deep Q-Networks (DQN)
DQN was the first major DRL success (DeepMind, 2013). It uses a CNN to estimate Q-values from images.
- **Experience Replay**: Stores transitions $(s, a, r, s')$ in a buffer and samples random batches for training to break data correlations.
- **Target Network**: Uses a separate, slowly-updating network to calculate the TD target, which stabilizes training.

### 2. Policy Gradient Methods
Instead of learning a value function, these methods directly learn a policy network $\pi_\theta(a|s)$.
- **Advantage**: Can learn stochastic policies and work well in continuous action spaces.
- **PPO (Proximal Policy Optimization)**: A stable, state-of-the-art policy gradient algorithm.

### 3. Actor-Critic Methods
A hybrid approach:
- **Actor**: Learns the policy (how to act).
- **Critic**: Learns the value function (how good the current state/action is).
- The critic provides feedback to the actor to improve the policy update.

## Challenges in DRL
- **Sample Inefficiency**: DRL often requires millions of interactions to learn.
- **Instability**: Small changes in neural network weights can lead to huge changes in behavior.
- **Reward Engineering**: Designing a reward function that accurately reflects the goal without leading to "reward hacking."

## See Also
- [[Reinforcement Learning MOC]]
- [[Neural Networks]]
- [[Convolutional Neural Networks]]
- [[Deep Q-Networks]]
