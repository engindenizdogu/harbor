---
title: Quartz 4 Commands
tags: [quartz, publishing, static-site]
draft: false
---

Quartz is used to build and publish this site (Quartz 4). This note collects the most-used local commands, config file locations, and quick examples.

## Common Commands

- Development server (live reload):

```
npx quartz build --serve
```

## Key Files

- `quartz.config.ts` — site configuration (routes, plugins, output dir).
- `quartz.layout.ts` — layout and component registration used at build time.
- `content/` — markdown notes and pages (source content).
- `public/` — generated site output after `npx quartz build`.

## Publishing Notes

- **Direct publish / sync:** `npx quartz sync` — Builds the site and (when configured) directly publishes the generated `public/` output to GitHub by pushing to the configured repository/branch (useful for quick deploys or local pushes to GitHub Pages). Ensure your `quartz.config.ts` and repo remotes are configured for sync before running.

## References

- See project `quartz.config.ts` and `quartz.layout.ts` for site-specific settings.
- For full Quartz documentation, consult the official Quartz docs and your project's docs in `docs/`.
