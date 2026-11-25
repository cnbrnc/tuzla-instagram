#!/usr/bin/env python3
"""Fotoğrafı yavaş kamera hareketiyle kısa bir dikey videoya çevirir (fragman sahnesi olarak kullanmak için).

  python3 foto_sahne.py <foto> <çıktı.mp4> --hf 0.7 --ust 0.25 --sol 0.0 0.3 [--sure 2.5] [--yakin 1.06]

Fragmanda görüntünün yalnız orta bandı görünür (1080×1310; üstte ve altta siyah sinema bantları var).
  --hf    pencerenin yüksekliği, fotoğraf yüksekliğinin oranı olarak (küçükse daha yakın çekim)
  --ust   pencerenin üst kenarı (0–1; fotoğraf yüksekliğine göre)
  --sol   pencerenin sol kenarının başlangıç ve bitiş konumu (0–1; fotoğraf genişliğine göre): yatay kayma
  --yakin süre boyunca hafif yaklaşma (1.0 = yok)
Yazı görünen bandın alt üçte birine gelir; konuyu pencerenin üst yarısında tut.
"""
import subprocess
import sys

from PIL import Image

GW, GH, UST_BANT = 1080, 1310, 250          # görünen bant ve üstteki siyah bant (reel_fragman.html)


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        raise SystemExit(__doc__)
    foto, cikti = a[0], a[1]
    al = lambda ad, n, vars: [float(x) for x in a[a.index(ad) + 1:a.index(ad) + 1 + n]] if ad in a else vars
    hf, ust, sure, yakin = al("--hf", 1, [0.7])[0], al("--ust", 1, [0.15])[0], al("--sure", 1, [2.5])[0], al("--yakin", 1, [1.06])[0]
    sol0, sol1 = al("--sol", 2, [0.0, 0.2])
    W, H = Image.open(foto).size
    ph = H * hf                              # pencere (fotoğraf pikseli)
    pw = ph * GW / GH
    if pw > W or ust * H + ph > H + 1 or max(sol0, sol1) * W + pw > W + 1:
        raise SystemExit("HATA: pencere fotoğrafın dışına taşıyor (pw=%d, W=%d)" % (pw, W))
    # Her kareyi ayrı hesapla: pencere yatayda kayar ve süre boyunca hafifçe küçülür (yaklaşma). Kesirli piksel
    # konumları PIL'in resize(box=...) çağrısıyla örneklenir; hareket titremez.
    im = Image.open(foto).convert("RGB")
    n = int(round(sure * 30))
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx1920" % GW,
                          "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-pix_fmt", "yuv420p",
                          "-an", cikti], stdin=subprocess.PIPE)
    for i in range(n):
        u = i / max(1, n - 1)
        z = 1 + (yakin - 1) * (1 - u)                     # başta geniş, sonda tam pencere
        z = min(z, H / ph, W / pw)                        # pencere fotoğrafın dışına taşmasın
        w, h = pw * z, ph * z
        cx = (sol0 + (sol1 - sol0) * u) * W + pw / 2      # pencere merkezi sabit hızla kayar
        cy = ust * H + ph / 2
        x0 = min(max(cx - w / 2, 0), W - w)
        y0 = min(max(cy - h / 2, 0), H - h)
        kare = im.resize((GW, GH), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h))
        tuval = Image.new("RGB", (GW, 1920), "black")
        tuval.paste(kare, (0, UST_BANT))
        p.stdin.write(tuval.tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise SystemExit("HATA: video yazılamadı")
    print(cikti)


if __name__ == "__main__":
    main()
