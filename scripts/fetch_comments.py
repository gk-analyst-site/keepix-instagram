"""Fetch comments on KEEPIX's own Instagram posts.

Usage:
  python scripts/fetch_comments.py                    # latest 10 media, their comments
  python scripts/fetch_comments.py --limit 25
  python scripts/fetch_comments.py --media MEDIA_ID   # single media
  python scripts/fetch_comments.py --save             # append JSON to data/comments.jsonl
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

from _common import IG_USER_ID, ROOT, graph_get, require


def list_recent_media(limit: int) -> list[dict]:
    resp = graph_get(
        f"/{IG_USER_ID}/media",
        {"fields": "id,caption,permalink,media_type,timestamp", "limit": limit},
    )
    return resp.get("data", [])


def list_comments(media_id: str) -> list[dict]:
    out: list[dict] = []
    params = {"fields": "id,text,username,timestamp,like_count,replies{id,text,username,timestamp}", "limit": 50}
    url_path = f"/{media_id}/comments"
    while True:
        resp = graph_get(url_path, params)
        out.extend(resp.get("data", []))
        next_url = resp.get("paging", {}).get("next")
        if not next_url:
            return out
        # naive pagination: re-extract the `after` cursor
        after = resp.get("paging", {}).get("cursors", {}).get("after")
        if not after:
            return out
        params["after"] = after


def main() -> None:
    require("INSTAGRAM_BUSINESS_ACCOUNT_ID", IG_USER_ID)
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10, help="How many recent media to scan")
    ap.add_argument("--media", help="Specific media id (skips media listing)")
    ap.add_argument("--save", action="store_true", help="Append to data/comments.jsonl")
    args = ap.parse_args()

    if args.media:
        media = [{"id": args.media, "caption": "", "permalink": "", "timestamp": ""}]
    else:
        media = list_recent_media(args.limit)
        if not media:
            print("[info] no media found on this account", file=sys.stderr)
            return

    results: list[dict] = []
    for m in media:
        comments = list_comments(m["id"])
        if not comments and not args.media:
            continue
        caption_snip = (m.get("caption") or "").strip().replace("\n", " ")[:80]
        print(f"\n=== {m['id']}  {caption_snip}")
        print(f"    {m.get('permalink', '')}")
        if not comments:
            print("    (no comments)")
        for c in comments:
            print(f"  @{c['username']}  {c['timestamp']}")
            print(f"    {c['text']}")
        results.append({"media": m, "comments": comments})

    if args.save:
        out = ROOT / "data" / "comments.jsonl"
        out.parent.mkdir(parents=True, exist_ok=True)
        stamp = dt.datetime.now(dt.timezone.utc).isoformat()
        with out.open("a", encoding="utf-8") as f:
            for r in results:
                f.write(json.dumps({"fetched_at": stamp, **r}, ensure_ascii=False) + "\n")
        print(f"\n[saved] {len(results)} media records -> {out}")


if __name__ == "__main__":
    main()
