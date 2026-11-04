#!/usr/bin/env python3
"""Onaya sunmak için önizleme görselleri üretir.

Kullanım: python3 onizleme.py <hafta.json> <çıktı_klasörü>

- Kaydırmalı gönderi: <id>-01.png, <id>-02.png ... dosyalarını tek görselde yan yana dizer -> <id>-onizleme.png
- Reels: <id>.mp4 videosundan 4 kare alır (1., 3,5., 6. ve 8,5. saniye) -> <id>-kareler.png
Tek görselli gönderiler için önizleme gerekmez; PNG'nin kendisi gönderilir.
Önizleme dosyaları yalnız onay içindir; depoya yüklenmez.
"""
import glob
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image

THUMB_W, THUMB_H, GAP, COLS = 432, 540, 12, 4


def sheet(images, thumb_w, thumb_h, cols, out_path):
    rows = (len(images) + cols - 1) // cols
    ncols = min(cols, len(images))
    canvas = Image.new("RGB", (ncols * thumb_w + (ncols - 1) * GAP, rows * thumb_h + (rows - 1) * GAP), (255, 255, 255))
    for i, im in enumerate(images):
        canvas.paste(im.convert("RGB").resize((thumb_w, thumb_h)), ((i % cols) * (thumb_w + GAP), (i // cols) * (thumb_h + GAP)))
    canvas.save(out_path)
    print("ok", out_path)


def main():
    spec_path, out = sys.argv[1], os.path.abspath(sys.argv[2])
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    for post in spec["posts"]:
        pid = post["id"]
        if post.get("slides"):
            files = sorted(glob.glob(os.path.join(out, pid + "-[0-9][0-9].png")))
            if not files:
                print("UYARI: slayt bulunamadı:", pid)
                continue
            sheet([Image.open(p) for p in files], THUMB_W, THUMB_H, COLS, os.path.join(out, pid + "-onizleme.png"))
        elif post.get("template") == "reel":
            mp4 = os.path.join(out, pid + ".mp4")
            if not os.path.exists(mp4):
                print("UYARI: video bulunamadı:", pid)
                continue
            frames = []
            with tempfile.TemporaryDirectory() as tmp:
                for k, sec in enumerate((1.0, 3.5, 6.0, 8.5)):
                    jpg = os.path.join(tmp, "k%d.jpg" % k)
                    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(sec), "-i", mp4,
                                    "-frames:v", "1", jpg], check=True)
                    frames.append(Image.open(jpg).copy())
            sheet(frames, 360, 640, 4, os.path.join(out, pid + "-kareler.png"))


if __name__ == "__main__":
    main()
