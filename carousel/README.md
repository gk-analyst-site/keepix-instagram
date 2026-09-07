# KEEPIX カルーセル連載 (GK coaching swipe carousels)

GKノウハウ記事を **スワイプ式カルーセル** に自動変換し、**@KEEPIX.GK_OFFICIAL** へ
**月・水・金 09:00 JST** に自動投稿する仕組みです。長い記事は **Part 1/2/3…** に自動分割して
小出し連載します。**各スライドは毎回「日本語（上）＋英語（下）」の併記**で出力します
（元記事は日本語でも英語でもOK。キャプションも日英併記）。

既存の Python 日次投稿とは **完全に独立**して動きます（この `carousel/` フォルダと
`.github/workflows/carousel.yml` だけで完結。GitHub Actions のクラウド上で動くので、
Mac の電源状態に一切依存しません）。

## 仕組み

1. `content/articles/*.md` … 1ファイル＝1記事（先頭に `--- title: ... lang: ja ---` を付けられます）。
2. スケジュール実行のたびに、**まだ投稿し終えていない記事の「次のパート」を1つだけ**投稿します。
3. 初回だけ Claude が記事を 2〜4 パート（各カルーセル4〜6枚）に分割し、`content/compiled/<記事>.json` に保存。
4. スライド画像を描画（`src/slides.js`、1080×1350、KEEPIXブランド色）。
5. 画像をこのリポジトリに commit → **コミットSHA固定の raw URL** を作成。
6. Instagram Graph API でカルーセル投稿（子コンテナ→FINISHED待ち→親CAROUSEL→publish、`9007` は自動リトライ）。
7. 進捗を `content/posted-articles.json` に記録。全パート投稿済みの記事は次回スキップ。

未投稿の記事が無い日は、何もせず終了します。

## 必要な設定（GitHub 側）

**Settings → Secrets and variables → Actions → Secrets** に3つ登録：

| Secret 名 | 値（Mac の `config/.env` からコピー） |
|---|---|
| `ANTHROPIC_API_KEY` | `ANTHROPIC_API_KEY=` の値 |
| `IG_USER_ID` | `INSTAGRAM_BUSINESS_ACCOUNT_ID=` の値 |
| `IG_ACCESS_TOKEN` | `META_ACCESS_TOKEN=` の値（無期限トークン） |

任意で **Variables**（Secretsではなく Variables タブ）：

| Variable 名 | 既定 | 用途 |
|---|---|---|
| `CLAUDE_MODEL` | `claude-opus-4-8` | 分割生成に使うモデル |
| `GRAPH_API_VERSION` | `v21.0` | Graph API バージョン |

## 使い方

- **記事を追加**: `content/articles/` に `.md` を置いてコミットするだけ。ファイル名の昇順で連載されます。
- **手動テスト（投稿しない）**: Actions → "KEEPIX carousel" → **Run workflow** → *dry_run = true*。
  スライドだけ描画され、`carousel/out/_preview` 相当の確認ができます（Actionsのログに枚数が出ます）。
- **手動で1パート投稿**: 同じく Run workflow で *dry_run = false*。
- **ローカルでデザイン確認**: `cd carousel && npm install && npm run preview` → `carousel/out/_preview/*.png`。

## ブランド / デザイン

- サイズ 1080×1350、背景 `#0B1512`、アクセント（ミント）`#5FE3A1`、本文 `#D7DEDA`。
- スライド種別: `cover`（表紙）/ `content`（本文・番号バッジ）/ `cta`（緑地の締め）。
- ロゴ: `carousel/assets/keepix-logo.png` を置くと表紙/CTAに描画（無ければ "KEEPIX" 文字）。
- フォント: Latin=Liberation Sans、日本語=Noto CJK（Actionsが自動インストール）。
  バンドルしたい場合は `carousel/assets/fonts/` に `Head.ttf` / `Body.ttf` / `JP.ttf`（or `.otf`）。

## 事実の扱い

記事本文に無い数値・価格・製品仕様などは **生成しません**（捏造防止のルールをプロンプトに明記）。
