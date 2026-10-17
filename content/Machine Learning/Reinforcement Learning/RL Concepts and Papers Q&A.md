---
title: RL Concepts and Papers Q&A
tags: [machine-learning, reinforcement-learning, study-guide, auto-captured]
draft: false
---
Study guide in question-and-answer form: reinforcement learning fundamentals, AlphaZero, and the paper *Deep Reinforcement Learning from Human Preferences*. Each answer starts with a short version, followed by details.

## Fundamentals

### What clue does each learning paradigm get from the problem?

| Paradigm | Clue |
|---|---|
| Unsupervised | nothing (finds structure in the data) |
| Supervised | labels |
| Self-supervised | labels built from the data itself |
| Reinforcement | rewards |

A reward is not a label: it is a scalar saying how good an outcome was, often delayed, and the agent must work out which actions earned it.

> [!example] Example
> Classifying photos as cat or dog uses labels; grouping customers by their purchases uses nothing; learning to play Pong uses only the score, a reward.

### What are the ingredients of the RL framework?

| Ingredient | Meaning |
|---|---|
| Agent | the decision maker |
| Environment | everything the agent interacts with |
| State | description of the environment |
| Action | how the agent affects the environment, chosen by the policy |
| Policy | rule mapping state to action |
| Reward | scalar that shapes behavior |

Each step: the agent observes the state, the policy picks an action, the environment changes and returns a new state and a reward. The agent's goal is to maximize the reward it receives.

> [!example] Example (chess)
> The state is the board position, an action is a legal move, the policy is the rule for picking the move (a neural network in modern systems), and the reward is +1 for a win, -1 for a loss, and 0 otherwise. For a robot scrambling an egg, the state is its sensor readings, the actions are motor commands, and the reward is whatever signal says the eggs came out well.

### What is the temporal credit assignment problem?

> [!tip] Short answer
> Given a final outcome (such as winning after 40 chess moves), which earlier actions deserve credit or blame? Minsky formalized it in 1961.

It arises because reward is not instant, actions have long-term consequences, and not all actions contribute equally.

| | Supervised learning | RL |
|---|---|---|
| Feedback | a label per example, immediately | a sparse scalar, often at the end |
| Whose fault is an error? | the prediction just made | any of many earlier actions, mixed with chance |
| Data | independent examples | actions change which states come next |

> [!example] Example
> A robot scrambles an egg with 200 motor commands and the only feedback is the taste at the end. Was it the grip on the whisk, the heat, or the timing that mattered? The same single reward is attached to all 200 commands.

### Why not reinforce every move in a won game?

- A won game contains mediocre and bad moves, and a lost game contains good ones, so reinforcing everything adds noise; one reward per 40 moves is a very thin signal.
- **Better signal:** estimate the chance of winning after each move and use the **change**, `V(state after) − V(state before)`. This is the TD error. In the chess example the estimate goes from 50% to 70%, so the queen capture is reinforced.
- What matters is the increase, not the absolute value: a move that drops the estimate from 90% to 70% is bad even though 70% is high.

### What does "reinforce" mean, and how does it relate to ordinary weight updates?

> [!tip] Short answer
> Make that action more likely in that state, by gradient ascent on expected reward.

```
θ ← θ + α · signal · ∇θ log π(a | s; θ)
```

| Symbol | Meaning |
|---|---|
| π(a given s; θ) | the policy: probability the network assigns to action a in state s |
| ∇θ log π | direction that makes that action more probable |
| signal | how good the action turned out to be; positive raises its probability, negative lowers it. Return in REINFORCE, TD error in actor-critic, clipped advantage in PPO |
| α | learning rate (step size) |

Same form as maximum likelihood: supervised learning does `θ ← θ + α · ∇θ log P(label | x)`, implicitly with signal 1 for the labeled answer. In RL there is no label, so the signal says how good the action was and can be negative. It resembles the language-model update, with each example's gradient weighted by a reward-like signal.

> [!example] Example (illustrative numbers)
> If π(capture queen | s) = 0.10 and the signal is +0.2, the update raises that probability (say to 0.12). With a signal of -0.2 it would lower it (say to 0.08).

### How is the value function defined?

```
V^π(s) = E_π [ r_{t+1} + γ·r_{t+2} + γ²·r_{t+3} + … | s_t = s ]
```

