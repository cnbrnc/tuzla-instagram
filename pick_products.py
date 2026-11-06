#!/usr/bin/env python3
"""Sitemap'ten yeni gönderi adayları bulur.

Kullanım: python3 pick_products.py [aday_sayısı]
Paylaşılmış (state.json), kuyruktaki (queue.json) ve planlanmış haftalardaki (weeks/) ürünleri atlar,
son haftalarda kullanılan grupları geriye atar, stokta olmayanları eler.
Çıktı: aday listesi (JSON) — son seçimi ve metni robot yapar.
"""
import glob
import html
import json
import os
import random
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
SITEMAP = "https://tuzlahirdavat.com.tr/products.xml"
CACHE = os.path.join(ROOT, "work", "products.xml")

GROUPS = {
    "baglanti": r"civata|din-?9[0-9]{2}|iso-?[0-9]{4}|somun|-pul-|saplama|inox",
    "tork": r"tork",
    "pense": r"pense|yan-keski|kargaburun",
    "akulu": r"akulu|komursuz",
    "kaynak": r"kaynak-makin|inverter|gazalti",
    "fener": r"fener|kafa-lambasi|calisma-lambasi",
    "kilavuz/matkap": r"kilavuz|matkap-ucu|matkap-seti",
    "helikoil": r"helikoil|helicoil",
    "kimyasal": r"sprey|silikon|yapistirici|epoksi|crc|pas-sokucu",
    "isg": r"eldiven|cizme|ayakkabi|gozluk|maske|baret",
    "kaldirma": r"vinc|caraskal|transpalet|kriko|hubzug|manyetik-kaldirac",
    "panc": r"panc",
    "testere": r"testere",
    "olcu": r"kumpas|su-terazisi|serit-metre|lazer-metre|gonye|komparator",
    "el-aleti": r"lokma|anahtar-takimi|tornavida|cekic|bits",
}


def curl(url, out=None):
    cmd = ["curl", "-sSL", "-m", "60", url]
    if out:
        cmd += ["-o", out]
    r = subprocess.run(cmd, capture_output=True, check=True)
    return None if out else r.stdout.decode("utf-8", "replace")


def load_json(name, default):
    p = os.path.join(ROOT, name)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return default


def main():
    want = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    if not os.path.exists(CACHE) or time.time() - os.path.getmtime(CACHE) > 86400:
        curl(SITEMAP, CACHE)
    xml = open(CACHE, encoding="utf-8", errors="replace").read()
    entries = []
    for block in re.findall(r"<url>(.*?)</url>", xml, re.S):
        loc = re.search(r"<loc>([^<]+)</loc>", block)
        img = re.search(r"<image:loc>([^<]+)</image:loc>", block)
        mod = re.search(r"<lastmod>([^<]+)</lastmod>", block)
        if loc and img:
            entries.append({"url": loc.group(1), "image": img.group(1), "lastmod": mod.group(1) if mod else ""})

    state = load_json("state.json", {})
    queue = load_json("queue.json", {})
    used = {p.get("url") for p in state.get("posted", [])}
    for k in ("products", "reels", "urun_carousel", "tekli"):
        used |= {p.get("url") for p in queue.get(k, []) if isinstance(p, dict)}
    # Planlanmış haftalar (önceden planlananlar ve yedekler dahil) da kullanılmış sayılır
    for path in glob.glob(os.path.join(ROOT, "weeks", "*.json")):
        with open(path, encoding="utf-8") as f:
            used |= {p.get("url") for p in json.load(f).get("posts", []) if isinstance(p, dict)}
    recent = state.get("recent_groups", [])[-8:]

    order = sorted(GROUPS, key=lambda g: (recent.count(g), random.random()))
    if "baglanti" not in recent[-4:]:
        order.remove("baglanti")
        order.insert(0, "baglanti")

    out = []
    for g in order:
        pat = re.compile(GROUPS[g])
        pool = [e for e in entries if e["url"] not in used and pat.search(e["url"].rsplit("/", 1)[-1])]
        random.shuffle(pool)
        found = 0
        for e in pool[:8]:
            try:
                page = curl(e["url"])
            except Exception:
                continue
            m = None
            for block in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', page, re.S):
                try:
                    d = json.loads(block)
                except Exception:
                    continue
                for it in (d if isinstance(d, list) else d.get("@graph", [d])):
                    if isinstance(it, dict) and it.get("@type") == "Product":
                        m = it
            if not m:
                continue
            offers = m.get("offers") or {}
            if isinstance(offers, list):
                offers = offers[0] if offers else {}
            if "InStock" not in str(offers.get("availability", "")):
                continue
            brand = m.get("brand")
            if isinstance(brand, dict):
                brand = brand.get("name")
            out.append({"group": g, "url": e["url"], "name": html.unescape(m.get("name", "")),
                        "brand": brand or "", "lastmod": e["lastmod"]})
            found += 1
            if found >= 2:
                break
        if len(out) >= want:
            break
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
