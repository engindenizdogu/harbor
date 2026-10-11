---
title: Correlation Coefficients
tags: [data-science, statistics, correlation, auto-captured]
draft: false
---
A **correlation coefficient** summarizes how strongly two variables move together on a scale from -1 (perfectly opposite) to +1 (perfectly together). Pearson, Spearman, and Kendall differ in the *kind* of togetherness they detect. For how to test and put intervals on them, see [[Statistical Inference Basics]].

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

## Normality
Computing any of the three coefficients assumes no distribution. Normality enters only for Pearson **inference** (the t-test and Fisher z interval assume approximate bivariate normality). Spearman and Kendall tests are distribution-free under independence, though they still assume independent observations. A bootstrap or permutation test lets you keep Pearson without the normality assumption.
