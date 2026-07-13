# KEEPIX Instagram 運用プロンプト集

最終更新: 2026-04-26

## 重要原則

- KEEPIXをAI関連の言葉で説明しない（"built by a GK coach, for goalkeeper coaches"）
- 個人名・所属チーム名・大学名・実績は一切出さない
- ブランドボイスは「KEEPIX」として発信、一人称は"we"
- `agents/content-creator.md` の Privacy Rules を常に適用
- **投稿・コメント送信・トークン更新などの公開アクションは必ず人間の承認を取ってから実行**
- **破壊的操作の前に必ず dry-run で内容確認**

---

## 1. 日常投稿（最もよく使う）

### 1-1. フル自動（週7日分まとめて作成） ⭐最頻出

**使う場面:** 毎週月曜〜日曜分のコンテンツをまとめて仕込む。キャプション・画像・Cloudinaryアップロード・calendar.json まで一気通貫。

```
agents/content-creator.md をsystem promptとして、
2026-[MM-DD]〜[MM-DD] の週7日分の投稿をフルパイプラインで作成して。

週テーマ: [例: "GKのポジショニング基礎"]

投稿タイプ配分（推奨）:
  月: Engage（コメント誘導）
  火: Story（現場エピソード）
  水: Story or Reflection
  木: Value（ドリル/Tips カルーセル4枚）
  金: Value（Quick Tip 1枚）
  土: Product（KEEPIX機能紹介）
  日: Value（技術解説カルーセル4枚）

実行手順:
1. 7本分のキャプション生成 → content/captions/[日付]-[type]-[slug].md に保存
2. 画像が必要な投稿は scripts/generate_week_posts.py 形式で PNG 生成
   - 1080x1350px、背景 #0f3d2e、アクセント #2ECC71、テキスト #F5F5F0
   - GK=黄 #FFD700、コーチ=青 #3498DB、コーン=橙 #E67E22
   - content/posts/[日付]-[type]/ に保存
3. scripts/_upload_week.py 形式で全PNG を Cloudinary にアップロード
4. content/calendar.json を新しいエントリで更新（status: "scheduled"）
5. 全7件のdry-runサマリを表示して確認させて
6. 私がOK出したら完了（実投稿は scheduled_post.py が毎晩22:00に自動実行）

禁止事項:
- 個人名・チーム名・大学名を使わない
- "AI" "smart" "algorithm" "revolutionary" を使わない
- Privacy Rules に反する内容は生成しない
```

**完了後の確認コマンド:**
```bash
cat content/calendar.json | python3 -m json.tool | grep -E '"id"|"status"'
```

---

### 1-2. お任せ企画（テーマも考えてほしい時）

**使う場面:** 「何か投稿したいけどネタが思いつかない」「次の1本を丸ごと任せたい」時。テーマ選定から実装まで全部お任せ。

```
agents/content-creator.md をsystem promptとして、
次のInstagram投稿を1本企画して作って。

直近の投稿状況:
- 直近7件: content/calendar.json を読んで確認
- 同じタイプ・テーマが連続しないように配慮

条件:
- 投稿日: [例: 明日 / 今週末 / 特に指定なし]
- コンテンツタイプ: 特に指定なし（バランスを見て最適なものを選んで）
- 避けてほしいテーマ: [例: クロスは先週やった / なければ「なし」]

企画フォーマット（まず提案してから、私がOKしたら実装）:

---
タイプ: [Value/Product/Story/Engage]
テーマ: [一文で]
HOOK案: [キャプション書き出し]
画像構成: [枚数と各スライドの概要]
選んだ理由: [なぜこのテーマが今の @keepix_gk_official に合うか]
---

提案を見て「OK」または「別のテーマで」と返す。
OKしたら 1-1 の手順（キャプション→画像→Cloudinary→calendar.json）で実装。
```

---

### 1-3. 特定の1本だけ作る

**使う場面:** 週の途中でスポット投稿を追加したい時。

