# KEEPIX Instagram Automation — 別Macへの移行手順

両方とも macOS の場合、約10〜15分で完了します。自動化スクリプト2本付き。

---

## 前提
- 旧Mac / 新Mac とも macOS
- Python 3.9+ が両方にインストール済（新Mac側になければ別途インストール）
- 新Macで `~/Desktop` に書き込める権限

---

## 旧Macで（パック）

```bash
cd ~/Desktop/keepix-instagram
bash scripts/migrate_pack.sh
```

出力: `~/Desktop/keepix-migration-<YYYYMMDD-HHMMSS>.tar.gz`（約3〜5MB）

このtar.gzに含まれるもの:
- プロジェクト一式 (`content/`, `scripts/`, `config/` 含む `.env` も同梱)
- `~/Library/LaunchAgents/com.keepix.instagram.{post,wakeup}.plist`
- `source_info.txt`（元の `$HOME` 情報、パス書き換え用）

含まれないもの: `__pycache__/`, `*.pyc`, `.DS_Store`

---

## tar.gz を新Macに転送

AirDrop / USB / `scp` / クラウドストレージなど好みで。**.env を含むので公開チャネルは避ける**。

---

## 新Macで（インストール）

```bash
# 1) 展開（~/Desktop に展開する想定）
tar -xzf ~/Desktop/keepix-migration-<YYYYMMDD-HHMMSS>.tar.gz -C ~/Desktop

# 2) インストール
bash ~/Desktop/keepix-migration-<YYYYMMDD-HHMMSS>/project/scripts/migrate_install.sh
```

`migrate_install.sh` が自動で:
- 既存の `~/Desktop/keepix-instagram` があればバックアップ
- `~/Desktop/keepix-instagram` にプロジェクトをコピー
- `pip install --user -r requirements.txt` で Python 依存をインストール (+ `resvg_py`, `cloudinary`)
- plist 内のパスを `旧$HOME → 新$HOME` に sed で書き換え
- `~/Library/LaunchAgents/` に配置
- `plutil -lint` で構文検証
- `launchctl load` で2本のジョブをロード
- `token_refresh.py` でMetaトークンの生存確認

---

## 動作確認チェックリスト

新Macで以下を実行:

```bash
cd ~/Desktop/keepix-instagram

# トークン有効？
python3 scripts/token_refresh.py
# → "Token expires: ... days left" と valid=True が出れば OK

# 翌日エントリが拾えるか
python3 scripts/scheduled_post.py --dry-run --window 1440
# → 翌日の scheduled エントリが表示されればOK

# launchdジョブが登録されているか
launchctl list | grep keepix
# → com.keepix.instagram.post / com.keepix.instagram.wakeup の2行

# 最近の運用ログ
tail -10 data/post_log.txt
```

---

## 旧Macの後始末（移行確認後）

新Macで正常に動作確認できたら、旧Macで以下を実行して二重投稿を防ぐ:

```bash
launchctl unload ~/Library/LaunchAgents/com.keepix.instagram.post.plist
launchctl unload ~/Library/LaunchAgents/com.keepix.instagram.wakeup.plist
# plist自体は残しても無害（unloadすれば発火しない）。完全削除なら:
# rm ~/Library/LaunchAgents/com.keepix.instagram.{post,wakeup}.plist
```

**注意**: 旧Macで `launchctl unload` する前に新Macで動作確認すること。先に旧を止めると、その日の22:00投稿がどちらでも走らない可能性。

---

## トラブルシューティング

### `pip install` が失敗
- `python3 -m pip install --user --upgrade pip` してから再試行
- 新Macで Python 3.9+ がない場合は Homebrew で `brew install python@3.11`

### `launchctl load` でエラー
- `plutil -lint <plist>` で構文確認
- plist のパスが `/Users/<旧ユーザー名>/...` のまま残っていないか確認（sedの書き換えミス）

### Macスリープ問題
- 旧Macでは `pmset schedule wake` で起床予約していた経緯あり（特殊な催し日のみ）
- 通常運用なら 21:50 の caffeinate ジョブで十分

### Cloudinary / Meta / Anthropic の認証
- 全部クラウド側の状態を共有。新Macに同じ `.env` を持っていけば動く
- ただし新Macで初回 `requests` が走るときに macOS が「ネットワーク許可」ダイアログを出す場合あり

---

## 重要な制約

- **Macが22:00 JST前後に起動していること**が必須（launchdベース）。スリープから自動起床はOSの設定次第
- 24時間止まらない運用が必要なら、後でVPS/GitHub Actions等に移行する選択肢あり（その時はまた相談を）
