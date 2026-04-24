#!/usr/bin/env python3
"""Generate a terminal animation GIF demo for Universal AI Memory Sync."""

import os
import sys
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── Colors ───────────────────────────────────────────────────
BG_COLOR       = (30, 30, 30)
BAR_COLOR      = (50, 50, 55)
BAR_BTN_RED    = (255, 95, 86)
BAR_BTN_YEL    = (255, 189, 46)
BAR_BTN_GRN    = (39, 201, 63)
TEXT_COLOR     = (200, 200, 200)
TEXT_GREEN     = (78, 201, 176)
TEXT_BLUE      = (88, 166, 255)
TEXT_WHITE     = (240, 240, 240)
TEXT_YELLOW    = (255, 220, 90)
TEXT_OK        = (78, 201, 176)
TEXT_WARN      = (255, 200, 80)
TEXT_ERROR     = (255, 90, 90)
TEXT_CURSOR    = (200, 200, 200)
MARGIN         = 20
LINE_H         = 26
TITLE_H        = 36
PAD_TOP        = TITLE_H + 14

WIDTH  = 760
HEIGHT = 520

FONT_SIZE = 15


def load_font(size: int = FONT_SIZE):
    candidates = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/cour.ttf",
        "C:/Windows/Fonts/lucon.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/System/Library/Fonts/Monaco.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


FONT = load_font(FONT_SIZE)


def parse_line(line: str) -> list:
    """Parse a line into (text, color) segments."""
    parts = []
    remaining = line

    tag_map = [
        ("[ERROR]", TEXT_ERROR),
        ("[WARN]",  TEXT_WARN),
        ("[OK]",    TEXT_OK),
        ("[INFO]",  TEXT_YELLOW),
        ("[信息]",  TEXT_YELLOW),
        ("[错误]",  TEXT_ERROR),
        ("[警告]",  TEXT_WARN),
    ]

    for tag, color in tag_map:
        if tag in remaining:
            idx = remaining.index(tag)
            before = remaining[:idx]
            after  = remaining[idx + len(tag):]
            if before:
                parts += parse_plain_text(before)
            parts.append((tag, color))
            if after:
                parts += parse_plain_text(after)
            return [(t, c) for t, c in parts if t]

    return parse_plain_text(line)


def parse_plain_text(text: str) -> list:
    if not text:
        return []
    result = []
    # Highlight prompt
    m = re.match(r'^(\$\s*|>|.*?\$\s)(.*)$', text)
    if m:
        if m.group(1):
            result.append((m.group(1), TEXT_GREEN))
        if m.group(2):
            result.append((m.group(2), TEXT_WHITE))
    else:
        result.append((text, TEXT_WHITE))
    return [(t, c) for t, c in result if t]


def draw_text(draw, pos, text, font, color):
    try:
        draw.text(pos, text, font=font, fill=color)
    except Exception:
        draw.text(pos, text, fill=color)


def text_length(draw, text, font):
    try:
        return draw.textlength(text, font=font)
    except Exception:
        return len(text) * 9


