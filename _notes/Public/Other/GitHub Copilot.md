---
title: GitHub Copilot
---
> [GitHub Copilot in VSCode cheat sheet](https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features)
# Agent Instructions
There are 3 types of instructions:
- The global instruction markdown: **.github/copilot-instructions.md file -** apply instructions automatically to all chat requests.
- Specific instruction sets that you can use for different programming languages, frameworks, or project types: **.github/instructions/*instruction-name*.instructions.md**. These instructions have a [front-matter](https://code.visualstudio.com/docs/copilot/customization/custom-instructions#_instructions-file-format) to indicate where the instructions should apply to.
- If you work with multiple AI agents in your workspace, you can define custom instructions for all agents in an `AGENTS.md`. This feature is experimental as of 01/09/2026.
# Agent Skills (Experimental)
There is also a feature called [agent skills](https://code.visualstudio.com/docs/copilot/customization/overview#_agent-skills-preview) that enables you to teach agents specialized capabilities through folders containing instructions, scripts, and resources. It is similar to instructions, however, there are some important differences:

| Feature         | Agent Skills                                                  | Custom Instructions                       |
| --------------- | ------------------------------------------------------------- | ----------------------------------------- |
| **Purpose**     | Teach specialized capabilities and workflows                  | Define coding standards and guidelines    |
| **Portability** | Works across VS Code, Copilot CLI, and Copilot coding agent   | VS Code and GitHub.com only               |
| **Content**     | ==Instructions, scripts, examples, and resources==            | ==Instructions only==                     |
| **Scope**       | ==Task-specific, loaded on-demand==                           | ==Always applied (or via glob patterns)== |
| **Standard**    | ==Open standard ([agentskills.io](https://agentskills.io/))== | ==VS Code-specific==                      |

The skills subdirectory could include files like:
- `SKILL.md` - Instructions for running tests
- `test-template.js` - A template test file
- `examples/` - Example test scenario

> Skills are not agent specific. Copilot automatically indexes skills based on the front-matter (name and description are required). **Skills are automatically activated based on your prompt when the request matches a skill's description.**

# Prompt Files
[Promt Files](https://code.visualstudio.com/docs/copilot/customization/overview#_prompt-files) let you define **reusable** prompts for common and repeatable development tasks in a Markdown file. You can also include a front-matter for additional information.

> Remember: In prompt files, you can reference [variables](https://code.visualstudio.com/docs/copilot/customization/prompt-files#_body) and tools!

# Agents
**Types of Agents:**
- **Local Agents** (works directly in VSCode) - your good old standard VSCode agent
- **Background Agents** (also works in VSCode, but creates a separate work tree to avoid conflicts and works in the background). Background agents:
	- run via the CLI and can't directly access VS Code built-in tools
	- don't have access to MCP servers or extension-provided tools
	- are limited to the models available via the CLI tool
	- can run terminal commands and might prompt you for approvals if needed
- **Cloud Agents** (isolated from local workspace, runs on cloud infrastructure). Cloud agents:
	- are limited to the MCP servers and language models that are configured in the cloud agent service
	- can do large-scale refactoring across your GitHub repository
	- can complete feature implementation from high-level requirements
	- can automatically pull request generation with detailed descriptions
	- can code review integration and feedback addressing

To be honest, it feels like most of the time I would use the local agent. I can't think of specific use case where you don't have to supervise the changes and work with the local agent (maybe with custom agents and task delegation it could make sense?).
# Custom Agents
You can define custom agents for specific purposes such as planning, implementation or testing. Agents can be bundled up in a pipeline using [handoffs](https://code.visualstudio.com/docs/copilot/customization/custom-agents#_handoffs). 

> [From the documentation:](https://code.visualstudio.com/docs/copilot/customization/custom-agents): You can also use handoffs to create guided workflows between agents, allowing you to transition from one specialized agent to another.

# MCP and Tools
[MCP and Tools](https://code.visualstudio.com/docs/copilot/customization/overview#_mcp-and-tools) let you connect external services and specialized tools through Model Context Protocol (MCP).
# Manage Context in Chat
* \#-mentions (initializes tools or context items)
* /-commands (shortcut specific functionality)
* @-mentions (initializes chat participants)
* Codebase search (use `#codebase`)
* [Copilot - All Supported Context Items](https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features)
# [Workspace Indexing](https://code.visualstudio.com/docs/copilot/reference/workspace-context)
- Two types of indexing: [Local Index](https://code.visualstudio.com/docs/copilot/reference/workspace-context#_local-index) and [Remote Index](https://code.visualstudio.com/docs/copilot/reference/workspace-context#_remote-index)
- If the project has less than 750 indexable files: VS Code automatically builds an advanced local index.
- If the project has between 750 and 2500 indexable files: run the **Build local workspace index** command in the Command Palette (Ctrl+Shift+P) - this should only be run once.
- If the project has more than 2500 indexable files: use a [basic index](https://code.visualstudio.com/docs/copilot/reference/workspace-context#_basic-index).

> VS Code automatically builds and uses remote code search indexes for any GitHub-backed repositories in your workspace.

> Repositories are automatically indexed the first time `@workspace` or `#codebase` is used in chat. You can also force indexing by running the **Build Remote Workspace Index** command in the Command Palette (Ctrl+Shift+P).

> VSCode recommends to use `#codebase` in your chat prompts as it provides more flexibility. [What is the difference between @workspace and #codebase?](https://code.visualstudio.com/docs/copilot/reference/workspace-context#_what-is-the-difference-between-atworkspace-and-hashcodebase)

To summarize, **while you don't have to configure anything about indexing initially**, it is a nice feature to keep in mind especially if your project grows larger in size. Keep in mind, if you find that chat is struggling to provide relevant answers to questions about your codebase, you might want to upgrade to a [remote index](https://code.visualstudio.com/docs/copilot/reference/workspace-context#_remote-index).
# Using MCP servers in VS Code
VSCode also supports use of [MCP servers](https://code.visualstudio.com/docs/copilot/customization/mcp-servers).

