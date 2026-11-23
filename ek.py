#!/usr/bin/env python3
"""Onaylı ek videolar (queue.json içindeki "ek_fragman" listesi).

Kullanıcı bu videoları 23 Kasım 2026'da izledi ve "hangisi iyi olacaksa onu yap" dedi. Videolar bitmiş halde
posts/ek/ klasöründe durur; yeniden üretilmez. Haftanın 4 gönderisine ek olarak, ayın toplamı 19'u geçmiyorsa
Salı 10:00'a bir tane eklenir ve Pazar günkü onay mesajında 5. gönderi olarak gösterilir.

  python3 ek.py liste                 sıradaki ek videolar ve ayın sayımı
  python3 ek.py ekle <HAFTA>          sıradaki videoyu weeks/<HAFTA>.json dosyasına ve out/<HAFTA>/ klasörüne ekler
                                      (hafta.py'den SONRA çalıştır; hafta.py yeniden çalışırsa bunu da yinele)
"""
import datetime as dt
import json
import os
import shutil
import sys

import planla

ROOT = os.path.dirname(os.path.abspath(__file__))
SINIR = 19                                   # Metricool ücretsiz plan 20; bir pay bırakılır
LISTE = "ek_fragman"


def ay_sayimi(ay, hafta=None):
    """O aya düşen gönderi + hikaye sayısı: state.json (planlanmışlar) + weeks/<HAFTA>.json (bu haftanın yenileri)."""
    state = planla.load(os.path.join(ROOT, "state.json"))
    gorulen, n = set(), 0
    for e in state.get("posted", []):
        if e["date"][:7] == ay:
            n += 2 if e.get("hikaye") else 1
        gorulen.add(e["id"])
    # önceden planlanmış haftalar Metricool'da hazırdır ama Pazar çalışmasına kadar "posted" listesine girmez
    for f in sorted(os.listdir(os.path.join(ROOT, "weeks"))):
        if not f[:4].isdigit():
            continue
        wk = planla.load(os.path.join(ROOT, "weeks", f))
        if not (wk.get("on_planli") or f[:-5] == hafta):
            continue
        for p in wk["posts"]:
            if p["id"] not in gorulen and p["date"][:7] == ay:
                n += 2 if p.get("hikaye") else 1
                gorulen.add(p["id"])
    return n


def cmd_liste():
    q = planla.load(os.path.join(ROOT, "queue.json"))
    kalan = q.get(LISTE, [])
    print("Sıradaki ek videolar (%d):" % len(kalan))
    for it in kalan:
        print("  %-22s %s · sitede arat: %s" % (it["key"], it["baslik"], it["search_code"]))
    bugun = dt.date.today()
    for i in range(3):
        y, m = bugun.year + (bugun.month - 1 + i) // 12, (bugun.month - 1 + i) % 12 + 1
        ay = "%04d-%02d" % (y, m)
        print("  %s: %d gönderi kayıtlı (sınır %d)" % (ay, ay_sayimi(ay), SINIR))


def cmd_ekle(hafta):
    pzt = dt.date.fromisoformat(hafta)
    if pzt.weekday() != 0:
        raise SystemExit("HATA: %s Pazartesi değil" % hafta)
    wpath = os.path.join(ROOT, "weeks", hafta + ".json")
    if not os.path.exists(wpath):
        raise SystemExit("HATA: önce hafta.py çalışmalı (weeks/%s.json yok)" % hafta)
    wk = planla.load(wpath)
    if wk.get("on_planli"):
        raise SystemExit("HATA: %s önceden planlanmış hafta; ek video eklenmez" % hafta)
    if any(p.get("ek") for p in wk["posts"]):
        raise SystemExit("Bu haftada zaten bir ek video var; ikinci eklenmez.")
    gun = (pzt + dt.timedelta(days=1)).isoformat()            # Salı
    n = ay_sayimi(gun[:7], hafta)
    if n + 1 > SINIR:
        raise SystemExit("EKLENMEDİ: %s ayında %d gönderi var; ek video sınırı (%d) aşar. Gelecek aya kalır." % (gun[:7], n, SINIR))
    q = planla.load(os.path.join(ROOT, "queue.json"))
    for it in q.get(LISTE, []):
        durum, neden = planla.urun_kontrol(it["url"], os.path.join(ROOT, "work", "ek-stok-" + it["key"]))
        if durum != "TAMAM":
            print("atlandı: %s (%s: %s)" % (it["key"], durum, neden))
            continue
        pid = "%s-%s" % (gun, it["key"])
        out = os.path.join(ROOT, "out", hafta)
        os.makedirs(out, exist_ok=True)
        for son in (".mp4", "-kapak.jpg"):
            kaynak = os.path.join(ROOT, it["medya"] + son)
            if not os.path.exists(kaynak):
                raise SystemExit("HATA: dosya yok: %s%s" % (it["medya"], son))
            shutil.copy2(kaynak, os.path.join(out, pid + son))
        post = dict(it, id=pid, date=gun, ek=True, hazir=True)
        wk["posts"] = sorted(wk["posts"] + [post], key=lambda p: p["date"])
        planla.save(wpath, wk)
        print("eklendi: %s → Salı %s 10:00 (ayın toplamı %d olur)" % (it["key"], gun, n + 1))
        print("video: out/%s/%s.mp4" % (hafta, pid))
        print("açıklama:\n" + it["caption"])
        return
    raise SystemExit("EKLENMEDİ: sırada stokta olan ek video yok.")


def main():
    a = sys.argv[1:]
    if a[:1] == ["liste"]:
        cmd_liste()
    elif a[:1] == ["ekle"] and len(a) == 2:
        cmd_ekle(a[1])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
