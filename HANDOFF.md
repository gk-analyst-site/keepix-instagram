# KEEPIX Instagram Automation — 引き継ぎ書

**作成日**: 2026-05-30 / **対象**: 次に運用を引き継ぐ人（または将来の自分）

このドキュメント1本で運用を継続できることを目標にしています。詳細仕様は
`CLAUDE.md` と `SETUP_CHECKLIST.md` を参照。

---

## 1. プロジェクト概要

- **ブランド**: KEEPIX（ゴールキーパー向けトレーニング製品）
- **IGアカウント**: `@keepix.gk_official` (Instagram Business Account ID: `17841436458021978`)
- **Facebook Page**: Keepix GK Training Builder (Page ID: `1017390374800030`)
- **ターゲット**: 海外（UK/EU/US）のGKコーチ
- **言語**: 英語（投稿本文・キャプション全て英語）
- **トーン**: プロフェッショナル&親しみやすい。**「AI」「機械学習」「アルゴリズム」等のテックワード禁止**
- **コンテンツ4タイプ**: Product / Story / Value / Engage（週次比 2:1:3:1）
- **配信頻度**: 毎日22:00 JST 1本

---

## 2. 現在のステータス（2026-05-30 時点）

### 投稿状況
| 区分 | 件数 | 範囲 |
|---|---|---|
| **posted** | 36本 | 2026-04-24 〜 2026-05-29（連続稼働中） |
| **scheduled** | 22本 | 2026-05-30 〜 2026-06-20（全件 image_urls 完備） |
| **failed** | 0本 | — |

### 認証（`config/.env`）
| 項目 | 値 / 失効日 |
|---|---|
| `META_APP_ID` | `934052956169952` |
| `META_APP_SECRET` | 設定済 |
| `META_ACCESS_TOKEN` | 60日長期トークン。**失効 2026-07-28** (残約59日) |
| `INSTAGRAM_BUSINESS_ACCOUNT_ID` | `17841436458021978` |
| `FACEBOOK_PAGE_ID` | `1017390374800030` |
| `ANTHROPIC_API_KEY` | 設定済 |
| `CLAUDE_MODEL` | `claude-sonnet-4-6` |
| `CLOUDINARY_CLOUD_NAME` | `drcsslwyg` |
| `CLOUDINARY_API_KEY` / `_SECRET` | 設定済 |

### 付与済み Meta スコープ
`pages_show_list`, `business_management`, `instagram_basic`, `instagram_manage_comments`,
`instagram_content_publish`, `instagram_manage_messages`, `pages_read_engagement`, `public_profile`

### 未取得スコープ（必要に応じてレビュー申請）
- `instagram_manage_insights` — `get_insights.py` が動かない理由
- `Instagram Public Content Access` — `hashtag_search.py` が動かない理由（Meta App Review必要）

---

## 3. アーキテクチャ（自動配信パイプライン）

```
[1] キャプション生成 (draft_post.py / _batch_captions_*)
   └→ content/captions/<id>.md
        ├─ TYPE / HOOK / CAPTION / CTA / HASHTAGS / IMAGE BRIEF / ALT TEXT
        └─ (IG送信時に組み立てるのは HOOK + CAPTION + CTA + HASHTAGS のみ)

[2] スライド画像生成 (_generate_slides_generic.py 等)
   └→ content/posts/<id>/slide-1.png

[3] Cloudinary upload (upload_to_cloudinary.py / _publish_batch_*)
   └→ https://res.cloudinary.com/drcsslwyg/...png

[4] calendar.json に entry 登録 (status="scheduled", image_urls=[url])

[5] launchd 21:50 JST → caffeinate (Macスリープ防止 20分)
[6] launchd 22:00 JST → scheduled_post.py
   └→ status=scheduled かつ scheduled_at が ±60min の entry を抽出
   └→ post_to_instagram.py --from-calendar <id> を subprocess 実行
        ├─ Caption ファイル parse → IG向け本文組み立て
        ├─ 単一画像 or carousel(複数) を判別
        ├─ Graph API: /media (container作成) → status polling → /media_publish
        └─ stdout に "published media id = <ig_media_id>" を出力

[7] scheduled_post.py が ig_media_id を抜き出し calendar.json を更新
   └→ status="posted", posted_at, ig_media_id を記録
```

### ステータス遷移
`draft` → `scheduled` → `posted` / `failed`（recovery後は `posted` + `recovered_reason`）