```
agents/content-creator.md をsystem promptとして、
[Value|Product|Story|Engage] 投稿を1本作って。

テーマ: [例: "クロスボール処理の3つの判断基準"]
投稿日: [例: 2026-05-03]
投稿時刻: 22:00 JST

手順:
1. キャプション生成 → content/captions/[日付]-[type]-[slug].md に保存
2. 画像生成（カルーセルなら4枚、単体なら1枚）
   → content/posts/[日付]-[slug]/ に保存
3. Cloudinary アップロード → secure_url を取得
4. calendar.json に新エントリを追加
5. dry-run で内容確認させて
6. 私がOK出したら完了（自動投稿に乗る）
```

---

### 1-4. キャプションだけ作る

**使う場面:** 画像は手元に用意済み、または後日作る。文章だけ先に固めたい時。

```
agents/content-creator.md をsystem promptとして、以下の投稿のキャプションを作って。

コンテンツタイプ: [Value / Product / Story / Engage]
テーマ: [例: "若手GKによくある足の入れ方ミス3つ"]
狙い: [例: "土曜の練習前に保存してもらえるTips"]

出力:
- content/captions/[日付]-[slug].md に保存
- ハッシュタグは15-20個（core/niche/broad のバランス）
- 英語ネイティブコーチ向けトーン
- markdown の **bold** は使ってOK（投稿時に自動で剥がれる）
```

---

### 1-5. 画像だけ作る

**使う場面:** キャプションが既にある、またはリール等で画像だけ必要な時。

```
以下のドリル/テーマを表現するInstagram用カルーセル画像を [N] 枚作って。

テーマ: [例: "ロングキックの3段階フォーム"]
スライド構成: [例: Hero / Step 1 / Step 2 / Step 3]

デザイン指定:
- 1080x1350px (4:5縦)
- 背景 #0f3d2e、ピッチエリア #1a5c3f、アクセント #2ECC71、テキスト #F5F5F0
- GK=黄 #FFD700、コーチ=青 #3498DB、コーン=橙 #E67E22、ボール=白
- ボール軌跡=白点線矢印、選手移動=黄色実線矢印
- トップダウン視点のピッチダイアグラム
- 距離は "4m" のように数字で明記
- 右下に小さく KEEPIX ロゴ
- sans-serif bold タイポグラフィ

手順:
1. scripts/generate_value_post.py を参考に1ファイルのPythonスクリプト作成
2. content/posts/[日付]-[slug]/ に PNG を保存
3. resvg-py でラスタライズ
4. 生成後、各PNGを1枚ずつ表示して確認させて
```

**注意:** `scripts/generate_week_posts.py` の既存ヘルパー（`svg_doc()`, `pitch_frame()`, `drill_header()`, `takeaway()`）を流用するとレイアウトが一貫する。

---

### 1-6. 手動で即時投稿（calendar.jsonを使わず）

**使う場面:** 用意済みの画像とキャプションをすぐに投稿したい時。

```bash
# dry-run で確認
cd ~/Desktop/keepix-instagram
python3 scripts/post_to_instagram.py \
  --auto-upload content/posts/[日付]-[slug]/slide-*.png \
  --caption-file content/captions/[日付]-[slug].md \
  --dry-run

# OK なら --dry-run を外して実行
```

---

### 1-7. calendar.json から特定エントリを手動投稿

**使う場面:** 自動投稿が失敗した時、または予定より早く投稿したい時。

```bash
# dry-run で確認
python3 scripts/post_to_instagram.py \
  --from-calendar [ID] \
  --dry-run

# 例: 2026-04-26-reflection-why-we-coach
# 投稿実行
python3 scripts/post_to_instagram.py --from-calendar 2026-04-26-reflection-why-we-coach
```

---

## 2. コンテンツタイプ別テンプレ

### Value投稿（ドリル・技術解説）

**使う場面:** 週3本の主力コンテンツ。コーチが保存したくなるドリル・技術解説。
**画像:** カルーセル3-4枚、フィールド俯瞰図

