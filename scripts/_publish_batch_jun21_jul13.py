"""Upload the 23 slides (6/21..7/13) to Cloudinary and append calendar entries.

Same pattern as _publish_batch_may29_jun20.py. Idempotent via overwrite=True.
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
    ("2026-06-21-value-low-vs-high-shots",       "Value",   "2026-06-21", "Reading low shots vs high shots"),
    ("2026-06-22-product-one-coach-templates",   "Product", "2026-06-22", "Session templates for the solo keeper coach"),
    ("2026-06-23-value-chest-vs-hands",          "Value",   "2026-06-23", "Catching with the chest vs the hands"),
    ("2026-06-24-engage-only-10-minutes",        "Engage",  "2026-06-24", "If you only had 10 minutes — what drill?"),
    ("2026-06-25-value-defensive-line-comms",    "Value",   "2026-06-25", "Defensive line communication"),
    ("2026-06-26-story-thought-wouldnt-make-it", "Story",   "2026-06-26", "The keeper I thought wasn't going to make it"),
    ("2026-06-27-product-matchday-routine",      "Product", "2026-06-27", "Building a match-day routine"),
    ("2026-06-28-value-corner-communication",    "Value",   "2026-06-28", "Communication when defending corners"),
    ("2026-06-29-product-plans-to-reps",         "Product", "2026-06-29", "Translating training plans into reps"),
    ("2026-06-30-value-restart-sets",            "Value",   "2026-06-30", "Restart sets — the kick-off as defense"),
    ("2026-07-01-engage-measure-confidence",     "Engage",  "2026-07-01", "How do you measure a keeper's confidence?"),
    ("2026-07-02-value-saving-in-the-rain",      "Value",   "2026-07-02", "Saving in the rain — grip and contact"),
    ("2026-07-03-story-silence-test",            "Story",   "2026-07-03", "Coaching through a bad streak — the silence test"),
    ("2026-07-04-product-drill-popularity",      "Product", "2026-07-04", "Tracking which drills keepers actually like"),
    ("2026-07-05-value-distribution-press",      "Value",   "2026-07-05", "Distribution under press — short vs long"),
    ("2026-07-06-product-multi-age-curriculum",  "Product", "2026-07-06", "Curriculum across multiple age groups"),
    ("2026-07-07-value-winger-body-shape",       "Value",   "2026-07-07", "Reading wingers' body shape in 1v1"),
    ("2026-07-08-engage-worst-feedback",         "Engage",  "2026-07-08", "Worst feedback you ever got — and why it stuck"),
    ("2026-07-09-value-limited-vision",          "Value",   "2026-07-09", "Goalkeeping with limited vision"),
    ("2026-07-10-story-stopped-feedback-rep",    "Story",   "2026-07-10", "Why I stopped giving feedback every rep"),
    ("2026-07-11-product-tryout-protocol",       "Product", "2026-07-11", "Goalkeeper-specific tryout protocol"),
    ("2026-07-12-value-near-post-crosses",       "Value",   "2026-07-12", "Keeper positioning on near-post crosses"),
    ("2026-07-13-product-concepts-vs-drills",    "Product", "2026-07-13", "Logging concepts vs logging drills"),
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
        print(f"  ✓ {slug:48}  {ptype:8}  uploaded + scheduled", file=sys.stderr)

    cal["posts"].sort(key=lambda p: p["scheduled_at"])
    cal_path.write_text(json.dumps(cal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nDONE: calendar now has {len(cal['posts'])} posts", file=sys.stderr)


if __name__ == "__main__":
    main()
