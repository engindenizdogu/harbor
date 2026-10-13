---
title: Correlation Coefficients
tags: [data-science, statistics, correlation, auto-captured]
draft: false
---
A **correlation coefficient** summarizes how strongly two variables move together on a scale from -1 (perfectly opposite) to +1 (perfectly together). Pearson, Spearman, and Kendall differ in the *kind* of togetherness they detect, and point-biserial and phi cover binary variables. For how to test and put intervals on them, see [[Statistical Inference Basics]].

> [!warning] Zero correlation is not independence
> A coefficient of 0 only means there is no *linear* relationship (Pearson) or no *monotonic* one (Spearman, Kendall). Independent variables always have correlation 0, but the reverse fails: $y = x^2$ on a symmetric range has $r \approx 0$ despite perfect dependence. The exception is a **jointly** bivariate normal pair, where uncorrelated does imply independent. Variables that are each normal but not jointly normal can be uncorrelated yet dependent.

## Pearson (linear)

$$r = \frac{\operatorname{cov}(X,Y)}{\sigma_X \sigma_Y} = \frac{\sum (x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum (x_i-\bar x)^2}\sqrt{\sum (y_i-\bar y)^2}}$$

- Measures how well a straight line fits; $r^2$ is the share of variance explained by the linear fit.
- Uses raw values, so a single outlier can move it a lot. Anscombe's quartet shows four very different datasets sharing the same $r$.

## Spearman rank (monotonic)

$$\rho_s = r\big(\text{rank}(X), \text{rank}(Y)\big) \;\overset{\text{no ties}}{=}\; 1 - \frac{6\sum d_i^2}{n(n^2-1)}$$

- Pearson applied to ranks, so any monotonic curve (such as $y = e^x$) scores 1.
- Robust to outliers; suitable for ordinal data. Ties get the average rank, and with many ties use the Pearson-on-ranks form, not the shortcut.

## Kendall's tau (concordance)
A pair of observations is **concordant** if both variables order it the same way, otherwise **discordant**.

$$\tau_a = \frac{C - D}{\binom n2}, \qquad \tau_b = \frac{C-D}{\sqrt{(n_0-n_1)(n_0-n_2)}}$$

