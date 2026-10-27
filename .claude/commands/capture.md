---
description: Flush this session's queued takeaways into the vault now
---

Flush this session's queue now, then continue the conversation.

1. Queue any settled takeaways not yet queued (see "Automatic Library Updates" in CLAUDE.md).
2. Run `python3 .scripts/vault_health.py --drain --session-id <this session's id>` (the id is in the SessionStart hook output).
3. Write the notes from the printed entries, following steps 3-6 of "Automatic Library Updates" in CLAUDE.md.
4. Run `python3 .scripts/vault_health.py --drain-done`.