**テーマ例:**
- GKドリル3-4種（カルーセル）
- ポジショニングの原則
- 1v1の駆け引き
- クロス対応のフットワーク
- セットプレー時の判断基準

```
agents/content-creator.md をsystem promptとして、Value投稿を作って。

テーマ: [例: "1v1ブレイクアウェイの足の置き方"]

構成:
- HOOK: 問題提起または数字で釣る（例: "3 drills, 12 minutes"）
- CAPTION: 具体的なドリル or Tips を3つ（各ドリルに所要時間 / セットアップ / 狙い）
- CTA: "Save this" 系
- HASHTAGS: 15-20個

画像: カルーセル4枚（Hero + ドリルごとに1枚、ピッチトップダウン視点）

内容要件:
- 具体的な距離・人数・時間を書く（"4m apart", "3 reps", "2 minutes"）
- 医学的主張（怪我予防を断言する等）は避ける
- "This drill will make you better" のような抽象表現を避ける
```

---

### Product投稿（KEEPIX機能紹介）

**使う場面:** KEEPIXそのものを見せる投稿。頻度は週1程度。
**画像:** 機能スクショ風 or インフォグラフィック

**テーマ例:**
- ドリルライブラリの使い方
- セッション設計5分で完成
- GK評価シートの活用法
- エクスポート機能（PNG/PDF）

```
agents/content-creator.md をsystem promptとして、Product投稿を作って。

訴求する機能: [例: "ドリルライブラリの検索フィルタ"]
見せたい状況: [例: "土曜朝の練習直前、phoneでサッと検索"]

画像案:
- 現場で使っている雰囲気のモックアップ
- スマホ画面にKEEPIXのUI（ドリルカード、フィルタチップ等）
- コーチの手元 or 練習場の雰囲気を入れる

禁止表現（絶対使わない）:
- AI / machine learning / algorithm / neural / smart *
- "Powered by AI" 系
- "Revolutionary" "Game-changing" 系のハイプ

代わりに使う表現:
- "Built by a GK coach, for goalkeeper coaches"
- "One tap away"
- "Session planning that doesn't eat your Sunday"
```

**注意:** 禁止表現チェックを最後に必ず実行してから投稿すること。

---

### Story投稿（匿名の観察・気づき）

**使う場面:** 月1-2本。ブランドの温度を伝える。個人名・所属は一切出さない。
**画像:** 1-2枚、シンプルなビジュアル

**テーマ例:**
- セッション中の小さな発見
- よくある指導ミス
- 選手の変化のサイン

```
agents/content-creator.md をsystem promptとして、Story投稿を作って。

エピソード: [例: "ユース指導でクロス処理の判断基準を変えたら失点が減った試合"]
今のKEEPIXとの接続: [例: "その小さい判断のズレをドリル化したのがKEEPIXの出発点"]

構成:
- HOOK: シーン描写で始める（"Matchday. 87th minute. 2-2..." のような具体性）
- CAPTION: コーチとしての語り口（"we" または "a keeper we worked with"）
- CTA: なし or "What's yours?" 系
- 画像: 引用風デザインスライド1枚（人物写真は不要）

トーン: ピッチサイドの同僚が話してる感じ。プレゼン風にしない。
Privacy: 固有名詞（人名・チーム名・大学名）を一切使わない。
```

---

### Engage投稿（質問・投票）

**使う場面:** 週1本、コメント欄を動かす目的。
**画像:** 1枚、質問テキスト中心

**テーマ例:**
- "あなたが最初に教えるGKの基礎は？"
- "セッション最初の10分、何をしている？"
- "影響を受けた1冊の本は？"

```
agents/content-creator.md をsystem promptとして、Engage投稿を作って。

質問テーマ: [例: "シュートストップで一番大事なのは何？"]

構成:
- HOOK: 質問そのもの、または前振り1行
- CAPTION: なぜ聞いているか短く、回答例を2-3個示してコメント敷居を下げる
- CTA: "Drop yours below — one sentence is enough"
- 画像: 1枚。質問文が大きく書かれたシンプルなカード

注意: 一般論すぎる質問（"What's your favorite drill?"）は避け、具体条件を付ける
（"What's your go-to warm-up for U14 keepers?"）。
```

