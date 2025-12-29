---
title: matplotlib
---
```python
# Different ways to define a figure
fig = plt.figure()             # an empty figure with no Axes
fig, ax = plt.subplots()       # a figure with a single Axes

# Definin a grid of Axes
fig, axs = plt.subplots(2, 2)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5, 2.7)) 
fig, axes = plt.subplots(2, 2, figsize=(5, 2.7))
```

