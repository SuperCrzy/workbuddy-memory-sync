#!/usr/bin/env python3
"""
WorkBuddy Memory Sync - 跨设备记忆同步工具
自动扫描所有工作区的 memory 目录，同步到 GitHub 私有仓库。

用法:
  python memory_sync.py setup                           # 交互式初始化配置
  python memory_sync.py setup --repo URL --token TOKEN  # 直接配置
  python memory_sync.py push                            # 推送全部记忆到 GitHub
  python memory_sync.py pull                            # 从 GitHub 拉取记忆到本地
  python memory_sync.py status                          # 查看同步状态

GitHub 仓库结构:
  memory/                  <- 用户级 memory (~/.workbuddy/memory/)
    MEMORY.md
  workspaces/
    <workspace_id>/        <- 各工作区 memory
      2026-04-24.md
      MEMORY.md

项目地址: https://github.com/SuperCrzy/workbuddy-memory-sync
"""

import sys
import os
import json
import subprocess
import shutil
import platform
from pathlib import Path
from datetime import datetime

# ── Windows 控制台 UTF-8 输出修复 ────────────────────────────
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── 路径：全部动态解析，无硬编码 ──────────────────────────────
WORKBUDDY_DIR  = Path.home() / ".workbuddy"
CONFIG_PATH    = WORKBUDDY_DIR / "memory-sync-config.json"
REPO_CACHE     = WORKBUDDY_DIR / "memory-sync-repo"

# WorkBuddy 工作区根目录（可通过环境变量覆盖）
def get_workspace_root() -> Path:
    env = os.environ.get("WORKBUDDY_WORKSPACE_ROOT")
    if env:
        return Path(env)
    # 自动推断：脚本所在的 Skill 目录向上找 WorkBuddy 根目录
    # 典型路径：~/.workbuddy/skills/memory-sync/scripts/memory_sync.py
    # 或：~/WorkBuddy/<workspace_id>/.workbuddy/skills/...
    # WorkBuddy 工作区通常在 ~/WorkBuddy/
    candidates = [
        Path.home() / "WorkBuddy",
        Path.home() / "workbuddy",
        Path("C:/Users") / os.environ.get("USERNAME", "user") / "WorkBuddy",
    ]
    for c in candidates:
        if c.exists():
            return c
    return Path.home() / "WorkBuddy"


def scan_all_memory_dirs() -> dict[str, Path]:
    """
    扫描所有 memory 目录，返回 {标识名: 路径} 字典。
    包括：
      - 用户级：~/.workbuddy/memory/
      - 各工作区：~/WorkBuddy/<id>/.workbuddy/memory/
    """
    dirs = {}

    # 用户级 memory
    user_mem = WORKBUDDY_DIR / "memory"
    if user_mem.exists() and list(user_mem.glob("*.md")):
        dirs["__user__"] = user_mem

    # 各工作区 memory
    ws_root = get_workspace_root()
    if ws_root.exists():
        for ws_dir in sorted(ws_root.iterdir()):
            if not ws_dir.is_dir():
                continue
            mem_path = ws_dir / ".workbuddy" / "memory"
            if mem_path.exists() and list(mem_path.glob("*.md")):
                dirs[ws_dir.name] = mem_path

    return dirs


# ── 工具函数 ──────────────────────────────────────────────────

def log(msg: str):
    print(msg, flush=True)

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        log("[ERROR] 未找到配置文件，请先运行 setup 命令：")
        log("  python memory_sync.py setup --repo <仓库URL> --token <Token>")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config: dict):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    log(f"[OK] 配置已保存到 {CONFIG_PATH}")

def build_auth_url(repo_url: str, token: str) -> str:
    if "github.com" in repo_url and token:
        return repo_url.replace("https://", f"https://{token}@")
    return repo_url

