---
title: ARMA and ARIMA Models
tags: [data-science, statistics, time-series, arima, forecasting, auto-captured]
draft: false
---
ARMA combines autoregressive and moving-average terms for stationary data; ARIMA adds differencing so it can handle trends. This note goes deeper than the overview in [[Autoregressive Models]] and relies on [[Stationarity and Unit Roots]].

## ARMA($p,q$)
$$X_t = c + \sum_{i=1}^{p}\phi_i X_{t-i} + \varepsilon_t + \sum_{j=1}^{q}\theta_j \varepsilon_{t-j}$$

With the **lag operator** $B$ ($BX_t=X_{t-1}$): $\phi(B)X_t=c+\theta(B)\varepsilon_t$, where $\phi(B)=1-\phi_1B-\dots-\phi_pB^p$ and $\theta(B)=1+\theta_1B+\dots+\theta_qB^q$.

**Why mix them:** a pure AR or MA model may need many terms for a process a mixed model captures with two. An ARMA(1,1) can replace an AR(5) or MA(5); the gain is parsimony.

| Condition | Applies to | Requirement |
| :-- | :-- | :-- |
| **Stationarity** | AR part | Roots of $\phi(B)=0$ outside the unit circle |
| **Invertibility** | MA part | Roots of $\theta(B)=0$ outside the unit circle |

Invertibility makes the shocks recoverable from the data and the representation unique; without it, different $\theta$ give the same autocorrelations. Software enforces it by default.

**Identification:** both ACF and PACF decay, with neither cutting off cleanly. Start small, for example (1,1), and compare neighbors by AIC/BIC. **Redundancy trap:** if the AR and MA polynomials share a common root they cancel and extra terms add nothing; symptoms are unstable estimates and large standard errors.

## ARIMA($p,d,q$)
$$\phi(B)(1-B)^d X_t = c + \theta(B)\varepsilon_t$$

Fit an ARMA($p,q$) to the $d$-times differenced series, then **integrate** (cumulatively sum) the forecasts back to the original scale. Example: `10, 12, 15, 19, 24` has first difference `2, 3, 4, 5` (still trending) and second difference `1, 1, 1` (stationary), so $d=2$.

| Model | Equivalent to |
| :-- | :-- |
| ARIMA(0,1,0) | Random walk $X_t=X_{t-1}+\varepsilon_t$ |
| ARIMA(0,1,0) with a constant | Random walk with drift |
| ARIMA(0,1,1) | Simple exponential smoothing |
| ARIMA(1,0,0) | AR(1) |
| ARIMA(0,2,2) | Related to Holt's linear trend |

**The constant with differencing:** $d=0$ sets the series mean; $d=1$ adds a linear drift to forecasts; $d=2$ would imply a quadratic trend and is normally omitted.

**Forecast behavior:** $d=0$ reverts to the mean; $d=1$ follows the last level or a drift line; $d=2$ continues the recent slope. Prediction intervals widen faster with larger $d$.

| Practical point | Detail |
| :-- | :-- |
| Over-differencing | Can add artificial negative autocorrelation and inflate variance; use the smallest $d$ that works. These warning signs did not always appear in a simulation (see below), so rely on the tests |
| Comparability | AIC/BIC across different $d$ are not comparable (different series); fix $d$ first, then compare $p,q$ |
| Seasonality | Plain ARIMA ignores it; SARIMA adds $(P,D,Q)_m$ with seasonal differencing $(1-B^m)^D$ |
| Variance growing with level | Take logs first |
| Check | Ljung-Box and the residual ACF should show white noise |

## Worked Example: Identifying an ARIMA Order
*Simulated data, run with `statsmodels` 0.15 in a throwaway environment.* 300 points from a true ARIMA(1,1,1) with $\phi=0.6$, $\theta=0.4$, $\sigma^2=1$ (fixed seed).

**Step 1, find $d$.**

| Series | ADF p | KPSS p | Note |
| :-- | :-- | :-- | :-- |
| Level ($d=0$) | 0.861 | 0.010 | Non-stationary; ACF decays very slowly |
| First difference ($d=1$) | 0.000 | 0.100 | Stationary, so $d=1$ |

The second difference also passed both tests, with variance falling from 2.24 to 1.21 and lag-1 ACF of $0.10$ (not negative), so the usual over-differencing signs did **not** appear. Take the smallest $d$ that passes the tests.

**Step 2, read ACF/PACF of the differenced series** (band about $\pm0.11$):

| Lag | 1 | 2 | 3 | 4 | 5 | 6 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| ACF | 0.72 | 0.40 | 0.23 | 0.09 | 0.00 | 0.00 |
| PACF | 0.73 | -0.27 | 0.13 | -0.14 | 0.01 | 0.09 |

The ACF tails off and the PACF alternates in sign and tails off, with no clean cutoff: a mixed ARMA, so start at ARIMA(1,1,1).

**Step 3, search $p,q\in\{0..3\}$ with $d=1$:**

| Rank | Order | AIC | BIC |
| :-- | :-- | :-- | :-- |
| 1 | **(1,1,1)** | **842.0** | **853.1** |
| 2 | (3,1,3) | 842.9 | 868.8 |
| 3 | (1,1,2) | 843.7 | 858.5 |
| 4 | (3,1,2) | 843.7 | 865.9 |
| 5 | (2,1,1) | 843.8 | 858.6 |

AIC and BIC both pick (1,1,1); larger models are within about 2 AIC points but use more parameters.

**Step 4, check.** Estimates $\hat\phi=0.55$, $\hat\theta=0.44$, $\hat\sigma^2=0.96$ against truths 0.6, 0.4, 1.0; Ljung-Box p-value at lag 10 is 0.689; residual ACF inside the band. The procedure recovered the true model.

```python
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
import itertools

adfuller(x)[1]; kpss(x, regression="c")[1]       # d: test level, then diff
d1 = np.diff(x)
acf(d1, nlags=6); pacf(d1, nlags=6)               # p, q guesses

fits = {(p, 1, q): ARIMA(x, order=(p, 1, q)).fit()
        for p, q in itertools.product(range(4), range(4))}
best = min(fits, key=lambda o: fits[o].aic)       # (1, 1, 1)
acorr_ljungbox(fits[best].resid[1:], lags=[10])   # residual check
```

Takeaways: tests set $d$, ACF/PACF give a starting guess, AIC/BIC choose, residuals confirm. Real data is noisier, so expect less clean plots.
