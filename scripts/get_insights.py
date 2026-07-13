"""Fetch account and per-post insights, save to data/insights/.

Usage:
  python scripts/get_insights.py                 # account-level (last 28 days) + latest 10 posts
  python scripts/get_insights.py --posts 25
  python scripts/get_insights.py --media MEDIA_ID
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from _common import IG_USER_ID, ROOT, graph_get, require

ACCOUNT_METRICS = ["impressions", "reach", "profile_views", "website_clicks", "follower_count"]
POST_METRICS_IMAGE = ["impressions", "reach", "saved", "likes", "comments", "shares"]
POST_METRICS_REEL = ["plays", "reach", "saved", "likes", "comments", "shares"]


def account_insights(days: int) -> dict:
    since = int((dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).timestamp())
    until = int(dt.datetime.now(dt.timezone.utc).timestamp())
    return graph_get(
        f"/{IG_USER_ID}/insights",
        {"metric": ",".join(ACCOUNT_METRICS), "period": "day", "since": since, "until": until},
    )


def account_profile() -> dict:
    return graph_get(
        f"/{IG_USER_ID}",
        {"fields": "username,followers_count,follows_count,media_count"},
    )


def list_recent_posts(limit: int) -> list[dict]:
    resp = graph_get(
        f"/{IG_USER_ID}/media",
        {"fields": "id,caption,permalink,media_type,media_product_type,timestamp", "limit": limit},
    )
    return resp.get("data", [])


def post_insights(media_id: str, media_product_type: str | None) -> dict:
    metrics = POST_METRICS_REEL if media_product_type == "REELS" else POST_METRICS_IMAGE
    try:
        return graph_get(f"/{media_id}/insights", {"metric": ",".join(metrics)})
    except Exception as e:
        return {"error": str(e)}


def main() -> None:
    require("INSTAGRAM_BUSINESS_ACCOUNT_ID", IG_USER_ID)
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=28)
    ap.add_argument("--posts", type=int, default=10)
    ap.add_argument("--media", help="Single media id; skips account-level")
    args = ap.parse_args()

    out_dir = ROOT / "data" / "insights"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")

    if args.media:
        data = post_insights(args.media, None)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        (out_dir / f"post-{args.media}-{stamp}.json").write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return

    profile = account_profile()
    print("== Profile ==")
    print(json.dumps(profile, indent=2, ensure_ascii=False))

    acct = account_insights(args.days)
    print(f"\n== Account insights (last {args.days}d) ==")
    for metric in acct.get("data", []):
        values = metric.get("values", [])
        total = sum(v.get("value", 0) or 0 for v in values if isinstance(v.get("value"), (int, float)))
        print(f"  {metric['name']}: total={total}  days={len(values)}")

    posts = list_recent_posts(args.posts)
    print(f"\n== Post insights (latest {len(posts)}) ==")
    posts_out: list[dict] = []
    for p in posts:
        stats = post_insights(p["id"], p.get("media_product_type"))
        caption_snip = (p.get("caption") or "").strip().replace("\n", " ")[:60]
        print(f"  {p['id']}  {p.get('timestamp', '')[:10]}  {caption_snip}")
        for m in stats.get("data", []):
            vals = m.get("values", [])
            v = vals[0].get("value") if vals else None
            print(f"    {m['name']}: {v}")
        posts_out.append({"post": p, "insights": stats})

    bundle = {
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "profile": profile,
        "account_insights": acct,
        "posts": posts_out,
    }
    out_file = out_dir / f"account-{stamp}.json"
    out_file.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[saved] -> {out_file}")


if __name__ == "__main__":
    main()
