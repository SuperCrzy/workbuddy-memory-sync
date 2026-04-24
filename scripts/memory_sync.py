#!/usr/bin/env python3
"""
Universal AI Memory Sync — Cross-platform AI memory synchronization tool
通用 AI 记忆同步工具 — 跨平台跨设备同步 AI 记忆文件

Supported agents / 支持的 AI 平台:
  workbuddy   WorkBuddy (.workbuddy/memory/ + workspace scans)
  cursor      Cursor IDE (.cursor/rules, CLAUDE.md, .cursorrules)
  openclaw    OpenClaw (MEMORY.md, SOUL.md, USER.md, IDENTITY.md, AGENTS.md, memory/*.md)
  hermes      Hermes Agent (~/.hermes/memories/MEMORY.md, USER.md)
  windsurf    Windsurf (.windsurf/rules, MEMORY.md)
  generic     Any directory — pass --memory-dir explicitly
  all         Sync all detected agents at once

Usage / 用法:
  python memory_sync.py setup [--repo URL] [--token TOKEN]
  python memory_sync.py push  [--agent AGENT]
  python memory_sync.py pull  [--agent AGENT]
  python memory_sync.py status
  python memory_sync.py agents   # list detected agents on this machine

Project / 项目地址: https://github.com/SuperCrzy/AI-Memory-Sync
"""

import sys
import os
import json
import subprocess
import shutil
import platform
import locale
from pathlib import Path
from datetime import datetime

# ── Windows console UTF-8 fix ────────────────────────────────
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── Language Detection ──────────────────────────────────────
def get_language() -> str:
    """
    Detect display language.
    Reads AI_MEMORY_LANG env var first (e.g. 'en', 'zh', 'zh-CN').
    Falls back to system locale.
    Returns 'zh' for Chinese, 'en' for all others.
    """
    lang = os.environ.get("AI_MEMORY_LANG", "").lower()
    if lang in ("zh", "zh-cn", "zh_tw", "zh-hk"):
        return "zh"
    # Auto-detect from system locale
    try:
        loc = locale.getlocale()[0] or ""
        if loc.lower().startswith("zh"):
            return "zh"
    except Exception:
        pass
    return "en"


_LANG = get_language()

