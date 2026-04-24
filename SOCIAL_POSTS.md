# Social Media Posts — Universal AI Memory Sync

## Twitter / X

**Version 1 (short, punchy):**
> Every AI agent you use has its own memory. None of them sync.
>
> Built a tool to fix that — one GitHub repo, all your AI agents, zero lock-in.
> WorkBuddy + Cursor + OpenClaw + Hermes + Windsurf = one command.
>
> Open source: github.com/SuperCrzy/AI-Memory-Sync
> #AI #OpenSource #AIagents #MemorySync

**Version 2 (for developers):**
> PSA: If you're using multiple AI coding agents (Cursor, Windsurf, OpenClaw, WorkBuddy...), their memory is siloed by default.
>
> I open-sourced a zero-dependency tool that syncs all of them to a single GitHub private repo.
> Python + Git only. MIT license.
>
> `python memory_sync.py push --agent all`
>
> github.com/SuperCrzy/AI-Memory-Sync

---

## Reddit — r/programming

**Title:** [Open Source] Universal AI Memory Sync — one tool to sync memory across all AI agents (WorkBuddy, Cursor, OpenClaw, Hermes, Windsurf) to a GitHub private repo

**Body:**
> Every AI developer I know uses multiple AI agents daily. But each one stores its memory differently, in its own format, with no way to sync it across devices — let alone across platforms.
>
> I built a tool to solve this. It's dead simple:
>
> ```bash
> # Push all agents' memory to GitHub
> python memory_sync.py push --agent all
>
> # Pull on another device
> python memory_sync.py pull --agent all
>
> # Discover all AI platforms on your machine
> python memory_sync.py agents
> ```
>
> **What it syncs:**
> - WorkBuddy: `.workbuddy/memory/*.md`
> - OpenClaw: `MEMORY.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`, `AGENTS.md`, `memory/*.md`
> - Hermes: `MEMORY.md`, `USER.md`, `state.db`
> - Cursor: `CLAUDE.md`, `.cursorrules`, `.cursor/rules/`
> - Windsurf: `.windsurf/rules/`, `.windsurf/memory/`
>
> **No dependencies** — just Python 3.8+ and Git. Config stored locally, never pushed. Conflict resolution via mtime + full Git history.
>
> Repo: github.com/SuperCrzy/AI-Memory-Sync
>
> MIT license. PRs welcome.

---

## Hacker News

**Title:** Show HN: Universal AI Memory Sync — sync memory across all AI agents to GitHub

**Body:**
> Every AI agent has its own memory format and storage location. None of them talk to each other.
>
> I use WorkBuddy, OpenClaw, and Hermes across multiple devices. The context I built in WorkBuddy disappears when I switch to Cursor. This is a solved problem for humans (Git) but nobody built it for AI memory specifically.
>
> So I built it.
>
> **github.com/SuperCrzy/AI-Memory-Sync** — MIT license, Python + Git only, zero lock-in.
>
> Supported agents: WorkBuddy, OpenClaw, Hermes, Cursor, Windsurf (and a generic mode for anything else).
>
> One command to push all memory to a GitHub private repo:
> `python memory_sync.py push --agent all`
>
> One command to pull on any other device: `python memory_sync.py pull --agent all`
>
> Key design decisions:
> - Pure file-based (Markdown). No database, no API dependency.
> - Git as the sync and versioning layer. Works offline, full history, rollback anytime.
> - Token stored locally, never pushed.
> - mtime-based conflict resolution.
>
> Would love feedback on the approach. Particularly curious if others hit this pain point too.

---

## Reddit — r/ArtificialIntelligence

**Title:** Built a free tool to sync AI agent memory across all platforms to GitHub — no vector DB, no API key, just Python + Git

**Body:**
> Been thinking about AI memory fragmentation. mem0 (53k stars) exists but it's heavy — needs a vector DB, LLM API, and costs money. AgentMem is $29/mo. SAMEP is academic.
>
> For people who just want their AI to remember things across devices without the overhead... here's a lightweight alternative.
>
> github.com/SuperCrzy/AI-Memory-Sync
>
> - Pure Markdown files + Git
> - Supports WorkBuddy, OpenClaw, Hermes, Cursor, Windsurf
> - One push pulls context from all agents into one private GitHub repo
> - Zero dependencies (Python 3.8+ and Git)
> - MIT license

---

## Product Hunt (optional launch)

**Tagline:** Sync your AI agent's memory across all platforms — for free.

**Pitch:**
> **Problem:** You use 3+ AI agents across devices. Each one has its own memory. You keep repeating yourself.
>
> **Solution:** One GitHub repo. All your AI agents. Zero lock-in.
>
> **How it works:**
> 1. Install the skill into your AI agent (WorkBuddy, OpenClaw, Hermes, etc.)
> 2. Run `push` once — all memory syncs to your private GitHub repo
> 3. On another device, run `pull` — AI context restored instantly
>
> No vector DB. No paid API. Just Python and Git.

