#!/usr/bin/env python3
"""Onaydan sonraki işler: dosyaları kopyala, Metricool isteklerini hazırla, durumu kaydet.

Kullanım:
  python3 planla.py kopyala <HAFTA>
      Onaylanan dosyaları out/<HAFTA>/ klasöründen posts/<HAFTA>/ klasörüne kopyalar
      (kaydırmalı: <id>-NN.png, tekli: <id>.png, Reels: <id>.mp4 ve <id>-kapak.jpg).
      Önizleme dosyaları kopyalanmaz.

  python3 planla.py json <HAFTA> <COMMIT_SHA> [--saat <id>=HH:MM] [--tarih <id>=YYYY-MM-DD] [--muzik <id>=<audioId>] [--ham]
      Her gönderi için createScheduledPost'a verilecek 'date' ve 'info' değerlerini JSON dizisi olarak yazar.
      Görseller raw.githubusercontent.com, videolar jsDelivr (@COMMIT_SHA) adresinden verilir.
      --ham   : videoları da raw.githubusercontent.com adresinden ver (jsDelivr reddedilirse yedek)
      --saat / --tarih : geç gelen onayda saati ya da günü değiştirmek için
      --muzik : yalnız Facebook bağlantısı varken, Reels'e müzik (Metricool audioId: numara ya da arama terimi)

  python3 planla.py durum <HAFTA> [--linkler <dosya.json>]
      state.json'u günceller (posted, planned_weeks, recent_groups, last_product_theme, last_tekli_week)
      ve kullanılan öğeleri queue.json'dan düşer. --linkler: {"<id>": "<Metricool plannerUrl>"} biçiminde dosya.
      Verilmezse bağlantı haftanın dosyasındaki "metricool" alanından alınır.

Önceden planlanmış haftalar (weeks/<HAFTA>.json içinde "on_planli": true; ROBOT.md'ye bak):
  python3 planla.py stok <HAFTA>
      Ürünlerin stokta olduğunu ve kampanya kartındaki eşiklerin sitede aynı yazdığını denetler.
      Çıkış kodu 0: sorun yok; 2: SORUNLU gönderi var; 3: bazıları denetlenemedi.
  python3 planla.py yedek <HAFTA> <id> <COMMIT_SHA>
      Sıradaki kullanılmamış yedeği (weeks/yedek.json) o gönderinin gününe ve saatine koyan
      updateScheduledPost isteğini yazar: yedek, date, uuid, info.
  python3 planla.py yedek <HAFTA> <id> --uygula <yedek_anahtarı> [--neden "<metin>"]
      Metricool güncellendikten SONRA çalıştırılır: haftanın dosyasında gönderiyi yedekle değiştirir,
      state.json'da yedeği kullanılmış sayar ve not düşer.
  python3 planla.py yakala <HAFTA>
      HAFTA'dan önceki, önceden planlanmış ama durumu kaydedilmemiş haftalar için 'durum' çalıştırır.
"""
import glob
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("IG_REPO", "cnbrnc/tuzla-instagram")
TZ_OFFSET = "+03:00"  # Türkiye, yaz saati uygulaması yok


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def week(hafta):
    return load(os.path.join(ROOT, "weeks", hafta + ".json"))


def files_for(post, folder):
    pid = post["id"]
    if post.get("format") == "reel" or post.get("template") == "reel":
        names = [pid + ".mp4", pid + "-kapak.jpg"]
    elif post.get("slides"):
        names = sorted(os.path.basename(p) for p in glob.glob(os.path.join(folder, pid + "-[0-9][0-9].png")))
        if len(names) != len(post["slides"]):
            raise SystemExit("HATA: %s için %d slayt bekleniyordu, %d PNG bulundu" % (pid, len(post["slides"]), len(names)))
    else:
        names = [pid + ".png"]
    return names


def opts(args, flag):
    out = {}
    for i, a in enumerate(args):
        if a == flag:
            k, v = args[i + 1].split("=", 1)
            out[k] = v
    return out