---

## 4. ディレクトリ構成

```
keepix-instagram/
├── CLAUDE.md                  # プロジェクト原則・ガイドライン
├── SETUP_CHECKLIST.md         # セットアップ手順
├── HANDOFF.md                 # ← この文書
├── PROMPTS.md                 # 過去に使った投稿生成プロンプト集
├── requirements.txt           # requests, python-dotenv, anthropic, cloudinary
├── agents/                    # Claudeエージェント定義 (system prompt)
│   ├── content-creator.md     # 投稿生成用 ← draft_post.py が読み込む
│   ├── comment-responder.md   # コメント返信案生成用
│   ├── scheduler.md           # 配信スケジューラ
│   ├── target-finder.md       # 見込み客発掘
│   └── analytics.md           # KPIブリーフ
├── config/
│   ├── .env                   # シークレット（gitignore対象）
│   └── .env.example
├── content/
│   ├── calendar.json          # 投稿マスタ。58 entries (posted 36 + scheduled 22)
│   ├── captions/              # <id>.md 形式の構造化キャプション
│   └── posts/                 # <id>/ ディレクトリに slide-*.png
├── data/
│   ├── post_log.txt           # scheduled_post.py の運用ログ
│   ├── publish.log            # post_to_instagram.py の構造化ログ
│   ├── launchd-stdout/err.log # launchd標準出力
│   └── caffeinate.log         # wakeup ジョブログ
├── docs/                      # 補助ドキュメント
└── scripts/                   # 全23ファイル
```

---

## 5. スクリプト一覧

### コア（毎日触る/触る可能性）
| ファイル | 役割 |
|---|---|
| `_common.py` | 環境変数読込・Graph API ラッパー・**caption parser**・logger |
| `scheduled_post.py` | launchd経由で毎日22:00に起動。calendar走査→投稿→結果記録 |
| `post_to_instagram.py` | 単発投稿。`--from-calendar <id>` で calendar entry を使用、`--dry-run` 対応。**carousel対応** |
| `token_refresh.py` | トークン状態確認＋長期化（短期→長期は `--exchange`） |
| `draft_post.py` | キャプション1本生成。`--type Value --topic "..." --save <file>.md` |

### キャプション生成（バッチ）
| ファイル | 役割 |
|---|---|
| `_batch_captions_may29_jun20.py` | 23本並列生成（5/29〜6/20分）。**ID/topicを書き換えれば次サイクルにも流用可** |

### スライド画像生成
| ファイル | 役割 |
|---|---|
| `_generate_slides_generic.py` | **汎用** v1：caption の HOOK + TYPE から自動レイアウトしてPNG出力（テキストオンリー、ダーク緑＋ミント） |
| `_generate_slides_v2_goal.py` | v2案（ゴール枠＋ボールモチーフ）。**ユーザー確認待ち。bulk未適用** |
| `_generate_catchup_slides.py` | 個別ハンドコード版（5/15-5/28 のキャッチアップ用） |
| `generate_value_post.py` / `generate_week_posts*.py` | 過去の手書きSVG生成スクリプト（参考） |

### Cloudinary
| ファイル | 役割 |
|---|---|
| `upload_to_cloudinary.py` | 単発upload（CLI: ファイルパスを渡す） |
| `_publish_batch_may29_jun20.py` | upload + calendar.json 登録を一括 |
| `_upload_week*.py` | 過去のweek単位upload（参考） |

### コメント/インサイト/検索
| ファイル | 役割 |
|---|---|
| `fetch_comments.py` | 自分の投稿のコメント取得 |
| `reply_comment.py` | Claude APIで返信案生成→**人間承認→送信** の3ステップ。**無承認自動返信は禁止** |
| `get_insights.py` | アカウント/投稿インサイト。**現状 `instagram_manage_insights` 未付与で401** |
| `hashtag_search.py` | ハッシュタグから見込み客発見。**Meta App Review 未承認で401** |

---

## 6. launchd ジョブ

`~/Library/LaunchAgents/` に2本登録、両方とも有効:

| Label | 時刻 | 役割 |
|---|---|---|
| `com.keepix.instagram.wakeup` | 毎日21:50 JST | `caffeinate -dimsu -t 4800`（80分スリープ防止、23:10まで） |
| `com.keepix.instagram.post` | 毎日22:00 / 22:30 / 23:00 JST | `scheduled_post.py` 実行。22:00空振り対策の **backup retry** 2回付き。`scheduled_post.py` は status=scheduled のみ拾うので二重投稿しない |

