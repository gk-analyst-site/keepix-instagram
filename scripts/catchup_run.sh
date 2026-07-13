#!/bin/bash
# catchup_run.sh — wrapper invoked by com.keepix.instagram.catchup.plist
# Runs scheduled_post.py once. After the target date, self-unloads the plist.
set -e

TARGET_DATE="2026-05-18"
TODAY=$(/bin/date "+%Y-%m-%d")
PLIST="$HOME/Library/LaunchAgents/com.keepix.instagram.catchup.plist"

if [ "$TODAY" != "$TARGET_DATE" ]; then
    # Past the catch-up day — cleanup self
    /bin/launchctl unload "$PLIST" 2>/dev/null || true
    /bin/rm -f "$PLIST"
    /bin/echo "$(date) catchup plist past target date — unloaded self"
    exit 0
fi

# Keep the Mac awake just for this short job (60s)
/usr/bin/caffeinate -dimsu -t 60 &
CAFF_PID=$!

cd /Users/user/Desktop/keepix-instagram
/usr/bin/python3 scripts/scheduled_post.py --window 60

# Caffeinate process auto-expires after 60s; kill it early to be clean
/bin/kill "$CAFF_PID" 2>/dev/null || true
