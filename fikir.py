#!/usr/bin/env python3
"""Fikir dağarcığından (dagarcik.json) Reels konusu seçer ve kuyruk öğesinin iskeletini yazar.

Kullanım:
  python3 fikir.py liste [bil|yd|ipucu]   kullanılmamış fikirleri listeler
  python3 fikir.py sec <HAFTA>            o hafta için 3'er aday önerir (Pazartesi "bil", Cuma "yd") ve nedenini yazar
  python3 fikir.py kuyruk <id>            fikrin kuyruk öğesi iskeletini yazdırır (url, urun, search_code, caption senin işin)
  python3 fikir.py karne                  kanca kalıbına ve kurguya göre geçme oranı ortalamasını yazar (state.json karnesinden)

Seçim kuralları (ayrıntı SENARYO.md):
  - Kullanılmış fikir yeniden önerilmez (state.json: kullanilan_fikirler).
  - Son 3 haftada işlenen grup ve bir önceki haftanın kanca kalıbı ile kurgusu (cift) geri sıraya düşer.
  - Doğrulanmış fikir öne geçer; doğrulanmamış olan kullanılmadan önce kaynakla doğrulanır.
  - Karnede yeterli veri varsa (kalıp başına en az 2 Reels) geçme oranı düşük olan kalıp öne geçer.
Ürün adayları work/products.xml dosyasından aranır (yoksa önce: python3 pick_products.py 10).
"""
import datetime as dt
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://tuzlahirdavat.com.tr/"
TR = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")


def oku(ad):
    with open(os.path.join(ROOT, ad), encoding="utf-8") as f:
        return json.load(f)


def haftalar():
    """weeks/*.json: (hafta, gönderiler) listesi, eskiden yeniye."""
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "weeks", "20*.json"))):
        with open(f, encoding="utf-8") as fh:
            out.append((os.path.basename(f)[:-5], json.load(fh).get("posts", [])))
    return out


def kullanilan(state):
    ids = {k["id"] for k in state.get("kullanilan_fikirler", [])}
    for _, posts in haftalar():
        ids |= {p["fikir"] for p in posts if p.get("fikir")}
    for v in oku("queue.json").values():
        if isinstance(v, list):
            ids |= {it["fikir"] for it in v if isinstance(it, dict) and it.get("fikir")}
    return ids


def urun_adaylari(aranan, n=4):
    yol = os.path.join(ROOT, "work", "products.xml")
    if not os.path.exists(yol):
        return None
    with open(yol, encoding="utf-8", errors="replace") as f:
        slugs = [u.rsplit("/", 1)[1] for u in re.findall(r"<loc>(%s[^<]+)</loc>" % re.escape(SITE), f.read())]
    out = []
    for ifade in aranan.split(","):
        kelimeler = [k for k in ifade.strip().lower().translate(TR).split() if k]
        if kelimeler:
            out += [s for s in slugs if all(k in s for k in kelimeler)][:n]
    return list(dict.fromkeys(out))[:n * 2]


def kalip_puani(state):
    """Karneden: kanca kalıbı ve kurgu başına ortalama geçme oranı (düşük iyi). En az 2 Reels'i olanlar."""
    bilgi = {}
    for _, posts in haftalar():
        for p in posts:
            if p.get("format") == "reel":
                bilgi[p["id"]] = (p.get("kanca_kalibi"), p.get("cift") or p.get("template", "").replace("reel_", ""))
    top = {}
    for k in state.get("karne", []):
        for r in k.get("reels", []):
            g = r.get("gecme_orani")
            if g is None or r.get("id") not in bilgi:
                continue
            for anahtar in bilgi[r["id"]]:
                if anahtar:
                    top.setdefault(anahtar, []).append(float(g))
    return {a: sum(v) / len(v) for a, v in top.items() if len(v) >= 2}, {a: len(v) for a, v in top.items()}


def sec(hafta):
    d = oku("dagarcik.json")
    state = oku("state.json")
    kul = kullanilan(state)
    pzt = dt.date.fromisoformat(hafta)
    son = [(h, ps) for h, ps in haftalar() if h < hafta][-3:]
    son_gruplar = {p.get("group") for _, ps in son for p in ps if p.get("group")}
    onceki = son[-1][1] if son else []
    onceki_kalip = {p.get("kanca_kalibi") for p in onceki if p.get("kanca_kalibi")}
    onceki_cift = {p.get("cift") or "yanlis-dogru" for p in onceki if p.get("template") == "reel_yd"}
    puan, sayi = kalip_puani(state)
    print("Hafta %s · son 3 haftanın grupları: %s" % (hafta, ", ".join(sorted(g for g in son_gruplar if g)) or "yok"))
    if puan:
        print("Karne (geçme oranı, düşük iyi): " + ", ".join("%s %%%.0f (%d Reels)" % (a, v, sayi[a]) for a, v in sorted(puan.items(), key=lambda x: x[1])))
    secilen_gruplar = set()
    for tur, gun in (("bil", "Pazartesi"), ("yd", "Cuma")):
        adaylar = []
        for f in d["fikirler"]:
            if f["tur"] != tur or f["id"] in kul:
                continue
            ay = f.get("mevsim")
            if ay and pzt.month not in ay:
                continue
            ceza, neden = 0, []
            if not f.get("dogrulandi"):
                ceza += 3; neden.append("önce doğrula")
            aile = f["grup"].split("-")[0]
            if f["grup"] in son_gruplar or aile in {str(g).split("-")[0] for g in son_gruplar}:
                ceza += 4; neden.append("grup yakın zamanda işlendi")
            if aile in secilen_gruplar:
                ceza += 6; neden.append("Pazartesi ile aynı grup")
            if f.get("kanca_kalibi") in onceki_kalip:
                ceza += 1; neden.append("geçen haftayla aynı kanca kalıbı")
            if tur == "yd" and f.get("cift") in onceki_cift:
                ceza += 2; neden.append("geçen haftayla aynı kurgu")
            for a in (f.get("kanca_kalibi"), f.get("cift")):
                if a in puan:                      # geçme oranı %60'ın altındaysa öne al, üstündeyse geri at
                    ceza += (puan[a] - 60) / 15
            adaylar.append((ceza, f, neden))
        adaylar.sort(key=lambda x: x[0])
        print("\n%s · %s" % (gun, "Bil bakalım" if tur == "bil" else "Yanlış / doğru ailesi"))
        if not adaylar:
            print("  Dağarcıkta kullanılmamış fikir kalmadı. SENARYO.md'deki kurallarla yenisini yaz ve dagarcik_yaz.py dosyasına ekle.")
        for i, (ceza, f, neden) in enumerate(adaylar[:3]):
            if i == 0:
                secilen_gruplar.add(f["grup"].split("-")[0])
            baslik = " ".join(f.get("question") or f.get("hook"))
            print("  %d. %-22s %s  [%s%s]" % (i + 1, f["id"], baslik, f["grup"], ", " + f["cift"] if f.get("cift") else ""))
            print("     meslek: %s · kanca kalıbı: %s%s" % (f["meslek"], f.get("kanca_kalibi"), (" · dikkat: " + "; ".join(neden)) if neden else ""))
            u = urun_adaylari(f["urun_ara"])
            print("     ürün ara: %s%s" % (f["urun_ara"], "" if u is None else (" → " + (", ".join(u[:4]) if u else "sitede bulunamadı"))))
            if f.get("not"):
                print("     not: " + f["not"])


