"""Generate all Instagram slide PNGs for 2026-05-01 through 2026-05-07.

Outputs one folder per post under content/posts/YYYY-MM-DD-[type]/.
"""
from __future__ import annotations

from pathlib import Path
import resvg_py

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "content" / "posts"

# ---- palette ----
BG     = "#0f3d2e"
PITCH  = "#1a5c3f"
ACCENT = "#2ECC71"
TEXT   = "#F5F5F0"
MUTED  = "#9FBFAE"
GK     = "#FFD700"
COACH  = "#3498DB"
CONE   = "#E67E22"

W, H = 1080, 1350
F_BOLD = 'sans-serif" font-weight="800'
F_REG  = 'sans-serif" font-weight="400'
F_ITAL = 'sans-serif" font-weight="400" font-style="italic'


def svg_doc(body: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <defs>
    <marker id="arr-white" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="{TEXT}"/>
    </marker>
    <marker id="arr-gk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="{GK}"/>
    </marker>
    <marker id="arr-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/>
    </marker>
  </defs>
  {body}
  <circle cx="{W-240}" cy="{H-59}" r="5" fill="{ACCENT}"/>
  <text x="{W-60}" y="{H-50}" font-family="{F_BOLD}" font-size="28" fill="{TEXT}" text-anchor="end" letter-spacing="4">KEEPIX</text>
</svg>'''


def pitch_frame(x: int, y: int, w: int, h: int) -> str:
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" ry="20" fill="{PITCH}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" ry="20" fill="none"'
            f' stroke="{TEXT}" stroke-width="3" opacity="0.25"/>')


def drill_header(eyebrow: str, title: str) -> str:
    return (f'<text x="80" y="120" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="4">{eyebrow}</text>'
            f'<text x="80" y="185" font-family="{F_BOLD}" font-size="58" fill="{TEXT}" letter-spacing="-1">{title}</text>')


def takeaway(text: str) -> str:
    return (f'<rect x="80" y="1150" width="60" height="6" fill="{ACCENT}"/>'
            f'<text x="80" y="1220" font-family="{F_BOLD}" font-size="38" fill="{TEXT}">{text}</text>')


# =========================================================
# Day 1 (5/1 Fri) — Quick Tip: "RESET"
# =========================================================
def day1_quicktip():
    body = f'''
  <!-- eyebrow -->
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">QUICK TIP · COACHING CUE</text>

  <!-- hero word -->
  <text x="{W//2}" y="480" font-family="{F_BOLD}" font-size="260" fill="{ACCENT}" text-anchor="middle" letter-spacing="-6">RESET</text>

  <!-- divider -->
  <line x1="160" y1="540" x2="{W-160}" y2="540" stroke="{TEXT}" stroke-width="2" opacity="0.3"/>

  <!-- three numbered points -->
  <!-- 1 -->
  <text x="120" y="640" font-family="{F_BOLD}" font-size="30" fill="{ACCENT}" letter-spacing="2">01</text>
  <text x="200" y="640" font-family="{F_BOLD}" font-size="30" fill="{TEXT}" letter-spacing="1">AFTER A SAVE</text>
  <text x="200" y="678" font-family="{F_REG}" font-size="26" fill="{MUTED}">Hands back up before the next ball.</text>

  <!-- 2 -->
  <text x="120" y="770" font-family="{F_BOLD}" font-size="30" fill="{ACCENT}" letter-spacing="2">02</text>
  <text x="200" y="770" font-family="{F_BOLD}" font-size="30" fill="{TEXT}" letter-spacing="1">AFTER AN ERROR</text>
  <text x="200" y="808" font-family="{F_REG}" font-size="26" fill="{MUTED}">One word before they overthink it.</text>

  <!-- 3 -->
  <text x="120" y="900" font-family="{F_BOLD}" font-size="30" fill="{ACCENT}" letter-spacing="2">03</text>
  <text x="200" y="900" font-family="{F_BOLD}" font-size="30" fill="{TEXT}" letter-spacing="1">BEFORE A SET PIECE</text>
  <text x="200" y="938" font-family="{F_REG}" font-size="26" fill="{MUTED}">Posture, position, next rep.</text>

  <!-- bottom accent bar -->
  <rect x="80" y="1150" width="60" height="6" fill="{ACCENT}"/>
  <text x="80" y="1220" font-family="{F_BOLD}" font-size="36" fill="{TEXT}">Build it in early. Use it forever.</text>
'''
    return [("slide-1.svg", svg_doc(body))]


# =========================================================
# Day 2 (5/2 Sat) — Reflection: "Forget the last rep."
# =========================================================
def day2_reflection():
    body = f'''
  <!-- top label -->
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="24" fill="{ACCENT}" text-anchor="middle" letter-spacing="8">KEEPIX · WEEKLY REFLECTION</text>

  <!-- large decorative quote mark -->
  <text x="{W//2}" y="430" font-family="{F_BOLD}" font-size="200" fill="{ACCENT}" text-anchor="middle" opacity="0.25">&#8220;</text>

  <!-- quote lines -->
  <text x="{W//2}" y="540" font-family="{F_BOLD}" font-size="62" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">Forget the last rep.</text>
  <text x="{W//2}" y="640" font-family="{F_BOLD}" font-size="62" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">What are your feet</text>
  <text x="{W//2}" y="740" font-family="{F_BOLD}" font-size="62" fill="{ACCENT}" text-anchor="middle" letter-spacing="-1">doing right now?</text>

  <!-- mint accent line -->
  <rect x="{W//2 - 80}" y="810" width="160" height="5" fill="{ACCENT}"/>

  <!-- attribution -->
  <text x="{W//2}" y="890" font-family="{F_ITAL}" font-size="28" fill="{MUTED}" text-anchor="middle" letter-spacing="2">— pitch-side, November</text>
'''
    return [("slide-1.svg", svg_doc(body))]


# =========================================================
# Day 3 (5/3 Sun) — Engage: "Keeper in their own head"
# =========================================================
def day3_engage():
    body = f'''
  <!-- eyebrow -->
  <rect x="80" y="230" width="8" height="80" fill="{ACCENT}"/>
  <text x="120" y="280" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="5">ENGAGE · COACHES' QUESTION</text>

  <!-- question -->
  <text x="80" y="460" font-family="{F_BOLD}" font-size="76" fill="{TEXT}" letter-spacing="-1">When a keeper</text>
  <text x="80" y="556" font-family="{F_BOLD}" font-size="76" fill="{TEXT}" letter-spacing="-1">is in their</text>
  <text x="80" y="652" font-family="{F_BOLD}" font-size="76" fill="{ACCENT}" letter-spacing="-1">own head —</text>
  <text x="80" y="748" font-family="{F_BOLD}" font-size="76" fill="{TEXT}" letter-spacing="-1">what do you do?</text>

  <!-- divider -->
  <line x1="80" y1="820" x2="300" y2="820" stroke="{TEXT}" stroke-width="2" opacity="0.4"/>

  <!-- three options -->
  <text x="80" y="890" font-family="{F_REG}" font-size="30" fill="{MUTED}">A physical cue — something with their feet?</text>
  <text x="80" y="940" font-family="{F_REG}" font-size="30" fill="{MUTED}">A question to bring them back?</text>
  <text x="80" y="990" font-family="{F_REG}" font-size="30" fill="{MUTED}">Silence — let the next ball do the work?</text>

  <!-- cta -->
  <rect x="80" y="1130" width="60" height="6" fill="{ACCENT}"/>
  <text x="80" y="1200" font-family="{F_BOLD}" font-size="34" fill="{TEXT}">One sentence below is enough.</text>
'''
    return [("slide-1.svg", svg_doc(body))]


# =========================================================
# Day 4 (5/4 Mon) — Story: "Distribution decision"
# =========================================================
def day4_story():
    px, py, pw, ph = 60, 560, 960, 480
    body = f'''
  <!-- eyebrow -->
  <rect x="80" y="110" width="8" height="60" fill="{ACCENT}"/>
  <text x="120" y="150" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="5">STORY · FROM THE PITCH</text>

  <!-- key phrase -->
  <text x="80" y="280" font-family="{F_BOLD}" font-size="66" fill="{TEXT}" letter-spacing="-1">We were training</text>
  <text x="80" y="362" font-family="{F_BOLD}" font-size="66" fill="{TEXT}" letter-spacing="-1">the execution.</text>
  <text x="80" y="480" font-family="{F_BOLD}" font-size="66" fill="{ACCENT}" letter-spacing="-1">Not the decision.</text>

  <!-- pitch: GK with distribution arrows radiating out -->
  {pitch_frame(px, py, pw, ph)}

  <!-- GK at centre-left of pitch -->
  <circle cx="{px + 160}" cy="{py + ph//2}" r="38" fill="{GK}" stroke="{BG}" stroke-width="4"/>
  <text x="{px + 160}" y="{py + ph//2 + 60}" font-family="{F_BOLD}" font-size="20" fill="{MUTED}" text-anchor="middle" letter-spacing="3">GK</text>

  <!-- distribution arrows: short left, long right, long diagonal -->
  <line x1="{px + 200}" y1="{py + ph//2}" x2="{px + 380}" y2="{py + ph//2 - 120}" stroke="{TEXT}" stroke-width="4" stroke-dasharray="10,8" marker-end="url(#arr-white)"/>
  <line x1="{px + 200}" y1="{py + ph//2}" x2="{px + 700}" y2="{py + ph//2}" stroke="{ACCENT}" stroke-width="5" marker-end="url(#arr-accent)"/>
  <line x1="{px + 200}" y1="{py + ph//2}" x2="{px + 550}" y2="{py + ph//2 + 160}" stroke="{TEXT}" stroke-width="4" stroke-dasharray="10,8" marker-end="url(#arr-white)"/>

  <!-- teammate dots -->
  <circle cx="{px + 380}" cy="{py + ph//2 - 130}" r="20" fill="{COACH}" stroke="{BG}" stroke-width="3"/>
  <circle cx="{px + 720}" cy="{py + ph//2}" r="20" fill="{COACH}" stroke="{BG}" stroke-width="3"/>
  <circle cx="{px + 560}" cy="{py + ph//2 + 170}" r="20" fill="{COACH}" stroke="{BG}" stroke-width="3"/>

  {takeaway("Train the decision. Then train the execution.")}
'''
    return [("slide-1.svg", svg_doc(body))]


# =========================================================
# Day 5 (5/5 Tue) — Value: "1v1: Three situations" (4 slides)
# =========================================================
def day5_value():
    slides: list[tuple[str, str]] = []

    # Slide 1 — Hero
    hero = f'''
  <rect x="80" y="300" width="8" height="200" fill="{ACCENT}"/>
  <text x="120" y="335" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="6">THREE SITUATIONS · ONE KEEPER</text>
  <text x="120" y="540" font-family="{F_BOLD}" font-size="240" fill="{TEXT}" letter-spacing="-6">1v1</text>
  <line x1="120" y1="660" x2="380" y2="660" stroke="{TEXT}" stroke-width="3"/>
  <text x="120" y="730" font-family="{F_REG}" font-size="36" fill="{TEXT}">Three situations.</text>
  <text x="120" y="778" font-family="{F_REG}" font-size="36" fill="{TEXT}">Three answers.</text>
  <text x="120" y="960" font-family="{F_BOLD}" font-size="26" fill="{MUTED}" letter-spacing="4">BREAKAWAY  ·  CUTBACK  ·  SMOTHER</text>
  <rect x="120" y="980" width="60" height="6" fill="{ACCENT}"/>
'''
    slides.append(("slide-1-hero.svg", svg_doc(hero)))

    # Slide 2 — The Breakaway (top-down)
    px, py, pw, ph = 60, 260, 960, 820
    breakaway = f'''
  {drill_header("SITUATION 01 / THE BREAKAWAY", "When to stop, not whether to come.")}
  {pitch_frame(px, py, pw, ph)}

  <!-- goal at bottom centre -->
  <rect x="{px + pw//2 - 100}" y="{py + ph - 30}" width="200" height="30" rx="4" fill="none" stroke="{TEXT}" stroke-width="4" opacity="0.7"/>
  <text x="{px + pw//2}" y="{py + ph + 20}" font-family="{F_BOLD}" font-size="20" fill="{MUTED}" text-anchor="middle" letter-spacing="3">GOAL</text>

  <!-- GK starting position (near goal) -->
  <circle cx="{px + pw//2}" cy="{py + ph - 130}" r="36" fill="{GK}" stroke="{BG}" stroke-width="4"/>
  <text x="{px + pw//2}" y="{py + ph - 190}" font-family="{F_BOLD}" font-size="20" fill="{MUTED}" text-anchor="middle" letter-spacing="3">GK</text>

  <!-- striker at top, bearing down -->
  <circle cx="{px + pw//2 + 40}" cy="{py + 120}" r="32" fill="{TEXT}" stroke="{BG}" stroke-width="3"/>
  <text x="{px + pw//2 + 40}" y="{py + 70}" font-family="{F_BOLD}" font-size="20" fill="{MUTED}" text-anchor="middle" letter-spacing="3">STRIKER</text>

  <!-- striker run arrow (downward) -->
  <line x1="{px + pw//2 + 40}" y1="{py + 155}" x2="{px + pw//2 + 30}" y2="{py + ph - 260}" stroke="{TEXT}" stroke-width="4" stroke-dasharray="10,8" marker-end="url(#arr-white)"/>

  <!-- GK closing arrow -->
  <line x1="{px + pw//2}" y1="{py + ph - 170}" x2="{px + pw//2 + 20}" y2="{py + ph//2 + 40}" stroke="{GK}" stroke-width="6" marker-end="url(#arr-gk)"/>

  <!-- decision zone marker -->
  <rect x="{px + pw//2 - 120}" y="{py + ph//2 - 20}" width="240" height="80" rx="10" fill="none" stroke="{ACCENT}" stroke-width="3" stroke-dasharray="10,8"/>
  <text x="{px + pw//2}" y="{py + ph//2 + 110}" font-family="{F_BOLD}" font-size="22" fill="{ACCENT}" text-anchor="middle" letter-spacing="3">DECISION ZONE — STOP HERE</text>

  {takeaway("Drill the closing line. Not the save.")}
'''
    slides.append(("slide-2-breakaway.svg", svg_doc(breakaway)))

    # Slide 3 — The Cutback (top-down)
    cutback = f'''
  {drill_header("SITUATION 02 / THE CUTBACK", "Stay big. Force the commit.")}
  {pitch_frame(px, py, pw, ph)}

  <!-- goal at bottom -->
  <rect x="{px + pw//2 - 100}" y="{py + ph - 30}" width="200" height="30" rx="4" fill="none" stroke="{TEXT}" stroke-width="4" opacity="0.7"/>

  <!-- GK wide between striker and goal centre -->
  <circle cx="{px + pw//2 - 40}" cy="{py + ph - 200}" r="36" fill="{GK}" stroke="{BG}" stroke-width="4"/>

  <!-- body width indicators (wide arms) -->
  <line x1="{px + pw//2 - 130}" y1="{py + ph - 210}" x2="{px + pw//2 + 60}" y2="{py + ph - 210}" stroke="{GK}" stroke-width="5" stroke-dasharray="8,4"/>
  <text x="{px + pw//2 - 40}" y="{py + ph - 260}" font-family="{F_BOLD}" font-size="22" fill="{GK}" text-anchor="middle" letter-spacing="3">STAY WIDE</text>

  <!-- striker has cut inside: positioned right-of-center box -->
  <circle cx="{px + pw//2 + 250}" cy="{py + ph//2}" r="32" fill="{TEXT}" stroke="{BG}" stroke-width="3"/>
  <text x="{px + pw//2 + 250}" y="{py + ph//2 - 50}" font-family="{F_BOLD}" font-size="20" fill="{MUTED}" text-anchor="middle" letter-spacing="3">STRIKER</text>

  <!-- striker cut-inside path -->
  <path d="M {px + pw - 120} {py + 150} Q {px + pw//2 + 380} {py + ph//2 - 100} {px + pw//2 + 250} {py + ph//2}" stroke="{TEXT}" stroke-width="4" fill="none" stroke-dasharray="10,8" marker-end="url(#arr-white)"/>

  <!-- "do not dive" annotation -->
  <text x="{px + pw//2 - 200}" y="{py + ph//2 + 80}" font-family="{F_BOLD}" font-size="24" fill="{ACCENT}" letter-spacing="3">DO NOT DIVE EARLY</text>
  <text x="{px + pw//2 - 200}" y="{py + ph//2 + 116}" font-family="{F_REG}" font-size="22" fill="{MUTED}" letter-spacing="2">Force the striker to commit first.</text>

  {takeaway("Patience is the drill.")}
'''
    slides.append(("slide-3-cutback.svg", svg_doc(cutback)))

    # Slide 4 — The Smother (top-down)
    smother = f'''
  {drill_header("SITUATION 03 / THE SMOTHER", "Drill the trigger. Not the dive.")}
  {pitch_frame(px, py, pw, ph)}

  <!-- goal at bottom -->
  <rect x="{px + pw//2 - 100}" y="{py + ph - 30}" width="200" height="30" rx="4" fill="none" stroke="{TEXT}" stroke-width="4" opacity="0.7"/>

  <!-- GK going to ground — elongated shape -->
  <ellipse cx="{px + pw//2 - 60}" cy="{py + ph - 250}" rx="130" ry="38" fill="{GK}" opacity="0.9" transform="rotate(-15, {px + pw//2 - 60}, {py + ph - 250})"/>
  <circle cx="{px + pw//2 - 150}" cy="{py + ph - 280}" r="28" fill="{GK}" stroke="{BG}" stroke-width="3"/>
  <text x="{px + pw//2 - 60}" y="{py + ph - 310}" font-family="{F_BOLD}" font-size="20" fill="{GK}" text-anchor="middle" letter-spacing="3">GK → SMOTHER</text>

  <!-- ball position -->
  <circle cx="{px + pw//2 + 80}" cy="{py + ph - 340}" r="20" fill="{TEXT}" stroke="{BG}" stroke-width="2"/>

  <!-- striker bearing down -->
  <circle cx="{px + pw//2 + 120}" cy="{py + ph//2 - 60}" r="32" fill="{TEXT}" stroke="{BG}" stroke-width="3"/>
  <line x1="{px + pw//2 + 115}" y1="{py + ph//2 - 25}" x2="{px + pw//2 + 90}" y2="{py + ph - 365}" stroke="{TEXT}" stroke-width="4" stroke-dasharray="10,8" marker-end="url(#arr-white)"/>

  <!-- trigger point zone -->
  <rect x="{px + pw//2 - 50}" y="{py + ph//2 + 80}" width="260" height="80" rx="10" fill="none" stroke="{ACCENT}" stroke-width="3" stroke-dasharray="10,8"/>
  <text x="{px + pw//2 + 80}" y="{py + ph//2 + 130}" font-family="{F_BOLD}" font-size="22" fill="{ACCENT}" text-anchor="middle" letter-spacing="3">TRIGGER ZONE</text>
  <text x="{px + pw//2 + 80}" y="{py + ph//2 + 200}" font-family="{F_REG}" font-size="22" fill="{MUTED}" text-anchor="middle">Too late = scored. Too early = lobbed.</text>

  {takeaway("Late smothers lose games. Drill the timing.")}
'''
    slides.append(("slide-4-smother.svg", svg_doc(smother)))

    return slides


# =========================================================
# Day 6 (5/6 Wed) — Quick Tip: "Head up. Feet. Next ball."
# =========================================================
def day6_quicktip():
    body = f'''
  <!-- eyebrow -->
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="24" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">QUICK TIP · AFTER A GOAL</text>

  <!-- 10 seconds label -->
  <text x="{W//2}" y="340" font-family="{F_BOLD}" font-size="48" fill="{MUTED}" text-anchor="middle" letter-spacing="4">10 SECONDS</text>

  <!-- divider -->
  <line x1="160" y1="380" x2="{W-160}" y2="380" stroke="{TEXT}" stroke-width="2" opacity="0.3"/>

  <!-- three cue words stacked -->
  <text x="{W//2}" y="560" font-family="{F_BOLD}" font-size="130" fill="{TEXT}" text-anchor="middle" letter-spacing="-3">HEAD UP.</text>
  <text x="{W//2}" y="720" font-family="{F_BOLD}" font-size="130" fill="{ACCENT}" text-anchor="middle" letter-spacing="-3">FEET.</text>
  <text x="{W//2}" y="880" font-family="{F_BOLD}" font-size="130" fill="{TEXT}" text-anchor="middle" letter-spacing="-3">NEXT BALL.</text>

  <!-- annotations -->
  <line x1="160" y1="940" x2="{W-160}" y2="940" stroke="{TEXT}" stroke-width="2" opacity="0.3"/>
  <text x="{W//2}" y="1010" font-family="{F_REG}" font-size="30" fill="{MUTED}" text-anchor="middle">Three words. In that order. Every time.</text>

  <rect x="80" y="1130" width="60" height="6" fill="{ACCENT}"/>
  <text x="80" y="1200" font-family="{F_BOLD}" font-size="34" fill="{TEXT}">Use it now so it means something later.</text>
'''
    return [("slide-1.svg", svg_doc(body))]


# =========================================================
# Day 7 (5/7 Thu) — Product: "Sunday Sorted" (3 slides)
# =========================================================
def day7_product():
    slides: list[tuple[str, str]] = []

    # Slide 1 — Hero
    hero = f'''
  <rect x="80" y="300" width="8" height="200" fill="{ACCENT}"/>
  <text x="120" y="335" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="6">SESSION PLANNING · KEEPIX</text>
  <text x="120" y="490" font-family="{F_BOLD}" font-size="130" fill="{TEXT}" letter-spacing="-3">SUNDAY</text>
  <text x="120" y="630" font-family="{F_BOLD}" font-size="130" fill="{ACCENT}" letter-spacing="-3">SORTED.</text>
  <line x1="120" y1="730" x2="380" y2="730" stroke="{TEXT}" stroke-width="3"/>
  <text x="120" y="800" font-family="{F_REG}" font-size="34" fill="{TEXT}">Session planning that fits</text>
  <text x="120" y="848" font-family="{F_REG}" font-size="34" fill="{TEXT}">in five minutes.</text>
  <text x="120" y="970" font-family="{F_BOLD}" font-size="24" fill="{MUTED}" letter-spacing="4">FILTER · BUILD · RUN</text>
  <rect x="120" y="990" width="60" height="6" fill="{ACCENT}"/>
'''
    slides.append(("slide-1-hero.svg", svg_doc(hero)))

    # Slide 2 — Session builder timeline
    block_data = [
        ("WARM-UP",   10, ACCENT),
        ("TECHNICAL", 20, COACH),
        ("TACTICAL",  20, GK),
        ("COOL-DOWN", 10, MUTED),
    ]
    sx, sy, swidth, sheight = 80, 360, 920, 100
    total_min = sum(b[1] for b in block_data)
    builder_parts = []
    cur_x = sx
    for name, mins, colour in block_data:
        bw = int(swidth * mins / total_min)
        builder_parts.append(
            f'<rect x="{cur_x}" y="{sy}" width="{bw - 6}" height="{sheight}" rx="12" fill="{colour}" opacity="0.85"/>'
            f'<text x="{cur_x + (bw-6)//2}" y="{sy + 36}" font-family="{F_BOLD}" font-size="20" fill="{BG}" text-anchor="middle" letter-spacing="2">{name}</text>'
            f'<text x="{cur_x + (bw-6)//2}" y="{sy + 66}" font-family="{F_BOLD}" font-size="24" fill="{BG}" text-anchor="middle">{mins} min</text>'
        )
        cur_x += bw

    # drill tiles below each block
    tile_y = sy + sheight + 40
    tile_data = [
        ("Set Position Intro",  "Warm-up",   ACCENT),
        ("Angle Play Drill",    "Technical", COACH),
        ("1v1 Scenarios",       "Technical", COACH),
        ("Breakaway Pressure",  "Tactical",  GK),
        ("Match Simulation",    "Tactical",  GK),
        ("Light Footwork",      "Cool-down", MUTED),
    ]
    tcols, tgap = 3, 16
    twidth = (swidth - tgap * (tcols - 1)) // tcols
    theight = 130
    tile_parts = []
    for i, (title, tag, col) in enumerate(tile_data):
        tr = i // tcols
        tc = i % tcols
        tx = sx + tc * (twidth + tgap)
        ty = tile_y + tr * (theight + tgap)
        tile_parts.append(
            f'<rect x="{tx}" y="{ty}" width="{twidth}" height="{theight}" rx="12" fill="{PITCH}" stroke="{col}" stroke-width="2" stroke-opacity="0.6"/>'
            f'<text x="{tx + 16}" y="{ty + 32}" font-family="{F_BOLD}" font-size="17" fill="{col}" letter-spacing="2">{tag.upper()}</text>'
            f'<text x="{tx + 16}" y="{ty + 66}" font-family="{F_BOLD}" font-size="22" fill="{TEXT}">{title}</text>'
        )

    builder_body = f'''
  <text x="80" y="120" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="4">BUILD IN FIVE MINUTES</text>
  <text x="80" y="195" font-family="{F_BOLD}" font-size="52" fill="{TEXT}" letter-spacing="-1">60-minute session. Done.</text>

  <!-- filter chips -->
  <rect x="80" y="270" width="110" height="44" rx="22" fill="{ACCENT}"/>
  <text x="135" y="300" font-family="{F_BOLD}" font-size="18" fill="{BG}" text-anchor="middle" letter-spacing="2">U16</text>
  <rect x="202" y="270" width="160" height="44" rx="22" fill="{PITCH}" stroke="{ACCENT}" stroke-width="2"/>
  <text x="282" y="300" font-family="{F_BOLD}" font-size="18" fill="{TEXT}" text-anchor="middle" letter-spacing="2">VALUE</text>
  <rect x="374" y="270" width="150" height="44" rx="22" fill="{PITCH}" stroke="{ACCENT}" stroke-width="2"/>
  <text x="449" y="300" font-family="{F_BOLD}" font-size="18" fill="{TEXT}" text-anchor="middle" letter-spacing="2">60 MIN</text>

  {"".join(builder_parts)}
  {"".join(tile_parts)}

  <rect x="80" y="1150" width="60" height="6" fill="{ACCENT}"/>
  <text x="80" y="1220" font-family="{F_BOLD}" font-size="34" fill="{TEXT}">Filter. Build. Run.</text>
'''
    slides.append(("slide-2-builder.svg", svg_doc(builder_body)))

    # Slide 3 — Phone mockup pitchside
    phone_x, phone_y, phone_w, phone_h = 280, 360, 520, 820
    mockup = f'''
  <text x="80" y="120" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="4">PITCHSIDE · NOT DESK-SIDE</text>
  <text x="80" y="195" font-family="{F_BOLD}" font-size="52" fill="{TEXT}" letter-spacing="-1">One card. Ready to run.</text>

  <!-- phone body -->
  <rect x="{phone_x}" y="{phone_y}" width="{phone_w}" height="{phone_h}" rx="50" ry="50" fill="#0a2d22" stroke="{TEXT}" stroke-width="4"/>
  <rect x="{phone_x + 180}" y="{phone_y + 20}" width="160" height="16" rx="8" fill="{TEXT}" opacity="0.2"/>

  <!-- screen bg -->
  <rect x="{phone_x + 30}" y="{phone_y + 70}" width="{phone_w - 60}" height="{phone_h - 100}" rx="24" ry="24" fill="{BG}"/>

  <!-- filter chips -->
  <rect x="{phone_x + 60}" y="{phone_y + 100}" width="120" height="44" rx="22" fill="{ACCENT}"/>
  <text x="{phone_x + 120}" y="{phone_y + 130}" font-family="{F_BOLD}" font-size="18" fill="{BG}" text-anchor="middle" letter-spacing="2">U16</text>
  <rect x="{phone_x + 190}" y="{phone_y + 100}" width="100" height="44" rx="22" fill="{PITCH}" stroke="{ACCENT}" stroke-width="2"/>
  <text x="{phone_x + 240}" y="{phone_y + 130}" font-family="{F_BOLD}" font-size="18" fill="{TEXT}" text-anchor="middle" letter-spacing="2">1v1</text>
  <rect x="{phone_x + 300}" y="{phone_y + 100}" width="120" height="44" rx="22" fill="{PITCH}" stroke="{ACCENT}" stroke-width="2"/>
  <text x="{phone_x + 360}" y="{phone_y + 130}" font-family="{F_BOLD}" font-size="18" fill="{TEXT}" text-anchor="middle" letter-spacing="2">15 MIN</text>

  <!-- drill card -->
  <rect x="{phone_x + 60}" y="{phone_y + 180}" width="{phone_w - 120}" height="310" rx="16" fill="{PITCH}" stroke="{ACCENT}" stroke-width="2"/>
  <text x="{phone_x + 80}" y="{phone_y + 220}" font-family="{F_BOLD}" font-size="18" fill="{ACCENT}" letter-spacing="3">DRILL · 1v1</text>
  <text x="{phone_x + 80}" y="{phone_y + 258}" font-family="{F_BOLD}" font-size="26" fill="{TEXT}">Breakaway Pressure</text>
  <text x="{phone_x + 80}" y="{phone_y + 294}" font-family="{F_REG}" font-size="17" fill="{MUTED}">15 min · U14-U18 · Main block</text>

  <!-- mini diagram inside card -->
  <rect x="{phone_x + 80}" y="{phone_y + 314}" width="{phone_w - 160}" height="150" rx="10" fill="{BG}"/>
  <circle cx="{phone_x + 160}" cy="{phone_y + 390}" r="14" fill="{GK}"/>
  <circle cx="{phone_x + 310}" cy="{phone_y + 360}" r="12" fill="{TEXT}"/>
  <line x1="{phone_x + 295}" y1="{phone_y + 365}" x2="{phone_x + 180}" y2="{phone_y + 388}" stroke="{TEXT}" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arr-white)"/>
  <line x1="{phone_x + 155}" y1="{phone_y + 376}" x2="{phone_x + 155}" y2="{phone_y + 435}" stroke="{GK}" stroke-width="3" marker-end="url(#arr-gk)"/>

  <!-- second card peek -->
  <rect x="{phone_x + 60}" y="{phone_y + 510}" width="{phone_w - 120}" height="160" rx="16" fill="{PITCH}" opacity="0.5"/>
  <text x="{phone_x + 80}" y="{phone_y + 550}" font-family="{F_BOLD}" font-size="18" fill="{ACCENT}" letter-spacing="3" opacity="0.7">DRILL · 1v1</text>
  <text x="{phone_x + 80}" y="{phone_y + 588}" font-family="{F_BOLD}" font-size="26" fill="{TEXT}" opacity="0.7">Cutback Patience</text>

  <rect x="80" y="1150" width="60" height="6" fill="{ACCENT}"/>
  <text x="80" y="1220" font-family="{F_BOLD}" font-size="34" fill="{TEXT}">Pick by purpose. Run the session.</text>
