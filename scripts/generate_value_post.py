"""Generate KEEPIX value-post SVGs (top-down pitch diagrams) and rasterize to PNG."""
from pathlib import Path
import resvg_py

OUT_DIR = Path(__file__).resolve().parent.parent / "content" / "posts" / "2026-04-23-value"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Palette
BG = "#0f3d2e"         # dark green background
PITCH = "#1a5c3f"      # lighter green pitch area
ACCENT = "#2ECC71"     # mint
TEXT = "#F5F5F0"       # off-white
MUTED = "#9FBFAE"      # muted label green-grey
GK = "#FFD700"         # keeper yellow
COACH = "#3498DB"      # coach blue
CONE = "#E67E22"       # cone orange

W, H = 1080, 1350

# font-family tricks: closes attr early so font-weight is appended
F_BOLD = 'sans-serif" font-weight="800'
F_REG = 'sans-serif" font-weight="400'

SVG_HEADER = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" fill="{BG}"/>

  <!-- arrow marker defs -->
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
'''

SVG_FOOTER_LOGO = f'''
  <circle cx="{W-240}" cy="{H-59}" r="5" fill="{ACCENT}"/>
  <text x="{W-60}" y="{H-50}" font-family="{F_BOLD}" font-size="28" fill="{TEXT}" text-anchor="end" letter-spacing="4">KEEPIX</text>
</svg>'''


# ---------- legend (reusable) ----------
def legend(x: int, y: int) -> str:
    return f'''
  <!-- legend -->
  <g transform="translate({x},{y})">
    <circle cx="18" cy="18" r="14" fill="{GK}"/>
    <text x="46" y="25" font-family="{F_BOLD}" font-size="22" fill="{TEXT}" letter-spacing="2">GK</text>

    <circle cx="140" cy="18" r="14" fill="{COACH}"/>
    <text x="168" y="25" font-family="{F_BOLD}" font-size="22" fill="{TEXT}" letter-spacing="2">COACH</text>

    <polygon points="310,32 330,32 320,4" fill="{CONE}"/>
    <text x="342" y="25" font-family="{F_BOLD}" font-size="22" fill="{TEXT}" letter-spacing="2">CONE</text>
  </g>'''


# ---------- slide 1: hero ----------
def slide1_hero() -> str:
    # Hero keeps the big type. Add a stylised pitch stripe at the bottom as visual anchor.
    pitch_stripe = f'''
  <!-- pitch stripe visual -->
  <rect x="0" y="1020" width="{W}" height="260" fill="{PITCH}"/>
  <!-- goal area simplified -->
  <rect x="340" y="1020" width="400" height="120" fill="none" stroke="{TEXT}" stroke-width="4" opacity="0.6"/>
  <rect x="440" y="1020" width="200" height="60" fill="none" stroke="{TEXT}" stroke-width="4" opacity="0.6"/>
  <line x1="0" y1="1020" x2="{W}" y2="1020" stroke="{TEXT}" stroke-width="4" opacity="0.6"/>
  <!-- penalty spot -->
  <circle cx="540" cy="1180" r="6" fill="{TEXT}" opacity="0.6"/>
  <!-- keeper marker on the line -->
  <circle cx="540" cy="1080" r="20" fill="{GK}" stroke="{BG}" stroke-width="3"/>
'''
    return SVG_HEADER + f'''
  <!-- accent bar -->
  <rect x="80" y="300" width="8" height="200" fill="{ACCENT}"/>

  <!-- eyebrow -->
  <text x="120" y="335" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="6">PRE-SESSION GK ACTIVATION</text>

  <!-- main title -->
  <text x="120" y="480" font-family="{F_BOLD}" font-size="130" fill="{TEXT}" letter-spacing="-2">3 WARM-UPS</text>
  <text x="120" y="610" font-family="{F_BOLD}" font-size="120" fill="{ACCENT}" letter-spacing="-2">12 MINUTES</text>

  <!-- divider -->
  <line x1="120" y1="720" x2="380" y2="720" stroke="{TEXT}" stroke-width="3"/>

  <!-- body -->
  <text x="120" y="790" font-family="{F_REG}" font-size="34" fill="{TEXT}">Three short drills every keeper coach</text>
  <text x="120" y="838" font-family="{F_REG}" font-size="34" fill="{TEXT}">can run before the main block.</text>

  <!-- theme tags -->
  <text x="120" y="960" font-family="{F_BOLD}" font-size="26" fill="{MUTED}" letter-spacing="4">FOOTWORK  ·  HANDLING  ·  DIVING</text>
  <rect x="120" y="980" width="60" height="6" fill="{ACCENT}"/>
  {pitch_stripe}
