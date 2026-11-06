#!/usr/bin/env python3
"""Reels için 9 saniyelik özgün ses izi (telifsiz, tamamen kodla üretilir). 2. sürüm: izleyiciyi tutmak için.

Zamanlama templates/reel.html ile aynıdır (120 BPM, vuruş 0,5 sn):
  0,00 / 0,25 / 0,50  kanca satırları çarparak gelir -> "tak-tak-TAK" metal vuruşlar (ilk karede ses var)
  0,5 – 1,75          kanca ekranda                 -> gerilim: boğuk ritim, trampet ya da cırcır, yükselen ses
  1,75 – 2,0          ürün paneli gelir            -> "vuuş" ve kısa nefes
  2,00                ürün                          -> düşüş: ritim, bas ve akılda kalan melodi başlar
  2,50                başlık                        -> tok vuruş
  3,00 / 3,50         ürüne yakınlaşma vuruşları    -> vurgu
  4,0 / 4,5 / 5,0     çipler                        -> "pıt" sesleri
  6,00                üründe parlama                -> metalik "şing"
  6,75 – 7,0          kapanış kartı                 -> "vuuş" ve metal "tınn"
  7,0 – 9,0           kapanış                       -> melodi bir kez daha; sonda başa saran yükseliş.
                                                       Video döngüde kesintisiz yeniden başlar.

Ritimler (imza sesleri hepsinde aynı): enerjik, atolye, derin.
  --efekt : ritim, bas ve melodi olmadan yalnız efektler (Instagram müziği eklenecek Reels için).
Kullanım: python3 ses.py <çıktı.wav> [--ritim enerjik|atolye|derin] [--efekt]
Tohum sabit; her çalıştırmada aynı ses çıkar. reel.html zamanları değişirse buradakileri de güncelle.
"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, istft, sosfilt, stft

SR = 44100
DUR = 9.0
N = int(SR * DUR)
rng = np.random.default_rng(11)

RITIMLER = {
    # kok: A minörden yarım ses kaydırma; kurgu: gerilim türü; takim: perküsyon; lead: melodi sesi; groove: ritim
    "enerjik": {"kok": 0, "kurgu": "trampet", "takim": "klasik", "lead": "pluck", "groove": "dort"},
    "atolye": {"kok": -2, "kurgu": "circir", "takim": "atolye", "lead": "bell", "groove": "dort"},
    "derin": {"kok": -7, "kurgu": "trampet", "takim": "klasik", "lead": "pluck", "groove": "yarim"},
}


# --- temel araçlar ---

def tt(d):
    return np.arange(int(SR * d)) / SR


def filt(x, kind, f, order=2):
    return sosfilt(butter(order, f, btype=kind, fs=SR, output="sos"), x)


def noise(d):
    return rng.standard_normal(int(SR * d))


def sweep_noise(d, f0, f1, width=0.6):
    n = noise(d)
    f, frames, Z = stft(n, fs=SR, nperseg=1024, noverlap=768)
    fc = f0 * (f1 / f0) ** np.clip(frames / d, 0, 1)
    lf = np.log2(np.maximum(f, 1))[:, None]
    mask = np.exp(-0.5 * ((lf - np.log2(fc)[None, :]) / width) ** 2)
    _, y = istft(Z * mask, fs=SR, nperseg=1024, noverlap=768)
    y = y[: int(SR * d)]
    return y / (np.abs(y).max() + 1e-9)


def bell(n, peak=0.6, a=2.0, b=1.5):
    x = np.linspace(0, 1, n)
    return np.where(x < peak, (x / peak) ** a, ((1 - x) / (1 - peak)) ** b)


def saw(f, t, ph=0.0):
    return 2 * ((f * t + ph) % 1) - 1


# --- vurmalılar ---

def kick(muffled=False):
    t = tt(0.35)
    body = np.sin(2 * np.pi * np.cumsum(48 + 110 * np.exp(-t / 0.03)) / SR) * np.exp(-t / 0.15)
    click = filt(noise(0.35), "highpass", 2500) * np.exp(-t / 0.004) * 0.25
    s = body + click
    return filt(s, "lowpass", 260) * 1.3 if muffled else s


def sub_boom():
    t = tt(0.9)
    return np.sin(2 * np.pi * np.cumsum(45 + 50 * np.exp(-t / 0.08)) / SR) * np.exp(-t / 0.45)


def hat(length=0.015):
    t = tt(0.08)
    return filt(noise(0.08), "highpass", 7500, 4) * np.exp(-t / length) * 0.35


def clap():
    t = tt(0.25)
    n = filt(noise(0.25), "bandpass", [900, 3800])
    e = np.exp(-t / 0.07) * 0.6
    for k, o in enumerate((0.0, 0.011, 0.022)):
        i = int(o * SR)
        e[i:] += np.exp(-t[: len(t) - i] / 0.007) * (0.5 if k < 2 else 0.9)
    return n * e * 0.45


def snare(tone=200):
    t = tt(0.3)
    n = filt(noise(0.3), "bandpass", [1000, 7000]) * np.exp(-t / 0.1) * 0.55
    return n + np.sin(2 * np.pi * tone * t) * np.exp(-t / 0.05) * 0.5


def crash(d=1.2):
    t = tt(d)
    return filt(noise(d), "highpass", 5000, 2) * np.exp(-t / 0.5) * 0.5


def shaker():
    t = tt(0.09)
    return filt(noise(0.09), "bandpass", [5000, 12000]) * np.minimum(1, t / 0.01) * np.exp(-t / 0.03) * 0.35


def tink(f=3200):
    t = tt(0.12)
    s = (np.sin(2 * np.pi * f * t) + 0.6 * np.sin(2 * np.pi * f * 1.47 * t) + 0.4 * np.sin(2 * np.pi * f * 2.09 * t)) * np.exp(-t / 0.03)
    return s * 0.35 + filt(noise(0.12), "highpass", 4000) * np.exp(-t / 0.004) * 0.3


def hammer():
    t = tt(0.5)
    s = sum(a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) * np.exp(-t / tau)
            for f, a, tau in ((310, 1.0, 0.12), (742, 0.6, 0.08), (1290, 0.4, 0.06), (2110, 0.3, 0.04)))
    thud = np.sin(2 * np.pi * np.cumsum(60 + 80 * np.exp(-t / 0.02)) / SR) * np.exp(-t / 0.1)
    nz = filt(noise(0.5), "bandpass", [800, 5000]) * np.exp(-t / 0.02) * 0.5
    return (s * 0.5 + thud * 0.7 + nz) * 0.8


def metal_hit(f):
    """Kancadaki 'tak' vuruşu: kısa metal tını + gürültü."""
    t = tt(0.6)
    s = sum(a * np.sin(2 * np.pi * f * m * t + rng.uniform(0, 6.28)) * np.exp(-t / tau)
            for m, a, tau in ((1.0, 1.0, 0.16), (2.32, 0.6, 0.1), (3.87, 0.4, 0.07), (5.4, 0.25, 0.05)))
    nz = filt(noise(0.6), "bandpass", [1500, 9000]) * np.exp(-t / 0.012) * 0.8
    return s * 0.55 + nz


def clank():
    """İmza: örse vurulmuş gibi metal 'tınn'."""
    t = tt(1.6)
    s = sum(a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) * np.exp(-t / tau)
            for f, a, tau in ((523, 1.0, 0.55), (529, 0.7, 0.5), (1187, 0.6, 0.35), (1931, 0.45, 0.28),
                              (2756, 0.35, 0.2), (3620, 0.25, 0.15), (4870, 0.18, 0.1), (6230, 0.12, 0.07)))
    return s * 0.45 + filt(noise(1.6), "highpass", 2500) * np.exp(-t / 0.008) * 0.9


def shing():
    """Üründe parlama: yukarı kayan metalik ışıltı."""
    d = 0.7
    t = tt(d)
    sw = sweep_noise(d, 2500, 12000, width=0.5) * bell(int(SR * d), 0.35) * 0.6
    ring = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / 0.25) for f, a in ((4186, 0.5), (5274, 0.35), (6644, 0.25)))
    return sw[: len(t)] + ring * np.minimum(1, t / 0.02) * 0.5


def pop(f):
    t = tt(0.14)
    return np.sin(2 * np.pi * np.cumsum(f * (1 + 0.9 * np.exp(-t / 0.012))) / SR) * np.exp(-t / 0.04)


def impact(gain_noise=0.35):
    t = tt(0.7)
    low = np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-t / 0.05)) / SR) * np.exp(-t / 0.28)
    return low + filt(noise(0.7), "lowpass", 1500) * np.exp(-t / 0.06) * gain_noise


def riser(d, f0=250, f1=7000):
    n = sweep_noise(d, f0, f1, width=0.8)
    e = np.linspace(0, 1, len(n)) ** 2.0
    t = tt(d)[: len(n)]
    tone = np.sin(2 * np.pi * np.cumsum(180 + 600 * (t / d) ** 2) / SR) * 0.25 * (t / d)
    return (n * 0.6 + tone) * e


def ratchet(d, r0=10, r1=32):
    out = np.zeros(int(SR * d))
    t = 0.0
    while t < d - 0.03:
        frac = t / d
        click = tink(2600 + 800 * rng.uniform())[: int(0.03 * SR)] * (0.45 + 0.55 * frac)
        i = int(t * SR)
        j = min(len(out), i + len(click))
        out[i:j] += click[: j - i]
        t += 1.0 / (r0 + (r1 - r0) * frac ** 1.4)
    return out


# --- ezgili sesler ---

def bass(freq, d=0.23, drive=False):
    t = tt(d)
    s = saw(freq, t) * 0.5 + np.sin(2 * np.pi * freq * t) * 0.9
    if drive:
        s = np.tanh(2.2 * s)
    return filt(s, "lowpass", 1000 if drive else 750) * np.minimum(1, t / 0.004) * np.exp(-t / 0.18)


def long_bass(freq, d):
    t = tt(d)
    s = filt(saw(freq, t) * 0.5 + np.sin(2 * np.pi * freq * t) * 0.9, "lowpass", 900)
    return s * np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.05)


def pluck(f, d=0.26):
    t = tt(d)
    w = saw(f, t) + saw(f * 1.005, t, 0.3)
    s = filt(w, "lowpass", 4200) * np.exp(-t / 0.05) + filt(w, "lowpass", 900) * np.exp(-t / 0.2)
    return s * np.minimum(1, t / 0.003) * 0.45


def bell_lead(f, d=0.35):
    t = tt(d)
    mod = 2.2 * np.exp(-t / 0.25) * np.sin(2 * np.pi * f * 1.4 * t)
    return np.sin(2 * np.pi * f * t + mod) * np.exp(-t / 0.3) * np.minimum(1, t / 0.003) * 0.5


def chord(freqs, d, cutoff=1500, attack=0.05, decay=3.0):
    t = tt(d)
    out = np.zeros(len(t))
    for f in freqs:
        for det in (-0.003, 0.0, 0.003):
            out += saw(f * (1 + det), t, rng.uniform(0, 1))
    out = filt(out, "lowpass", cutoff) / (3 * len(freqs))
    return out * np.minimum(1, t / attack) * np.minimum(1, (d - t) / 0.1) * np.exp(-t / decay)


def main():
    out_path = sys.argv[1]
    efekt = "--efekt" in sys.argv[2:]
    adi = sys.argv[sys.argv.index("--ritim") + 1] if "--ritim" in sys.argv else "enerjik"
    if adi not in RITIMLER:
        raise SystemExit("bilinmeyen ritim: " + adi)
    R = RITIMLER[adi]
    tr = 2 ** (R["kok"] / 12)
    note = lambda semi: 440.0 * tr * 2 ** (semi / 12)         # 0 = La4 (kaydırılmış)
    dry = np.zeros((2, N))
    wet = np.zeros((2, N))

    def put(sig, at, gain=1.0, pan=0.0, send=0.0):
        i = int(round(at * SR))
        j = min(N, i + len(sig))
        if j <= i:
            return
        s = sig[: j - i] * gain
        th = (pan + 1) * np.pi / 4
        l, r = np.sqrt(2) * np.cos(th), np.sqrt(2) * np.sin(th)
        dry[0, i:j] += s * l
        dry[1, i:j] += s * r
        if send:
            wet[0, i:j] += s * l * send
            wet[1, i:j] += s * r * send

    muzik = not efekt

    # 1) Kanca: ilk karede ses. Üç satır = tak, tak, TAK
    for at, semi, g in ((0.0, -12, 0.9), (0.25, -9, 0.8), (0.5, -5, 1.0)):
        put(metal_hit(note(semi)), at, g, (at - 0.25) * 1.2, send=0.25)
        if muzik:
            put(kick(), at, 0.9 if at != 0.25 else 0.55)
    if muzik:
        put(sub_boom(), 0.0, 0.6)

    # 2) Gerilim (0,5 – 1,75)
    if muzik:
        for at in (1.0, 1.5):
            put(kick(muffled=True), at, 0.8)
        if R["kurgu"] == "circir":
            put(ratchet(1.2), 0.55, 0.5, 0.2, send=0.15)
        else:
            for k, at in enumerate((1.0, 1.25, 1.5, 1.625)):
                put(snare(190 + 25 * k), at, 0.35 + 0.15 * k, send=0.2)
    put(riser(1.25), 0.5, 0.45)
    put(sweep_noise(0.45, 500, 6000) * bell(int(SR * 0.45), 0.85), 1.55, 0.6, send=0.2)

    # 3) Düşüş (2,0): ürün geldi
    put(impact(), 2.0, 0.6)
    if muzik:
        put(kick(), 2.0, 1.0)
        put(sub_boom(), 2.0, 0.7)
        put(crash(), 2.0, 0.5, send=0.3)

    if muzik:
        chords = [(2.0, 4.0, (0, 3, 7)), (4.0, 5.0, (-4, 0, 3)), (5.0, 6.0, (-2, 2, 5)), (6.0, 7.0, (-5, -2, 2)), (7.0, 9.0, (0, 3, 7))]
        roots = [(2.0, 4.0, -24), (4.0, 5.0, -28), (5.0, 6.0, -26), (6.0, 7.0, -29), (7.0, 8.25, -24)]
        for a, b, c in chords:                                # alçak sesli akor zemini
            put(chord([note(s - 12) for s in c], b - a, cutoff=1300, decay=4.0), a, 0.14, send=0.4)

        if R["groove"] == "dort":
            for k in range(10):                              # 2,0 – 6,5 dört vuruş
                put(kick(), 2.0 + 0.5 * k, 0.9)
            for at in (3.75, 5.75):
                put(kick(), at, 0.6)
            for k in range(40):                              # on altılık hihat
                at = 2.0 + 0.125 * k
                acc = k % 4 == 2
                if R["takim"] == "atolye":
                    if acc:
                        put(tink(3000 + 250 * (k % 3)), at, 0.5, 0.35 if k % 8 == 2 else -0.35, send=0.15)
                else:
                    put(hat(0.022 if acc else 0.008), at, 0.75 if acc else 0.32, 0.2 if k % 2 else -0.2)
            for at in (2.5, 3.5, 4.5, 5.5, 6.5):
                if R["takim"] == "atolye":
                    put(hammer(), at, 0.75, send=0.3)
                else:
                    put(clap(), at, 0.85, send=0.25)
                    put(snare(), at, 0.35)
            for a, b, s in roots[:4]:                        # sekizlik bas, ara sekizlik oktav
                k = 0
                while a + 0.25 * k < b - 0.01:
                    put(bass(note(s) * (2 if k % 2 else 1), drive=R["takim"] == "atolye"), a + 0.25 * k, 0.5 if k % 2 else 0.72)
                    k += 1
        else:                                                # yarım tempo (derin)
            for at in (2.0, 2.75, 4.0, 4.75, 6.0, 6.75):
                put(kick(), at, 0.9 if at in (2.0, 4.0, 6.0) else 0.55)
            for at in (3.0, 5.0):
                put(snare(170), at, 0.75, send=0.35)
                put(clap(), at, 0.5, send=0.3)
            for k in range(20):
                at = 2.0 + 0.25 * k
                put(shaker(), at, 0.5 if k % 2 else 0.3, 0.3 if k % 2 else -0.3)
            for a, b, s in roots[:4]:
                put(long_bass(note(s), b - a), a, 0.62)

        # akılda kalan melodi (sekizlikler; None = es)
        lead = pluck if R["lead"] == "pluck" else bell_lead
        octave = -12 if R["groove"] == "yarim" else 0
        motif = [(2.0, [7, None, 7, 5, 3, None, 0, None]), (4.0, [3, None, 3, 0]), (5.0, [2, None, 2, 5]), (6.0, [7, None, 5, 2])]
        for a, seq in motif:
            for k, s in enumerate(seq):
                if s is not None:
                    put(lead(note(s + octave)), a + 0.25 * k, 0.5, 0.15 if k % 2 else -0.15, send=0.35)

    # 4) Başlık, yakınlaşma, çipler, parlama
    put(impact(0.25), 2.5, 0.45)
    if muzik:
        put(impact(0.2), 3.0, 0.35)
        put(snare(), 3.5, 0.3, send=0.3)
    for at, f, p in ((4.02, 700, -0.2), (4.52, 830, 0.0), (5.02, 960, 0.2)):
        put(pop(f * tr ** 0.25), at, 0.6, p, send=0.35)
    put(shing(), 5.95, 0.4, 0.2, send=0.4)

    # 5) Kapanış kartı (7,0) ve başa saran yükseliş
    put(sweep_noise(0.4, 300, 6500) * bell(int(SR * 0.4), 0.8), 6.62, 0.6, send=0.2)
    put(clank(), 7.0, 0.6, send=0.5)
    if muzik:
        put(kick(), 7.0, 0.95)
        put(crash(), 7.0, 0.4, send=0.3)
        put(long_bass(note(-24), 1.25), 7.0, 0.55)
        if R["groove"] == "dort":
            for at in (7.5, 8.0):
                put(kick(), at, 0.7)
        for k in range(10):
            put(hat(0.02), 7.25 + 0.125 * k * 2, 0.4, 0.2 if k % 2 else -0.2)
        for k, s in enumerate([7, None, 7, 5, 3, None, 0, None]):      # melodi bir kez daha, kısık
            if s is not None:
                put(lead(note(s + octave)), 7.0 + 0.25 * k, 0.32, send=0.4)
        rev = crash(0.75)[::-1]                                       # ters zil: başa çekiş
        put(rev, 8.25, 0.55, send=0.1)
        if R["kurgu"] == "circir":
            put(ratchet(0.75, 14, 36), 8.25, 0.45, -0.2)
        else:
            for k in range(6):
                put(snare(200 + 20 * k), 8.25 + 0.125 * k, 0.25 + 0.08 * k)
    put(riser(0.75, 400, 8000), 8.25, 0.5)

    # yankı
    ir_t = tt(1.4)
    ir = np.stack([filt(rng.standard_normal(len(ir_t)), "lowpass", 5000) * np.exp(-ir_t / 0.4) for _ in range(2)])
    ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
    rev = np.stack([fftconvolve(wet[c], ir[c])[:N] for c in range(2)]) * 0.3

    mix = dry + rev
    mix = np.stack([filt(mix[c], "highpass", 30) for c in range(2)])
    edge = int(0.006 * SR)                                   # yalnız tık önleme; sonda kısılma yok (döngü)
    mix[:, :edge] *= np.linspace(0, 1, edge)
    mix[:, -edge:] *= np.linspace(1, 0, edge)
    mix = np.tanh(mix * 0.9) / np.tanh(0.9)
    mix /= np.abs(mix).max() / 0.89
    wavfile.write(out_path, SR, (mix.T * 32767).astype(np.int16))
    print("ok", out_path)


if __name__ == "__main__":
    main()
