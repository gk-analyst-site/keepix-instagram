"""Batch-generate the 23 captions for 2026-07-14 .. 2026-08-05."""
from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from anthropic import Anthropic

from _common import ANTHROPIC_KEY, CLAUDE_MODEL, ROOT, require

PLAN = [
    ("2026-07-14-value-narrowing-angles",        "Value",   "Narrowing the angle in 1v1 — how far to come, the arc not the straight line, and the moment to hold"),
    ("2026-07-15-product-periodised-block",      "Product", "Building a periodised training block for a keeper — base, build, peak — inside one planning system instead of loose PDFs"),
    ("2026-07-16-value-claiming-crowded-crosses","Value",   "Claiming crosses in a crowded box — the call, the jump through traffic, and protecting the ball on the way down"),
    ("2026-07-17-engage-first-preseason-drill",  "Engage",  "Ask coaches: what's the very first drill you run on day one of pre-season with your keepers"),
    ("2026-07-18-value-parry-zones",             "Value",   "Parrying to safe zones — steering the ball wide and away from danger instead of straight back into play"),
    ("2026-07-19-story-save-not-coached",        "Story",   "The save I never coached — watching a keeper solve a moment we'd never trained, and what it taught me about over-coaching"),
    ("2026-07-20-product-save-type-tracking",    "Product", "Tracking save types over a season — seeing which situations a keeper actually faces so training matches the game"),
    ("2026-07-21-value-long-range-set",          "Value",   "Set position for long-range shots — depth off the line, weight, and staying big when the shot comes early"),
    ("2026-07-22-product-drills-for-parents",    "Product", "Sharing simple keeper drills parents can run at home without turning them into coaches"),
    ("2026-07-23-value-reading-second-ball",     "Value",   "Reading the second ball — where to look after the first save and how to be set before the rebound arrives"),
    ("2026-07-24-engage-how-you-end-session",    "Engage",  "Ask coaches: how do you end a keeper session — a game, a challenge, a quiet word — and why"),
    ("2026-07-25-value-goal-kick-buildup",       "Value",   "The keeper in build-up from goal kicks — scanning before the ball is placed, body shape to receive, and the first safe option"),
    ("2026-07-26-story-keeper-quit-came-back",   "Story",   "The keeper who quit for a season and came back — what changed, and why the break made him better"),
    ("2026-07-27-product-theme-tagging-drills",  "Product", "Tagging drills by theme so you can build a whole session around one weakness in under five minutes"),
    ("2026-07-28-value-handling-deflections",    "Value",   "Handling deflections — staying tall late, short adjusting steps, and trusting the hands when the ball changes direction"),
    ("2026-07-29-value-one-handed-saves",        "Value",   "One-handed saves — when reaching with one hand beats two, and how to coach a strong, firm contact"),
    ("2026-07-30-engage-what-age-start-diving",  "Engage",  "Ask coaches: what age do you actually start teaching young keepers to dive, and how do you introduce it safely"),
    ("2026-07-31-product-preseason-testing",     "Product", "Building a simple pre-season testing battery for keepers so you can measure progress, not just feel it"),
    ("2026-08-01-value-close-range-reactions",   "Value",   "Close-range reaction saves — hand speed, staying on the feet, and not committing to ground too early"),
    ("2026-08-02-story-learning-to-say-less",    "Story",   "Learning to say less on the pitch — the season I cut my coaching cues in half and the keepers got sharper"),
    ("2026-08-03-value-near-post-shot-defense",  "Value",   "Defending the near post on shots — why the near post is non-negotiable and the footwork that protects it"),
    ("2026-08-04-product-progress-report",       "Product", "Turning a season of session notes into a one-page progress report you can hand a keeper or a parent"),
    ("2026-08-05-value-recovering-after-beaten", "Value",   "Recovery after being beaten — the scramble save, getting back to your feet, and never giving up on the second effort"),
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
            print(f"  {slug:48}  {status}", file=sys.stderr)

    ok = sum(1 for v in results.values() if v.startswith("ok"))
    skip = sum(1 for v in results.values() if v.startswith("skipped"))
    err = sum(1 for v in results.values() if v.startswith("ERROR"))
    print(f"\nDONE: {ok} generated, {skip} skipped, {err} errors")


if __name__ == "__main__":
    main()
