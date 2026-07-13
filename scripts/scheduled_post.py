"""scheduled_post.py — calendar.json から当日エントリを投稿する自動実行スクリプト。"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CALENDAR_PATH = ROOT / "content" / "calendar.json"
LOG_PATH = ROOT / "data" / "post_log.txt"
ALERTS_LOG = ROOT / "data" / "alerts.log"
POSTER = ROOT / "scripts" / "post_to_instagram.py"

JST = timezone(timedelta(hours=9))


def log(msg: str, also_print: bool = True) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S JST")
    line = f"[{ts}] {msg}"
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    if also_print:
        print(line)


def notify(title: str, message: str) -> None:
    """macOS通知 + data/alerts.log。人が気づくべき失敗イベント用。"""
    ALERTS_LOG.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S JST")
    with ALERTS_LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {title} - {message}\n")
    try:
        safe_msg = message.replace('"', "'")[:200]
        safe_title = title.replace('"', "'")
        subprocess.run(
            ["osascript", "-e",
             f'display notification "{safe_msg}" with title "KEEPIX: {safe_title}"'],
            check=False, capture_output=True,
        )
    except Exception:
        pass


def load_calendar() -> dict:
    return json.loads(CALENDAR_PATH.read_text(encoding="utf-8"))


def save_calendar(cal: dict) -> None:
    CALENDAR_PATH.write_text(json.dumps(cal, ensure_ascii=False, indent=2), encoding="utf-8")


def mark_posted(post_id: str, ig_media_id: str) -> None:
    cal = load_calendar()
    for entry in cal.get("posts", []):
        if entry["id"] == post_id:
            entry["status"] = "posted"
            entry["posted_at"] = datetime.now(JST).strftime("%Y-%m-%dT%H:%M:%S+09:00")
            entry["ig_media_id"] = ig_media_id
            break
    save_calendar(cal)


def mark_failed(post_id: str, reason: str) -> None:
    cal = load_calendar()
    for entry in cal.get("posts", []):
        if entry["id"] == post_id:
            entry["status"] = "failed"
            entry["failed_at"] = datetime.now(JST).strftime("%Y-%m-%dT%H:%M:%S+09:00")
            entry["fail_reason"] = reason
            break
    save_calendar(cal)


def find_due_entries(window_minutes: int = 60) -> list[dict]:
    cal = load_calendar()
    now = datetime.now(JST)
    due = []
    for entry in cal.get("posts", []):
        if entry.get("status") != "scheduled":
            continue
        try:
            scheduled = datetime.fromisoformat(entry["scheduled_at"])
        except (KeyError, ValueError):
            continue
        if abs((now - scheduled).total_seconds()) <= window_minutes * 60:
            due.append(entry)
    return due


def extract_media_id(output: str) -> str | None:
    for line in output.splitlines():
        if "published media id" in line.lower():
            parts = line.strip().split()
            return parts[-1] if parts else None
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description="Post scheduled KEEPIX entries from calendar.json")
    ap.add_argument("--dry-run", action="store_true", help="Show what would be posted without calling the API")
    ap.add_argument("--window", type=int, default=60, help="Window in minutes around scheduled_at (default: 60)")
    args = ap.parse_args()

    log("=" * 60)
    log(f"scheduled_post.py 起動 (dry_run={args.dry_run}, window=±{args.window}min)")

    due = find_due_entries(args.window)
    if not due:
        log("投稿対象エントリなし — 終了")
        return

    log(f"{len(due)} 件の投稿対象を検出")

    for entry in due:
        post_id = entry["id"]
        log(f"  → {post_id} (scheduled_at={entry['scheduled_at']})")
        cmd = [sys.executable, str(POSTER), "--from-calendar", post_id]
        if args.dry_run:
            cmd.append("--dry-run")
        log(f"実行: {' '.join(cmd)}")

        if args.dry_run:
            result = subprocess.run(cmd, capture_output=False, text=True)
            log(f"[dry-run] 終了コード: {result.returncode}")
            continue

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
        except Exception as e:
            log(f"❌ 投稿失敗: {post_id} → 実行エラー: {e}")
            mark_failed(post_id, f"subprocess error: {e}")
            notify("投稿失敗", f"{post_id}: 実行エラー {e}")
            continue

        combined = result.stdout + result.stderr
        for line in combined.splitlines():
            log(f"  | {line}", also_print=True)

        if result.returncode == 0:
            media_id = extract_media_id(result.stdout) or "unknown"
            log(f"✅ 投稿成功: {post_id} → ig_media_id={media_id}")
            mark_posted(post_id, media_id)
        else:
            reason = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "unknown error"
            log(f"❌ 投稿失敗: {post_id} → {reason}")
            mark_failed(post_id, reason)
            notify("投稿失敗", f"{post_id}: {reason}")

    log("scheduled_post.py 完了")
    log("=" * 60)


if __name__ == "__main__":
    main()
