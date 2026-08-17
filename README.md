# えいご シールクイズ

5歳〜小学生むけの無料英単語クイズ（全300語・読み上げつき・4択）。
公開URL: https://tagc.works/eigo-quiz/

## 構成

```
eigo-quiz/
├ index.html              クイズ本体（表紙・デモ・プレイ画面）
├ data/words.json         単語300語。語を足すときはここだけ編集
├ audio/                  読み上げmp3（tools/generate_audio.py で生成）
├ icons/                  PWAアイコン
├ manifest.webmanifest    ホーム画面追加の設定
├ sw.js                   Service Worker（オフライン対応）
├ for-parents/            おうちの方へ
├ words/                  カテゴリ別の単語一覧（検索の入口）
├ sitemap.xml / robots.txt
└ tools/generate_audio.py 音声一括生成
```

## デプロイ（GitHub Pages）

1. このディレクトリの中身を `eigo-quiz` リポジトリのルートに置く
2. Settings → Pages → Deploy from a branch → main / (root)
3. ユーザーサイト（`ユーザー名.github.io`）に `tagc.works` を設定済みなら、
   自動で `https://tagc.works/eigo-quiz/` で配信される
4. Search Console に `sitemap.xml` を登録

`robots.txt` と `sitemap.xml` はドメイン直下（`tagc.works/`）に置くのが正式です。
このリポジトリのものはコピー元として使ってください。

## 音声の生成

```bash
brew install ffmpeg
python3 tools/generate_audio.py --engine say       # 無料・オフライン
python3 tools/generate_audio.py --engine openai    # 高品質（要 OPENAI_API_KEY）
```

audio/ が空でも動きます（端末の読み上げ機能にフォールバック）。

## 単語を増やす

`data/words.json` に追記するだけ。形式:

```json
{ "en": "apple", "ja": "りんご", "emoji": "🍎", "cat": "food", "level": 1, "ex": "" }
```

絵文字で表せない語は `emoji` を空にして `ex`（例文ヒント）を書く。
`words/` の一覧ページは `tools/` のスクリプトで再生成する想定。

## 注意

- パスはすべて相対（`./`）。サブディレクトリ配信のため絶対パスにしない
- Service Worker を更新したら `sw.js` の `V` を上げる
