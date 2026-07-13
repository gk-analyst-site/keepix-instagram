"""Check access token status and retrieve Instagram Business Account ID.

Usage:
  python scripts/token_refresh.py              # inspect current long-lived token
  python scripts/token_refresh.py --exchange   # exchange SHORT token (META_ACCESS_TOKEN) for a 60-day token
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys

from _common import (
    ACCESS_TOKEN,
    APP_ID,
    APP_SECRET,
    PAGE_ID,
    graph_get,
    require,
)


def debug_token() -> dict:
    require("META_ACCESS_TOKEN", ACCESS_TOKEN)
    require("META_APP_ID", APP_ID)
    require("META_APP_SECRET", APP_SECRET)
    app_token = f"{APP_ID}|{APP_SECRET}"
    return graph_get(
        "/debug_token",
        {"input_token": ACCESS_TOKEN, "access_token": app_token},
    )


def exchange_long_lived() -> dict:
    require("META_ACCESS_TOKEN", ACCESS_TOKEN)
    require("META_APP_ID", APP_ID)
    require("META_APP_SECRET", APP_SECRET)
    return graph_get(
        "/oauth/access_token",
        {
            "grant_type": "fb_exchange_token",
            "client_id": APP_ID,
            "client_secret": APP_SECRET,
            "fb_exchange_token": ACCESS_TOKEN,
        },
    )


def list_pages() -> dict:
    return graph_get("/me/accounts", {"fields": "id,name,instagram_business_account"})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exchange", action="store_true", help="Exchange token for a long-lived one")
    args = ap.parse_args()

    if args.exchange:
        resp = exchange_long_lived()
        print("Long-lived token response:")
        print(resp)
        print("\nCopy access_token into config/.env as META_ACCESS_TOKEN.")
        return

    info = debug_token().get("data", {})
    if not info:
        print("[error] empty debug_token response", file=sys.stderr)
        sys.exit(1)

    exp_ts = info.get("expires_at")
    if exp_ts:
        exp_dt = dt.datetime.fromtimestamp(exp_ts, tz=dt.timezone.utc)
        days_left = (exp_dt - dt.datetime.now(dt.timezone.utc)).days
        print(f"Token expires: {exp_dt.isoformat()} ({days_left} days left)")
    else:
        print("Token has no expiry (or expires_at missing)")

    print(f"Scopes: {', '.join(info.get('scopes', []))}")
    print(f"Valid: {info.get('is_valid')}")

    print("\nLinked Facebook Pages:")
    pages = list_pages().get("data", [])
    if not pages:
        print("  (none — has this token been granted pages_show_list?)")
        return
    for p in pages:
        ig = p.get("instagram_business_account", {})
        ig_id = ig.get("id", "—")
        print(f"  page_id={p['id']}  name={p['name']}  ig_business_account_id={ig_id}")
        if PAGE_ID and p["id"] == PAGE_ID:
            print("    ^ matches FACEBOOK_PAGE_ID in .env")


if __name__ == "__main__":
    main()
