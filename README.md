# WorkBuddy Memory Sync

> 跨设备同步 WorkBuddy AI 记忆的 Skill —— 换台电脑，AI 依然记得你们聊过什么。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-green)]()

---

## 为什么需要这个 Skill？

WorkBuddy 默认将 AI 的记忆（`.workbuddy/memory/`）存储在本地。当你在家里和 AI 聊了很多、建立了上下文之后，换到公司电脑，AI 对之前的一切一无所知。

这个 Skill 通过 GitHub 私有仓库，将记忆文件自动同步到云端，让你在任何设备上都能让 AI 延续之前的上下文。

```
家里电脑                      GitHub 私有仓库               公司电脑
.workbuddy/memory/   →  push  →  memory/MEMORY.md   →  pull  →  .workbuddy/memory/
                                  memory/2026-04-24.md
                                  ...
```

---

## 功能特性

- ✅ **一句话触发**：对 AI 说"同步记忆"即可自动推送
- ✅ **跨平台**：支持 Windows / macOS / Linux
- ✅ **冲突处理**：按最新修改时间自动合并，不会覆盖更新的内容
- ✅ **版本历史**：每次同步都有 Git 提交记录，可回溯任意历史版本
- ✅ **隐私安全**：使用 GitHub 私有仓库，Token 存储在本地不会上传
- ✅ **零依赖**：只需 Python 3.8+ 和 Git，无需安装第三方库

---

## 快速开始

### 第一步：准备 GitHub 私有仓库

1. 访问 [github.com/new](https://github.com/new)
2. 创建一个**私有（Private）仓库**，名称建议：`workbuddy-memory`
3. 勾选 **Add a README file**（仓库不能为空）

### 第二步：获取 Personal Access Token

1. 访问 [GitHub Token 设置页](https://github.com/settings/tokens/new)
2. Note 填写：`workbuddy-memory-sync`
3. 权限勾选：`repo`（完整仓库读写权限）
4. 点击 **Generate token**，**立即复制**（只显示一次！）

### 第三步：安装 Skill

将本项目复制到 WorkBuddy 的用户级 Skill 目录：

**Windows：**
```powershell
# 克隆到 Skill 目录
git clone https://github.com/SuperCrzy/workbuddy-memory-sync "$env:USERPROFILE\.workbuddy\skills\memory-sync"
```

**macOS / Linux：**
```bash
git clone https://github.com/SuperCrzy/workbuddy-memory-sync ~/.workbuddy/skills/memory-sync
```

### 第四步：初始化配置

在 WorkBuddy 中对 AI 说：

> "配置记忆同步，仓库是 `https://github.com/你的用户名/workbuddy-memory`，Token 是 `ghp_xxxxx`"

或者直接运行命令：

```bash
python ~/.workbuddy/skills/memory-sync/scripts/memory_sync.py setup \
  --repo https://github.com/你的用户名/workbuddy-memory \
  --token ghp_xxxxx
```

---

## 使用方法

### 对 AI 说话（推荐）

| 你说的话 | AI 执行的操作 |
|---|---|
| 同步记忆 / 推送记忆 / 备份记忆 | 将本地 memory 推送到 GitHub |
| 拉取记忆 / 下载记忆 / 恢复记忆 | 从 GitHub 拉取最新 memory |
| 记忆同步状态 | 查看仓库和本地文件信息 |
| 配置记忆同步 | 初始化配置 |

### 直接运行命令

```bash
# 推送记忆
python scripts/memory_sync.py push

# 拉取记忆
python scripts/memory_sync.py pull

# 查看状态
python scripts/memory_sync.py status

# 初始化配置
python scripts/memory_sync.py setup
```

---

## 多设备同步工作流

```
第一台电脑（如家里）              第二台电脑（如公司）
─────────────────────            ─────────────────────
1. 安装 Skill                    1. 安装 Skill
2. 运行 setup 配置同一仓库        2. 运行 setup 配置同一仓库
3. 工作完成后说"同步记忆"  ──→   3. 开始工作前说"拉取记忆"
   (push 到 GitHub)                 (pull 最新 memory)
                                 4. AI 自动读取记忆，上下文恢复
```

---

## 自定义 Memory 目录

如果你的 WorkBuddy memory 不在默认位置，可通过环境变量指定：

```bash
# Windows PowerShell
$env:WORKBUDDY_MEMORY_DIR = "D:\MyWorkBuddy\memory"
python scripts/memory_sync.py push

# macOS / Linux
WORKBUDDY_MEMORY_DIR=/custom/path/memory python scripts/memory_sync.py push
```

---

## 文件结构

```
memory-sync/
├── SKILL.md              # WorkBuddy Skill 描述文件
├── README.md             # 本文档
├── LICENSE               # MIT License
├── .gitignore            # 排除配置文件（含 Token）
└── scripts/
    └── memory_sync.py    # 核心同步脚本
```

**注意**：配置文件 `~/.workbuddy/memory-sync-config.json` 存储在用户目录，不包含在本仓库中。

---

## 冲突处理策略

当两台设备都修改了同一个 memory 文件时：

- 以**最新修改时间**（mtime）为准
- 更新的版本会覆盖较旧的版本
- 每次推送都会产生一条 Git 提交记录，可通过 `git log` 查看历史

---

## 常见问题

**Q: 推送失败，提示 authentication failed？**  
A: 检查 Token 是否过期，重新运行 `setup` 命令更新 Token。

**Q: 拉取后 AI 还是不记得之前的事？**  
A: 确认 memory 文件已拉取到正确目录（运行 `status` 查看），然后开启新的对话即可。

**Q: 能同时同步多个工作区的 memory 吗？**  
A: 可以多次运行 push 并传入不同目录：`python memory_sync.py push /path/to/memory`

**Q: Token 安全吗？**  
A: Token 仅存储在本地 `~/.workbuddy/memory-sync-config.json`，不会被推送到任何仓库。建议使用最小权限（仅 `repo` 权限）并定期更换。

---

## License

MIT © [SuperCrzy](https://github.com/SuperCrzy)

欢迎提 Issue 和 PR！
