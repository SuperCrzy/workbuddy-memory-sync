---
name: memory-sync
description: >
  WorkBuddy Memory cloud sync skill. Syncs AI memory files (.workbuddy/memory/) to a
  private GitHub repository, enabling cross-device context sharing.
  Supports push, pull, status check, and initial setup.
  WorkBuddy Memory 云同步技能。将 AI 的记忆文件同步到 GitHub 私有仓库，
  实现多设备之间的上下文记忆共享。支持推送记忆、拉取记忆、查看同步状态、初始化配置。
  支持多平台：workbuddy / cursor / openclaw / windsurf / generic / all。
  触发词：同步记忆、上传记忆、下载记忆、memory同步、记忆同步、sync memory、
  push memory、pull memory、多设备同步、跨设备记忆、记忆备份、memory备份、
  同步记忆到github、拉取最新记忆、记忆云同步、查看有哪些平台、agents扫描。
version: 1.3.0
author: SuperCrzy
license: MIT
repository: https://github.com/SuperCrzy/workbuddy-memory-sync
scripts_dir: scripts
---

# Memory Sync Skill

将 WorkBuddy 及所有主流 AI 平台的 Memory 文件同步到 GitHub 私有仓库，支持跨设备、跨平台共享 AI 记忆上下文。

**核心脚本 / Core script**：`scripts/memory_sync.py`  
**支持平台 / Platforms**：Windows / macOS / Linux  
**依赖 / Dependencies**：Python 3.8+、Git

---

## 支持的平台 / Supported Agents

| 平台 | 触发参数 |
|---|---|
| WorkBuddy | `--agent workbuddy` |
| Cursor | `--agent cursor` |
| OpenClaw | `--agent openclaw` |
| Hermes | `--agent hermes` |
| Windsurf | `--agent windsurf` |
| 自定义目录 | `--agent generic` |
| **全部平台 / All** | `--agent all` |

---

## 触发词识别规则 / Trigger Rules

| 用户说的话 / User says | 执行操作 / Action |
|---|---|
| "同步记忆"、"推送记忆"、"上传记忆"、"备份记忆" / "sync memory", "push memory" | push（默认 workbuddy） |
| "同步全部"、"推送所有平台" / "sync all agents", "push all" | push --agent all |
| "同步 OpenClaw/Hermes/Cursor" / "sync openclaw" | push --agent openclaw/hermes/cursor |
| "拉取记忆"、"下载记忆"、"恢复记忆" / "pull memory", "download memory" | pull |
| "记忆同步状态"、"查看同步" / "memory sync status" | status |
| "查看有哪些平台"、"扫描 AI 平台" / "show agents", "agents scan" | agents |
| "配置记忆同步"、"初始化同步" / "setup memory sync" | setup |

---

## 命令参考 / Command Reference

### 推送记忆 / Push memory
```bash
# Windows
python %USERPROFILE%\.workbuddy\skills\memory-sync\scripts\memory_sync.py push --agent workbuddy

# macOS / Linux
python3 ~/.workbuddy/skills/memory-sync/scripts/memory_sync.py push --agent all
```

### 拉取记忆 / Pull memory
```bash
python scripts/memory_sync.py pull --agent cursor
python scripts/memory_sync.py pull --agent all    # 拉取所有平台 / Pull all
```

### 查看本机 AI 平台 / Discover agents
```bash
python scripts/memory_sync.py agents               # 扫描并列出所有检测到的记忆目录
```

### 查看同步状态 / Check status
```bash
python scripts/memory_sync.py status
```

### 初始化配置 / Initialize
```bash
python scripts/memory_sync.py setup --repo <URL> --token <TOKEN>
```

---

## 完整工作流程 / Full Workflow

### push 触发时 / When push is triggered:
1. 检查 `~/.workbuddy/memory-sync-config.json` 是否存在
2. 若未配置，提示用户运行 setup
3. 根据 `--agent` 参数扫描对应的记忆目录
4. 推送到 GitHub，展示结果

### pull 触发时 / When pull is triggered:
1. 从 GitHub 拉取最新文件
2. 按 agent 类型还原到本地对应目录
3. 展示更新了哪些文件

### agents 触发时 / When agents is triggered:
1. 扫描本机所有支持的 AI 平台
2. 列出检测到的记忆目录和文件数量
3. 帮助用户了解哪些平台有记忆可同步

### setup 触发时 / When setup is triggered:
1. 询问 GitHub 仓库 URL
2. 询问 Personal Access Token（需 `repo` 权限）
3. 验证连接，完成配置

---

## 注意事项 / Notes

- 配置文件 `~/.workbuddy/memory-sync-config.json` 包含 Token，已加入 `.gitignore`，永不推送
- 冲突策略：**最新修改时间（mtime）** 优先
- 建议使用 **GitHub 私有仓库**
- 环境变量 `WORKBUDDY_WORKSPACE_ROOT` 可覆盖工作区根目录
- 环境变量 `MEMORY_DIR` 用于 generic 模式指定自定义目录