- The expected discounted total future reward from state s following policy π; γ in [0, 1] is the discount factor.
- If the only reward is +1 for a win, V(s) is the probability of winning from s.
- **Q(s, a):** the same quantity after first taking action a.
- **TD error:** `δ = r + γ·V(s′) − V(s)`.
- In practice V is a neural network, the critic.

> [!example] Example (discount)
> With γ = 0.9, a reward of 10 that arrives at the third future step is worth `γ² · 10 = 0.9² · 10 = 8.1` now, so earlier rewards count more. **Example (chess):** V(position) = 0.7 means that, playing as usual from here, the win probability is 70%.

### What did the dopamine experiments show?

> [!tip] Short answer
> Dopamine signals the reward prediction error (actual minus predicted reward), not reward itself.

| Situation | Predicted | Actual | Error | Dopamine |
|---|---|---|---|---|
| Early, new cue, reward arrives | 0 | 1 | +1 | burst at the reward |
| Trained, reward arrives | 1 | 1 | 0 | no change at the reward, burst at the **cue** |
| Trained, cue shown, reward withheld | 1 | 0 | -1 | dip below baseline at the expected reward time |

- After training, the cue itself is unpredictable and raises the estimated value, a positive TD error; the error signal has moved backward to the earliest reliable predictor.
- Dayan, Montague, and Schultz (1997) argued dopamine matches the TD error, the critic's learning signal. Sutton called it one of the greatest interactions between engineering and natural science about the brain.

> [!warning] Common mistake
> Dopamine does not signal reward or expectation in general: it signals the prediction error. A withheld, expected reward gives a dip below baseline at the expected time, not continued activity.

### Policy vs. value, and why combine them (actor-critic)?

| | Policy (actor) | Value (critic) | Actor-critic |
|---|---|---|---|
| Intuition | instinct, reflex | deliberate judgment | acts and is judged |
| Learns | state to action | state (or state-action) to value | both |
| Example | REINFORCE | Q-learning | PPO, A2C, TRPO |
| Weakness | noisy, slow (final outcome only) | no explicit policy; awkward for continuous actions | two things to train |

- The **critic converts the sparse delayed reward into a dense, immediate signal** (the TD error), so the actor need not wait for the end of the episode and gets less noise.
- Both learn simultaneously: the critic is trained so V(s) matches `r + γV(s′)`; the actor reinforces actions using the same TD error.
- In the chess example the critic produces the 50% to 70% estimate and the actor chooses the move.

> [!question]+ Check yourself: which component computes the TD error and which one uses it?
> The critic computes it (the change in its value estimate, `r + γV(s′) − V(s)`), and the actor uses it as the signal to raise or lower the probability of the action it just took.
- AlphaZero's network outputs a policy and a value together, which is the same idea in one network.

### How do REINFORCE, Q-learning, A2C, TRPO, and PPO differ?

| Method | Learns | Signal | Distinct trait |
|---|---|---|---|
| REINFORCE | policy | full return G_t | simple and unbiased, but high variance; waits for the episode end |
| Q-learning | Q(s, a) | TD error | no explicit policy; act greedily with some exploration; max over actions makes continuous actions awkward |
| A2C | policy + V | advantage (about the TD error) | lower variance; the paper used it for Atari |
| TRPO | policy + V | advantage | KL-divergence trust region limits each update; stable but complex; the paper used it for robotics |
| PPO | policy + V | clipped advantage | clips the ratio π_new/π_old to [1-ε, 1+ε]; simple and stable; the standard optimizer in RLHF for language models |

- **REINFORCE update:** `θ ← θ + α · G_t · ∇θ log π`; subtracting a baseline V(s) leads to actor-critic.
- **Q-learning update:** `Q(s,a) ← Q(s,a) + α [ r + γ · max_a′ Q(s′,a′) − Q(s,a) ]`. DQN used a neural network for Q on Atari.

> [!example] Example (numbers)
> Suppose Q(s, a) = 2, the reward is r = 1, γ = 0.9, the best next value is max Q(s′, a′) = 5, and α = 0.5. The target is `1 + 0.9·5 = 5.5`, the TD error is `5.5 − 2 = 3.5`, and the new value is `2 + 0.5·3.5 = 3.75`.
- **Advantage:** `A ≈ r + γV(s′) − V(s)`, how much better the action was than the state's average.

