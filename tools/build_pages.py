#!/usr/bin/env python3
"""
data/words.json から words/ 以下のカテゴリ別一覧ページと sitemap.xml を再生成する。
単語を追加したら実行すること。

  python3 tools/build_pages.py
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://tagc.works/eigo-quiz"
GA_ID = "G-XXXXXXXXXX"   # ← 実際の測定IDに合わせる
GA = f"""<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}
gtag('js',new Date());gtag('config','{GA_ID}');</script>
"""

WORDS = json.load(open(os.path.join(ROOT, "data/words.json"), encoding="utf-8"))

GROUPS = [
 ("animals","どうぶつ",["animal","animal2"],"いぬ・ねこから、いるか・ちょうちょまで。子どもが最初に覚えやすい動物の英単語です。"),
 ("food","たべもの",["food","food2"],"くだもの・野菜から、ハンバーガー・カレーまで。食卓で使える食べ物の英単語です。"),
 ("colors","いろとかたち",["color"],"あか・あお・きいろなど、身のまわりのものを説明するときに欠かせない色の英単語です。"),
 ("numbers","かず",["number"],"1から20まで。年齢や個数を言うときの基本になる数の英単語です。"),
 ("calendar","ようびと つき",["calendar"],"曜日7つと月12個。絵で表しにくいので、例文で覚えるのがおすすめです。"),
 ("weather-season","てんきときせつ",["weather","season"],"はれ・くもり・あめから、春夏秋冬と行事まで。毎日の会話で使いやすい英単語です。"),
 ("nature","しぜん",["nature"],"たいよう・つき・ほしなど、外に出たときに指させる自然の英単語です。"),
 ("body","からだ",["body","body2"],"め・みみ・はなから、うで・ひざまで。歌やお風呂で覚えやすい体の英単語です。"),
 ("family","かぞく",["family"],"おかあさん・おとうさんなど、いちばん身近な人を表す英単語です。"),
 ("feelings","きもち",["feeling"],"うれしい・かなしい・ねむい。気持ちを英語で言えると会話がぐっと広がります。"),
 ("house","おうちのもの",["house"],"ドア・まど・ベッドなど、家の中で指させるものの英単語です。"),
 ("clothes","ふく",["clothes"],"シャツ・ズボン・くつなど、毎朝の身じたくで使える英単語です。"),
 ("school","がっこう",["school","subject"],"えんぴつ・ノートから、さんすう・りかなどの教科まで。"),
 ("vehicles","のりもの",["vehicle"],"くるま・でんしゃ・ひこうき。乗り物好きの子が真っ先に覚える英単語です。"),
 ("places","ばしょ",["place"],"こうえん・びょういん・えきなど、お出かけ先を表す英単語です。"),
 ("sports","スポーツ",["sport"],"サッカー・やきゅう・スイミングなど、習いごとでもよく出てくる英単語です。"),
 ("jobs","しごと",["job"],"せんせい・いしゃ・パイロット。「大きくなったら何になりたい？」で使える英単語です。"),
 ("actions","うごきのことば",["action","verb"],"たべる・はしる・つくるなど、文をつくる土台になる動詞です。"),
 ("adjectives","ようすのことば",["adjective"],"おおきい・ちいさい・たのしいなど、ものごとを説明する形容詞です。"),
 ("greetings","あいさつ",["greeting"],"こんにちは・ありがとう・ごめんなさい。今日から使えるあいさつの英語です。"),
]
LVN = {1:"レベル1（5〜6歳）",2:"レベル2（小1〜3）",3:"レベル3（小4〜6）"}

CSS = '''*{box-sizing:border-box;margin:0;padding:0}
:root{--paper:#EDEBFF;--ink:#2E2350;--pink:#FF6FA5;--sun:#FFD23F}
body{font-family:"Zen Maru Gothic","Hiragino Maru Gothic ProN",system-ui,sans-serif;color:var(--ink);
background:var(--paper);line-height:1.8;padding:24px 16px 60px}
.wrap{max-width:720px;margin:0 auto}
a{color:#2E2350}
.crumb{font-size:12px;opacity:.7;margin-bottom:14px}
h1{font-size:26px;font-weight:900;line-height:1.35;margin-bottom:12px}
h2{font-size:19px;font-weight:900;margin:28px 0 10px;padding-left:11px;border-left:6px solid var(--sun)}
h3{font-size:16px;font-weight:900;margin:18px 0 6px}
p{font-size:15px;margin-bottom:12px}
.card{background:#fff;border:3px solid var(--ink);border-radius:20px;box-shadow:0 6px 0 var(--ink);
padding:16px;margin:16px 0}
table{width:100%;border-collapse:collapse;background:#fff;border:3px solid var(--ink);border-radius:16px;overflow:hidden}
th,td{padding:10px 12px;text-align:left;font-size:15px;border-bottom:2px dotted #2E235033}
th{background:var(--sun);font-weight:900;font-size:13px}
tr:last-child td{border-bottom:0}
td.en{font-weight:900;font-family:"Baloo 2",system-ui,sans-serif}
td.lv{font-size:11px;opacity:.65;white-space:nowrap}\ntd.kana{font-size:13px;opacity:.8}
.btn{display:block;text-align:center;background:var(--pink);border:3px solid var(--ink);border-radius:20px;
padding:16px;font-size:20px;font-weight:900;text-decoration:none;box-shadow:0 6px 0 var(--ink);margin:24px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-top:12px}
.grid a{background:#fff;border:2.5px solid var(--ink);border-radius:14px;padding:11px;text-decoration:none;
font-weight:900;font-size:14px;box-shadow:0 3px 0 var(--ink)}
.grid a span{display:block;font-size:11px;font-weight:700;opacity:.6}
footer{margin-top:40px;font-size:12px;opacity:.7;text-align:center}
ul{margin:0 0 12px 20px;font-size:15px}li{margin-bottom:5px}'''

def page(title, desc, canon, body, crumb=""):
    return f'''<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="apple-touch-icon" href="{BASE}/icons/apple-touch-icon.png">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}/icons/icon-512.png"><meta property="og:url" content="{canon}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&family=Baloo+2:wght@600;800&display=swap" rel="stylesheet">
<style>{CSS}</style>{GA}</head><body><div class="wrap">{crumb}{body}
<footer>© <a href="https://tagc.works/">tagc</a> ／ <a href="{BASE}/">えいご シールクイズ</a> ／ <a href="{BASE}/for-parents/">おうちの方へ</a></footer>
</div></body></html>'''

def wtable(ws):
    rows = "".join(f'<tr><td class="en">{w["en"]}</td><td class="kana">{w.get("kana","")}</td><td>{w["ja"]}</td><td class="lv">{LVN[w["level"]][:5]}</td></tr>' for w in ws)
    return f'<table><thead><tr><th>英単語</th><th>読み方</th><th>いみ</th><th>レベル</th></tr></thead><tbody>{rows}</tbody></table>'

for gslug, gname, cats, intro in GROUPS:
    ws = [w for w in WORDS if w["cat"] in cats]
    os.makedirs(f"{ROOT}/words/{gslug}", exist_ok=True)
    title = f"{gname}の英単語{len(ws)}個 一覧｜5歳からの無料クイズで練習"
    desc = f"{gname}に関する英単語{len(ws)}個を意味つきで一覧にしました。{intro[:40]}"
    ex = [w for w in ws if w.get("ex")]
    exhtml = ""
    if ex:
        exhtml = "<h2>例文で覚える</h2><ul>" + "".join(f'<li><b>{w["en"]}</b> … {w["ex"]}</li>' for w in ex[:8]) + "</ul>"
    body = f'''<h1>{gname}の英単語 {len(ws)}個 一覧</h1>
<p>{intro}</p>
<p>カタカナの読み方つきなので、おうちの方が声に出して読んであげられます。この一覧の単語は、そのまま<a href="{BASE}/">えいご シールクイズ</a>で音声つきの4択クイズとして練習できます。読み上げを聞きながら遊べるので、英語の文字が読めない年齢でも取り組めます。</p>
{wtable(ws)}
{exhtml}
<h2>おうちでの覚え方</h2>
<p>いちどに全部は覚えられません。<b>1日5〜10個</b>を目安に、声に出して読むところから始めるのがおすすめです。上の表を見ながら親子で言い合って、そのあとクイズで確認すると定着しやすくなります。</p>
<a class="btn" href="{BASE}/">クイズで {gname} を練習する</a>
<p><a href="{BASE}/words/">ほかのカテゴリの単語一覧を見る</a></p>'''
    crumb = f'<div class="crumb"><a href="{BASE}/">トップ</a> ＞ <a href="{BASE}/words/">単語一覧</a> ＞ {gname}</div>'
    open(f"{ROOT}/words/{gslug}/index.html","w",encoding="utf-8").write(
        page(title, desc, f"{BASE}/words/{gslug}/", body, crumb))

cards = "".join(f'<a href="{BASE}/words/{g}/">{n}<span>{len([w for w in WORDS if w["cat"] in c])}語</span></a>' for g,n,c,_ in GROUPS)
body = f'''<h1>小学生・幼児むけ 英単語一覧（全300語）</h1>
<p>5歳から小学生までに使いやすい英単語300語を、20のカテゴリに分けて一覧にしました。すべて意味つきで、そのまま音声つきの4択クイズとして練習できます。</p>
<h2>レベルの目安</h2>
<ul><li><b>レベル1（5〜6歳）110語</b>：どうぶつ・たべものなど、絵で示せる身近な名詞</li>
<li><b>レベル2（小1〜3）118語</b>：数・曜日・月・天気・気持ち・場所など</li>
<li><b>レベル3（小4〜6）72語</b>：動詞・形容詞・職業・あいさつなど</li></ul>
<h2>カテゴリから探す</h2>
<div class="grid">{cards}</div>
<a class="btn" href="{BASE}/">クイズで練習する</a>
<p><a href="{BASE}/for-parents/">おうちの方へ（使い方と安全性について）</a></p>'''
open(f"{ROOT}/words/index.html","w",encoding="utf-8").write(page(
 "幼児・小学生の英単語一覧300語（意味つき）｜えいご シールクイズ",
 "5歳から小学生までに使う英単語300語を20カテゴリの一覧に。すべて意味つき・音声つきクイズで練習できます。",
 f"{BASE}/words/", body, f'<div class="crumb"><a href="{BASE}/">トップ</a> ＞ 単語一覧</div>'))


# sitemap（ドメイン直下用のものは tag-work.github.io 側にもコピーすること）
urls = [f"{BASE}/", f"{BASE}/for-parents/", f"{BASE}/words/"] + [f"{BASE}/words/{g}/" for g,_,_,_ in GROUPS]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"<url><loc>{u}</loc><changefreq>monthly</changefreq></url>\n" for u in urls) + "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sm)

print(f"単語 {len(WORDS)} 語 / 一覧 {len(GROUPS)} ページ / sitemap {len(urls)} URL を書き出しました")
