"""Generate all Instagram slide PNGs for 2026-05-08 through 2026-05-14."""
from __future__ import annotations
from pathlib import Path
import resvg_py

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "content" / "posts"

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


def pitch_frame(x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" ry="20" fill="{PITCH}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" ry="20" fill="none"'
            f' stroke="{TEXT}" stroke-width="3" opacity="0.25"/>')


def drill_header(eyebrow, title):
    return (f'<text x="80" y="120" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="4">{eyebrow}</text>'
            f'<text x="80" y="185" font-family="{F_BOLD}" font-size="58" fill="{TEXT}" letter-spacing="-1">{title}</text>')


def takeaway(text):
    return (f'<rect x="80" y="1150" width="60" height="6" fill="{ACCENT}"/>'
            f'<text x="80" y="1220" font-family="{F_BOLD}" font-size="38" fill="{TEXT}">{text}</text>')


# =========================================================
# Day 1 (5/8 Fri) — Quick Tip: "5-second feedback"
# =========================================================
def day1_quicktip():
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">QUICK TIP · COACHING FEEDBACK</text>

  <!-- hero -->
  <text x="{W//2}" y="430" font-family="{F_BOLD}" font-size="220" fill="{ACCENT}" text-anchor="middle" letter-spacing="-6">5 SEC</text>

  <line x1="160" y1="480" x2="{W-160}" y2="480" stroke="{TEXT}" stroke-width="2" opacity="0.3"/>

  <!-- format 1 -->
  <text x="120" y="578" font-family="{F_BOLD}" font-size="28" fill="{ACCENT}" letter-spacing="2">01  NAME + FIX</text>
  <text x="120" y="618" font-family="{F_REG}" font-size="26" fill="{MUTED}">"Feet — wider before the ball."</text>

  <!-- format 2 -->
  <text x="120" y="716" font-family="{F_BOLD}" font-size="28" fill="{ACCENT}" letter-spacing="2">02  QUESTION + PAUSE</text>
  <text x="120" y="756" font-family="{F_REG}" font-size="26" fill="{MUTED}">"Where were your hands?" Then wait.</text>

  <!-- format 3 -->
  <text x="120" y="854" font-family="{F_BOLD}" font-size="28" fill="{ACCENT}" letter-spacing="2">03  SILENCE + NEXT REP</text>
  <text x="120" y="894" font-family="{F_REG}" font-size="26" fill="{MUTED}">Load the ball. Move on. Fast.</text>

  <rect x="80" y="1150" width="60" height="6" fill="{ACCENT}"/>
  <text x="80" y="1220" font-family="{F_BOLD}" font-size="36" fill="{TEXT}">One sentence. Then the next ball.</text>
'''
    return [("slide-1.svg", svg_doc(body))]


# =========================================================
# Day 2 (5/9 Sat) — Reflection: "Worst sessions teach most"
# =========================================================
def day2_reflection():
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="24" fill="{ACCENT}" text-anchor="middle" letter-spacing="8">KEEPIX · WEEKLY REFLECTION</text>

  <text x="{W//2}" y="430" font-family="{F_BOLD}" font-size="200" fill="{ACCENT}" text-anchor="middle" opacity="0.25">&#8220;</text>

  <text x="{W//2}" y="530" font-family="{F_BOLD}" font-size="66" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">The sessions we</text>
  <text x="{W//2}" y="630" font-family="{F_BOLD}" font-size="66" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">control too tightly</text>
  <text x="{W//2}" y="730" font-family="{F_BOLD}" font-size="66" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">sometimes train</text>
  <text x="{W//2}" y="830" font-family="{F_BOLD}" font-size="66" fill="{ACCENT}" text-anchor="middle" letter-spacing="-1">the plan, not the keeper.</text>

  <rect x="{W//2 - 80}" y="900" width="160" height="5" fill="{ACCENT}"/>
  <text x="{W//2}" y="970" font-family="{F_ITAL}" font-size="28" fill="{MUTED}" text-anchor="middle" letter-spacing="2">— a wet Tuesday in March</text>
'''
    return [("slide-1.svg", svg_doc(body))]


