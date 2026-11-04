#!/usr/bin/env python3
"""Ürün sayfasından bilgi ve görsel çeker.

Kullanım: python3 fetch_product.py <ürün_sayfası_url> <çıktı_klasörü>
Çıktı: <çıktı_klasörü>/product.json ve product.png (kenar boşluğu kırpılmış görsel)
"""
import html as htmlmod
import json
import os
import re
import subprocess
import sys

from PIL import Image


def get(url, binary=False):
    r = subprocess.run(["curl", "-sSL", "-m", "40", url], capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def product_from_jsonld(page):
    for block in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', page, re.S):
        try:
            data = json.loads(block)
        except Exception:
            continue
        items = data if isinstance(data, list) else data.get("@graph", [data])
        for it in items:
            if isinstance(it, dict) and it.get("@type") == "Product":
                return it
    return None


def trim_white(im, thr=242, pad=0.04):
    rgb = im.convert("RGB")
    mask = rgb.convert("L").point(lambda v: 255 if v < thr else 0)
    box = mask.getbbox()
    if not box:
        return rgb
    c = rgb.crop(box)
    w, h = c.size
    p = int(max(w, h) * pad)
    out = Image.new("RGB", (w + 2 * p, h + 2 * p), (255, 255, 255))
    out.paste(c, (p, p))
    return out


def border_info(im):
    rgb = im.convert("RGB")
    w, h = rgb.size
    pts = [(x, 0) for x in range(0, w, max(1, w // 40))] + [(x, h - 1) for x in range(0, w, max(1, w // 40))]
    pts += [(0, y) for y in range(0, h, max(1, h // 40))] + [(w - 1, y) for y in range(0, h, max(1, h // 40))]
    px = [rgb.getpixel(p) for p in pts]
    avg = tuple(sum(c[i] for c in px) // len(px) for i in range(3))
    white = all(min(c) >= 238 for c in px)
    return white, "#%02X%02X%02X" % avg


def image_style(w, h, non_white):
    r = w / h
    if non_white:
        target = min(560, int(h * 1.6))
        return "height:%dpx;width:auto;max-width:880px;margin-top:36px;border-radius:16px" % target
    if r > 4:
        return "width:860px;height:auto;transform:rotate(-14deg)"
    if r > 2.6:
        return "width:820px;height:auto;transform:rotate(-10deg)"
    if r >= 880 / 560:
        return "width:%dpx;height:auto;margin-top:36px" % min(880, int(w * 1.6))
    return "height:%dpx;width:auto;margin-top:36px" % min(560, int(h * 1.6))


def main():
    url, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    page = get(url)
    prod = product_from_jsonld(page) or {}
    images = prod.get("image") or []
    if isinstance(images, str):
        images = [images]
    offers = prod.get("offers") or {}
    if isinstance(offers, list):
        offers = offers[0] if offers else {}
    brand = prod.get("brand")
    if isinstance(brand, dict):
        brand = brand.get("name")
    info = {
        "url": url,
        "name": htmlmod.unescape(prod.get("name", "")),
        "brand": brand or "",
        "sku": prod.get("sku", ""),
        "description": htmlmod.unescape(re.sub(r"<[^>]+>", " ", prod.get("description", "") or "")).strip(),
        "availability": (offers.get("availability") or "").rsplit("/", 1)[-1],
        "images": images,
    }
    if images:
        raw = os.path.join(out, "raw_image")
        with open(raw, "wb") as f:
            f.write(get(images[0], binary=True))
        im = Image.open(raw)
        white, edge = border_info(im)
        final = trim_white(im) if white else im.convert("RGB")
        final_path = os.path.join(out, "product.png")
        final.save(final_path, optimize=True)
        w, h = final.size
        info.update({
            "image": os.path.abspath(final_path),
            "image_size": [w, h],
            "panel_bg": "#FFFFFF" if white else edge,
            "image_style": image_style(w, h, not white),
        })
    with open(os.path.join(out, "product.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print(json.dumps({k: info[k] for k in ("name", "brand", "sku", "availability")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
