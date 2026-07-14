"""One-time: obtain a NON-EXPIRING Page access token and store it in config/.env."""
from __future__ import annotations

import datetime as dt
import re
import sys

from _common import (
    ACCESS_TOKEN,
    APP_ID,
    APP_SECRET,
    ENV_PATH,
    PAGE_ID,
    graph_get,
    require,
)


def mask(token: str) -> str:
    return f"{token[:6]}...{token[-4:]}" if len(token) > 12 else "****"


def debug_token(tok: str) -> dict:
    app_token = f"{APP_ID}|{APP_SECRET}"
    return graph_get("/debug_token", {"input_token": tok, "access_token": app_token}).get("data", {})


def get_page_token() -> tuple[str | None, str | None]:
    resp = graph_get("/me/accounts", {"fields": "id,name,access_token"})
    for p in resp.get("data", []):
        if p.get("id") == PAGE_ID:
            return p.get("access_token"), p.get("name")
    return None, None


def write_token(new_token: str) -> None:
    text = ENV_PATH.read_text(encoding="utf-8")
    (ENV_PATH.parent / ".env.bak").write_text(text, encoding="utf-8")
    if re.search(r"(?m)^META_ACCESS_TOKEN=", text):
        text = re.sub(r"(?m)^META_ACCESS_TOKEN=.*$", f"META_ACCESS_TOKEN={new_token}", text)
    else:
        text = text.rstrip("\n") + f"\nMETA_ACCESS_TOKEN={new_token}\n"
    ENV_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    require("META_ACCESS_TOKEN", ACCESS_TOKEN)
    require("META_APP_ID", APP_ID)
    require("META_APP_SECRET", APP_SECRET)
    require("FACEBOOK_PAGE_ID", PAGE_ID)

    tok, name = get_page_token()
    if not tok:
        print(f"[error] no page access_token returned for PAGE_ID={PAGE_ID}.", file=sys.stderr)
        print("        Is the Page linked and the token granted pages_show_list / content perms?", file=sys.stderr)
        sys.exit(1)

    info = debug_token(tok)
    exp = info.get("expires_at")
    never = exp in (0, None)
    print(f"Page name : {name}")
    print(f"Token type: {info.get('type')}")
    print(f"Valid     : {info.get('is_valid')}")
    if never:
        print("Expires   : NEVER (permanent)")
    else:
        print(f"Expires   : {dt.datetime.fromtimestamp(exp, tz=dt.timezone.utc).isoformat()}")
    print(f"Scopes    : {', '.join(info.get('scopes', []))}")
    print(f"New token : {mask(tok)}")

    if not info.get("is_valid"):
        print("[error] page token reported invalid - aborting, .env left unchanged.", file=sys.stderr)
        sys.exit(1)

    write_token(tok)
    if never:
        print("\nStored a NON-EXPIRING page token in config/.env. No more token refresh needed.")
    else:
        print("\nStored the page token, but it still shows an expiry.")
        print("That usually means the source user token was not long-lived. Tell your assistant this output.")


if __name__ == "__main__":
    main()
