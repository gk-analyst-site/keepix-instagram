#!/bin/bash
# migrate_pack.sh — bundle this Mac's KEEPIX automation into a single .tar.gz
# Run this on the OLD Mac. Output: ~/Desktop/keepix-migration-<timestamp>.tar.gz
set -euo pipefail

PROJECT="$HOME/Desktop/keepix-instagram"
LAUNCHD_DIR="$HOME/Library/LaunchAgents"
TS=$(date +%Y%m%d-%H%M%S)
STAGE="$(mktemp -d)/keepix-migration-$TS"
OUT="$HOME/Desktop/keepix-migration-$TS.tar.gz"

if [ ! -d "$PROJECT" ]; then
    echo "ERROR: $PROJECT not found" >&2
    exit 1
fi

mkdir -p "$STAGE/project" "$STAGE/launchd"
echo "→ copying project (excluding __pycache__, .DS_Store)"
rsync -a \
    --exclude='__pycache__' \
    --exclude='.DS_Store' \
    --exclude='*.pyc' \
    "$PROJECT/" "$STAGE/project/"

echo "→ copying launchd plists"
for f in com.keepix.instagram.post.plist com.keepix.instagram.wakeup.plist; do
    if [ -f "$LAUNCHD_DIR/$f" ]; then
        cp "$LAUNCHD_DIR/$f" "$STAGE/launchd/$f"
    else
        echo "  [warn] $f not found, skipping"
    fi
done

# Record source paths so the install script can rewrite them
cat > "$STAGE/source_info.txt" <<EOF
SOURCE_HOME=$HOME
SOURCE_USER=$(whoami)
SOURCE_PROJECT=$PROJECT
TIMESTAMP=$TS
EOF

echo "→ packing -> $OUT"
tar -czf "$OUT" -C "$(dirname "$STAGE")" "$(basename "$STAGE")"
rm -rf "$STAGE"

SIZE=$(du -h "$OUT" | cut -f1)
echo ""
echo "✅ DONE — archive: $OUT ($SIZE)"
echo ""
echo "Next steps:"
echo "  1) Copy this .tar.gz to the new Mac (AirDrop, USB, scp, etc.)"
echo "  2) On the new Mac, extract and run scripts/migrate_install.sh from the extracted directory"
