"""Draft a reply to an IG comment with Claude, then send ONLY after human approval.

Three steps, always in this order:
  1) generate draft with Claude
  2) show to human, wait for y / n / e(dit)
  3) if approved, POST /{comment-id}/replies

Usage:
  python scripts/reply_comment.py --comment COMMENT_ID
  python scripts/reply_comment.py --comment COMMENT_ID --context "Product post about footwork"
"""
from __future__ import annotations

import argparse
import sys

from anthropic import Anthropic

from _common import ANTHROPIC_KEY, CLAUDE_MODEL, graph_get, graph_post, require

SYSTEM_PROMPT = """You draft replies to Instagram comments on KEEPIX's posts.
KEEPIX is a goalkeeper training product for coaches. Audience: goalkeeper coaches
outside Japan — English primary.

Rules:
- Never describe KEEPIX with AI / machine-learning / algorithmic language.
- 1-3 sentences, coach-to-coach tone.
- Never promise shipping dates, compatibility, or pricing you can't verify.
- If the comment is sensitive (injury, medical, politics, harassment), reply with
  just the token: SKIP — do not draft.
- If the comment is spam / promo / unrelated, reply with: SKIP.

Return ONLY the draft reply text (or SKIP). No preamble, no quotes, no labels."""


def fetch_comment(comment_id: str) -> dict:
    return graph_get(
        f"/{comment_id}",
        {"fields": "id,text,username,timestamp,media{id,caption,permalink}"},
    )


def draft_reply(client: Anthropic, comment_text: str, username: str, context: str) -> str:
    user_msg = (
        f"POST CONTEXT: {context or '(none provided)'}\n"
        f"COMMENT from @{username}: {comment_text}\n\n"
        "Draft the reply."
    )
    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    return "".join(b.text for b in resp.content if getattr(b, "type", None) == "text").strip()


def send_reply(comment_id: str, text: str) -> dict:
    return graph_post(f"/{comment_id}/replies", {"message": text})


def approve_loop(draft: str) -> str | None:
    """Return the approved text, or None to abort."""
    while True:
        print("\n--- DRAFT REPLY ---")
        print(draft)
        print("-------------------")
        choice = input("send? [y]es / [n]o / [e]dit / [r]egenerate: ").strip().lower()
        if choice == "y":
            return draft
        if choice == "n":
            return None
        if choice == "e":
            print("Enter the reply text (end with a single '.' on its own line):")
            lines: list[str] = []
            while True:
                line = input()
                if line == ".":
                    break
                lines.append(line)
            edited = "\n".join(lines).strip()
            if edited:
                draft = edited
            continue
        if choice == "r":
            return "__REGENERATE__"


def main() -> None:
    require("ANTHROPIC_API_KEY", ANTHROPIC_KEY)
    ap = argparse.ArgumentParser()
    ap.add_argument("--comment", required=True, help="IG comment id")
    ap.add_argument("--context", default="", help="Brief context (post type / caption snippet)")
    args = ap.parse_args()

    comment = fetch_comment(args.comment)
    text = comment.get("text", "")
    username = comment.get("username", "unknown")
    if not text:
        print("[error] comment has no text", file=sys.stderr)
        sys.exit(1)

    context = args.context
    if not context and comment.get("media", {}).get("caption"):
        context = comment["media"]["caption"].strip().replace("\n", " ")[:200]

    print(f"Comment from @{username}:")
    print(f"  {text}")

    client = Anthropic(api_key=ANTHROPIC_KEY)

    while True:
        draft = draft_reply(client, text, username, context)
        if draft.strip().upper() == "SKIP":
            print("\n[claude] proposes SKIP — nothing to send. Done.")
            return

        approved = approve_loop(draft)
        if approved is None:
            print("[aborted] no reply sent.")
            return
        if approved == "__REGENERATE__":
            continue

        resp = send_reply(args.comment, approved)
        print(f"[sent] reply id = {resp.get('id')}")
        return


if __name__ == "__main__":
    main()