> [!example] Example (PPO clipping, ε = 0.2)
> The old policy gave an action probability 0.10 and the advantage is positive. If the update raises it to 0.15, the ratio is 1.5, which is clipped to 1.2, so the objective stops rewarding larger increases. If the advantage were negative, the clip would similarly limit how far the probability is lowered.
- **Lineage:** REINFORCE, add a critic (A2C), constrain updates (TRPO), simplify with clipping (PPO). Q-learning is a separate value-only branch.
- REINFORCE, A2C, TRPO, and PPO are on-policy; Q-learning is off-policy.
- The paper's reward predictor r̂ is **not** a value function: it gives immediate per-step reward learned from comparisons, while value is expected future reward under a policy.

## AlphaZero

### How does AlphaZero search a game tree too large to enumerate?

> [!tip] Short answer
> Monte Carlo tree search guided by a network that outputs a policy and a value.

| Network output | How MCTS uses it | What it saves |
|---|---|---|
| Policy (move probabilities) | prior: explore promising moves first | breadth |
| Value (expected outcome) | evaluate a leaf directly instead of playing random games to the end | depth |

- Moves in the simulations are selected by combining low visit count, high move probability, and high estimated value.
- After many simulations, the **visit counts** give improved move probabilities, better than the network's raw policy.

> [!example] Example (illustrative)
> In a Go position the network's policy gives move X 5% and move Y 30%. MCTS runs, say, 800 simulations and explores Y often but also tests X. If X turns out to win more often, the visit counts shift (for example X 55%, Y 25%). Those proportions become the training target for the policy, so the network learns that X is better than it first thought.

### Where does the training data come from, and what is the loss?

From **self-play**: the network plus MCTS plays against itself from randomly initialized weights, with no human games or knowledge beyond the rules.

| Stored per position | Trains |
|---|---|
| position s | the input |
| MCTS search probabilities | policy head (cross-entropy against the predicted policy) |
| final result z (+1 win, 0 draw, -1 loss) | value head (mean-squared error against the predicted value) |

### What is the knowledge discovery loop?

```
search (deliberate thinking) finds better moves than the raw network
  → train the network to match what the search found (update intuition)
  → a better network guides better search → repeat
```

Like learning addition, then multiplication, then exponents: each learned skill is a building block for increasingly complex behavior.

> [!question]+ Check yourself: what are the network's two outputs, and which training signal trains each?
> The policy output (move probabilities) is trained with cross-entropy against the MCTS search probabilities; the value output is trained with mean-squared error against the final game result z (+1, 0, -1).

## Deep Reinforcement Learning from Human Preferences (2017)

### What problem motivates the paper?

> [!tip] Short answer
> Many goals are hard to specify as a reward, and human feedback as a direct reward is too expensive. Learn a reward from human feedback, then optimize it with ordinary RL.

- **Hard to specify:** for tasks such as scrambling an egg, a hand-designed simple reward is typically optimized without satisfying our actual preferences (the misalignment concern).
- **Too expensive:** deep RL needs hundreds or thousands of hours of experience, so feedback must shrink by several orders of magnitude; the paper uses feedback on under 1% of interactions.
- **Demonstrations fail** for behaviors humans cannot demonstrate (a robot with a very non-human body), while humans can often recognize good behavior.
- **Goals:** handle tasks we can only recognize, work with non-expert teachers, scale to large problems, and be economical with feedback.

### What three processes does the method run?

| # | Process | Output |
|---|---|---|
| 1 | the policy acts in the environment; a standard RL algorithm (A2C for Atari, TRPO for robotics) updates it to maximize the predicted reward r̂ | trajectories |
| 2 | pairs of trajectory segments are selected and sent to a human for comparison | human comparisons |
| 3 | the reward model r̂ is fit to the comparisons by supervised learning | updated reward parameters |

They run **asynchronously**: trajectories flow 1 to 2, comparisons 2 to 3, reward-model parameters 3 to 1. The human is outside the inner RL loop; the reward predictor stands in for them.

Figure 1 flows:

| From to | What flows |
|---|---|
| environment to RL algorithm and reward predictor | observation |
| RL algorithm to environment | action |
| reward predictor to RL algorithm | predicted reward |
| human to reward predictor | comparison feedback |

### What is shown to the human, and what do they answer?

- Two **trajectory segments**, each a short sequence of observations and actions `σ = ((o₀,a₀), …, (o_{k−1},a_{k−1}))` showing what the agent actually did, presented as 1 to 2 second video clips.

