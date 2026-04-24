# Universal AI Memory Sync

> One tool to sync memory across all your AI agents — Cursor, OpenClaw, Hermes, Windsurf, WorkBuddy, and more.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-green)]()
[![Version](https://img.shields.io/badge/version-1.5.0-brightgreen)]()

![Demo](demo.gif)

---

## Vision

> **"Every AI agent has memory. No AI agent should lose it."**

Today, every AI developer uses multiple AI tools: Cursor for coding, Windsurf for design, OpenClaw for automation, Hermes for tasks… but each tool's memory is an island — the project context you built in Cursor disappears the moment you switch to Windsurf.

**This shouldn't be a problem.**

Universal AI Memory Sync aims to become the **public infrastructure for AI memory** — one tool that connects all AI platforms, syncing scattered memory files to GitHub, so that AI context follows the user, not the device or application.

```
Today's Reality:
Cursor    ──── isolated memory ──── (no sync)
OpenClaw  ──── isolated memory ──── (different repo)
Windsurf  ──── isolated memory ──── (no sync)
Hermes    ──── isolated memory ──── (no sync)

With Universal Memory Sync:
Cursor    ──┐
OpenClaw  ──┼── unified sync ── GitHub private repo ── any device
Windsurf  ──┤                     (one tool, all agents)
Hermes    ──┘
WorkBuddy ──┘
```

---

## Competitive Landscape

| Project | Focus | Stars | Notes |
|---------|-------|-------|-------|
| **mem0** | Universal Memory Layer | ⭐ 53.9k | Vector DB + semantic search; requires LLM API, paid cloud service |
| **AgentMem** | SaaS Cross-Agent Sync | Commercial | API service, $29/mo+ |
| **SAMEP** (arXiv) | Enterprise Protocol | Paper only | PostgreSQL + Pinecone + Redis, complex setup |
| **ClawSouls Memory Sync** | OpenClaw Official | — | `age` encryption + GitHub API, OpenClaw-only |

> **Key insight:** Heavy solutions (mem0/AgentMem) are too complex and expensive; lightweight solutions (ClawSouls/ours) are each tied to a single platform. **Nobody is doing "cross-platform + lightweight + pure Git files + zero dependencies" — that's our positioning.**

---

## Features

| Feature | Description |
|---|---|
| ✅ **One-phrase trigger** | Just say "sync memory" — no commands needed |
| ✅ **Multi-agent support** | cursor / openclaw / hermes / windsurf / workbuddy / generic / all |
| ✅ **Full workspace scan** | Auto-scans all workspaces in one shot |
| ✅ **Cross-platform** | Windows / macOS / Linux |
| ✅ **Conflict handling** | Latest mtime wins; full Git history for rollback |
| ✅ **Version history** | Every sync creates a Git commit; revert anytime |
| ✅ **Privacy-first** | Private repo; token stored locally only |
| ✅ **Zero dependencies** | Python 3.8+ and Git — that's it |
| ✅ **Discovery command** | `agents` command scans all AI platforms on your machine |

---

## Supported Agents

| Agent | Memory Files | Search Paths |
|---|---|---|
| **cursor** | `CLAUDE.md`, `.cursorrules`, `.cursor/rules/` | `~/.cursor/rules/` + `~/projects/*/` |
| **openclaw** | `MEMORY.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`, `AGENTS.md`, `memory/*.md` | `~/.openclaw/workspace/` + `~/.openclaw/agents/<cid>/` + project dirs |
| **hermes** | `MEMORY.md`, `USER.md`, `state.db` | `~/.hermes/memories/` |
| **windsurf** | `.windsurf/rules/`, `.windsurf/memory/` | `~/.windsurf/rules/`, `~/.windsurf/memory/` |
| **workbuddy** | `.workbuddy/memory/*.md` | `~/.ai-memory/memory/workbuddy/` + `~/WorkBuddy/<id>/.workbuddy/memory/` |
| **generic** | Any directory | Custom via `MEMORY_DIR` env var |
| **all** | All of the above | All detected sources |

---

## Quick Start

### Step 1: Create a GitHub Private Repo

1. Go to [github.com/new](https://github.com/new)
2. Create a **Private** repo, name it: `ai-memory`
3. Check **Add a README file**

### Step 2: Get a Personal Access Token

1. Go to [github.com/settings/tokens/new](https://github.com/settings/tokens/new)
2. Note: `ai-memory-sync`
3. Scopes: check `repo` (full control)
4. Generate and copy the token

### Step 3: Install

```bash
# Clone anywhere convenient:
git clone https://github.com/SuperCrzy/AI-Memory-Sync ~/.ai-memory/skill

# Or as a WorkBuddy skill:
git clone https://github.com/SuperCrzy/AI-Memory-Sync ~/.workbuddy/skills/memory-sync
```

### Step 4: Initialize

```bash
# Windows
python ~/.ai-memory/skill/scripts/memory_sync.py setup --repo https://github.com/yourname/ai-memory --token ghp_xxxxx

# macOS / Linux
python3 ~/.ai-memory/skill/scripts/memory_sync.py setup --repo https://github.com/yourname/ai-memory --token ghp_xxxxx
```

---

## Usage

### Talk to Your AI (Recommended)

| What you say | AI does |
|---|---|
| "sync memory" / "push memory" | Push all agent memory to GitHub |
| "sync all agents" / "push all" | Push all platforms at once |
| "sync openclaw" / "sync hermes" | Push specific agent |
| "pull memory" / "download memory" | Pull latest memory from GitHub |
| "memory sync status" | Show repo and local file info |
| "agents" / "show agents" | Scan all AI platforms on this machine |
| "setup memory sync" | Initialize configuration |

### Run Commands Directly

```bash
# Push specific agent
python memory_sync.py push --agent cursor
python memory_sync.py push --agent all          # Push all at once

# Pull
python memory_sync.py pull --agent openclaw
python memory_sync.py pull --agent all          # Pull all at once

# Discover agents on your machine
python memory_sync.py agents

# Check status
python memory_sync.py status
```

---

## Language / i18n

Output language is auto-detected from your system locale. You can also set it manually:

```bash
# Force English (default if not set)
AI_MEMORY_LANG=en python memory_sync.py agents

# Force Chinese
AI_MEMORY_LANG=zh python memory_sync.py agents
```

Without the env var, the script reads `os.environ.get("LANG")` or `locale.getpreferredencoding()` to decide — Chinese system → Chinese output, otherwise English.

---

## Repository Structure

After sync, your GitHub private repo stores memory for all agents:

```
ai-memory/
├── agents/
│   ├── cursor/
│   │   ├── rules/               # ~/.cursor/rules/
│   │   └── projects/             # Project-level CLAUDE.md
│   ├── openclaw/
│   │   ├── workspace/            # ~/.openclaw/workspace/
│   │   │   ├── MEMORY.md
│   │   │   ├── SOUL.md
│   │   │   ├── USER.md
│   │   │   ├── IDENTITY.md
│   │   │   └── memory/
│   │   │       └── YYYY-MM-DD.md
│   │   └── agents/<cid>/        # Per-session state dirs
│   ├── hermes/
│   │   ├── memories/             # ~/.hermes/memories/
│   │   │   ├── MEMORY.md
│   │   │   └── USER.md
│   │   └── state.db              # SQLite session state
│   ├── windsurf/
│   │   ├── rules/
│   │   └── memory/
│   └── workbuddy/
│       ├── __user__/             # User-level memory
│       │   └── MEMORY.md
│       └── workspaces/           # Per-workspace memory
│           ├── 20260424095145/
│           └── Claw/
```

---

## Multi-Device Workflow

```
Device A (Home)                              Device B (Office)
───────────────────────                      ───────────────────────
1. Install Skill                             1. Install Skill
2. Run setup                                 2. Run setup
3. Say "sync memory" ────────→               3. Say "pull memory"
   (push --agent all)                           (pull --agent all)
                                              4. AI resumes context
                                                 on all platforms
```

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `AI_MEMORY_WORKSPACE_ROOT` | Workspace root directory | `~/WorkBuddy` |
| `AI_MEMORY_LANG` | Force output language (`en` or `zh`) | Auto-detect from system locale |
| `MEMORY_DIR` | Memory dir for generic mode | (none) |

---

## Project Structure

```
universal-ai-memory-sync/
├── SKILL.md              # Skill descriptor
├── README.md             # This document
├── LICENSE               # MIT License
├── .gitignore            # Excludes config (contains token)
├── demo.gif              # Terminal animation demo
└── scripts/
    ├── memory_sync.py    # Core script v1.5.0
    └── generate_demo_gif.py  # Demo GIF generator (optional)
```

---

## Conflict Resolution

When the same file is modified on multiple devices simultaneously, the **latest mtime wins**. Every push creates a Git commit — use `git log` to review history and revert if needed.

---

## FAQ

**Q: Push failed with authentication error?**
A: Your token may have expired. Re-run `setup` to update it.

**Q: AI still doesn't remember after pulling?**
A: Run `status` to confirm files were pulled, then **start a new conversation** — AI reads memory at the start of each session.

**Q: How do I sync Cursor memory?**
A: `python memory_sync.py push --agent cursor` — auto-scans `~/.cursor/rules/` and project directories.

**Q: Does it support OpenClaw?**
A: Yes. Detects `MEMORY.md` / `SOUL.md` / `USER.md` / `IDENTITY.md` / `AGENTS.md` and `memory/*.md` files, archives to `agents/openclaw/`.

**Q: Is my token safe?**
A: Token is stored in `~/.ai-memory/config.json`, which is in `.gitignore` and never pushed.

---

## Roadmap

- [ ] **v1.6** — Optional `age` encryption layer (end-to-end encryption)
- [ ] **v2.0** — Universal AI Memory Spec: a unified `.ai-memory/` directory structure adopted across all platforms
- [ ] **v2.1** — MCP protocol integration: agents can query each other's memory
- [ ] **Community** — Drive adoption of standardized memory file formats across AI agents

---

## Contributing

Issues and PRs are welcome!

- Bug reports → [Issues](https://github.com/SuperCrzy/AI-Memory-Sync/issues)
- Feature requests → [Issues](https://github.com/SuperCrzy/AI-Memory-Sync/issues)
- Add new platform support → Open a PR, reference the `discover_agent_dirs()` function

---

## License

MIT © [SuperCrzy](https://github.com/SuperCrzy)
