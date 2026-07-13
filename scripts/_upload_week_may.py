"""One-off: upload all 2026-05-01..2026-05-07 slide PNGs to Cloudinary."""
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
    "2026-05-01-quicktip",
    "2026-05-02-reflection",
    "2026-05-03-engage",
    "2026-05-04-story",
    "2026-05-05-value",
    "2026-05-06-quicktip",
    "2026-05-07-product",
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