| Human response | Stored as |
|---|---|
| clip 1 preferred | µ puts all its mass on 1 |
| clip 2 preferred | µ puts all its mass on 2 |
| equally good | µ is uniform |
| cannot compare | pair dropped |

- Each judgment is stored as a triple (σ¹, σ², µ) in a database D.
- **Comparisons instead of scores:** humans give consistent comparisons far more easily, and reward scales vary.
- **Clips instead of single states:** nearly as fast to judge but much more informative per label.

> [!example] Example (from the paper)
> Nobody wrote a reward for "backflip". Humans watched pairs of 1 to 2 second clips of the Hopper robot and picked the clip that looked more like a backflip, for example the one where it rotates in the air over the one where it falls over. About 900 comparisons, under an hour of human time, taught it to backflip, land upright, and repeat.

### How are comparisons turned into a reward function (Eq. 1, Section 2.2.3)?

> [!tip] Short answer
> Sum predicted reward over each clip and model the preference probability as a softmax (Bradley-Terry) of the two sums.

```
R¹ = Σₜ r̂(o¹ₜ, a¹ₜ)        R² = Σₜ r̂(o²ₜ, a²ₜ)
P̂[σ¹ ≻ σ²] = exp(R¹) / ( exp(R¹) + exp(R²) )  =  sigmoid(R¹ − R²)
```

| Property | Why it matters |
|---|---|
| depends only on R¹ − R² | absolute reward scale is irrelevant |
| equal sums give 0.5 | no preference |
| larger gap approaches 1 | confident preference |
| the two directions sum to 1 | valid probability |

- This is the **Bradley-Terry model** (Luce-Shepard choice rule), analogous to Elo ratings in chess: a rating difference gives a win probability, and clip rewards play the role of ratings.
- **Example:** R¹ = 2.0 and R² = 1.0 give about 0.73. If the human chose clip 1 the loss is -log 0.73 ≈ 0.31; if clip 2, -log 0.27 ≈ 1.31.
- **Loss:** cross-entropy between the predictions and the human labels µ.
- **Humans err**, so the paper assumes a 10% chance the human answers uniformly at random, keeping predictions away from 0 and 1.

> [!info] Paper detail
> The full method (Sections 2.2.3 and 2.2.4) fits an **ensemble** of reward predictors trained on bootstrap samples, holds out 1/e of the data for validation with ℓ2 regularization, normalizes the predicted rewards, and chooses which pairs to ask about by the highest **disagreement** between ensemble members. Scale: about 700 queries for the MuJoCo robotics tasks and 5,500 for Atari, with real human feedback taking between 30 minutes and 5 hours.

> [!question]+ Check yourself: if the network gives R¹ = 0.5 and R² = 1.5, what is the probability that the human prefers clip 1?
> `sigmoid(0.5 − 1.5) = sigmoid(−1) ≈ 0.27`, which is below 0.5 because clip 2 has the higher predicted reward.

### Why must feedback be gathered during training and not once at the start?

> [!tip] Short answer
> The agent's behavior keeps changing, so a reward model trained on early data covers only part of the true reward, and the agent can exploit the gap.

- The paper's ablation (Section 3.3): training the reward predictor only on queries gathered at the beginning ("no online queries") performs poorly because the distribution of states the agent visits changes over time.
- **Example (Pong, from the paper):** with offline reward training, the agent sometimes learns to avoid losing points but not to score them, which produces extremely long volleys that repeat the same sequence forever.
- So human feedback needs to be intertwined with RL learning rather than provided statically.

---

*Sources: [Deep Reinforcement Learning from Human Preferences](https://arxiv.org/abs/1706.03741) (Christiano et al., 2017) and [AlphaZero](https://arxiv.org/abs/1712.01815) (Silver et al., 2017). The human-preferences method, formulas, and experiment figures were checked against the paper. The fundamentals and AlphaZero sections follow lecture material, and the algorithm summaries (REINFORCE, Q-learning, A2C, TRPO, PPO) are standard formulations written from general knowledge. The worked examples with illustrative numbers are not from the sources.*

## Related Notes
- [[Reinforcement Learning]] - Agent, environment, and reward basics.
- [[Temporal Difference Learning]] - Credit assignment and the TD error.
- [[Actor-Critic Methods]] - Policy and value methods.
- [[AlphaZero]] - Self-play and tree search.
- [[Deep Reinforcement Learning from Human Preferences]] - The paper in note form.
- [[Transformer, GPT and BERT Q&A]] - The companion guide for the language-model papers.
