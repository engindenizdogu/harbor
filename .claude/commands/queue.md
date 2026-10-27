---
description: Show what is queued for the vault, per session
---

Run `python3 .scripts/vault_health.py --status --session-id <this session's id>` (the id is in the SessionStart hook output) and show its output as is. Read-only: do not flush, edit, or add anything. If the queue is empty, say so in one line.
