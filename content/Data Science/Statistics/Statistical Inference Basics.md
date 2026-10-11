---
title: Statistical Inference Basics
tags: [data-science, statistics, hypothesis-testing, bayesian, auto-captured]
draft: false
---
Inference turns a sample into statements about a population. This note covers the frequentist toolkit (p-values, confidence intervals, t-tests) and the Bayesian counterpart (credible intervals), with worked examples. Correlation tests are covered in [[Correlation Coefficients]].

## Core Ideas
- **Null hypothesis ($H_0$):** the "nothing is going on" claim, such as "the mean is 200" or "A equals B".
- **p-value:** the probability of data at least this extreme **if $H_0$ were true**. It is not $P(H_0 \text{ true})$ and not the chance the result is a fluke.
- **Confidence interval (CI):** a range from a procedure that captures the true value in 95% of repeated samples. It is not a 95% probability that this particular interval contains the truth.
- **t-test:** compares a mean (or difference) to a hypothesis, scaled by its uncertainty:

$$t = \frac{\text{estimate} - \text{hypothesized value}}{\text{standard error}}$$

The t distribution has heavier tails than the normal, accounting for estimating variance from a small sample.

### How the CI relates to $H_0$
The interval for a mean, $\bar x \pm t_{0.975,df}\cdot s/\sqrt n$, is computed from the sample alone and never uses $H_0$; only the t-statistic does. They connect by **test inversion**: a 95% CI is the set of null values a two-sided $\alpha=0.05$ test would not reject. For the mean this is exact. For proportions it is approximate (the Wald interval and the Wald test use different standard errors), and the Wilson score interval is the exact inversion of the score test.

## Worked Examples

| Test | Scenario | Result |
| :-- | :-- | :-- |
| One-sample | 12 API latencies vs. a 200 ms target; mean 215.4, SD 10.0 | $t=5.32$, df 11, $p=0.00025$, 95% CI [209.0, 221.8] ms |
| Two-sample (Welch) | Page load: variant A mean 3.18 s vs. B 2.71 s, 10 users each | $t=4.54$, df 16.3, $p=0.0003$, CI for A−B [0.25, 0.69] s |
| Paired | Blood pressure before/after for 8 patients | Mean drop 5.5, $t=5.40$, df 7, $p=0.001$, CI [3.1, 7.9] |
| Non-significant | Pearson of two unrelated variables, $n=30$ | $r=0.014$, $p=0.94$, CI [-0.35, 0.37] |

```python
from scipy import stats
stats.ttest_1samp(lat, 200)                  # one-sample
stats.ttest_ind(a, b, equal_var=False)       # Welch two-sample
stats.ttest_rel(before, after)               # paired
```
Prefer **Welch** by default: no equal-variance assumption and almost no cost when variances match. Use **paired** when the same units are measured twice; it removes between-unit variation. The last row shows that a large p-value means "not enough evidence": the wide CI still allows effects up to about ±0.35. The Pearson test is itself a t-test with $t = r\sqrt{(n-2)/(1-r^2)}$.

## From Statistics to a Business Decision
Take the latency example with a 200 ms target. The p-value says the service is almost certainly not meeting target; the CI says by roughly 9 to 22 ms. The interval is what supports a decision:

> Act if the lower bound is above the target (clearly failing). Collect more data if the interval straddles the target (inconclusive). Ignore if the upper bound is below the target (clearly meeting it).

The same test serves different uses: an SLA breach check, a regression check after a deploy, or confirming an optimization. Caveats that apply in practice:
- **Small samples:** 12 requests give a wide interval; about 45 would shrink the half-width to near ±3 ms at the same variability.
- **Skew and tails:** latency is right-skewed and business targets are usually p95/p99, which a mean test does not address. Use a bootstrap CI on the percentile.
- **Independence:** requests from one server or minute are correlated, so the effective n is smaller and the interval too narrow.
- **Practical vs. statistical significance:** with huge n, a 1 ms excess gets $p<0.001$. Set a threshold that matters before testing.
- **Framing:** "must be at most 200" suits a one-sided or non-inferiority test.

A test can only contradict an expectation or fail to; a non-significant result never proves the target is met.

## Assumptions

| Test | Assumes | If violated |
| :-- | :-- | :-- |
| One-sample, paired | Independent observations; mean (or paired differences) roughly normal, fine for moderate n by the CLT | Wilcoxon signed-rank, bootstrap |
| Two-sample | Independent groups; Welch needs no equal variances | Mann-Whitney U, permutation test |

Independence matters most; repeated measures on the same user and time series break it.

## Common Mistakes
1. Reading $p$ as $P(H_0 \text{ true})$.
2. Treating "significant" as "important"; read the CI.
3. Multiple comparisons: 20 tests at $\alpha=0.05$ yield about one false positive. Correct with Bonferroni or Benjamini-Hochberg.
4. Peeking in A/B tests and stopping when $p<0.05$; fix the sample size or use sequential methods.
5. Choosing a one-tailed test after seeing the direction.

## Bayesian Credible Intervals

| | Confidence interval | Credible interval |
| :-- | :-- | :-- |
| Parameter $\theta$ | Fixed, unknown | Random, with a distribution |
| Varies across | Repeated experiments | Your belief given this dataset |
| Built from | Sampling distribution | Posterior $p(\theta\mid \text{data}) \propto p(\text{data}\mid\theta)\,p(\theta)$ |
| "95%" means | The method captures $\theta$ in 95% of repeats | $P(\theta \in \text{interval}) = 0.95$ given data and prior |
| Prior | No | Yes, explicit |

Variants: **equal-tailed** (2.5th to 97.5th percentiles) and **HPD** (shortest interval holding 95% of the mass, better for skewed or multimodal posteriors).

**Example: conversion rate, 18 of 100.**

| Method | 95% interval |
| :-- | :-- |
| Wald confidence interval | [0.105, 0.255] |
| Clopper-Pearson confidence interval | [0.110, 0.269] |
| Credible, flat Beta(1,1) prior (posterior Beta(19, 83)) | [0.117, 0.267] |
| Credible, informative Beta(10, 40) prior | [0.129, 0.253] |

The flat prior nearly matches the frequentist answers; an informative prior pulls toward its mean and tightens the interval. The posterior also answers direct questions: $P(\text{rate}>15\%)=0.83$, and comparing A (18/100) with B (27/100) gives $P(B>A)=0.93$ with a 95% credible interval for the lift of [-0.03, +0.20].

```python
post = stats.beta(1 + k, 1 + n - k)
post.ppf([0.025, 0.975])   # credible interval
post.sf(0.15)              # P(rate > 0.15)
```

**Use credible intervals** with real prior information, small samples, a need for direct probability statements and decision thresholds, hierarchical models, or when uncertainty must propagate (Bayesian ML, Thompson sampling). **Use confidence intervals** when you need guaranteed long-run coverage, no defensible prior exists, or convention and tooling require them. Caveats: results depend on the prior (run a sensitivity analysis), coverage holds only if the prior is right, and non-conjugate models need MCMC or variational inference (PyMC, Stan). See also [[4. Bayesian Decision Theory]] and [[1. Probability]].
*Source: [SciPy stats documentation](https://docs.scipy.org/doc/scipy/reference/stats.html).*
