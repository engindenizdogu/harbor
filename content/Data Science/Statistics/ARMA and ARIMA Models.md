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

## Notation Details
- **$B$ is notation, not a computed value.** It means "shift back one step": $BX_t=X_{t-1}$ and $B^kX_t=X_{t-k}$. An AR(2), $X_t=\phi_1X_{t-1}+\phi_2X_{t-2}+\varepsilon_t$, becomes $(1-\phi_1B-\phi_2B^2)X_t=\varepsilon_t$. Software never computes $B$; it applies the shifts from the orders you give. It also appears in the stationarity condition: roots of $\phi(B)=0$, treating $B$ as an ordinary variable, must lie outside the unit circle.
- **$d$ counts repetitions, not distance.** $(1-B)^dX_t$ applies the first difference $d$ times, and each pass shortens the series by one point. For $d=3$: $(1-B)^3X_t=X_t-3X_{t-1}+3X_{t-2}-X_{t-3}$. Example with the cubes `1, 8, 27, 64, 125`: $d=1$ gives `7, 19, 37, 61`, $d=2$ gives `12, 18, 24`, and $d=3$ gives `6, 6`.
- **A single difference at lag $m$** is $(1-B^m)X_t=X_t-X_{t-m}$. That is seasonal differencing (the $D$ in SARIMA), not $d$. A value of $d=3$ is rare and usually signals over-differencing.
- **What ARIMA does not cover:** it handles trends (stochastic trends or unit roots) through differencing, not long-memory dependence, which needs fractional models such as ARFIMA. Plain ARIMA also ignores seasonality (use SARIMA). Financial price levels are non-stationary while returns are roughly stationary, so ARMA suits returns, not price levels.

## Example: ARIMA on Real Data (US Real GDP)
*Run with `statsmodels` 0.15 on the quarterly US macroeconomic dataset bundled with the library (203 quarters, 1959Q1 to 2009Q3).* The series is log real GDP, which has a clear upward trend, so it needs $d=1$.

```python
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA

gdp = sm.datasets.macrodata.load_pandas().data["realgdp"]   # US real GDP, quarterly
y = np.log(gdp)                                             # log stabilizes growth

print("ADF p-value, level:      ", round(adfuller(y)[1], 3))
print("ADF p-value, differenced:", round(adfuller(y.diff().dropna())[1], 3))

fit = ARIMA(y[:-8], order=(2, 1, 0), trend="t").fit()       # d=1, with drift
print(fit.summary().tables[1])
print(np.exp(fit.forecast(4)).round(0))                     # back to GDP scale
```

Output:

```
ADF p-value, level:       0.383
ADF p-value, differenced: 0.0
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
x1             0.0082      0.001      8.645      0.000       0.006       0.010
ar.L1          0.2253      0.066      3.426      0.001       0.096       0.354
ar.L2          0.1493      0.062      2.416      0.016       0.028       0.270
sigma2      6.632e-05    5.1e-06     13.007      0.000    5.63e-05    7.63e-05
195    13433.0
196    13545.0
197    13658.0
198    13771.0
```

![[arima-us-real-gdp-forecast.png]]
*Left: real GDP in billions of dollars, with the ARIMA(2,1,0) forecast and 95% interval for the last 8 quarters; the actuals fall below the forecast during the 2008 recession. Right: the first difference of log GDP, which fluctuates around a constant mean.*

**Reading it:**
- The level is non-stationary (ADF $p=0.383$) and the first difference is stationary (ADF $p\approx0$), so $d=1$.
- `x1` is the **drift**: about 0.0082 per quarter in log terms, roughly 0.8 percent growth per quarter (about 3.3 percent a year). With $d=1$, `trend="t"` adds this drift to the differenced series.
- The AR coefficients (0.23 and 0.15) are significant and sum to well below 1: growth in one quarter carries over modestly into the next.
- The model was fit on all but the last 8 quarters; the forecast is exponentiated back to GDP in billions of dollars.

**Order selection (grid over $p,q\in\{0,1,2\}$, $d=1$, training data only):**

