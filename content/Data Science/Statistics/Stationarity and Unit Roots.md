---
title: Stationarity and Unit Roots
tags: [data-science, statistics, time-series, stationarity, auto-captured]
draft: false
---
A **stationary** series has statistical properties that do not change over time; a **non-stationary** one does not. Models such as AR, ARMA, and VAR ([[Autoregressive Models]], [[ARMA and ARIMA Models]], [[Vector Autoregression]]) learn stable relationships from the past, which only makes sense if the process behaves the same way in the future.

## Definitions
**Weak (covariance) stationarity**, the version used in practice, requires:
1. **Constant mean:** $E[X_t]=\mu$
2. **Constant variance:** $\operatorname{Var}(X_t)=\sigma^2$
3. **Autocovariance depends only on the lag:** $\operatorname{Cov}(X_t,X_{t+h})=\gamma(h)$

**Strict stationarity** says the whole joint distribution is unchanged by a time shift. It is stronger and rarely testable; the two coincide for Gaussian processes.

| Series | Stationary? | Why |
| :-- | :-- | :-- |
| White noise | Yes | Constant mean and variance, no autocorrelation |
| AR(1) with $\lvert\phi\rvert<1$ | Yes | Shocks fade, reverts to the mean |
| Stock price level | No | Wanders like a random walk |
| Monthly retail sales | No | Trend and seasonality |
| Daily returns (price changes) | Roughly | Differencing removes the wander |
| Sensor with a drifting baseline | No | The mean changes over time |

## Types of Non-Stationarity

| Type | What changes | Typical fix |
| :-- | :-- | :-- |
| **Deterministic trend** (trend-stationary) | Mean follows a fixed line; deviations around it are stationary | Detrend, or include a time term |
| **Stochastic trend / unit root** (difference-stationary) | Shocks accumulate permanently (random walk, $\phi=1$) | **Difference** the series |
| **Seasonality** | Mean repeats in a cycle | Seasonal differencing $X_t-X_{t-m}$, seasonal dummies, or SARIMA |
| **Changing variance** | Spread grows or shrinks | Log or Box-Cox transform; ARCH/GARCH for volatility |
| **Structural break** | Mean, variance, or dynamics shift at some date | Model regimes separately, or regime-switching models |

The first two differ importantly: detrending a unit-root series leaves residual non-stationarity, and differencing a trend-stationary series over-differences it. This is why both ADF and KPSS are used.

## Why It Matters
- **Forecasts:** a stationary model reverts to a mean; a non-stationary one has no stable mean, and its forecast uncertainty grows without bound.
- **Inference:** standard t-tests, confidence intervals, and $R^2$ are unreliable on non-stationary data.
- **Spurious regression:** two unrelated trending series can show a high correlation and impressive $R^2$ purely because both trend, so correlation analysis ([[Correlation Coefficients]]) on raw trending data can mislead.
- **Cointegration:** the exception. Non-stationary series can share a stable long-run relationship, handled by a vector error-correction model (see [[Vector Autoregression]]).

## Detecting It

| Method | What to look for |
| :-- | :-- |
| Plot | Trend, changing spread, cycles, level shifts |
| ACF | Stationary: decays quickly. Non-stationary: stays high for many lags |
| Rolling mean and variance | They drift over time |
| **ADF** (Augmented Dickey-Fuller) | Null: unit root. Small p-value suggests stationary |
| **KPSS** | Null: stationary. Small p-value suggests non-stationary |
| Phillips-Perron | Alternative unit-root test, robust to some serial correlation |

Read ADF and KPSS together (the four-way table is in [[Autoregressive Models]]) and always plot. Both tests have low power on short series.

## Fixing It
1. **Transform** for variance: log or Box-Cox.
2. **Difference** for a stochastic trend, $\Delta X_t=X_t-X_{t-1}$ (the "I" in ARIMA), with the smallest order that works.
3. **Seasonally difference** for cycles.
4. **Detrend** for a deterministic trend.
5. **Re-test** after each step, and undo the transformations on the forecasts to return to the original scale.

| | Stationary | Non-stationary |
| :-- | :-- | :-- |
| Mean | Constant | Changes |
| Variance | Constant | May change |
| ACF | Decays fast | Decays slowly |
| Shocks | Fade out | Persist or accumulate |
| Long-horizon forecast | Reverts to the mean | Drifts or wanders |
| Models | AR, ARMA, VAR directly | Difference or transform first (ARIMA, VECM) |