---

### Quick Tip投稿（1枚完結）

**使う場面:** 週1本、スクロールを止める即効性のある1枚。読んですぐ使える内容。
**画像:** 1枚、読んですぐ実践できる内容

**テーマ例:**
- 30秒ウォームアップキュー
- コーチングワードの使い分け
- 試合前のメンタルチェック

```
agents/content-creator.md をsystem promptとして、Quick Tip投稿を1枚で作って。

テーマ: [例: "ハイクロスに入るタイミングを決める3秒ルール"]

構成:
- 画像1枚: Tip本文がそのまま読めるレイアウト（箇条書き or 3ステップ）
  フォント大きめ、背景 #0f3d2e、アクセント #2ECC71
- CAPTION: 画像の内容を自然に補足（画像と同じ内容の繰り返しにしない）
- CTA: "Save for your next session" 系
- HASHTAGS: 15個程度

要件:
- 1枚で完結する情報量に抑える
- 実際の練習で使える具体性（抽象論にしない）
```

---

### Quote/Reflection投稿（週末の振り返り）

**使う場面:** 週末（土・日）、数字やドリルを離れて温度を上げる投稿。
**画像:** 引用風デザイン1枚

**テーマ例:**
- "Why we coach"
- コーチングの本質
- 週の学び

```
agents/content-creator.md をsystem promptとして、Quote/Reflection投稿を作って。

テーマ: [例: "Why we coach" / "週の学び" / "コーチングの本質"]
きっかけ: [例: "今週、選手が初めて声を出してビルドアップに関わった瞬間があった"]

構成:
- CAPTION: 短め（150-250words）、詩的すぎず、主張を1つに絞る
- CTA: なし or "What's your why?" 系
- 画像: 引用風デザイン1枚
  - 中央に短いキーフレーズ（キャプションの核心を1-2行）
  - 背景 #0f3d2e、mint アクセントライン、KEEPIX ロゴ右下

Privacy: 固有名詞なし、シーン描写のみで温度を出す。
トーン: 静か、力まない、コーチとしての誠実さ。
```

---

## 3. コメント返信

### 3-1. 新コメント取得＆返信案生成

```
scripts/fetch_comments.py で直近の未返信コメントを取得して、
agents/comment-responder.md をsystem promptに返信案を生成して。

対象: 過去24時間の全投稿
出力先: data/pending_replies.json（既存なら追記）

返信案の要件:
- 英語、コーチ同士の会話トーン
- 質問には具体的に答える（"Good question" だけで終わらせない）
- スパム/宣伝コメントには reply 案を作らず skip フラグを立てる
- 生成後、各コメントと返信案をペアで一覧表示して確認させて
```

---

### 3-2. 承認済み返信の送信

```
data/pending_replies.json の中で approved=true のものを
scripts/reply_comment.py で送信して。

手順:
1. approved=true のエントリを一覧表示して最終確認させて
2. 私がOK出したら1件ずつ送信、結果をログ
3. 送信済みは status=sent に更新
4. 失敗したものは status=failed に更新して理由を残す
```

**注意:** 一度送ったコメントは編集不可。誤字/表現ミスがないか最終確認は必須。

---

### 3-3. pending返信一覧確認

```
data/pending_replies.json を読んで、status別にカウントして一覧表示して。

出力:
- pending（未承認）の件数と元コメントの抜粋
- approved（送信待ち）の件数
- sent/failed の直近10件
- 古い pending があれば警告（48時間以上前）
```

---

## 4. トークン・アカウント管理

### 4-1. トークン有効期限確認

```
scripts/token_refresh.py --check で META_ACCESS_TOKEN の有効期限を確認して。

出力:
- 現在のトークン種別（short-lived / long-lived）
- 残り有効日数
- 紐づく Instagram Business Account / Facebook Page
- 30日以内に失効するなら警告
```

---

### 4-2. トークン長期化（60日前に実行）