'''
    slides.append(("slide-3-phone.svg", svg_doc(mockup)))

    return slides


# =========================================================
# Orchestration
# =========================================================
POSTS = [
    ("2026-05-01-quicktip",  day1_quicktip),
    ("2026-05-02-reflection", day2_reflection),
    ("2026-05-03-engage",    day3_engage),
    ("2026-05-04-story",     day4_story),
    ("2026-05-05-value",     day5_value),
    ("2026-05-06-quicktip",  day6_quicktip),
    ("2026-05-07-product",   day7_product),
]


def rasterize(svg_text: str) -> bytes:
    return bytes(
        resvg_py.svg_to_bytes(
            svg_string=svg_text,
            width=W,
            height=H,
            sans_serif_family="Helvetica",
        )
    )


def build_all():
    all_outputs: dict[str, list[Path]] = {}
    for folder_name, fn in POSTS:
        out_dir = POSTS_DIR / folder_name
        out_dir.mkdir(parents=True, exist_ok=True)
        slides = fn()
        paths: list[Path] = []
        for svg_name, svg_text in slides:
            svg_p = out_dir / svg_name
            svg_p.write_text(svg_text, encoding="utf-8")
            png_p = svg_p.with_suffix(".png")
            png_p.write_bytes(rasterize(svg_text))
            paths.append(png_p)
        all_outputs[folder_name] = paths
        print(f"{folder_name}: {len(paths)} slides -> {out_dir}")
    return all_outputs


if __name__ == "__main__":
    outputs = build_all()
    total = sum(len(v) for v in outputs.values())
    print(f"\nTotal: {total} PNGs generated")
