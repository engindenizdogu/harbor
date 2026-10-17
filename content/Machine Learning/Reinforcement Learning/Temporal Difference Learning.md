---
title: Temporal Difference Learning
tags: [machine-learning, reinforcement-learning, td-learning, value-functions, auto-captured]
draft: false
---
Temporal difference (TD) learning is the idea that an agent can learn from **changes in its own predictions** instead of waiting for the final outcome. It is the standard answer to the credit assignment problem in [[Reinforcement Learning]], and it underlies value-based methods such as [[Q-Learning]] and the critic in [[Actor-Critic Methods]].

## The Credit Assignment Problem

Reward is **not instant**, actions have **long-term consequences**, and **not all actions contribute equally** to the outcome. Given a single outcome at the end (winning a chess game after 40 moves), which earlier actions deserve credit or blame? Minsky formalized this as the *temporal credit assignment problem* in 1961.

| | Supervised learning | Reinforcement learning |
| - | ------------------- | ---------------------- |
| Feedback | A label per example, immediately | A sparse scalar, often at the end |
| Whose fault is an error? | The prediction just made | Any of many earlier actions, mixed with chance |
| Data | Independent examples | Actions change which states come next |

Reinforcing every move of a won game is noisy (a won game contains weak moves and a lost game contains good ones) and gives one thin signal for dozens of decisions. An early attempt, Minsky's 1951 SNARC maze machine, strengthened recently active connections whenever the agent succeeded; it solved some simple mazes but nothing more complex.

## Sutton's Idea: Learn Values

In 1984, Sutton proposed maximizing the **expected** reward (the *value*) instead of the raw reward. Rewards are sparse, but expected rewards exist at every step, so there are many more chances to learn.

The **value function** of a state is the expected discounted total future reward from it:

$$V^\pi(s) = \mathbb{E}_\pi\left[ r_{t+1} + \gamma r_{t+2} + \gamma^2 r_{t+3} + \cdots \mid s_t = s \right]$$

If the only reward is $+1$ for a win, $V(s)$ is the **probability of winning** from $s$. The discount factor $\gamma \in [0, 1]$ makes earlier rewards count more: a reward of 10 arriving at the third future step is worth $\gamma^2 \cdot 10 = 8.1$ now when $\gamma = 0.9$.

## The TD Error

The learning signal is how much the value estimate **changes** from one step to the next:

$$\delta = r + \gamma V(s') - V(s)$$

Reinforce actions that increase the estimated value (positive $\delta$) and punish actions that decrease it (negative $\delta$). The tabular update is $V(s) \leftarrow V(s) + \alpha \, \delta$.

**Example (chess).** Before a move you estimate a 50% chance of winning. You capture the opponent's queen and the estimate rises to 70%. The TD error is $+20\%$, so the queen capture is reinforced immediately, without waiting for the end of the game. What matters is the **increase**, not the absolute value: a move that drops the estimate from 90% to 70% is bad even though 70% is high.

## Actor and Critic

TD learning has two components:
- **Critic:** predicts the likelihood of reward (the value).
- **Actor:** chooses actions, and is rewarded by the critic's change in expected reward instead of the actual reward.

This split is developed in [[Actor-Critic Methods]].

## Evidence from the Brain: Dopamine

Neuroscientist Wolfram Schultz recorded dopamine neurons in monkeys that saw a visual cue and, five seconds later, received sugar water. In 1997, Dayan, Montague, and Schultz argued that dopamine encodes the **reward prediction error**, which is the TD error, and not the reward itself.

| Situation | Predicted | Actual | Error | Dopamine response |
| --------- | --------- | ------ | ----- | ----------------- |
| Early training, new cue, reward arrives | 0 | 1 | +1 | Burst at the reward |
| Trained, reward arrives as expected | 1 | 1 | 0 | No change at the reward; burst at the **cue** |
| Trained, cue shown, reward withheld | 1 | 0 | -1 | Dip below baseline at the expected reward time |

After training, the cue itself is unpredictable and raises the estimated value, which is a positive TD error. The error signal has moved backward in time to the earliest reliable predictor.

## Related Notes
- [[Reinforcement Learning]] - The agent-environment loop and the credit assignment problem.
- [[Q-Learning]] - TD learning applied to action values.
- [[Actor-Critic Methods]] - Policy and value learning combined.
- [[Markov Decision Processes]] - The framework in which value functions are defined.

*Sources: [Sutton & Barto, Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html). The history (Minsky 1951 and 1961, Sutton 1984) and the dopamine experiment summary follow lecture material; Dayan, Montague, and Schultz (1997) is "A Neural Substrate of Prediction and Reward". The update rule and value definition are the standard formulation written from general knowledge. Please check the sources.*
