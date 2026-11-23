#!/usr/bin/env python3
"""Yeni Reels türleri için 9 saniyelik özgün ses izleri (telifsiz, kodla üretilir). Çalgılar ses.py'den gelir.

Türler ve zamanlama (şablonlarla aynıdır; birini değiştirirsen ötekini de değiştir):

  bil  -> templates/reel_bil.html ("Bil bakalım")
    0,00 / 0,25   soru satırları            -> "tak-TAK"
    0,50 / 0,75   A ve B seçenekleri        -> iki "pıt"
    1,0 – 4,0     geri sayım 3-2-1          -> saat tik-takı, yükselen gerilim, son saniyede hızlanır
    4,00          cevap açılır              -> vuruş, "ding" ve ritim başlar
    4,25 / 4,75 / 5,25  cevap ve nedeni     -> "pıt" sesleri
    6,75 – 9,0    kapanış kartı             -> ürün Reels'iyle aynı: "tınn", sonda başa saran yükseliş

  yd   -> templates/reel_yd.html ("Yanlış / doğru")
    0,00 / 0,25 / 0,50  kanca satırları     -> "tak-tak-TAK"
    1,50          YANLIŞ paneli gelir       -> "vuuş" ve tok vuruş
    2,00          YANLIŞ damgası            -> hata sesi (kalın "bızz")
    3,50          DOĞRU paneli gelir        -> "vuuş" ve tok vuruş
    4,00          DOĞRU damgası             -> "ding" ve ritim başlar
    5,00          neden satırı              -> "pıt"
    6,75 – 9,0    kapanış kartı             -> aynı kapanış

Kullanım: python3 ses_tur.py <çıktı.wav> --tur bil|yd
Tohum sabit; her çalıştırmada aynı ses çıkar.
"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve

import ses as S

SR, N = S.SR, S.N
TURLER = {
    "bil": {"kok": 0, "takim": "klasik", "lead": "pluck"},
    "yd": {"kok": -2, "takim": "atolye", "lead": "bell"},
}


class Mix:
    def __init__(self):
        self.dry = np.zeros((2, N))
        self.wet = np.zeros((2, N))

    def put(self, sig, at, gain=1.0, pan=0.0, send=0.0):
        i = int(round(at * SR))
        j = min(N, i + len(sig))
        if j <= i:
            return
        s = sig[: j - i] * gain
        th = (pan + 1) * np.pi / 4
        l, r = np.sqrt(2) * np.cos(th), np.sqrt(2) * np.sin(th)
        self.dry[0, i:j] += s * l
        self.dry[1, i:j] += s * r
        if send:
            self.wet[0, i:j] += s * l * send
            self.wet[1, i:j] += s * r * send

    def write(self, path):
        ir_t = S.tt(1.4)
        ir = np.stack([S.filt(S.rng.standard_normal(len(ir_t)), "lowpass", 5000) * np.exp(-ir_t / 0.4) for _ in range(2)])
        ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
        rev = np.stack([fftconvolve(self.wet[c], ir[c])[:N] for c in range(2)]) * 0.3
        mix = self.dry + rev
        mix = np.stack([S.filt(mix[c], "highpass", 30) for c in range(2)])
        edge = int(0.006 * SR)                               # yalnız tık önleme; sonda kısılma yok (döngü)
        mix[:, :edge] *= np.linspace(0, 1, edge)
        mix[:, -edge:] *= np.linspace(1, 0, edge)
        mix = np.tanh(mix * 0.9) / np.tanh(0.9)
        mix /= np.abs(mix).max() / 0.89
        wavfile.write(path, SR, (mix.T * 32767).astype(np.int16))
        print("ok", path)


def buzzer():
    """Hata sesi: kalın, hafif akortsuz iki ton."""
    d = 0.42
    t = S.tt(d)
    s = np.sign(np.sin(2 * np.pi * 98 * t)) * 0.5 + np.sign(np.sin(2 * np.pi * 104 * t)) * 0.5
    s = S.filt(s, "lowpass", 1100)
    return s * np.minimum(1, t / 0.006) * np.minimum(1, (d - t) / 0.05) * 0.8


def ding(m, note, at):
    """Doğru cevap: parlak, yukarı çıkan üç nota ve ışıltı."""
    for k, semi in enumerate((3, 7, 15)):
        m.put(S.bell_lead(note(semi), 0.6), at + 0.07 * k, 0.55, -0.2 + 0.2 * k, send=0.5)
    m.put(S.shing(), at, 0.3, 0.1, send=0.4)


def groove(m, note, T):
    """4,0 – 6,5 sn: dört vuruş, bas ve akılda kalan melodi (ürün Reels'indeki ezgi)."""
    lead = S.pluck if T["lead"] == "pluck" else S.bell_lead
    atolye = T["takim"] == "atolye"
    chords = [(4.0, 5.0, (-4, 0, 3)), (5.0, 6.0, (-2, 2, 5)), (6.0, 7.0, (-5, -2, 2)), (7.0, 9.0, (0, 3, 7))]
    roots = [(4.0, 5.0, -28), (5.0, 6.0, -26), (6.0, 7.0, -29)]
    for a, b, c in chords:
        m.put(S.chord([note(s - 12) for s in c], b - a, cutoff=1300, decay=4.0), a, 0.14, send=0.4)
    for k in range(6):
        m.put(S.kick(), 4.0 + 0.5 * k, 0.9)
    m.put(S.kick(), 5.75, 0.6)
    for k in range(20):
        at = 4.0 + 0.125 * k
        acc = k % 4 == 2
        if atolye:
            if acc:
                m.put(S.tink(3000 + 250 * (k % 3)), at, 0.5, 0.35 if k % 8 == 2 else -0.35, send=0.15)
        else:
            m.put(S.hat(0.022 if acc else 0.008), at, 0.75 if acc else 0.32, 0.2 if k % 2 else -0.2)
    for at in (4.5, 5.5, 6.5):
        if atolye:
            m.put(S.hammer(), at, 0.75, send=0.3)
        else:
            m.put(S.clap(), at, 0.85, send=0.25)
            m.put(S.snare(), at, 0.35)
    for a, b, s in roots:
        k = 0
        while a + 0.25 * k < b - 0.01:
            m.put(S.bass(note(s) * (2 if k % 2 else 1), drive=atolye), a + 0.25 * k, 0.5 if k % 2 else 0.72)
            k += 1
    for a, seq in [(4.0, [3, None, 3, 0]), (5.0, [2, None, 2, 5]), (6.0, [7, None, 5, 2])]:
        for k, s in enumerate(seq):
            if s is not None:
                m.put(lead(note(s)), a + 0.25 * k, 0.5, 0.15 if k % 2 else -0.15, send=0.35)


def kapanis(m, note, T):
    """6,62 – 9,0 sn: kapanış kartı ve başa saran yükseliş (ürün Reels'iyle aynı)."""
    lead = S.pluck if T["lead"] == "pluck" else S.bell_lead
    m.put(S.sweep_noise(0.4, 300, 6500) * S.bell(int(SR * 0.4), 0.8), 6.62, 0.6, send=0.2)
    m.put(S.clank(), 7.0, 0.6, send=0.5)
    m.put(S.kick(), 7.0, 0.95)
    m.put(S.crash(), 7.0, 0.4, send=0.3)
    m.put(S.long_bass(note(-24), 1.25), 7.0, 0.55)
    for at in (7.5, 8.0):
        m.put(S.kick(), at, 0.7)
    for k in range(10):
        m.put(S.hat(0.02), 7.25 + 0.25 * k, 0.4, 0.2 if k % 2 else -0.2)
    for k, s in enumerate([7, None, 7, 5, 3, None, 0, None]):
        if s is not None:
            m.put(lead(note(s)), 7.0 + 0.25 * k, 0.32, send=0.4)
    m.put(S.crash(0.75)[::-1], 8.25, 0.55, send=0.1)
    if T["takim"] == "atolye":
        m.put(S.ratchet(0.75, 14, 36), 8.25, 0.45, -0.2)
    else:
        for k in range(6):
            m.put(S.snare(200 + 20 * k), 8.25 + 0.125 * k, 0.25 + 0.08 * k)
    m.put(S.riser(0.75, 400, 8000), 8.25, 0.5)


def bil(m, note, T):
    for at, semi, g in ((0.0, -12, 0.9), (0.25, -5, 1.0)):                 # soru: tak-TAK
        m.put(S.metal_hit(note(semi)), at, g, (at - 0.12) * 1.5, send=0.25)
        m.put(S.kick(), at, 0.9)
    m.put(S.sub_boom(), 0.0, 0.6)
    for at, f, p in ((0.5, 700, -0.35), (0.75, 930, 0.35)):                # A ve B
        m.put(S.pop(f), at, 0.7, p, send=0.3)
        m.put(S.kick(muffled=True), at, 0.6)
    # geri sayım: 3 (1,0) – 2 (2,0) – 1 (3,0); cevap 4,0
    for k in range(3):
        at = 1.0 + k
        m.put(S.tink(2400 + 200 * k), at, 0.95, -0.15, send=0.25)
        m.put(S.kick(muffled=True), at, 0.95)
        m.put(S.tink(1800), at + 0.5, 0.5, 0.15, send=0.15)
        m.put(S.kick(muffled=True), at + 0.5, 0.45)
    for k, at in enumerate((3.25, 3.5, 3.625, 3.75, 3.875)):                # son saniye hızlanır
        m.put(S.tink(2700 + 120 * k), at, 0.5 + 0.08 * k, 0.2 if k % 2 else -0.2)
        m.put(S.snare(190 + 22 * k), at, 0.3 + 0.1 * k, send=0.2)
    m.put(S.long_bass(note(-24), 3.0), 1.0, 0.3)
    m.put(S.riser(3.0, 200, 7000), 1.0, 0.42)
    m.put(S.sweep_noise(0.4, 500, 6000) * S.bell(int(SR * 0.4), 0.85), 3.6, 0.5, send=0.2)
    # cevap
    m.put(S.impact(), 4.0, 0.6)
    m.put(S.sub_boom(), 4.0, 0.7)
    m.put(S.crash(), 4.0, 0.5, send=0.3)
    ding(m, note, 4.0)
    groove(m, note, T)
    for at, f, p in ((4.27, 760, -0.2), (4.77, 860, 0.0), (5.27, 960, 0.2)):
        m.put(S.pop(f), at, 0.55, p, send=0.35)
    kapanis(m, note, T)


def yd(m, note, T):
    for at, semi, g in ((0.0, -12, 0.9), (0.25, -9, 0.8), (0.5, -5, 1.0)):  # kanca: tak-tak-TAK
        m.put(S.metal_hit(note(semi)), at, g, (at - 0.25) * 1.2, send=0.25)
        m.put(S.kick(), at, 0.9 if at != 0.25 else 0.55)
    m.put(S.sub_boom(), 0.0, 0.6)
    m.put(S.kick(muffled=True), 1.0, 0.8)
    m.put(S.riser(0.95), 0.55, 0.4)
    # YANLIŞ: panel 1,5; damga 2,0
    m.put(S.sweep_noise(0.3, 400, 5000) * S.bell(int(SR * 0.3), 0.85), 1.25, 0.55, send=0.2)
    m.put(S.impact(), 1.5, 0.6)
    m.put(buzzer(), 2.0, 0.6, send=0.15)
    m.put(S.hammer(), 2.0, 0.6, send=0.2)
    m.put(S.long_bass(note(-29), 1.4), 2.05, 0.38)                           # huzursuz bekleyiş
    for at in (2.5, 3.0):
        m.put(S.kick(muffled=True), at, 0.75)
    for k in range(5):
        m.put(S.tink(2000), 2.25 + 0.25 * k, 0.22, 0.3 if k % 2 else -0.3)
    # DOĞRU: panel 3,5; damga 4,0
    m.put(S.sweep_noise(0.3, 400, 5000) * S.bell(int(SR * 0.3), 0.85), 3.25, 0.55, send=0.2)
    m.put(S.impact(), 3.5, 0.55)
    m.put(S.riser(0.5, 500, 8000), 3.5, 0.4)
    for k, at in enumerate((3.75, 3.875)):
        m.put(S.snare(210 + 30 * k), at, 0.4 + 0.15 * k, send=0.2)
    m.put(S.impact(0.25), 4.0, 0.5)
    m.put(S.sub_boom(), 4.0, 0.7)
    m.put(S.crash(), 4.0, 0.45, send=0.3)
    ding(m, note, 4.0)
    groove(m, note, T)
    m.put(S.pop(820), 5.02, 0.6, 0.0, send=0.35)
    kapanis(m, note, T)


def main():
    out_path = sys.argv[1]
    tur = sys.argv[sys.argv.index("--tur") + 1] if "--tur" in sys.argv else ""
    if tur not in TURLER:
        raise SystemExit("kullanım: python3 ses_tur.py <çıktı.wav> --tur bil|yd")
    T = TURLER[tur]
    tr = 2 ** (T["kok"] / 12)
    note = lambda semi: 440.0 * tr * 2 ** (semi / 12)
    m = Mix()
    {"bil": bil, "yd": yd}[tur](m, note, T)
    m.write(out_path)


if __name__ == "__main__":
    main()
