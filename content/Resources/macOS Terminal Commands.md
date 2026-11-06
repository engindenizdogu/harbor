---
title: macOS Terminal Commands
tags: [resources, macos, terminal]
draft: false
---
Handy macOS terminal commands worth remembering.

## Power Management

### Disable sleep entirely

```bash
sudo pmset -a disablesleep 1
```

Stops the Mac from sleeping on any power source (`-a` applies to battery, charger, and UPS), including when the lid is closed. This is useful for long-running jobs such as training runs, downloads, or a server on a laptop.

Revert it when done, since a closed laptop that never sleeps runs warm and drains the battery:

```bash
sudo pmset -a disablesleep 0
```

Check the current state with `pmset -g` (look for `SleepDisabled`).

### Lighter alternative: `caffeinate`

```bash
caffeinate -dims
```

Keeps the Mac awake only while the command runs (or while a wrapped command runs, e.g. `caffeinate -i python train.py`). It needs no `sudo` and resets itself on exit, but it does not keep the Mac awake with the lid closed on battery.

## Related

- [[Quartz 4 Commands]] - Local commands for building and previewing this site.
- [[Git Cheat Sheets]] - Quick reference for common Git commands.
