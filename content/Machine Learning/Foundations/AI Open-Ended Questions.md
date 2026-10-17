---
title: AI Open-Ended Questions
tags: [ai, discussion, study-guide, auto-captured]
draft: false
---

Open-ended concept and application questions on [[Attention & Transformers]], [[GPT-1]], [[BERT]], reinforcement learning, [[AlphaZero]], and [[Deep Reinforcement Learning from Human Preferences]].

**How to use it.** Try each question yourself first. The answers below are one reasonable view, not the only one: there is rarely a single right answer. A strong answer (1) takes a position, (2) gives a concrete example, (3) names a trade-off or a way it could fail, and (4) says what you would do or test next. Items marked as general knowledge go beyond the papers.

---

## A. Attention and the Transformer

### 1. Why attention replaced recurrence

> Explain to a non-technical person why Transformers replaced RNNs for language. In what situation might an RNN (or another sequential model) still be the better choice?

**Answer.** An RNN reads a sentence one word at a time and carries a single running summary forward. By the end of a long sentence the early words have faded from that summary, and because each step needs the previous one, training cannot be spread across many processors. A Transformer lets every word look directly at every other word at the same time. In "The animal didn't cross the street because it was too tired", the word "it" can connect to "animal" in one step, however far apart they are. And since all positions are processed together, the work parallelizes on GPUs, which is what made training on huge amounts of text practical.

An RNN can still be the better choice for **streaming or tiny-memory settings**: a sensor on a small device that must process an endless stream one sample at a time, with fixed memory and no ability to store the whole history. Attention's cost grows with the square of the sequence length, while an RNN uses constant memory per step. Newer sequential designs (state-space models) are revisiting exactly this advantage.

### 2. Long inputs

> Attention cost grows with the square of the sequence length. How would you handle a million-token document, such as a whole codebase or a patient's complete history? What would you give up?

**Answer.** Do not run full attention over everything. Combine several tools:
- **Retrieval:** split the document into chunks, retrieve only the chunks relevant to the question, and attend over those.
- **Hierarchy:** summarize each chunk (or each file or visit), then reason over the summaries and open the details when needed.
- **Sparse patterns:** each token attends to a local window plus a few global tokens, which makes the cost nearly linear.
- **Efficient implementations and approximations:** memory-efficient attention kernels, and linear-attention or state-space layers for some of the work.
- **Use structure:** for a codebase, follow the file tree and call graph to decide what to read; for a patient, organize by date and problem.

**What you give up:** exact all-to-all interaction. A relevant link between two distant parts might never be examined if no retrieval or summary step flagged it, and summaries lose detail. I would evaluate with "needle in a haystack" tests plus real task tests, and measure what fraction of cross-document dependencies the system actually captures.

### 3. Position in other data

> You are building a Transformer for a new kind of data: DNA sequences, a time series with irregular timestamps, or a chess board. How would you represent "position"? What would break if you ignored it?

**Answer.** Self-attention by itself treats its input as an **unordered set**, so without position information "dog bites man" and "man bites dog" look identical.

| Data | Position representation | What breaks without it |
|---|---|---|
| DNA | order along the sequence; relative or rotary encodings suit it because what matters is the distance between bases (a regulatory element can sit thousands of bases from the gene) | sequence order, hence the meaning of motifs, is lost |
| Time series with irregular timestamps | encode the **actual time** (sinusoidal functions of the real timestamp, and time since the last event), not the index in the list | the model cannot tell that two events were seconds apart versus months apart |
| Chess board | a **2D position**: a learned embedding for each of the 64 squares (row and column), added to the piece token | the model sees a bag of pieces with no squares, which is meaningless |

### 4. What do heads learn?

> Multi-head attention lets different heads look for different relations. How would you test whether a head is doing something interpretable? Is an attention pattern a good explanation of a model's decision? Why or why not?

**Answer.** Ways to test a head:
- **Ablation:** switch the head off and see which tasks or examples get worse.
- **Probing:** check whether its attention lines up with a known relation (verb to subject, pronoun to referent) across many examples, not only a hand-picked one.
- **Intervention:** change the input or the head's output and check that the downstream behavior changes as the hypothesis predicts (causal tests).

