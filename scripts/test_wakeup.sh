#!/usr/bin/env bash
# test_wakeup.sh — caffeinate の動作確認スクリプト
#
# 使い方:
#   bash scripts/test_wakeup.sh           # デフォルト: 60秒間テスト
#   bash scripts/test_wakeup.sh 120       # 引数で秒数を指定
#
# caffeinate が実行中の間:
#   - ディスプレイスリープ防止 (-d)
#   - アイドルスリープ防止 (-i)
#   - システムスリープ防止 (-s)
#   - ユーザーアイドル防止 (-u)
#
# Ctrl+C で即時停止

DURATION=${1:-60}
LOG_DIR="$(cd "$(dirname "$0")/.." && pwd)/data"
LOG="$LOG_DIR/caffeinate-test.log"

mkdir -p "$LOG_DIR"

echo "=============================="
echo " KEEPIX caffeinate テスト起動"
echo "=============================="
echo "  期間  : ${DURATION}秒"
echo "  ログ  : $LOG"
echo "  停止  : Ctrl+C"
echo "------------------------------"

START=$(date '+%Y-%m-%d %H:%M:%S')
echo "[${START}] caffeinate 開始 (${DURATION}s)" | tee -a "$LOG"

/usr/bin/caffeinate -dimsu -t "$DURATION" &
CAFE_PID=$!

echo "  caffeinate PID: $CAFE_PID"
echo "  pmset -g assertions で状態確認できます"
echo ""

# 1秒ごとにカウントダウン表示
for ((i=DURATION; i>0; i--)); do
    printf "\r  残り %3ds ..." "$i"
    sleep 1
    # caffeinate が終わっていたら抜ける
    kill -0 "$CAFE_PID" 2>/dev/null || break
done

echo ""
END=$(date '+%Y-%m-%d %H:%M:%S')
echo "[${END}] caffeinate 終了" | tee -a "$LOG"
echo "=============================="
echo " テスト完了"
echo "=============================="
