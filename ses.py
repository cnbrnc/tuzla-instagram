#!/usr/bin/env python3
"""Reels için 10 saniyelik özgün ses izi (telifsiz, tamamen kodla üretilir).

Zamanlama templates/reel.html animasyonlarıyla aynıdır:
  0,05 / 0,20 / 0,35 sn  kanca satırları   -> üç kısa "tık"
  0,1 – 1,9 sn           kanca ekranda     -> yükselen gerilim
  1,9 – 2,5 sn           ürün paneli gelir -> "vuuş" ve ritim başlar
  2,6 sn                 başlık            -> tok vuruş
  4,4 / 4,9 / 5,4 sn     çipler            -> üç "pıt" (vuruşla aynı anda)
  7,2 – 7,7 sn           kapanış kartı     -> "vuuş" ve metal "tınn"
  7,7 – 10 sn            kapanış           -> akor, sönerek biter

Kullanım: python3 ses.py <çıktı.wav> [--efekt]
  --efekt : ritim, bas ve akor olmadan yalnız efektler. Facebook bağlantısıyla Instagram müziği
            eklenecek Reels'te kullanılır; böylece efektler müzikle çakışmaz.

Kullanıcı 5 Kasım 2026'da tam sürümü onayladı. Tohum (seed) sabit olduğu için her çalıştırmada aynı ses çıkar.
reel.html'deki animasyon zamanları değişirse buradaki zamanları da güncelle ve assets/ altındaki dosyaları yeniden üret:
  python3 ses.py assets/reel-ses.wav && python3 ses.py assets/reel-ses-efekt.wav --efekt
"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, istft, sosfilt, stft

SR = 44100
DUR = 10.0
N = int(SR * DUR)
rng = np.random.default_rng(7)


def tt(d):
    return np.arange(int(SR * d)) / SR


def filt(x, kind, f, order=2):
    return sosfilt(butter(order, f, btype=kind, fs=SR, output="sos"), x)


def sweep_noise(d, f0, f1, width=0.6):
    """Merkez frekansı f0'dan f1'e kayan gürültü (vuuş sesi)."""
    n = rng.standard_normal(int(SR * d))
    f, frames, Z = stft(n, fs=SR, nperseg=1024, noverlap=768)
    frac = np.clip(frames / d, 0, 1)
    fc = f0 * (f1 / f0) ** frac
    lf = np.log2(np.maximum(f, 1))[:, None]
    mask = np.exp(-0.5 * ((lf - np.log2(fc)[None, :]) / width) ** 2)
    _, y = istft(Z * mask, fs=SR, nperseg=1024, noverlap=768)
    y = y[: int(SR * d)]
    return y / (np.abs(y).max() + 1e-9)


def bell(n, peak=0.6, a=2.0, b=1.5):
    x = np.linspace(0, 1, n)
    return np.where(x < peak, (x / peak) ** a, ((1 - x) / (1 - peak)) ** b)


def kick():
    t = tt(0.35)
    f = 48 + 110 * np.exp(-t / 0.03)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.15)
    click = filt(rng.standard_normal(len(t)), "highpass", 2500) * np.exp(-t / 0.004) * 0.25
    return body + click


def hat(length=0.015):
    t = tt(0.08)
    return filt(rng.standard_normal(len(t)), "highpass", 7500, 4) * np.exp(-t / length) * 0.35


def clap():
    t = tt(0.25)
    n = filt(rng.standard_normal(len(t)), "bandpass", [900, 3800])
    e = np.exp(-t / 0.07) * 0.6
    for k, o in enumerate((0.0, 0.011, 0.022)):
        i = int(o * SR)
        e[i:] += np.exp(-t[: len(t) - i] / 0.007) * (0.5 if k < 2 else 0.9)
    return n * e * 0.45


def bass(freq, d=0.23):
    t = tt(d)
    saw = 2 * ((freq * t) % 1) - 1
    s = filt(saw * 0.45 + np.sin(2 * np.pi * freq * t) * 0.9, "lowpass", 700)
    return s * np.minimum(1, t / 0.004) * np.exp(-t / 0.18)


def tick(f):
    t = tt(0.07)
    s = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * f * 2.01 * t)
    return s * np.exp(-t / 0.013) * 0.6


def pop(f):
    t = tt(0.14)
    fr = f * (1 + 0.9 * np.exp(-t / 0.012))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.04)


def impact():
    t = tt(0.7)
    low = np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-t / 0.05)) / SR) * np.exp(-t / 0.28)
    nz = filt(rng.standard_normal(len(t)), "lowpass", 1500) * np.exp(-t / 0.06) * 0.35
    return low + nz


def clank():
    """Örs ya da çelik parçaya vurulmuş gibi metalik 'tınn'."""
    t = tt(1.8)
    partials = [(523, 1.0, 0.55), (529, 0.7, 0.5), (1187, 0.6, 0.35), (1931, 0.45, 0.28),
                (2756, 0.35, 0.2), (3620, 0.25, 0.15), (4870, 0.18, 0.1), (6230, 0.12, 0.07)]
    s = sum(a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) * np.exp(-t / tau) for f, a, tau in partials)
    hit = filt(rng.standard_normal(len(t)), "highpass", 2500) * np.exp(-t / 0.008) * 0.9
    return s * 0.45 + hit


def riser(d):
    n = sweep_noise(d, 250, 6000, width=0.8)
    e = np.linspace(0, 1, len(n)) ** 2.2
    t = tt(d)[: len(n)]
    tone = np.sin(2 * np.pi * np.cumsum(170 + 520 * (t / d) ** 2) / SR) * 0.25 * (t / d)
    return (n * 0.55 + tone) * e


def pad(d):
    t = tt(d)
    out = np.zeros(len(t))
    for f in (220.0, 261.63, 329.63, 493.88):          # La minör (add9)
        for det in (-0.004, 0.0, 0.004):
            ph = rng.uniform(0, 1)
            out += 2 * (((f * (1 + det)) * t + ph) % 1) - 1
    out = filt(out, "lowpass", 1800) / 12
    env = np.minimum(1, t / 0.25) * np.exp(-t / 2.2)
    return out * env


def main():
    out_path = sys.argv[1]
    efekt = "--efekt" in sys.argv[2:]
    dry = np.zeros((2, N))
    wet = np.zeros((2, N))

    def put(sig, at, gain=1.0, pan=0.0, send=0.0):
        i = int(at * SR)
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

    # 1. sahne: kanca
    for at, f, p in ((0.06, 1300, -0.3), (0.21, 1500, 0.0), (0.36, 1700, 0.3)):
        put(tick(f), at, 0.55, p, send=0.4)
    put(riser(1.85), 0.1, 0.45)

    # geçiş: panel gelir
    put(sweep_noise(0.75, 400, 5000) * bell(int(SR * 0.75), 0.55), 1.75, 0.6, send=0.2)

    # 2. sahne: ritim (120 BPM, vuruş = 0,5 sn)
    if not efekt:
        for k in range(10):                              # 2,0 – 6,5 sn
            put(kick(), 2.0 + 0.5 * k, 0.9)
        for k in range(20):
            at = 2.25 + 0.25 * k
            if at < 7.15:
                put(hat(0.03 if k % 2 else 0.015), at, 0.9 if k % 2 else 0.6, 0.25 if k % 2 else -0.25)
        for at in (2.5, 3.5, 4.5, 5.5, 6.5):
            put(clap(), at, 0.8, send=0.25)
        notes = [110.0] * 8 + [87.31] * 4 + [98.0] * 4 + [82.41] * 4  # La, Fa, Sol, Mi
        for k, f in enumerate(notes):                     # sekizlik bas, 2,0 – 7,0 sn
            put(bass(f), 2.0 + 0.25 * k, 0.75 if k % 2 == 0 else 0.5)
    put(impact(), 2.62, 0.55)

    # çipler
    for at, f, p in ((4.48, 700, -0.2), (4.98, 830, 0.0), (5.48, 960, 0.2)):
        put(pop(f), at, 0.6, p, send=0.35)

    # 3. sahne: kapanış kartı
    put(sweep_noise(0.6, 300, 6500) * bell(int(SR * 0.6), 0.7), 6.95, 0.6, send=0.2)
    if not efekt:
        put(kick(), 7.62, 0.9)
    put(clank(), 7.62, 0.6, send=0.5)
    if not efekt:
        put(pad(2.4), 7.62, 0.55, send=0.6)

    # yankı (sentetik oda)
    ir_t = tt(1.6)
    ir = np.stack([filt(rng.standard_normal(len(ir_t)), "lowpass", 5000) * np.exp(-ir_t / 0.45) for _ in range(2)])
    ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
    rev = np.stack([fftconvolve(wet[c], ir[c])[:N] for c in range(2)]) * 0.35

    mix = dry + rev
    mix = np.stack([filt(mix[c], "highpass", 30) for c in range(2)])
    fade = np.ones(N)
    fade[: int(0.01 * SR)] = np.linspace(0, 1, int(0.01 * SR))
    fade[-int(0.5 * SR):] = np.linspace(1, 0, int(0.5 * SR)) ** 1.5
    mix *= fade
    mix = np.tanh(mix * 0.9) / np.tanh(0.9)               # yumuşak sınırlama
    mix /= np.abs(mix).max() / 0.89                      # tepe: -1 dBFS
    wavfile.write(out_path, SR, (mix.T * 32767).astype(np.int16))
    print("ok", out_path)


if __name__ == "__main__":
    main()
