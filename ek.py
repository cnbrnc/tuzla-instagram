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
import subprocess
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


def uret(taslak, out, pid):
    """Taslak tanımındaki (tek gönderili JSON) videoyu üretir; stok kesitleri eksikse 'url' alanından indirir."""
    spec = planla.load(os.path.join(ROOT, taslak))
    post = spec["posts"][0]
    for c in post.get("sahneler", []) + ([post["bg_video"]] if post.get("bg_video") else []):
        yol = os.path.join(ROOT, c["file"])
        if not os.path.exists(yol):
            os.makedirs(os.path.dirname(yol), exist_ok=True)
            subprocess.run(["curl", "-sSL", "-m", "240", "-A", "Mozilla/5.0", "-o", yol, c.get("url", "")])
            if not (os.path.exists(yol) and os.path.getsize(yol) > 50000):
                raise SystemExit("HATA: kesit indirilemedi: %s (%s)" % (c["file"], c.get("url")))
    if post.get("product_dir") and not os.path.exists(os.path.join(ROOT, post["product_dir"], "product.json")):
        subprocess.run([sys.executable, "-I", os.path.join(ROOT, "fetch_product.py"), post["url"], os.path.join(ROOT, post["product_dir"])], check=True)
    gecici = os.path.join(out, "_ek")
    subprocess.run([sys.executable, os.path.join(ROOT, "reel.py"), os.path.join(ROOT, taslak), gecici], check=True, cwd=ROOT)
    for son in (".mp4", "-kapak.jpg"):
        shutil.move(os.path.join(gecici, post["id"] + son), os.path.join(out, pid + son))
    shutil.rmtree(gecici, ignore_errors=True)
    return {k: v for k, v in post.items() if k != "id"}


def cmd_liste():
    q = planla.load(os.path.join(ROOT, "queue.json"))
    kalan = q.get(LISTE, [])
    print("Sıradaki ek videolar (%d):" % len(kalan))
    for it in kalan:
        print("  %-22s %s%s" % (it["key"], it.get("baslik") or it.get("not", ""), "  (taslaktan üretilecek)" if it.get("taslak") else ""))
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
    dolu = [e["id"] for e in planla.load(os.path.join(ROOT, "state.json")).get("posted", []) if e["date"][:10] == gun]
    if dolu:
        raise SystemExit("EKLENMEDİ: %s Salı günü zaten planlı gönderi var (%s). Bu hafta ek video yok." % (gun, ", ".join(dolu)))
    n = ay_sayimi(gun[:7], hafta)
    # ayın bu haftadan sonraki normal gönderileri de (Pzt, Çrş, Prş, Cuma) sınıra sayılır
    d, kalan = pzt + dt.timedelta(days=7), 0
    while d.isoformat()[:7] <= gun[:7]:
        kalan += d.isoformat()[:7] == gun[:7] and d.weekday() in (0, 2, 3, 4)
        d += dt.timedelta(days=1)
    if n + kalan + 1 > SINIR:
        raise SystemExit("EKLENMEDİ: %s ayında %d gönderi var, %d normal gönderi daha gelecek; ek video sınırı (%d) aşar. Gelecek aya kalır."
                         % (gun[:7], n, kalan, SINIR))
    q = planla.load(os.path.join(ROOT, "queue.json"))
    for it in q.get(LISTE, []):
        if it.get("url"):                                     # ürünlü video: stokta mı?
            durum, neden = planla.urun_kontrol(it["url"], os.path.join(ROOT, "work", "ek-stok-" + it["key"]))
            if durum != "TAMAM":
                print("atlandı: %s (%s: %s)" % (it["key"], durum, neden))
                continue
        pid = "%s-%s" % (gun, it["key"])
        out = os.path.join(ROOT, "out", hafta)
        os.makedirs(out, exist_ok=True)
        if it.get("medya"):                                   # bitmiş video depoda (posts/ek/)
            for son in (".mp4", "-kapak.jpg"):
                kaynak = os.path.join(ROOT, it["medya"] + son)
                if not os.path.exists(kaynak):
                    raise SystemExit("HATA: dosya yok: %s%s" % (it["medya"], son))
                shutil.copy2(kaynak, os.path.join(out, pid + son))
        else:                                                 # video depoda yok: taslak tanımından yeniden üretilir
            it = dict(uret(it["taslak"], out, pid), **it)
        post = dict(it, id=pid, date=gun, ek=True, hazir=True)
        wk["posts"] = sorted(wk["posts"] + [post], key=lambda p: p["date"])
        planla.save(wpath, wk)
        print("eklendi: %s → Salı %s 10:00 (ay sonunda toplam %d olur)" % (it["key"], gun, n + kalan + 1))
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