''' + SVG_FOOTER_LOGO


# ---------- slide headers (drills 2-4) ----------
def drill_header(num: str, minutes: str, title: str) -> str:
    return f'''
  <!-- small caption row -->
  <text x="80" y="120" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" letter-spacing="4">DRILL {num}  /  {minutes} MIN</text>
  <text x="80" y="185" font-family="{F_BOLD}" font-size="58" fill="{TEXT}" letter-spacing="-1">{title}</text>
'''


def takeaway_block(text: str) -> str:
    return f'''
  <!-- takeaway -->
  <rect x="80" y="1150" width="60" height="6" fill="{ACCENT}"/>
  <text x="80" y="1220" font-family="{F_BOLD}" font-size="38" fill="{TEXT}">{text}</text>
'''


# ---------- pitch frame (shared) ----------
def pitch_frame(x: int, y: int, w: int, h: int) -> str:
    return f'''
  <!-- pitch area -->
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" ry="20" fill="{PITCH}"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" ry="20" fill="none" stroke="{TEXT}" stroke-width="3" opacity="0.25"/>
'''


# ---------- slide 2: Ladder -> Set -> Catch ----------
def slide2_ladder() -> str:
    # Layout (top-down):
    # ladder on left (horizontal rungs), GK in middle (yellow circle with arms out),
    # coach on right (blue) throws a chest-height ball (dotted arrow from coach -> GK).
    # Yellow arrow from ladder exit -> GK.
    px, py, pw, ph = 60, 260, 960, 820
    pitch = pitch_frame(px, py, pw, ph)

    # Ladder: 6 rungs, vertical arrangement so GK runs up through it
    lad_x = 150
    lad_top = 340
    rung_w = 170
    rung_gap = 60
    rails = f'<rect x="{lad_x-6}" y="{lad_top-10}" width="6" height="{6*rung_gap+20}" fill="{TEXT}" opacity="0.7"/>' \
            f'<rect x="{lad_x+rung_w}" y="{lad_top-10}" width="6" height="{6*rung_gap+20}" fill="{TEXT}" opacity="0.7"/>'
    rungs = ""
    for i in range(6):
        y = lad_top + i * rung_gap
        rungs += f'<rect x="{lad_x}" y="{y}" width="{rung_w}" height="12" rx="3" fill="{TEXT}"/>\n    '
    ladder_label = f'<text x="{lad_x + rung_w//2}" y="{lad_top + 6*rung_gap + 60}" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">6-RUNG LADDER</text>'

    # GK circle (set position) — draw hands as two small yellow spheres either side
    gk_cx, gk_cy = 560, 700
    gk = f'''
    <!-- gk movement arrow from ladder exit to GK -->
    <line x1="{lad_x + rung_w//2}" y1="{lad_top + 6*rung_gap + 10}" x2="{gk_cx - 80}" y2="{gk_cy}" stroke="{GK}" stroke-width="6" marker-end="url(#arr-gk)"/>

    <!-- GK body (keeper circle with hands out) -->
    <circle cx="{gk_cx}" cy="{gk_cy}" r="38" fill="{GK}" stroke="{BG}" stroke-width="4"/>
    <!-- hands extended -->
    <circle cx="{gk_cx - 70}" cy="{gk_cy + 20}" r="16" fill="{GK}"/>
    <circle cx="{gk_cx + 70}" cy="{gk_cy + 20}" r="16" fill="{GK}"/>
    <line x1="{gk_cx - 30}" y1="{gk_cy + 15}" x2="{gk_cx - 60}" y2="{gk_cy + 20}" stroke="{GK}" stroke-width="8" stroke-linecap="round"/>
    <line x1="{gk_cx + 30}" y1="{gk_cy + 15}" x2="{gk_cx + 60}" y2="{gk_cy + 20}" stroke="{GK}" stroke-width="8" stroke-linecap="round"/>
    <text x="{gk_cx}" y="{gk_cy + 95}" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">SET POSITION</text>