```
scripts/token_refresh.py で long-lived token を更新して。

手順:
1. 現在のトークン有効期限を確認
2. 新しい long-lived token を取得（/oauth/access_token?grant_type=fb_exchange_token）
3. config/.env の META_ACCESS_TOKEN を書き換える前に古い値をコメントで残す
4. 更新後、新トークンで /me を叩いて動作確認
5. 成功したらコメントアウトした古い値を削除
```

**注意:** トークンは絶対にチャット/PR/Slack に貼らない。.env 以外に書き出さない。

---

### 4-3. アカウント情報確認

```
Graph API で以下を取得して表示:
- Instagram Business Account ID (@keepix_gk_official)
- Facebook Page ID
- 現在のアクセストークンの scope
- フォロワー数、投稿数、メディア総数

秘匿情報（トークン本体、App Secret）は絶対に表示しないこと。
```

---

## 5. 自動投稿パイプライン管理

### 5-1. launchd ステータス確認

```bash
# 登録済みジョブ確認
launchctl list | grep keepix

# 期待出力:
# -  0  com.keepix.instagram.post     ← 毎日 22:00 投稿実行
# -  0  com.keepix.instagram.wakeup   ← 毎日 21:50 スリープ防止
```

---

### 5-2. 今夜の投稿を手動でdry-run確認

```bash
cd ~/Desktop/keepix-instagram
python3 scripts/scheduled_post.py --dry-run
```

---

### 5-3. 投稿ログ確認

```bash
# リアルタイムログ
tail -f ~/Desktop/keepix-instagram/data/launchd-stdout.log

# 投稿ログ（成功/失敗ステータス）
tail -30 ~/Desktop/keepix-instagram/data/post_log.txt

# caffeinate ログ
tail -10 ~/Desktop/keepix-instagram/data/caffeinate.log
```

---

### 5-4. calendar.json のステータス確認

```bash
# 全エントリのid/statusを一覧
python3 -c "
import json
cal = json.load(open('content/calendar.json'))
for p in cal['posts']:
    print(f\"{p['scheduled_at'][:10]}  {p['status']:10}  {p['id']}\")
"
```

---

### 5-5. launchd の再起動・解除

```bash
# 投稿ジョブを再起動
launchctl unload ~/Library/LaunchAgents/com.keepix.instagram.post.plist
launchctl load  ~/Library/LaunchAgents/com.keepix.instagram.post.plist

# スリープ防止ジョブを再起動
launchctl unload ~/Library/LaunchAgents/com.keepix.instagram.wakeup.plist
launchctl load  ~/Library/LaunchAgents/com.keepix.instagram.wakeup.plist

# 両方を完全に解除（自動投稿停止）
launchctl unload ~/Library/LaunchAgents/com.keepix.instagram.post.plist
launchctl unload ~/Library/LaunchAgents/com.keepix.instagram.wakeup.plist
```

---

## 6. インサイト・分析（App Review承認後）

> **注意:** `instagram_manage_insights` 権限の App Review が通るまでは 6-1, 6-2 は使えない。

### 6-1. 週次レポート生成

```
scripts/get_insights.py で過去7日間のインサイトを取得して、
agents/analytics.md をsystem promptに週次レポート作成。

対象指標:
- リーチ / インプレッション / プロフィール訪問 / ウェブサイトクリック
- 投稿ごとの reach, saves, shares, comments
- 新規フォロワー / フォロワー解除
- ベスト投稿3本 / ワースト投稿3本

出力先: data/reports/$(date +%Y-week-%V).md
形式: マークダウン、数字＋一行コメント、翌週のアクション3つ
```

---

### 6-2. 投稿パフォーマンス確認

```
Instagram media ID [xxxxxxx] のインサイトを取得して分析して。

取得指標:
- reach, impressions, saves, shares, comments, likes
- 時間帯別のエンゲージ推移（可能なら）
- 同コンテンツタイプ（Value/Product/Story/Engage）の平均と比較

出力: 何が効いた/効かなかったかの仮説を3つまで。
今後の同タイプ投稿への示唆。
```

