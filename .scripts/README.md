# Harbor Reference: Ingestion and Quartz

Read this file only when running an ingestion or touching the Quartz site. It is not needed for normal note work.

## How `ingest.py` behaves
- Resolves paths relative to the repo, so it runs from anywhere: `python3 .scripts/ingest.py`.
- Each top-level folder in `.raw_sources/` becomes a domain folder in `content/`. Notes get `title`, `tags`, `draft: false` front matter (any existing front matter and a duplicate H1 are dropped).
- Creates or updates the domain MOC, and adds a row to the table in `content/toc.md` for new domains. The row's summary is a `TODO` placeholder: replace it with a real one.
- Never overwrites existing notes and leaves non-markdown files and loose files in place, printing `SKIPPED` for each. Place these manually, then clear `.raw_sources/`.
- Edit the script's mapping logic (tags, destination, MOC layout) for each batch before running.

## How `vault_health.py` behaves
- `python3 .scripts/vault_health.py` prints a full lint report: front matter keys, H1 duplicating the title, orphan notes, notes missing from their folder MOC, near-duplicate titles. Skips `_Private`, `Templates`, `Assets`.
- `--session` is what the SessionStart hook in `.claude/settings.json` runs: it reports files in `.raw_sources/`, notes in `content/_Private/Inbox/`, and a short lint summary at most once every 30 days (stamp: `.quartz-cache/vault_health_stamp`; delete it to force a run).

## Repo Commands
- Site config, plugins and layout all live in `quartz.config.yaml` (defaults in `quartz.config.default.yaml`). Custom CSS is `quartz/styles/custom.scss`.
- `npx quartz build --serve` previews the site locally; CI installs with `npm ci` then builds.
- `npm run check` runs `tsc --noEmit` and Prettier checks; `npm run format` formats.
- Commits are normally automated "Quartz sync" snapshots from Obsidian. Manual commits and pushes happen only on the `ship` command (see CLAUDE.md).
