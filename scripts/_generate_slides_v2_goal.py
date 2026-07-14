"""Generic slide generator v2 — goal-frame + ball motif, per-TYPE background."""
from __future__ import annotations

import sys
from pathlib import Path

import resvg_py

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, parse_caption_file  # noqa: E402

POSTS = ROOT / "content" / "posts"

BG     = "#0f3d2e"
ACCENT = "#2ECC71"
TEXT   = "#F5F5F0"
MUTED  = "#9FBFAE"

W, H = 1080, 1350
F_BOLD = 'sans-serif" font-weight="800'
F_ITAL = 'sans-serif" font-weight="400" font-style="italic'

EYEBROW = {
    "Value":   "VALUE · COACHING POINT",
    "Product": "PRODUCT · KEEPIX",
    "Story":   "KEEPIX · STORY",
    "Engage":  "ENGAGE · YOUR TURN",
}
FOOTER = {
    "Value":   "SAVE FOR YOUR NEXT SESSION",
    "Product": "LINK IN BIO",
    "Story":   "— a coaching reflection",
    "Engage":  "DROP YOUR ANSWER BELOW",
}

GOAL_TOP    = 920
GOAL_BOT    = 1110
POST_L_X    = 210
POST_R_X    = 870
POST_STROKE = 6
BALL_CX     = W // 2
BALL_CY     = GOAL_BOT - 14
BALL_R      = 34


def background(ptype: str) -> str:
    """Per-TYPE background, all inside the dark-green KEEPIX family.
      Value->Centre Glow  Product->Diagonal Depth  Story->Spotlight
      Engage->Mowed Stripes  other->Flat Pitch
    """
    t = (ptype or "").strip().lower()

    if t == "value":
        return (
            '<defs><radialGradient id="bg" cx="50%" cy="36%" r="75%">'
            '<stop offset="0%" stop-color="#1e6544"/>'
            '<stop offset="46%" stop-color="#0f3d2e"/>'
            '<stop offset="100%" stop-color="#0a2c20"/>'
            '</radialGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
        )
    if t == "product":
        return (
            '<defs><linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">'
            '<stop offset="0%" stop-color="#0f3d2e"/>'
            '<stop offset="48%" stop-color="#0d3a37"/>'
            '<stop offset="100%" stop-color="#0b2b3d"/>'
            '</linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
        )
    if t == "story":
        return (
            '<defs><radialGradient id="glow" cx="82%" cy="12%" r="62%">'
            '<stop offset="0%" stop-color="#2ECC71" stop-opacity="0.22"/>'
            '<stop offset="46%" stop-color="#2ECC71" stop-opacity="0"/>'
            '</radialGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="#0a2118"/>'
            f'<rect width="{W}" height="{H}" fill="url(#glow)"/>'
        )
    if t == "engage":
        stripe = W // 10
        rects = f'<rect width="{W}" height="{H}" fill="#0f3d2e"/>'
        for x in range(0, W, stripe * 2):
            rects += f'<rect x="{x}" y="0" width="{stripe}" height="{H}" fill="#123f31"/>'
        return rects

    return f'<rect width="{W}" height="{H}" fill="{BG}"/>'


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def pick_font_size(n_lines: int) -> int:
    if n_lines <= 2:
        return 78
    if n_lines == 3:
        return 70
    if n_lines == 4:
        return 60
    if n_lines == 5:
        return 52
    return 46


def split_emphasis(hook: str) -> tuple[str, str]:
    for sep in (" — ", " - "):
        if sep in hook:
            lead, tail = hook.rsplit(sep, 1)
            return lead.strip(), tail.strip()
    words = hook.split()
    if len(words) <= 4:
        return "", hook
    cut = int(len(words) * 0.6)
    return " ".join(words[:cut]), " ".join(words[cut:])