# =========================================================
# Day 3 (5/10 Sun) — Engage: "Drill you keep coming back to"
# =========================================================
def day3_engage():
    body = f'''
  <rect x="80" y="230" width="8" height="80" fill="{ACCENT}"/>
  <text x="120" y="280" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="5">ENGAGE · COACHES' QUESTION</text>

  <text x="80" y="470" font-family="{F_BOLD}" font-size="82" fill="{TEXT}" letter-spacing="-2">What's the drill</text>
  <text x="80" y="570" font-family="{F_BOLD}" font-size="82" fill="{TEXT}" letter-spacing="-2">you keep</text>
  <text x="80" y="670" font-family="{F_BOLD}" font-size="82" fill="{ACCENT}" letter-spacing="-2">coming back to?</text>

  <line x1="80" y1="740" x2="300" y2="740" stroke="{TEXT}" stroke-width="2" opacity="0.4"/>

  <text x="80" y="820" font-family="{F_REG}" font-size="30" fill="{MUTED}">Not the flashiest one.</text>
  <text x="80" y="866" font-family="{F_REG}" font-size="30" fill="{MUTED}">The one that always works.</text>

  <rect x="80" y="1130" width="60" height="6" fill="{ACCENT}"/>
  <text x="80" y="1200" font-family="{F_BOLD}" font-size="34" fill="{TEXT}">Name it below — and tell us why.</text>
'''
    return [("slide-1.svg", svg_doc(body))]


# =========================================================
# Day 4 (5/11 Mon) — Story: "Planned differently"
# =========================================================
def day4_story():
    body = f'''
  <rect x="80" y="110" width="8" height="60" fill="{ACCENT}"/>
  <text x="120" y="150" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="5">STORY · FROM THE PITCH</text>

  <text x="80" y="300" font-family="{F_BOLD}" font-size="68" fill="{TEXT}" letter-spacing="-1">Same drills.</text>
  <text x="80" y="386" font-family="{F_BOLD}" font-size="68" fill="{TEXT}" letter-spacing="-1">Same volume.</text>
  <text x="80" y="530" font-family="{F_BOLD}" font-size="68" fill="{ACCENT}" letter-spacing="-1">Different order.</text>
  <text x="80" y="616" font-family="{F_BOLD}" font-size="68" fill="{ACCENT}" letter-spacing="-1">Different keeper.</text>

  <line x1="80" y1="700" x2="400" y2="700" stroke="{TEXT}" stroke-width="2" opacity="0.3"/>

  <!-- mini session-order diagram -->
  <rect x="80" y="750" width="880" height="120" rx="16" fill="{PITCH}"/>

  <!-- blocks: old order -->
  <rect x="110" y="775" width="160" height="70" rx="10" fill="{ACCENT}" opacity="0.7"/>
  <text x="190" y="817" font-family="{F_BOLD}" font-size="20" fill="{BG}" text-anchor="middle">WARM-UP</text>
  <rect x="290" y="775" width="160" height="70" rx="10" fill="{COACH}" opacity="0.7"/>
  <text x="370" y="817" font-family="{F_BOLD}" font-size="20" fill="{BG}" text-anchor="middle">TECHNICAL</text>
  <rect x="470" y="775" width="160" height="70" rx="10" fill="{GK}" opacity="0.7"/>
  <text x="550" y="817" font-family="{F_BOLD}" font-size="18" fill="{BG}" text-anchor="middle">TACTICAL</text>
  <rect x="650" y="775" width="160" height="70" rx="10" fill="{MUTED}" opacity="0.7"/>
  <text x="730" y="817" font-family="{F_BOLD}" font-size="18" fill="{BG}" text-anchor="middle">COOL-DOWN</text>

  <!-- shuffle arrows -->
  <text x="{W//2}" y="930" font-family="{F_BOLD}" font-size="28" fill="{MUTED}" text-anchor="middle" letter-spacing="3">SWAP THE ORDER TWICE A WEEK</text>

  {takeaway("Train the keeper, not just the plan.")}
'''
    return [("slide-1.svg", svg_doc(body))]


