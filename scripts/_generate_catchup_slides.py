"""Generate single hero slide PNGs for the 3 catch-up posts (5/15, 5/16, 5/17).

One-off helper. Outputs to content/posts/<id>/slide-1.png matching the existing
brand palette so the carousel feels consistent with the surrounding week.
"""
from __future__ import annotations

from pathlib import Path

import resvg_py

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "content" / "posts"

BG     = "#0f3d2e"
ACCENT = "#2ECC71"
TEXT   = "#F5F5F0"
MUTED  = "#9FBFAE"

W, H = 1080, 1350
F_BOLD = 'sans-serif" font-weight="800'
F_REG  = 'sans-serif" font-weight="400'
F_ITAL = 'sans-serif" font-weight="400" font-style="italic'


def svg_doc(body: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  {body}
  <circle cx="{W-240}" cy="{H-59}" r="5" fill="{ACCENT}"/>
  <text x="{W-60}" y="{H-50}" font-family="{F_BOLD}" font-size="28" fill="{TEXT}" text-anchor="end" letter-spacing="4">KEEPIX</text>
</svg>'''


def slide_value_building() -> str:
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">VALUE · BUILD-OUT</text>

  <rect x="{W//2 - 40}" y="260" width="80" height="6" fill="{ACCENT}"/>

  <text x="{W//2}" y="450" font-family="{F_BOLD}" font-size="86" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">Three cues that</text>
  <text x="{W//2}" y="555" font-family="{F_BOLD}" font-size="86" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">turn your keeper</text>
  <text x="{W//2}" y="660" font-family="{F_BOLD}" font-size="86" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">from a last resort</text>
  <text x="{W//2}" y="765" font-family="{F_BOLD}" font-size="86" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">into the first pass.</text>

  <line x1="{W//2 - 200}" y1="900" x2="{W//2 + 200}" y2="900" stroke="{TEXT}" stroke-width="2" opacity="0.25"/>

  <text x="{W//2}" y="990" font-family="{F_ITAL}" font-size="32" fill="{MUTED}" text-anchor="middle">scan · shape · weight</text>

  <text x="{W//2}" y="1200" font-family="{F_BOLD}" font-size="34" fill="{TEXT}" text-anchor="middle" letter-spacing="2">SAVE FOR YOUR NEXT BLOCK</text>
'''
    return svg_doc(body)


def slide_story_resilient() -> str:
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="24" fill="{ACCENT}" text-anchor="middle" letter-spacing="8">KEEPIX · STORY</text>

  <text x="{W//2}" y="420" font-family="{F_BOLD}" font-size="200" fill="{ACCENT}" text-anchor="middle" opacity="0.25">&#8220;</text>

  <text x="{W//2}" y="540" font-family="{F_BOLD}" font-size="72" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">The keeper</text>
  <text x="{W//2}" y="630" font-family="{F_BOLD}" font-size="72" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">who improved</text>
  <text x="{W//2}" y="720" font-family="{F_BOLD}" font-size="72" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">most this season</text>

  <line x1="{W//2 - 60}" y1="780" x2="{W//2 + 60}" y2="780" stroke="{ACCENT}" stroke-width="3"/>

  <text x="{W//2}" y="870" font-family="{F_BOLD}" font-size="62" fill="{ACCENT}" text-anchor="middle" letter-spacing="-1">wasn't the most</text>
  <text x="{W//2}" y="940" font-family="{F_BOLD}" font-size="62" fill="{ACCENT}" text-anchor="middle" letter-spacing="-1">talented one.</text>

  <text x="{W//2}" y="1200" font-family="{F_ITAL}" font-size="30" fill="{MUTED}" text-anchor="middle">— a coaching reflection</text>
'''
    return svg_doc(body)


def slide_engage_mistake() -> str:
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">ENGAGE · COACHING MOMENT</text>

  <rect x="{W//2 - 40}" y="260" width="80" height="6" fill="{ACCENT}"/>

  <text x="{W//2}" y="430" font-family="{F_BOLD}" font-size="68" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">The game is still alive.</text>

  <text x="{W//2}" y="660" font-family="{F_BOLD}" font-size="220" fill="{ACCENT}" text-anchor="middle" letter-spacing="-6">30s</text>

  <text x="{W//2}" y="730" font-family="{F_ITAL}" font-size="32" fill="{MUTED}" text-anchor="middle">before the restart</text>

  <line x1="{W//2 - 180}" y1="830" x2="{W//2 + 180}" y2="830" stroke="{TEXT}" stroke-width="2" opacity="0.25"/>

  <text x="{W//2}" y="940" font-family="{F_BOLD}" font-size="80" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">What do</text>
  <text x="{W//2}" y="1030" font-family="{F_BOLD}" font-size="80" fill="{ACCENT}" text-anchor="middle" letter-spacing="-1">you say?</text>

  <text x="{W//2}" y="1220" font-family="{F_BOLD}" font-size="32" fill="{TEXT}" text-anchor="middle" letter-spacing="2">COMMENT YOUR ANSWER BELOW</text>
'''
    return svg_doc(body)


def slide_value_distribution() -> str:
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">VALUE · DISTRIBUTION</text>

  <rect x="{W//2 - 40}" y="260" width="80" height="6" fill="{ACCENT}"/>

  <text x="{W//2}" y="440" font-family="{F_BOLD}" font-size="76" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">Before the ball</text>
  <text x="{W//2}" y="535" font-family="{F_BOLD}" font-size="76" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">leaves your</text>
  <text x="{W//2}" y="630" font-family="{F_BOLD}" font-size="76" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">keeper's hands,</text>

  <line x1="{W//2 - 200}" y1="700" x2="{W//2 + 200}" y2="700" stroke="{ACCENT}" stroke-width="2"/>

  <text x="{W//2}" y="820" font-family="{F_BOLD}" font-size="78" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">the game is</text>
  <text x="{W//2}" y="915" font-family="{F_BOLD}" font-size="78" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">already decided.</text>

  <text x="{W//2}" y="1080" font-family="{F_ITAL}" font-size="32" fill="{MUTED}" text-anchor="middle">read · choose · release</text>

  <text x="{W//2}" y="1220" font-family="{F_BOLD}" font-size="32" fill="{TEXT}" text-anchor="middle" letter-spacing="2">DISTRIBUTION IS A DECISION</text>
'''
    return svg_doc(body)


def slide_product_crossing() -> str:
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">PRODUCT · CROSSING BLOCK</text>

  <rect x="{W//2 - 40}" y="260" width="80" height="6" fill="{ACCENT}"/>

  <text x="{W//2}" y="430" font-family="{F_BOLD}" font-size="64" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">Most crossing sessions</text>
  <text x="{W//2}" y="510" font-family="{F_BOLD}" font-size="64" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">stop at "get to the ball."</text>

  <line x1="{W//2 - 220}" y1="580" x2="{W//2 + 220}" y2="580" stroke="{TEXT}" stroke-width="2" opacity="0.25"/>

  <text x="{W//2}" y="680" font-family="{F_BOLD}" font-size="58" fill="{ACCENT}" text-anchor="middle" letter-spacing="-1">KEEPIX takes it</text>

  <text x="{W//2}" y="850" font-family="{F_BOLD}" font-size="200" fill="{ACCENT}" text-anchor="middle" letter-spacing="-6">3</text>

  <text x="{W//2}" y="940" font-family="{F_BOLD}" font-size="44" fill="{TEXT}" text-anchor="middle" letter-spacing="4">PHASES FURTHER</text>

  <text x="{W//2 - 280}" y="1080" font-family="{F_BOLD}" font-size="26" fill="{MUTED}" text-anchor="middle">POSITION</text>
  <text x="{W//2}" y="1080" font-family="{F_BOLD}" font-size="26" fill="{MUTED}" text-anchor="middle">CONTACT</text>
  <text x="{W//2 + 280}" y="1080" font-family="{F_BOLD}" font-size="26" fill="{MUTED}" text-anchor="middle">DECISION</text>

  <text x="{W//2}" y="1220" font-family="{F_BOLD}" font-size="32" fill="{TEXT}" text-anchor="middle" letter-spacing="2">LINK IN BIO — TRY THE BLOCK</text>
'''
    return svg_doc(body)


def slide_value_crosses() -> str:
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">VALUE · READING CROSSES</text>

  <rect x="{W//2 - 40}" y="260" width="80" height="6" fill="{ACCENT}"/>

  <text x="{W//2}" y="450" font-family="{F_BOLD}" font-size="90" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">Before the ball</text>
  <text x="{W//2}" y="560" font-family="{F_BOLD}" font-size="90" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">is even struck,</text>

  <line x1="{W//2 - 180}" y1="620" x2="{W//2 + 180}" y2="620" stroke="{ACCENT}" stroke-width="2"/>

  <text x="{W//2}" y="740" font-family="{F_BOLD}" font-size="90" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">a good keeper</text>
  <text x="{W//2}" y="850" font-family="{F_BOLD}" font-size="90" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">has already</text>
  <text x="{W//2}" y="960" font-family="{F_BOLD}" font-size="90" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">decided.</text>

  <text x="{W//2}" y="1140" font-family="{F_ITAL}" font-size="32" fill="{MUTED}" text-anchor="middle">stay · go · hold</text>

  <text x="{W//2}" y="1220" font-family="{F_BOLD}" font-size="34" fill="{TEXT}" text-anchor="middle" letter-spacing="2">THREE DECISIONS · ONE READ</text>
'''
    return svg_doc(body)


def slide_story_45_seconds() -> str:
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="24" fill="{ACCENT}" text-anchor="middle" letter-spacing="8">KEEPIX · STORY</text>

  <text x="{W//2}" y="420" font-family="{F_BOLD}" font-size="200" fill="{ACCENT}" text-anchor="middle" opacity="0.25">&#8220;</text>

  <text x="{W//2}" y="560" font-family="{F_BOLD}" font-size="200" fill="{ACCENT}" text-anchor="middle" letter-spacing="-6">45s</text>

  <text x="{W//2}" y="630" font-family="{F_ITAL}" font-size="32" fill="{MUTED}" text-anchor="middle">after the goal</text>

  <line x1="{W//2 - 60}" y1="720" x2="{W//2 + 60}" y2="720" stroke="{ACCENT}" stroke-width="3"/>

  <text x="{W//2}" y="830" font-family="{F_BOLD}" font-size="68" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">The window</text>
  <text x="{W//2}" y="920" font-family="{F_BOLD}" font-size="68" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">that matters most.</text>

  <text x="{W//2}" y="1220" font-family="{F_ITAL}" font-size="30" fill="{MUTED}" text-anchor="middle">— a coaching reflection</text>
'''
    return svg_doc(body)


def slide_value_1v1() -> str:
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">VALUE · 1V1</text>

  <rect x="{W//2 - 40}" y="260" width="80" height="6" fill="{ACCENT}"/>

  <text x="{W//2}" y="450" font-family="{F_BOLD}" font-size="82" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">Most keepers</text>
  <text x="{W//2}" y="550" font-family="{F_BOLD}" font-size="82" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">lose 1v1s</text>

  <line x1="{W//2 - 200}" y1="620" x2="{W//2 + 200}" y2="620" stroke="{ACCENT}" stroke-width="2"/>

  <text x="{W//2}" y="740" font-family="{F_BOLD}" font-size="76" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">before the striker</text>
  <text x="{W//2}" y="830" font-family="{F_BOLD}" font-size="76" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">even touches</text>
  <text x="{W//2}" y="920" font-family="{F_BOLD}" font-size="76" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">the ball.</text>

  <text x="{W//2}" y="1080" font-family="{F_ITAL}" font-size="32" fill="{MUTED}" text-anchor="middle">starting position · weight · timing</text>

  <text x="{W//2}" y="1220" font-family="{F_BOLD}" font-size="32" fill="{TEXT}" text-anchor="middle" letter-spacing="2">SAVE FOR YOUR NEXT BLOCK</text>
'''
    return svg_doc(body)


def slide_engage_best_cue() -> str:
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">ENGAGE · COMMUNITY QUESTION</text>

  <rect x="{W//2 - 40}" y="260" width="80" height="6" fill="{ACCENT}"/>

  <text x="{W//2}" y="450" font-family="{F_BOLD}" font-size="78" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">One coaching cue.</text>
  <text x="{W//2}" y="550" font-family="{F_BOLD}" font-size="78" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">One session.</text>

  <line x1="{W//2 - 200}" y1="620" x2="{W//2 + 200}" y2="620" stroke="{ACCENT}" stroke-width="2"/>

  <text x="{W//2}" y="740" font-family="{F_BOLD}" font-size="78" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">Your keeper</text>
  <text x="{W//2}" y="830" font-family="{F_BOLD}" font-size="78" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">stood differently</text>
  <text x="{W//2}" y="920" font-family="{F_BOLD}" font-size="78" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">after it.</text>

  <text x="{W//2}" y="1100" font-family="{F_ITAL}" font-size="32" fill="{MUTED}" text-anchor="middle">share yours below</text>

  <text x="{W//2}" y="1220" font-family="{F_BOLD}" font-size="32" fill="{TEXT}" text-anchor="middle" letter-spacing="2">COMMENT THE CUE 👇</text>
'''
    return svg_doc(body)


def slide_product_4week() -> str:
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">PRODUCT · CURRICULUM</text>

  <rect x="{W//2 - 40}" y="260" width="80" height="6" fill="{ACCENT}"/>

  <text x="{W//2}" y="500" font-family="{F_BOLD}" font-size="280" fill="{ACCENT}" text-anchor="middle" letter-spacing="-12">4</text>
  <text x="{W//2}" y="580" font-family="{F_BOLD}" font-size="48" fill="{TEXT}" text-anchor="middle" letter-spacing="6">WEEK PLAN</text>

  <line x1="{W//2 - 220}" y1="650" x2="{W//2 + 220}" y2="650" stroke="{TEXT}" stroke-width="2" opacity="0.25"/>

  <text x="{W//2}" y="770" font-family="{F_BOLD}" font-size="68" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">Progress your</text>
  <text x="{W//2}" y="855" font-family="{F_BOLD}" font-size="68" fill="{ACCENT}" text-anchor="middle" letter-spacing="-1">keepers can feel.</text>

  <text x="{W//2 - 320}" y="1030" font-family="{F_BOLD}" font-size="24" fill="{MUTED}" text-anchor="middle" letter-spacing="2">W1 · BASE</text>
  <text x="{W//2 - 105}" y="1030" font-family="{F_BOLD}" font-size="24" fill="{MUTED}" text-anchor="middle" letter-spacing="2">W2 · LOAD</text>
  <text x="{W//2 + 110}" y="1030" font-family="{F_BOLD}" font-size="24" fill="{MUTED}" text-anchor="middle" letter-spacing="2">W3 · TEST</text>
  <text x="{W//2 + 320}" y="1030" font-family="{F_BOLD}" font-size="24" fill="{MUTED}" text-anchor="middle" letter-spacing="2">W4 · PEAK</text>

  <text x="{W//2}" y="1220" font-family="{F_BOLD}" font-size="32" fill="{TEXT}" text-anchor="middle" letter-spacing="2">LINK IN BIO — BUILD YOURS</text>
'''
    return svg_doc(body)


def slide_value_set_position() -> str:
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">VALUE · SET POSITION</text>

  <rect x="{W//2 - 40}" y="260" width="80" height="6" fill="{ACCENT}"/>

  <text x="{W//2}" y="450" font-family="{F_BOLD}" font-size="84" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">Most keepers</text>
  <text x="{W//2}" y="550" font-family="{F_BOLD}" font-size="84" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">are set.</text>

  <text x="{W//2}" y="680" font-family="{F_BOLD}" font-size="56" fill="{MUTED}" text-anchor="middle">But set for what —</text>

  <text x="{W//2 - 220}" y="850" font-family="{F_BOLD}" font-size="92" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">a save,</text>
  <text x="{W//2}" y="850" font-family="{F_BOLD}" font-size="48" fill="{MUTED}" text-anchor="middle">or</text>
  <text x="{W//2 + 220}" y="850" font-family="{F_BOLD}" font-size="92" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">a stumble?</text>

  <line x1="{W//2 - 200}" y1="930" x2="{W//2 + 200}" y2="930" stroke="{ACCENT}" stroke-width="2"/>

  <text x="{W//2}" y="1080" font-family="{F_ITAL}" font-size="32" fill="{MUTED}" text-anchor="middle">weight · hands · loading moment</text>

  <text x="{W//2}" y="1220" font-family="{F_BOLD}" font-size="32" fill="{TEXT}" text-anchor="middle" letter-spacing="2">SAVE THIS COACHING POINT</text>
'''
    return svg_doc(body)


def slide_product_session_variety() -> str:
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">PRODUCT · SESSION DESIGN</text>

  <rect x="{W//2 - 40}" y="260" width="80" height="6" fill="{ACCENT}"/>

  <text x="{W//2}" y="450" font-family="{F_BOLD}" font-size="68" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">The moment</text>
  <text x="{W//2}" y="540" font-family="{F_BOLD}" font-size="68" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">your keeper</text>
  <text x="{W//2}" y="630" font-family="{F_BOLD}" font-size="68" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">stops being surprised</text>

  <line x1="{W//2 - 200}" y1="700" x2="{W//2 + 200}" y2="700" stroke="{ACCENT}" stroke-width="2"/>

  <text x="{W//2}" y="820" font-family="{F_BOLD}" font-size="68" fill="{ACCENT}" text-anchor="middle" letter-spacing="-1">the session</text>
  <text x="{W//2}" y="910" font-family="{F_BOLD}" font-size="68" fill="{ACCENT}" text-anchor="middle" letter-spacing="-1">stops working.</text>

  <text x="{W//2}" y="1080" font-family="{F_ITAL}" font-size="32" fill="{MUTED}" text-anchor="middle">rotate · re-stack · re-challenge</text>

  <text x="{W//2}" y="1220" font-family="{F_BOLD}" font-size="32" fill="{TEXT}" text-anchor="middle" letter-spacing="2">LINK IN BIO — SHAKE THE PLAN</text>
'''
    return svg_doc(body)


def slide_value_penalty() -> str:
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">VALUE · PENALTIES</text>

  <rect x="{W//2 - 40}" y="260" width="80" height="6" fill="{ACCENT}"/>

  <text x="{W//2}" y="450" font-family="{F_BOLD}" font-size="64" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">Your keeper is already</text>
  <text x="{W//2}" y="535" font-family="{F_BOLD}" font-size="64" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">at a disadvantage</text>

  <line x1="{W//2 - 220}" y1="610" x2="{W//2 + 220}" y2="610" stroke="{ACCENT}" stroke-width="2"/>

  <text x="{W//2}" y="730" font-family="{F_BOLD}" font-size="64" fill="{ACCENT}" text-anchor="middle" letter-spacing="-1">before the ball</text>
  <text x="{W//2}" y="815" font-family="{F_BOLD}" font-size="64" fill="{ACCENT}" text-anchor="middle" letter-spacing="-1">is placed.</text>

  <text x="{W//2}" y="950" font-family="{F_BOLD}" font-size="56" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">Close the gap.</text>

  <text x="{W//2}" y="1090" font-family="{F_ITAL}" font-size="32" fill="{MUTED}" text-anchor="middle">routine · breath · commitment</text>

  <text x="{W//2}" y="1220" font-family="{F_BOLD}" font-size="32" fill="{TEXT}" text-anchor="middle" letter-spacing="2">SAVE THIS BEFORE NEXT SHOOTOUT</text>
'''
    return svg_doc(body)


def slide_product_preseason() -> str:
    body = f'''
  <text x="{W//2}" y="200" font-family="{F_BOLD}" font-size="26" fill="{ACCENT}" text-anchor="middle" letter-spacing="6">PRODUCT · PRE-SEASON</text>

  <rect x="{W//2 - 40}" y="260" width="80" height="6" fill="{ACCENT}"/>

  <text x="{W//2}" y="460" font-family="{F_BOLD}" font-size="78" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">Pre-season is</text>
  <text x="{W//2}" y="555" font-family="{F_BOLD}" font-size="78" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">the one window</text>

  <line x1="{W//2 - 200}" y1="625" x2="{W//2 + 200}" y2="625" stroke="{ACCENT}" stroke-width="2"/>

  <text x="{W//2}" y="755" font-family="{F_BOLD}" font-size="78" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">technique gets</text>
  <text x="{W//2}" y="850" font-family="{F_BOLD}" font-size="78" fill="{ACCENT}" text-anchor="middle" letter-spacing="-2">your full attention.</text>

  <text x="{W//2}" y="990" font-family="{F_BOLD}" font-size="56" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">Don't waste it.</text>

  <text x="{W//2}" y="1220" font-family="{F_BOLD}" font-size="32" fill="{TEXT}" text-anchor="middle" letter-spacing="2">LINK IN BIO — BUILD THE BLOCK</text>
'''
    return svg_doc(body)


def render(svg_text: str, out_png: Path) -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    png_bytes = resvg_py.svg_to_bytes(svg_string=svg_text)
    out_png.write_bytes(bytes(png_bytes))
    print(f"wrote {out_png}  ({out_png.stat().st_size} bytes)")


def main() -> None:
    plan = [
        ("2026-05-15-value-building-from-back", slide_value_building()),
        ("2026-05-16-story-resilient-keeper",   slide_story_resilient()),
        ("2026-05-17-value-reading-crosses",    slide_value_crosses()),
        ("2026-05-18-engage-after-mistake",     slide_engage_mistake()),
        ("2026-05-19-value-distribution",       slide_value_distribution()),
        ("2026-05-20-product-crossing-session", slide_product_crossing()),
        ("2026-05-21-story-after-goal-conceded",   slide_story_45_seconds()),
        ("2026-05-22-value-1v1-angles",            slide_value_1v1()),
        ("2026-05-23-engage-best-cue",             slide_engage_best_cue()),
        ("2026-05-24-product-4week-curriculum",    slide_product_4week()),
        ("2026-05-25-value-set-position",          slide_value_set_position()),
        # Note: id mismatches scheduled_at after the swap — id matches the caption file.
        ("2026-05-27-product-session-variety",     slide_product_session_variety()),
        ("2026-05-26-value-penalty-psychology",    slide_value_penalty()),
        ("2026-05-28-product-pre-season",          slide_product_preseason()),
    ]
    for slug, svg in plan:
        out_dir = POSTS / slug
        render(svg, out_dir / "slide-1.png")


if __name__ == "__main__":
    main()
