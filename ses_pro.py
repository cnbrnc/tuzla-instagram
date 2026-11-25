#!/usr/bin/env python3
"""Sinematik Reels için profesyonel ses: stok müzik + stok efektler + kendi imza seslerimiz.

Kullanım: python3 ses_pro.py <bil|yd|urun|fragman> <müzik kimliği: a–j; assets/ses-kaynak.json> [--taslama] [--yumusak]
Çıktı:    work/ses/pro-<tür>-<varyant>[-taslama][-yumusak].wav (9 sn; yolu yazdırır)

- Müzik ve efekt kaynakları assets/ses-kaynak.json dosyasındadır (Pixabay; ticari kullanım serbest,
  Content ID kaydı olmayanlar). Dosyalar work/muzik/ klasörüne indirilir; depoya konmaz.
- Müzik 120 BPM'e getirilir ve düşüşü tam 4. saniyeye oturtulur: "Bil bakalım"da cevabın, "Yanlış / doğru"da
  DOĞRU damgasının geldiği an. Kesim noktaları şablonlarla aynıdır (reel_bil.html, reel_yd.html).
- İmza seslerimiz kalır: baştaki "tak" vuruşları, doğru cevapta "ding", yanlışta hata sesi, kapanışta "tınn".
- --yumusak: "zor yol / kolay yol" kurgusu için; ilk damgada hata sesi (buzzer) çalmaz.
- --taslama: "Yanlış / doğru" kancasına gerçek taşlama sesi ekler (taş, disk, spiral konularında).
İndirme ya da üretim başarısız olursa 1 koduyla çıkar; reel.py o zaman kodla üretilmiş sese döner.
"""
import json
import os
import subprocess
import sys

import numpy as np
from scipy.io import wavfile

import ses as S
from ses_tur import Mix, buzzer, ding

ROOT = os.path.dirname(os.path.abspath(__file__))
SR, N = S.SR, S.N
KAYNAK = os.path.join(ROOT, "assets", "ses-kaynak.json")
HAM = os.path.join(ROOT, "work", "muzik")
CIKTI = os.path.join(ROOT, "work", "ses")


def yukle(ad, url, tempo=None):
    """mp3'ü indirir, 44,1 kHz mono diziye çevirir (tempo verilirse hızını ayarlar)."""
    os.makedirs(HAM, exist_ok=True)
    mp3 = os.path.join(HAM, ad + ".mp3")
    if not (os.path.exists(mp3) and os.path.getsize(mp3) > 20000):
        subprocess.run(["curl", "-sSL", "-m", "180", "-A", "Mozilla/5.0", "-e", "https://pixabay.com/", "-o", mp3, url], capture_output=True)
    if not (os.path.exists(mp3) and os.path.getsize(mp3) > 20000):
        raise SystemExit("HATA: indirilemedi: " + url)
    wav = os.path.join(HAM, ad + ("-120" if tempo else "") + ".wav")
    af = ["-af", "atempo=%.5f" % tempo] if tempo else []
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3] + af + ["-ar", str(SR), "-ac", "2", wav], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("HATA: ses dosyası okunamadı: " + mp3)
    sr, x = wavfile.read(wav)
    return x.astype(float) / 32768