---

## 7. トラブルシューティング

### 自動投稿が失敗した時

```
昨夜22:00の自動投稿が失敗した。以下を順番に確認して。

1. launchctl list | grep keepix でジョブ登録確認
2. tail -50 ~/Desktop/keepix-instagram/data/launchd-stderr.log
3. tail -50 ~/Desktop/keepix-instagram/data/launchd-stdout.log
4. tail -30 ~/Desktop/keepix-instagram/data/post_log.txt
5. calendar.json の当日エントリの status を確認
6. python3 scripts/scheduled_post.py --dry-run で手動再現確認

結果をまとめて: 失敗原因 / エラー箇所 / 修正方法の提案
（修正・再投稿は私の承認後に実行）
```

---

### Graph API エラー時

```
直前のInstagram投稿が失敗した。ログを確認して根本原因を特定して。

確認項目:
1. エラーメッセージ（Graph API error code / subcode）を整理
2. Cloudinary URL が公開HTTPSで reachable か curl で確認
3. キャプション文字数（2200以内）
4. 画像サイズ（最大8MB、1080x1350推奨）
5. カルーセルの場合、子コンテナの status_code が ERROR になっていないか
6. トークンが有効か

原因特定後、修正案を提示（投稿は再実行しない、私の承認を待つ）。
```

---

### トークンエラー時

```
META_ACCESS_TOKEN のエラーが出た。以下を順に確認して。

1. scripts/token_refresh.py --check で失効確認
2. App ID とトークンの App ID が一致するか
3. 必要な scope（instagram_basic, instagram_content_publish, pages_show_list 等）があるか
4. Instagram Business Account との紐付けが切れていないか
5. 直近でパスワード変更やログイン通知が来ていないか（ユーザーに質問）

トークン再取得が必要なら手順を提示、勝手に更新しない。
```

---

### Cloudinary エラー時

```
Cloudinaryアップロードが失敗した。以下を確認して。

1. config/.env の CLOUDINARY_* 3項目が埋まっているか
2. Cloud Name のスペルミス（ハイフン/アンダースコア）
3. API Secret がquoteされていないか（.env は quote 不要）
4. Cloudinaryダッシュボードで直接ログインできるか（API停止がないか）
5. 月間無料枠（25GB/月）を超えていないか
6. アップロード対象ファイルが存在するか、サイズが10MB以下か

原因特定後、.env 修正が必要なら私に値を聞く。勝手に書き換えない。
```

---

## 8. メンテナンス

### 週次タスク（毎週月曜朝）

```
以下の週次メンテナンスを順に実行して。

1. 前週のインサイト確認（セクション6-1）
2. data/pending_replies.json のステータス確認
3. 今週の投稿カレンダー content/calendar.json を確認
   → status=scheduled のエントリが7件あるか
   → 不足スロットがあれば1-1のプロンプトで補充提案
4. トークン残日数確認（セクション4-1）
5. content/posts/ の古いディレクトリ（60日以上前）をリストアップ
   （削除はしない、確認のみ）

最後にサマリを3行で報告。
```

---

### 月次タスク（毎月1日）

```
以下の月次メンテナンスを順に実行して。

1. 月間サマリレポート作成（リーチ/エンゲージ/ベスト投稿）
2. トークン有効期限が60日以内なら更新（セクション4-2）
3. content/posts/ の90日以上前の画像をアーカイブ候補としてリスト
4. Cloudinary の使用量確認（ダッシュボードURL案内）
5. agents/ のプロンプト見直し提案
   （直近1ヶ月の失敗ケースから学習点を抽出）

月次レポートは data/reports/$(date +%Y-%m)-monthly.md に保存。
```

---

## 9. 運用フロー

### 毎日の自動フロー

