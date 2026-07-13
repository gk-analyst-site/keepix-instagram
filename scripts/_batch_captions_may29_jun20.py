"""Batch-generate the 23 captions for 2026-05-29 .. 2026-06-20.

Uses the content-creator agent system prompt (agents/content-creator.md) via the
Claude API, threaded for speed. Saves each to content/captions/<id>.md.
Idempotent: skips ids whose caption file already exists (so it can be re-run).
"""
from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from anthropic import Anthropic

from _common import ANTHROPIC_KEY, CLAUDE_MODEL, ROOT, require

PLAN = [
    ("2026-05-29-value-catch-vs-parry",        "Value",   "Catching vs parrying — when to hold and when to deflect, and the read that decides"),
    ("2026-05-30-product-season-tracking",     "Product", "Tracking a goalkeeper's progress across a full season so coaches can see what's actually improving"),
    ("2026-05-31-value-through-ball-position", "Value",   "Starting position for through balls — how high a keeper should hold their line and when to drop"),
    ("2026-06-01-engage-non-negotiable",       "Engage",  "Ask coaches: the one thing you never cut from a keeper session no matter how short on time"),
    ("2026-06-02-value-high-balls-timing",     "Value",   "High balls and crosses: timing the jump, the standing leg, and protecting the catch in traffic"),
    ("2026-06-03-story-keeper-nobody-picked",  "Story",   "The keeper nobody picked at trials who became the captain — what changed and what we learned"),
    ("2026-06-04-product-age-appropriate",     "Product", "Designing age-appropriate goalkeeper sessions: how U10 work differs from U16, and planning for both"),
    ("2026-06-05-value-recovery-saves",        "Value",   "Recovery saves: getting back to your feet and re-set fast after the first save"),
    ("2026-06-06-product-small-spaces",        "Product", "Adapting goalkeeper drills for small or shared training spaces without losing quality"),
    ("2026-06-07-value-backpass-pressure",     "Value",   "Receiving back-passes under pressure: first touch, body shape and the decision before the ball arrives"),
    ("2026-06-08-engage-lost-confidence",      "Engage",  "Ask coaches: how do you rebuild a keeper who has lost confidence after a run of goals conceded"),
    ("2026-06-09-value-organizing-wall",       "Value",   "Organizing the wall on free kicks: communication, counting bodies and positioning the keeper"),
    ("2026-06-10-story-mistake-changed-coaching", "Story", "A coaching mistake that changed how I work with keepers — over-coaching the technique, missing the player"),
    ("2026-06-11-product-share-with-assistants", "Product", "Sharing structured session plans with assistant coaches so everyone runs the same picture"),
    ("2026-06-12-value-diving-technique",      "Value",   "Diving technique: the collapse save for low shots vs the power dive for the top corner"),
    ("2026-06-13-product-video-review",        "Product", "Pairing short video review with your session plans to close the gap between feedback and the next rep"),
    ("2026-06-14-value-rebounds-second-phase", "Value",   "Reading rebounds and second-phase situations: where to spill, recover and reset"),
    ("2026-06-15-engage-surface-debate",       "Engage",  "Ask coaches: grass, astro or indoor — which surface teaches keepers the most and why"),
    ("2026-06-16-value-wet-weather",           "Value",   "Handling the ball in wet weather: grip choices, when to parry everything, adjusting footwork"),
    ("2026-06-17-story-coaching-own-child",    "Story",   "Coaching your own child as a goalkeeper — the line between coach and parent on the pitch"),
    ("2026-06-18-product-periodization",       "Product", "Periodization across a goalkeeping season: base, load, peak and taper for keepers"),
    ("2026-06-19-value-close-range-footwork",  "Value",   "Footwork for close-range shots: short steps, set early, hands ready in tight spaces"),
    ("2026-06-20-product-drill-library",       "Product", "Navigating a goalkeeper drill library by purpose so you find the right drill in seconds"),
]


def load_system_prompt() -> str:
    return (ROOT / "agents" / "content-creator.md").read_text(encoding="utf-8")


def strip_fences(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def generate_one(client: Anthropic, system: str, slug: str, ptype: str, topic: str) -> tuple[str, str]:
    out = ROOT / "content" / "captions" / f"{slug}.md"
    if out.exists():
        return slug, "skipped (exists)"
    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2000,
        system=system,
        messages=[{
            "role": "user",
            "content": f"Please draft a {ptype} post for KEEPIX.\n\nTopic: {topic}\n\nFollow the output format exactly.",
        }],
    )
    text = strip_fences("".join(b.text for b in resp.content if getattr(b, "type", None) == "text").strip())
    out.write_text(text + "\n", encoding="utf-8")
    return slug, f"ok ({len(text)} chars)"


def main() -> None:
    require("ANTHROPIC_API_KEY", ANTHROPIC_KEY)
    client = Anthropic(api_key=ANTHROPIC_KEY)
    system = load_system_prompt()

    results: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(generate_one, client, system, s, t, top): s for s, t, top in PLAN}
        for fut in as_completed(futs):
            slug = futs[fut]
            try:
                slug, status = fut.result()
            except Exception as e:
                status = f"ERROR: {e}"
            results[slug] = status
            print(f"  {slug:42}  {status}", file=sys.stderr)

    ok = sum(1 for v in results.values() if v.startswith("ok"))
    skip = sum(1 for v in results.values() if v.startswith("skipped"))
    err = sum(1 for v in results.values() if v.startswith("ERROR"))
    print(f"\nDONE: {ok} generated, {skip} skipped, {err} errors")


if __name__ == "__main__":
    main()
