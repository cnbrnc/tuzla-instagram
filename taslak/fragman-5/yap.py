#!/usr/bin/env python3
"""TASLAK (23 Kasım 2026, onay bekliyor): 5 ürün için "Fragman" türünde tanıtım Reels'i.

Kullanım (depo kökünden):
  python3 taslak/fragman-5/yap.py --indir   # ürün sayfalarını ve stok videoları work/ altına indirir
  python3 taslak/fragman-5/yap.py           # taslak/fragman-5/fragman-5.json dosyasını yazar
  python3 reel.py taslak/fragman-5/fragman-5.json out/fragman5
Bütün özellikler ürün sayfasından ya da ürün fotoğrafındaki etiketten alındı (23 Kasım 2026). Fiyat yok.
"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = "https://tuzlahirdavat.com.tr/"
P = "https://videos.pexels.com/video-files/"
STOK = {  # dosya adı → kaynak adresi (Pexels ve Pixabay lisansı; depoya konmaz)
    "pexels-5846450": P + "5846450/5846450-hd_1080_1920_25fps.mp4", "pexels-6046362": None, "pixabay-94063": "https://cdn.pixabay.com/video/2021/10/31/94063-641767740_large.mp4",
    "pexels-2386581": P + "2386581/2386581-uhd_4096_2160_24fps.mp4", "pexels-6046352": P + "6046352/6046352-hd_1920_1080_24fps.mp4",
    "pexels-9373200": None, "pexels-6685025": P + "6685025/6685025-hd_1920_1080_30fps.mp4", "pexels-4941356": P + "4941356/4941356-hd_1920_1080_25fps.mp4",
    "pexels-13159531": P + "13159531/13159531-hd_1920_1080_60fps.mp4", "pexels-5038492": P + "5038492/5038492-hd_1920_1080_24fps.mp4",
    "pexels-8851164": P + "8851164/8851164-hd_1920_1080_30fps.mp4"}
SON = "\n🛒 tuzlahirdavat.com.tr\n✉️ Sipariş: satis5@tuzlacivata.com.tr\n📞 0542 189 02 69\n\n"


GAMMA = {"pexels-5846450": 1.7, "pexels-6046352": 1.5, "pexels-2386581": 1.35, "pexels-9373200": 1.25}   # karanlık kesitler


def s(dosya, start, x=0.5, hiz=1.0, pan=0.02):
    return {"file": "work/stok/%s.mp4" % dosya, "url": STOK.get(dosya), "start": start, "x": x, "pan": pan, "hiz": hiz,
            "gamma": GAMMA.get(dosya, 1.0)}


URUNLER = [
 dict(key="karbosan-thinline", slug="115x1-6x22-nk-thinline-kesme-tasi-karbosan", group="asindirici", tag="KESME TAŞI",
      replikler=[["DEMİRİ", "KES."], ["PROFİLİ", "KES."], ["İNCE", "KES."], ["KARBOSAN'LA", "KES."]],
      sahneler=[s("pexels-5846450", 3), s("pixabay-94063", 1, .6), s("pexels-6046362", 5, .55), s("pexels-5846450", 14)],
      baslik="KARBOSAN", tur_yazi="THINLINE KESME TAŞI", ozellikler=["115 × 1,6 mm", "Çelik ve demir", "13.300 dev/dk"],
      slogan="Kesmeye özel taş: taşlama yapma.", search_code="910450",
      urun={"kicker": "SİTEMİZDE", "marka": "KARBOSAN", "ad": "NK Thinline kesme taşı", "ozellik": "115 × 1,6 × 22,23 mm · çelik"},
      kaynak="Ürün adı ve ürün fotoğrafındaki etiket: 115 x 1,6 x 22,23 mm, STEEL, max 13.300 RPM, 80 m/s, 'Taşlama yapmayınız'.",
      giris="Karbosan NK Thinline kesme taşı: 115 × 1,6 mm, çelik ve demir kesimi için. ⚙️\n\nEn yüksek devir 13.300 dev/dk (80 m/sn). Yalnız kesme içindir; etiketinde de yazar: taşlama yapmayınız.",
      cagri="📤 Demirci arkadaşına gönder.", etiket="#kesmetaşı #karbosan #demirci #aşındırıcı #tuzlahırdavat"),
 dict(key="tyrolit-flap", slug="115x60-inoxst-flap-disk-one-serisi-tyrolit-34689695", group="asindirici", tag="FLAP DİSK",
      replikler=[["KAYNAK", "DİKİŞİ."], ["PAS."], ["YÜZEY", "TEMİZLİĞİ."], ["TEK DİSK", "YETER."]],
      sahneler=[s("pexels-6046352", 4, .45), s("pexels-5846450", 8), s("pexels-6046352", 11, .45), s("pexels-5846450", 20)],
      baslik="TYROLIT ONE", tur_yazi="2'Sİ 1 ARADA FLAP DİSK", ozellikler=["115 mm · 60 kum", "Çelik ve paslanmaz", "Zirkonyum"],
      slogan="Disk değiştirmeden çelik ve paslanmaz.", search_code="34689695",
      urun={"kicker": "SİTEMİZDE", "marka": "TYROLIT", "ad": "ONE 2in1 flap disk", "ozellik": "115 mm · 60 kum · zirkonyum"},
      kaynak="Ürün sayfası: 2in1 (çelik ve paslanmaz), 60 kum zirkonyum alüminyum, 115 mm, 22,23 mm göbek; taşlama, pas alma, kaynak dikişi düzeltme, yüzey temizleme.",
      giris="Tyrolit ONE 2in1 flap disk: 115 mm, 60 kum; çelikte de paslanmazda da aynı diskle çalış. 🔧\n\nZirkonyum aşındırıcı ile kaynak dikişi düzeltme, pas alma ve yüzey temizleme. Fiberglas altlık, 22,23 mm göbek; 115'lik avuç taşlamaya uyar.",
      cagri="📤 Kaynakçı arkadaşına gönder.", etiket="#flapdisk #tyrolit #kaynakçı #aşındırıcı #tuzlahırdavat"),
 dict(key="egesan-inox", slug="115x1x22-inox-kesme-tasi-pro-serisi-egesan--8697442725817", group="asindirici", tag="İNOX KESME",
      replikler=[["PASLANMAZ", "KESİLECEK."], ["ISI", "AZ OLSUN."], ["KESİM", "İNCE OLSUN."], ["TAŞ", "İNOX OLSUN."]],
      sahneler=[s("pexels-2386581", 3, .6), s("pixabay-94063", 5, .6), s("pexels-6046362", 12, .55), s("pexels-2386581", 14, .6)],
      baslik="EGESAN PRO", tur_yazi="İNOX İNCE KESME TAŞI", ozellikler=["115 × 1 mm", "Paslanmaz ve çelik", "13.300 dev/dk"],
      slogan="Soğuk kesim: malzemede en az ısı.", search_code="Egesan inox",
      urun={"kicker": "SİTEMİZDE", "marka": "EGESAN", "ad": "Pro serisi inox kesme taşı", "ozellik": "115 × 1 × 22 mm"},
      kaynak="Ürün sayfası: 115 mm çap, 1 mm kalınlık, paslanmaz ve çelikte ince kesim, soğuk kesim (minimum ısı), 13.300 rpm, 80 m/s, Türkiye'de üretim.",
      giris="Egesan Pro inox ince kesme taşı: 115 × 1 mm, paslanmaz ve çelikte ince kesim. ✨\n\nSoğuk kesim sayesinde malzemede ısı az oluşur. En yüksek devir 13.300 dev/dk (80 m/sn). Türkiye'de üretilir.",
      cagri="📤 Paslanmazcı arkadaşına gönder.", etiket="#inoxkesme #egesan #paslanmaz #aşındırıcı #tuzlahırdavat"),
 dict(key="izeltas-lokma-35", slug="1-4-1-2-lokma-anahtar-takimi-35parca-izeltas", group="el-aleti", tag="LOKMA TAKIMI",
      replikler=[["SOMUN", "SIKIŞMIŞ."], ["YER", "DAR."], ["ANAHTAR", "UYMUYOR."], ["TAKIMIN", "TAM OLSUN."]],
      sahneler=[s("pexels-9373200", 14, .62), s("pexels-6685025", 3, .66), s("pexels-4941356", .5, .56), s("pexels-9373200", 18, .62)],
      baslik="İZELTAŞ", tur_yazi="35 PARÇA LOKMA TAKIMI", ozellikler=["1/4\" ve 1/2\"", "35 parça", "Çantalı set"],
      slogan="Lokmalar ve cırcır kol tek çantada.", search_code="1113001038",
      urun={"marka": "İZELTAŞ", "ad": "Lokma anahtar takımı", "ozellik": "35 parça · 1/4\" ve 1/2\""},
      kaynak="Ürün adı: İzeltaş 1/4\"-1/2\" Lokma Anahtar Takımı 35 Parça 1113001038. Çanta, lokmalar ve cırcır kol ürün fotoğrafında görünüyor.",
      giris="İzeltaş 35 parça lokma anahtar takımı: 1/4\" ve 1/2\" lokmalar ve cırcır kol tek çantada. 🧰\n\nSanayi, atölye ve servis işleri için.",
      cagri="📤 Tamirci arkadaşına gönder.", etiket="#lokmatakımı #izeltaş #otoservis #elaletleri #tuzlahırdavat"),
 dict(key="paslanmaz-din933", slug="m8x100-inox-akb-civata-din933-a2-304", group="baglanti", tag="PASLANMAZ",
      replikler=[["YAĞMUR."], ["NEM."], ["GÜNEŞ."], ["BAĞLANTI", "DAYANSIN."]],
      sahneler=[s("pexels-13159531", 2, .35, .5), s("pexels-5038492", 1, .3), s("pexels-8851164", 3, .5), s("pexels-13159531", 6, .35, .5)],
      baslik="A2 PASLANMAZ", tur_yazi="ALTI KÖŞE BAŞLI CIVATA · DIN 933", ozellikler=["A2 (304)", "DIN 933", "Stoktan gönderim"],
      slogan="Deniz kenarı için A4 de var.", search_code="DIN 933 A2",
      urun={"kicker": "SİTEMİZDE", "marka": "PASLANMAZ", "ad": "Altı köşe başlı cıvata DIN 933", "ozellik": "A2 (304) kalite"},
      kaynak="Ürün sayfası: DIN 933, A2-304; tersane, yat, güneş enerjisi, su arıtma, gıda tesisleri. Sitede A4 (316) ürünler de var. A2/A4 farkı: A4 klorlu ve deniz ortamına daha dayanıklı (önceki doğrulama).",
      giris="A2 paslanmaz altı köşe başlı cıvata, DIN 933: dış ortamda, nemde ve yağmurda uzun ömürlü bağlantı. 🔩\n\nGüneş enerjisi, su arıtma, gıda tesisi ve endüstriyel mutfak imalatında kullanılır. Deniz kenarı ve klorlu ortam için A4 (316) kalite de sitemizde.",
      cagri="💾 Kaydet, lazım olur.", etiket="#paslanmazcıvata #inox #a2 #bağlantıelemanları #tuzlahırdavat"),
]

if "--indir" in sys.argv:
    for u in URUNLER:
        subprocess.run([sys.executable, "-I", os.path.join(ROOT, "fetch_product.py"), SITE + u["slug"], os.path.join(ROOT, "work", "f-" + u["key"])], check=True)
    os.makedirs(os.path.join(ROOT, "work", "stok"), exist_ok=True)
    for ad, url in STOK.items():
        hedef = os.path.join(ROOT, "work", "stok", ad + ".mp4")
        if url and not os.path.exists(hedef):
            subprocess.run(["curl", "-sSL", "-m", "300", "-A", "Mozilla/5.0", "-o", hedef, url], check=True)
    sys.exit(0)

posts = []
for i, u in enumerate(URUNLER):
    u = dict(u)
    cap = u.pop("giris") + "\n\n" + u.pop("cagri") + "\n🔎 Sitede “%s” arat" % u["search_code"] + SON + u.pop("etiket")
    assert len([w for w in cap.split() if w.startswith("#")]) == 5, u["key"]
    slug = u.pop("slug")
    posts.append(dict(u, id="fragman-" + u["key"], format="reel", template="reel_fragman", stil="sinematik", muzik="fgdhj"[i],     # her videoda ayrı parça (assets/ses-kaynak.json)
                      kanca_kalibi="fragman", kapak_ms=4900, url=SITE + slug, product_dir="work/f-" + u["key"], caption=cap,
                      kaynak_video="Pexels ve Pixabay lisansı; dosya adlarındaki numaralar video kimliğidir"))
json.dump({"hafta": "taslak", "taslak": "23 Kasım 2026: kullanıcı 5-6 ürüne fragman türünde tanıtım istedi; onay bekliyor", "posts": posts},
          open(os.path.join(ROOT, "taslak/fragman-5/fragman-5.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for p in posts:
    print(p["id"], p["muzik"])
