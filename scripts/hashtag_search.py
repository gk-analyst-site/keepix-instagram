"""Search a hashtag for recent / top posts to find prospect accounts (for MANUAL review).

Usage:
  python scripts/hashtag_search.py --tag goalkeepertraining
  python scripts/hashtag_search.py --tag gkcoach --mode recent --limit 50 --save

Important:
  - Output is a prospect list for a HUMAN to review and contact.
  - This script does NOT like / comment / follow. Doing so automatically violates
    Meta's Platform Terms.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

from _common import IG_USER_ID, ROOT, graph_get, require


def resolve_hashtag_id(tag: str) -> str:
    tag = tag.lstrip("#")
    resp = graph_get("/ig_hashtag_search", {"user_id": IG_USER_ID, "q": tag})
    data = resp.get("data", [])
    if not data:
        print(f"[error] hashtag not found or unsearchable: #{tag}", file=sys.stderr)
        sys.exit(1)
    return data[0]["id"]


def fetch_hashtag_media(hashtag_id: str, mode: str, limit: int) -> list[dict]:
    edge = "top_media" if mode == "top" else "recent_media"
    resp = graph_get(
        f"/{hashtag_id}/{edge}",
        {
            "user_id": IG_USER_ID,
            "fields": "id,caption,permalink,media_type,media_url,timestamp",
            "limit": limit,
        },
    )
    return resp.get("data", [])


def main() -> None:
    require("INSTAGRAM_BUSINESS_ACCOUNT_ID", IG_USER_ID)
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True, help="Hashtag (with or without #)")
    ap.add_argument("--mode", choices=["top", "recent"], default="top")
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--save", action="store_true", help="Append results to data/hashtag_<tag>.jsonl")
    args = ap.parse_args()

    tag = args.tag.lstrip("#")
    hid = resolve_hashtag_id(tag)
    print(f"#{tag} -> id={hid}  mode={args.mode}  limit={args.limit}")

    posts = fetch_hashtag_media(hid, args.mode, args.limit)
    print(f"got {len(posts)} posts\n")

    for p in posts:
        caption = (p.get("caption") or "").strip().replace("\n", " ")
        print(f"- {p['permalink']}")
        print(f"    {caption[:140]}")

    if args.save:
        out = ROOT / "data" / f"hashtag_{tag}.jsonl"
        out.parent.mkdir(parents=True, exist_ok=True)
        stamp = dt.datetime.now(dt.timezone.utc).isoformat()
        with out.open("a", encoding="utf-8") as f:
            for p in posts:
                f.write(json.dumps({"fetched_at": stamp, "tag": tag, **p}, ensure_ascii=False) + "\n")
        print(f"\n[saved] -> {out}")

    print("\nreminder: this list is for MANUAL review. no automated likes/comments/follows.")


if __name__ == "__main__":
    main()
