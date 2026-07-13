"""Publish an image / carousel / video post to Instagram via Graph API.

Two-step protocol:
  1) create a media container (or N item-containers + 1 carousel container)
  2) poll container status until FINISHED
  3) call /media_publish

Caption files (content/captions/<id>.md) are structured documents:
  TYPE / HOOK / CAPTION / CTA / HASHTAGS / IMAGE BRIEF / ALT TEXT
Only HOOK + CAPTION + CTA + HASHTAGS are joined into the IG caption.
IMAGE BRIEF and ALT TEXT are internal notes.

Usage:
  python scripts/post_to_instagram.py --from-calendar 2026-05-20-product-crossing-session
  python scripts/post_to_instagram.py --from-calendar 2026-05-20-product-crossing-session --dry-run
  python scripts/post_to_instagram.py --image URL --caption-file content/captions/x.md
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from _common import (
    IG_USER_ID,
    ROOT,
    assemble_ig_caption,
    graph_get,
    graph_post,
    log,
    parse_caption_file,
    require,
)

CONTAINER_POLL_INTERVAL_S = 5
CONTAINER_POLL_TIMEOUT_S = 240


def create_item_container(image_url: str | None, video_url: str | None, is_carousel_item: bool, caption: str | None) -> str:
    """Create a single media container. For carousels, leave caption=None on items."""
    require("INSTAGRAM_BUSINESS_ACCOUNT_ID", IG_USER_ID)
    data: dict = {}
    if caption is not None:
        data["caption"] = caption
    if video_url:
        data["media_type"] = "REELS"
        data["video_url"] = video_url
    else:
        data["image_url"] = image_url
    if is_carousel_item:
        data["is_carousel_item"] = "true"
    resp = graph_post(f"/{IG_USER_ID}/media", data)
    return resp["id"]


def create_carousel_container(child_ids: list[str], caption: str) -> str:
    require("INSTAGRAM_BUSINESS_ACCOUNT_ID", IG_USER_ID)
    data = {
        "media_type": "CAROUSEL",
        "children": ",".join(child_ids),
        "caption": caption,
    }
    resp = graph_post(f"/{IG_USER_ID}/media", data)
    return resp["id"]


def wait_ready(container_id: str, timeout_s: int = CONTAINER_POLL_TIMEOUT_S) -> None:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        info = graph_get(f"/{container_id}", {"fields": "status_code,status"})
        code = info.get("status_code")
        if code == "FINISHED":
            return
        if code == "ERROR":
            raise RuntimeError(f"media container {container_id} failed: {info}")
        time.sleep(CONTAINER_POLL_INTERVAL_S)
    raise TimeoutError(f"container {container_id} did not finish within {timeout_s}s")


def publish(container_id: str) -> dict:
    return graph_post(f"/{IG_USER_ID}/media_publish", {"creation_id": container_id})


def resolve_calendar_entry(post_id: str) -> dict:
    cal = json.loads((ROOT / "content" / "calendar.json").read_text(encoding="utf-8"))
    entry = next((p for p in cal.get("posts", []) if p["id"] == post_id), None)
    if not entry:
        raise SystemExit(f"[error] post id not found in calendar.json: {post_id}")
    return entry


def caption_from_entry(entry: dict) -> str:
    """Read the entry's caption_path (or caption_file) and return the IG-ready caption."""
    cap_rel = entry.get("caption_path") or entry.get("caption_file")
    if not cap_rel:
        raise SystemExit(f"[error] entry {entry['id']} has no caption_path/caption_file")
    cap_path = ROOT / cap_rel if "/" in cap_rel else ROOT / "content" / "captions" / cap_rel
    if not cap_path.exists():
        raise SystemExit(f"[error] caption file not found: {cap_path}")
    sections = parse_caption_file(cap_path)
    return assemble_ig_caption(sections)


def _emit_media_id(media_id: str | None) -> None:
    """Emit the canonical 'published media id = X' line so subprocess parsers
    (e.g. scheduled_post.py) can extract the ID from stdout reliably."""
    if media_id:
        print(f"  published media id = {media_id}")


def publish_entry(entry: dict, dry_run: bool = False) -> str | None:
    """Publish a calendar entry. Returns ig_media_id on success, None on dry-run."""
    image_urls: list[str] = list(entry.get("image_urls") or [])
    if not image_urls and entry.get("image_url"):
        image_urls = [entry["image_url"]]
    video_url = entry.get("video_url")

    if not image_urls and not video_url:
        raise SystemExit(f"[error] entry {entry['id']} has no image_urls or video_url")

    caption = caption_from_entry(entry)

    print(f"=== {entry['id']}  type={entry.get('type', '?')}  media={len(image_urls) or 1}")
    print(f"caption preview ({len(caption)} chars):")
    print(caption[:300] + ("…" if len(caption) > 300 else ""))
    print()

    if dry_run:
        print("[dry-run] no API call")
        return None

    # Single image / video → simple container
    if video_url or len(image_urls) == 1:
        log(f"[publish] {entry['id']} single-media")
        container_id = create_item_container(
            image_url=image_urls[0] if image_urls else None,
            video_url=video_url,
            is_carousel_item=False,
            caption=caption,
        )
        wait_ready(container_id)
        resp = publish(container_id)
        media_id = resp.get("id")
        log(f"[publish] {entry['id']} -> ig_media_id={media_id}")
        _emit_media_id(media_id)
        return media_id

    # Carousel (2–10 images)
    if len(image_urls) > 10:
        raise SystemExit(f"[error] {entry['id']}: carousel exceeds 10 images ({len(image_urls)})")

    log(f"[publish] {entry['id']} carousel({len(image_urls)})")
    child_ids: list[str] = []
    for url in image_urls:
        cid = create_item_container(image_url=url, video_url=None, is_carousel_item=True, caption=None)
        child_ids.append(cid)
    # All children must be FINISHED before assembling the carousel
    for cid in child_ids:
        wait_ready(cid)
    parent_id = create_carousel_container(child_ids, caption)
    wait_ready(parent_id)
    resp = publish(parent_id)
    media_id = resp.get("id")
    log(f"[publish] {entry['id']} -> ig_media_id={media_id}")
    return media_id


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-calendar", help="Calendar entry id")
    ap.add_argument("--image", help="Public HTTPS image URL (single)")
    ap.add_argument("--video", help="Public HTTPS video URL (Reels)")
    ap.add_argument("--caption-file", help="Path to caption .md file")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.from_calendar:
        entry = resolve_calendar_entry(args.from_calendar)
    else:
        if not (args.image or args.video):
            sys.exit("[error] need --from-calendar OR --image/--video + --caption-file")
        if not args.caption_file:
            sys.exit("[error] --caption-file required without --from-calendar")
        cap_path = Path(args.caption_file)
        sections = parse_caption_file(cap_path)
        caption = assemble_ig_caption(sections)
        entry = {
            "id": cap_path.stem,
            "type": sections.get("TYPE", "?"),
            "image_urls": [args.image] if args.image else [],
            "video_url": args.video,
            "caption_path": str(cap_path.resolve()),
        }
        # bypass caption_from_entry — we already parsed it
        # but publish_entry will re-parse; that's fine since the file exists

    media_id = publish_entry(entry, dry_run=args.dry_run)
    if media_id:
        print(f"\nPublished: https://www.instagram.com/p/  (media id {media_id})")


if __name__ == "__main__":
    main()
