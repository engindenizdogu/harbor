---
description: Toggle vault recording on or off
---

Run `python3 .scripts/vault_health.py --toggle-record`, which flips the state in `.scripts/state.json` and prints the new one. Reply with only that one line ("Recording off" / "Recording on"). Never flip based on what the conversation suggests; the script reads the file.

- **Off:** follow the "Recording" rules in CLAUDE.md from now on.
- **Back on:** resume batch capture from this point. Nothing said while recording was off is captured retroactively unless Deniz asks for it explicitly.
