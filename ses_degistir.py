#!/usr/bin/env python3
"""Üretilmiş bir Reels'in yalnız sesini değiştirir (görüntü aynen kalır).

Kullanım: python3 ses_degistir.py <video.mp4> <tür: bil|yd|urun|fragman> <müzik kimliği> <çıktı.mp4> [--taslama] [--yumusak]
"""
import os, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
video, tur, kimlik, cikti = sys.argv[1:5]
r = subprocess.run([sys.executable, os.path.join(ROOT, "ses_pro.py"), tur, kimlik] + sys.argv[5:], capture_output=True, text=True, cwd=ROOT)
if r.returncode != 0:
    raise SystemExit("HATA: ses üretilemedi: " + (r.stderr or r.stdout)[-300:])
wav = os.path.join(ROOT, r.stdout.strip().splitlines()[-1])
os.makedirs(os.path.dirname(os.path.abspath(cikti)), exist_ok=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-map", "0:v", "-c:v", "copy", "-map", "1:a",
                "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "160k", "-t", "9", "-movflags", "+faststart", cikti], check=True)
print("ok", cikti, kimlik)