# =========================================================
# Day 5 (5/12 Tue) — Value: "Footwork: Three patterns" (4 slides)
# =========================================================
def day5_value():
    slides = []

    # Slide 1 — Hero
    hero = f'''
  <rect x="80" y="300" width="8" height="200" fill="{ACCENT}"/>
  <text x="120" y="335" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="6">THREE PATTERNS · EVERY KEEPER NEEDS</text>
  <text x="120" y="530" font-family="{F_BOLD}" font-size="170" fill="{TEXT}" letter-spacing="-4">FOOT</text>
  <text x="120" y="700" font-family="{F_BOLD}" font-size="170" fill="{ACCENT}" letter-spacing="-4">WORK</text>
  <line x1="120" y1="790" x2="380" y2="790" stroke="{TEXT}" stroke-width="3"/>
  <text x="120" y="860" font-family="{F_REG}" font-size="34" fill="{TEXT}">Most keepers default to one.</text>
  <text x="120" y="908" font-family="{F_REG}" font-size="34" fill="{TEXT}">All three solve different problems.</text>
  <text x="120" y="1020" font-family="{F_BOLD}" font-size="24" fill="{MUTED}" letter-spacing="4">SHUFFLE  ·  CROSS-STEP  ·  DROP-STEP</text>
  <rect x="120" y="1040" width="60" height="6" fill="{ACCENT}"/>
'''
    slides.append(("slide-1-hero.svg", svg_doc(hero)))

    # Slide 2 — Shuffle & Set
    px, py, pw, ph = 60, 260, 960, 820
    shuffle = f'''
  {drill_header("PATTERN 01 / THE SHUFFLE &amp; SET", "Short lateral. Finish in position.")}
  {pitch_frame(px, py, pw, ph)}

  <!-- GK start position (left) -->
  <circle cx="{px + 200}" cy="{py + ph//2}" r="36" fill="{GK}" stroke="{BG}" stroke-width="4"/>
  <text x="{px + 200}" y="{py + ph//2 - 56}" font-family="{F_BOLD}" font-size="20" fill="{MUTED}" text-anchor="middle" letter-spacing="3">START</text>

  <!-- footstep trail (shuffle) -->
  <ellipse cx="{px + 310}" cy="{py + ph//2 + 42}" rx="18" ry="10" fill="{GK}" opacity="0.5"/>
  <ellipse cx="{px + 380}" cy="{py + ph//2 - 30}" rx="18" ry="10" fill="{GK}" opacity="0.5"/>
  <ellipse cx="{px + 450}" cy="{py + ph//2 + 42}" rx="18" ry="10" fill="{GK}" opacity="0.5"/>
  <ellipse cx="{px + 520}" cy="{py + ph//2 - 30}" rx="18" ry="10" fill="{GK}" opacity="0.5"/>

  <!-- GK end position (set) -->
  <circle cx="{px + 640}" cy="{py + ph//2}" r="36" fill="{GK}" stroke="{ACCENT}" stroke-width="5"/>
  <text x="{px + 640}" y="{py + ph//2 - 56}" font-family="{F_BOLD}" font-size="20" fill="{ACCENT}" text-anchor="middle" letter-spacing="3">SET</text>

  <!-- distance label -->
  <line x1="{px + 200}" y1="{py + ph - 80}" x2="{px + 640}" y2="{py + ph - 80}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="{px + 420}" y="{py + ph - 40}" font-family="{F_BOLD}" font-size="24" fill="{MUTED}" text-anchor="middle" letter-spacing="3">1 – 3 m</text>

  <!-- ball arrival arrow from right -->
  <line x1="{px + pw - 80}" y1="{py + ph//2}" x2="{px + 700}" y2="{py + ph//2}" stroke="{TEXT}" stroke-width="5" stroke-dasharray="12,8" marker-end="url(#arr-white)"/>
  <text x="{px + pw - 60}" y="{py + ph//2 - 24}" font-family="{F_BOLD}" font-size="20" fill="{MUTED}" letter-spacing="3">BALL</text>

  {takeaway("Most keepers do this well. Few do it tired.")}
'''
    slides.append(("slide-2-shuffle.svg", svg_doc(shuffle)))

    # Slide 3 — Cross-step
    crossstep = f'''
  {drill_header("PATTERN 02 / THE CROSS-STEP", "Wider coverage. Faster across.")}
  {pitch_frame(px, py, pw, ph)}

  <!-- GK start (centre) -->
  <circle cx="{px + pw//2}" cy="{py + ph//2}" r="36" fill="{GK}" stroke="{BG}" stroke-width="4"/>
  <text x="{px + pw//2}" y="{py + ph//2 - 56}" font-family="{F_BOLD}" font-size="20" fill="{MUTED}" text-anchor="middle" letter-spacing="3">START</text>

  <!-- cross-step path (legs crossing) -->
  <path d="M {px+pw//2+36} {py+ph//2} C {px+pw//2+160} {py+ph//2-80} {px+pw//2+260} {py+ph//2+80} {px+pw//2+380} {py+ph//2}" stroke="{GK}" stroke-width="5" fill="none" stroke-dasharray="10,6"/>
  <path d="M {px+pw//2+36} {py+ph//2} C {px+pw//2+160} {py+ph//2+80} {px+pw//2+260} {py+ph//2-80} {px+pw//2+380} {py+ph//2}" stroke="{GK}" stroke-width="3" fill="none" stroke-dasharray="6,8" opacity="0.5"/>

  <!-- GK end + recovery arrow back to set -->
  <circle cx="{px + pw//2 + 420}" cy="{py + ph//2}" r="36" fill="{GK}" stroke="{ACCENT}" stroke-width="5"/>
  <text x="{px+pw//2+420}" y="{py+ph//2-56}" font-family="{F_BOLD}" font-size="20" fill="{ACCENT}" text-anchor="middle" letter-spacing="3">SET</text>

  <!-- distance label -->
  <line x1="{px+pw//2}" y1="{py+ph-80}" x2="{px+pw//2+420}" y2="{py+ph-80}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="{px+pw//2+210}" y="{py+ph-40}" font-family="{F_BOLD}" font-size="24" fill="{MUTED}" text-anchor="middle" letter-spacing="3">3 – 6 m</text>

  <!-- "drill the recovery" note -->
  <text x="{px+80}" y="{py+ph//2+140}" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="3">DRILL THE RECOVERY</text>
  <text x="{px+80}" y="{py+ph//2+176}" font-family="{F_REG}" font-size="24" fill="{MUTED}">Getting back to set after the cross-step</text>
  <text x="{px+80}" y="{py+ph//2+212}" font-family="{F_REG}" font-size="24" fill="{MUTED}">is what most coaches skip.</text>

  {takeaway("The recovery is what you actually drill.")}
'''
    slides.append(("slide-3-crossstep.svg", svg_doc(crossstep)))

    # Slide 4 — Drop-step
    dropstep = f'''
  {drill_header("PATTERN 03 / THE DROP-STEP", "Ball behind. First step back.")}
  {pitch_frame(px, py, pw, ph)}

  <!-- ball coming from above (high ball) -->
  <circle cx="{px + pw//2}" cy="{py + 100}" r="20" fill="{TEXT}" stroke="{BG}" stroke-width="2"/>
  <line x1="{px+pw//2}" y1="{py+122}" x2="{px+pw//2 - 80}" y2="{py+ph//2 - 120}" stroke="{TEXT}" stroke-width="4" stroke-dasharray="12,8" marker-end="url(#arr-white)"/>
  <text x="{px+pw//2 + 40}" y="{py+80}" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" letter-spacing="3">HIGH BALL</text>

  <!-- GK start position -->
  <circle cx="{px+pw//2}" cy="{py+ph//2+60}" r="36" fill="{GK}" stroke="{BG}" stroke-width="4"/>
  <text x="{px+pw//2}" y="{py+ph//2+130}" font-family="{F_BOLD}" font-size="20" fill="{MUTED}" text-anchor="middle" letter-spacing="3">START</text>

  <!-- WRONG: sideways first step (red X) -->
  <line x1="{px+pw//2+38}" y1="{py+ph//2+60}" x2="{px+pw//2+160}" y2="{py+ph//2+60}" stroke="#E74C3C" stroke-width="5"/>
  <text x="{px+pw//2+180}" y="{py+ph//2+66}" font-family="{F_BOLD}" font-size="28" fill="#E74C3C">&#10007;</text>
  <text x="{px+pw//2+220}" y="{py+ph//2+50}" font-family="{F_BOLD}" font-size="22" fill="#E74C3C" letter-spacing="2">SIDEWAYS FIRST</text>
  <text x="{px+pw//2+220}" y="{py+ph//2+82}" font-family="{F_REG}" font-size="20" fill="{MUTED}">loses the ball</text>

  <!-- CORRECT: drop back first (green arrow) -->
  <line x1="{px+pw//2}" y1="{py+ph//2+22}" x2="{px+pw//2 - 40}" y2="{py+ph//2 - 100}" stroke="{GK}" stroke-width="6" marker-end="url(#arr-gk)"/>
  <text x="{px+pw//2 - 220}" y="{py+ph//2 - 100}" font-family="{F_BOLD}" font-size="22" fill="{ACCENT}" letter-spacing="2">FIRST STEP BACK</text>
  <text x="{px+pw//2 - 220}" y="{py+ph//2 - 68}" font-family="{F_REG}" font-size="20" fill="{MUTED}">then arc to ball</text>

  {takeaway("Instinct says sideways. Train it out.")}
'''
    slides.append(("slide-4-dropstep.svg", svg_doc(dropstep)))

    return slides


