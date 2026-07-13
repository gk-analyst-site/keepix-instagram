# Setup Checklist

KEEPIX Instagram自動化環境のセットアップ手順。順番にチェック。

## 1. Meta / Instagram 準備

- [ ] Facebookページを作成（KEEPIXブランド用）
- [ ] Instagramアカウントを**プロアカウント（ビジネス）**に切替
- [ ] Instagramアカウントを上記FacebookページにリンクIGアカウント → 設定 → リンク済みアカウント
- [ ] [Meta for Developers](https://developers.facebook.com/) でアプリ作成（本プロジェクトは App ID `934052956169952`）
- [ ] アプリに **Instagram Graph API** / **Facebook Login** のプロダクトを追加
- [ ] アプリレビュー or Dev Mode で以下の権限を付与:
  - `instagram_basic`
  - `instagram_content_publish`
  - `instagram_manage_comments`
  - `instagram_manage_insights`
  - `pages_show_list`
  - `pages_read_engagement`

## 2. シークレット取得

- [ ] **App Secret**: アプリ設定 → ベーシック → app secret を表示
- [ ] **Short-lived User Token**: Graph API Explorer で上記スコープを選んで生成
- [ ] **Long-lived Token への変換**:
  ```bash
  curl "https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=SHORT_TOKEN"
  ```
- [ ] **Facebook Page ID**: `GET /me/accounts` で取得
- [ ] **Instagram Business Account ID**: `GET /{page-id}?fields=instagram_business_account`
- [ ] **Anthropic API Key**: https://console.anthropic.com/ で取得

## 3. `.env` に書き込み

- [ ] `config/.env.example` を `config/.env` にコピー
- [ ] 以下を埋める:
  - `META_APP_ID=934052956169952`
  - `META_APP_SECRET=`
  - `META_ACCESS_TOKEN=`（long-lived）
  - `INSTAGRAM_BUSINESS_ACCOUNT_ID=`
  - `FACEBOOK_PAGE_ID=`
  - `ANTHROPIC_API_KEY=`

## 4. Python環境

- [ ] Python 3.10+ がインストール済み
- [ ] 仮想環境を作成: `python3 -m venv venv && source venv/bin/activate`
- [ ] 依存関係: `pip install -r requirements.txt`

## 5. 動作確認

- [ ] `python scripts/token_refresh.py` → トークン残存日数とIG Business Account IDが表示される
- [ ] `python scripts/get_insights.py` → アカウントのフォロワー数などが取得できる
- [ ] `python scripts/fetch_comments.py` → 最新投稿にコメントが無ければ空配列が返る

## 6. 初回投稿テスト

- [ ] `content/posts/` にテスト画像（**公開URL**でもOK）を用意
- [ ] `content/calendar.json` にエントリを追加
- [ ] `python scripts/post_to_instagram.py --dry-run` で内容確認
- [ ] 本番送信

## 7. 自動配信パイプライン

```
[content-creator] → captions/*.md  ┐
                                    ├→ calendar.json (status: scheduled)
[upload_to_cloudinary] → image_urls ┘                │
                                                     ▼
                       launchd 21:50 JST → caffeinate (sleep防止 20分)
                       launchd 22:00 JST → scheduled_post.py
                                                     │
                                                     ▼
                                        post_to_instagram.py --from-calendar
                                                     │
                                                     ▼
                                      Graph API: container → publish
                                                     │
                                                     ▼
                                  calendar.json (status: posted + ig_media_id)
```

### 投稿フロー（1日分）

1. **キャプション生成**: `python3 scripts/draft_post.py --type Value --topic "..." --save <date>-<slug>.md`
2. **calendar.json に追加**: `status: "scheduled"`, `image_urls: []`
3. **画像準備**: `scripts/upload_to_cloudinary.py` で Cloudinary に upload → URLを `image_urls` に書き込み
4. **dry-run確認**: `python3 scripts/post_to_instagram.py --from-calendar <id> --dry-run`
5. **当日 22:00 JST**: launchd → scheduled_post.py が ±60分の window 内エントリを自動投稿
6. **結果記録**: calendar.json が `status: "posted"` + `ig_media_id` で更新

### launchd ジョブ

| Label | 実行時刻 | 役割 |
|---|---|---|
| `com.keepix.instagram.wakeup` | 21:50 JST | caffeinate でMacのスリープを20分間防止 |
| `com.keepix.instagram.post` | 22:00 JST | scheduled_post.py を実行 |

確認: `launchctl list \| grep keepix`
再ロード: `launchctl unload ~/Library/LaunchAgents/com.keepix.instagram.post.plist && launchctl load ~/Library/LaunchAgents/com.keepix.instagram.post.plist`

### キャプションのフォーマット

```
TYPE: <Product|Story|Value|Engage>
HOOK (first line of caption): <one-liner>

CAPTION:
<本文>

CTA: <one line>

HASHTAGS: <space-separated>

IMAGE BRIEF: <内部用、IGには送信されない>

ALT TEXT: <内部用>
```

`HOOK + CAPTION + CTA + HASHTAGS` のみがIGに送信される。`IMAGE BRIEF` と `ALT TEXT` はデザイン・アクセシビリティの社内メモ。

### ステータス遷移

`draft` → `scheduled` → `posted`  /  `failed` (`failed_at`, `fail_reason` も記録)

`scheduled` のままで `image_urls` が空のまま22:00を迎えると、その日は投稿スキップ（エラー）→ 翌日以降は ±60分 window 外になり恒久的に未投稿。手動で `image_urls` 入れて当夜中に手動投稿するか、`scheduled_at` を未来日に書き換える。

## 8. 運用ルール

- [ ] 他人の投稿への自動いいね/コメントは**絶対に行わない**
- [ ] コメント返信は必ず `reply_comment.py` の承認フローを通す
- [ ] トークン失効前（残り7日）にリフレッシュ
- [ ] Metaからの警告メールは即座に確認

## トラブルシューティング

| 症状 | 対処 |
|------|------|
| `(#10) Application does not have permission` | アプリレビューで権限再申請、または開発モードにテスターを追加 |
| `Invalid OAuth access token` | `token_refresh.py` で状況確認、必要なら再発行 |
| `Media container is not ready` | publish前に数秒待つ。`post_to_instagram.py` は内部でポーリング済み |
| キャプションが切れる | IGの上限は2,200文字。ハッシュタグは最大30個 |