def goal_svg() -> str:
    parts: list[str] = []
    for x in range(POST_L_X + 30, POST_R_X, 36):
        parts.append(
            f'<line x1="{x}" y1="{GOAL_TOP + POST_STROKE}" x2="{x}" y2="{GOAL_BOT}" '
            f'stroke="{MUTED}" stroke-width="1.2" opacity="0.35"/>'
        )
    for y in range(GOAL_TOP + 40, GOAL_BOT, 38):
        parts.append(
            f'<line x1="{POST_L_X + POST_STROKE}" y1="{y}" x2="{POST_R_X - POST_STROKE}" y2="{y}" '
            f'stroke="{MUTED}" stroke-width="1.2" opacity="0.35"/>'
        )
    parts.append(f'<line x1="{POST_L_X}" y1="{GOAL_TOP}" x2="{POST_R_X}" y2="{GOAL_TOP}" stroke="{TEXT}" stroke-width="{POST_STROKE}" stroke-linecap="round"/>')
    parts.append(f'<line x1="{POST_L_X}" y1="{GOAL_TOP}" x2="{POST_L_X}" y2="{GOAL_BOT}" stroke="{TEXT}" stroke-width="{POST_STROKE}" stroke-linecap="round"/>')
    parts.append(f'<line x1="{POST_R_X}" y1="{GOAL_TOP}" x2="{POST_R_X}" y2="{GOAL_BOT}" stroke="{TEXT}" stroke-width="{POST_STROKE}" stroke-linecap="round"/>')
    parts.append(f'<line x1="{POST_L_X - 40}" y1="{GOAL_BOT}" x2="{POST_R_X + 40}" y2="{GOAL_BOT}" stroke="{TEXT}" stroke-width="3" opacity="0.6"/>')
    cx, cy, r = BALL_CX, BALL_CY, BALL_R
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{TEXT}"/>')
    p_top = (cx, cy - r + 8); p_l1 = (cx - 18, cy - 4); p_l2 = (cx - 11, cy + 17)
    p_r2 = (cx + 11, cy + 17); p_r1 = (cx + 18, cy - 4)
    pts = " ".join(f"{int(a)},{int(b)}" for (a, b) in [p_top, p_l1, p_l2, p_r2, p_r1])
    parts.append(f'<polygon points="{pts}" fill="{BG}"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ACCENT}" stroke-width="2" opacity="0.7"/>')
    return "".join(parts)


def render_slide(slug: str, ptype: str, hook: str) -> None:
    eyebrow = EYEBROW.get(ptype, "KEEPIX")
    footer = FOOTER.get(ptype, "")

    lead, tail = split_emphasis(hook)
    combined = (lead + " " + tail).strip()

    best_lines = None
    best_fs = 46
    for max_chars in (16, 18, 20, 22, 24):
        lines = wrap(combined, max_chars)
        if 2 <= len(lines) <= 4:
            best_lines = lines
            best_fs = pick_font_size(len(lines))
            break
    if best_lines is None:
        best_lines = wrap(combined, 22)
        best_fs = pick_font_size(len(best_lines))

    rebuilt: list[tuple[str, bool]] = []
    word_idx = 0
    lead_words = len(lead.split())
    for line in best_lines:
        is_accent = word_idx >= lead_words
        rebuilt.append((line, is_accent))
        word_idx += len(line.split())

    text_zone_top = 300
    text_zone_bot = GOAL_TOP - 40
    text_zone_h = text_zone_bot - text_zone_top
    line_height = int(best_fs * 1.15)
    block_h = line_height * len(rebuilt)
    start_y = text_zone_top + (text_zone_h - block_h) // 2 + best_fs // 2

    text_svgs = []
    y = start_y
    for line, is_accent in rebuilt:
        color = ACCENT if is_accent else TEXT
        text_svgs.append(
            f'<text x="{W//2}" y="{y}" font-family="{F_BOLD}" font-size="{best_fs}" '
            f'fill="{color}" text-anchor="middle" letter-spacing="-1">{esc(line)}</text>'
        )
        y += line_height

    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">{esc(eyebrow)}</text>
  <rect x="{W//2 - 40}" y="250" width="80" height="6" fill="{ACCENT}"/>
  {"".join(text_svgs)}
  {goal_svg()}
  <text x="{W//2}" y="{H-130}" font-family="{F_BOLD}" font-size="28" fill="{TEXT}" text-anchor="middle" letter-spacing="2">{esc(footer)}</text>
'''
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  {background(ptype)}
  {body}
  <circle cx="{W-240}" cy="{H-59}" r="5" fill="{ACCENT}"/>
  <text x="{W-60}" y="{H-50}" font-family="{F_BOLD}" font-size="28" fill="{TEXT}" text-anchor="end" letter-spacing="4">KEEPIX</text>
</svg>'''

    out = POSTS / slug / "slide-1.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    png = resvg_py.svg_to_bytes(svg_string=svg)
    out.write_bytes(bytes(png))
    print(f"  {slug:42}  {ptype:8}  {len(rebuilt)} lines @ {best_fs}px -> {out.name}", file=sys.stderr)


def main(ids: list[str]) -> None:
    for slug in ids:
        cap = ROOT / "content" / "captions" / f"{slug}.md"
        if not cap.exists():
            print(f"  [skip] no caption: {slug}", file=sys.stderr)
            continue
        sections = parse_caption_file(cap)
        ptype = sections.get("TYPE", "Value")
        hook = sections.get("HOOK", "")
        if not hook:
            print(f"  [skip] no HOOK: {slug}", file=sys.stderr)
            continue
        render_slide(slug, ptype, hook)


if __name__ == "__main__":
    main(sys.argv[1:])