def kuyruk(fid):
    f = next((x for x in oku("dagarcik.json")["fikirler"] if x["id"] == fid), None)
    if not f:
        raise SystemExit("HATA: dağarcıkta yok: " + fid)
    ortak = {"key": f["id"], "fikir": f["id"], "group": f["grup"], "kanca_kalibi": f.get("kanca_kalibi"),
             "url": "YAZ: tanıtılacak ürünün sayfası (stokta olmalı)", "search_code": "YAZ: sitede aranacak kod ya da kelime",
             "urun": {"marka": "YAZ", "ad": "YAZ", "ozellik": "YAZ"}, "kaynak": f["kaynak"] + (" (%s'de doğrulandı)" % f["dogrulandi"] if f.get("dogrulandi") else " (DOĞRULA ve tarihi yaz)"),
             "caption": "YAZ: SENARYO.md → Açıklama"}
    if f["tur"] == "bil":
        oge = dict(ortak, template="reel_bil", tag="BİL BAKALIM", question_kicker=f["question_kicker"], question=f["question"],
                   options=f["options"], answer=f["answer"], answer_text=f["answer_text"], why=f["why"])
    else:
        etiket = {"yanlis-dogru": ("USTA HATASI", "SIK YAPILAN HATA"), "efsane-gercek": ("EFSANE Mİ?", "DOĞRU BİLİNEN YANLIŞ"),
                  "zor-kolay": ("USTA İPUCU", "ZOR YOLDAN MI?")}[f["cift"]]
        oge = dict(ortak, template="reel_yd", cift=f["cift"], tag=etiket[0], hook_kicker=etiket[1], hook=f["hook"],
                   yanlis=dict(f["yanlis"], product_url="İSTEĞE BAĞLI: yanlış kullanılan ürünün sayfası; yoksa bu satırı sil"),
                   dogru=dict(f["dogru"], product_url="İSTEĞE BAĞLI: doğru ürünün sayfası; yoksa bu satırı sil"),
                   why_kicker="Neden?", why=f["why"])
        if f.get("sfx_kanca"):
            oge["sfx_kanca"] = f["sfx_kanca"]
    if not f.get("dogrulandi"):
        oge["dogrula"] = "Bu fikir dağarcıkta doğrulanmamış. Kullanmadan önce kaynakla doğrula."
    print(json.dumps(oge, ensure_ascii=False, indent=2))
    if f.get("not"):
        print("\nNOT: " + f["not"], file=sys.stderr)


def liste(tur=None):
    d, kul = oku("dagarcik.json"), kullanilan(oku("state.json"))
    if tur in (None, "bil", "yd"):
        for f in d["fikirler"]:
            if tur and f["tur"] != tur:
                continue
            print("%s %-3s %-24s %-18s %s%s" % ("x" if f["id"] in kul else " ", f["tur"], f["id"], f["grup"],
                                             " ".join(f.get("question") or f.get("hook")), "" if f.get("dogrulandi") else "  (doğrulanacak)"))
    if tur in (None, "ipucu"):
        for k in d["ipucu"]:
            print("  ipucu %s%s" % (k["konu"], "" if k.get("dogrulandi") else "  (doğrulanacak)"))
    print("\nx = kullanıldı ya da kuyrukta")


def karne():
    puan, sayi = kalip_puani(oku("state.json"))
    if not sayi:
        print("Karnede kanca kalıbı yazılı Reels yok. Kalıp ve kurgu, weeks/*.json içindeki kanca_kalibi ve cift alanlarından okunur.")
    for a, n in sorted(sayi.items()):
        print("%-16s %d Reels%s" % (a, n, "  geçme oranı ortalaması %%%.0f" % puan[a] if a in puan else "  (kıyas için en az 2 gerekir)"))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("liste", "sec", "kuyruk", "karne"):
        raise SystemExit(__doc__)
    if a[0] == "liste":
        liste(a[1] if len(a) > 1 else None)
    elif a[0] == "sec":
        sec(a[1])
    elif a[0] == "kuyruk":
        kuyruk(a[1])
    else:
        karne()