# ── i18n Translations ────────────────────────────────────────
_MSGS = {
    "en": {
        # Config
        "no_config":        "[ERROR] No config found. Please run setup first:",
        "no_config_hint":   "  python memory_sync.py setup --repo <URL> --token <TOKEN>",
        "config_saved":     "[OK] Config saved to {path}",
        # Setup
        "setup_repo_prompt":"Enter your GitHub private repo URL",
        "setup_repo_hint":  "Example: https://github.com/yourname/ai-memory",
        "setup_token_prompt":"Enter your GitHub Personal Access Token (needs 'repo' scope)",
        "setup_verifying":  "[INFO] Verifying connection...",
        "setup_done":       "[OK] Setup complete!",
        "setup_cache":      "  Local repo cache : {path}",
        "setup_workspace":  "  Workspace root   : {path}",
        "setup_hint":       "Run: python memory_sync.py push",
        # Ensure repo
        "cloning":          "[INFO] Cloning repo to {path} ...",
        "clone_failed":      "[ERROR] Clone failed: {err}",
        "clone_check":      "Check your repo URL and Token, and ensure the repo has at least one commit.",
        "clone_ok":         "[OK] Clone successful",
        # Push
        "push_scanning":    "[INFO] Syncing agent={agent}, found {n} source(s)...",
        "push_no_memory":   "[WARN] No memory directories found for agent: {agent}",
        "push_files":      "  {key}: {n} file(s)",
        "push_nothing":     "[INFO] Nothing to sync",
        "push_no_changes":  "[OK] No changes since last sync",
        "push_success":     "[OK] Push successful! Synced {n} file(s) from {m} source(s)",
        "push_failed":      "[ERROR] Push failed: {err}",
        # Pull
        "pull_fetching":    "[INFO] Pulling latest memory from GitHub (agent={agent})...",
        "pull_warn":        "[WARN] Pull issue: {err}",
        "pull_first_hint":  "If this is the first use, push from another device first.",
        "pull_no_data":     "[INFO] No synced data found in repo yet.",
        "pull_updated":      "  {key}: {n} file(s) updated",
        "pull_done":        "[OK] Pull complete! Updated {n} file(s)",
        "pull_up_to_date":  "[OK] Already up to date",
        # Agents
        "agents_scanning":  "[INFO] Scanning for AI agents on this machine...\n",
        "agents_none":      "  No agent memory directories detected.",
        "agents_section":   "\n[{agent}]",
        "agents_dir":       "  {key}: {n} .md file(s)  ({path})",
        "agents_file":      "  {key}: 1 file  ({path})",
        # Status
        "status_repo":      "Repo URL    : {url}",
        "status_cache":     "Local cache : {path}",
        "status_platform":  "Platform    : {platform}",
        "status_hostname":  "Hostname    : {name}",
        "status_last":      "\nLast 5 syncs:",
        "status_sources":   "\nDetected memory sources:",
        "status_none":      "  (none found)",
        "status_sources_detail": "  {key}: {n} file(s)  ({path})",
        "status_sources_file":  "  {key}: 1 file  ({path})",
        # Generic / warnings
        "generic_warn":     "[WARN] --agent generic requires MEMORY_DIR env var to be set.",
        "generic_hint":     "  Example: MEMORY_DIR=/path/to/memory python memory_sync.py push --agent generic",
        # Main
        "unknown_cmd":      "[ERROR] Unknown command: {cmd}",
        "available":        "Available: {cmds}",
    },
    "zh": {
        # Config
        "no_config":        "[错误] 未找到配置文件。请先运行 setup：",
        "no_config_hint":   "  python memory_sync.py setup --repo <URL> --token <TOKEN>",
        "config_saved":     "[OK] 配置已保存至 {path}",
        # Setup
        "setup_repo_prompt":"请输入 GitHub 私有仓库 URL",
        "setup_repo_hint":  "示例：https://github.com/yourname/ai-memory",
        "setup_token_prompt":"请输入 GitHub Personal Access Token（需具备 repo 权限）",
        "setup_verifying":  "[信息] 正在验证连接...",
        "setup_done":       "[OK] 配置完成！",
        "setup_cache":      "  本地仓库缓存 : {path}",
        "setup_workspace":  "  工作区根目录   : {path}",
        "setup_hint":       "运行：python memory_sync.py push",
        # Ensure repo
        "cloning":          "[信息] 正在克隆仓库至 {path} ...",
        "clone_failed":      "[错误] 克隆失败：{err}",
        "clone_check":      "请检查仓库 URL 和 Token，并确保仓库至少有一个提交。",
        "clone_ok":         "[OK] 克隆成功",
        # Push
        "push_scanning":    "[信息] 正在同步 agent={agent}，发现 {n} 个源...",
        "push_no_memory":   "[警告] 未找到 agent={agent} 的记忆目录",
        "push_files":       "  {key}: {n} 个文件",
        "push_nothing":      "[信息] 无需同步",
        "push_no_changes":  "[OK] 自上次同步以来无变化",
        "push_success":      "[OK] 推送成功！已同步 {n} 个文件，来自 {m} 个源",
        "push_failed":      "[错误] 推送失败：{err}",
        # Pull
        "pull_fetching":    "[信息] 正在从 GitHub 拉取最新记忆 (agent={agent})...",
        "pull_warn":        "[警告] 拉取异常：{err}",
        "pull_first_hint":  "如果这是首次使用，请先在另一台设备执行推送。",
        "pull_no_data":     "[信息] 仓库中尚未发现同步数据。",
        "pull_updated":      "  {key}: 更新了 {n} 个文件",
        "pull_done":        "[OK] 拉取完成！已更新 {n} 个文件",
        "pull_up_to_date":  "[OK] 已是最新",
        # Agents
        "agents_scanning":  "[信息] 正在扫描本机 AI 平台...\n",
        "agents_none":      "  未检测到任何 AI 平台的记忆目录。",
        "agents_section":   "\n【{agent}】",
        "agents_dir":       "  {key}: {n} 个 .md 文件  ({path})",
        "agents_file":      "  {key}: 1 个文件  ({path})",
        # Status
        "status_repo":      "仓库 URL   : {url}",
        "status_cache":     "本地缓存   : {path}",
        "status_platform":  "平台       : {platform}",
        "status_hostname":  "主机名     : {name}",
        "status_last":      "\n最近 5 次同步：",
        "status_sources":   "\n检测到的记忆源：",
        "status_none":      "  （未找到）",
        "status_sources_detail": "  {key}: {n} 个文件  ({path})",
        "status_sources_file":  "  {key}: 1 个文件  ({path})",
        # Generic / warnings
        "generic_warn":     "[警告] --agent generic 需要设置 MEMORY_DIR 环境变量。",
        "generic_hint":     "  示例：MEMORY_DIR=/path/to/memory python memory_sync.py push --agent generic",
        # Main
        "unknown_cmd":      "[错误] 未知命令：{cmd}",
        "available":        "可用命令：{cmds}",
    }
}


