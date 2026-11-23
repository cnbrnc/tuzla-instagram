#!/usr/bin/env python3
"""Reels videosu üretir (1080x1920, 30 fps, 9 sn, MP4).

Kullanım: python3 reel.py <hafta.json> <çıktı_klasörü>
hafta.json içinde template alanı "reel" ile başlayan gönderileri işler. Her biri için <id>.mp4 ve kapak <id>-kapak.jpg yazar.

Türler ve gerekli alanlar:
  reel      Ürün Reels'i: hook (satırlar), hook_kicker, tag, brand, sku, title, chips, search_code, product_dir.
  reel_bil  "Bil bakalım": tag, question_kicker, question (en çok 2 satır), options (2 adet: big ya da product_dir,
            isteğe bağlı label), answer (0 ya da 1), answer_text, why (en çok 2 satır), search_code.
  reel_yd   "Yanlış / doğru": tag, hook_kicker, hook (satırlar), yanlis ve dogru ({ne, alt, product_dir}),
            why (isteğe bağlı why_kicker), search_code. Panelde görsel yoksa yazı tüm genişliği kullanır.
            cift: damga çifti. "yanlis-dogru" (varsayılan), "efsane-gercek", "zor-kolay" (çarpı ve hata sesi yok).
            hook_image: kancada yanlış ürün yerine gösterilecek görsel (isteğe bağlı).
  Yeni türlerde seçenek yazısı iki satırsa big yerine lines = ["ÜST", "ALT"] verilir.
  urun = {marka, ad, ozellik} ve product_dir verilirse kapanış kartında ürünün fotoğrafı ve adı durur (ürün tanıtımı).
  Seçeneklerde ve panellerde image_shape = "daire" yuvarlak ürünü (disk, taş) daire içinde gösterir.

İsteğe bağlı (yeni türlerde): stil = "sinematik" (koyu sahne, film greni, fragman havasında ses) ve onunla birlikte
bg_video = {"file": "<yerel mp4>", "start": sn, "x": 0–1 (kırpmanın yatay merkezi), "pan": kayma oranı, "hiz": 1.0}.
muzik = "a" | "b" | "c": stok müzikli profesyonel ses (ses_pro.py); sfx_kanca = "taslama" kancaya gerçek taşlama sesi ekler.
bg_video varsa gerçek görüntü zemine konur: şablon saydam çizilir ve ffmpeg ile görüntünün üstüne bindirilir.
Stok görüntü depoya yüklenmez (lisans); hafta.py onu kaynağından work/stok/ klasörüne indirir.

İsteğe bağlı: ses. Ürün Reels'inde "enerjik" (varsayılan), "atolye", "derin", "efekt" (yalnız efekt; Instagram
müziği eklenecekse); yeni türlerde kendi sesi ("bil", "yd") varsayılandır. "yok" sessiz üretir.
Video ve ses döngüde başa kesintisiz bağlanır.
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
SECONDS = 9
REEL_STYLE_DEFAULT = "max-width:860px;max-height:640px;width:auto;height:auto"
# Kodla üretilmiş özgün ses izleri (ses.py). Zamanlama templates/reel.html ile aynıdır.
# Yeni türlerin sesi ses_tur.py ile üretilir; zamanlaması reel_bil.html ve reel_yd.html ile aynıdır.
SOUNDS = {k: os.path.join(ROOT, "assets", "reel-ses-%s.wav" % k)
          for k in ("enerjik", "atolye", "derin", "efekt", "bil", "yd", "bil-sin", "yd-sin")}
DEFAULT_SOUND = {"reel": "enerjik", "reel_bil": "bil", "reel_yd": "yd"}


def mutlak(yol):
    """Depoya göre verilmiş görsel yolunu tam yola çevirir (HTML başka klasörde açılır)."""
    return yol if not yol or os.path.isabs(yol) or "://" in yol else os.path.join(ROOT, yol)


def with_image(d):
    """product_dir verilmiş seçenek ya da panele ürün görselinin yolunu ekler."""
    if isinstance(d, dict) and d.get("product_dir") and not d.get("image"):
        with open(os.path.join(ROOT, d["product_dir"], "product.json"), encoding="utf-8") as f:
            d = dict(d, image=os.path.join(ROOT, d["product_dir"], "product.png"))
            if not os.path.exists(d["image"]):
                d["image"] = json.load(f)["image"]
    elif isinstance(d, dict) and d.get("image"):
        d = dict(d, image=mutlak(d["image"]))
    return d


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
            tpl = post.get("template") or ""
            if tpl not in DEFAULT_SOUND:
                continue
            ctx = {"fontdir": os.path.join(ROOT, "node_modules"), "logo": os.path.join(ROOT, "assets", "logo.png"),
                   "accent": "#FFC629"}
            if tpl == "reel":
                with open(os.path.join(post["product_dir"], "product.json"), encoding="utf-8") as f:
                    prod = json.load(f)
                ctx.update({"image": prod["image"], "panel_bg": prod.get("panel_bg", "#FFFFFF"),
                            "image_style": reel_image_style(prod)})
            ctx.update(post)
            bg = post.get("bg_video") if post.get("stil") == "sinematik" and tpl != "reel" else None
            if bg and not os.path.exists(bg["file"]):
                raise SystemExit("HATA: zemin videosu yok: %s" % bg["file"])
            ctx["video_zemin"] = bool(bg)
            # zeminin bulanıklaşıp karardığı an: Yanlış/doğru'da ilk panel (1,4 sn), Bil bakalım'da geri sayım (1,0 sn)
            ctx["bg_gecis"] = gecis = float(post.get("bg_gecis", 1.0 if tpl == "reel_bil" else 1.4))
            if tpl == "reel_bil":
                ctx["options"] = [with_image(o) for o in post["options"]]
            elif tpl == "reel_yd":
                ctx["yanlis"], ctx["dogru"] = with_image(post["yanlis"]), with_image(post["dogru"])
                ctx["hook_image"] = mutlak(post.get("hook_image"))
            # Kapanışta ürün: "urun" = {marka, ad, ozellik} ve product_dir varsa ürün fotoğrafı kapanış kartına girer
            if tpl != "reel" and post.get("urun") and post.get("product_dir"):
                ctx["urun_gorsel"] = with_image({"product_dir": post["product_dir"]})["image"]
            html_path = os.path.join(out, "html", post["id"] + ".html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(env.get_template(tpl + ".html").render(**ctx))
            page.goto("file://" + html_path)
            page.evaluate("document.fonts.ready.then(() => true)")
            # Yazı sığdırma, animasyonlar durgunken yapılır (1,2 sn): büyüyerek gelen satırlar ölçümü bozmasın
            page.evaluate("document.getAnimations().forEach(a => { a.pause(); a.currentTime = 1200; })")
            page.evaluate("window.fitText()")
            page.wait_for_timeout(300)
            frames = os.path.join(out, "frames-" + post["id"])
            shutil.rmtree(frames, ignore_errors=True)
            os.makedirs(frames)
            total = FPS * SECONDS
            for i in range(total):
                t = i * 1000.0 / FPS
                page.evaluate("t => { document.getAnimations().forEach(a => { a.pause(); a.currentTime = t; }); if (window.setTime) window.setTime(t); }", t)
                if bg:   # saydam kare: gerçek görüntünün üstüne bindirilecek
                    page.screenshot(path=os.path.join(frames, "f%04d.png" % i), type="png", omit_background=True)
                else:
                    page.screenshot(path=os.path.join(frames, "f%04d.jpg" % i), type="jpeg", quality=92)
            mp4 = os.path.join(out, post["id"] + ".mp4")
            # Ses: ritim adı (varsayılan "enerjik"), "efekt" (Instagram müziği eklenecekse) ya da "yok"
            varsayilan = DEFAULT_SOUND[tpl] + ("-sin" if post.get("stil") == "sinematik" and tpl != "reel" else "")
            audio = SOUNDS.get(post.get("ses") or varsayilan)
            # Profesyonel ses (stok müzik + efekt): "muzik": "a" | "b" | "c". Üretilemezse kodla üretilmiş ses kalır.
            if post.get("muzik") and post.get("stil") == "sinematik" and tpl != "reel" and not post.get("ses"):
                tur = DEFAULT_SOUND[tpl]
                komut = [sys.executable, os.path.join(ROOT, "ses_pro.py"), tur, post["muzik"]]
                if post.get("sfx_kanca") == "taslama" and tur == "yd":
                    komut.append("--taslama")
                if post.get("cift") == "zor-kolay" and tur == "yd":
                    komut.append("--yumusak")
                r = subprocess.run(komut, capture_output=True, text=True, cwd=ROOT)
                yol = os.path.join(ROOT, r.stdout.strip().splitlines()[-1]) if r.returncode == 0 and r.stdout.strip() else ""
                if yol and os.path.exists(yol):
                    audio = yol
                else:
                    print("UYARI: profesyonel ses üretilemedi, kodla üretilmiş ses kullanılıyor:", post["id"])
            if audio and os.path.exists(audio):
                audio_in = ["-i", audio]
                audio_fx = ["-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100"]
            else:
                audio_in = ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
                audio_fx = []
            if bg:
                # Zemin: dikey kırp (yavaş kaydırma), renk ve kontrast, panel gelince bulanıklaş, hafif gren; üstüne şablon
                zemin = ("[0:v]setpts=PTS/%s,fps=%d,crop=ih*9/16:ih:x='min(max(iw*%s-ow/2+iw*%s*t/%d\\,0)\\,iw-ow)':y=0,"
                         "scale=1080:1920:flags=lanczos,eq=contrast=1.14:saturation=1.12:brightness=-0.03,"
                         "gblur=sigma=16:enable='gte(t,%s)',noise=alls=6:allf=t[bg];[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v]"
                         % (bg.get("hiz", 1.0), FPS, bg.get("x", 0.5), bg.get("pan", 0.0), SECONDS, gecis))
                video_in = ["-stream_loop", "-1", "-ss", str(bg.get("start", 0)), "-i", bg["file"],
                            "-framerate", str(FPS), "-i", os.path.join(frames, "f%04d.png")]
                video_map = ["-filter_complex", zemin, "-map", "[v]", "-map", "2:a", "-t", str(SECONDS)]
            else:
                video_in = ["-framerate", str(FPS), "-i", os.path.join(frames, "f%04d.jpg")]
                video_map = []
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + video_in
                           + audio_in + video_map + ["-shortest", "-c:v", "libx264", "-preset", "veryfast",
                                         # film greni dosyayı büyütür; sinematik stilde biraz daha sıkıştır (jsDelivr sınırı 20 MB)
                                         "-crf", "24" if post.get("stil") == "sinematik" else "20", "-pix_fmt", "yuv420p"]
                           + audio_fx + ["-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", mp4], check=True)
            kapak = os.path.join(out, post["id"] + "-kapak.jpg")
            if bg:
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.2", "-i", mp4, "-frames:v", "1", "-q:v", "3", kapak], check=True)
            else:
                shutil.copy(os.path.join(frames, "f%04d.jpg" % int(FPS * 1.2)), kapak)
            shutil.rmtree(frames, ignore_errors=True)
            print("ok", mp4)
        browser.close()


if __name__ == "__main__":
    main()