def main():
    a = sys.argv[1:]
    if len(a) < 2 or a[0] not in ("bil", "yd", "urun", "fragman"):
        raise SystemExit(__doc__)
    tur, varyant, taslama, yumusak = a[0], a[1], "--taslama" in a, "--yumusak" in a
    # --uzat <sn>: uzun sürüm (yalnız fragman). Düşüş T = 4 + uzat saniyesine, kapanış sesleri de o kadar ileri kayar.
    global N
    U = float(a[a.index("--uzat") + 1]) if "--uzat" in a else 0.0
    if U and tur != "fragman":
        raise SystemExit("HATA: --uzat yalnız fragman türünde kullanılır")
    T = 4.0 + U
    N = int(round(SR * (S.DUR + U)))
    import ses_tur
    ses_tur.N = N                                            # Mix dizileri de aynı uzunlukta olsun
    with open(KAYNAK, encoding="utf-8") as f:
        K = json.load(f)
    mz = K["muzik"]
    if varyant in K.get("muzikler", {}):                      # ayrı parça (d, e, f, ...): başlangıç anı dosyada yazılı
        mz = K["muzikler"][varyant]
        oran = 120.0 / mz["bpm"]                              # 120 BPM: vuruş 0,5 sn, çubuk 2 sn
        muzik = yukle("muzik-" + mz["dosya"], mz["url"], tempo=oran)
        bas = mz["bas_sn"] / oran + mz.get("kaydirma", 0.0)
    elif varyant in mz["varyantlar"]:                         # ilk parçanın bölümleri (a, b, c)
        oran = 120.0 / mz["bpm"]
        muzik = yukle("muzik", mz["url"], tempo=oran)
        bas = (mz["faz"] + mz["varyantlar"][varyant] * 4 * 60.0 / mz["bpm"]) / oran + mz.get("kaydirma", {}).get(varyant, 0.0)
    else:
        raise SystemExit("HATA: bilinmeyen müzik kimliği: " + varyant)
    i = int(round((bas - U) * SR))                          # uzun sürümde müzik düşüşten U saniye önce başlar
    if i < 0:
        raise SystemExit("HATA: bu parçada düşüşten önce %g saniye yok; başka müzik seç" % U)
    parca = muzik[i:i + N]
    if len(parca) < N:
        raise SystemExit("HATA: müzik parçası kısa")
    fx = {k: yukle("efekt-" + k, v["url"]) for k, v in K["efektler"].items() if k != "taslama" or taslama}
    vur = {k: v["vurus"] for k, v in K["efektler"].items()}

    stereo = np.zeros((2, N))
    EFEKT = 0.5            # stok efektlerin (vuruş, vuuş, yükseliş) düzeyi: müziğin önüne geçmesin

    def koy(x, at, kazanc=1.0, bas=0.0, sure=None):
        """Stok sesi (stereo) 'at' saniyesine yerleştirir; bas = kaynaktaki başlangıç, sure = en çok süre."""
        seg = x[int(bas * SR):int((bas + sure) * SR) if sure else None]
        i0 = int(round(at * SR))
        if i0 < 0:
            seg, i0 = seg[-i0:], 0
        n = min(len(seg), N - i0)
        if n > 0:
            stereo[:, i0:i0 + n] += seg[:n].T * kazanc * EFEKT

    # müzik: başta ve sonda tık önleme; kapanış kartında biraz geri çekilir
    zarf = np.ones(N)
    k = int(0.01 * SR); zarf[:k] = np.linspace(0, 1, k)
    k = int(0.08 * SR); zarf[-k:] = np.linspace(1, 0, k)
    i7 = int((6.9 + U) * SR); zarf[i7:] *= np.concatenate([np.linspace(1, 0.7, int(0.3 * SR)), np.full(N - i7 - int(0.3 * SR), 0.7)])
    # Müzik öndedir (kullanıcı: "hep aynı melodi"): her parça aynı düzeye getirilir, kendi efektlerimiz geride kalır
    parca = parca * (0.26 / (np.sqrt(np.mean(parca ** 2)) + 1e-9))
    stereo += parca.T * zarf

    m = Mix()                                                  # kendi seslerimiz (ses.py çalgıları)
    note = lambda semi: 440.0 * 2 ** (semi / 12)
    if tur == "bil":
        for at, semi, g in ((0.0, -12, 0.8), (0.25, -5, 0.9)):                 # soru: tak-TAK
            m.put(S.metal_hit(note(semi)), at, g, (at - 0.12) * 1.5, send=0.3)
        m.put(S.sub_boom(), 0.0, 0.7)
        for at, f, p in ((0.5, 520, -0.35), (0.75, 700, 0.35)):                # A ve B
            m.put(S.pop(f), at, 0.6, p, send=0.4)
        for n in range(3):                                                     # geri sayım: saat ve kalp atışı
            at = 1.0 + n
            m.put(S.tink(1500 + 150 * n), at, 0.75, -0.2, send=0.5)
            m.put(S.kick(muffled=True), at, 0.9)
            m.put(S.tink(1200), at + 0.5, 0.35, 0.2, send=0.5)
        koy(fx["riser"], 4.0 - vur["riser"], 0.55)                             # cevaba doğru yükseliş
        koy(fx["hit"], 4.0 - vur["hit"], 0.7)                                  # cevap
        ding(m, note, 4.0)
        for at, f, p in ((4.27, 560, -0.2), (4.77, 640, 0.0), (5.27, 720, 0.2)):
            m.put(S.pop(f), at, 0.45, p, send=0.5)
    elif tur == "fragman":                                                     # film fragmanı (reel_fragman.html)
        koy(fx["hit"], 0.0 - vur["hit"], 0.55)                                 # açılış vuruşu
        m.put(S.sub_boom(), 0.0, 0.8)
        m.put(S.metal_hit(note(-12)), 0.0, 0.7, 0.0, send=0.4)
        for k in range(1, int(T)):                                             # sahne kesimleri: vuuş ve darbe
            at = float(k)
            guclu = U == 0 or k % 2 == 0                                       # uzun sürümde tek saniyeler hafif geçer
            if guclu:
                koy(fx["whoosh"], at - vur["whoosh"], 0.5)
            m.put(S.impact(), at, 0.75 if guclu else 0.4)
            m.put(S.sub_boom(), at, 0.65 if guclu else 0.35)
            m.put(S.kick(muffled=True), at - 0.5, 0.5)
        koy(fx["riser"], T - vur["riser"], 0.65)                               # ürüne doğru yükseliş
        koy(fx["hit"], T - vur["hit"], 0.85)                                   # ürün ortaya çıkar
        m.put(S.hammer(), T, 0.7, send=0.5)
        m.put(S.sub_boom(), T, 0.9)
        m.put(S.pop(520), T + 0.27, 0.45, 0.0, send=0.4)                       # ad
        m.put(S.pop(600), T + 0.52, 0.4, 0.0, send=0.4)                        # tür
        for n, at in enumerate((T + 0.77, T + 1.02, T + 1.27)):                # özellikler
            m.put(S.pop(600 + 80 * n), at, 0.55, -0.3 + 0.3 * n, send=0.45)
            m.put(S.tink(1400 + 150 * n), at, 0.45, 0.2, send=0.5)
        m.put(S.pop(700), T + 1.52, 0.45, 0.0, send=0.5)                       # slogan
    elif tur == "urun":                                                        # ürün tanıtımı (reel_tanitim.html)
        for at, semi, g in ((0.0, -12, 0.8), (0.25, -9, 0.7), (0.5, -5, 0.9)):  # kanca: tak-tak-TAK
            m.put(S.metal_hit(note(semi)), at, g, (at - 0.25) * 1.2, send=0.3)
        m.put(S.sub_boom(), 0.0, 0.7)
        koy(fx["whoosh"], 1.5 - vur["whoosh"], 0.65)                           # ürün fotoğrafı
        m.put(S.impact(), 1.5, 0.75)
        m.put(S.hammer(), 1.5, 0.6, send=0.5)
        m.put(S.sub_boom(), 1.5, 0.7)
        m.put(S.pop(520), 1.77, 0.45, 0.0, send=0.4)                           # başlık
        for n, at in enumerate((2.0, 2.5, 3.0, 3.5)):                          # özellikler: yükselen tık
            m.put(S.pop(560 + 70 * n), at, 0.6, -0.3 + 0.2 * n, send=0.45)
            m.put(S.tink(1400 + 120 * n), at, 0.5, 0.2, send=0.5)
            m.put(S.kick(muffled=True), at, 0.7)
        koy(fx["riser"], 4.0 - vur["riser"], 0.5)                              # rozete doğru yükseliş
        koy(fx["hit"], 4.0 - vur["hit"], 0.7)                                  # rozet
        m.put(S.pop(640), 5.02, 0.5, 0.0, send=0.5)                            # slogan
    else:
        if taslama:
            t = np.arange(int(1.45 * SR)) / SR
            tz = np.minimum(1, t / 0.05) * np.minimum(1, (1.45 - t) / 0.25)
            seg = fx["taslama"][int(vur["taslama"] * SR):int(vur["taslama"] * SR) + len(t)]
            stereo[:, :len(seg)] += (seg * tz[:len(seg), None]).T * 1.6       # kanca: gerçek taşlama sesi
        for at, semi, g in ((0.0, -12, 0.8), (0.25, -9, 0.7), (0.5, -5, 0.9)):  # kanca: tak-tak-TAK
            m.put(S.metal_hit(note(semi)), at, g, (at - 0.25) * 1.2, send=0.3)
        m.put(S.sub_boom(), 0.0, 0.7)
        koy(fx["whoosh"], 1.5 - vur["whoosh"], 0.6)                            # YANLIŞ paneli
        m.put(S.impact(), 1.5, 0.7)
        if not yumusak:
            m.put(buzzer(), 2.0, 0.5, send=0.3)                                # YANLIŞ damgası (zor-kolay kurgusunda çalmaz)
        m.put(S.hammer(), 2.0, 0.7, send=0.5)
        m.put(S.sub_boom(), 2.0, 0.6)
        for at in (2.5, 2.72, 3.0, 3.22):
            m.put(S.kick(muffled=True), at, 0.7 if at in (2.5, 3.0) else 0.45)
        koy(fx["whoosh"], 3.5 - vur["whoosh"], 0.6)                            # DOĞRU paneli
        m.put(S.impact(), 3.5, 0.6)
        koy(fx["hit"], 4.0 - vur["hit"], 0.7)                                  # DOĞRU damgası
        ding(m, note, 4.0)
        m.put(S.pop(600), 5.02, 0.5, 0.0, send=0.5)
    # kapanış kartı: vuuş, imza "tınn", başa saran yükseliş
    koy(fx["whoosh"], 6.85 + U - vur["whoosh"], 0.55)
    m.put(S.clank(), 7.0 + U, 0.55, send=0.7)
    m.put(S.sub_boom(), 7.0 + U, 0.8)
    m.put(S.crash(0.75)[::-1], 8.25 + U, 0.4, send=0.2)
    m.put(S.riser(0.75, 300, 7000), 8.25 + U, 0.45)

    os.makedirs(CIKTI, exist_ok=True)
    gecici = os.path.join(CIKTI, "_bizim.wav")
    m.write(gecici)                                            # kendi seslerimiz: yankılı, tepe 0,89
    sr, biz = wavfile.read(gecici)
    os.remove(gecici)
    mix = stereo + (biz.astype(float) / 32768).T * 0.45
    mix = np.tanh(mix * 0.9) / np.tanh(0.9)
    mix /= np.abs(mix).max() / 0.89
    yol = os.path.join(CIKTI, "pro-%s-%s%s%s%s.wav" % (tur, varyant, "-taslama" if taslama else "", "-yumusak" if yumusak else "", "-u%g" % U if U else ""))
    wavfile.write(yol, SR, (mix.T * 32767).astype(np.int16))
    print(os.path.relpath(yol, ROOT))


if __name__ == "__main__":
    main()