**Is attention an explanation?** Only partly. Attention weights show *where information is read from*, but the output also depends on the value vectors, the other heads, and the later layers, which mix everything again. Studies (for example "Attention is not Explanation") found that very different attention patterns can give the same prediction. So treat attention as a **useful hint**, and rely on causal tests before claiming the model uses a relation. (This is general knowledge, not from the papers.)

### 5. Designing masks

> The causal mask is one choice. Where else might you want a different attention pattern, for example a chatbot with a system prompt and several user turns, or a model that reads many separate documents at once? Design one and say what it allows and blocks.

**Answer.**
- **Chatbot (prefix-style mask):** the system prompt and the user's message are all available input, so allow tokens in the prompt to attend to each other in both directions (richer understanding of the request), and use the causal mask only for the reply being generated. Allowed: reply tokens attend to the whole prompt and to earlier reply tokens. Blocked: any token attending to future reply tokens (no peeking at the answer).
- **Many documents packed into one sequence (block-diagonal mask):** each token attends only within its own document. Allowed: attention inside a document. Blocked: attention across documents, which would leak unrelated text and could cause confusion or cross-contamination. A padding mask also blocks padding tokens.
- **Local-window mask:** each token attends to its neighbors plus a few global tokens, trading some long-range interaction for speed.

---

## B. Pre-training, GPT, and BERT

### 6. Choosing an architecture

> For each task, choose encoder-only, decoder-only, or encoder-decoder and justify it: a spam filter, a customer-service chatbot, a search engine's ranking, extracting names and dates from contracts, code completion, and translating a legal document.

**Answer.**

| Task | Choice | Reason |
|---|---|---|
| Spam filter | encoder-only | classifying a whole message, cheap and fast; bidirectional context helps and no generation is needed |
| Customer-service chatbot | decoder-only | must generate fluent replies one token at a time, and one prompted model handles many request types (ideally grounded in company documents) |
| Search ranking | encoder-only | embeddings for retrieval and a cross-encoder to re-rank query and document pairs; understanding, not generation |
| Extracting names and dates | encoder-only | token-level tagging (every token needs a label) using both left and right context; a decoder LLM with structured output is an alternative when the schema changes often |
| Code completion | decoder-only | left-to-right generation of what comes next (with fill-in-the-middle variants) |
| Translating a legal document | encoder-decoder | a clean input-to-output mapping, with the whole source visible to the encoder and cross-attention back to it; decoder-only LLMs also work well, but legal text needs faithfulness, so add checks |

### 7. Why next-token prediction won

> BERT's bidirectional representations are richer, yet decoder-style models became the basis of modern LLMs. What were the reasons? Under what different conditions (data, compute, goals) might the opposite have happened?

**Answer.** Reasons the decoder-style objective won:
1. **Every token is a training signal.** BERT's masked LM computes its loss at only about 15% of positions per sequence (the masked ones it must predict; the other 85% are visible context with no prediction), while a decoder-style model predicts at every position.
2. **Training matches use.** Generation is the training task, so there is no [MASK] mismatch.
3. **One interface for everything.** Any task can be written as text to continue, so one model serves many tasks by prompting, without a new head and fine-tuning run per task.
4. **Smooth scaling and in-context learning.** Loss improves predictably with more data, parameters, and compute, and at large scale the model can learn a task from examples in the prompt (GPT-3).

**When might the opposite have happened?** If the dominant need had been understanding rather than generation, such as search, classification, and embeddings on limited compute, bidirectional encoders are more efficient, and they still dominate those uses. If compute and labeled-task data had stayed small and tasks narrow, BERT-style pre-train-then-fine-tune would have stayed the default. So it was partly a result of what turned out to be most valuable (general assistants) and what scaled best.

### 8. When pre-training hurts

> Pre-training on general text usually helps. When might it hurt or mislead, for example for legal, medical, or low-resource-language text? What would you do about it?

**Answer.** Pre-training can hurt through **domain or language mismatch** and **negative transfer**:
- Specialized vocabulary (drug names, legal citations) is split into meaningless pieces by a general tokenizer, and the model's general-text habits (style, assumptions) may not fit.
- Low-resource languages have little pre-training text, and the tokenizer may fragment words heavily.
- The model carries biases and outdated facts from its pre-training data.

