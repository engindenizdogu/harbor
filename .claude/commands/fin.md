---
description: Flush takeaways from all sessions, report in one line, and sign off
---

Flush the queues of all sessions, report in one line, and sign off. No further suggestions or questions.

1. Queue any settled takeaways from this conversation not yet queued (see "Automatic Library Updates" in CLAUDE.md).
2. Run `python3 .scripts/vault_health.py --drain --all --session-id <this session's id>` (the id is in the SessionStart hook output).
3. Write the notes from the printed entries, merging entries on the same topic across sessions, following steps 3-6 of "Automatic Library Updates" in CLAUDE.md.
4. Run `python3 .scripts/vault_health.py --drain-done`.
