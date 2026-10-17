---
title: Deep Reinforcement Learning from Human Preferences
tags: [machine-learning, reinforcement-learning, rlhf, reward-learning, alignment, auto-captured]
draft: false
---
Christiano et al. (2017) show that deep RL agents can learn complex behavior from **human preferences between pairs of short trajectory clips**, without access to a reward function, using feedback on under 1% of the agent's interactions. It is the paper that scaled learning from human feedback to modern deep RL, and the root of [[Reinforcement Learning from Human Feedback]].

## The Problem

Many tasks (scrambling an egg, cleaning a table) have goals that are complex or poorly defined. A hand-designed simple reward is usually optimized without satisfying the real preferences, the misalignment concern. Using a human's score as the reward at every step is far too expensive, because deep RL needs hundreds or thousands of hours of experience. Learning from demonstrations (imitation learning, inverse RL) fails for behaviors a human cannot demonstrate, such as controlling a robot with a very non-human body, but humans can often **recognize** good behavior.

The paper's goals: handle tasks we can only recognize, work with non-expert teachers, scale to large problems, and be economical with feedback.

**Core idea:** learn a reward function from human feedback, then optimize that reward with an ordinary RL algorithm.

## Setting

The agent sees observations $o_t$ and takes actions $a_t$, but the environment gives no reward. Instead a human can compare **trajectory segments** $\sigma = ((o_0, a_0), \ldots, (o_{k-1}, a_{k-1}))$ and say which they prefer, written $\sigma^1 \succ \sigma^2$. The goal is to produce behavior the human prefers while asking as few questions as possible.

## Method: Three Asynchronous Processes

| # | Process | Output |
| - | ------- | ------ |
| 1 | The policy interacts with the environment and is updated by a standard RL algorithm to maximize the **predicted** reward $\hat r$ (A2C for Atari, TRPO for simulated robotics) | Trajectories |
| 2 | Pairs of segments are selected and shown to a human for comparison | Human comparisons |
| 3 | The reward model $\hat r$ is fit to the comparisons by supervised learning | Updated reward parameters |

Trajectories flow from 1 to 2, comparisons from 2 to 3, and reward-model parameters from 3 to 1. The human is outside the inner RL loop, and the reward predictor stands in for them. Predicted rewards are normalized to zero mean and constant standard deviation, since the position of the reward is underdetermined.

## Preference Elicitation

The human sees two clips of **1 to 2 seconds** and indicates which is preferred, that they are equally good, or that they cannot be compared. Each judgment is stored as a triple $(\sigma^1, \sigma^2, \mu)$, where $\mu$ is a distribution over $\{1, 2\}$: all its mass on the preferred segment, uniform if equal, and incomparable pairs are dropped.

Comparisons are used instead of scores because people give consistent comparisons more easily, especially on continuous control tasks, and reward scales vary. Clips are used instead of single states because a clip is nearly as fast to judge but far more informative per label.

## Fitting the Reward Function

Treat $\hat r$ as a latent factor that explains the judgments: the probability that the human prefers a segment depends exponentially on the predicted reward summed over its length.

$$\hat P[\sigma^1 \succ \sigma^2] = \frac{\exp \sum_t \hat r(o_t^1, a_t^1)}{\exp \sum_t \hat r(o_t^1, a_t^1) + \exp \sum_t \hat r(o_t^2, a_t^2)}$$

$\hat r$ is chosen to minimize the cross-entropy between these predictions and the human labels:

$$\text{loss}(\hat r) = -\sum_{(\sigma^1, \sigma^2, \mu) \in D} \left[ \mu(1) \log \hat P[\sigma^1 \succ \sigma^2] + \mu(2) \log \hat P[\sigma^2 \succ \sigma^1] \right]$$

This is the **Bradley-Terry model** (a special case of the Luce-Shepard choice rule). It is analogous to Elo ratings in chess: the difference in two players' ratings gives the probability one beats the other, and here the difference in predicted reward of two clips gives the probability that one is chosen.

**Properties.** The probability depends only on the difference of the two summed rewards, is 0.5 when they are equal, approaches 1 as the gap grows, and the two directions sum to 1. **Example:** summed rewards of 2.0 and 1.0 give $e^2 / (e^2 + e^1) \approx 0.73$.

**Practical modifications** (found helpful in early experiments):
- An **ensemble** of predictors, each trained on data sampled with replacement, each normalized and then averaged.
- A fraction $1/e$ of the data held out for validation, with $\ell_2$ regularization (and sometimes dropout) tuned to keep validation loss between 1.1 and 1.5 times the training loss.
- A **10% chance that the human answers uniformly at random**, because raters keep a constant error rate even when the reward gap is large.

## Selecting Queries

Which pairs to ask about is chosen by an approximation of uncertainty: sample many pairs of segments, have each ensemble member predict which would be preferred, and ask about the pairs where the **predictions have the highest variance** across members. The paper notes this is crude and sometimes hurts, and that ideal selection would use the expected value of information.

## Experiments

| Domain | Result |
| ------ | ------ |
| Simulated robotics (MuJoCo, 8 tasks) | About 700 human queries nearly match RL on the true reward; with 1,400 synthetic labels it slightly beats RL, perhaps because the learned reward is better shaped. Real human feedback is typically a bit less effective than synthetic feedback |
| Atari (7 games) | 5,500 queries; harder than robotics, but substantial learning on most games, and matches or exceeds RL on some |
| Human time | Roughly 30 minutes to 5 hours of feedback |
| Novel behaviors | A Hopper robot learned to backflip, land upright, and repeat from 900 queries in under an hour; a Half-Cheetah learned to run on one leg from 800 queries; an Enduro car learned to stay alongside other cars from about 1,300 queries |

**Example (backflip).** Nobody wrote a reward for "backflip". Humans watched pairs of clips of the robot and picked the one that looked more like a backflip, for example one that rotates in the air over one that falls over.

Summary claim: learning a separate reward model by supervised learning cuts the interaction complexity by roughly **three orders of magnitude**, to the point where the cost of compute is comparable to the cost of non-expert feedback.

## Ablations

Variants tested: random queries instead of disagreement-based, no ensemble, **no online queries** (feedback gathered only at the start), no regularization, segments of length 1, and regressing the true total reward instead of comparing.

- **Online feedback matters.** With a reward predictor trained once on early data, the predictor captures only part of the true reward, and maximizing that partial reward can give bizarre behavior. In **Pong**, the agent sometimes learned to avoid losing points but not to score them, producing extremely long volleys that repeat forever. Human feedback must be intertwined with RL, not provided statically.
- **Comparisons versus scores:** for continuous control, predicting comparisons worked much better than predicting scores, likely because reward scales vary. For Atari (rewards were clipped), neither consistently won.
- **Clips versus single frames:** longer clips were far more helpful per clip, though less per frame.

## Why It Matters

This is the template for later systems: learn a reward model from human comparisons, then optimize it. It also shows the weak point: the reward model is a **proxy**, and the policy can exploit it unless the feedback keeps up with the agent's changing behavior.

## Related Notes
- [[Reinforcement Learning from Human Feedback]] - The language-model descendants of this method.
- [[Actor-Critic Methods]] - A2C and TRPO, the policy optimizers used here; the reward predictor is not a value function.
- [[Reinforcement Learning]] - The setting without an environment-supplied reward.
- [[World Models]] - Learned simulators as another route to scarce-feedback learning.

*Source: [Deep Reinforcement Learning from Human Preferences](https://arxiv.org/abs/1706.03741) (Christiano et al., 2017). Method, formulas, and experiment figures were checked against Sections 1 to 4 of the paper.*
