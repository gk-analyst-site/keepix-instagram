# KEEPIX Instagram Automation

Instagram自動化プロジェクト。KEEPIX（ゴールキーパー向けトレーニングツール）のInstagramマーケティングを運用するためのスクリプトとワークフロー群。

## プロジェクトの目的

- KEEPIXの認知拡大とEC/問い合わせへの導線作り
- 主要ターゲット: **海外のゴールキーパーコーチ**（English primary）
- 投稿・分析・コメント返信案生成までを半自動化し、最終判断は人間が行う

## ブランディングの原則

- KEEPIXは「AI」「機械学習」などの技術ワードで説明しない
- 現場の声・選手の動き・コーチング観点からメリットを伝える
- 投稿トーンはプロフェッショナル＆親しみやすい（英語ネイティブGKコーチが読む前提）

## コンテンツ4タイプ

| Type | 目的 | 例 |
|------|------|-----|
| **Product** | KEEPIX本体・使い方を見せる | プロダクト紹介動画、セッション中の設置シーン |
| **Story** | 開発背景・選手の物語 | Founder story、コーチの導入事例 |
| **Value** | GKコーチが得する情報 | ドリル集、コーチングTips、戦術解説 |
| **Engage** | 会話を生む問いかけ | "What's your favorite warm-up?" 系 |

週あたり Product:Story:Value:Engage = 2:1:3:1 を目安にする。

## Graph API メモ

- バージョン: **v19.0**
- 投稿は 2-step: `POST /{ig-user-id}/media` → `POST /{ig-user-id}/media_publish`
- 長期トークンは60日で失効。`scripts/token_refresh.py` で残存日数確認
- 自分の投稿のコメント取得・返信はGraph APIで可能
- **他人の投稿への自動いいね・自動コメントはMetaプラットフォーム規約違反** — 行わない

## コメント返信の3ステップ

1. `fetch_comments.py` で自分の投稿のコメント取得
2. `reply_comment.py` がClaude APIで返信案を生成し表示
3. 人間が承認（y/n）→ 承認時のみGraph API経由で送信

無承認の自動返信は絶対に行わない。

## ファイル構成

```
keepix-instagram/
├── agents/          # 役割別Claudeエージェント定義
├── scripts/         # Graph API / Claude API実行スクリプト
├── config/          # .env（シークレット）
├── content/         # 投稿素材・キャプション・カレンダー
└── data/            # ログ・インサイト保存先
```

## 実行前チェック

- `config/.env` に必要な値がすべて入っているか
- `python scripts/token_refresh.py` でトークン有効期限を確認
- 新規投稿は `content/calendar.json` に登録してから `post_to_instagram.py`

詳細は `SETUP_CHECKLIST.md` を参照。