# =========================================================
# Day 6 (5/13 Wed) — Quick Tip: "8-minute pre-match warm-up"
# =========================================================
def day6_quicktip():
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="24" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">QUICK TIP · PRE-MATCH</text>

  <text x="{W//2}" y="350" font-family="{F_BOLD}" font-size="48" fill="{MUTED}" text-anchor="middle" letter-spacing="4">THE KEEPER WARM-UP</text>
  <text x="{W//2}" y="430" font-family="{F_BOLD}" font-size="140" fill="{ACCENT}" text-anchor="middle" letter-spacing="-4">8 MIN</text>

  <line x1="160" y1="480" x2="{W-160}" y2="480" stroke="{TEXT}" stroke-width="2" opacity="0.3"/>

  <!-- four blocks -->
  <text x="120" y="566" font-family="{F_BOLD}" font-size="28" fill="{ACCENT}" letter-spacing="2">1–2 MIN</text>
  <text x="360" y="566" font-family="{F_BOLD}" font-size="28" fill="{TEXT}">DYNAMIC MOVEMENT</text>
  <text x="360" y="600" font-family="{F_REG}" font-size="24" fill="{MUTED}">Shuffles, high knees, hips. No static stretch.</text>

  <text x="120" y="686" font-family="{F_BOLD}" font-size="28" fill="{ACCENT}" letter-spacing="2">3–4 MIN</text>
  <text x="360" y="686" font-family="{F_BOLD}" font-size="28" fill="{TEXT}">HANDLING</text>
  <text x="360" y="720" font-family="{F_REG}" font-size="24" fill="{MUTED}">Light rolls and throws. Hands calibrate.</text>

  <text x="120" y="806" font-family="{F_BOLD}" font-size="28" fill="{ACCENT}" letter-spacing="2">5–6 MIN</text>
  <text x="360" y="806" font-family="{F_BOLD}" font-size="28" fill="{TEXT}">SHOT-STOPPING</text>
  <text x="360" y="840" font-family="{F_REG}" font-size="24" fill="{MUTED}">Close range, building intensity. Feet moving.</text>

  <text x="120" y="926" font-family="{F_BOLD}" font-size="28" fill="{ACCENT}" letter-spacing="2">7–8 MIN</text>
  <text x="360" y="926" font-family="{F_BOLD}" font-size="28" fill="{TEXT}">DECISION REP</text>
  <text x="360" y="960" font-family="{F_REG}" font-size="24" fill="{MUTED}">One cross or long shot. End sharp.</text>

  <rect x="80" y="1130" width="60" height="6" fill="{ACCENT}"/>
  <text x="80" y="1200" font-family="{F_BOLD}" font-size="32" fill="{TEXT}">Beyond 8 min is for the coach's nerves.</text>