```
21:50  launchd → caffeinate 起動（スリープ防止 20分）
22:00  launchd → scheduled_post.py 起動
         calendar.json から status=scheduled かつ ±60分のエントリを検索
         → post_to_instagram.py --from-calendar [ID] を実行
         → 成功: status="posted", posted_at, ig_media_id を記録
         → 失敗: status="failed", fail_reason を記録、post_log.txt にも出力
22:10  caffeinate 自動終了
```

**ログ確認:**
```bash
tail -20 ~/Desktop/keepix-instagram/data/post_log.txt
```

---

### 週次運用サイクル

```
月曜（朝）  週次メンテ（セクション8）
           └─ インサイト確認 / calendar確認 / トークン残日数確認

月曜（午前）1-1 フル自動で翌週7日分を仕込む
           └─ キャプション → 画像 → Cloudinary → calendar.json

月〜日（22:00）自動投稿（launchd）
           └─ scheduled_post.py が毎晩実行

随時        コメント返信（セクション3）
           └─ 朝の確認 → 返信案生成 → 承認 → 送信
```

---

### 月次運用サイクル

```
毎月1日     月次メンテ（セクション8）
           └─ 月間レポート / トークン更新 / ストレージ整理

随時        トークン残日数が60日を切ったら更新（セクション4-2）
```

---

### パイプライン全体図

```
[アイデア/テーマ]
       ↓
[キャプション生成]  agents/content-creator.md
content/captions/[日付]-[type]-[slug].md
       ↓
[画像生成]  scripts/generate_week_posts.py → resvg_py
content/posts/[日付]-[type]/slide-*.png
       ↓
[Cloudinaryアップロード]  scripts/_upload_week.py
https://res.cloudinary.com/drcsslwyg/...
       ↓
[calendar.json 登録]  status: "scheduled"
       ↓
[自動投稿]  launchd 22:00 → scheduled_post.py
       ↓
[calendar.json 更新]  status: "posted" + ig_media_id
       ↓
[コメント管理]  fetch → 返信案生成 → 承認 → 送信
       ↓
[インサイト確認]  週次レポート → 翌週改善
```

---

### 緊急時の手動投稿手順

自動投稿が失敗した場合:

```bash
# 1. 失敗確認
tail -30 ~/Desktop/keepix-instagram/data/post_log.txt

# 2. dry-run で内容確認
cd ~/Desktop/keepix-instagram
python3 scripts/post_to_instagram.py --from-calendar [失敗したID] --dry-run

# 3. 問題なければ実投稿
python3 scripts/post_to_instagram.py --from-calendar [失敗したID]
```

---

### 主要ファイル一覧

| ファイル | 役割 |
|---|---|
| `content/calendar.json` | 投稿スケジュール管理（scheduled/posted/failed） |
| `content/captions/` | 全キャプション .md ファイル |
| `content/posts/` | 生成済み PNG 画像 |
| `config/.env` | 全シークレット（Git管理外） |
| `agents/content-creator.md` | コンテンツ生成用 system prompt |
| `scripts/scheduled_post.py` | 自動投稿スクリプト（launchd から呼ばれる） |
| `scripts/post_to_instagram.py` | 単体投稿スクリプト（手動・自動共通） |
| `scripts/generate_week_posts.py` | 週7日分の画像一括生成 |
| `scripts/_upload_week.py` | 週7日分の Cloudinary 一括アップロード |
| `data/post_log.txt` | 投稿成功/失敗ログ |
| `data/launchd-stdout.log` | launchd 標準出力ログ |
| `data/launchd-stderr.log` | launchd エラーログ |
| `~/Library/LaunchAgents/com.keepix.instagram.post.plist` | 22:00 投稿ジョブ |
| `~/Library/LaunchAgents/com.keepix.instagram.wakeup.plist` | 21:50 スリープ防止ジョブ |

---

## 使い方メモ

- プロンプトは全部そのまま上から貼らず、**該当セクションだけコピペ**するのがコツ
- `[括弧で囲った部分]` は毎回書き換える可変値
- 新しいパターンが出てきたらこのファイルに追記していく（このファイル自体が運用ログ）
- 一番の時短ルート: **セクション1-1**（週7日分まとめて作成）→ あとは全自動