'''

    # Coach circle on right throwing ball
    coach_cx, coach_cy = 900, 700
    coach = f'''
    <circle cx="{coach_cx}" cy="{coach_cy}" r="36" fill="{COACH}" stroke="{BG}" stroke-width="4"/>
    <text x="{coach_cx}" y="{coach_cy + 80}" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">COACH</text>
    <!-- ball trajectory (dotted) from coach chest to GK chest -->
    <line x1="{coach_cx - 40}" y1="{coach_cy - 10}" x2="{gk_cx + 50}" y2="{gk_cy - 20}" stroke="{TEXT}" stroke-width="4" stroke-dasharray="10,10" marker-end="url(#arr-white)"/>
    <text x="{(coach_cx + gk_cx)//2}" y="{coach_cy - 50}" font-family="{F_BOLD}" font-size="20" fill="{TEXT}" text-anchor="middle" letter-spacing="2">CHEST-HEIGHT BALL</text>
'''

    return SVG_HEADER + drill_header("01", "4", "Ladder &#8594; Set &#8594; Catch") + pitch + f'''
    {rails}
    {rungs}
    {ladder_label}
    {gk}
    {coach}
''' + legend(80, 1050) + takeaway_block("Feet &#8594; Hands &#8594; Reset") + SVG_FOOTER_LOGO


# ---------- slide 3: Reaction Wall Tennis ----------
def slide3_wall() -> str:
    px, py, pw, ph = 60, 260, 960, 820
    pitch = pitch_frame(px, py, pw, ph)

    # Wall at top (thick white bar)
    wall_y = 330
    wall = f'''
    <rect x="{px + 60}" y="{wall_y}" width="{pw - 120}" height="24" fill="{TEXT}"/>
    <!-- wall hatching -->
    <g stroke="{BG}" stroke-width="4">
      <line x1="{px + 90}" y1="{wall_y}" x2="{px + 70}" y2="{wall_y + 24}"/>
      <line x1="{px + 180}" y1="{wall_y}" x2="{px + 160}" y2="{wall_y + 24}"/>
      <line x1="{px + 270}" y1="{wall_y}" x2="{px + 250}" y2="{wall_y + 24}"/>
      <line x1="{px + 360}" y1="{wall_y}" x2="{px + 340}" y2="{wall_y + 24}"/>
      <line x1="{px + 450}" y1="{wall_y}" x2="{px + 430}" y2="{wall_y + 24}"/>
      <line x1="{px + 540}" y1="{wall_y}" x2="{px + 520}" y2="{wall_y + 24}"/>
      <line x1="{px + 630}" y1="{wall_y}" x2="{px + 610}" y2="{wall_y + 24}"/>
      <line x1="{px + 720}" y1="{wall_y}" x2="{px + 700}" y2="{wall_y + 24}"/>
      <line x1="{px + 810}" y1="{wall_y}" x2="{px + 790}" y2="{wall_y + 24}"/>
    </g>
    <text x="{W/2}" y="{wall_y - 20}" font-family="{F_BOLD}" font-size="24" fill="{TEXT}" text-anchor="middle" letter-spacing="3">WALL</text>
'''

    # GK 2m below wall (center)
    gk_cx, gk_cy = 540, 680
    gk = f'''
    <!-- 2m distance indicator -->
    <line x1="{gk_cx}" y1="{wall_y + 34}" x2="{gk_cx}" y2="{gk_cy - 50}" stroke="{TEXT}" stroke-width="2" stroke-dasharray="6,6" opacity="0.7"/>
    <rect x="{gk_cx - 36}" y="{(wall_y + gk_cy)//2 - 18}" width="72" height="36" rx="6" fill="{BG}"/>
    <text x="{gk_cx}" y="{(wall_y + gk_cy)//2 + 8}" font-family="{F_BOLD}" font-size="26" fill="{TEXT}" text-anchor="middle" letter-spacing="2">2 m</text>

    <!-- GK -->
    <circle cx="{gk_cx}" cy="{gk_cy}" r="40" fill="{GK}" stroke="{BG}" stroke-width="4"/>
    <!-- one hand up ready -->
    <circle cx="{gk_cx + 70}" cy="{gk_cy - 40}" r="16" fill="{GK}"/>
    <line x1="{gk_cx + 30}" y1="{gk_cy - 15}" x2="{gk_cx + 62}" y2="{gk_cy - 36}" stroke="{GK}" stroke-width="8" stroke-linecap="round"/>
    <text x="{gk_cx}" y="{gk_cy + 90}" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">GK</text>
