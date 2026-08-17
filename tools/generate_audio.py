#!/usr/bin/env python3
"""
300語の読み上げmp3を一括生成する。
  python3 tools/generate_audio.py --engine say      # macOS内蔵（無料・オフライン）
  python3 tools/generate_audio.py --engine openai   # OpenAI TTS（高品質・約8円）
出力: audio/<単語>.mp3（24kbps モノラル）
ffmpeg が必要: brew install ffmpeg
"""
import json, os, re, subprocess, argparse, sys

ap = argparse.ArgumentParser()
ap.add_argument("--engine", choices=["say", "openai"], default="say")
ap.add_argument("--voice", default=None)
ap.add_argument("--force", action="store_true", help="既存ファイルも作り直す")
a = ap.parse_args()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORDS = json.load(open(os.path.join(ROOT, "data/words.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "audio"); os.makedirs(OUT, exist_ok=True)
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def to_mp3(src, dst):
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",src,
                    "-ac","1","-ar","24000","-b:a","24k",dst], check=True)

def gen_say(text, dst, voice):
    tmp = dst + ".aiff"
    subprocess.run(["say","-v",voice,"-r","150","-o",tmp,text], check=True)
    to_mp3(tmp, dst); os.remove(tmp)

def gen_openai(text, dst, voice):
    from openai import OpenAI            # pip install openai
    client = OpenAI()                    # 環境変数 OPENAI_API_KEY を使用
    tmp = dst + ".src.mp3"
    with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts", voice=voice, input=text, speed=0.9) as r:
        r.stream_to_file(tmp)
    to_mp3(tmp, dst); os.remove(tmp)

voice = a.voice or ("Samantha" if a.engine == "say" else "nova")
made = skipped = 0
for w in WORDS:
    dst = os.path.join(OUT, slug(w["en"]) + ".mp3")
    if os.path.exists(dst) and not a.force:
        skipped += 1; continue
    try:
        (gen_say if a.engine == "say" else gen_openai)(w["en"], dst, voice)
        made += 1
        print(f"  {made:3d}  {w['en']}")
    except Exception as e:
        print("  FAILED:", w["en"], e, file=sys.stderr)

total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT) if f.endswith(".mp3"))
print(f"\n生成 {made} / スキップ {skipped} / 合計 {total/1024/1024:.2f} MB")
