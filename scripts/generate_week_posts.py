"""Generate all Instagram slide PNGs for 2026-04-24 through 2026-04-30.

Outputs one folder per post under content/posts/YYYY-MM-DD-[type]/.
"""
from __future__ import annotations

from pathlib import Path
import resvg_py

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "content" / "posts"

# ---- palette ----
BG = "#0f3d2e"
PITCH = "#1a5c3f"
ACCENT = "#2ECC71"
TEXT = "#F5F5F0"
MUTED = "#9FBFAE"
GK = "#FFD700"
COACH = "#3498DB"
CONE = "#E67E22"
TENNIS = "#D4F542"

W, H = 1080, 1350
F_BOLD = 'sans-serif" font-weight="800'
F_REG = 'sans-serif" font-weight="400'
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
    return f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" ry="20" fill="{PITCH}"/>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" ry="20" fill="none" stroke="{TEXT}" stroke-width="3" opacity="0.25"/>'''


def drill_header(eyebrow: str, title: str) -> str:
    return f'''<text x="80" y="120" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="4">{eyebrow}</text>
    <text x="80" y="185" font-family="{F_BOLD}" font-size="58" fill="{TEXT}" letter-spacing="-1">{title}</text>'''


def takeaway(text: str) -> str:
    return f'''<rect x="80" y="1150" width="60" height="6" fill="{ACCENT}"/>
    <text x="80" y="1220" font-family="{F_BOLD}" font-size="38" fill="{TEXT}">{text}</text>'''


# =========================================================
# Day 1 — Engage: "What's the first thing you teach a young keeper?"
# =========================================================
def day1_engage():
    # Single slide: bold question on dark green with pitch-line motif at base
    body = f'''
  <!-- eyebrow -->
  <rect x="80" y="230" width="8" height="80" fill="{ACCENT}"/>
  <text x="120" y="280" font-family="{F_BOLD}" font-size="28" fill="{ACCENT}" letter-spacing="6">ENGAGE · COACHES' QUESTION</text>

  <!-- big question -->
  <text x="80" y="490" font-family="{F_BOLD}" font-size="94" fill="{TEXT}" letter-spacing="-2">What's the</text>
  <text x="80" y="600" font-family="{F_BOLD}" font-size="94" fill="{TEXT}" letter-spacing="-2">first thing</text>
  <text x="80" y="710" font-family="{F_BOLD}" font-size="94" fill="{ACCENT}" letter-spacing="-2">you teach</text>
  <text x="80" y="820" font-family="{F_BOLD}" font-size="94" fill="{TEXT}" letter-spacing="-2">a young keeper?</text>

  <!-- subline -->
  <line x1="80" y1="900" x2="240" y2="900" stroke="{TEXT}" stroke-width="3"/>
  <text x="80" y="970" font-family="{F_REG}" font-size="32" fill="{TEXT}">Comment below — one sentence is enough.</text>

  <!-- pitch stripe base -->
  <rect x="0" y="1120" width="{W}" height="180" fill="{PITCH}"/>
  <line x1="0" y1="1120" x2="{W}" y2="1120" stroke="{TEXT}" stroke-width="4" opacity="0.4"/>
  <rect x="380" y="1120" width="320" height="100" fill="none" stroke="{TEXT}" stroke-width="3" opacity="0.5"/>
  <circle cx="540" cy="1170" r="20" fill="{GK}" stroke="{BG}" stroke-width="3"/>
