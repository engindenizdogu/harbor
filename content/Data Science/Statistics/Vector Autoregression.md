---
title: Vector Autoregression
tags: [data-science, statistics, time-series, var, forecasting, auto-captured]
draft: false
---
A **VAR (vector autoregression)** is the multivariate version of AR: several series are modeled jointly, and each depends on the past of **all** of them, not only its own. It builds on [[Autoregressive Models]] and needs the stationarity checks from [[Stationarity and Unit Roots]].

## The Model
For $k$ series $\mathbf{y}_t=(y_{1t},\dots,y_{kt})^\top$:

$$\mathbf{y}_t=\mathbf{c}+A_1\mathbf{y}_{t-1}+\dots+A_p\mathbf{y}_{t-p}+\boldsymbol\varepsilon_t$$

Each $A_i$ is a $k\times k$ matrix. For temperature $T$ and power $P$ with $p=1$:

$$\begin{aligned} T_t &= c_1 + a_{11}T_{t-1} + a_{12}P_{t-1} + \varepsilon_{1t} \\ P_t &= c_2 + a_{21}T_{t-1} + a_{22}P_{t-1} + \varepsilon_{2t} \end{aligned}$$

The off-diagonal coefficients capture how one series feeds into the other.

| | AR / ARIMA | VAR |
| :-- | :-- | :-- |
| Series | One | Several, modeled jointly |
| Predictors | Own past | Own past and the other series' past |
| Output | One forecast | A forecast for every series |
| Inputs | Chosen by you (ARIMAX adds given exogenous inputs) | Every variable is endogenous |

## Workflow
1. **Stationarity:** make each series stationary (ADF/KPSS per series, difference as needed).
2. **Lag order $p$:** compare VAR($p$) by AIC, BIC, or HQC; one $p$ applies to all equations.
3. **Estimate:** OLS equation by equation (efficient, since every equation has the same regressors).
4. **Check:** residuals free of autocorrelation, and a stable system (companion-matrix roots inside the unit circle).
5. **Use:** forecast, plus the tools below.

| Tool | Question it answers |
| :-- | :-- |
| **Granger causality test** | Do past values of $x$ help predict $y$ beyond $y$'s own past? (Predictive, not true causation) |
| **Impulse response function** | How do all series respond over time to a one-time shock in one series? |
| **Forecast error variance decomposition** | What share of each series' forecast uncertainty comes from shocks to each series? |

## Limits and Extensions
- **Parameter explosion:** coefficients grow as $k^2p$ (5 series and 4 lags gives 100 plus constants). It needs plenty of data, or regularization (Bayesian VAR, LASSO-VAR) or dimension reduction.
- **Cointegration:** non-stationary series with a stable long-run relationship should not simply be differenced; use a **VECM** (vector error-correction model), which models short-run dynamics and the pull back toward equilibrium.
- **Linearity:** like AR, linear; nonlinear and neural multivariate models relax this.
- **Identification:** impulse responses depend on assumptions about how shocks relate.

| Extension | Adds |
| :-- | :-- |
| VARMA | MA terms (rare, hard to estimate) |
| VARX | Exogenous inputs |
| VECM | Cointegration |
| Bayesian VAR | Shrinkage priors, helpful with large $k$ |
| Structural VAR | Explicit assumptions to interpret shocks |

```python
from statsmodels.tsa.api import VAR

model = VAR(df_stationary)                 # one column per series
order = model.select_order(maxlags=8)      # AIC, BIC, HQIC, FPE
res = model.fit(order.aic)
res.forecast(df_stationary.values[-res.k_ar:], steps=10)
res.test_causality("power", ["temp"], kind="f")   # Granger test
res.irf(10).plot()                                # impulse responses
```
*Not executed.*

**When to use:** several series influence each other and you want joint forecasts or to study how shocks propagate (temperature and power in a machine, interest rates and inflation). Use plain AR/ARIMA when one series suffices, and ARIMAX when external drivers need no forecasting.
