---
description: Commit all current changes and push the current branch
---

Commit all current changes, then push the current branch.

- Check `git status` first and flag anything that looks like a secret or stray artifact instead of staging it. Stage the rest with `git add -A`.
- Write a short imperative message, split by area if both vault notes and site code changed (e.g. "Add Context Graphs note; restyle home frame").
- Never amend, force-push, skip hooks, or switch branches.
- Report the commit and push result in one line.
