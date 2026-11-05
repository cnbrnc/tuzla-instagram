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
"""
import glob
import json
import os
import shutil
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
        names = files_for(post, folder)
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
            if pid in muzik:
                # Videonun kendi efektleri (ses: "efekt") müziğin altında kalsın
                info["instagramData"]["audioConfiguration"] = {"audioId": muzik[pid], "videoVolume": 50}
        else:
            info["media"] = [raw + n for n in names]
            alt = post.get("alt")
            if isinstance(alt, str):
                alt = [alt]
            info["mediaAltText"] = alt if alt and len(alt) == len(names) else []
            info["instagramData"] = {"type": "POST"}
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
            "metricool": links.get(post["id"], ""),
        })
        used.add(post.get("key"))
        if post.get("group"):
            state["recent_groups"] = (state.get("recent_groups", []) + [post["group"]])[-6:]
        if post.get("format") == "carousel" and post.get("url"):
            state["last_product_theme"] = post.get("theme", state.get("last_product_theme"))
        if post.get("format") == "tekli":
            state["last_tekli_week"] = hafta
    if hafta not in state.setdefault("planned_weeks", []):
        state["planned_weeks"].append(hafta)
    for k in ("reels", "urun_carousel", "ipucu_carousel", "tekli"):
        queue[k] = [it for it in queue.get(k, []) if it.get("key") not in used]
    save(state_path, state)
    save(queue_path, queue)
    print("state.json ve queue.json güncellendi; düşülen öğeler:", ", ".join(sorted(k for k in used if k)))


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
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
