"""Refresh the Meta long-lived access token and write it back into config/.env.

Runs daily via launchd. If the token is within THRESHOLD days of expiry it is
exchanged for a fresh 60-day token and written back to config/.env (backup kept
as config/.env.bak). The token is never printed or logged in full — only masked.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys

from _common import (
    ACCESS_TOKEN,
    APP_ID,
    APP_SECRET,
    ENV_PATH,
    ROOT,
    graph_get,
    require,
)

ALERTS_LOG = ROOT / "data" / "alerts.log"
DEFAULT_THRESHOLD_DAYS = 20


def alert(title: str, message: str) -> None:
    ALERTS_LOG.parent.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with ALERTS_LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {title} - {message}\n")
    try:
        safe_msg = message.replace('"', "'")
        safe_title = title.replace('"', "'")
        subprocess.run(
            ["osascript", "-e",
             f'display notification "{safe_msg}" with title "KEEPIX: {safe_title}"'],
            check=False, capture_output=True,
        )
    except Exception:
        pass


def mask(token: str) -> str:
    return f"{token[:6]}...{token[-4:]}" if len(token) > 12 else "****"


def debug_token() -> dict:
    require("META_ACCESS_TOKEN", ACCESS_TOKEN)
    require("META_APP_ID", APP_ID)
    require("META_APP_SECRET", APP_SECRET)
    app_token = f"{APP_ID}|{APP_SECRET}"
    return graph_get(
        "/debug_token",
        {"input_token": ACCESS_TOKEN, "access_token": app_token},
    ).get("data", {})


def exchange_long_lived() -> dict:
    return graph_get(
        "/oauth/access_token",
        {
            "grant_type": "fb_exchange_token",
            "client_id": APP_ID,
            "client_secret": APP_SECRET,
            "fb_exchange_token": ACCESS_TOKEN,
        },
    )


def days_left(info: dict) -> int | None:
    exp_ts = info.get("expires_at")
    if not exp_ts:
        return None
    exp = dt.datetime.fromtimestamp(exp_ts, tz=dt.timezone.utc)
    return (exp - dt.datetime.now(dt.timezone.utc)).days


def write_token(new_token: str) -> None:
    text = ENV_PATH.read_text(encoding="utf-8")
    (ENV_PATH.parent / ".env.bak").write_text(text, encoding="utf-8")
    if re.search(r"(?m)^META_ACCESS_TOKEN=", text):
        text = re.sub(r"(?m)^META_ACCESS_TOKEN=.*$", f"META_ACCESS_TOKEN={new_token}", text)
    else:
        text = text.rstrip("\n") + f"\nMETA_ACCESS_TOKEN={new_token}\n"
    ENV_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD_DAYS,
                    help="Refresh when fewer than this many days remain (default 20)")
    ap.add_argument("--force", action="store_true", help="Exchange now regardless of days left")
    args = ap.parse_args()

    info = debug_token()
    if not info:
        alert("token check failed", "debug_token returned empty. Token may be invalid.")
        sys.exit(1)

    if not info.get("is_valid"):
        alert("TOKEN INVALID", "Current token is not valid - re-auth needed via Graph API Explorer.")
        print("[error] token is not valid", file=sys.stderr)
        sys.exit(1)

    left = days_left(info)
    left_str = "no-expiry" if left is None else f"{left} days"
    print(f"Current token: valid, {left_str} left ({mask(ACCESS_TOKEN)})")

    need = args.force or (left is not None and left <= args.threshold)
    if not need:
        print(f"No refresh needed (threshold {args.threshold}d).")
        return

    print("Exchanging for a fresh 60-day token...")
    resp = exchange_long_lived()
    new_token = resp.get("access_token")
    if not new_token:
        alert("REFRESH FAILED", f"No access_token in exchange response: {resp}")
        print(f"[error] exchange failed: {resp}", file=sys.stderr)
        sys.exit(1)

    write_token(new_token)
    exp_in = resp.get("expires_in")
    exp_days = round(int(exp_in) / 86400) if exp_in else "~60"
    msg = f"Token refreshed OK. New token valid ~{exp_days} days ({mask(new_token)})."
    print(msg)
    alert("token refreshed", msg)


if __name__ == "__main__":
    main()
