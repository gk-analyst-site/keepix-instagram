"""Shared helpers for Instagram Graph API scripts."""
from __future__ import annotations

import datetime as dt
import os
import re
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / "config" / ".env"
load_dotenv(ENV_PATH, override=True)

GRAPH_VERSION = os.getenv("GRAPH_API_VERSION", "v19.0")
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_VERSION}"

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "").strip()
IG_USER_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
APP_ID = os.getenv("META_APP_ID", "").strip()
APP_SECRET = os.getenv("META_APP_SECRET", "").strip()
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "").strip()
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "").strip()
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "").strip()
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "").strip()


def require(name: str, value: str) -> str:
    if not value:
        print(f"[error] missing env var: {name}. Fill it in config/.env", file=sys.stderr)
        sys.exit(2)
    return value


def graph_get(path: str, params: dict | None = None) -> dict:
    params = dict(params or {})
    params.setdefault("access_token", ACCESS_TOKEN)
    r = requests.get(f"{GRAPH_BASE}{path}", params=params, timeout=30)
    _raise_with_body(r)
    return r.json()


def graph_post(path: str, data: dict) -> dict:
    data = dict(data)
    data.setdefault("access_token", ACCESS_TOKEN)
    r = requests.post(f"{GRAPH_BASE}{path}", data=data, timeout=60)
    _raise_with_body(r)
    return r.json()


def _raise_with_body(r: requests.Response) -> None:
    if r.ok:
        return
    try:
        body = r.json()
    except Exception:
        body = r.text
    print(f"[graph api error] {r.status_code}: {body}", file=sys.stderr)
    r.raise_for_status()


# ---------- Caption parser ----------

_SECTION_KEYS = ("CAPTION", "CTA", "HASHTAGS", "IMAGE BRIEF", "ALT TEXT")


def parse_caption_file(path: Path) -> dict:
    """Parse a structured caption .md file into its sections.

    Recognises: TYPE, HOOK, CAPTION, CTA, HASHTAGS, IMAGE BRIEF, ALT TEXT.
    Returns a dict with those keys (missing keys absent).
    """
    text = path.read_text(encoding="utf-8")
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []

    for line in text.splitlines():
        # TYPE
        if line.startswith("TYPE:"):
            if current:
                sections[current] = "\n".join(buf).strip()
                current, buf = None, []
            sections["TYPE"] = line[len("TYPE:"):].strip()
            continue
        # HOOK (may contain inline qualifier "HOOK (first line of caption):")
        m = re.match(r"HOOK[^:]*:\s*(.*)", line)
        if m:
            if current:
                sections[current] = "\n".join(buf).strip()
                current, buf = None, []
            sections["HOOK"] = m.group(1).strip()
            continue
        # Section starts
        matched = False
        for key in _SECTION_KEYS:
            prefix = f"{key}:"
            if line.startswith(prefix):
                if current:
                    sections[current] = "\n".join(buf).strip()
                current = key
                buf = []
                rest = line[len(prefix):].strip()
                if rest:
                    buf.append(rest)
                matched = True
                break
        if matched:
            continue
        if current:
            buf.append(line)

    if current:
        sections[current] = "\n".join(buf).strip()
    return sections


def assemble_ig_caption(sections: dict, max_chars: int = 2200) -> str:
    """Assemble the actual Instagram caption from parsed sections.

    Order: HOOK (blank) CAPTION (blank) CTA (blank) HASHTAGS.
    Excludes IMAGE BRIEF and ALT TEXT (internal-only).
    """
    parts: list[str] = []
    if sections.get("HOOK"):
        parts.append(sections["HOOK"])
    if sections.get("CAPTION"):
        parts.append(sections["CAPTION"])
    if sections.get("CTA"):
        parts.append(sections["CTA"])
    if sections.get("HASHTAGS"):
        parts.append(sections["HASHTAGS"])
    text = "\n\n".join(parts).strip()
    if len(text) > max_chars:
        print(f"[warn] caption is {len(text)} chars; truncating to {max_chars}", file=sys.stderr)
        text = text[:max_chars]
    return text


# ---------- Simple logger ----------

LOG_PATH = ROOT / "data" / "publish.log"


def log(message: str) -> None:
    """Append a timestamped line to data/publish.log and echo to stderr."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"{stamp}  {message}"
    print(line, file=sys.stderr)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