def T(msg_key: str, **kwargs) -> str:
    """Return translated string for current language."""
    return _MSGS[_LANG].get(msg_key, _MSGS["en"].get(msg_key, msg_key)).format(**kwargs)


# ── Global paths (all dynamic, no hardcoding) ────────────────
HOME           = Path.home()
AI_MEMORY_DIR  = HOME / ".ai-memory"
CONFIG_PATH    = AI_MEMORY_DIR / "config.json"
REPO_CACHE     = AI_MEMORY_DIR / "repo-cache"

# ── Agent definitions ────────────────────────────────────────

def get_workspace_root() -> Path:
    """Detect workspace root directory."""
    env = os.environ.get("AI_MEMORY_WORKSPACE_ROOT")
    if env:
        return Path(env)
    candidates = [
        HOME / "WorkBuddy",
        HOME / "workbuddy",
        Path("C:/Users") / os.environ.get("USERNAME", "user") / "WorkBuddy",
    ]
    for c in candidates:
        if c.exists():
            return c
    return HOME / "WorkBuddy"


def discover_agent_dirs(agent: str) -> dict:
    """
    Return {repo_subpath: local_path} for the given agent name.
    repo_subpath is where files land in the GitHub repo.
    """
    result = {}

    if agent in ("workbuddy", "all"):
        # User-level memory
        user_mem = AI_MEMORY_DIR / "memory" / "workbuddy"
        if user_mem.exists() and list(user_mem.glob("*.md")):
            result["agents/workbuddy/__user__"] = user_mem
        # Workspace-level memory
        ws_root = get_workspace_root()
        if ws_root.exists():
            for ws_dir in sorted(ws_root.iterdir()):
                if not ws_dir.is_dir():
                    continue
                mem_path = ws_dir / ".workbuddy" / "memory"
                if mem_path.exists() and list(mem_path.glob("*.md")):
                    result[f"agents/workbuddy/workspaces/{ws_dir.name}"] = mem_path

    if agent in ("cursor", "all"):
        # .cursor/rules directory
        cursor_rules = HOME / ".cursor" / "rules"
        if cursor_rules.exists() and list(cursor_rules.glob("*")):
            result["agents/cursor/rules"] = cursor_rules
        # Project-level CLAUDE.md / .cursorrules (scan common project dirs)
        for proj_root in [HOME / "projects", HOME / "code", HOME / "dev", HOME / "Documents"]:
            if proj_root.exists():
                for proj in list(proj_root.iterdir())[:20]:
                    if not proj.is_dir():
                        continue
                    for fname in ["CLAUDE.md", ".cursorrules", "CURSOR.md"]:
                        f = proj / fname
                        if f.exists():
                            result[f"agents/cursor/projects/{proj.name}/{fname}"] = f

    if agent in ("openclaw", "all"):
        # OpenClaw standard workspace (~/.openclaw/workspace/)
        oc_workspace = HOME / ".openclaw" / "workspace"
        if oc_workspace.exists():
            core_files = [
                "MEMORY.md", "SOUL.md", "USER.md", "IDENTITY.md",
                "AGENTS.md", "BOOT.md", "HEARTBEAT.md", "DREAMS.md",
            ]
            found = {}
            for fname in core_files:
                f = oc_workspace / fname
                if f.exists():
                    found[fname] = f
            mem_dir = oc_workspace / "memory"
            if mem_dir.exists() and list(mem_dir.glob("*.md")):
                found["memory/"] = mem_dir
            if found:
                for fname, fpath in found.items():
                    key = f"agents/openclaw/workspace/{fname}" if fname != "memory/" else "agents/openclaw/workspace/memory/"
                    result[key] = fpath
        # OpenClaw per-agent state dirs (~/.openclaw/agents/<cid>/)
        oc_agents_root = HOME / ".openclaw" / "agents"
        if oc_agents_root.exists():
            for cid_dir in list(oc_agents_root.iterdir())[:20]:
                if not cid_dir.is_dir():
                    continue
                agent_found = {}
                for fname in ["MEMORY.md", "SOUL.md", "USER.md", "IDENTITY.md", "AGENTS.md"]:
                    f = cid_dir / fname
                    if f.exists():
                        agent_found[fname] = f
                mem_dir = cid_dir / "memory"
                if mem_dir.exists() and list(mem_dir.glob("*.md")):
                    agent_found["memory/"] = mem_dir
                if agent_found:
                    for fname, fpath in agent_found.items():
                        key = f"agents/openclaw/agents/{cid_dir.name}/{fname}" if fname != "memory/" else f"agents/openclaw/agents/{cid_dir.name}/memory/"
                        result[key] = fpath
        # Workspace-level OpenClaw files (in project dirs)
        for search_root in [HOME / "WorkBuddy", HOME / "projects", HOME / "code", HOME]:
            if not search_root.exists():
                continue
            for subdir in list(search_root.iterdir())[:30]:
                if not subdir.is_dir():
                    continue
                collected = {}
                for fname in ["MEMORY.md", "SOUL.md", "USER.md", "IDENTITY.md", "AGENTS.md", "TOOLS.md"]:
                    f = subdir / fname
                    if f.exists():
                        collected[fname] = f
                mem_dir = subdir / "memory"
                if mem_dir.exists() and list(mem_dir.glob("*.md")):
                    collected["memory/"] = mem_dir
                if len(collected) >= 3:  # require 3+ files to confirm it's an OpenClaw project
                    for fname, fpath in collected.items():
                        key = f"agents/openclaw/projects/{subdir.name}/{fname}" if fname != "memory/" else f"agents/openclaw/projects/{subdir.name}/memory/"
                        result[key] = fpath

    if agent in ("hermes", "all"):
        # Hermes standard memories directory (~/.hermes/memories/)
        hm_memories = HOME / ".hermes" / "memories"
        if hm_memories.exists():
            for fname in ["MEMORY.md", "USER.md"]:
                f = hm_memories / fname
                if f.exists():
                    result[f"agents/hermes/memories/{fname}"] = f
        # Also sync the state DB as a blob (optional but useful)
        hm_state = HOME / ".hermes" / "state.db"
        if hm_state.exists():
            result["agents/hermes/state.db"] = hm_state

    if agent in ("windsurf", "all"):
        ws_rules = HOME / ".windsurf" / "rules"
        if ws_rules.exists():
            result["agents/windsurf/rules"] = ws_rules
        ws_mem = HOME / ".windsurf" / "memory"
        if ws_mem.exists() and list(ws_mem.glob("*.md")):
            result["agents/windsurf/memory"] = ws_mem

    if agent == "generic":
        mem_dir_env = os.environ.get("MEMORY_DIR") or os.environ.get("AI_MEMORY_DIR_ENV")
        if mem_dir_env:
            p = Path(mem_dir_env)
            if p.exists():
                result["agents/generic/memory"] = p
        else:
            log(T("generic_warn"))
            log(T("generic_hint"))

    return result