def run_git(args: list, cwd: str, silent: bool = False) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=os.environ.copy()
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def ensure_repo(config: dict) -> Path:
    repo_url = config["repo_url"]
    token    = config.get("token", "")
    auth_url = build_auth_url(repo_url, token)

    if not (REPO_CACHE / ".git").exists():
        log(f"[INFO] 首次克隆仓库到 {REPO_CACHE} ...")
        REPO_CACHE.parent.mkdir(parents=True, exist_ok=True)
        code, out, err = run_git(["clone", auth_url, str(REPO_CACHE)], cwd=str(Path.home()))
        if code != 0:
            log(f"[ERROR] 克隆失败：{err}")
            log("请检查仓库 URL 和 Token 是否正确，以及仓库是否已有初始 commit。")
            sys.exit(1)
        log("[OK] 克隆成功")
    else:
        run_git(["remote", "set-url", "origin", auth_url], cwd=str(REPO_CACHE), silent=True)

    return REPO_CACHE

def get_current_branch(repo_dir: Path) -> str:
    code, out, _ = run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=str(repo_dir), silent=True)
    return out if (code == 0 and out) else "main"

def get_hostname() -> str:
    try:
        return platform.node() or "unknown"
    except Exception:
        return "unknown"


# ── 命令实现 ──────────────────────────────────────────────────

def cmd_setup(args: list):
    repo_url = None
    token    = None
    i = 0
    while i < len(args):
        if args[i] == "--repo" and i + 1 < len(args):
            repo_url = args[i + 1]; i += 2
        elif args[i] == "--token" and i + 1 < len(args):
            token = args[i + 1]; i += 2
        else:
            i += 1

    if not repo_url:
        log("请输入 GitHub 私有仓库 URL")
        log("示例：https://github.com/yourname/workbuddy-memory")
        repo_url = input("> ").strip()
    if not token:
        log("请输入 GitHub Personal Access Token（需要 repo 权限）")
        token = input("> ").strip()

    config = {"repo_url": repo_url, "token": token}
    save_config(config)

    log("\n[INFO] 正在验证连接...")
    ensure_repo(config)
    log(f"\n[OK] 配置完成！")
    log(f"  本地仓库缓存：{REPO_CACHE}")
    log(f"  工作区根目录：{get_workspace_root()}")
    log("\n现在可以运行：python memory_sync.py push")


def cmd_push(args: list):
    """将所有 memory 文件推送到 GitHub"""
    config   = load_config()
    repo_dir = ensure_repo(config)

    # 扫描所有 memory 目录
    all_dirs = scan_all_memory_dirs()
    if not all_dirs:
        log("[WARN] 未找到任何含 .md 文件的 memory 目录")
        return

    log(f"[INFO] 发现 {len(all_dirs)} 个 memory 目录，开始同步...")

    total_copied = 0
    for label, mem_dir in all_dirs.items():
        # 确定仓库中的目标目录
        if label == "__user__":
            dest = repo_dir / "memory"
        else:
            dest = repo_dir / "workspaces" / label
        dest.mkdir(parents=True, exist_ok=True)

        copied = 0
        for f in sorted(mem_dir.glob("*.md")):
            shutil.copy2(f, dest / f.name)
            copied += 1

        if copied > 0:
            ws_label = "用户级" if label == "__user__" else f"工作区 {label}"
            log(f"  {ws_label}: {copied} 个文件")
            total_copied += copied

    if total_copied == 0:
        log("[INFO] 没有文件需要同步")
        return

    # Git 提交推送
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname  = get_hostname()

    run_git(["add", "."], cwd=str(repo_dir))
    code, out, err = run_git(
        ["commit", "-m", f"sync: {timestamp} from {hostname} ({total_copied} files)"],
        cwd=str(repo_dir)
    )
    if code != 0 and "nothing to commit" in (out + err).lower():
        log("[OK] 内容无变化，无需推送")
        return

    branch = get_current_branch(repo_dir)
    code, out, err = run_git(["push", "origin", branch], cwd=str(repo_dir))
    if code != 0:
        code, out, err = run_git(
            ["push", "--set-upstream", "origin", branch],
            cwd=str(repo_dir)
        )

    if code == 0:
        log(f"\n[OK] 推送成功！共同步 {total_copied} 个文件（{len(all_dirs)} 个工作区）")
    else:
        log(f"[ERROR] 推送失败：{err}")
        sys.exit(1)