def cmd_kopyala(hafta):
    src, dst = os.path.join(ROOT, "out", hafta), os.path.join(ROOT, "posts", hafta)
    os.makedirs(dst, exist_ok=True)
    for post in week(hafta)["posts"]:
        for name in files_for(post, src):
            if not os.path.exists(os.path.join(src, name)):
                raise SystemExit("HATA: dosya yok: out/%s/%s" % (hafta, name))
            shutil.copy2(os.path.join(src, name), os.path.join(dst, name))
            print("kopyalandı: posts/%s/%s" % (hafta, name))


def make_info(post, local, names, raw, cdn, ham=False, audio=None):
    """createScheduledPost ve updateScheduledPost için 'info' sözlüğü."""
    is_reel = post.get("format") == "reel" or post.get("template") == "reel"
    info = {
        "autoPublish": True, "draft": False, "text": post["caption"],
        "providers": [{"network": "instagram"}],
        "publicationDate": {"dateTime": local, "timezone": "Europe/Istanbul"},
        "firstCommentText": "", "shortener": False, "smartLinkData": {"ids": []},
        "descendants": [], "hasNotReadNotes": False,
    }
    if is_reel:
        info["media"] = [(raw if ham else cdn) + names[0]]
        info["mediaAltText"] = []
        info["videoCoverMilliseconds"] = 1200
        info["instagramData"] = {"type": "REEL", "showReelOnFeed": True}
        if audio:
            # Videonun kendi efektleri (ses: "efekt") müziğin altında kalsın
            info["instagramData"]["audioConfiguration"] = {"audioId": audio, "videoVolume": 50}
    else:
        info["media"] = [raw + n for n in names]
        alt = post.get("alt")
        if isinstance(alt, str):
            alt = [alt]
        info["mediaAltText"] = alt if alt and len(alt) == len(names) else []
        info["instagramData"] = {"type": "POST"}
    return info


def cmd_json(hafta, sha, args):
    saat, tarih, muzik = opts(args, "--saat"), opts(args, "--tarih"), opts(args, "--muzik")
    ham = "--ham" in args
    raw = "https://raw.githubusercontent.com/%s/%s/posts/%s/" % (REPO, sha, hafta)
    cdn = "https://cdn.jsdelivr.net/gh/%s@%s/posts/%s/" % (REPO, sha, hafta)
    folder = os.path.join(ROOT, "posts", hafta)
    result = []
    for post in week(hafta)["posts"]:
        pid = post["id"]
        day = tarih.get(pid, post["date"])
        hm = saat.get(pid, "10:00")
        local = "%sT%s:00" % (day, hm)
        info = make_info(post, local, files_for(post, folder), raw, cdn, ham, muzik.get(pid))
        result.append({"id": pid, "date": local + TZ_OFFSET, "info": json.dumps(info, ensure_ascii=False)})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_durum(hafta, args):
    links = {}
    if "--linkler" in args:
        links = load(args[args.index("--linkler") + 1])
    wk = week(hafta)
    state_path, queue_path = os.path.join(ROOT, "state.json"), os.path.join(ROOT, "queue.json")
    state, queue = load(state_path), load(queue_path)
    used = set()
    for post in wk["posts"]:
        state.setdefault("posted", []).append({
            "date": post["date"] + "T10:00:00", "id": post["id"], "type": post.get("format"),
            "key": post.get("key"), "group": post.get("group", ""), "url": post.get("url", ""),
            "metricool": links.get(post["id"]) or (post.get("metricool") or {}).get("url", ""),
        })
        used.add(post.get("key"))
        if post.get("group"):
            state["recent_groups"] = (state.get("recent_groups", []) + [post["group"]])[-6:]
        if post.get("format") == "carousel" and post.get("url"):
            state["last_product_theme"] = post.get("theme", state.get("last_product_theme"))
        if post.get("format") == "tekli":
            state["last_tekli_week"] = hafta
    n_reels = sum(1 for p in wk["posts"] if p.get("format") == "reel" or p.get("template") == "reel")
    state["ses_sirasi"] = state.get("ses_sirasi", 0) + n_reels
    if hafta not in state.setdefault("planned_weeks", []):
        state["planned_weeks"].append(hafta)
    for k in ("reels", "urun_carousel", "ipucu_carousel", "tekli"):
        queue[k] = [it for it in queue.get(k, []) if it.get("key") not in used]
    save(state_path, state)
    save(queue_path, queue)
    print("state.json ve queue.json güncellendi; düşülen öğeler:", ", ".join(sorted(k for k in used if k)))