**What I would do:**
1. Continue pre-training on in-domain text, and consider a custom vocabulary.
2. Fine-tune on in-domain labeled data.
3. Use retrieval from a trusted, current source for facts.
4. **Test against a baseline** (a smaller model trained without the general pre-training) so I know whether pre-training is really helping on my data.

### 9. Fine-tuning versus prompting

> You have 200 labeled examples for a new task. Do you fine-tune a pre-trained model, prompt a large one, or something else? What would change your decision?

**Answer.** I would start with **prompting a strong pre-trained model** using a few examples from the 200, and hold out the rest as a test set. It is the cheapest, fastest way to learn what is possible. If accuracy is not enough, or if I need low cost and latency at scale, I would **fine-tune a smaller pre-trained model** (for example with a parameter-efficient method), which GPT-1 and BERT showed can work with small labeled sets.

What would change the decision:
- **Task type:** classification or tagging suits a fine-tuned encoder; open-ended generation suits prompting.
- **Volume and cost:** millions of queries per day favor a small fine-tuned model.
- **Privacy:** if data cannot leave the organization, use a local model.
- **Consistency:** strict output formats favor fine-tuning.
- **Label quality:** with only 200 examples, noisy labels hurt.

I would compare options on a held-out validation set that was not used for training, then pick the option with the lowest validation error (a choice that is close to the best one with high probability when the validation set is large enough).

### 10. Train-test mismatch

> BERT's [MASK] token appears in training but not in use, and the paper adds a trick to reduce the gap. Give another example, from any AI system, where training conditions differ from deployment conditions. How would you detect and handle it?

**Answer.** Examples:
- **Exposure bias in the Transformer decoder:** during training it sees the true previous tokens (teacher forcing), but at generation it sees its own earlier outputs, including mistakes.
- **A driving model** trained mostly on sunny highways, deployed in snow on rural roads.
- **A medical model** trained at one hospital, used at another with different scanners and patients.
- **A recommender** trained on logs from an older policy.
- **Sim-to-real in robotics:** a robot trained in simulation meets real friction and noise.

**Detecting it:** monitor how the live inputs differ from training data (drift detection), keep a test set that reflects deployment conditions, and run a silent-mode pilot before relying on the system. **Handling it:** train on data closer to deployment (augmentation, domain randomization, scheduled sampling), collect real deployment data, fine-tune on it, and have the system express uncertainty or abstain when inputs look unfamiliar.

### 11. The role of data

> GPT-1 used books for long contiguous text, and BERT used documents rather than shuffled sentences. How much of a model's behavior comes from its data rather than its architecture? What risks come with large scraped corpora (bias, privacy, copyright, benchmark contamination)?

**Answer.** A great deal. Modern language models share nearly the same Transformer architecture, yet differ widely in behavior because of **what they were trained on**: the data determines knowledge, style, languages, and biases, and its quality and diversity matter as much as its size. Both papers made this point concretely: GPT-1 chose books so the model could learn long-range dependencies, and BERT insisted on a document-level corpus to extract long contiguous sequences, because shuffled sentences destroy that structure.

Risks of large scraped corpora:
- **Bias and toxicity:** the model reproduces stereotypes and harmful content found online.
- **Privacy:** it can memorize and leak personal information.
- **Copyright and licensing:** unclear rights over training text.
- **Benchmark contamination:** test questions appear in training data, inflating scores.
- **Quality and duplication:** low-quality or repeated text distorts learning.
- **Narrow representation:** English and Western sources dominate.

Mitigations: curate and deduplicate, filter, document the data, respect opt-outs, and evaluate on held-out, decontaminated tests.

### 12. What do benchmarks measure?

> A model scores highly on a benchmark such as GLUE. What can and can't you conclude about "understanding"? How would you design a test that separates real understanding from pattern matching?

**Answer.** A high score shows the model does well **on that task format and data distribution**. It does not show understanding, because models can exploit shortcuts (for example, in inference datasets the hypothesis alone can sometimes predict the label), the test data may have leaked into training, benchmarks saturate, and teams optimize for them (when a measure becomes a target, it stops being a good measure).