def cmd_pull(args: list):
    """从 GitHub 拉取最新 memory 文件到本地"""
    config   = load_config()
    repo_dir = ensure_repo(config)

    log("[INFO] 正在从 GitHub 拉取最新 memory...")
    branch = get_current_branch(repo_dir)
    code, out, err = run_git(["pull", "origin", branch], cwd=str(repo_dir))
    if code != 0:
        log(f"[WARN] 拉取遇到问题：{err}")
        log("如果是首次使用，请先在另一台设备执行 push。")
        return

    total_copied = 0

    # 还原用户级 memory
    src_user = repo_dir / "memory"
    if src_user.exists():
        dest_user = WORKBUDDY_DIR / "memory"
        dest_user.mkdir(parents=True, exist_ok=True)
        copied = _copy_newer(src_user, dest_user)
        if copied:
            log(f"  用户级 memory: {copied} 个文件已更新")
            total_copied += copied

    # 还原各工作区 memory
    src_ws = repo_dir / "workspaces"
    if src_ws.exists():
        ws_root = get_workspace_root()
        for ws_id_dir in sorted(src_ws.iterdir()):
            if not ws_id_dir.is_dir():
                continue
            ws_id = ws_id_dir.name
            dest = ws_root / ws_id / ".workbuddy" / "memory"

            # 仅还原已存在的工作区（避免在新设备创建大量空目录）
            # 若工作区不存在但用户明确指定了工作区根目录，则也还原
            ws_dir = ws_root / ws_id
            if not ws_dir.exists():
                continue  # 本机没有这个工作区，跳过

            dest.mkdir(parents=True, exist_ok=True)
            copied = _copy_newer(ws_id_dir, dest)
            if copied:
                log(f"  工作区 {ws_id}: {copied} 个文件已更新")
                total_copied += copied

    if total_copied > 0:
        log(f"\n[OK] 拉取完成！共更新 {total_copied} 个文件")
    else:
        log("[OK] 本地已是最新，无需更新")


def _copy_newer(src_dir: Path, dest_dir: Path) -> int:
    """将 src_dir 中比 dest_dir 更新的 .md 文件复制过去，返回复制数量"""
    copied = 0
    for f in sorted(src_dir.glob("*.md")):
        dest_file = dest_dir / f.name
        if dest_file.exists() and dest_file.stat().st_mtime >= f.stat().st_mtime:
            continue  # 本地更新，保留本地
        shutil.copy2(f, dest_file)
        copied += 1
    return copied


def cmd_status(args: list):
    """查看同步状态"""
    if not CONFIG_PATH.exists():
        log("[ERROR] 未配置，请先运行：python memory_sync.py setup")
        return

    config = load_config()
    log(f"仓库地址  : {config['repo_url']}")
    log(f"本地缓存  : {REPO_CACHE}")
    log(f"工作区根  : {get_workspace_root()}")
    log(f"运行平台  : {platform.system()} {platform.release()}")

    if (REPO_CACHE / ".git").exists():
        code, out, _ = run_git(["log", "--oneline", "-5"], cwd=str(REPO_CACHE), silent=True)
        if code == 0 and out:
            log("\n最近 5 次同步记录：")
            for line in out.split("\n"):
                log(f"  {line}")

    log("\n本地 memory 目录扫描：")
    all_dirs = scan_all_memory_dirs()
    if not all_dirs:
        log("  (未找到任何含 .md 文件的 memory 目录)")
    else:
        for label, mem_dir in all_dirs.items():
            files = sorted(mem_dir.glob("*.md"))
            ws_label = "用户级" if label == "__user__" else f"工作区 {label}"
            log(f"  [{ws_label}] {len(files)} 个文件  ({mem_dir})")


# ── 入口 ─────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd  = sys.argv[1].lower()
    rest = sys.argv[2:]

    commands = {
        "setup":  cmd_setup,
        "push":   cmd_push,
        "pull":   cmd_pull,
        "status": cmd_status,
    }

    if cmd not in commands:
        log(f"[ERROR] 未知命令：{cmd}")
        log(f"可用命令：{' / '.join(commands.keys())}")
        sys.exit(1)

    commands[cmd](rest)


if __name__ == "__main__":
    main()
