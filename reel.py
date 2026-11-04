#!/usr/bin/env python3
"""Reels videosu üretir (1080x1920, 30 fps, MP4).

Kullanım: python3 reel.py <hafta.json> <çıktı_klasörü>
hafta.json içinde template = "reel" olan gönderileri işler. Her biri için <id>.mp4 ve kapak <id>-kapak.jpg yazar.
Gerekli alanlar: hook (satırlar), hook_kicker, tag, brand, sku, title, chips, search_code, product_dir.
"""
import json
import os
import shutil
import subprocess
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
CHROME = "/usr/bin/google-chrome"
FPS = 30
SECONDS = 10
REEL_STYLE_DEFAULT = "max-width:860px;max-height:640px;width:auto;height:auto"


def reel_image_style(prod):
    w, h = prod.get("image_size", [800, 800])
    r = w / h
    if r > 4:
        return "width:900px;height:auto;transform:rotate(-14deg)"
    if r > 2.6:
        return "width:880px;height:auto;transform:rotate(-10deg)"
    if r >= 900 / 640:
        return "width:%dpx;height:auto;margin-top:40px" % min(900, int(w * 1.7))
    return "height:%dpx;width:auto;margin-top:40px" % min(640, int(h * 1.7))


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
        page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        for post in spec["posts"]:
            if post.get("template") != "reel":
                continue
            with open(os.path.join(post["product_dir"], "product.json"), encoding="utf-8") as f:
                prod = json.load(f)
            ctx = {"fontdir": os.path.join(ROOT, "node_modules"), "logo": os.path.join(ROOT, "assets", "logo.png"),
                   "accent": "#FFC629", "image": prod["image"], "panel_bg": prod.get("panel_bg", "#FFFFFF"),
                   "image_style": reel_image_style(prod)}
            ctx.update(post)
            html_path = os.path.join(out, "html", post["id"] + ".html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(env.get_template("reel.html").render(**ctx))
            page.goto("file://" + html_path)
            page.evaluate("document.fonts.ready.then(() => true)")
            page.evaluate("window.fitText()")
            page.wait_for_timeout(300)
            frames = os.path.join(out, "frames-" + post["id"])
            shutil.rmtree(frames, ignore_errors=True)
            os.makedirs(frames)
            total = FPS * SECONDS
            for i in range(total):
                t = i * 1000.0 / FPS
                page.evaluate("t => document.getAnimations().forEach(a => { a.pause(); a.currentTime = t; })", t)
                page.screenshot(path=os.path.join(frames, "f%04d.jpg" % i), type="jpeg", quality=92)
            mp4 = os.path.join(out, post["id"] + ".mp4")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(frames, "f%04d.jpg"),
                            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", mp4], check=True)
            shutil.copy(os.path.join(frames, "f%04d.jpg" % int(FPS * 1.2)), os.path.join(out, post["id"] + "-kapak.jpg"))
            shutil.rmtree(frames, ignore_errors=True)
            print("ok", mp4)
        browser.close()


if __name__ == "__main__":
    main()
