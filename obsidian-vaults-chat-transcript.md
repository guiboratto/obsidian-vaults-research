# Obsidian Vaults Chat Transcript

## User Message
"Best obsidian vaults for business and product development"

## Assistant Response

### Initial Response
"I'll research the best Obsidian vaults and templates for business and product development."

### Research Findings

**1. lukeinglis/work-vault**
- **URL**: https://github.com/lukeinglis/work-vault
- **Description**: An AI-powered work vault built on Obsidian + Claude Code. Structured templates, automated workflows, and MCP integrations for managing meetings, decisions, initiatives, and research.

**Key Features:**
- This vault puts everything in one place. Strategy, research, decisions, meeting notes, and project thinking all live here as plain markdown files, powered by Obsidian for linking and visualization and Claude Code for automation and AI assistance.
- Built by a Product Manager, but designed for anyone who juggles meetings, decisions, and initiatives -- PMs, project managers, engineering leads, TPMs, chiefs of staff, or anyone who needs a system to stay on top of complex work.
- **A structured vault** with folders for components, initiatives, meetings, weekly notes, people, and a triage inbox.
- **Templates** for every note type: meetings, decisions, specs, research, one-pagers, weekly scratch pads, initiative overviews, and more.
- **A shared task system** (`Todo.md`) where you and Claude Code collaborate on tasks with clear ownership and handoff rules.

**How to Use:**
Open the `work-vault` folder as a vault in Obsidian. It will prompt you to trust the plugins -- accept to enable Dataview, Kanban, Templater, and other community plugins.

**Vault Structure:**
```
work-vault/
  Home.md                  -- Dashboard (Dataview-powered)
  Todo.md                  -- Shared task list (you + Claude Code)
  Initiatives Board.md     -- Kanban board of all initiatives
  Commands.md              -- Reference for all slash commands
  Automation.md            -- Reference for all automation
  CLAUDE.md                -- Claude Code context and rules

  01-Components/           -- Product areas (permanent domains)
    example-component/
      _overview.md         -- Component overview and status
      decisions/           -- Decision records
      initiatives/         -- Time-bound projects
      research/            -- Research briefs
      spec-drafts/         -- Draft specs before shipping to Jira

  02-Weekly/               -- Weekly scratch pads
    _summaries/            -- Curated end-of-week summaries

  03-Meetings/             -- Meeting notes by recurring series
    _one-off/              -- Non-recurring meetings
      _transcripts/        -- AI transcripts

  04-Inbox/                -- Quick capture, triage later
    intake/                -- New items awaiting routing

  05-People/               -- Stakeholder reference
  06-Presentations/        -- Slide decks and materials
  07-Usage/                -- Claude Code session logs
  99-Archive/              -- Shipped/killed work

  Templates/               -- Templates for every note type
  scripts/                 -- Automation scripts
  docs/                    -- Setup guides and examples

  .claude/
    commands/              -- Slash command definitions
    rules/                 -- Path-scoped behavior rules
    settings.json          -- Claude Code project settings

  .obsidian/               -- Obsidian config and plugins
  .mcp.json                -- Project-level MCP server config
```

**Obsidian Plugins:**
The vault uses these community plugins (installed automatically when you open in Obsidian):

| Plugin | Purpose |
|--------|---------|
| **Dataview** | Powers the Home dashboard and dynamic queries |
| **Templater** | Template engine for creating notes |
| **Periodic Notes** | Auto-creates weekly notes |
| **QuickAdd** | Quick capture to inbox, todo, or scratch pad (see shortcuts) |
| **Kanban** | Visual initiative board |
| **Excalidraw** | Diagrams and sketches |
| **Terminal** | Run commands from within Obsidian |
| **Charts View** | Data visualization |

**Documentation:**
| Doc | What's in it |
|-----|-------------|
| Philosophy | Why the vault is structured this way -- components vs. initiatives, the inbox pattern, decision logging, and the shared task system |
| Integration Setup | Configure slash command placeholders (email, Slack, GitHub, Jira) |
| MCP Setup | Step-by-step setup for Jira, Slack, Google Workspace, and Browser MCP servers |
| QuickAdd Shortcuts | The three pre-configured Obsidian capture shortcuts and how to customize them |

**MCP Requirements:**
No. The vault works without any MCP servers -- you just won't have the automated calendar/email/Slack/Jira integrations. Add them incrementally as needed.

---

**2. Second Brain: a project vault for you and your AI agent**
- **Description**: A ready-made Obsidian vault that turns your project notes into a second brain your AI agent can read and write.

**Key Points:**
- A ready-made Obsidian structure that turns your notes into a second brain an AI agent can read and write. Download it, open it as a vault, fill it with your project, and your agent will work from your context instead of guessing.
- Models got good. The bottleneck now isn't the model, it's how much context it has about you and your work. Without context, an agent reaches for an average answer off the internet, or invents one. A structured vault in plain text closes that gap: the context lives in files, the agent reads them, nothing gets distorted or lost.
- Founders, indie makers, designers, and product people who run a project and want an agent that actually knows it. This is the **project / product** template. A personal-life version is a separate thing, don't mix the two.

**Vault Structure:**
```
00. Vault Rules & Guide     how the vault works, for you and the agent
01. Inbox/                  quick capture
02. Projects/                active work
03. Archive/                 completed work
04. People/                  stakeholders and references
05. Research/                external reading
06. Systems/                 infrastructure, tools, processes
07. Finance/                 money stuff
08. Health/                  wellness and habits
09. Learning/                courses and certifications
10. Memories/                personal history and experiences
11. Relationships/           people in your life
12. Environment/             home, workspace, gear
13. Travel/                  trips and adventures
14. Favorites/               anything you want quick access to
15. Templates/               note templates
16. Meta/                    templates, attachments, bases
```

Every domain folder ships with an **index note** that doubles as documentation. It tells you (and the agent) what belongs there. Six note templates (Note, Decision, Meeting, Person, Release, Post) live in `16. Meta/Templates/`.

**Requirements:**
- **Obsidian** (free).
- **Templates** (core plugin, built in) for the note templates. Enable it and point it at `16. Meta/Templates`.
- **Obsidian Git** (community plugin) optional, for GitHub sync.

**Agent Compatibility:**
The vault is plain text, so any agent with filesystem access can use it.

**Skills Included:**
Two skills ship in **`Skills/`** `vault-keeper` (recall, promote, link, gap-check) and `draft-in-voice` (write copy that sounds like the p...)

---

## Summary

The chat identified two excellent Obsidian vaults for business and product development:

1. **lukeinglis/work-vault** - A comprehensive AI-powered vault with Claude Code integrations, perfect for PMs and project managers who need structured workflows, meeting notes, decisions, and initiatives tracking.

2. **Second Brain project vault** - A general-purpose second brain template designed for AI agents, with well-organized domains for all aspects of life and work.

Both vaults are available on GitHub and use plain text markdown, making them easy to use with AI agents while maintaining full Obsidian functionality.