# ── Utilities ────────────────────────────────────────────────

def log(msg: str):
    print(msg, flush=True)

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        log(T("no_config"))
        log(T("no_config_hint"))
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config: dict):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    log(T("config_saved", path=CONFIG_PATH))

def build_auth_url(repo_url: str, token: str) -> str:
    if "github.com" in repo_url and token:
        return repo_url.replace("https://", f"https://{token}@")
    return repo_url

def run_git(args: list, cwd: str, silent: bool = False) -> tuple:
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
        log(T("cloning", path=REPO_CACHE))
        REPO_CACHE.parent.mkdir(parents=True, exist_ok=True)
        code, out, err = run_git(["clone", auth_url, str(REPO_CACHE)], cwd=str(HOME))
        if code != 0:
            log(T("clone_failed", err=err))
            log(T("clone_check"))
            sys.exit(1)
        log(T("clone_ok"))
    else:
        run_git(["remote", "set-url", "origin", auth_url], cwd=str(REPO_CACHE), silent=True)

    return REPO_CACHE

def get_current_branch(repo_dir: Path) -> str:
    code, out, _ = run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=str(repo_dir))
    return out if (code == 0 and out) else "main"

def get_hostname() -> str:
    try:
        return platform.node() or "unknown"
    except Exception:
        return "unknown"

