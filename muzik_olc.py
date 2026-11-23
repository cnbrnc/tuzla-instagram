#!/usr/bin/env python3
"""Bir müzik dosyasının temposunu, vuruş fazını ve iyi başlangıç çubuklarını ölçer (assets/ses-kaynak.json için).

Kullanım: python3 muzik_olc.py <mp3> [...]
Çıktı: bpm, faz (ilk çubuğun başı, sn), cubuk adayları. Aday = iki sakin çubuktan sonra enerjinin yükseldiği yer:
Reels'te müziğin düşüşü 4. saniyeye (2 çubuk sonrasına) oturur. Gerekli: pip install librosa
"""
import sys
import numpy as np
import librosa


def olc(yol):
    y, sr = librosa.load(yol, sr=22050, mono=True)
    oenv = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, vurus = librosa.beat.beat_track(onset_envelope=oenv, sr=sr, units="time")
    vurus = np.asarray(vurus)
    if len(vurus) < 16:
        return None
    aralik = np.median(np.diff(vurus))
    bpm = 60.0 / aralik
    k = np.arange(len(vurus))                       # düzgün ızgara: en küçük kareler ile faz ve aralık
    A = np.vstack([k, np.ones_like(k)]).T
    aralik, t0 = np.linalg.lstsq(A, vurus, rcond=None)[0]
    bpm = 60.0 / aralik
    t0 = t0 % aralik
    zaman = librosa.times_like(oenv, sr=sr)
    guc = lambda t: float(np.interp(t, zaman, oenv))
    n = int((len(y) / sr - t0) / aralik)
    # çubuk başı: 4 kaymadan vuruş gücü en yüksek olan
    kayma = max(range(4), key=lambda o: sum(guc(t0 + (o + 4 * b) * aralik) for b in range((n - o) // 4)))
    faz = t0 + kayma * aralik
    cubuk = aralik * 4
    nb = int((len(y) / sr - faz) / cubuk)
    E = np.array([np.sqrt(np.mean(y[int((faz + b * cubuk) * sr):int((faz + (b + 1) * cubuk) * sr)] ** 2)) for b in range(nb)])
    med = np.median(E)
    aday = []
    for i in range(0, nb - 5):
        once, sonra = E[i:i + 2].mean(), E[i + 2:i + 5].mean()
        if once > 0.2 * med and sonra > 0.9 * med:
            aday.append((sonra / max(once, 1e-6), i))
    aday.sort(reverse=True)
    return dict(bpm=round(float(bpm), 2), faz=round(float(faz), 3), cubuk_sayisi=nb, oran=round(120.0 / bpm, 3),
                adaylar=[(i, round(float(s), 2)) for s, i in aday[:5]], sure=round(len(y) / sr, 1))


if __name__ == "__main__":
    for f in sys.argv[1:]:
        print(f, olc(f))


def baslangic(yol, n=3):
    """Vuruş ızgarasında, 8 vuruş (4 sn) sonra enerjinin en çok yükseldiği başlangıç anlarını bulur (özgün dosya zamanı)."""
    y, sr = librosa.load(yol, sr=22050, mono=True)
    oenv = librosa.onset.onset_strength(y=y, sr=sr)
    _, vurus = librosa.beat.beat_track(onset_envelope=oenv, sr=sr, units="time")
    vurus = np.asarray(vurus)
    k = np.arange(len(vurus))
    aralik, t0 = np.linalg.lstsq(np.vstack([k, np.ones_like(k)]).T, vurus, rcond=None)[0]
    t0 = t0 % aralik
    rms = lambda a, b: float(np.sqrt(np.mean(y[int(a * sr):int(b * sr)] ** 2) + 1e-12))
    genel = rms(0, len(y) / sr)
    out = []
    for i in range(int((len(y) / sr - t0) / aralik) - 19):
        s = t0 + i * aralik
        once, sonra = rms(s, s + 8 * aralik), rms(s + 8 * aralik, s + 13 * aralik)
        kenar = rms(s + 8 * aralik, s + 9 * aralik) / rms(s + 7 * aralik, s + 8 * aralik)
        if once > 0.45 * genel and sonra > 0.9 * genel:    # baş da duyulur olsun: parça ilk saniyeden tanınsın
            out.append(((sonra / once) * np.sqrt(kenar), round(float(s), 3), round(sonra / once, 2), round(kenar, 2)))
    out.sort(reverse=True)
    secilen = []
    for o in out:                                   # birbirine yakın adayları ele
        if all(abs(o[1] - x[1]) > 6 for x in secilen):
            secilen.append(o)
        if len(secilen) == n:
            break
    return dict(bpm=round(60.0 / float(aralik), 2), adaylar=[dict(bas_sn=o[1], oran=o[2], kenar=o[3]) for o in secilen])


if __name__ == "__main__" and "--bas" in sys.argv:
    for f in [a for a in sys.argv[1:] if not a.startswith("--")]:
        print("BAS", f, baslangic(f))
