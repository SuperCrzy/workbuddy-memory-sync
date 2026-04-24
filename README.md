# Universal AI Memory Sync

> 跨平台 AI 记忆同步 — 一个工具，同步所有 AI 智能体的记忆上下文。  
> One tool to sync memory across all your AI agents.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-green)]()
[![Version](https://img.shields.io/badge/version-1.3.0-brightgreen)]()

---

## 愿景 / Vision

> **"Every AI agent has memory. No AI agent should lose it."**

今天，每个 AI 开发者都在使用多个 AI 工具：WorkBuddy 处理日常任务、Cursor 写代码、Windsurf 做设计……但每个工具的记忆都是一座孤岛——在 WorkBuddy 里建立的项目上下文，换到 Cursor 就消失了。

**这个问题不应该存在。**

Universal AI Memory Sync 的目标是成为 AI 记忆的"公共基础设施"：一个工具，连接所有 AI 平台，把散落在各处的记忆文件统一同步到 GitHub，让 AI 的上下文真正跟人走，而不是跟设备或应用绑定。

**This project aims to become the "public infrastructure" for AI memory** — one tool that connects all AI platforms, syncing scattered memory files to GitHub, so that AI context follows the user, not the device or application.

```
Today's Reality:
WorkBuddy ──── isolated memory ──── GitHub private repo
Cursor    ──── isolated memory ──── (no sync)
OpenClaw  ──── isolated memory ──── (different repo)
Windsurf  ──── isolated memory ──── (no sync)

With Universal Memory Sync:
WorkBuddy ──┐
Cursor    ──┼── unified sync ── GitHub private repo ── any device
OpenClaw  ──┤                     (one tool, all agents)
Windsurf  ──┘
```

---

## 全网调研：竞品格局分析 / Competitive Landscape

| 项目 | 定位 | Stars | 特点 |
|------|------|-------|------|
| **mem0** | Universal Memory Layer | ⭐ 53.9k | 向量数据库 + 语义检索，依赖 LLM API，付费云服务 |
| **AgentMem** | SaaS 跨 Agent 同步 | 商业产品 | API 服务，$29/月起 |
| **SAMEP** (arXiv) | 企业级协议 | 论文阶段 | PostgreSQL + Pinecone + Redis，复杂部署 |
| **ClawSouls Memory Sync** | OpenClaw 官方方案 | — | `age` 加密 + GitHub API，绑定 OpenClaw |
| **OpenClaw Memory Sync Protocol** | Skill 工作流规范 | — | 多文件协同更新逻辑，非云同步工具 |

> **关键发现：** 重量级方案（mem0/AgentMem）太重太贵；轻量方案（ClawSouls/我们）又各自绑定单一平台。**没有人做"跨平台 + 轻量 + 纯 Git 文件 + 零依赖"这件事——这是本项目的差异化定位。**

---

## 功能特性 / Features

| 功能 / Feature | 说明 / Description |
|---|---|
| ✅ **一句话触发 / One-phrase trigger** | 对 AI 说"同步记忆"即可 / Just say "sync memory" |
| ✅ **多平台支持 / Multi-agent support** | workbuddy / cursor / openclaw / windsurf / generic |
| ✅ **全量工作区扫描 / Full workspace scan** | 自动扫描所有工作区，一次同步 / Auto-scans all workspaces in one shot |
| ✅ **跨平台 / Cross-platform** | Windows / macOS / Linux |
| ✅ **冲突处理 / Conflict handling** | 按最新修改时间合并 / Latest mtime wins |
| ✅ **版本历史 / Version history** | 每次同步生成 Git commit，随时回溯 |
| ✅ **隐私安全 / Privacy** | 私有仓库，Token 仅存本地 / Private repo, Token stored locally |
| ✅ **零依赖 / Zero dependencies** | 只需 Python 3.8+ 和 Git |
| ✅ **agents 命令 / Discovery** | 一键扫描本机所有 AI 平台的记忆目录 |

---

## 支持的 AI 平台 / Supported Agents

| 平台 / Agent | 记忆文件 / Memory Files | 检测路径 / Search Paths |
|---|---|---|
| **workbuddy** | `.workbuddy/memory/*.md` | `~/.workbuddy/memory/` + `~/WorkBuddy/<id>/.workbuddy/memory/` |
| **cursor** | `CLAUDE.md`, `.cursorrules`, `.cursor/rules/` | `~/.cursor/rules/` + `~/projects/*/` |
| **openclaw** | `MEMORY.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`, `AGENTS.md`, `memory/*.md` | `~/.openclaw/workspace/` + `~/.openclaw/agents/<cid>/` + 项目目录 |
| **hermes** | `MEMORY.md`, `USER.md`, `state.db` | `~/.hermes/memories/` |
| **windsurf** | `.windsurf/rules/`, `.windsurf/memory/` | `~/.windsurf/rules/`, `~/.windsurf/memory/` |
| **generic** | 任意目录（环境变量指定） | Custom via `MEMORY_DIR` env var |
| **all** | 以上全部 | All detected sources |

---

## 快速开始 / Quick Start

### 第一步 / Step 1：创建 GitHub 私有仓库 / Create GitHub Private Repo

1. 访问 [github.com/new](https://github.com/new)
2. 创建 **Private** 仓库，名称建议：`ai-memory`
3. 勾选 **Add a README file**

### 第二步 / Step 2：获取 Personal Access Token

1. 访问 [github.com/settings/tokens/new](https://github.com/settings/tokens/new)
2. Note: `ai-memory-sync`
3. 权限：勾选 `repo`
4. 生成并复制 Token

### 第三步 / Step 3：安装 / Install

**Windows：**
```powershell
git clone https://github.com/SuperCrzy/workbuddy-memory-sync "$env:USERPROFILE\.workbuddy\skills\memory-sync"
```

**macOS / Linux：**
```bash
git clone https://github.com/SuperCrzy/workbuddy-memory-sync ~/.workbuddy/skills/memory-sync
```

### 第四步 / Step 4：初始化 / Initialize

```bash
# Windows
python %USERPROFILE%\.workbuddy\skills\memory-sync\scripts\memory_sync.py setup --repo https://github.com/yourname/ai-memory --token ghp_xxxxx

# macOS / Linux
python3 ~/.workbuddy/skills/memory-sync/scripts/memory_sync.py setup --repo https://github.com/yourname/ai-memory --token ghp_xxxxx
```

---

## 使用方法 / Usage

### 对 AI 说话（推荐）/ Talk to AI (Recommended)

| 你说的话 / What you say | AI 执行 / AI does |
|---|---|
| 同步记忆 / sync memory / push memory | 推送所有平台记忆到 GitHub |
| 拉取记忆 / pull memory / download memory | 从 GitHub 拉取最新记忆 |
| 记忆同步状态 / memory sync status | 查看仓库和本地文件信息 |
| 查看有哪些平台 / agents | 扫描本机所有 AI 平台的记忆目录 |
| 配置记忆同步 / setup memory sync | 初始化配置 |

### 直接运行命令 / Run Commands Directly

```bash
# 推送指定平台 / Push specific agent
python memory_sync.py push --agent workbuddy
python memory_sync.py push --agent cursor
python memory_sync.py push --agent all          # 推送全部 / Push all

# 拉取 / Pull
python memory_sync.py pull --agent openclaw

# 查看本机有哪些 AI 平台 / Discover agents on this machine
python memory_sync.py agents

# 查看状态 / Check status
python memory_sync.py status
```

---

## GitHub 仓库结构 / Repository Structure

同步后，GitHub 私有仓库按以下结构存储所有平台的记忆：  
After sync, your private GitHub repo stores memory for all agents:

```
ai-memory/                    (你的私有仓库 / your private repo)
├── agents/
│   ├── workbuddy/
│   │   ├── __user__/         ← 用户级记忆 / User-level memory
│   │   │   └── MEMORY.md
│   │   └── workspaces/       ← 工作区记忆 / Workspace memory
│   │       ├── 20260424095145/
│   │       │   └── 2026-04-24.md
│   │       └── Claw/
│   ├── cursor/
│   │   ├── rules/            ← Cursor rules
│   │   └── projects/         ← Project-level CLAUDE.md
│   ├── openclaw/
│   │   ├── workspace/        ← OpenClaw 标准工作区 ~/.openclaw/workspace/
│   │   │   ├── MEMORY.md
│   │   │   ├── SOUL.md
│   │   │   ├── USER.md
│   │   │   ├── IDENTITY.md
│   │   │   └── memory/
│   │   │       └── YYYY-MM-DD.md
│   │   └── agents/<cid>/    ← 各会话的状态目录
│   ├── hermes/
│   │   ├── memories/         ← Hermes 标准记忆 ~/.hermes/memories/
│   │   │   ├── MEMORY.md
│   │   │   └── USER.md
│   │   └── state.db          ← SQLite 会话状态
│   └── windsurf/
│       ├── rules/
│       └── memory/
```

---

## 多设备同步工作流 / Multi-Device Workflow

```
设备 A（如家里）/ Device A (Home)              设备 B（如公司）/ Device B (Office)
──────────────────────────────────────         ──────────────────────────────────────
1. 安装 Skill / Install Skill                  1. 安装 Skill / Install Skill
2. 运行 setup / Run setup                      2. 运行 setup / Run setup
3. 对 AI 说"同步记忆"  ────────────────→        3. 对 AI 说"拉取记忆" / Run "pull"
   (push --agent all)                              (pull all agents)
                                              4. AI 在各平台恢复上下文
                                                 AI resumes context on all platforms
```

---

## 环境变量 / Environment Variables

| 变量 / Variable | 说明 / Description | 默认值 / Default |
|---|---|---|
| `WORKBUDDY_WORKSPACE_ROOT` | WorkBuddy 工作区根目录 / Workspace root | `~/WorkBuddy` |
| `MEMORY_DIR` | generic 模式的记忆目录 / Memory dir for generic mode | (none) |

---

## 文件结构 / Project Structure

```
memory-sync/
├── SKILL.md              # WorkBuddy Skill 描述 / Skill descriptor
├── README.md             # 本文档 / This document
├── LICENSE               # MIT License
├── .gitignore            # 排除配置文件（含 Token）/ Exclude config file
└── scripts/
    └── memory_sync.py    # 核心脚本 v1.3.0 / Core script
```

---

## 冲突处理 / Conflict Resolution

当同一文件在多台设备被同时修改时，以**最新修改时间（mtime）**为准。每次推送生成一条 Git commit，可通过 `git log` 查看历史并回滚。

---

## 常见问题 / FAQ

**Q: 推送失败，提示 authentication failed？**  
A: Token 可能已过期，重新运行 `setup` 命令更新。

**Q: 拉取后 AI 还是不记得之前的事？**  
A: 运行 `status` 确认文件已拉取，然后**开启新对话**，AI 在会话开始时读取 memory。

**Q: 如何同步 Cursor 的记忆？**  
A: `python memory_sync.py push --agent cursor` — 自动扫描 `~/.cursor/rules/` 和项目目录。

**Q: 支持 OpenClaw 吗？**  
A: 支持。OpenClaw 检测 `MEMORY.md` / `TOOLS.md` / `AGENTS.md` 和 `memory/*.md` 文件，自动归档到 `agents/openclaw/` 目录。

**Q: Token 安全吗？**  
A: Token 仅存储在 `~/.workbuddy/memory-sync-config.json`，已加入 `.gitignore`，永不推送。

---

## Roadmap

- [ ] **v1.4** — 可选 age 加密层（参考 ClawSouls，实现端到端加密）
- [ ] **v2.0** — 通用 AI Memory Spec：统一的 `.ai-memory/` 目录结构，让所有平台采用同一标准
- [ ] **v2.1** — MCP 协议集成，让 Agent 之间可以互相查询彼此的记忆
- [ ] **社区** — 推动更多 AI Agent 采用标准化的记忆文件格式

---

## 参与贡献 / Contributing

欢迎提 Issue 和 PR！  
Issues and PRs are welcome!

- 报告 Bug → [Issues](https://github.com/SuperCrzy/workbuddy-memory-sync/issues)
- 功能建议 → [Issues](https://github.com/SuperCrzy/workbuddy-memory-sync/issues)
- 添加新平台支持 → 提交 PR，参考 `discover_agent_dirs()` 函数

---

## License

MIT © [SuperCrzy](https://github.com/SuperCrzy)
