#!/bin/bash
# migrate_install.sh — install KEEPIX automation on the NEW Mac
# Run this AFTER extracting the migration tar.gz, from inside the extracted dir.
# Usage:
#   tar -xzf ~/Desktop/keepix-migration-<ts>.tar.gz -C ~/Desktop
#   cd ~/Desktop/keepix-migration-<ts>
#   bash project/scripts/migrate_install.sh
set -euo pipefail

# Find the migration root (this script lives in <root>/project/scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MIG_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

DEST_PROJECT="$HOME/Desktop/keepix-instagram"
DEST_LAUNCHD="$HOME/Library/LaunchAgents"

if [ ! -f "$MIG_ROOT/source_info.txt" ]; then
    echo "ERROR: source_info.txt not found. Run from extracted migration dir." >&2
    exit 1
fi

# Load source info
source "$MIG_ROOT/source_info.txt"
echo "Source: user=$SOURCE_USER home=$SOURCE_HOME"
echo "Destination: user=$(whoami) home=$HOME"
echo ""

# 1) Project files
if [ -d "$DEST_PROJECT" ]; then
    BACKUP="$DEST_PROJECT.bak.$(date +%Y%m%d-%H%M%S)"
    echo "→ existing $DEST_PROJECT detected; backing up to $BACKUP"
    mv "$DEST_PROJECT" "$BACKUP"
fi
echo "→ copying project to $DEST_PROJECT"
mkdir -p "$DEST_PROJECT"
rsync -a "$MIG_ROOT/project/" "$DEST_PROJECT/"

# 2) Python deps (with broken-pip auto-repair)
echo "→ installing Python dependencies"
if ! command -v python3 >/dev/null 2>&1; then
    echo "  [warn] python3 not found. Install Python 3.9+ from https://www.python.org/downloads/ then re-run"
    echo "  after Python install: python3 -m pip install --user -r $DEST_PROJECT/requirements.txt"
elif ! python3 -m pip --version >/dev/null 2>&1; then
    echo "  [repair] pip is broken — running ensurepip"
    python3 -m ensurepip --upgrade --user || {
        echo "  [warn] ensurepip failed. Try: curl -sSL https://bootstrap.pypa.io/get-pip.py | python3 - --user"
    }
    python3 -m pip install --user -r "$DEST_PROJECT/requirements.txt" >/dev/null 2>&1 || \
        echo "  [warn] pip install still failing after repair. Check python3 version (need 3.9+)"
    python3 -m pip install --user resvg_py cloudinary >/dev/null 2>&1 || true
else
    python3 -m pip install --user -r "$DEST_PROJECT/requirements.txt" >/dev/null 2>&1 || {
        echo "  [warn] pip install failed. Try running by hand:"
        echo "    python3 -m pip install --user -r $DEST_PROJECT/requirements.txt"
    }
    python3 -m pip install --user resvg_py cloudinary >/dev/null 2>&1 || true
fi
echo "  Python: $(python3 --version 2>&1)"

# 3) launchd plists — rewrite paths and install
mkdir -p "$DEST_LAUNCHD"
for f in com.keepix.instagram.post.plist com.keepix.instagram.wakeup.plist; do
    SRC="$MIG_ROOT/launchd/$f"
    DST="$DEST_LAUNCHD/$f"
    if [ ! -f "$SRC" ]; then
        echo "  [warn] $f not in archive, skipping"
        continue
    fi
    echo "→ installing $f (rewriting paths $SOURCE_HOME → $HOME)"

    # Unload old version if loaded
    /bin/launchctl unload "$DST" 2>/dev/null || true

    # Path rewrite
    sed "s|$SOURCE_HOME|$HOME|g" "$SRC" > "$DST"

    # Validate
    if ! /usr/bin/plutil -lint "$DST" >/dev/null; then
        echo "  ERROR: $DST failed plutil lint" >&2
        exit 1
    fi

    # Load
    /bin/launchctl load "$DST"
done

echo ""
echo "→ verifying launchd jobs"
/bin/launchctl list | grep keepix || echo "  [warn] no keepix jobs registered"

echo ""
echo "→ verifying .env"
if [ -f "$DEST_PROJECT/config/.env" ]; then
    echo "  config/.env present ($(wc -l < "$DEST_PROJECT/config/.env") lines)"
else
    echo "  [ERROR] config/.env MISSING — copy it manually from the old Mac" >&2
fi

echo ""
echo "→ smoke test: token check"
cd "$DEST_PROJECT"
python3 scripts/token_refresh.py 2>&1 | grep -v NotOpenSSLWarning | grep -v "warnings.warn" | head -3 || true

echo ""
echo "✅ MIGRATION COMPLETE"
echo ""
echo "Verify in detail:"
echo "  cd ~/Desktop/keepix-instagram"
echo "  python3 scripts/token_refresh.py          # Meta token alive?"
echo "  python3 scripts/scheduled_post.py --dry-run --window 1440  # next-day dry run"
echo "  launchctl list | grep keepix              # both jobs loaded?"
echo "  tail -5 data/post_log.txt                 # last fire log"
