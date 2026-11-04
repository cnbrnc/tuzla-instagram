#!/usr/bin/env python3
"""Haftalık gönderi listesini 1080x1350 PNG'lere çevirir.

Kullanım: python3 render.py <hafta.json> <çıktı_klasörü>
hafta.json: {"posts": [ {id, template, theme, tag, ...şablon alanları} ]}
urun şablonu için "product_dir" verilirse product.json içindeki görsel, stil ve zemin rengi kullanılır.
"""
import json
import os
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
CHROME = "/usr/bin/google-chrome"


def build_html(env, post):
    ctx = {
        "fontdir": os.path.join(ROOT, "node_modules"),
        "logo": os.path.join(ROOT, "assets", "logo.png"),
        "accent": "#FFC629",
        "title": post.get("id", "gonderi"),
    }
    ctx.update(post)
    if post.get("template") == "urun" and post.get("product_dir"):
        with open(os.path.join(post["product_dir"], "product.json"), encoding="utf-8") as f:
            prod = json.load(f)
        for k in ("image", "image_style", "panel_bg"):
            ctx.setdefault(k, prod.get(k))
    ctx.setdefault("panel_bg", "#FFFFFF")
    for key in ("illustration", "icon"):
        fname = post.get(key + "_file")
        if fname:
            with open(os.path.join(ROOT, fname), encoding="utf-8") as f:
                ctx[key] = f.read()
    return env.get_template(post["template"] + ".html").render(**ctx)


def main():
    spec_path, out = sys.argv[1], os.path.abspath(sys.argv[2])
    os.makedirs(os.path.join(out, "html"), exist_ok=True)
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "templates")),
                      autoescape=select_autoescape(["html"]))
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, args=[
            "--no-sandbox", "--no-first-run", "--disable-background-networking",
            "--disable-component-update", "--disable-sync", "--allow-file-access-from-files"])
        page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for post in spec["posts"]:
            items = []
            if post.get("slides"):
                # Kaydırmalı gönderi: her slayt ayrı PNG (id-01, id-02, ...); sağ üstte sayaç
                n = len(post["slides"])
                for i, s in enumerate(post["slides"], 1):
                    item = {k: v for k, v in post.items() if k not in ("slides", "caption", "tag")}
                    item.update(s)
                    item["id"] = "%s-%02d" % (post["id"], i)
                    item.setdefault("tag", "%d / %d" % (i, n))
                    items.append(item)
            elif post.get("template") == "reel":
                continue  # videolar reel.py ile üretilir
            else:
                items.append(post)
            for item in items:
                html_path = os.path.join(out, "html", item["id"] + ".html")
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(build_html(env, item))
                page.goto("file://" + html_path)
                page.evaluate("document.fonts.ready.then(() => true)")
                page.evaluate("window.fitText()")
                page.wait_for_timeout(150)
                png = os.path.join(out, item["id"] + ".png")
                page.locator("#post").screenshot(path=png)
                print("ok", png)
        browser.close()


if __name__ == "__main__":
    main()