'''
    return [("slide-1.svg", svg_doc(body))]


# =========================================================
# Day 7 (5/14 Thu) — Product: "Keeper progress tracking" (3 slides)
# =========================================================
def day7_product():
    slides = []

    # Slide 1 — Hero
    hero = f'''
  <rect x="80" y="300" width="8" height="200" fill="{ACCENT}"/>
  <text x="120" y="335" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="6">KEEPER PROFILES · KEEPIX</text>
  <text x="120" y="490" font-family="{F_BOLD}" font-size="92" fill="{TEXT}" letter-spacing="-2">KNOW WHERE</text>
  <text x="120" y="590" font-family="{F_BOLD}" font-size="92" fill="{TEXT}" letter-spacing="-2">EVERY KEEPER</text>
  <text x="120" y="690" font-family="{F_BOLD}" font-size="92" fill="{ACCENT}" letter-spacing="-2">STANDS.</text>
  <line x1="120" y1="770" x2="380" y2="770" stroke="{TEXT}" stroke-width="3"/>
  <text x="120" y="840" font-family="{F_REG}" font-size="34" fill="{TEXT}">Progress you can see.</text>
  <text x="120" y="888" font-family="{F_REG}" font-size="34" fill="{TEXT}">Not just feel.</text>
  <text x="120" y="1010" font-family="{F_BOLD}" font-size="24" fill="{MUTED}" letter-spacing="4">6 AREAS · SESSION BY SESSION</text>
  <rect x="120" y="1030" width="60" height="6" fill="{ACCENT}"/>
