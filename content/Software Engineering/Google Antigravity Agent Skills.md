---
title: Google Antigravity Agent Skills
tags:
  - ai
  - agents
  - development
  - tools
  - antigravity
draft: false
---
In Google Antigravity, while the underlying language models are powerful generalists, they do not possess specific project context or team-specific standards out of the box. Loading every rule, guideline, or tool into the agent's context window leads to tool bloat, higher token costs, latency, and model confusion.

To solve this, Antigravity uses **progressive disclosure** via **skills**. A skill is a specialized package of instructions and tools that remains dormant until the agent determines that a user's prompt matches the skill's defined description.

---

## Structure and Scope

Skills are organized as directory-based packages. They can be defined at different levels depending on how widely they should be accessible:

| Scope | Directory Path | Description |
| :--- | :--- | :--- |
| **Global Scope** | `~/.gemini/skills/`<br>or `.agents/skills/` | Available across all Antigravity products and projects. |
| **Product Scope** | `~/.gemini/antigravity/skills/`<br>or `~/.gemini/antigravity-cli/skills/` | Restricts the skill's availability to a specific product environment (e.g., Standalone App vs. CLI). |
| **Project / Workspace Scope** | `<project-root>/.agents/skills/` | Available only within the specific code workspace/project. |

---

## Anatomy of a Skill

A typical skill is structured as a directory containing the following components:

```text
my-skill/
├── SKILL.md    # (Required) Metadata and instructions
├── scripts/    # (Optional) Python or Bash scripts for execution
├── references/ # (Optional) Reference texts, documentation, or templates
└── assets/     # (Optional) Associated images, icons, or logos
```

### The SKILL.md File

The core of any skill is its `SKILL.md` file. It contains a YAML front matter block defining the metadata, followed by the actual markdown instructions.

Example structure of a `SKILL.md` file for a code review skill:

```markdown
---
name: code-review
description: Reviews code changes for bugs, style issues, and best practices. Use when reviewing PRs or checking code quality.
---

# Code Review Skill

When reviewing code, follow these steps:

## Review checklist

1. **Correctness**: Does the code do what it's supposed to?
2. **Edge cases**: Are error conditions handled?
3. **Style**: Does it follow project conventions?
4. **Performance**: Are there obvious inefficiencies?

## How to provide feedback

- Be specific about what needs to change
- Explain why, not just what
- Suggest alternatives when possible
```

> [!IMPORTANT]
> The `description` field in the front matter of `SKILL.md` is critical. The agent parses this description to perform semantic matching against the user's prompt to decide when to activate and load the skill.

---

## Skill Activation

To trigger a skill, the user simply has to write a prompt that semantically maps to the skill's description. 

For instance, with the `code-review` skill active, a prompt like:
> "review the @demo_bad_code.py file"

will cause the agent to identify the `code-review` skill, load its instructions, and apply the checklist criteria when outputting its response.

---
*Source: [Getting Started with Google Antigravity Codelab](https://codelabs.developers.google.com/getting-started-google-antigravity#8)*

## Related Notes
- [[Software Engineering MOC]]
- [[Model Context Protocol Architecture]]
- [[GitHub Copilot]] - Outlines GitHub Copilot's experimental support for the `agentskills.io` standard.