def parse_args(args: list) -> dict:
    """Simple key-value arg parser: --key value"""
    parsed = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--") and i + 1 < len(args):
            parsed[args[i][2:]] = args[i + 1]
            i += 2
        else:
            parsed[f"_pos_{i}"] = args[i]
            i += 1
    return parsed


# ── Commands ─────────────────────────────────────────────────

def cmd_setup(args: list):
    p = parse_args(args)
    repo_url = p.get("repo")
    token    = p.get("token")

    if not repo_url:
        log(T("setup_repo_prompt"))
        log(T("setup_repo_hint"))
        repo_url = input("> ").strip()
    if not token:
        log(T("setup_token_prompt"))
        token = input("> ").strip()

    config = {"repo_url": repo_url, "token": token}
    save_config(config)

    log("\n" + T("setup_verifying"))
    ensure_repo(config)
    log("\n" + T("setup_done"))
    log(T("setup_cache", path=REPO_CACHE))
    log(T("setup_workspace", path=get_workspace_root()))
    log("\n" + T("setup_hint"))


def _copy_dir_to_repo(src_dir: Path, dest_dir: Path) -> int:
    """Copy all .md files from src_dir to dest_dir. Returns count."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    for f in sorted(src_dir.glob("*.md")):
        shutil.copy2(f, dest_dir / f.name)
        copied += 1
    return copied

def _copy_file_to_repo(src_file: Path, dest_dir: Path) -> int:
    """Copy a single file to dest_dir. Returns 1 if copied."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_file, dest_dir / src_file.name)
    return 1


def cmd_push(args: list):
    p = parse_args(args)
    agent    = p.get("agent", "workbuddy")
    config   = load_config()
    repo_dir = ensure_repo(config)

    agent_dirs = discover_agent_dirs(agent)
    if not agent_dirs:
        log(T("push_no_memory", agent=agent))
        return

    log(T("push_scanning", agent=agent, n=len(agent_dirs)))

    total_copied = 0
    for repo_key, local_path in agent_dirs.items():
        dest = repo_dir / repo_key
        if local_path.is_dir():
            copied = _copy_dir_to_repo(local_path, dest)
        else:
            copied = _copy_file_to_repo(local_path, dest.parent)
        if copied > 0:
            log(T("push_files", key=repo_key, n=copied))
            total_copied += copied

    if total_copied == 0:
        log(T("push_nothing"))
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname  = get_hostname()

    run_git(["add", "."], cwd=str(repo_dir))
    code, out, err = run_git(
        ["commit", "-m", f"sync({agent}): {timestamp} from {hostname} ({total_copied} files)"],
        cwd=str(repo_dir)
    )
    if code != 0 and "nothing to commit" in (out + err).lower():
        log(T("push_no_changes"))
        return

    branch = get_current_branch(repo_dir)
    code, out, err = run_git(["push", "origin", branch], cwd=str(repo_dir))
    if code != 0:
        code, out, err = run_git(["push", "--set-upstream", "origin", branch], cwd=str(repo_dir))

    if code == 0:
        log("\n" + T("push_success", n=total_copied, m=len(agent_dirs)))
    else:
        log(T("push_failed", err=err))
        sys.exit(1)


def _copy_newer(src_dir: Path, dest_dir: Path) -> int:
    """Copy files from src to dest only if src is newer. Returns count."""
    copied = 0
    for f in sorted(src_dir.glob("*.md")):
        dest_file = dest_dir / f.name
        if dest_file.exists() and dest_file.stat().st_mtime >= f.stat().st_mtime:
            continue
        shutil.copy2(f, dest_file)
        copied += 1
    return copied