'''
    slides.append(("slide-1-hero.svg", svg_doc(hero)))

    # Slide 2 — 2x3 evaluation grid with rating bars
    areas = [
        ("SET POSITION", 0.85),
        ("HANDLING",     0.70),
        ("FOOTWORK",     0.55),
        ("CROSSING",     0.60),
        ("DISTRIBUTION", 0.75),
        ("1v1",          0.50),
    ]
    trends = ["↑", "↑", "→", "↑", "↑", "↑"]
    cols, rows = 2, 3
    cw, ch = 440, 210
    gx, gy = 20, 20
    grid_w = cols * cw + (cols-1) * gx
    sx = (W - grid_w) // 2
    sy = 330
    grid_parts = []
    for i, ((name, val), trend) in enumerate(zip(areas, trends)):
        r, c = divmod(i, cols)
        x = sx + c * (cw + gx)
        y = sy + r * (ch + gy)
        bar_w = int((cw - 60) * val)
        trend_color = ACCENT if trend == "↑" else MUTED
        grid_parts.append(
            f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{PITCH}"/>'
            f'<text x="{x+24}" y="{y+44}" font-family="{F_BOLD}" font-size="22" fill="{TEXT}" letter-spacing="2">{name}</text>'
            f'<text x="{x+cw-30}" y="{y+44}" font-family="{F_BOLD}" font-size="28" fill="{trend_color}" text-anchor="end">{trend}</text>'
            f'<rect x="{x+24}" y="{y+70}" width="{cw-48}" height="16" rx="8" fill="{BG}"/>'
            f'<rect x="{x+24}" y="{y+70}" width="{bar_w}" height="16" rx="8" fill="{ACCENT}"/>'
            f'<text x="{x+24}" y="{y+130}" font-family="{F_REG}" font-size="20" fill="{MUTED}">Session avg · last 6 weeks</text>'
        )

    grid_body = f'''
  <text x="80" y="120" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="4">SIX AREAS · ONE PICTURE</text>
  <text x="80" y="195" font-family="{F_BOLD}" font-size="52" fill="{TEXT}" letter-spacing="-1">Rate after every session.</text>
  {"".join(grid_parts)}
  <rect x="80" y="1150" width="60" height="6" fill="{ACCENT}"/>
  <text x="80" y="1220" font-family="{F_BOLD}" font-size="34" fill="{TEXT}">Six weeks later, you have a picture.</text>