def draw_terminal(lines: list, cursor_visible: bool = True):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Background
    draw.rectangle([0, 0, WIDTH, HEIGHT], fill=BG_COLOR)

    # Title bar
    draw.rectangle([0, 0, WIDTH, TITLE_H], fill=BAR_COLOR)

    # Traffic light buttons
    cx, cy = 16, TITLE_H // 2
    for color in [BAR_BTN_RED, BAR_BTN_YEL, BAR_BTN_GRN]:
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=color)
        cx += 22

    # Title
    title = "Terminal — universal ai memory sync demo"
    tw = text_length(draw, title, FONT)
    draw_text(draw, ((WIDTH - tw) // 2, TITLE_H - 10), title, FONT, (150, 150, 160))

    # Lines (show last 18 max)
    y = PAD_TOP
    for line in lines[-18:]:
        x = MARGIN
        for text, color in parse_line(line):
            draw_text(draw, (x, y), text, FONT, color)
            x += text_length(draw, text, FONT)
        y += LINE_H

    # Cursor
    if cursor_visible and lines:
        last = lines[-1]
        x = MARGIN
        for text, _ in parse_line(last):
            x += text_length(draw, text, FONT)
        draw.rectangle([x, y, x + 9, y + LINE_H - 2], fill=TEXT_CURSOR)

    return img


def generate_gif(output_path: str):
    scenes = [
        # Scene 1: agents discovery
        [
            "$ python memory_sync.py agents",
            "[INFO] Scanning for AI agents on this machine...",
            "",
            "[CURSOR]",
            "  rules/: 3 files  (~/.cursor/rules)",
            "",
            "[OPENCLAW]",
            "  workspace/MEMORY.md: 1 file  (~/.openclaw/workspace/MEMORY.md)",
            "  workspace/SOUL.md: 1 file  (~/.openclaw/workspace/SOUL.md)",
            "  agents/a1b2c3/MEMORY.md: 1 file",
            "",
            "[HERMES]",
            "  memories/MEMORY.md: 1 file  (~/.hermes/memories/MEMORY.md)",
            "",
            "[WINDSURF]",
            "  memory/: 2 files  (~/.windsurf/memory)",
            "",
            "[WORKBUDDY]",
            "  __user__: 2 file(s)  (~/.ai-memory/memory/workbuddy)",
        ],
        # Scene 2: push
        [
            "$ python memory_sync.py push --agent all",
            "[INFO] Syncing agent=all, found 10 source(s)...",
            "  cursor/rules: 3 file(s)",
            "  openclaw/workspace: 4 file(s)",
            "  hermes/memories: 1 file(s)",
            "  windsurf/memory: 2 file(s)",
            "",
            "[OK] Push successful! Synced 15 file(s) from 5 platforms!",
        ],
        # Scene 3: pull
        [
            "$ python memory_sync.py pull --agent all",
            "[INFO] Pulling latest memory from GitHub (agent=all)...",
            "  cursor/rules/custom-rule.md: updated",
            "  openclaw/workspace/MEMORY.md: updated",
            "  hermes/memories/MEMORY.md: updated",
            "  windsurf/memory/session.md: updated",
            "",
            "[OK] Pull complete! Updated 7 file(s)",
        ],
        # Scene 4: status
        [
            "$ python memory_sync.py status",
            "Repo URL    : https://github.com/user/ai-memory",
            "Local cache : C:/Users/admin/.ai-memory/repo-cache",
            "Platform    : Windows 11",
            "Hostname    : home-pc",
            "",
            "Last 4 syncs:",
            "  abc1234 sync(cursor):   2026-04-24 11:00:00 (3 files)",
            "  def5678 sync(openclaw): 2026-04-24 10:55:00 (4 files)",
            "  ghi9012 sync(hermes):   2026-04-24 10:50:00 (1 files)",
            "",
            "Detected memory sources:",
            "  cursor/rules/:     3 file(s)",
            "  openclaw/:          4 file(s)",
            "  hermes/memories:    1 file(s)",
            "  windsurf/memory:    2 file(s)",
        ],
    ]

    frames = []
    frame_duration = 55  # ms per frame

    for scene in scenes:
        for i in range(1, len(scene) + 1):
            img = draw_terminal(scene[:i], cursor_visible=True)
            frames.append(img)
        # Pause + cursor blink on last frame
        for _ in range(4):
            frames.append(draw_terminal(scene[:], cursor_visible=True))
        frames.append(draw_terminal(scene[:], cursor_visible=False))

    # Save
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration,
        loop=0,
        optimize=True,
    )
    print(f"Saved: {output_path}  ({len(frames)} frames, {len(scenes)} scenes)")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "demo.gif"
    generate_gif(out)
