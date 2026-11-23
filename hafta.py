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

queue.json içindeki "reels_slotlari" ayarı varsa ve HAFTA onun "baslangic" tarihinden önce değilse,
Pazartesi ve Cuma Reels'i ayarda yazan listelerin ilk öğesinden alınır
(4 Ocak 2027'den itibaren: Pazartesi reels_bil "Bil bakalım", Cuma reels_yd "Yanlış / doğru").
Ayarda "stil" varsa (sinematik) yeni türlerin gönderilerine yazılır. Öğede bg_video.url varsa stok görüntü
work/stok/ klasörüne indirilir; indirilemezse uyarı verilir ve gönderi kodla üretilmiş sahneyle hazırlanır.

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


def stok_indir(url):
    """Stok videoyu work/stok/ klasörüne indirir; yolu (depoya göre) ya da None döndürür."""
    hedef = os.path.join(ROOT, "work", "stok", os.path.basename(url.split("?")[0]))
    os.makedirs(os.path.dirname(hedef), exist_ok=True)
    if not (os.path.exists(hedef) and os.path.getsize(hedef) > 100000):
        subprocess.run(["curl", "-sSL", "-m", "240", "-A", "Mozilla/5.0", "-o", hedef, url], capture_output=True)
    ok = os.path.exists(hedef) and os.path.getsize(hedef) > 100000 and subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "csv=p=0", hedef],
        capture_output=True, text=True).stdout.strip() != ""
    if not ok:
        if os.path.exists(hedef):
            os.remove(hedef)
        return None
    return os.path.relpath(hedef, ROOT)


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
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            if json.load(f).get("on_planli"):
                fail("%s haftası önceden planlandı ve Metricool'da hazır. hafta.py çalıştırma; "
                     "ROBOT.md'deki 'Önceden planlanmış haftalar' bölümünü uygula." % hafta)
    if "--cikti" in args:
        out_path = os.path.abspath(args[args.index("--cikti") + 1])

    with open(os.path.join(ROOT, "queue.json"), encoding="utf-8") as f:
        q = json.load(f)
    with open(os.path.join(ROOT, "state.json"), encoding="utf-8") as f:
        state = json.load(f)

    rs = q.get("reels_slotlari") or {}
    if rs and hafta >= rs.get("baslangic", "9999"):
        pzt_list, cuma_list = rs["pazartesi"], rs["cuma"]
    else:
        pzt_list = cuma_list = "reels"
    need = {"urun_carousel": 1}
    if pzt_list == cuma_list:
        need[pzt_list] = 2
    else:
        need[pzt_list] = need[cuma_list] = 1
    need["tekli" if tekli else "ipucu_carousel"] = 1
    for k, n in need.items():
        if len(q.get(k, [])) < n:
            fail("kuyruk boş: '%s' listesinde en az %d öğe olmalı. Önce ROBOT.md'deki kurallarla yeni öğe ekle." % (k, n))

    day = lambda n: (monday + dt.timedelta(days=n)).isoformat()
    slots = [
        (day(0), "reel", q[pzt_list][0]),
        (day(2), "carousel", q["urun_carousel"][0]),
        (day(3), "tekli" if tekli else "carousel", (q["tekli"] if tekli else q["ipucu_carousel"])[0]),
        (day(4), "reel", q[cuma_list][1 if pzt_list == cuma_list else 0]),
    ]
    theme = "light" if state.get("last_product_theme") == "dark" else "dark"
    # Reels ritimleri sırayla döner; aynı hafta iki Reels'te aynı ritim olmaz (state.json: ses_sirasi)
    ritimler = ["enerjik", "atolye", "derin"]
    # Yeni türlerde müzik: ses-kaynak.json'daki sıra (farklı parçalar); art arda iki Reels aynı parçayla çıkmaz
    try:
        with open(os.path.join(ROOT, "assets", "ses-kaynak.json"), encoding="utf-8") as f:
            muzik_sirasi = json.load(f).get("sira") or ["a", "b", "c"]
    except (OSError, ValueError):
        muzik_sirasi = ["a", "b", "c"]
    ses_i = state.get("ses_sirasi", 0)
    # Hikaye denemesi: listedeki haftalarda Reels aynı gün hikaye olarak da yayınlanır (state.json)
    deneme = state.get("hikaye_denemesi") or {}
    hikaye_saati = deneme.get("saat", "18:00") if hafta in deneme.get("haftalar", []) else None

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
            post.setdefault("template", "reel")
            if post["template"] == "reel":       # yeni türlerin kendi sesi var (reel.py: DEFAULT_SOUND)
                post.setdefault("ses", ritimler[ses_i % len(ritimler)])
                ses_i += 1
            if hikaye_saati:
                post["hikaye"] = hikaye_saati
            if post["template"] != "reel" and rs.get("stil") and hafta >= rs.get("baslangic", "9999"):
                post.setdefault("stil", rs["stil"])
                # profesyonel ses: müzik varyantı sırayla döner (a, b, c)
                post.setdefault("muzik", muzik_sirasi[ses_i % len(muzik_sirasi)])
                ses_i += 1
            bgv = post.get("bg_video")
            if bgv and bgv.get("url"):
                yol = stok_indir(bgv["url"]) if post.get("stil") == "sinematik" else None
                if yol:
                    post["bg_video"] = dict(bgv, file=yol)
                else:
                    post.pop("bg_video")
                    warnings.append("%s: stok video indirilemedi ya da stil sinematik değil; kodla üretilmiş sahneyle hazırlanacak" % item["key"])
        if item.get("url"):
            dest = os.path.join(ROOT, "work", item["key"])
            prod = fetch(item["url"], dest)
            if prod.get("availability") != "InStock":
                fail("stokta yok: %s (%s). Bu öğeyi atla: sıradaki öğeyi öne al ya da yenisini ekle." % (item["key"], item["url"]))
            post["product_dir"] = os.path.relpath(dest, ROOT)
        # Yeni Reels türleri: seçeneklerin ve panellerin ürün görselleri
        nested = [("options", i, o) for i, o in enumerate(item.get("options", []))]
        nested += [(k, None, item[k]) for k in ("yanlis", "dogru") if isinstance(item.get(k), dict)]
        for alan, i, d in nested:
            if not d.get("product_url"):
                continue
            d = dict(d)
            ad = "ab"[i] if alan == "options" else alan
            dest = os.path.join(ROOT, "work", item["key"], ad)
            prod = fetch(d.pop("product_url"), dest)
            if prod.get("availability") != "InStock":
                if alan == "dogru":
                    fail("stokta yok: %s içinde önerilen ürün (%s). Bu öğeyi atla ya da başka ürünle güncelle." % (item["key"], prod.get("name")))
                warnings.append("%s: %s görselindeki ürün stokta yok (görsel yine kullanılabilir)" % (item["key"], ad))
            d["product_dir"] = os.path.relpath(dest, ROOT)
            if alan == "options":
                post["options"] = list(post["options"])
                post["options"][i] = d
            else:
                post[alan] = d
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