# --- Önceden planlanmış haftalar (weeks/<HAFTA>.json içinde "on_planli": true) ---

SITE = "https://tuzlahirdavat.com.tr/"  # www'li adres bu ortamdan açılmıyor
KAMPANYA = [  # (ad, desen): anasayfa metninde (küçük harf) aranır
    ("3.000 TL üstü ücretsiz kargo",
     r"(?<![\d.])3\.?000 ?(tl|₺) ve üzeri (sepette kargo bedava|siparişlerinizde ücretsiz kargo)"),
    ("5.000 TL üstü vade farksız 3 taksit", r"(?<![\d.])5\.?000 ?(tl|₺).{0,60}?vade far\w* 3 taksit"),
    ("20.000 TL üstü vade farksız 6 taksit", r"(?<![\d.])20\.?000 ?(tl|₺).{0,60}?vade far\w* 6 taksit"),
]


def http_kodu(url):
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-L", "-m", "40", "-w", "%{http_code}", url],
                       capture_output=True, text=True)
    return r.stdout.strip() or "000"


def urun_kontrol(url, dest):
    """('TAMAM' | 'SORUN' | 'KONTROL EDİLEMEDİ', açıklama)"""
    kod = http_kodu(url)
    if kod in ("404", "410"):
        return "SORUN", "ürün sayfası kaldırılmış (HTTP %s)" % kod
    if kod != "200":
        return "KONTROL EDİLEMEDİ", "sayfa açılmadı (HTTP %s)" % kod
    shutil.rmtree(dest, ignore_errors=True)
    r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "fetch_product.py"), url, dest],
                       capture_output=True, text=True)
    pj = os.path.join(dest, "product.json")
    if r.returncode != 0 or not os.path.exists(pj):
        return "KONTROL EDİLEMEDİ", "ürün bilgisi okunamadı"
    stok = load(pj).get("availability", "")
    if stok == "InStock":
        return "TAMAM", "stokta"
    if not stok:
        return "KONTROL EDİLEMEDİ", "stok bilgisi yok"
    return "SORUN", "stokta değil (%s)" % stok


def kampanya_kontrol():
    import html as htmlmod
    import re
    r = subprocess.run(["curl", "-sSL", "-m", "40", SITE], capture_output=True)
    if r.returncode != 0 or len(r.stdout) < 10000:
        return "KONTROL EDİLEMEDİ", "anasayfa açılmadı"
    metin = re.sub(r"\s+", " ", htmlmod.unescape(r.stdout.decode("utf-8", "replace"))).lower()
    eksik = [ad for ad, desen in KAMPANYA if not re.search(desen, metin)]
    if eksik:
        return "SORUN", "sitede artık yazmıyor: " + "; ".join(eksik)
    return "TAMAM", "kargo ve taksit eşikleri sitede aynı"


def cmd_stok(hafta):
    """Önceden planlanmış haftanın ürünlerinin stokta olduğunu ve kampanya eşiklerinin değişmediğini denetler.
    Çıkış kodu: 0 her şey yolunda, 2 en az bir SORUN var, 3 sorun yok ama denetlenemeyen var."""
    sorunlu, belirsiz = [], []
    for post in week(hafta)["posts"]:
        pid = post["id"]
        if post.get("url"):
            durum, neden = urun_kontrol(post["url"], os.path.join(ROOT, "work", "stok", hafta, post["key"]))
        elif str(post.get("key", "")).startswith("kampanya"):
            durum, neden = kampanya_kontrol()
        else:
            durum, neden = "TAMAM", "denetim gerekmez (%s)" % post.get("format")
        print("%-17s %-40s %s" % (durum, pid, neden))
        if durum == "SORUN":
            sorunlu.append(pid)
        elif durum != "TAMAM":
            belirsiz.append(pid)
    print("SORUNLU:", ", ".join(sorunlu) or "yok")
    if belirsiz:
        print("DENETLENEMEDİ:", ", ".join(belirsiz))
    sys.exit(2 if sorunlu else 3 if belirsiz else 0)