'''

    # Coach to the side (right of GK) — throws past keeper onto the wall
    coach_cx, coach_cy = 820, 730
    coach = f'''
    <circle cx="{coach_cx}" cy="{coach_cy}" r="36" fill="{COACH}" stroke="{BG}" stroke-width="4"/>
    <text x="{coach_cx}" y="{coach_cy + 80}" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">COACH</text>

    <!-- throw 1: coach -> wall (dotted) -->
    <path d="M {coach_cx - 30} {coach_cy - 20} Q 600 440 {px + 280} {wall_y + 26}" stroke="{TEXT}" stroke-width="4" fill="none" stroke-dasharray="10,10" marker-end="url(#arr-white)"/>
    <!-- rebound 2: wall -> GK one-hand (dotted) -->
    <path d="M {px + 280} {wall_y + 26} Q 400 540 {gk_cx + 62} {gk_cy - 40}" stroke="{TEXT}" stroke-width="4" fill="none" stroke-dasharray="10,10" marker-end="url(#arr-white)"/>

    <!-- small labels on the paths -->
    <text x="720" y="450" font-family="{F_BOLD}" font-size="20" fill="{TEXT}" letter-spacing="2">1. THROW</text>
    <text x="300" y="540" font-family="{F_BOLD}" font-size="20" fill="{TEXT}" letter-spacing="2">2. REBOUND</text>

    <!-- tennis ball near coach -->
    <circle cx="{coach_cx - 50}" cy="{coach_cy - 30}" r="12" fill="#d4f542" stroke="{BG}" stroke-width="2"/>
'''

    return SVG_HEADER + drill_header("02", "3", "Reaction Wall Tennis") + pitch + f'''
    {wall}
    {gk}
    {coach}
''' + legend(80, 1050) + takeaway_block("One hand. Alternate sides.") + SVG_FOOTER_LOGO


# ---------- slide 4: Low-Dive Diagonals ----------
def slide4_lowdive() -> str:
    px, py, pw, ph = 60, 260, 960, 820
    pitch = pitch_frame(px, py, pw, ph)

    # Two cones 4m apart horizontally
    cone_lx, cone_rx = 240, 840
    cone_y = 560
    cones = f'''
    <polygon points="{cone_lx - 22},{cone_y + 30} {cone_lx + 22},{cone_y + 30} {cone_lx},{cone_y - 40}" fill="{CONE}"/>
    <polygon points="{cone_rx - 22},{cone_y + 30} {cone_rx + 22},{cone_y + 30} {cone_rx},{cone_y - 40}" fill="{CONE}"/>

    <!-- 4m distance indicator -->
    <line x1="{cone_lx + 30}" y1="{cone_y + 60}" x2="{cone_rx - 30}" y2="{cone_y + 60}" stroke="{TEXT}" stroke-width="2" stroke-dasharray="6,6" opacity="0.7"/>
    <rect x="{(cone_lx + cone_rx)//2 - 36}" y="{cone_y + 42}" width="72" height="36" rx="6" fill="{BG}"/>
    <text x="{(cone_lx + cone_rx)//2}" y="{cone_y + 68}" font-family="{F_BOLD}" font-size="26" fill="{TEXT}" text-anchor="middle" letter-spacing="2">4 m</text>

    <text x="{cone_lx}" y="{cone_y + 110}" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">CONE A</text>
    <text x="{cone_rx}" y="{cone_y + 110}" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">CONE B</text>