'''
    slides.append(("slide-2-grid.svg", svg_doc(grid_body)))

    # Slide 3 — Phone mockup with keeper profile
    phone_x, phone_y, phone_w, phone_h = 280, 340, 520, 840
    mockup = f'''
  <text x="80" y="120" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="4">PITCHSIDE · SESSION BY SESSION</text>
  <text x="80" y="195" font-family="{F_BOLD}" font-size="52" fill="{TEXT}" letter-spacing="-1">One note. Six ratings. Done.</text>

  <!-- phone -->
  <rect x="{phone_x}" y="{phone_y}" width="{phone_w}" height="{phone_h}" rx="50" fill="#0a2d22" stroke="{TEXT}" stroke-width="4"/>
  <rect x="{phone_x+180}" y="{phone_y+20}" width="160" height="16" rx="8" fill="{TEXT}" opacity="0.2"/>
  <rect x="{phone_x+30}" y="{phone_y+70}" width="{phone_w-60}" height="{phone_h-100}" rx="24" fill="{BG}"/>

  <!-- keeper label (anonymised) -->
  <rect x="{phone_x+60}" y="{phone_y+100}" width="200" height="44" rx="22" fill="{PITCH}" stroke="{ACCENT}" stroke-width="2"/>
  <text x="{phone_x+160}" y="{phone_y+130}" font-family="{F_BOLD}" font-size="18" fill="{TEXT}" text-anchor="middle" letter-spacing="2">KEEPER #3</text>

  <!-- session date chip -->
  <rect x="{phone_x+270}" y="{phone_y+100}" width="180" height="44" rx="22" fill="{ACCENT}"/>
  <text x="{phone_x+360}" y="{phone_y+130}" font-family="{F_BOLD}" font-size="18" fill="{BG}" text-anchor="middle" letter-spacing="2">13 MAY 2026</text>

  <!-- 6 mini rating rows -->
  mini_areas = [("SET",0.85),("HANDLING",0.70),("FOOTWORK",0.55),("CROSSING",0.60),("DISTRIB.",0.75),("1v1",0.50)]
  <!-- manual render instead -->
  <text x="{phone_x+70}" y="{phone_y+200}" font-family="{F_BOLD}" font-size="18" fill="{MUTED}" letter-spacing="2">SET POSITION</text>
  <rect x="{phone_x+70}" y="{phone_y+212}" width="360" height="10" rx="5" fill="{PITCH}"/>
  <rect x="{phone_x+70}" y="{phone_y+212}" width="306" height="10" rx="5" fill="{ACCENT}"/>

  <text x="{phone_x+70}" y="{phone_y+258}" font-family="{F_BOLD}" font-size="18" fill="{MUTED}" letter-spacing="2">HANDLING</text>
  <rect x="{phone_x+70}" y="{phone_y+270}" width="360" height="10" rx="5" fill="{PITCH}"/>
  <rect x="{phone_x+70}" y="{phone_y+270}" width="252" height="10" rx="5" fill="{ACCENT}"/>

  <text x="{phone_x+70}" y="{phone_y+316}" font-family="{F_BOLD}" font-size="18" fill="{MUTED}" letter-spacing="2">FOOTWORK</text>
  <rect x="{phone_x+70}" y="{phone_y+328}" width="360" height="10" rx="5" fill="{PITCH}"/>
  <rect x="{phone_x+70}" y="{phone_y+328}" width="198" height="10" rx="5" fill="{ACCENT}" opacity="0.7"/>

  <text x="{phone_x+70}" y="{phone_y+374}" font-family="{F_BOLD}" font-size="18" fill="{MUTED}" letter-spacing="2">CROSSING</text>
  <rect x="{phone_x+70}" y="{phone_y+386}" width="360" height="10" rx="5" fill="{PITCH}"/>
  <rect x="{phone_x+70}" y="{phone_y+386}" width="216" height="10" rx="5" fill="{ACCENT}" opacity="0.7"/>

  <text x="{phone_x+70}" y="{phone_y+432}" font-family="{F_BOLD}" font-size="18" fill="{MUTED}" letter-spacing="2">DISTRIBUTION</text>
  <rect x="{phone_x+70}" y="{phone_y+444}" width="360" height="10" rx="5" fill="{PITCH}"/>
  <rect x="{phone_x+70}" y="{phone_y+444}" width="270" height="10" rx="5" fill="{ACCENT}"/>

  <text x="{phone_x+70}" y="{phone_y+490}" font-family="{F_BOLD}" font-size="18" fill="{MUTED}" letter-spacing="2">1v1</text>
  <rect x="{phone_x+70}" y="{phone_y+502}" width="360" height="10" rx="5" fill="{PITCH}"/>
  <rect x="{phone_x+70}" y="{phone_y+502}" width="180" height="10" rx="5" fill="{ACCENT}" opacity="0.6"/>

  <!-- session note field -->
  <rect x="{phone_x+60}" y="{phone_y+540}" width="{phone_w-120}" height="100" rx="12" fill="{PITCH}"/>
  <text x="{phone_x+80}" y="{phone_y+570}" font-family="{F_BOLD}" font-size="16" fill="{ACCENT}" letter-spacing="2">SESSION NOTE</text>
  <text x="{phone_x+80}" y="{phone_y+600}" font-family="{F_REG}" font-size="17" fill="{MUTED}">Good footwork in crossing block.</text>
  <text x="{phone_x+80}" y="{phone_y+624}" font-family="{F_REG}" font-size="17" fill="{MUTED}">Drop-step still needs work.</text>

  <rect x="80" y="1150" width="60" height="6" fill="{ACCENT}"/>
  <text x="80" y="1220" font-family="{F_BOLD}" font-size="34" fill="{TEXT}">Track every keeper. Every session.</text>
'''
    slides.append(("slide-3-phone.svg", svg_doc(mockup)))

    return slides


# =========================================================
# Orchestration
# =========================================================
POSTS = [
    ("2026-05-08-quicktip",  day1_quicktip),
    ("2026-05-09-reflection", day2_reflection),
    ("2026-05-10-engage",    day3_engage),
    ("2026-05-11-story",     day4_story),
    ("2026-05-12-value",     day5_value),
    ("2026-05-13-quicktip",  day6_quicktip),
    ("2026-05-14-product",   day7_product),
]


def rasterize(svg_text):
    return bytes(resvg_py.svg_to_bytes(svg_string=svg_text, width=W, height=H, sans_serif_family="Helvetica"))


def build_all():
    all_outputs = {}
    for folder_name, fn in POSTS:
        out_dir = POSTS_DIR / folder_name
        out_dir.mkdir(parents=True, exist_ok=True)
        slides = fn()
        paths = []
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
    print(f"\nTotal: {sum(len(v) for v in outputs.values())} PNGs generated")
