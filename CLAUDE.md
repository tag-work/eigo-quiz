# えいご シールクイズ — プロジェクトメモ

5歳〜小学生むけの無料英単語クイズ。作者は tagc、最初のユーザーは6歳の娘。
本番: https://tagc.works/eigo-quiz/

## 全体構成

GitHub Pages で配信。ドメインは Porkbun で取得し、apex を GitHub Pages に向けている。

```
tag-work.github.io リポジトリ → https://tagc.works/           ポートフォリオ
eigo-quiz リポジトリ          → https://tagc.works/eigo-quiz/  このリポジトリ
```

`tag-work.github.io` 側にだけカスタムドメインを設定してあり、このリポジトリは
Custom domain を空にすることで自動的に `tagc.works/eigo-quiz/` で配信される。
**このリポジトリの Pages 設定に Custom domain を入れてはいけない。**

## ファイル

```
index.html              クイズ本体。HTML/CSS/JS が1ファイルに入っている
data/words.json         単語300語。語の追加はここだけ触る
audio/<slug>.mp3        読み上げ音声300個
icons/                  PWAアイコン（おしりん）
manifest.webmanifest    ホーム画面追加の設定
sw.js                   Service Worker
for-parents/index.html  おうちの方へ
words/<group>/          カテゴリ別の単語一覧20ページ（SEOの入口）
tools/generate_audio.py 音声の一括生成
tools/build_pages.py    words/ と sitemap.xml の再生成
```

`index.html` が唯一の実装。ビルドツールもフレームワークも使っていない。
外部依存は Google Fonts（Zen Maru Gothic / Baloo 2）だけ。

## 触るときの必須ルール

**1. パスは必ず相対パス（`./`）。**
サブディレクトリ配信なので `/data/words.json` と書くと 404 になる。

**2. `sw.js` を変更したら `const V="eigo-quiz-vN"` を必ず上げる。**
上げないとホーム画面に追加済みの端末で古いファイルが読まれ続ける。
`index.html` を更新したときも上げること。ここを忘れると「直したのに直らない」が起きる。

**3. SVG を `<symbol>` + `<use>` で書かない。**
`<use>` の中身はシャドウDOMになり、外側のCSSセレクタが届かず全部黒く潰れる。
キャラクターは `MASCOT` というテンプレート文字列を `innerHTML` で挿し込んでいる。この方式を維持する。

**4. 画面セクションは必ず `<div class="wrap">` の内側に置く。**
外に出すと `max-width:420px` と左右padding が効かず、横幅いっぱいに広がる。

**5. localStorage は try/catch でラップする。**
`store` オブジェクトが、使えない環境ではメモリに退避するようになっている。この構造を壊さない。

**6. 音声ファイル名は英単語の slug。**
`en.toLowerCase().replace(/[^a-z0-9]+/g,"-")` で、`ice cream` → `ice-cream.mp3`。
mp3 がなければ端末の読み上げに自動フォールバックするので、音声なしでも動く。

## デザインの決まり

CSS 変数で定義済み。勝手に増やさない。

```
--paper #EDEBFF  背景     --ink   #2E2350  文字と枠線
--pink  #FF6FA5  主ボタン  --sun   #FFD23F  強調
--grass #3DBE7A  正解     --sky   #57BCF0  音声ボタン
--skin  #FFB5A3  おしりん
```

- 枠線は太く（3〜4px）、影は `0 Npx 0 var(--ink)` のオフセット影。ぼかしは使わない
- 押した瞬間に `translateY` で沈める
- **子どもが見る画面はひらがなのみ。** 漢字とカタカナ語は使わない
- **おうちの方が見る画面（for-parents、words/）は漢字でよい**
- 対象は6歳。1画面の情報量を増やさない。ボタンは最低96px高

## キャラクター「おしりん」

おしり型の応援キャラ。正解するとジャンプして力こぶを作り、目が「＾＾」になって褒める。
セリフは `PRAISE` / `PRAISE3` / `PRAISE8` / `MISS` / `IDLE` の配列からランダム。

- おしりネタは正解時だけ。**間違えたときは普通に励ます**（落ち込ませない）
- 割れ目の線は口までつなげない。つなぐと怖い顔になる
- 3連続・8連続で演出とセリフが1段階ずつ強くなる

## 単語を追加する手順

1. `data/words.json` に追記

```json
{ "en": "apple", "ja": "りんご", "kana": "アップル", "emoji": "🍎",
  "cat": "food", "level": 1, "ex": "" }
```

- `ja` は全単語でユニークにする（同じだと4択の答えが2つになる）
- 絵文字で表せない語は `emoji` を空にして `ex` に例文ヒントを書く
- `level` は 1（5〜6歳）/ 2（小1〜3）/ 3（小4〜6）
- `cat` は同じレベル・同じカテゴリからダミー選択肢が選ばれるので、意味の近いものを

2. 音声を生成: `python3 tools/generate_audio.py --engine openai`
3. 一覧ページを再生成: `python3 tools/build_pages.py`
4. `sw.js` の `V` を上げて push

`index.html` にも300語が埋め込まれているが、これは `data/words.json` の読み込みに
失敗したときのフォールバック。本番では JSON が優先されるので、**通常は JSON だけ更新すればよい**。

## やらないこと

- **クイズ画面に広告を入れない。** 親向けページには入れる可能性がある
- **学習記録を外部送信しない。** localStorage に閉じる。for-parents でそう明記している
- 登録・ログインを要求しない
- 外部リンクをクイズ画面に置かない
- 絶対パスを書かない

## 確認方法

```bash
python3 -m http.server 8000   # file:// では Service Worker が動かない
```

- iPhone 実機で、ホーム画面に追加した状態で音が出るか
- ピンチで拡大されないか（`touch-action:manipulation` と gesture イベント抑止で対応済み）
- ずかんが横幅いっぱいに広がっていないか

## デプロイ

`main` に push すれば GitHub Pages が自動で反映する。1〜2分。
反映されないときは Service Worker のキャッシュを疑う（`V` の上げ忘れ）。

## 経緯のメモ

- ネイティブアプリではなく Web を選んだのは、検索から辿り着けることと配布の手間がないため
- 10問終了後の自動送りは一度実装したが、**喜びを噛みしめる前に次へ進んでしまうため廃止した**。
  親に見せに行く間があるので、押すまで待つ
- 15分で休憩を促すのは意図的な仕様。外さない
