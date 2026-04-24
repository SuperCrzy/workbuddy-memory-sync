#!/usr/bin/env python3
"""
WorkBuddy Memory Sync - 跨设备记忆同步工具
将 WorkBuddy 的 Memory 文件同步到 GitHub 私有仓库，实现多设备共享 AI 记忆上下文。

用法:
  python memory_sync.py setup                        # 交互式初始化配置
  python memory_sync.py setup --repo URL --token TOKEN  # 直接配置
  python memory_sync.py push                         # 推送记忆到 GitHub
  python memory_sync.py pull                         # 从 GitHub 拉取记忆
  python memory_sync.py status                       # 查看同步状态

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
WORKBUDDY_DIR = Path.home() / ".workbuddy"
CONFIG_PATH   = WORKBUDDY_DIR / "memory-sync-config.json"
REPO_CACHE    = WORKBUDDY_DIR / "memory-sync-repo"

# WorkBuddy memory 目录：优先使用环境变量覆盖
def get_default_memory_dirs() -> list[Path]:
    """
    返回所有候选 memory 目录。
    支持通过环境变量 WORKBUDDY_MEMORY_DIR 自定义。
    """
    dirs = []

    # 环境变量覆盖
    env_dir = os.environ.get("WORKBUDDY_MEMORY_DIR")
    if env_dir:
        dirs.append(Path(env_dir))

    # 用户级默认目录
    dirs.append(WORKBUDDY_DIR / "memory")

    # 过滤出实际存在的目录
    return [d for d in dirs if d.exists()]


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
    """将 Token 嵌入 HTTPS URL 用于认证（不写入任何文件）"""
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
    if not silent and result.returncode != 0:
        pass  # 由调用方决定如何处理
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def ensure_repo(config: dict) -> Path:
    """确保本地 Git 仓库已克隆，否则执行克隆"""
    repo_url  = config["repo_url"]
    token     = config.get("token", "")
    auth_url  = build_auth_url(repo_url, token)

    if not (REPO_CACHE / ".git").exists():
        log(f"[INFO] 首次克隆仓库到 {REPO_CACHE} ...")
        REPO_CACHE.parent.mkdir(parents=True, exist_ok=True)
        code, out, err = run_git(["clone", auth_url, str(REPO_CACHE)], cwd=str(Path.home()))
        if code != 0:
            log(f"[ERROR] 克隆失败：{err}")
            log("请检查仓库 URL 和 Token 是否正确，以及仓库是否为空（需至少有一次 commit）。")
            sys.exit(1)
        log("[OK] 克隆成功")
    else:
        # 更新 remote URL（Token 可能已变化）
        run_git(["remote", "set-url", "origin", auth_url], cwd=str(REPO_CACHE), silent=True)

    return REPO_CACHE

def get_current_branch(repo_dir: Path) -> str:
    """获取当前默认分支名（main 或 master）"""
    code, out, _ = run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=str(repo_dir), silent=True)
    if code == 0 and out:
        return out
    return "main"

def get_hostname() -> str:
    try:
        return platform.node() or "unknown"
    except Exception:
        return "unknown"


# ── 命令实现 ──────────────────────────────────────────────────

def cmd_setup(args: list):
    """交互式或参数化初始化配置"""
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
        log("获取方式：GitHub -> Settings -> Developer settings -> Personal access tokens")
        token = input("> ").strip()

    config = {"repo_url": repo_url, "token": token}
    save_config(config)

    log("\n[INFO] 正在验证连接...")
    ensure_repo(config)
    log(f"\n[OK] 配置完成！本地仓库缓存：{REPO_CACHE}")
    log("现在可以运行：python memory_sync.py push")


def cmd_push(args: list):
    """将本地 memory 文件推送到 GitHub"""
    config   = load_config()
    repo_dir = ensure_repo(config)

    # 确定要同步的 memory 目录
    if args:
        memory_dirs = [Path(args[0])]
        memory_dirs = [d for d in memory_dirs if d.exists()]
    else:
        memory_dirs = get_default_memory_dirs()

    if not memory_dirs:
        log("[WARN] 未找到任何 memory 目录，请通过 WORKBUDDY_MEMORY_DIR 环境变量指定路径")
        return

    # 复制文件到仓库目录
    dest = repo_dir / "memory"
    dest.mkdir(exist_ok=True)

    copied = 0
    for mem_dir in memory_dirs:
        for f in sorted(mem_dir.glob("*.md")):
            shutil.copy2(f, dest / f.name)
            copied += 1

    if copied == 0:
        log("[INFO] 没有 memory 文件需要同步")
        return

    log(f"[INFO] 共找到 {copied} 个文件，正在推送...")

    # Git 提交
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname  = get_hostname()

    run_git(["add", "."], cwd=str(repo_dir))
    code, out, err = run_git(
        ["commit", "-m", f"sync: {timestamp} from {hostname}"],
        cwd=str(repo_dir)
    )
    if code != 0 and "nothing to commit" in (out + err).lower():
        log("[OK] 内容无变化，无需推送")
        return

    # 推送
    branch = get_current_branch(repo_dir)
    code, out, err = run_git(["push", "origin", branch], cwd=str(repo_dir))
    if code != 0:
        # 尝试设置上游分支后再推
        code, out, err = run_git(
            ["push", "--set-upstream", "origin", branch],
            cwd=str(repo_dir)
        )

    if code == 0:
        log(f"[OK] 推送成功！{copied} 个文件已同步到 GitHub ({branch})")
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
        log("如果是首次使用，仓库可能为空，请先在另一台设备执行 push。")
        return

    # 确定目标 memory 目录
    if args:
        target_dirs = [Path(args[0])]
    else:
        target_dirs = get_default_memory_dirs()
        if not target_dirs:
            # 目录不存在则自动创建
            default = WORKBUDDY_DIR / "memory"
            default.mkdir(parents=True, exist_ok=True)
            target_dirs = [default]

    src = repo_dir / "memory"
    if not src.exists() or not list(src.glob("*.md")):
        log("[INFO] 仓库中暂无 memory 文件，请先在另一台设备执行 push。")
        return

    copied = 0
    for f in sorted(src.glob("*.md")):
        for target in target_dirs:
            dest_file = target / f.name
            # 冲突策略：以最新修改时间为准
            if dest_file.exists():
                if dest_file.stat().st_mtime >= f.stat().st_mtime:
                    continue  # 本地更新，保留本地
            shutil.copy2(f, dest_file)
            copied += 1

    if copied > 0:
        log(f"[OK] 拉取完成！{copied} 个文件已更新到本地")
    else:
        log("[OK] 本地已是最新，无需更新")


def cmd_status(args: list):
    """查看同步状态"""
    if not CONFIG_PATH.exists():
        log("[ERROR] 未配置，请先运行：python memory_sync.py setup")
        return

    config = load_config()
    log(f"仓库地址  : {config['repo_url']}")
    log(f"本地缓存  : {REPO_CACHE}")
    log(f"配置文件  : {CONFIG_PATH}")
    log(f"运行平台  : {platform.system()} {platform.release()}")

    if (REPO_CACHE / ".git").exists():
        code, out, _ = run_git(["log", "--oneline", "-5"], cwd=str(REPO_CACHE), silent=True)
        if code == 0 and out:
            log("\n最近 5 次同步记录：")
            for line in out.split("\n"):
                log(f"  {line}")
    else:
        log("\n[WARN] 本地仓库未初始化，请先运行 push 或 pull")

    log("\n本地 memory 文件：")
    for mem_dir in get_default_memory_dirs():
        files = sorted(mem_dir.glob("*.md"))
        log(f"  目录: {mem_dir}  ({len(files)} 个文件)")
        for f in files:
            size  = f.stat().st_size
            mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            log(f"    {f.name:<30} {size:>6} bytes  {mtime}")


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