| Order | AIC | BIC |
| :-- | :-- | :-- |
| **(2,1,0)** | **-1307.8** | -1294.7 |
| (0,1,2) | -1306.8 | -1293.7 |
| (1,1,1) | -1306.3 | -1293.2 |
| (2,1,1) | -1306.0 | -1289.6 |

AIC picks (2,1,0) and BIC picks the smaller (1,1,0), the usual pattern of BIC favoring simplicity. Differences between the top candidates are about 1 AIC point, a near tie. Ljung-Box on the residuals gives $p=0.841$ at lag 8: no leftover autocorrelation.

**Honest check on held-out data.** Over the last 8 quarters the model's RMSE (about 793 billion dollars) is no better than a plain random walk with drift (about 787 billion). The held-out window covers the 2008 recession, which a linear model of past growth cannot anticipate: the forecast keeps rising while actual GDP fell. A model passing residual checks and getting good AIC does not guarantee good forecasts across a regime change.

## Example: Seasonal ARIMA on Monthly CO2
*Run with `statsmodels` 0.15 on the monthly atmospheric CO2 series bundled with the library (526 months, 1958 to 2001, in ppm).* The series has an upward trend and a yearly cycle, so plain ARIMA is not enough: a seasonal ARIMA (SARIMA) adds seasonal terms with period 12.

```python
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX

co2 = sm.datasets.co2.load_pandas().data["co2"].resample("MS").mean().ffill()  # monthly CO2 (ppm)
print("ADF p-value, level:", round(adfuller(co2)[1], 3))
print("ADF p-value, after d=1 and D=1:", round(adfuller(co2.diff().diff(12).dropna())[1], 3))

train, test = co2[:-24], co2[-24:]
fit = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)).fit(disp=False)
print(fit.summary().tables[1])

fc = fit.get_forecast(24)
rmse = lambda f: np.sqrt(np.mean((np.asarray(f) - test.values) ** 2))
print("RMSE  SARIMA:          ", round(rmse(fc.predicted_mean), 2))
print("RMSE  seasonal naive:  ", round(rmse(np.tile(train[-12:], 2)), 2))
print("RMSE  last value:      ", round(rmse([train.iloc[-1]] * 24), 2))
```

Output:

```
ADF p-value, level: 0.999
ADF p-value, after d=1 and D=1: 0.0
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
ar.L1          0.3018      0.105      2.868      0.004       0.096       0.508
ma.L1         -0.6341      0.090     -7.058      0.000      -0.810      -0.458
ar.S.L12       0.0116      0.052      0.222      0.825      -0.091       0.114
ma.S.L12      -0.8526      0.035    -24.296      0.000      -0.921      -0.784
sigma2         0.1051      0.006     18.820      0.000       0.094       0.116
RMSE  SARIMA:           0.42
RMSE  seasonal naive:   2.07
RMSE  last value:       2.93
```

![[sarima-monthly-co2-forecast.png]]
*Left: the full monthly series with trend and yearly cycle. Right: the last 24 months held out, with the SARIMA forecast and 95% interval.*

**Reading it:**
- The level is non-stationary (ADF $p=0.999$); one regular difference ($d=1$) plus one seasonal difference ($D=1$, lag 12) makes it stationary.
- `ma.S.L12` is strongly significant, while the seasonal AR term `ar.S.L12` is not ($p=0.825$), so a simpler $(1,1,1)(0,1,1)_{12}$ would do about as well.
- On 24 held-out months the model's RMSE is about 0.42 ppm, versus 2.07 for repeating last year's values and 2.93 for repeating the last value, so it clearly beats both baselines. The forecast follows both the trend and the seasonal cycle, and the actuals stay inside the 95% interval (the second peak is slightly overshot).
- Contrast with the GDP example: CO2 follows a stable trend and seasonal pattern, so a model fit on the past extrapolates well, while GDP contained a recession the past could not predict.

**Also tried:** the bundled sunspot series, which is roughly stationary and fits an ARMA(3,0,1); on 20 held-out years it had an RMSE of about 29 versus 53 for predicting the training mean. Annual CO2 means needed $d=2$ (accelerating growth), which is unusual and makes a poor first example.
