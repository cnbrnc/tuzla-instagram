#!/usr/bin/env python3
"""queue.json'dan bir haftanın 4 gönderisini kurar ve weeks/<HAFTA>.json dosyasını yazar.

Kullanım:
  python3 hafta.py <HAFTA> [--tekli] [--cikti <yol>]

  HAFTA   : gönderilerin başladığı Pazartesi, YYYY-MM-DD
  --tekli : Perşembe slotunda Usta İpucu yerine 'tekli' listesindeki ilk kartı kullan
  --cikti : varsayılan weeks/<HAFTA>.json

Slotlar (hepsi 10:00):
  Pazartesi  reels[0]           (Reels videosu)
  Çarşamba   urun_carousel[0]   (ürün kaydırmalısı, 3 slayt)
  Perşembe   ipucu_carousel[0]  (Usta İpucu kaydırmalısı) ya da --tekli ile tekli[0]
  Cuma       reels[1]           (Reels videosu)

Ürün sayfalarını fetch_product.py ile work/<anahtar>/ klasörüne indirir ve stok durumunu kontrol eder.
queue.json ve state.json DEĞİŞMEZ; kullanılan öğeler planlamadan sonra 'planla.py durum' ile düşülür.
Bir sorun varsa (kuyruk boş, ürün stokta yok, sayfa açılmadı) açıklayıp 1 koduyla çıkar.
"""
import datetime as dt
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def fail(msg):
    print("HATA:", msg)
    sys.exit(1)


def fetch(url, dest):
    """Ürünü indirir; product.json içeriğini döndürür."""
    r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "fetch_product.py"), url, dest],
                       capture_output=True, text=True)
    pj = os.path.join(dest, "product.json")
    if r.returncode != 0 or not os.path.exists(pj):
        fail("ürün sayfası okunamadı: %s\n%s" % (url, (r.stderr or r.stdout)[-600:]))
    with open(pj, encoding="utf-8") as f:
        return json.load(f)


def main():
    args = sys.argv[1:]
    if not args:
        fail("kullanım: python3 hafta.py <HAFTA> [--tekli] [--cikti <yol>]")
    hafta = args[0]
    monday = dt.date.fromisoformat(hafta)
    if monday.weekday() != 0:
        fail("%s Pazartesi değil" % hafta)
    tekli = "--tekli" in args
    out_path = os.path.join(ROOT, "weeks", hafta + ".json")
    if "--cikti" in args:
        out_path = os.path.abspath(args[args.index("--cikti") + 1])

    with open(os.path.join(ROOT, "queue.json"), encoding="utf-8") as f:
        q = json.load(f)
    with open(os.path.join(ROOT, "state.json"), encoding="utf-8") as f:
        state = json.load(f)

    need = {"reels": 2, "urun_carousel": 1}
    need["tekli" if tekli else "ipucu_carousel"] = 1
    for k, n in need.items():
        if len(q.get(k, [])) < n:
            fail("kuyruk boş: '%s' listesinde en az %d öğe olmalı. Önce ROBOT.md'deki kurallarla yeni öğe ekle." % (k, n))

    day = lambda n: (monday + dt.timedelta(days=n)).isoformat()
    slots = [
        (day(0), "reel", q["reels"][0]),
        (day(2), "carousel", q["urun_carousel"][0]),
        (day(3), "tekli" if tekli else "carousel", (q["tekli"] if tekli else q["ipucu_carousel"])[0]),
        (day(4), "reel", q["reels"][1]),
    ]
    theme = "light" if state.get("last_product_theme") == "dark" else "dark"

    posts, warnings = [], []
    for date, fmt, item in slots:
        post = {k: v for k, v in item.items() if k not in ("key", "dogrula")}
        post["id"] = "%s-%s" % (date, item["key"])
        post["date"] = date
        post["format"] = fmt
        post["key"] = item["key"]
        if item.get("dogrula"):
            warnings.append("%s: %s" % (item["key"], item["dogrula"]))
        if fmt == "reel":
            post["template"] = "reel"
        if item.get("url"):
            dest = os.path.join(ROOT, "work", item["key"])
            prod = fetch(item["url"], dest)
            if prod.get("availability") != "InStock":
                fail("stokta yok: %s (%s). Bu öğeyi atla: sıradaki öğeyi öne al ya da yenisini ekle." % (item["key"], item["url"]))
            post["product_dir"] = os.path.relpath(dest, ROOT)
        if item.get("slides"):
            slides = []
            for i, s in enumerate(item["slides"], 1):
                s = dict(s)
                if s.get("product_url"):
                    dest = os.path.join(ROOT, "work", item["key"], "%02d" % i)
                    prod = fetch(s.pop("product_url"), dest)
                    if prod.get("availability") != "InStock":
                        warnings.append("%s slayt %d: görseldeki ürün stokta yok (görsel yine kullanılabilir)" % (item["key"], i))
                    s["product_dir"] = os.path.relpath(dest, ROOT)
                slides.append(s)
            post["slides"] = slides
            if "theme" not in post:
                post["theme"] = theme
        posts.append(post)

    groups = [p.get("group") for p in posts if p.get("group")]
    dup = sorted({g for g in groups if groups.count(g) > 1 and g != "baglanti"})
    if dup:
        warnings.append("aynı haftada tekrar eden grup: %s" % ", ".join(dup))

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"hafta": hafta, "posts": posts}, f, ensure_ascii=False, indent=2)
    print("yazıldı:", os.path.relpath(out_path, ROOT))
    for p in posts:
        print("  %s  %-8s  %s" % (p["date"], p["format"], p["id"]))
    for w in warnings:
        print("UYARI:", w)


if __name__ == "__main__":
    main()