def cmd_yedek(hafta, args):
    """yedek <HAFTA> <id> <SHA>                          sıradaki yedeğin Metricool isteğini yazar
       yedek <HAFTA> <id> --uygula <anahtar> [--neden ..]  Metricool güncellendikten sonra dosyalara işler"""
    if not args:
        raise SystemExit(__doc__)
    pid = args[0]
    wk_path = os.path.join(ROOT, "weeks", hafta + ".json")
    wk = load(wk_path)
    post = next((p for p in wk["posts"] if p["id"] == pid), None)
    if post is None:
        raise SystemExit("HATA: %s haftasında %s yok" % (hafta, pid))
    state_path = os.path.join(ROOT, "state.json")
    state = load(state_path)
    used = state.get("kullanilan_yedekler", [])
    yedekler = load(os.path.join(ROOT, "weeks", "yedek.json"))["posts"]

    if "--uygula" in args:
        key = args[args.index("--uygula") + 1]
        y = next((p for p in yedekler if p["key"] == key), None)
        if y is None:
            raise SystemExit("HATA: weeks/yedek.json içinde %s yok" % key)
        if key in used:
            raise SystemExit("HATA: %s yedeği daha önce kullanıldı" % key)
        neden = args[args.index("--neden") + 1] if "--neden" in args else "stok ya da kampanya denetimi"
        new = {k: v for k, v in y.items() if k not in ("id", "date")}
        new.update({"id": "%s-%s" % (post["date"], key), "date": post["date"], "format": y.get("format", "carousel"),
                    "key": key, "medya": "posts/yedek/%s-NN.png" % y["id"],
                    "yerine": {"id": post["id"], "key": post.get("key"), "neden": neden}})
        if post.get("metricool"):
            new["metricool"] = post["metricool"]
        wk["posts"] = [new if p["id"] == pid else p for p in wk["posts"]]
        save(wk_path, wk)
        state["kullanilan_yedekler"] = used + [key]
        state.setdefault("notes", []).append("%s: %s yerine yedek gönderi %s planlandı (%s)." % (
            post["date"], post.get("key"), key, neden))
        save(state_path, state)
        print("işlendi: %s → %s (weeks/%s.json, state.json)" % (pid, new["id"], hafta))
        return

    if len(args) < 2:
        raise SystemExit("HATA: commit kimliği (SHA) gerekli")
    sha = args[1]
    y = next((p for p in yedekler if p["key"] not in used), None)
    if y is None:
        raise SystemExit("HATA: kullanılmamış yedek kalmadı")
    raw = "https://raw.githubusercontent.com/%s/%s/posts/yedek/" % (REPO, sha)
    cdn = "https://cdn.jsdelivr.net/gh/%s@%s/posts/yedek/" % (REPO, sha)
    local = "%sT10:00:00" % post["date"]
    info = make_info(y, local, files_for(y, os.path.join(ROOT, "posts", "yedek")), raw, cdn)
    print(json.dumps({"yedek": y["key"], "yerine": pid, "date": local + TZ_OFFSET,
                      "uuid": (post.get("metricool") or {}).get("uuid", ""),
                      "info": json.dumps(info, ensure_ascii=False)}, ensure_ascii=False, indent=2))


def cmd_yakala(hafta):
    """Tarihi HAFTA'dan önce olan, önceden planlanmış ama durumu henüz kaydedilmemiş haftaları sırayla kaydeder."""
    done = set(load(os.path.join(ROOT, "state.json")).get("planned_weeks", []))
    bekleyen = []
    for path in sorted(glob.glob(os.path.join(ROOT, "weeks", "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].json"))):
        ad = os.path.basename(path)[:-5]
        if ad < hafta and ad not in done and load(path).get("on_planli"):
            bekleyen.append(ad)
    if not bekleyen:
        print("kaydedilecek eski hafta yok")
    for ad in bekleyen:
        print("kaydediliyor:", ad)
        cmd_durum(ad, [])


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        raise SystemExit(__doc__)
    if a[0] == "kopyala":
        cmd_kopyala(a[1])
    elif a[0] == "json" and len(a) >= 3:
        cmd_json(a[1], a[2], a[3:])
    elif a[0] == "durum":
        cmd_durum(a[1], a[2:])
    elif a[0] == "stok":
        cmd_stok(a[1])
    elif a[0] == "yedek":
        cmd_yedek(a[1], a[2:])
    elif a[0] == "yakala":
        cmd_yakala(a[1])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