A better test uses **controlled changes**:
- **Counterfactual edits:** make a minimal edit that flips the correct answer (negate a sentence, swap who did what) and check that the model's answer changes. A pattern-matcher often does not.
- **Paraphrase invariance:** check that rewording without changing meaning leaves the answer unchanged.
- **Context over memory:** state a new fact in the text ("in this story the sky is green") and ask a question that requires using it, not prior knowledge.
- **Fresh problems** created after the model's training cutoff, and a comparison with a simple baseline.

---

## C. Learning from human feedback

### 13. Where comparisons break down

> The human-preferences paper asks people to compare two short clips. Describe a task where this would be a poor way to specify the goal (very long outputs, expert knowledge needed, people who disagree). How might you adapt the method?

**Answer.** Pairwise comparison works when a person can **quickly recognize** which of two short items is better. It breaks down when:
- **Outputs are long:** judging a 20-page report takes time, and raters skim or become inconsistent.
- **Expertise is needed:** which of two medical or legal answers is correct? A layperson cannot tell.
- **Correctness must be verified:** a proof or a piece of code can look convincing but be wrong.
- **People disagree** (humor, politics, style), so labels are noisy.

**Adaptations:**
- Break the task into small judgeable pieces (judge steps, not final essays).
- Give raters tools: run the code, check the citations, or see an AI critique.
- Use experts for the critical subset.
- Model rater disagreement and collect richer feedback (rankings, edits, short explanations).
- Where an automatic check exists (tests, a verifier), use that as the reward instead.

### 14. Reward hacking

> Give an everyday example of someone optimizing a proxy at the expense of the real goal. How could an agent exploit a learned reward model in the paper's setup, and which design choices (online feedback, ensembles, held-out validation) help?