'''

    # GK start at center (between cones), shuffle arrow to left cone, dive arc to ball beyond cone A
    gk_cx, gk_cy = 540, 540
    gk_shuffle_target_x = cone_lx + 60
    dive_ball_x, dive_ball_y = cone_lx - 60, cone_y + 180

    gk = f'''
    <circle cx="{gk_cx}" cy="{gk_cy}" r="34" fill="{GK}" stroke="{BG}" stroke-width="4"/>
    <text x="{gk_cx}" y="{gk_cy - 55}" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">START</text>

    <!-- 1. shuffle arrow (yellow solid) center -> left -->
    <line x1="{gk_cx - 40}" y1="{gk_cy}" x2="{gk_shuffle_target_x}" y2="{gk_cy}" stroke="{GK}" stroke-width="6" marker-end="url(#arr-gk)"/>
    <text x="{(gk_cx + gk_shuffle_target_x)//2}" y="{gk_cy - 20}" font-family="{F_BOLD}" font-size="22" fill="{GK}" text-anchor="middle" letter-spacing="3">1. SHUFFLE</text>

    <!-- 2. dive arc from cone A downward to far ball (yellow) -->
    <path d="M {cone_lx} {cone_y + 10} Q {cone_lx - 80} {cone_y + 80} {dive_ball_x + 20} {dive_ball_y - 10}"
          stroke="{GK}" stroke-width="6" fill="none" marker-end="url(#arr-gk)"/>
    <text x="90" y="{cone_y - 90}" font-family="{F_BOLD}" font-size="22" fill="{GK}" letter-spacing="3">2. LOW DIVE</text>
'''

    # Coach below center, dotted arrow to ball beyond cone A (where GK dives to)
    coach_cx, coach_cy = 620, 900
    coach = f'''
    <circle cx="{coach_cx}" cy="{coach_cy}" r="36" fill="{COACH}" stroke="{BG}" stroke-width="4"/>
    <text x="{coach_cx}" y="{coach_cy + 70}" font-family="{F_BOLD}" font-size="22" fill="{MUTED}" text-anchor="middle" letter-spacing="3">COACH</text>

    <!-- ball trajectory (dotted) -->
    <path d="M {coach_cx - 30} {coach_cy - 20} Q 400 720 {dive_ball_x + 16} {dive_ball_y}"
          stroke="{TEXT}" stroke-width="4" fill="none" stroke-dasharray="10,10" marker-end="url(#arr-white)"/>

    <!-- ball at landing -->
    <circle cx="{dive_ball_x}" cy="{dive_ball_y}" r="14" fill="{TEXT}" stroke="{BG}" stroke-width="2"/>
    <text x="{dive_ball_x}" y="{dive_ball_y + 46}" font-family="{F_BOLD}" font-size="20" fill="{TEXT}" text-anchor="middle" letter-spacing="2">BALL</text>
'''

    return SVG_HEADER + drill_header("03", "4", "Low-Dive Diagonals") + pitch + f'''
    {cones}
    {gk}
    {coach}
''' + legend(80, 1050) + takeaway_block("Shuffle &#8594; Low dive &#8594; Recover") + SVG_FOOTER_LOGO


# ---------- build & rasterize ----------
def build_svgs():
    svgs = {
        "slide-1-hero.svg": slide1_hero(),
        "slide-2-ladder-set-catch.svg": slide2_ladder(),
        "slide-3-reaction-wall-tennis.svg": slide3_wall(),
        "slide-4-low-dive-diagonals.svg": slide4_lowdive(),
    }
    paths = []
    for name, body in svgs.items():
        p = OUT_DIR / name
        p.write_text(body, encoding="utf-8")
        paths.append(p)
    return paths


def rasterize(svg_paths):
    png_paths = []
    for svg_p in svg_paths:
        svg_text = svg_p.read_text(encoding="utf-8")
        png_bytes = resvg_py.svg_to_bytes(
            svg_string=svg_text,
            width=W,
            height=H,
            sans_serif_family="Helvetica",
        )
        png_p = svg_p.with_suffix(".png")
        png_p.write_bytes(bytes(png_bytes))
        png_paths.append(png_p)
    return png_paths


if __name__ == "__main__":
    svg_paths = build_svgs()
    png_paths = rasterize(svg_paths)
    for p in png_paths:
        print(p)
