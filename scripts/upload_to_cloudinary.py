"""Upload local image files to Cloudinary under the keepix-instagram folder.

Usage:
  python scripts/upload_to_cloudinary.py path/to/1.png path/to/2.png
  python scripts/upload_to_cloudinary.py content/posts/2026-04-23-value/*.png

Emits a JSON list of { "file", "public_id", "secure_url" } objects on stdout
so the result can be piped into other tools.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cloudinary
import cloudinary.uploader

from _common import (
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
    CLOUDINARY_CLOUD_NAME,
    require,
)

DEFAULT_FOLDER = "keepix-instagram"


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


def upload_one(path: Path, folder: str) -> dict:
    if not path.exists():
        print(f"[error] file not found: {path}", file=sys.stderr)
        sys.exit(2)
    res = cloudinary.uploader.upload(
        str(path),
        folder=folder,
        public_id=path.stem,
        overwrite=True,
        resource_type="image",
    )
    return {
        "file": str(path),
        "public_id": res["public_id"],
        "secure_url": res["secure_url"],
    }


def upload_many(paths: list[Path], folder: str) -> list[dict]:
    return [upload_one(p, folder) for p in paths]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", help="Local image file paths")
    ap.add_argument("--folder", default=DEFAULT_FOLDER, help="Cloudinary folder (default: keepix-instagram)")
    args = ap.parse_args()

    configure()
    paths = [Path(f).expanduser().resolve() for f in args.files]
    results = upload_many(paths, args.folder)
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