$n_0=\binom n2$; $n_1, n_2$ count pairs tied in $X$ and in $Y$. Use **$\tau_b$** with ties (SciPy's default).

- Meaning: $\tau = P(\text{concordant}) - P(\text{discordant})$ for a random pair.
- Robust, best for small samples and many ties; usually smaller in magnitude than Spearman.
- Naive cost $O(n^2)$; Knight's algorithm gives $O(n\log n)$.
- Under a bivariate normal only: $\tau = \tfrac{2}{\pi}\arcsin r$ and $\rho_s = \tfrac{6}{\pi}\arcsin(r/2)$.

## Comparison

| | Pearson | Spearman | Kendall |
| :-- | :-- | :-- | :-- |
| Detects | Linear | Monotonic | Monotonic |
| Uses | Raw values | Ranks | Pair orderings |
| Outlier robust | No | Yes | Yes |
| Ordinal data | No | Yes | Yes |
| Small n / many ties | Fine | OK | Best |
| Interpretation | $r^2$ = variance explained | Pearson on ranks | Concordant minus discordant probability |

## Example
`x = [1,2,3,4,5]`, `y = [1,2,3,4,100]` is perfectly monotonic with one extreme point. Pearson $\approx 0.73$ (the outlier distorts the fit); Spearman $= 1$ and Kendall $= 1$.

```python
from scipy.stats import pearsonr, spearmanr, kendalltau
pearsonr(x, y), spearmanr(x, y), kendalltau(x, y)
```
*Source: [SciPy statistics reference](https://docs.scipy.org/doc/scipy/reference/stats.html).*

## Which to Use
1. Plot the scatter first.
2. Clean, continuous, roughly linear data: **Pearson**.
3. Curved but monotonic, outliers, or ordinal ratings: **Spearman**.
4. Small sample, many ties, or a probabilistic reading wanted: **Kendall**.
5. Non-monotonic patterns (U-shapes, cycles): none of these work. Use distance correlation (zero only under independence), mutual information, or a plot.

Correlation never implies causation. In practice, correlation matrices and heatmaps are a standard step in [[Exploratory Data Analysis]].

## Monotonic Functions
A function is **monotonic** if it never changes direction: non-decreasing ($x_1\le x_2 \Rightarrow f(x_1)\le f(x_2)$) or non-increasing. Every line with nonzero slope is monotonic, but so are $e^x$, $\log x$, and $-x^3$. $x^2$ over all reals and $\sin x$ are not. This is the gap Spearman and Kendall exploit: they score 1 whenever the ranking is perfectly preserved, whatever the curve.

## Ranking Is Not Binning
Spearman ranks each variable separately, so it works when one variable is continuous and the other ordinal (or both are either). Each distinct value gets its own rank and ties share the average rank, e.g. ages `[23, 31, 45, 31, 60]` get ranks `[1, 2.5, 4, 2.5, 5]`. Order is preserved; only the spacing is discarded, which is why outliers cannot dominate. With heavy ties from a short ordinal scale, Kendall's $\tau_b$ is often preferable.

## Ordinal Association and Other Variable Types
**Ordinal** variables have an order but no meaningful distances (star ratings, education level). An **ordinal association** is the tendency for higher ranks of one variable to go with higher (or lower) ranks of another, using only order. Kendall's tau captures this directly through concordant and discordant pairs.

| Coefficient | Variables | Example | Result |
| :-- | :-- | :-- | :-- |
| Pearson | Two continuous, linear | Hours studied vs. exam score | $r=0.996$ |
| Spearman | Continuous or ordinal, monotonic | Saturating dose-response (1 to 32 mg) | $\rho_s=1.0$, Pearson only $0.69$ |
| Kendall | Ordinal, small n, many ties | Satisfaction (1 to 5) vs. loyalty tier (1 to 3) | $\tau_b=0.67$ |
| Point-biserial | Continuous and binary | Passed (0/1) vs. hours studied | $r_{pb}=0.76$ |
| Phi | Two binary | Smoker vs. disease in a 2x2 table | $\varphi=0.41$ |

**Point-biserial** is Pearson with the binary variable coded 0/1:

$$r_{pb} = \frac{\bar x_1 - \bar x_0}{s_x}\sqrt{\frac{n_1 n_0}{n^2}}$$

Testing $r_{pb}=0$ is equivalent to a pooled two-sample t-test of the group means. Use it for a true dichotomy; an artificially split continuous variable calls for the biserial coefficient.

**Phi** is Pearson on two 0/1 variables. From a 2x2 table with counts $a,b,c,d$:

$$\varphi = \frac{ad-bc}{\sqrt{(a+b)(c+d)(a+c)(b+d)}}, \qquad \varphi^2 = \chi^2/n$$

Smokers with disease $a=30$, without $b=20$, non-smokers with disease $c=10$, without $d=40$ give $\varphi=0.41$. Its maximum falls below 1 when the margins are unequal, so compare it across tables with care.

| Variable types | Use |
| :-- | :-- |
| Continuous, continuous, linear | Pearson |
| Continuous or ordinal, monotonic | Spearman |
| Ordinal, small n, many ties | Kendall |
| Continuous, binary | Point-biserial |
| Binary, binary | Phi |

## Normality
Normality only matters for **inference** (p-values, intervals), never for computing a coefficient, and it is a reason to choose a *test*, not a different coefficient.

| Coefficient | Inference assumes | If violated |
| :-- | :-- | :-- |
| Pearson | Approximately **bivariate normal** (the joint distribution, not each variable alone). The CLT helps at moderate n; outliers and heavy tails hurt most. | Bootstrap CI or permutation test |
| Spearman | Distribution-free under independence (exact or permutation tables) | Usually none needed |
| Kendall | Distribution-free under independence; exact test is reliable at small n | Usually none needed |
| Point-biserial | Equals the pooled t-test: continuous variable roughly normal **within each group**, equal variances | Welch, Mann-Whitney U, permutation test |
| Phi | No normality; chi-square needs expected counts of about 5 or more per cell | Fisher's exact test |

Independence of observations is the assumption that matters most across all five and fails most often (repeated measures, time series, clustered data). For paired binary data use McNemar's test. Ties need the corrections noted above (average ranks, $\tau_b$); SciPy applies them.

## Application: Early Warning in Industrial Systems
Sensors that normally move together form a stable correlation pattern during healthy operation. A change in that pattern can be the warning, often before any single sensor crosses an alarm threshold, supporting predictive maintenance and less unplanned downtime.

| Setting | Signals | Early warning |
| :-- | :-- | :-- |
| Pumps, motors, fans | Vibration vs. current vs. bearing temperature | Vibration rises at constant load, suggesting bearing wear |
| Cooling systems | Coolant flow vs. outlet temperature | Normally strongly negative; weakening suggests fouling or pump failure |
| Process plants | Feed rate vs. reactor temperature vs. quality | A tight relationship loosens: catalyst aging or sensor drift |
| Manufacturing | Cutting force vs. surface roughness | Tool wear before parts fail inspection |
| Power utilities | Transformer load vs. oil temperature | Temperature rises faster than load explains |
| Redundant sensors | Two sensors measuring the same quantity | Correlation near 1 degrades, flagging sensor drift |

See [[Correlation Drift Monitoring with Spark]] for a runnable batch and streaming example.

**Method:** learn a baseline correlation matrix on healthy data, recompute over a rolling window, alert when correlations leave their normal band, and use lagged cross-correlation for lead time. **Caveats:** a change is a symptom, not a diagnosis; start-up and load regimes legitimately alter correlations; Pearson misses nonlinear patterns (use Spearman or mutual information); trending variables correlate spuriously unless detrended; short windows are fast but noisy, long ones stable but slow.