def cmd_pull(args: list):
    p = parse_args(args)
    agent    = p.get("agent", "workbuddy")
    config   = load_config()
    repo_dir = ensure_repo(config)

    log(T("pull_fetching", agent=agent))
    branch = get_current_branch(repo_dir)
    code, out, err = run_git(["pull", "origin", branch], cwd=str(repo_dir))
    if code != 0:
        log(T("pull_warn", err=err))
        log(T("pull_first_hint"))
        return

    total_copied = 0
    agents_dir = repo_dir / "agents"
    if not agents_dir.exists():
        log(T("pull_no_data"))
        return

    if agent == "all":
        scan_agents = [d.name for d in agents_dir.iterdir() if d.is_dir()]
    else:
        scan_agents = [agent]

    for ag in scan_agents:
        ag_dir = agents_dir / ag
        if not ag_dir.exists():
            continue

        if ag == "workbuddy":
            # User-level
            src_user = ag_dir / "__user__"
            if src_user.exists():
                dest = AI_MEMORY_DIR / "memory" / "workbuddy"
                dest.mkdir(parents=True, exist_ok=True)
                copied = _copy_newer(src_user, dest)
                if copied:
                    log(T("pull_updated", key="workbuddy/__user__", n=copied))
                    total_copied += copied
            # Workspace-level
            ws_src = ag_dir / "workspaces"
            if ws_src.exists():
                ws_root = get_workspace_root()
                for ws_id_dir in sorted(ws_src.iterdir()):
                    if not ws_id_dir.is_dir():
                        continue
                    ws_dest = ws_root / ws_id_dir.name / ".workbuddy" / "memory"
                    if not (ws_root / ws_id_dir.name).exists():
                        continue
                    ws_dest.mkdir(parents=True, exist_ok=True)
                    copied = _copy_newer(ws_id_dir, ws_dest)
                    if copied:
                        log(T("pull_updated", key=f"workbuddy/workspaces/{ws_id_dir.name}", n=copied))
                        total_copied += copied

        elif ag == "cursor":
            rules_src = ag_dir / "rules"
            if rules_src.exists():
                dest = HOME / ".cursor" / "rules"
                dest.mkdir(parents=True, exist_ok=True)
                for f in rules_src.glob("*"):
                    shutil.copy2(f, dest / f.name)
                    total_copied += 1
                    log(T("pull_updated", key=f"cursor/rules/{f.name}", n=1))

        elif ag == "openclaw":
            oc_ws_src = ag_dir / "workspace"
            if oc_ws_src.exists():
                oc_ws_dest = HOME / ".openclaw" / "workspace"
                oc_ws_dest.mkdir(parents=True, exist_ok=True)
                for f in oc_ws_src.rglob("*"):
                    if f.is_file() and (f.suffix == ".md" or f.suffix == ""):
                        rel = f.relative_to(oc_ws_src)
                        dest_file = oc_ws_dest / rel
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        if not dest_file.exists() or dest_file.stat().st_mtime < f.stat().st_mtime:
                            shutil.copy2(f, dest_file)
                            log(T("pull_updated", key=f"openclaw/workspace/{rel}", n=1))
                            total_copied += 1
            oc_agents_src = ag_dir / "agents"
            if oc_agents_src.exists():
                oc_agents_dest = HOME / ".openclaw" / "agents"
                for cid_dir in oc_agents_src.iterdir():
                    if not cid_dir.is_dir():
                        continue
                    cid_dest = oc_agents_dest / cid_dir.name
                    cid_dest.mkdir(parents=True, exist_ok=True)
                    for f in cid_dir.rglob("*"):
                        if f.is_file():
                            rel = f.relative_to(cid_dir)
                            dest_file = cid_dest / rel
                            dest_file.parent.mkdir(parents=True, exist_ok=True)
                            if not dest_file.exists() or dest_file.stat().st_mtime < f.stat().st_mtime:
                                shutil.copy2(f, dest_file)
                                log(T("pull_updated", key=f"openclaw/agents/{cid_dir.name}/{rel}", n=1))
                                total_copied += 1

        elif ag == "hermes":
            hm_src = ag_dir / "memories"
            if hm_src.exists():
                hm_dest = HOME / ".hermes" / "memories"
                hm_dest.mkdir(parents=True, exist_ok=True)
                for f in hm_src.glob("*.md"):
                    if not f.exists() or f.stat().st_mtime < hm_src.stat().st_mtime:
                        shutil.copy2(f, hm_dest / f.name)
                        log(T("pull_updated", key=f"hermes/memories/{f.name}", n=1))
                        total_copied += 1
            state_src = ag_dir / "state.db"
            if state_src.exists():
                state_dest = HOME / ".hermes" / "state.db"
                shutil.copy2(state_src, state_dest)
                log(T("pull_updated", key="hermes/state.db", n=1))
                total_copied += 1

        elif ag == "windsurf":
            ws_src = ag_dir / "rules"
            if ws_src.exists():
                dest = HOME / ".windsurf" / "rules"
                dest.mkdir(parents=True, exist_ok=True)
                for f in ws_src.glob("*"):
                    if not f.exists() or f.stat().st_mtime < ws_src.stat().st_mtime:
                        shutil.copy2(f, dest / f.name)
                        log(T("pull_updated", key=f"windsurf/rules/{f.name}", n=1))
                        total_copied += 1
            ws_mem_src = ag_dir / "memory"
            if ws_mem_src.exists():
                dest = HOME / ".windsurf" / "memory"
                dest.mkdir(parents=True, exist_ok=True)
                for f in ws_mem_src.glob("*.md"):
                    shutil.copy2(f, dest / f.name)
                    log(T("pull_updated", key=f"windsurf/memory/{f.name}", n=1))
                    total_copied += 1

        elif ag == "generic":
            for item in ag_dir.rglob("*.md"):
                rel = item.relative_to(ag_dir)
                dest_file = HOME / ".ai-memory" / ag / rel
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                if not dest_file.exists() or dest_file.stat().st_mtime < item.stat().st_mtime:
                    shutil.copy2(item, dest_file)
                    log(T("pull_updated", key=f"generic/{rel}", n=1))
                    total_copied += 1

    if total_copied > 0:
        log("\n" + T("pull_done", n=total_copied))
    else:
        log(T("pull_up_to_date"))


