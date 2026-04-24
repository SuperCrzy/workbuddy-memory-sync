---
name: memory-sync
description: >
  WorkBuddy Memory 云同步技能。将 AI 的记忆文件（.workbuddy/memory/）同步到 GitHub 私有仓库，
  实现多设备之间的上下文记忆共享。支持推送记忆、拉取记忆、查看同步状态、初始化配置。
  触发词：同步记忆、上传记忆、下载记忆、memory同步、记忆同步、sync memory、
  push memory、pull memory、多设备同步、跨设备记忆、记忆备份、memory备份。
version: 1.1.0
author: SuperCrzy
license: MIT
repository: https://github.com/SuperCrzy/workbuddy-memory-sync
scripts_dir: scripts
---

# Memory Sync Skill

将 WorkBuddy 的 Memory 文件同步到 GitHub 私有仓库，让你在多台设备之间共享 AI 的记忆上下文。

**核心脚本**：`scripts/memory_sync.py`  
**支持平台**：Windows / macOS / Linux  
**依赖**：Python 3.8+、Git

---

## 触发词识别规则

| 用户说的话 | 执行操作 |
|---|---|
| "同步记忆"、"推送记忆"、"上传记忆"、"备份记忆" | push |
| "拉取记忆"、"下载记忆"、"恢复记忆"、"同步到本地" | pull |
| "记忆同步状态"、"查看同步" | status |
| "配置记忆同步"、"初始化同步" | setup |

---

## 命令执行方式

执行脚本前，先用以下方式确定 Python 命令：
- Windows：`python` 或 `py`
- macOS/Linux：`python3`

### 推送记忆到 GitHub
```bash
python scripts/memory_sync.py push
```

### 从 GitHub 拉取最新记忆
```bash
python scripts/memory_sync.py pull
```

### 查看同步状态
```bash
python scripts/memory_sync.py status
```

### 初始化配置（首次使用）
```bash
python scripts/memory_sync.py setup --repo <仓库URL> --token <Token>
```

---

## 完整工作流程

### 当用户触发 push 时：
1. 检查配置文件 `~/.workbuddy/memory-sync-config.json` 是否存在
2. 若未配置，提示用户先运行 setup，并引导获取 GitHub Token
3. 执行 push 命令，展示结果

### 当用户触发 pull 时：
1. 执行 pull 命令
2. 展示更新了哪些文件

### 当用户触发 setup 时：
1. 询问用户的 GitHub 仓库 URL
2. 询问 GitHub Personal Access Token（需要 repo 权限）
3. 执行 setup 命令完成配置

---

## 注意事项

- 配置文件 `~/.workbuddy/memory-sync-config.json` 包含 Token，已加入 `.gitignore`，不会被上传
- 冲突策略：以**最新修改时间**为准，更新的文件覆盖旧文件
- 建议使用 **GitHub 私有仓库**，memory 内容属于个人隐私
- 可通过环境变量 `WORKBUDDY_MEMORY_DIR` 指定自定义 memory 目录