'''
    return [("slide-1.svg", svg_doc(body))]


# =========================================================
# Day 2 — Story: "A small detail most GK coaches miss"
# =========================================================
def day2_story():
    # Single: top-down of a keeper with "reset loop" arrows, quote "Watch the gaps between reps."
    px, py, pw, ph = 60, 360, 960, 660
    body = f'''
  {drill_header("STORY · A SMALL DETAIL", "Watch the gaps between reps.")}

  {pitch_frame(px, py, pw, ph)}

  <!-- keeper in set position at center -->
  <g transform="translate({W//2}, {py + ph//2 - 10})">
    <circle cx="0" cy="0" r="46" fill="{GK}" stroke="{BG}" stroke-width="4"/>
    <circle cx="-80" cy="25" r="18" fill="{GK}"/>
    <circle cx="80" cy="25" r="18" fill="{GK}"/>
    <line x1="-36" y1="15" x2="-70" y2="22" stroke="{GK}" stroke-width="9" stroke-linecap="round"/>
    <line x1="36" y1="15" x2="70" y2="22" stroke="{GK}" stroke-width="9" stroke-linecap="round"/>
    <text x="0" y="110" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">SET. HANDS UP. RESET.</text>
  </g>

  <!-- reset-loop arrows around the keeper -->
  <g fill="none" stroke="{ACCENT}" stroke-width="4" stroke-dasharray="10,10">
    <path d="M {W//2 + 140} {py + ph//2 - 10} A 200 200 0 0 1 {W//2 + 140} {py + ph//2 + 180}" marker-end="url(#arr-accent)"/>
    <path d="M {W//2 - 140} {py + ph//2 + 180} A 200 200 0 0 1 {W//2 - 140} {py + ph//2 - 10}" marker-end="url(#arr-accent)"/>
  </g>
  <text x="{W//2 + 220}" y="{py + ph//2 + 100}" font-family="{F_BOLD}" font-size="22" fill="{ACCENT}" letter-spacing="3">REP</text>
  <text x="{W//2 - 250}" y="{py + ph//2 + 100}" font-family="{F_BOLD}" font-size="22" fill="{ACCENT}" letter-spacing="3">RESET</text>

  {takeaway("The habit lives between the reps.")}
'''
    return [("slide-1.svg", svg_doc(body))]


# =========================================================
# Day 3 — Reflection: "Why we coach"
# =========================================================
def day3_reflection():
    body = f'''
  <!-- top tag -->
  <text x="{W//2}" y="280" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="8">WEEKLY REFLECTION</text>

  <!-- quote mark -->
  <text x="{W//2}" y="460" font-family="{F_BOLD}" font-size="160" fill="{ACCENT}" text-anchor="middle" opacity="0.5">&#8220;</text>

  <!-- quote lines -->
  <text x="{W//2}" y="620" font-family="{F_BOLD}" font-size="72" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">The scoreline</text>
  <text x="{W//2}" y="710" font-family="{F_BOLD}" font-size="72" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">is not the</text>
  <text x="{W//2}" y="800" font-family="{F_BOLD}" font-size="72" fill="{ACCENT}" text-anchor="middle" letter-spacing="-1">scoreboard.</text>

  <!-- divider and attribution -->
  <line x1="{W//2 - 60}" y1="880" x2="{W//2 + 60}" y2="880" stroke="{TEXT}" stroke-width="2" opacity="0.6"/>
  <text x="{W//2}" y="940" font-family="{F_ITAL}" font-size="26" fill="{MUTED}" text-anchor="middle" letter-spacing="3">— KEEPIX, on why we coach</text>
'''
    return [("slide-1.svg", svg_doc(body))]


# =========================================================
# Day 4 — Value: "Reading the Striker's Eyes" (4 slides)
# =========================================================
def day4_value():
    slides: list[tuple[str, str]] = []

    # Slide 1 — Hero
    hero = f'''
  <rect x="80" y="300" width="8" height="200" fill="{ACCENT}"/>
  <text x="120" y="335" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="6">BEFORE THE BALL IS STRUCK</text>
  <text x="120" y="480" font-family="{F_BOLD}" font-size="130" fill="{TEXT}" letter-spacing="-2">READING</text>
  <text x="120" y="610" font-family="{F_BOLD}" font-size="130" fill="{ACCENT}" letter-spacing="-2">THE STRIKER</text>
  <line x1="120" y1="720" x2="380" y2="720" stroke="{TEXT}" stroke-width="3"/>
  <text x="120" y="790" font-family="{F_REG}" font-size="34" fill="{TEXT}">Three cues good keepers read</text>
  <text x="120" y="838" font-family="{F_REG}" font-size="34" fill="{TEXT}">a half-second before contact.</text>
  <text x="120" y="960" font-family="{F_BOLD}" font-size="26" fill="{MUTED}" letter-spacing="4">EYES  ·  SHOULDER  ·  STANDING FOOT</text>
  <rect x="120" y="980" width="60" height="6" fill="{ACCENT}"/>