def cmd_agents(args: list):
    """List all detected agents and their memory directories on this machine."""
    log(T("agents_scanning"))
    all_dirs = discover_agent_dirs("all")
    if not all_dirs:
        log(T("agents_none"))
        return
    current_prefix = ""
    for repo_key, local_path in sorted(all_dirs.items()):
        agent_name = repo_key.split("/")[1]
        if agent_name != current_prefix:
            log(T("agents_section", agent=agent_name.upper()))
            current_prefix = agent_name
        if local_path.is_dir():
            files = list(local_path.glob("*.md"))
            log(T("agents_dir", key=repo_key.split("/", 2)[-1], n=len(files), path=local_path))
        else:
            log(T("agents_file", key=repo_key.split("/", 2)[-1], path=local_path))


def cmd_status(args: list):
    if not CONFIG_PATH.exists():
        log("[ERROR] Not configured. Run: python memory_sync.py setup")
        return

    config = load_config()
    log(T("status_repo", url=config["repo_url"]))
    log(T("status_cache", path=REPO_CACHE))
    log(T("status_platform", platform=f"{platform.system()} {platform.release()}"))
    log(T("status_hostname", name=get_hostname()))

    if (REPO_CACHE / ".git").exists():
        code, out, _ = run_git(["log", "--oneline", "-5"], cwd=str(REPO_CACHE))
        if code == 0 and out:
            log(T("status_last"))
            for line in out.split("\n"):
                log(f"  {line}")

    log(T("status_sources"))
    all_dirs = discover_agent_dirs("all")
    if not all_dirs:
        log(T("status_none"))
    else:
        for repo_key, local_path in sorted(all_dirs.items()):
            if local_path.is_dir():
                files = list(local_path.glob("*.md"))
                log(T("status_sources_detail", key=repo_key, n=len(files), path=local_path))
            else:
                log(T("status_sources_file", key=repo_key, path=local_path))


# ── Entry point ───────────────────────────────────────────────

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
        "agents": cmd_agents,
    }

    if cmd not in commands:
        log(T("unknown_cmd", cmd=cmd))
        log(T("available", cmds=" / ".join(commands.keys())))
        sys.exit(1)

    commands[cmd](rest)


if __name__ == "__main__":
    main()