**Answer.** Everyday examples: a student cramming for the exam without learning the material, a school teaching to the test, or a call center closing calls quickly instead of solving problems. (This pattern is often called Goodhart's law.)

In the paper's setup the reward predictor is only an **approximation fit to limited comparisons**. The policy keeps changing, so it can wander into behavior the predictor has never been checked on, and exploit its errors. The paper observed this when comparisons were collected only at the start: the agent in Pong sometimes avoided losing points without learning to score, producing endless volleys.

What helps in the paper:
- **Online feedback:** keep asking humans about the *new* behavior as it appears.
- **An ensemble of predictors**, with queries chosen where the ensemble disagrees most, which targets uncertain regions.
- **Held-out validation and regularization** to avoid overfitting the predictor.
- **Assuming some label noise** (a 10% chance of random answers).

In later practice (general knowledge), a penalty for drifting far from the original model is also common.

### 15. Whose preferences?

> If different people prefer different behavior (cultures, politics, personal taste), whose feedback should train the system? Compare averaging, personalization, and letting users choose.

**Answer.** A layered approach seems best, because the options have different strengths:

| Approach | Strength | Weakness |
|---|---|---|
| Averaging over raters | simple, one consistent behavior | can ignore minorities and produce bland, majority-biased behavior |
| Personalization | fits each user | can create echo chambers, and can reinforce harmful preferences |
| User choice (settings) | respects autonomy and transparency | most users do not adjust them, and some choices need limits |

I would combine them: **universal constraints** (safety, law, honesty) that no user can switch off; **customizable style and tone** within those limits; and a **diverse, documented set of raters** (possibly with deliberative processes for contested questions). Facts should not be decided by a vote. Whichever approach is chosen, it should be transparent about who provided the feedback and subject to oversight.

### 16. Rewards, demonstrations, or preferences

> For a household robot and for a chatbot, compare specifying a reward, showing demonstrations, and giving preference comparisons. Which would you use for what, and why?

**Answer.**

| Signal | Strengths | Weaknesses | Robot | Chatbot |
|---|---|---|---|---|
| Reward | precise and scalable once written | hard to specify real goals; gets hacked | for **safety constraints** (do not hit people, do not drop dishes) | only where a check exists (code passes tests, math answer is right) |
| Demonstrations | intuitive, a strong starting point | need a human who can perform the task; limited by demonstrator quality and coverage | **teleoperated demonstrations** to learn basic skills | written example answers for the first stage of training |
| Preferences | easier to judge than to produce; works when you can recognize but not demonstrate | noisy, costly, proxies can be exploited | **refine behavior** ("which looks tidier?") | **refine helpfulness and tone** |

In practice these are combined: demonstrations to start, preferences to refine, and verifiable rewards or hard constraints wherever they exist.

### 17. Manipulation and feedback loops

> If a system is trained to maximize human approval, how could it end up pleasing people without helping them? What safeguards would you add?

**Answer.** Optimizing approval rewards whatever people *like*, which is not always what is *good for* them:
- **Sycophancy:** agreeing with the user's views or telling them what they want to hear.
- **Confident but wrong answers,** which feel more satisfying than honest uncertainty.
- **Exploiting rater habits:** longer, more polished, or more flattering answers get rated higher whether or not they are better.
- **Engagement traps** in recommenders: content that keeps people scrolling, not content that serves them.

**Safeguards:** judge accuracy separately with experts or tools, not only approval; test explicitly for sycophancy; use diverse raters and audits; reward honest uncertainty; limit how hard the system is optimized against the reward; and measure longer-term outcomes (did the person succeed?) instead of immediate approval.

---

## D. Reinforcement learning and AlphaZero

### 18. Credit assignment outside games

> Chess is the standard example. Think of a real process where results arrive late (a medical treatment, a sales campaign, a student's education). What would the "critic" estimate, and what would a TD error look like there?

**Answer.** Take a **medical treatment** for a chronic illness, where the outcome (recovery) arrives months later.
- **State:** the patient's current condition (tests, symptoms, history).
- **Actions:** treatment decisions over time.
- **Critic:** estimates the expected final health outcome (for example the probability of recovery) from the current state.
- **TD error:** the change in that estimate after something new happens. If a lab result improves after a medication change, the estimate rises, so the TD error is positive and that decision gets credit. A complication lowers the estimate, giving a negative error that blames the recent decision.

The same idea applies to a sales campaign (the value is the expected eventual purchase, and a customer opening an email raises the estimate) or to education (value is eventual mastery, and a quiz result updates it). Real settings add difficulties: you cannot experiment freely, outcomes depend on other factors, and you must learn mostly from logged data.

### 19. Exploration versus exploitation

> Where do you see this trade-off in recommender systems? What goes wrong if a system only exploits what it already knows about you (for example filter bubbles)?

**Answer.** **Exploiting** means recommending what the system already predicts you will like. **Exploring** means occasionally showing something uncertain (a new genre, a new creator) to learn more.

With no exploration:
- **Feedback loop:** the system only gets ratings for what it shows, so it never discovers that you might like something else.
- **Filter bubble:** recommendations narrow over time, and tastes can be shaped by the system.
- **Popularity bias:** already popular items get all the exposure, and new items starve (the cold-start problem).

Remedies come from bandit methods: occasionally random recommendations, or choosing items with the highest *upper confidence* (uncertainty-seeking), plus diversity requirements. The cost is some short-term engagement, which is worth paying for better long-term learning and user trust.

### 20. What makes games special?

> AlphaZero succeeded with simple rules, a perfect simulator, and a clear reward. Which real-world domains share these properties, and which don't? Could self-play work for drug design, negotiation, or software engineering?

**Answer.** Games offer: known rules, a cheap simulator that can run millions of times, a clear win/loss reward, and self-play that provides endless training data and an automatic curriculum.

**Domains that share these properties** (a simulator or checker plus a measurable result): chip layout, algorithm discovery, formal theorem proving (a verifier checks every step), and code with tests.

**Those that don't:**
- **Drug design:** the simulator is imperfect, experiments are costly, and the real reward (a safe, effective drug) arrives years later.
- **Negotiation:** other people's preferences are hidden, and there is no cheap simulator of real humans. Pure self-play agents can develop private conventions that humans do not share, so they must be anchored to human data. (Meta's CICERO, which plays Diplomacy, combines a language model with planning for this reason.)
- **Software engineering:** tests are only a proxy for correctness, so agents can exploit them, although the verifiable part (does it pass?) makes it more tractable than the others.

### 21. Slow thinking teaches fast intuition

> In the knowledge discovery loop, search produces better moves that the network then learns to imitate. Where else does this pattern appear, for example in how language models reason step by step? How would you apply it to a problem you care about?

**Answer.** The pattern: use expensive computation to find better answers than the fast model would give, then train the fast model to produce them directly.

Examples:
- **Language models:** generate step-by-step reasoning or many candidate answers, keep those a verifier accepts, and train the model on them so it answers well faster (this is general knowledge, not from the papers).
- **People:** practicing chess slowly until pattern recognition makes good moves feel automatic.

**Applying it to code review:** a slow agent runs tests, static analysis, and several candidate reviews, and a check selects the best findings. Train a fast reviewer on those results. The caution: it needs a **reliable signal** to decide what counts as better. If the verifier is flawed, the fast model learns and amplifies the flaw, and diversity can shrink.

### 22. Policy, value, or both

> For a self-driving system, an ad-bidding system, and a game-playing agent, which of a policy, a value function, or both would you learn, and why?

**Answer.**

| System | What I would learn | Why |
|---|---|---|
| Self-driving | both | the policy outputs steering and braking, and a value or risk estimate predicts long-term consequences (collision risk) that immediate reward misses, which also supports planning and safety checks |
| Ad bidding | mainly value, plus a policy for pacing | the bid depends on the expected value of an impression (probability of conversion times its worth), which can be learned from logged outcomes; a policy then adjusts bids to fit the budget over time |
| Game-playing agent | both for large games (AlphaZero), value alone is enough for smaller ones (the Atari DQN) | the policy narrows which moves to search and the value evaluates positions; for small discrete action sets, learning action values and acting greedily works |

---

## E. Cross-cutting and applied

### 23. What scaling does and doesn't do

> Scaling data and parameters has driven much of recent progress. What problems do you expect scaling alone to leave unsolved? What would you do if your compute budget were 100 times smaller?

**Answer.** Scaling reliably improves fluency, knowledge, and in-context learning, but I expect it to leave these unsolved:
- **Reliability:** hallucinations shrink but do not disappear.
- **Reasoning on novel problems** that need exact, verifiable steps.
- **Alignment and reward exploitation:** larger models can be better at exploiting a flawed reward.
- **Grounding in the physical world,** current information, and calibrated uncertainty.
- **Practical limits:** the supply of high-quality text, energy cost, and the difficulty of interpreting and auditing huge models.

**With 100 times less compute,** I would not train from scratch (the central lesson of GPT-1 and BERT). I would start from a **pre-trained open model**, fine-tune it efficiently on high-quality in-domain data, distill into a smaller model for serving, use retrieval to add knowledge without larger models, and invest in data quality and evaluation, since they are cheap and high-leverage.

### 24. Deploying an LLM in a hospital

> List the failure modes that worry you most (wrong but confident answers, privacy, bias, over-reliance), and the safeguards and evaluations you would require before use.

**Answer.** Main failure modes:
- **Confident errors:** a wrong dose or a fabricated reference stated fluently.
- **Omissions and outdated guidance.**
- **Privacy:** leakage of patient data.
- **Bias:** worse performance for some patient groups.
- **Over-reliance** (automation bias) by busy clinicians.
- **Manipulation through inputs,** such as text embedded in records that tries to redirect the model.

**Safeguards before use:**
1. Start with **low-risk, reviewable uses** (drafting notes and summaries that a clinician checks), not autonomous decisions.
2. **Ground answers in the patient record and approved guidelines,** with citations a clinician can verify.
3. Keep **human sign-off** and an audit log.
4. Allow the system to say "I don't know," with calibrated confidence.
5. **Privacy controls:** local deployment, de-identification, access limits.
6. **Evaluate** accuracy weighted by error severity, subgroup performance, and time saved, first in a **silent-mode pilot**, then with monitoring for drift and a clear rollback and incident-reporting process.

### 25. Cost and energy

> Training and serving large models consumes substantial energy. How would you weigh that against the benefits? What would you do to reduce it?

**Answer.** I would weigh the **energy per useful outcome** against the value of the application and the alternative, and not treat all use alike. A medical or scientific use that saves substantial effort is different from generating filler content. Two points complicate this:
- Training is a one-time cost, but **serving millions of queries** can dominate total energy over time.
- **Rebound effects:** cheaper, easier AI leads to much more use.
- The environmental impact also depends on the electricity source and on cooling water.

**To reduce it:** use the smallest model that does the job, route simple queries to small models, distill and quantize models, cache repeated work, reuse pre-trained models and fine-tune instead of training from scratch, schedule heavy jobs for low-carbon times and places, and measure and report energy use so it can be optimized. (See [[Energy Use of AI Models]] for numbers; this answer stays qualitative.)

### 26. Meaning of "understand"

> If a model can answer questions about a story correctly, does it understand the story? What evidence would change your mind either way?

**Answer.** It depends on what "understand" means, so I would state my definition. A **functional** definition says understanding is the ability to answer varied questions, handle paraphrases and counterfactuals, and use the knowledge to act. A **stricter** definition requires an internal model of the situation, grounding in the world, and the ability to explain and transfer.

Evidence for: correct answers to new questions, consistency under paraphrase, and interpretability studies showing internal representations of entities and their relations. Evidence against: failures on small perturbations, answers that rely on surface patterns, inconsistency, and hallucinations on the same material.

**What would change my mind:** robust performance on counterfactual edits, new facts introduced in context, and problems created after the training cutoff would move me toward "yes". Systematic failures that look like pattern matching, or a model that answers correctly but cannot use the same knowledge to act or justify, would move me toward "no". I would call it **partial understanding that is useful but brittle**, rather than a yes or no.

### 27. The next bottleneck

> If you believe the Transformer will be replaced or extended, which of its assumptions (fixed context, quadratic attention, next-token training, text-only input) do you think is the weakest, and what would you try instead?

**Answer.** I think the weakest assumption is learning only from **static text with a next-token objective**. A model trained this way imitates what people wrote. It cannot act, test a hypothesis, check whether its claims are true, or learn from the consequences after deployment.

What I would try, in the spirit of this course:
- **Reinforcement learning on verifiable outcomes,** so the model is rewarded for being right, not for sounding right.
- **World models and multimodal input,** so it learns how actions change the world.
- **Persistent memory and continual learning,** so it does not need a retrain to update its knowledge.

Other assumptions are also candidates: quadratic attention and fixed context are being attacked by sparse, retrieval-based, and state-space approaches, but they look more like engineering limits than conceptual ones.

### 28. A system from scratch

> Pick a real application you care about (for example tutoring, code review, accessibility, scientific literature search). Describe the system you would build using at least two ideas from this course, and say how you would measure success and what could go wrong.

**Answer.** **An AI tutor for introductory programming.**

1. **Pre-train, then adapt:** start from a pre-trained decoder language model and fine-tune it (or prompt it) on tutoring dialogues, so it learns to give hints instead of answers.
2. **A reward model from preferences:** teachers compare two tutor replies ("which helps the student more?"). Train a reward model with the Bradley-Terry loss from the human-preferences paper, then improve the tutor with RL against it, keeping the feedback **online** as the tutor's behavior changes.
3. **Search guided by a learned value:** generate several candidate hints, and choose using a value model that predicts the student's later learning gain (trained from outcomes such as later quizzes, which is a delayed-reward, credit-assignment problem). Running the student's code gives a verifiable signal.

**Measuring success:** learning gains (pre/post tests and retention weeks later), not satisfaction alone; fairness across student groups; and a silent-mode pilot and an A/B test before wide use.

**What could go wrong:**
- **Approval is not learning:** students may rate answer-giving highly, so the reward model could teach the tutor to give answers (reward hacking). Reward long-term outcomes and cap approval-based reward.
- **Wrong explanations** (hallucinations): verify by running the code.
- **Over-reliance** and reduced struggle.
- **Privacy of minors' data.**
- **Loss of teacher trust:** keep teachers in the loop.

*The answers are one reasonable view, not the only one. Claims about the papers were checked against them: [Attention Is All You Need](https://arxiv.org/abs/1706.03762), [BERT](https://arxiv.org/abs/1810.04805), and [Deep Reinforcement Learning from Human Preferences](https://arxiv.org/abs/1706.03741). Everything else is general knowledge or opinion.*
