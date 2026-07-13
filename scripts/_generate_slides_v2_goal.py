"""Generic slide generator v2 — adds a goal-frame + ball motif at the bottom.

Same interface as _generate_slides_generic.py: pass post ids as args. For each
id, reads content/captions/<id>.md → TYPE + HOOK → renders a 1080x1350 PNG with
hero text on the upper two-thirds and a goal+ball illustration filling the
lower band. The last accent-coloured clause of the hook still gets the mint
emphasis colour.
"""
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

# Goal layout
GOAL_TOP    = 920
GOAL_BOT    = 1110
POST_L_X    = 210
POST_R_X    = 870
POST_STROKE = 6
BALL_CX     = W // 2
BALL_CY     = GOAL_BOT - 14
BALL_R      = 34


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
    """Return the SVG snippet for the goal frame + net + ball."""
    parts: list[str] = []

    # Net background — vertical strands
    for x in range(POST_L_X + 30, POST_R_X, 36):
        parts.append(
            f'<line x1="{x}" y1="{GOAL_TOP + POST_STROKE}" x2="{x}" y2="{GOAL_BOT}" '
            f'stroke="{MUTED}" stroke-width="1.2" opacity="0.35"/>'
        )
    # Net horizontal strands
    for y in range(GOAL_TOP + 40, GOAL_BOT, 38):
        parts.append(
            f'<line x1="{POST_L_X + POST_STROKE}" y1="{y}" x2="{POST_R_X - POST_STROKE}" y2="{y}" '
            f'stroke="{MUTED}" stroke-width="1.2" opacity="0.35"/>'
        )

    # Posts + crossbar (drawn on top of net so they read as frame)
    parts.append(
        f'<line x1="{POST_L_X}" y1="{GOAL_TOP}" x2="{POST_R_X}" y2="{GOAL_TOP}" '
        f'stroke="{TEXT}" stroke-width="{POST_STROKE}" stroke-linecap="round"/>'
    )
    parts.append(
        f'<line x1="{POST_L_X}" y1="{GOAL_TOP}" x2="{POST_L_X}" y2="{GOAL_BOT}" '
        f'stroke="{TEXT}" stroke-width="{POST_STROKE}" stroke-linecap="round"/>'
    )
    parts.append(
        f'<line x1="{POST_R_X}" y1="{GOAL_TOP}" x2="{POST_R_X}" y2="{GOAL_BOT}" '
        f'stroke="{TEXT}" stroke-width="{POST_STROKE}" stroke-linecap="round"/>'
    )

    # Ground line / goal line
    parts.append(
        f'<line x1="{POST_L_X - 40}" y1="{GOAL_BOT}" x2="{POST_R_X + 40}" y2="{GOAL_BOT}" '
        f'stroke="{TEXT}" stroke-width="3" opacity="0.6"/>'
    )

    # Ball — white sphere with one accent pentagon at top
    cx, cy, r = BALL_CX, BALL_CY, BALL_R
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{TEXT}"/>')
    # Single dark pentagon at the top of the ball (simplified soccer ball cue)
    p_top = (cx, cy - r + 8)
    p_l1  = (cx - 18, cy - 4)
    p_l2  = (cx - 11, cy + 17)
    p_r2  = (cx + 11, cy + 17)
    p_r1  = (cx + 18, cy - 4)
    pts = " ".join(f"{int(x)},{int(y)}" for (x, y) in [p_top, p_l1, p_l2, p_r2, p_r1])
    parts.append(f'<polygon points="{pts}" fill="{BG}"/>')
    # Subtle accent rim
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

    # Tag lines as accent based on lead word count
    rebuilt: list[tuple[str, bool]] = []
    word_idx = 0
    lead_words = len(lead.split())
    for line in best_lines:
        is_accent = word_idx >= lead_words
        rebuilt.append((line, is_accent))
        word_idx += len(line.split())

    # Layout: text block lives between y=300 and y=GOAL_TOP - 40
    text_zone_top = 300
    text_zone_bot = GOAL_TOP - 40
    text_zone_h = text_zone_bot - text_zone_top

    line_height = int(best_fs * 1.15)
    block_h = line_height * len(rebuilt)
    # vertically centre the block within the text zone
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
  <rect width="{W}" height="{H}" fill="{BG}"/>
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
