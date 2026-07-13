"""Generic hero-slide generator for a list of post ids.

For each id: reads content/captions/<id>.md, pulls TYPE + HOOK, auto-wraps the
hook to fit, and renders a branded 1080x1350 PNG to content/posts/<id>/slide-1.png.

The last clause of the hook (after the final em-dash, comma, or just the tail) is
coloured in the mint accent for emphasis; the rest is off-white.
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
MARGIN = 90
USABLE = W - 2 * MARGIN
F_BOLD = 'sans-serif" font-weight="800'

# These ids carry the eyebrow label for each TYPE
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
    "Engage":  "COMMENT BELOW 👇",
}


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
    # Fewer lines → bigger text
    if n_lines <= 2:
        return 84
    if n_lines == 3:
        return 76
    if n_lines == 4:
        return 66
    if n_lines == 5:
        return 58
    return 50


def split_emphasis(hook: str) -> tuple[str, str]:
    """Return (lead, tail) where tail gets the accent colour.
    Split on the last em-dash if present, else colour the final ~40%.
    """
    for sep in (" — ", " - "):
        if sep in hook:
            lead, tail = hook.rsplit(sep, 1)
            return lead.strip(), tail.strip()
    # else colour the final sentence/clause
    words = hook.split()
    if len(words) <= 4:
        return "", hook
    cut = int(len(words) * 0.6)
    return " ".join(words[:cut]), " ".join(words[cut:])


def render_slide(slug: str, ptype: str, hook: str) -> None:
    eyebrow = EYEBROW.get(ptype, "KEEPIX")
    footer = FOOTER.get(ptype, "")

    lead, tail = split_emphasis(hook)

    # Decide wrapping width by trying font sizes
    # Start by wrapping combined text to estimate line count
    combined = (lead + " " + tail).strip()
    # try max_chars from 18..26 to land 2-4 lines
    best_lines = None
    best_fs = 50
    for max_chars in (16, 18, 20, 22, 24):
        lines = wrap(combined, max_chars)
        if 2 <= len(lines) <= 4:
            best_lines = lines
            best_fs = pick_font_size(len(lines))
            break
    if best_lines is None:
        best_lines = wrap(combined, 22)
        best_fs = pick_font_size(len(best_lines))

    # Determine which wrapped lines belong to the accent tail
    lead_len = len(lead.split())
    rebuilt: list[tuple[str, bool]] = []  # (line, is_accent)
    word_idx = 0
    lead_words = lead.split()
    for line in best_lines:
        n = len(line.split())
        # a line is accent if the majority of its words are past lead_len
        is_accent = word_idx >= lead_len
        rebuilt.append((line, is_accent))
        word_idx += n

    # Vertical layout: center block
    line_height = int(best_fs * 1.15)
    block_h = line_height * len(rebuilt)
    start_y = (H - block_h) // 2 + best_fs // 2

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
  <text x="{W//2}" y="{H-150}" font-family="{F_BOLD}" font-size="30" fill="{TEXT}" text-anchor="middle" letter-spacing="2">{esc(footer)}</text>
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
    print(f"  {slug:42}  {ptype:8}  {len(rebuilt)} lines @ {best_fs}px", file=sys.stderr)


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
