---
title: Loss Curve Plotting Snippets
tags: [deep-learning, visualization, matplotlib, code-snippets, auto-captured]
draft: false
---
Matplotlib code that plots training against validation or test loss and error, plus how to read the shape of the curves. A **learning curve** (over epochs) shows how the [[Loss Functions|loss]] on the training data and on held-out data changes as training goes on. The gap between the two curves is the quickest check for underfitting and overfitting. The snippets take the `history` dict that [[PyTorch Training Template]] returns, and a Keras `History` object. For general figure setup, see [[Matplotlib Snippets]].

## Train vs. Validation Loss

```python
import numpy as np
import matplotlib.pyplot as plt

def plot_loss(history, title="Training vs. validation loss", log_y=False):
    tr, va = np.asarray(history["train_loss"]), np.asarray(history["val_loss"])
    epochs = np.arange(1, len(tr) + 1)
    best = int(va.argmin())

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(epochs, tr, label="Train", lw=2)
    ax.plot(epochs, va, label="Validation", lw=2)
    ax.axvline(epochs[best], ls="--", c="gray", lw=1)
    ax.scatter(epochs[best], va[best], c="red", zorder=3,
               label=f"Best val {va[best]:.4f} @ epoch {epochs[best]}")
    if log_y:
        ax.set_yscale("log")                             # useful when loss spans orders of magnitude
    ax.set(xlabel="Epoch", ylabel="Loss", title=title)
    ax.grid(alpha=0.3); ax.legend()
    fig.tight_layout()
    return fig, ax

plot_loss(history)
plt.show()
```

## Loss and Error Side by Side

Error rate is `1 - accuracy`. Plotting it next to loss shows whether falling loss actually means fewer mistakes: loss can keep improving because the model grows more confident while the error rate stays flat.

```python
def plot_loss_and_error(history, figsize=(11, 4)):
    epochs = np.arange(1, len(history["train_loss"]) + 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    ax1.plot(epochs, history["train_loss"], label="Train")
    ax1.plot(epochs, history["val_loss"],   label="Validation")
    ax1.set(xlabel="Epoch", ylabel="Loss", title="Loss")

    ax2.plot(epochs, 1 - np.asarray(history["train_acc"]), label="Train")
    ax2.plot(epochs, 1 - np.asarray(history["val_acc"]),   label="Validation")
    ax2.set(xlabel="Epoch", ylabel="Error rate (1 - accuracy)", title="Error")
    ax2.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))

    for ax in (ax1, ax2):
        ax.grid(alpha=0.3); ax.legend()
    fig.tight_layout()
    return fig

plot_loss_and_error(history)
plt.show()
```

## Adding the Final Test Score

The test set is evaluated once at the end, so draw it as a horizontal reference line, not a curve. Tracking it every epoch and choosing the epoch from it leaks test information into model selection.

```python
fig, ax = plot_loss(history)
ax.axhline(test_loss, c="black", ls=":", label=f"Test {test_loss:.4f}")
ax.legend()
plt.show()
```

## From a Keras History Object

`model.fit(...)` returns a `History` whose `.history` dict uses `loss` / `val_loss` and `accuracy` / `val_accuracy` keys. Rename them and reuse the functions above.

```python
h = keras_history.history
history = {
    "train_loss": h["loss"],      "val_loss": h["val_loss"],
    "train_acc":  h.get("accuracy", []), "val_acc": h.get("val_accuracy", []),
}
plot_loss(history)
```

## Smoothing Noisy Per-Batch Loss

Per-batch losses jump around. An exponential moving average (the same smoothing TensorBoard uses) shows the trend; keep the raw curve faintly behind it.

```python
def ema(values, alpha=0.9):
    out, s = [], values[0]
    for v in values:
        s = alpha * s + (1 - alpha) * v
        out.append(s)
    return np.asarray(out)

# batch_losses: list of loss.item() appended inside the training loop
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(batch_losses, alpha=0.25, label="Raw")
ax.plot(ema(batch_losses, 0.98), lw=2, label="EMA (0.98)")
ax.set(xlabel="Step", ylabel="Loss", title="Per-batch training loss")
ax.legend(); ax.grid(alpha=0.3)
plt.show()
```

## Comparing Several Runs

Use the same colour per run, with a solid line for validation and a dashed line for train, so the legend stays short.

```python
def plot_runs(runs, figsize=(8, 4.5)):
    """runs: {"lr=1e-3": history1, "lr=1e-4": history2, ...}"""
    fig, ax = plt.subplots(figsize=figsize)
    for (name, h), c in zip(runs.items(), plt.cm.tab10.colors):
        ep = np.arange(1, len(h["val_loss"]) + 1)
        ax.plot(ep, h["val_loss"],   c=c, lw=2, label=f"{name} (val)")
        ax.plot(ep, h["train_loss"], c=c, lw=1, ls="--", alpha=0.6)
    ax.set(xlabel="Epoch", ylabel="Loss", title="Validation loss by run (dashed = train)")
    ax.grid(alpha=0.3); ax.legend()
    fig.tight_layout()
    return fig
```

## Reading the Curves

| Pattern                                      | What it means                                                                                   | What to try                                                                                                     |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Both curves high and flat                    | Underfitting: the model is too simple or the learning rate is too low                           | Bigger model, train longer, raise the learning rate, better features                                            |
| Train keeps falling, validation turns upward | Overfitting: the model memorizes the training set                                               | Early stopping at the validation minimum, [[Regularization]] (dropout, weight decay), more data or augmentation |
| Both fall and level off close together       | Good fit                                                                                        | Stop at the plateau; a small gap is normal                                                                      |
| Validation below train                       | Usually dropout or augmentation is active only during training, or the validation set is easier | Expected with dropout; otherwise check the split                                                                |
| Loss spikes or diverges to `nan`             | Learning rate too high, or exploding gradients                                                  | Lower the learning rate, add gradient clipping, check inputs for `nan`/`inf`                                    |
| Validation curve very jagged                 | Small validation set or a batch size that is too small                                          | Larger validation set, report a smoothed curve                                                                  |

These shapes are the bias-variance trade-off seen over training time: an underfit model has high bias and an overfit one has high variance (see [[Metrics and Model Evaluation]]).

*Source: [Google ML Crash Course: Overfitting and loss curves](https://developers.google.com/machine-learning/crash-course/overfitting/interpreting-loss-curves), [Matplotlib: pyplot.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html)*
