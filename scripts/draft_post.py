"""Generate a KEEPIX Instagram post draft using the content-creator agent's system prompt.

Usage:
  python scripts/draft_post.py --type Value --topic "3 footwork drills for shot-stoppers"
  python scripts/draft_post.py --type Product --topic "setting up a session with KEEPIX"
  python scripts/draft_post.py --type Engage --topic "favorite pre-match warm-up"
  python scripts/draft_post.py --type Story  --topic "why we built KEEPIX"
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from anthropic import Anthropic

from _common import ANTHROPIC_KEY, CLAUDE_MODEL, ROOT, require


def load_system_prompt() -> str:
    agent_path = ROOT / "agents" / "content-creator.md"
    return agent_path.read_text(encoding="utf-8")


def main() -> None:
    require("ANTHROPIC_API_KEY", ANTHROPIC_KEY)
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True, choices=["Product", "Story", "Value", "Engage"])
    ap.add_argument("--topic", required=True, help="One-line brief of what the post is about")
    ap.add_argument("--save", help="Optional: save caption-only section to content/captions/<FILE>")
    args = ap.parse_args()

    client = Anthropic(api_key=ANTHROPIC_KEY)
    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2000,
        system=load_system_prompt(),
        messages=[{
            "role": "user",
            "content": f"Please draft a {args.type} post for KEEPIX.\n\nTopic: {args.topic}\n\nFollow the output format exactly.",
        }],
    )
    text = "".join(b.text for b in resp.content if getattr(b, "type", None) == "text").strip()

    # Strip markdown code fences Claude sometimes adds
    lines = text.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    text = "\n".join(lines).strip()

    print(text)

    if args.save:
        out = ROOT / "content" / "captions" / args.save
        out.parent.mkdir(parents=True, exist_ok=True)
        # Save full structured draft (matches existing caption file format)
        out.write_text(text + "\n", encoding="utf-8")
        print(f"\n[saved] -> {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
