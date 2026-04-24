---
name: universal-memory-sync
description: >
  Universal AI Memory Sync Skill. Syncs memory files from Cursor / OpenClaw / Hermes / Windsurf / WorkBuddy
  and other AI agents to a private GitHub repository, enabling cross-device context sharing.
  Supports push, pull, status check, agents scan, and initial setup.
  Trigger phrases: sync memory, push memory, pull memory, download memory, memory sync, memory backup,
  memory sync status, agents scan, show agents, setup memory sync, push all agents,
  sync openclaw, sync hermes, sync cursor, universal memory sync, cross-agent memory.
version: 1.5.0
author: SuperCrzy
license: MIT
repository: https://github.com/SuperCrzy/AI-Memory-Sync
scripts_dir: scripts
---

# Universal Memory Sync Skill

Sync AI memory files from all major AI agents to a GitHub private repo — cross-device, cross-platform.

**Core script**: `scripts/memory_sync.py`
**Platforms**: Windows / macOS / Linux
**Dependencies**: Python 3.8+, Git

---

## Supported Agents

| Agent | Flag |
|---|---|
| Cursor | `--agent cursor` |
| OpenClaw | `--agent openclaw` |
| Hermes | `--agent hermes` |
| Windsurf | `--agent windsurf` |
| WorkBuddy | `--agent workbuddy` |
| Generic (custom dir) | `--agent generic` |
| **All platforms** | `--agent all` |

---

## Trigger Rules

| User says | Action |
|---|---|
| "sync memory", "push memory", "upload memory", "backup memory" | `push` (default: all) |
| "sync all agents", "push all" | `push --agent all` |
| "sync openclaw", "sync hermes", "sync cursor" | `push --agent <platform>` |
| "pull memory", "download memory", "restore memory" | `pull` |
| "memory sync status" | `status` |
| "show agents", "agents scan" | `agents` |
| "setup memory sync" | `setup` |

---

## Command Reference

### Push memory
```bash
# Push all platforms
python scripts/memory_sync.py push --agent all

# Push specific platform
python scripts/memory_sync.py push --agent cursor
```

### Pull memory
```bash
python scripts/memory_sync.py pull --agent cursor
python scripts/memory_sync.py pull --agent all    # Pull all platforms
```

### Discover agents
```bash
python scripts/memory_sync.py agents    # Scan and list all detected memory dirs
```

### Check status
```bash
python scripts/memory_sync.py status
```

### Initialize
```bash
python scripts/memory_sync.py setup --repo <URL> --token <TOKEN>
```

---

## Workflows

### When push is triggered:
1. Check config file exists (at `~/.ai-memory/config.json`)
2. If not configured, prompt user to run setup
3. Scan corresponding memory directories by `--agent` flag
4. Push to GitHub, display results

### When pull is triggered:
1. Pull latest files from GitHub
2. Restore to local directories per agent type
3. Display which files were updated

### When agents is triggered:
1. Scan all supported AI platforms on this machine
2. List detected memory directories and file counts
3. Help users understand which platforms have memory to sync

### When setup is triggered:
1. Ask for GitHub repo URL
2. Ask for Personal Access Token (requires `repo` scope)
3. Verify connection, save config

---

## Notes

- Config file at `~/.ai-memory/config.json` contains the token, is in `.gitignore`, and is never pushed
- Conflict strategy: **latest mtime wins**
- Use a **GitHub private repository** for security
- `AI_MEMORY_WORKSPACE_ROOT` env var overrides workspace root
- `AI_MEMORY_LANG` env var forces output language (`en` or `zh`)
- `MEMORY_DIR` env var specifies custom dir for generic mode