'''
    slides.append(("slide-1-hero.svg", svg_doc(hero)))

    # Slide 2 — Cue 1: Eyes
    eyes_body = f'''
  {drill_header("CUE 01 / THE EYES", "A flicker, not a stare.")}
  {pitch_frame(60, 260, 960, 820)}

  <!-- striker head (top-down bird's eye: circle + shoulders hint) -->
  <g transform="translate(540, 540)">
    <circle cx="0" cy="0" r="60" fill="{TEXT}"/>
    <!-- eyes -->
    <circle cx="-20" cy="-8" r="6" fill="{BG}"/>
    <circle cx="20" cy="-8" r="6" fill="{BG}"/>
    <!-- eye glance direction (mint arrow to corner) -->
    <line x1="22" y1="-8" x2="160" y2="-90" stroke="{ACCENT}" stroke-width="4" marker-end="url(#arr-accent)"/>
  </g>
  <text x="780" y="430" font-family="{F_BOLD}" font-size="22" fill="{ACCENT}" letter-spacing="3">BRIEF GLANCE</text>
  <text x="780" y="460" font-family="{F_BOLD}" font-size="22" fill="{ACCENT}" letter-spacing="3">TO TARGET</text>

  <!-- keeper reading in peripheral (yellow circle below) -->
  <circle cx="540" cy="900" r="40" fill="{GK}" stroke="{BG}" stroke-width="4"/>
  <text x="540" y="980" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">KEEPER (PERIPHERAL READ)</text>

  <!-- label for top figure -->
  <text x="540" y="370" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">STRIKER</text>

  {takeaway("Catch the flicker. Don't lock on.")}
'''
    slides.append(("slide-2-eyes.svg", svg_doc(eyes_body)))

    # Slide 3 — Cue 2: Shoulder
    shoulder_body = f'''
  {drill_header("CUE 02 / THE SHOULDER", "Closed = near. Open = far.")}
  {pitch_frame(60, 260, 960, 820)}

  <!-- closed shoulder (left) -->
  <g transform="translate(310, 630)">
    <ellipse cx="0" cy="0" rx="100" ry="30" fill="{TEXT}"/>
    <circle cx="0" cy="-55" r="35" fill="{TEXT}"/>
    <!-- arrow indicating near-post direction -->
    <line x1="-80" y1="30" x2="-160" y2="140" stroke="{ACCENT}" stroke-width="5" marker-end="url(#arr-accent)"/>
    <text x="0" y="120" font-family="{F_BOLD}" font-size="24" fill="{TEXT}" text-anchor="middle" letter-spacing="3">CLOSED</text>
    <text x="0" y="152" font-family="{F_BOLD}" font-size="22" fill="{ACCENT}" text-anchor="middle" letter-spacing="2">near post</text>
  </g>

  <!-- open shoulder (right) -->
  <g transform="translate(770, 630)">
    <ellipse cx="0" cy="0" rx="100" ry="30" fill="{TEXT}" transform="rotate(25)"/>
    <circle cx="0" cy="-55" r="35" fill="{TEXT}"/>
    <!-- arrow indicating far-post direction -->
    <line x1="80" y1="50" x2="180" y2="150" stroke="{ACCENT}" stroke-width="5" marker-end="url(#arr-accent)"/>
    <text x="0" y="120" font-family="{F_BOLD}" font-size="24" fill="{TEXT}" text-anchor="middle" letter-spacing="3">OPEN</text>
    <text x="0" y="152" font-family="{F_BOLD}" font-size="22" fill="{ACCENT}" text-anchor="middle" letter-spacing="2">far post</text>
  </g>

  <!-- divider -->
  <line x1="540" y1="360" x2="540" y2="940" stroke="{TEXT}" stroke-width="2" stroke-dasharray="6,6" opacity="0.4"/>

  <text x="310" y="380" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">FRONT SHOULDER</text>
  <text x="770" y="380" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">FRONT SHOULDER</text>

  {takeaway("Tell, not law — read in layers.")}
'''
    slides.append(("slide-3-shoulder.svg", svg_doc(shoulder_body)))

    # Slide 4 — Cue 3: Standing foot
    foot_body = f'''
  {drill_header("CUE 03 / THE STANDING FOOT", "The most reliable tell.")}
  {pitch_frame(60, 260, 960, 820)}

  <!-- Left case: foot AHEAD of ball -> driven shot -->
  <g transform="translate(310, 620)">
    <!-- ball -->
    <circle cx="0" cy="60" r="22" fill="{TEXT}" stroke="{BG}" stroke-width="2"/>
    <!-- standing foot ahead -->
    <ellipse cx="0" cy="-20" rx="40" ry="18" fill="{CONE}" opacity="0.9"/>
    <text x="0" y="-60" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">FOOT AHEAD</text>
    <!-- downward/low arrow -->
    <line x1="60" y1="60" x2="170" y2="130" stroke="{ACCENT}" stroke-width="5" marker-end="url(#arr-accent)"/>
    <text x="0" y="150" font-family="{F_BOLD}" font-size="24" fill="{TEXT}" text-anchor="middle" letter-spacing="3">LOW &amp; DRIVEN</text>
  </g>

  <!-- Right case: foot LEVEL with ball -> lifted/placed -->
  <g transform="translate(770, 620)">
    <circle cx="0" cy="60" r="22" fill="{TEXT}" stroke="{BG}" stroke-width="2"/>
    <ellipse cx="0" cy="60" rx="40" ry="18" fill="{CONE}" opacity="0.9"/>
    <text x="0" y="20" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">FOOT LEVEL</text>
    <!-- upward/placed arrow -->
    <line x1="60" y1="40" x2="170" y2="-20" stroke="{ACCENT}" stroke-width="5" marker-end="url(#arr-accent)"/>
    <text x="0" y="150" font-family="{F_BOLD}" font-size="24" fill="{TEXT}" text-anchor="middle" letter-spacing="3">LIFTED &amp; PLACED</text>
  </g>

  <line x1="540" y1="360" x2="540" y2="940" stroke="{TEXT}" stroke-width="2" stroke-dasharray="6,6" opacity="0.4"/>

  {takeaway("Learn this last — trust it most.")}
'''
    slides.append(("slide-4-foot.svg", svg_doc(foot_body)))

    return slides


# =========================================================
# Day 5 — Quick Tip: "30-second warm-up cue"
# =========================================================
def day5_quicktip():
    px, py, pw, ph = 60, 340, 960, 680
    body = f'''
  {drill_header("QUICK TIP / 30 SECONDS", "Hop. Set. Reset.")}

  {pitch_frame(px, py, pw, ph)}

  <!-- GK in the middle with motion lines and a dashed loop -->
  <circle cx="{W//2}" cy="{py + ph//2}" r="44" fill="{GK}" stroke="{BG}" stroke-width="4"/>

  <!-- hop motion lines (small springs above) -->
  <g stroke="{GK}" stroke-width="4" fill="none" stroke-linecap="round">
    <path d="M {W//2 - 60} {py + 130} q 10 -20 20 0"/>
    <path d="M {W//2 - 20} {py + 130} q 10 -20 20 0"/>
    <path d="M {W//2 + 20} {py + 130} q 10 -20 20 0"/>
  </g>
  <text x="{W//2}" y="{py + 100}" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">HOP · HOP · HOP</text>

  <!-- set hands -->
  <circle cx="{W//2 - 80}" cy="{py + ph//2 + 25}" r="16" fill="{GK}"/>
  <circle cx="{W//2 + 80}" cy="{py + ph//2 + 25}" r="16" fill="{GK}"/>
  <line x1="{W//2 - 38}" y1="{py + ph//2 + 18}" x2="{W//2 - 70}" y2="{py + ph//2 + 22}" stroke="{GK}" stroke-width="9" stroke-linecap="round"/>
  <line x1="{W//2 + 38}" y1="{py + ph//2 + 18}" x2="{W//2 + 70}" y2="{py + ph//2 + 22}" stroke="{GK}" stroke-width="9" stroke-linecap="round"/>

  <!-- dashed reset loop -->
  <g fill="none" stroke="{ACCENT}" stroke-width="4" stroke-dasharray="10,10">
    <path d="M {W//2 + 130} {py + ph//2 + 30} A 180 140 0 0 1 {W//2 + 130} {py + ph//2 - 100}" marker-end="url(#arr-accent)"/>
  </g>
  <text x="{W//2 + 220}" y="{py + ph//2 - 30}" font-family="{F_BOLD}" font-size="22" fill="{ACCENT}" letter-spacing="3">RESET</text>

  <!-- stopwatch label -->
  <text x="{W//2}" y="{py + ph - 40}" font-family="{F_BOLD}" font-size="72" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">30s</text>
  <text x="{W//2}" y="{py + ph - 10}" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">EVERY SESSION · SAME SPOT</text>

  {takeaway("Make it a ritual, not a drill.")}
'''
    return [("slide-1.svg", svg_doc(body))]


# =========================================================
# Day 6 — Product: "100 Drills, Organized by Purpose" (3 slides)
# =========================================================
def day6_product():
    slides: list[tuple[str, str]] = []

    # Slide 1 — Hero
    hero = f'''
  <rect x="80" y="300" width="8" height="200" fill="{ACCENT}"/>
  <text x="120" y="335" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="6">THE KEEPIX DRILL LIBRARY</text>
  <text x="120" y="490" font-family="{F_BOLD}" font-size="200" fill="{TEXT}" letter-spacing="-4">100</text>
  <text x="120" y="600" font-family="{F_BOLD}" font-size="90" fill="{ACCENT}" letter-spacing="-2">DRILLS</text>
  <line x1="120" y1="700" x2="380" y2="700" stroke="{TEXT}" stroke-width="3"/>
  <text x="120" y="770" font-family="{F_REG}" font-size="34" fill="{TEXT}">Organised by purpose — not</text>
  <text x="120" y="818" font-family="{F_REG}" font-size="34" fill="{TEXT}">whatever you happened to remember.</text>
  <text x="120" y="960" font-family="{F_BOLD}" font-size="24" fill="{MUTED}" letter-spacing="4">9 CATEGORIES · FILTER BY AGE, PHASE, TIME</text>
  <rect x="120" y="980" width="60" height="6" fill="{ACCENT}"/>
'''
    slides.append(("slide-1-hero.svg", svg_doc(hero)))

    # Slide 2 — 3x3 grid of categories
    cats = [
        "FOOTWORK", "HANDLING", "SET POSITION",
        "CROSSING", "1v1", "DISTRIBUTION",
        "RECOVERY", "COMMUNICATION", "MATCH SIM",
    ]
    grid_parts = []
    cols, rows = 3, 3
    cw, ch = 290, 190
    gap_x, gap_y = 20, 20
    grid_w = cols * cw + (cols - 1) * gap_x
    start_x = (W - grid_w) // 2
    start_y = 330
    for i, name in enumerate(cats):
        r, c = divmod(i, cols)
        x = start_x + c * (cw + gap_x)
        y = start_y + r * (ch + gap_y)
        grid_parts.append(
            f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{PITCH}" stroke="{ACCENT}" stroke-width="2" stroke-opacity="0.35"/>'
            f'<circle cx="{x + cw//2}" cy="{y + ch//2 - 20}" r="10" fill="{ACCENT}"/>'
            f'<text x="{x + cw//2}" y="{y + ch//2 + 35}" font-family="{F_BOLD}" font-size="22" fill="{TEXT}" text-anchor="middle" letter-spacing="2">{name}</text>'
        )

    grid_body = f'''
  <text x="80" y="120" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="4">PURPOSE-BASED CATEGORIES</text>
  <text x="80" y="195" font-family="{F_BOLD}" font-size="58" fill="{TEXT}" letter-spacing="-1">Pick by what you need to fix.</text>
  {"".join(grid_parts)}
  {takeaway("Nine tiles. Every session plan starts here.")}
'''
    slides.append(("slide-2-categories.svg", svg_doc(grid_body)))

    # Slide 3 — Phone mockup
    # Phone body centered
    phone_x, phone_y, phone_w, phone_h = 280, 360, 520, 820
    mockup = f'''
  <text x="80" y="120" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="4">PITCHSIDE, NOT DESK-SIDE</text>
  <text x="80" y="195" font-family="{F_BOLD}" font-size="58" fill="{TEXT}" letter-spacing="-1">One drill card. Ready to run.</text>

  <!-- phone body -->
  <rect x="{phone_x}" y="{phone_y}" width="{phone_w}" height="{phone_h}" rx="50" ry="50" fill="#0a2d22" stroke="{TEXT}" stroke-width="4"/>
  <rect x="{phone_x + 180}" y="{phone_y + 20}" width="160" height="16" rx="8" fill="{TEXT}" opacity="0.2"/>

  <!-- screen bg -->
  <rect x="{phone_x + 30}" y="{phone_y + 70}" width="{phone_w - 60}" height="{phone_h - 100}" rx="24" ry="24" fill="{BG}"/>

  <!-- filter chips row -->
  <rect x="{phone_x + 60}" y="{phone_y + 100}" width="120" height="44" rx="22" fill="{ACCENT}"/>
  <text x="{phone_x + 120}" y="{phone_y + 130}" font-family="{F_BOLD}" font-size="18" fill="{BG}" text-anchor="middle" letter-spacing="2">U14</text>

  <rect x="{phone_x + 190}" y="{phone_y + 100}" width="170" height="44" rx="22" fill="{PITCH}" stroke="{ACCENT}" stroke-width="2"/>
  <text x="{phone_x + 275}" y="{phone_y + 130}" font-family="{F_BOLD}" font-size="18" fill="{TEXT}" text-anchor="middle" letter-spacing="2">CROSSING</text>

  <rect x="{phone_x + 370}" y="{phone_y + 100}" width="110" height="44" rx="22" fill="{PITCH}" stroke="{ACCENT}" stroke-width="2"/>
  <text x="{phone_x + 425}" y="{phone_y + 130}" font-family="{F_BOLD}" font-size="18" fill="{TEXT}" text-anchor="middle" letter-spacing="2">20 MIN</text>

  <!-- selected drill card -->
  <rect x="{phone_x + 60}" y="{phone_y + 180}" width="{phone_w - 120}" height="300" rx="16" fill="{PITCH}" stroke="{ACCENT}" stroke-width="2"/>
  <text x="{phone_x + 80}" y="{phone_y + 220}" font-family="{F_BOLD}" font-size="20" fill="{ACCENT}" letter-spacing="3">DRILL · CROSSING</text>
  <text x="{phone_x + 80}" y="{phone_y + 260}" font-family="{F_BOLD}" font-size="28" fill="{TEXT}">High Ball Under Pressure</text>
  <text x="{phone_x + 80}" y="{phone_y + 300}" font-family="{F_REG}" font-size="18" fill="{MUTED}">20 min · U14-U18 · Main block</text>

  <!-- mini diagram inside card -->
  <rect x="{phone_x + 80}" y="{phone_y + 320}" width="{phone_w - 160}" height="140" rx="10" fill="{BG}"/>
  <circle cx="{phone_x + 180}" cy="{phone_y + 390}" r="14" fill="{GK}"/>
  <circle cx="{phone_x + 300}" cy="{phone_y + 370}" r="12" fill="{COACH}"/>
  <polygon points="{phone_x + 380},{phone_y + 420} {phone_x + 400},{phone_y + 420} {phone_x + 390},{phone_y + 395}" fill="{CONE}"/>
  <line x1="{phone_x + 290}" y1="{phone_y + 380}" x2="{phone_x + 200}" y2="{phone_y + 390}" stroke="{TEXT}" stroke-width="2" stroke-dasharray="5,5"/>

  <!-- second (fainter) card peek -->
  <rect x="{phone_x + 60}" y="{phone_y + 500}" width="{phone_w - 120}" height="160" rx="16" fill="{PITCH}" opacity="0.5"/>
  <text x="{phone_x + 80}" y="{phone_y + 540}" font-family="{F_BOLD}" font-size="20" fill="{ACCENT}" letter-spacing="3" opacity="0.7">DRILL · CROSSING</text>
  <text x="{phone_x + 80}" y="{phone_y + 580}" font-family="{F_BOLD}" font-size="28" fill="{TEXT}" opacity="0.7">Contested Corner Claim</text>

  {takeaway("Pick by purpose. Run the session.")}
'''
    slides.append(("slide-3-phone.svg", svg_doc(mockup)))

    return slides


# =========================================================
# Day 7 — Value: "What 'being set' really means" (4 slides)
# =========================================================
def day7_value():
    slides: list[tuple[str, str]] = []

    # Slide 1 — Hero
    hero = f'''
  <rect x="80" y="300" width="8" height="200" fill="{ACCENT}"/>
  <text x="120" y="335" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="6">THE MOST MISUNDERSTOOD CUE</text>
  <text x="120" y="490" font-family="{F_BOLD}" font-size="150" fill="{TEXT}" letter-spacing="-3">BEING</text>
  <text x="120" y="640" font-family="{F_BOLD}" font-size="150" fill="{ACCENT}" letter-spacing="-3">SET.</text>
  <line x1="120" y1="740" x2="380" y2="740" stroke="{TEXT}" stroke-width="3"/>
  <text x="120" y="810" font-family="{F_REG}" font-size="34" fill="{TEXT}">It's a shape, not a pause.</text>
  <text x="120" y="858" font-family="{F_REG}" font-size="34" fill="{TEXT}">Three things we check, every time.</text>
  <text x="120" y="980" font-family="{F_BOLD}" font-size="26" fill="{MUTED}" letter-spacing="4">BALANCE  ·  STANCE  ·  CENTRE OF MASS</text>
  <rect x="120" y="1000" width="60" height="6" fill="{ACCENT}"/>
'''
    slides.append(("slide-1-hero.svg", svg_doc(hero)))

    # Slide 2 — Balance (side-on)
    balance = f'''
  {drill_header("CHECK 01 / BALANCE", "Weight on the balls of the feet.")}
  {pitch_frame(60, 260, 960, 820)}

  <!-- side-on silhouette -->
  <g transform="translate({W//2}, 700)">
    <!-- head -->
    <circle cx="0" cy="-180" r="40" fill="{TEXT}"/>
    <!-- torso leaning slightly forward -->
    <path d="M -40 -140 L 30 -140 L 40 0 L -30 0 Z" fill="{TEXT}"/>
    <!-- arms forward -->
    <path d="M 30 -130 Q 90 -80 100 0" stroke="{TEXT}" stroke-width="18" fill="none" stroke-linecap="round"/>
    <path d="M -40 -130 Q -100 -80 -100 0" stroke="{TEXT}" stroke-width="18" fill="none" stroke-linecap="round"/>
    <!-- legs bent -->
    <path d="M -20 0 L -30 120" stroke="{TEXT}" stroke-width="20" stroke-linecap="round"/>
    <path d="M 30 0 L 40 120" stroke="{TEXT}" stroke-width="20" stroke-linecap="round"/>
    <!-- ground line -->
    <line x1="-200" y1="125" x2="200" y2="125" stroke="{MUTED}" stroke-width="3"/>
    <!-- feet shadow (weight forward) -->
    <ellipse cx="-30" cy="125" rx="44" ry="8" fill="{ACCENT}" opacity="0.7"/>
    <ellipse cx="40" cy="125" rx="44" ry="8" fill="{ACCENT}" opacity="0.7"/>
    <!-- forward arrow -->
    <line x1="0" y1="-180" x2="160" y2="-160" stroke="{ACCENT}" stroke-width="5" marker-end="url(#arr-accent)"/>
    <text x="180" y="-155" font-family="{F_BOLD}" font-size="22" fill="{ACCENT}" letter-spacing="3">WEIGHT FORWARD</text>
  </g>

  {takeaway("A finger shouldn't push them back.")}
'''
    slides.append(("slide-2-balance.svg", svg_doc(balance)))

    # Slide 3 — Stance width (top-down)
    stance = f'''
  {drill_header("CHECK 02 / STANCE WIDTH", "Shoulder-width. Alive.")}
  {pitch_frame(60, 260, 960, 820)}

  <!-- top-down view: yellow circle (head) with two feet ovals -->
  <g transform="translate({W//2}, 620)">
    <!-- mint guide box indicating shoulder width -->
    <rect x="-110" y="-90" width="220" height="180" rx="8" fill="none" stroke="{ACCENT}" stroke-width="3" stroke-dasharray="10,10"/>
    <text x="0" y="-110" font-family="{F_BOLD}" font-size="22" fill="{ACCENT}" text-anchor="middle" letter-spacing="3">SHOULDER WIDTH</text>

    <!-- head -->
    <circle cx="0" cy="0" r="40" fill="{GK}" stroke="{BG}" stroke-width="3"/>
    <!-- feet -->
    <ellipse cx="-85" cy="70" rx="24" ry="40" fill="{TEXT}"/>
    <ellipse cx="85" cy="70" rx="24" ry="40" fill="{TEXT}"/>
  </g>

  <!-- annotations left/right -->
  <text x="190" y="620" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" letter-spacing="3" text-anchor="end">TOO NARROW</text>
  <text x="190" y="650" font-family="{F_REG}" font-size="20" fill="{TEXT}" text-anchor="end">lateral collapses</text>

  <text x="890" y="620" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" letter-spacing="3">TOO WIDE</text>
  <text x="890" y="650" font-family="{F_REG}" font-size="20" fill="{TEXT}">first step dies</text>

  {takeaway("Slightly wider for taller keepers.")}
'''
    slides.append(("slide-3-stance.svg", svg_doc(stance)))

    # Slide 4 — Centre of mass (side-on)
    com = f'''
  {drill_header("CHECK 03 / CENTRE OF MASS", "First move across, not up.")}
  {pitch_frame(60, 260, 960, 820)}

  <g transform="translate({W//2}, 700)">
    <!-- head -->
    <circle cx="0" cy="-180" r="40" fill="{TEXT}"/>
    <!-- torso -->
    <path d="M -40 -140 L 30 -140 L 40 0 L -30 0 Z" fill="{TEXT}"/>
    <!-- arms out -->
    <path d="M 30 -130 Q 90 -90 110 -20" stroke="{TEXT}" stroke-width="18" fill="none" stroke-linecap="round"/>
    <path d="M -40 -130 Q -100 -90 -110 -20" stroke="{TEXT}" stroke-width="18" fill="none" stroke-linecap="round"/>
    <!-- hips low: bent knees -->
    <path d="M -20 0 L -40 80 L -30 120" stroke="{TEXT}" stroke-width="20" fill="none" stroke-linecap="round"/>
    <path d="M 30 0 L 50 80 L 40 120" stroke="{TEXT}" stroke-width="20" fill="none" stroke-linecap="round"/>
    <!-- hip line marker -->
    <line x1="-150" y1="0" x2="150" y2="0" stroke="{ACCENT}" stroke-width="3" stroke-dasharray="10,10"/>
    <text x="170" y="8" font-family="{F_BOLD}" font-size="22" fill="{ACCENT}" letter-spacing="3">HIP LINE</text>
    <!-- horizontal explosion arrows -->
    <line x1="-170" y1="-20" x2="-280" y2="-20" stroke="{GK}" stroke-width="6" marker-end="url(#arr-gk)"/>
    <line x1="170" y1="-20" x2="280" y2="-20" stroke="{GK}" stroke-width="6" marker-end="url(#arr-gk)"/>
    <text x="0" y="165" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">LOW &amp; LATERAL</text>
  </g>

  {takeaway("If first move is up, set is too tall.")}
'''
    slides.append(("slide-4-centre-of-mass.svg", svg_doc(com)))

    return slides


# =========================================================
# Orchestration
# =========================================================
POSTS = [
    ("2026-04-24-engage", day1_engage),
    ("2026-04-25-story", day2_story),
    ("2026-04-26-reflection", day3_reflection),
    ("2026-04-27-value", day4_value),
    ("2026-04-28-quicktip", day5_quicktip),
    ("2026-04-29-product", day6_product),
    ("2026-04-30-value", day7_value),
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
