"""Batch-generate the 23 captions for 2026-06-21 .. 2026-07-13.

Same workflow as _batch_captions_may29_jun20.py — 5-worker threaded calls to
Claude with the content-creator system prompt. Idempotent (skips existing files).
"""
from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from anthropic import Anthropic

from _common import ANTHROPIC_KEY, CLAUDE_MODEL, ROOT, require

PLAN = [
    ("2026-06-21-value-low-vs-high-shots",       "Value",   "Reading low shots vs high shots — different stance entries, different recovery paths"),
    ("2026-06-22-product-one-coach-templates",   "Product", "Session templates for the solo keeper coach — when you're the only specialist on the pitch"),
    ("2026-06-23-value-chest-vs-hands",          "Value",   "Catching with the chest vs the hands — when each is the right call and the cue that decides"),
    ("2026-06-24-engage-only-10-minutes",        "Engage",  "Ask coaches: if you only had 10 minutes with your keeper this week, what's the one drill you'd run"),
    ("2026-06-25-value-defensive-line-comms",    "Value",   "Defensive line communication — when the keeper leads and the language that travels in 90 minutes"),
    ("2026-06-26-story-thought-wouldnt-make-it", "Story",   "The keeper I thought wasn't going to make it — and what changed when I stopped trying to fix him"),
    ("2026-06-27-product-matchday-routine",      "Product", "Building a match-day routine you can hand to a keeper and an assistant coach and still get the same picture"),
    ("2026-06-28-value-corner-communication",    "Value",   "Communication patterns when defending corners — who you talk to first and what you actually say"),
    ("2026-06-29-product-plans-to-reps",         "Product", "Translating a training plan into actual reps — closing the gap between what you wrote and what they did"),
    ("2026-06-30-value-restart-sets",            "Value",   "Restart sets — the kick-off as a defensive moment, not just the start of the half"),
    ("2026-07-01-engage-measure-confidence",     "Engage",  "Ask coaches: how do you measure a keeper's confidence — what's the signal that tells you they're back"),
    ("2026-07-02-value-saving-in-the-rain",      "Value",   "Saving in the rain — grip changes, contact choices, and the footwork adjustments wet grass demands"),
    ("2026-07-03-story-silence-test",            "Story",   "Coaching through a bad streak — the silence test, and the day I stopped trying to talk it out of them"),
    ("2026-07-04-product-drill-popularity",      "Product", "Tracking which drills your keepers actually like — and what that data tells you about your session"),
    ("2026-07-05-value-distribution-press",      "Value",   "Distribution under press — the short vs long decision and the two seconds that matter most"),
    ("2026-07-06-product-multi-age-curriculum",  "Product", "Building one curriculum for multiple age groups without diluting it for anyone"),
    ("2026-07-07-value-winger-body-shape",       "Value",   "Reading wingers' body shape in 1v1 — the hip, the planted foot, and what they give away early"),
    ("2026-07-08-engage-worst-feedback",         "Engage",  "Ask keepers and coaches: what's the worst piece of feedback you ever got — and why did it stick"),
    ("2026-07-09-value-limited-vision",          "Value",   "Goalkeeping with limited vision — sunset, low floodlights, and how to coach the keeper through it"),
    ("2026-07-10-story-stopped-feedback-rep",    "Story",   "Why I stopped giving feedback every rep — and what changed in the keepers because of it"),
    ("2026-07-11-product-tryout-protocol",       "Product", "Designing a goalkeeper-specific tryout protocol — what to look for, in what order, and what to ignore"),
    ("2026-07-12-value-near-post-crosses",       "Value",   "Compact box defense — keeper positioning on near-post crosses, the first step that decides the rest"),
    ("2026-07-13-product-concepts-vs-drills",    "Product", "Logging concepts vs logging drills — which one gives you a curriculum and which one gives you a folder of PDFs"),
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
