"""One-off: upload all 2026-04-24..2026-04-30 slide PNGs to Cloudinary.

Uses the post folder name as a Cloudinary subfolder so public_ids don't collide
across days (each day has a 'slide-1.png').
"""
from __future__ import annotations

import json
from pathlib import Path

import cloudinary
import cloudinary.uploader

from _common import (
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
    CLOUDINARY_CLOUD_NAME,
)

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "content" / "posts"

POST_FOLDERS = [
    "2026-04-24-engage",
    "2026-04-25-story",
    "2026-04-26-reflection",
    "2026-04-27-value",
    "2026-04-28-quicktip",
    "2026-04-29-product",
    "2026-04-30-value",
]

result: dict[str, list[str]] = {}
for name in POST_FOLDERS:
    urls: list[str] = []
    pngs = sorted((POSTS_DIR / name).glob("slide-*.png"))
    for p in pngs:
        r = cloudinary.uploader.upload(
            str(p),
            folder=f"keepix-instagram/{name}",
            public_id=p.stem,
            overwrite=True,
            resource_type="image",
        )
        urls.append(r["secure_url"])
        print(f"{name}/{p.name} -> {r['secure_url']}")
    result[name] = urls

print("\n--- JSON ---")
print(json.dumps(result, indent=2))