確認: `launchctl list | grep keepix`
再ロード（plist編集時）: `launchctl unload <path> && launchctl load <path>`

### 過去の一時ジョブ（既に削除済）
- `com.keepix.instagram.catchup`: 5/18 のキャッチアップ用、self-cleanup wrapper付き
- `com.keepix.instagram.autopost`: 重複登録したが scheduled_post.py と統合して削除

---

## 7. キャプションファイルのフォーマット

```
TYPE: <Product|Story|Value|Engage>
HOOK (first line of caption): <1行>

CAPTION:
<本文>

CTA: <1行>

HASHTAGS: <スペース区切り、20-28個>

IMAGE BRIEF:
<デザイン指示。IGには送信されない内部メモ>

ALT TEXT: <アクセシビリティ用、IGには送信されない>
```

`post_to_instagram.py` が IG に送るのは **HOOK + CAPTION + CTA + HASHTAGS** のみ
（IMAGE BRIEF と ALT TEXT は社内/デザイン用）。
パーサーは `_common.py` の `parse_caption_file()` / `assemble_ig_caption()`。

---

## 8. 日次運用フロー

### 通常日（投稿予約 + 画像準備済の場合）
1. 21:50 JST: `wakeup` 発火 → caffeinate 20分
2. 22:00 JST: `post` 発火 → `scheduled_post.py`
3. 22:00:30〜22:01:30 頃: container作成→polling→publish
4. `data/post_log.txt` に成功ログ、calendar.json に `status=posted`

### 必要なときに手で実行
| やりたいこと | コマンド |
|---|---|
| 今すぐ何かをdry-run | `python3 scripts/post_to_instagram.py --from-calendar <id> --dry-run` |
| 今すぐ手動投稿（リカバリ） | `python3 scripts/post_to_instagram.py --from-calendar <id>`（calendar更新は手動、後述） |
| トークン残日数確認 | `python3 scripts/token_refresh.py` |
| コメント取得 | `python3 scripts/fetch_comments.py` |
| コメント返信案 | `python3 scripts/reply_comment.py --comment <id> --context "..."` |

### 手動投稿後の calendar.json 更新（コピペ用）
```python
import json, datetime as dt
from pathlib import Path
JST = dt.timezone(dt.timedelta(hours=9))
now = dt.datetime.now(JST).strftime("%Y-%m-%dT%H:%M:%S+09:00")
cal = json.loads(Path('content/calendar.json').read_text())
for p in cal['posts']:
    if p['id'] == '<POST_ID>':
        p['status'] = 'posted'
        p['posted_at'] = now
        p['ig_media_id'] = '<IG_MEDIA_ID>'
        p['recovered_reason'] = '<理由>'
Path('content/calendar.json').write_text(json.dumps(cal, indent=2, ensure_ascii=False) + '\n')
```

---

## 9. 次サイクル準備（6/21 以降 を作る手順）

23本を一気に作る手順を再現可能にしてあります:

1. **トピック設計**: `_batch_captions_may29_jun20.py` を `_batch_captions_jun21_jul13.py` などにコピーし、`PLAN` 配列の id / type / topic を入れ替え。比率 Product 2 / Story 1 / Value 3 / Engage 1 を守る
2. **Caption生成**: `python3 scripts/_batch_captions_jun21_jul13.py` → 23本のmdが生成される
3. **画像生成**: `python3 scripts/_generate_slides_generic.py <id> <id> ...` で23本のpng（汎用版、テキストオンリー）
   - **将来 v2（ゴール枠+ボール）の方向で正式化したら**: `_generate_slides_v2_goal.py` を使う
4. **Cloudinary upload + calendar登録**: `_publish_batch_may29_jun20.py` のPLAN配列を編集して実行
5. **検証**: 任意の1本で `python3 scripts/post_to_instagram.py --from-calendar <id> --dry-run`
6. 後は毎日22:00に自動投稿される

トークンは毎月Graph API Explorerで短期トークンを発行 → `_common.py` の交換ロジックを通すか、 `token_refresh.py --exchange` を実行（手順は §10 参照）。

---

## 10. トークン更新（**60日に1回必須**）

長期トークンは60日で失効。**長期→長期の再交換では延長されない**ので、必ず短期トークンを起点にする:

1. [Graph API Explorer](https://developers.facebook.com/tools/explorer/) を開く
2. アプリ「KEEPIX」(934052956169952) を選択
3. 以下スコープを付与:
   - `instagram_basic` / `instagram_content_publish` / `instagram_manage_comments`
   - `pages_show_list` / `pages_read_engagement` / `business_management`
4. **Generate Access Token** をクリック（短期トークン、1〜2時間有効）
5. ターミナルで:
   ```bash
   cd ~/Desktop/keepix-instagram
   # .envの META_ACCESS_TOKEN を短期トークンに一時的に書き換える
   python3 scripts/token_refresh.py --exchange
   # 表示された access_token を .env の META_ACCESS_TOKEN に確定
   python3 scripts/token_refresh.py  # 残日数確認（59日になるはず）
   ```
6. 次回更新は **2026-07-21 頃**（失効7日前）が目安

---

## 11. 既知の制限・未対応事項

| 項目 | 内容 | 対応案 |
|---|---|---|
| 5/29 の投稿が22:00ジョブで取得できず | scheduled_post.py が「対象なし」を返した。原因未特定（スリープ復帰タイミング or 競合の可能性） | **対応済**: post.plist を 22:00/22:30/23:00 の3回発火に拡張。wakeup も80分に延長して全カバー |
| `get_insights.py` が401 | `instagram_manage_insights` スコープ未付与 | App Review で申請 |
| `hashtag_search.py` が401 | `Instagram Public Content Access` 未承認 | App Review で申請 |
| resvg_py が絵文字を描画できない | 👇 等が `?` ボックスになる | スライドの footer はテキストオンリーに（v2では修正済） |
| Python 3.9 環境 | `dict \| None` 等の3.10+構文を使うため、全スクリプトに `from __future__ import annotations` を付与済 | 3.10+ にアップグレード or 現状維持 |
| シェル `ANTHROPIC_API_KEY=` (空) が `.env` を上書き | `load_dotenv(ENV_PATH, override=True)` で対策済 | — |

---

## 12. 未決事項（次セッションで決めるべきこと）

1. **スライドデザイン v2 の採用可否**: ゴール枠+ボールモチーフのサンプルは生成済（5/31, 6/3, 6/4, 6/8 の `slide-1-v2.png`）。採用なら `_generate_slides_v2_goal.py` で 5/30〜6/20 を再生成 → 上書きupload → calendar の image_urls 差し替え
2. ~~**22:00ジョブのバックアップ retry**~~ → **対応済** (post.plist が 22:00/22:30/23:00 で発火)
3. **次の23本（6/21〜7/13）の準備時期**: 6/14 頃に手をつける想定

---

## 13. 緊急時の対処

### 「投稿が出ていない」
1. `tail -30 data/post_log.txt` で直近ログ確認
2. `python3 -c "import json,pathlib; print([p for p in json.loads(pathlib.Path('content/calendar.json').read_text())['posts'] if p['id']=='<id>'])"` で entry 確認
3. status が `failed` なら image_urls / caption の整合確認後、`post_to_instagram.py --from-calendar <id>` で再投稿
4. 手動投稿後は §8 の calendar 更新スニペットで status を `posted` に

### 「トークンが切れた」
1. `python3 scripts/token_refresh.py` で確認（valid=False ならNG）
2. §10 の手順で再発行

### 「画像が間違っていた」
- `content/posts/<id>/slide-1.png` を差し替え → `python3 scripts/upload_to_cloudinary.py --folder keepix-instagram/<slug> content/posts/<id>/slide-1.png` で上書きupload
- calendar の `image_urls` URL は v番号付きなので、再upload後の新URLに差し替えが必要

### 「キャプションを直したい（投稿前）」
- `content/captions/<id>.md` を直接編集 → 22:00で自動反映
- 投稿済の場合はIG側で直接編集（Graph APIでも可能だが運用上は手動）

---

## 14. 連絡先・参考リンク

- Meta for Developers: https://developers.facebook.com/
- Graph API Explorer: https://developers.facebook.com/tools/explorer/
- Anthropic Console: https://console.anthropic.com/
- Cloudinary Console: https://console.cloudinary.com/
- KEEPIX IG: https://www.instagram.com/keepix.gk_official/

---

**EOF** — この文書はリポジトリのルートに `HANDOFF.md` として保存されています。
更新が必要になったら、次セッションで書き換えてください。
