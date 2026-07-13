"""Upload the 23 slides (5/29..6/20) to Cloudinary and append calendar entries.

For each post: upload content/posts/<id>/slide-1.png to Cloudinary folder
keepix-instagram/<id>, then add/replace a calendar.json entry with
status="scheduled", scheduled_at = <date>T22:00:00+09:00, image_urls=[url].

Idempotent: re-running re-uploads (overwrite=True) and updates the entry in place.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cloudinary
import cloudinary.uploader

from _common import (
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
    CLOUDINARY_CLOUD_NAME,
    ROOT,
    require,
)

# (id, type, scheduled_date, theme)
PLAN = [
    ("2026-05-29-value-catch-vs-parry",          "Value",   "2026-05-29", "Catching vs parrying — when to choose each"),
    ("2026-05-30-product-season-tracking",       "Product", "2026-05-30", "Tracking a keeper's progress across a season"),
    ("2026-05-31-value-through-ball-position",   "Value",   "2026-05-31", "Starting position for through balls"),
    ("2026-06-01-engage-non-negotiable",         "Engage",  "2026-06-01", "Your non-negotiable in every keeper session"),
    ("2026-06-02-value-high-balls-timing",       "Value",   "2026-06-02", "High balls: timing the jump"),
    ("2026-06-03-story-keeper-nobody-picked",    "Story",   "2026-06-03", "The keeper nobody picked who became captain"),
    ("2026-06-04-product-age-appropriate",       "Product", "2026-06-04", "Age-appropriate sessions: U10 vs U16"),
    ("2026-06-05-value-recovery-saves",          "Value",   "2026-06-05", "Recovery saves: getting back up fast"),
    ("2026-06-06-product-small-spaces",          "Product", "2026-06-06", "Adapting drills for small training spaces"),
    ("2026-06-07-value-backpass-pressure",       "Value",   "2026-06-07", "Receiving back-passes under pressure"),
    ("2026-06-08-engage-lost-confidence",        "Engage",  "2026-06-08", "Bringing back a keeper who lost confidence"),
    ("2026-06-09-value-organizing-wall",         "Value",   "2026-06-09", "Organizing the wall: communication"),
    ("2026-06-10-story-mistake-changed-coaching","Story",   "2026-06-10", "A mistake that changed how I coach"),
    ("2026-06-11-product-share-with-assistants", "Product", "2026-06-11", "Sharing session plans with assistants"),
    ("2026-06-12-value-diving-technique",        "Value",   "2026-06-12", "Diving: collapse save vs power dive"),
    ("2026-06-13-product-video-review",          "Product", "2026-06-13", "Pairing video review with session plans"),
    ("2026-06-14-value-rebounds-second-phase",   "Value",   "2026-06-14", "Reading rebounds and second phases"),
    ("2026-06-15-engage-surface-debate",         "Engage",  "2026-06-15", "Grass, astro or indoor — where keepers learn most"),
    ("2026-06-16-value-wet-weather",             "Value",   "2026-06-16", "Handling the ball in wet weather"),
    ("2026-06-17-story-coaching-own-child",      "Story",   "2026-06-17", "Coaching your own child as a keeper"),
    ("2026-06-18-product-periodization",         "Product", "2026-06-18", "Periodization across a GK season"),
    ("2026-06-19-value-close-range-footwork",    "Value",   "2026-06-19", "Footwork for close-range shots"),
    ("2026-06-20-product-drill-library",         "Product", "2026-06-20", "Navigating a drill library by purpose"),
]


def configure() -> None:
    require("CLOUDINARY_CLOUD_NAME", CLOUDINARY_CLOUD_NAME)
    require("CLOUDINARY_API_KEY", CLOUDINARY_API_KEY)
    require("CLOUDINARY_API_SECRET", CLOUDINARY_API_SECRET)
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
        secure=True,
    )


def main() -> None:
    configure()
    cal_path = ROOT / "content" / "calendar.json"
    cal = json.loads(cal_path.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in cal["posts"]}

    for slug, ptype, date, theme in PLAN:
        png = ROOT / "content" / "posts" / slug / "slide-1.png"
        if not png.exists():
            print(f"  [skip] no slide: {slug}", file=sys.stderr)
            continue
        res = cloudinary.uploader.upload(
            str(png),
            folder=f"keepix-instagram/{slug}",
            public_id="slide-1",
            overwrite=True,
            resource_type="image",
        )
        url = res["secure_url"]
        entry = {
            "id": slug,
            "scheduled_at": f"{date}T22:00:00+09:00",
            "type": ptype,
            "theme": theme,
            "caption_path": f"content/captions/{slug}.md",
            "image_urls": [url],
            "status": "scheduled",
        }
        if slug in by_id:
            by_id[slug].update(entry)
        else:
            cal["posts"].append(entry)
        print(f"  ✓ {slug:42}  {ptype:8}  uploaded + scheduled", file=sys.stderr)

    # Keep posts sorted by scheduled_at
    cal["posts"].sort(key=lambda p: p["scheduled_at"])
    cal_path.write_text(json.dumps(cal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nDONE: calendar now has {len(cal['posts'])} posts", file=sys.stderr)


if __name__ == "__main__":
    main()
