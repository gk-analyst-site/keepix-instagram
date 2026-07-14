"""Re-date all still-unposted (status=="scheduled") calendar entries to
consecutive future days at 22:00 JST, starting START_DATE, in chronological order.
A backup is written to content/calendar.json.bak before saving."""
from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAL = ROOT / "content" / "calendar.json"

START_DATE = date(2026, 7, 14)
POST_TIME = "T22:00:00+09:00"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Write changes (otherwise preview only)")
    ap.add_argument("--start", default=START_DATE.isoformat(), help="First date YYYY-MM-DD (default 2026-07-14)")
    args = ap.parse_args()

    start = date.fromisoformat(args.start)
    cal = json.loads(CAL.read_text(encoding="utf-8"))

    todo = [p for p in cal["posts"] if p.get("status") == "scheduled"]
    todo.sort(key=lambda p: p.get("scheduled_at", ""))

    if not todo:
        print("再予約対象（status=scheduled）はありません。")
        return

    print(f"{len(todo)} 件を {start.isoformat()} から日割りに再予約します:\n")
    for i, p in enumerate(todo):
        new_date = (start + timedelta(days=i)).isoformat()
        print(f"  {p.get('scheduled_at','?')[:10]}  ->  {new_date}   {p['id']}")
        p["scheduled_at"] = f"{new_date}{POST_TIME}"

    cal["posts"].sort(key=lambda p: p.get("scheduled_at", ""))

    if not args.apply:
        print("\n[preview] 変更は保存していません。--apply を付けると保存します。")
        return

    (CAL.parent / "calendar.json.bak").write_text(CAL.read_text(encoding="utf-8"), encoding="utf-8")
    CAL.write_text(json.dumps(cal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    last = (start + timedelta(days=len(todo) - 1)).isoformat()
    print(f"\n✅ 保存しました（バックアップ: content/calendar.json.bak）。")
    print(f"   {start.isoformat()} 〜 {last} の毎晩22時に1件ずつ自動投稿されます。")


if __name__ == "__main__":
    main()
