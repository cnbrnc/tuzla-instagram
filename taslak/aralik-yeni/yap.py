#!/usr/bin/env python3
"""TASLAK (23 Kasım 2026, kullanıcı onayı bekliyor): Aralık'ın 10 ürün Reels'ini yeni türlere çevirir.

Kullanım (depo kökünden):
  python3 taslak/aralik-yeni/yap.py --indir     # destek ürün görsellerini ve stok videoları work/ altına indirir
  python3 taslak/aralik-yeni/yap.py             # taslak/aralik-yeni/aralik-yeni.json dosyasını yazar
  python3 reel.py taslak/aralik-yeni/aralik-yeni.json out/aralik-yeni

weeks/*.json içindeki eski öğeyi okur; kimlik, tarih, ürün sayfası ve açıklamanın çağrı kısmı aynı kalır.
Onay gelmeden Metricool'a dokunulmaz ve video depoya konmaz (ROBOT.md → "Aralık Reels'leri: yeni biçim taslağı").
"""
import glob, json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = "work/aralik-yeni/destek/"
SITE = "https://tuzlahirdavat.com.tr/"
DESTEK = {"krom-lokma2": "17mm-lokma-6-kose-12-nttools-ncl1217", "havali-lokma": "19mm-havali-lokma-12-nt-ntzl1219",
          "uzatma": "opt-mk-165-makarali-uzatma-kablo-osaka-opt-mk-165", "t101b": "t-101-b-clean-for-wood-bosch-2608630030",
          "t118a": "t-118-a-basic-for-metal-bosch-2608631964", "serit": "rcm0525-5x25-celik-serit-metre-retta-rcm0525"}
P = "https://videos.pexels.com/video-files/"
STOK = {"pexels-4941356": P + "4941356/4941356-hd_1920_1080_25fps.mp4", "pexels-4873237": P + "4873237/4873237-hd_1920_1080_30fps.mp4",
        "pexels-6079664": P + "6079664/6079664-uhd_2560_1440_24fps.mp4", "pexels-6160043": P + "6160043/6160043-uhd_2560_1440_24fps.mp4",
        "pexels-7033925": P + "7033925/7033925-uhd_2560_1440_25fps.mp4"}


def indir():
    from PIL import Image
    for ad, yol in DESTEK.items():
        subprocess.run([sys.executable, "-I", os.path.join(ROOT, "fetch_product.py"), SITE + yol, os.path.join(ROOT, D, ad)], check=True)
    for ad in ("t101b", "t118a"):          # dekupaj bıçağı: diş kısmının yakın kırpması
        im = Image.open(os.path.join(ROOT, D, ad, "product.png")).convert("RGB")
        w, h = im.size
        c = im.crop((0, int(h * .04), w, int(h * .36)))
        c.resize((c.width * 2, c.height * 2), Image.LANCZOS).save(os.path.join(ROOT, D, ad, "dis.png"))
    os.makedirs(os.path.join(ROOT, "work", "stok"), exist_ok=True)
    for ad, url in STOK.items():
        hedef = os.path.join(ROOT, "work", "stok", ad + ".mp4")
        if not os.path.exists(hedef):
            subprocess.run(["curl", "-sSL", "-m", "300", "-A", "Mozilla/5.0", "-o", hedef, url], check=True)


BIL = "Tahminini yoruma yaz: A mı, B mi? Cevap videoda."
YENI = {
 "2026-11-30-volkel-helikoil": dict(template="reel_bil", tag="BİL BAKALIM", question_kicker="DİŞ TAMİRİ",
    question=["Alüminyumda", "hangisi sağlam?"],
    options=[{"lines": ["ORİJİNAL", "DİŞ"], "label": "Parçaya açılan diş"}, {"lines": ["HELİKOİL", "DİŞ"], "label": "Çelik helisli diş"}],
    answer=1, answer_text="Cevap: Helikoil",
    why=["Çelik helis yükü daha geniş alana yayar", "Yumuşak alüminyumda diş daha zor sıyrılır"],
    urun={"marka": "VÖLKEL", "ad": "Helikoil diş tamir seti", "ozellik": "M8 × 1,25 · set halinde"},
    bg_video={"file": "work/stok/pexels-4941356.mp4", "url": STOK["pexels-4941356"], "start": 0.0, "x": 0.56, "pan": 0.03},
    kaynak_video="https://www.pexels.com/video/4941356/ (Pexels lisansı)",
    kaynak="Böllhoff HELICOIL: düşük dayanımlı malzemede (alüminyum) yüksek dayanımlı diş",
    giris="Bil bakalım: alüminyumda hangisi daha sağlam, parçaya açılan orijinal diş mi, helikoil diş mi? 🤔 " + BIL
          + "\n\nDiş sıyırdıysa parçayı atma: Völkel V-04012 helikoil seti M8×1,25 dişi orijinal ölçüsüne geri getirir. Alüminyum blokta, motor gövdesinde, makine parçasında işe yarar. 🛠️"),
 "2026-12-04-crommac-isitici": dict(template="reel_yd", tag="USTA HATASI", hook_kicker="SIK YAPILAN HATA",
    hook=["Isıtıcıyı", "uzatmaya mı", "takıyorsun?"],
    yanlis={"ne": "Isıtıcıyı uzatma kablosuna ya da çoklu prize takmak", "alt": "Kablo ısınır, priz erir", "product_dir": D + "uzatma"},
    dogru={"ne": "Fişi doğrudan duvar prizine takmak", "alt": "Crommac CRM3KW fanlı ısıtıcı", "product_dir": "work/crommac-isitici"},
    why_kicker="Neden?", why="Güçlü ısıtıcı yüksek akım çeker. İnce ya da makaraya sarılı kablo ısınır, yangına yol açabilir.",
    urun={"marka": "CROMMAC", "ad": "Fanlı ısıtıcı CRM3KW", "ozellik": "150 m³/sa hava · devrilme emniyeti"},
    bg_video={"file": "work/stok/pexels-4873237.mp4", "url": STOK["pexels-4873237"], "start": 1.5, "x": 0.72, "pan": 0.0},
    kaynak_video="https://www.pexels.com/video/4873237/ (Pexels lisansı)",
    kaynak="CPSC, NFPA, ESFI: ısıtıcı doğrudan duvar prizine takılır; uzatma kablosu ve çoklu priz kullanılmaz",
    giris="Isıtıcıyı uzatma kablosuna mı takıyorsun? ❌ Sık yapılan hata.\n\nGüçlü ısıtıcı yüksek akım çeker; ince ya da makaraya sarılı uzatma kablosu ısınır. Doğrusu: fişi doğrudan duvar prizine tak."
          "\n\nCrommac CRM3KW fanlı ısıtıcı: saatte 150 m³ hava akışı, devrilme emniyeti ve 4 kg'lık taşınabilir gövde. 🔥"),
 "2026-12-07-grangos-somun-sikma": dict(template="reel_bil", tag="BİL BAKALIM", question_kicker="OTO SERVİS",
    question=["Darbeliye", "hangi lokma?"],
    options=[{"product_dir": D + "krom-lokma2", "label": "Krom lokma"}, {"product_dir": D + "havali-lokma", "label": "Siyah darbeli lokma"}],
    answer=1, answer_text="Cevap: Siyah lokma",
    why=["Krom lokma serttir; darbede çatlayıp fırlayabilir", "Siyah darbeli lokma tok çeliktir, darbeyi emer"],
    urun={"marka": "GRANGOS", "ad": "Akülü somun sıkma", "ozellik": "360 Nm · çift akü · 1/2\" kare uç"},
    kaynak="Snap-on, Draper, Chicago Pneumatic: darbeli alette yalnız darbeli (impact) lokma kullanılır",
    giris="Bil bakalım: darbeli somun sıkmaya hangi lokma takılır, krom mu, siyah mı? 🤔 " + BIL
          + "\n\nGrangos GCW20-F2 akülü somun sıkma: 360 Nm tork, kömürsüz motor, çift akü ve LED çalışma ışığı. 1/2\" kare uç; siyah darbeli lokmayla kullan. 🛞"),
 "2026-12-11-bosch-sicak-hava": dict(template="reel_yd", tag="USTA HATASI", hook_kicker="SIK YAPILAN HATA",
    hook=["Makaronu", "çakmakla mı", "daraltıyorsun?"],
    yanlis={"ne": "Makaronu çakmak aleviyle daraltmak", "alt": "Alev yakar, is bırakır, kabloyu zedeler"},
    dogru={"ne": "Sıcak hava tabancasıyla daraltmak", "alt": "Bosch GHG 20-63", "product_dir": "work/bosch-sicak-hava"},
    why_kicker="Neden?", why="Sıcak hava makaronu her yandan eşit ısıtır; makaron yanmadan, düzgün oturur.",
    urun={"marka": "BOSCH", "ad": "Sıcak hava tabancası GHG 20-63", "ozellik": "50–630 °C · 2000 W"},
    bg_video={"file": "work/stok/pexels-6079664.mp4", "url": STOK["pexels-6079664"], "start": 2.0, "x": 0.42, "pan": 0.02},
    kaynak_video="https://www.pexels.com/video/6079664/ (Pexels lisansı)",
    kaynak="Essentra Components: makaron için sıcak hava tabancası önerilir; açık alev eşit ısıtmaz ve güvenlik riskidir",
    giris="Makaronu çakmakla mı daraltıyorsun? ❌ Sık yapılan hata.\n\nAçık alev makaronu yakar, is bırakır, kabloyu zedeler. Sıcak hava her yandan eşit ısıtır, makaron düzgün oturur."
          "\n\nBosch GHG 20-63 sıcak hava tabancası: 50–630 °C ayar, 2000 W güç, 3 kademeli hava akışı, aşırı ısınmada otomatik kesme. 🔥"),
 "2026-12-14-fusion-boru-kaynak": dict(template="reel_bil", tag="BİL BAKALIM", question_kicker="TESİSAT",
    question=["PPR kaynağı", "kaç derece?"],
    options=[{"big": "160°C", "label": "Düşük ısı"}, {"big": "260°C", "label": "Yüksek ısı"}],
    answer=1, answer_text="Cevap: 260 °C",
    why=["PPR kaynağı 250–270 °C arasında yapılır", "Düşük ısıda ek tam kaynamaz, sonradan sızdırır"],
    urun={"marka": "FUSION", "ad": "Boru kaynak makinesi seti", "ozellik": "1500 W · PPR-C boru"},
    kaynak="Wavin Ekoplastik PP-R montaj kılavuzu: kaynak sıcaklığı 250–270 °C",
    giris="Bil bakalım: PPR boru kaynağı kaç derecede yapılır, 160 mı, 260 mı? 🤔 " + BIL
          + "\n\nFusion FSBK15-S1 1500 W plastik boru kaynak makinesi seti ile PPR-C borularda sızdırmaz ek yap. Su ve sıhhi tesisat işleri için set halinde. 💧"),
 "2026-12-18-bosch-dekupaj": dict(template="reel_yd", tag="USTA HATASI", hook_kicker="SIK YAPILAN HATA",
    hook=["Sacı ahşap", "bıçağıyla mı", "kesiyorsun?"], hook_image="work/bosch-dekupaj/product.png",
    yanlis={"ne": "Sacı iri dişli ahşap bıçağıyla kesmek", "alt": "Bosch T 101 B: ahşap için", "image": D + "t101b/dis.png"},
    dogru={"ne": "İnce dişli metal bıçağı takmak", "alt": "Bosch T 118 A: 1–3 mm sac için", "image": D + "t118a/dis.png"},
    why_kicker="Neden?", why="İri diş ince saca takılır; bıçak körelir, sac titrer, kesim bozulur.",
    urun={"marka": "BOSCH", "ad": "Dekupaj testere GST 8000 E", "ozellik": "710 W · 4 kademeli pandül"},
    kaynak="Bosch: T 118 A ince dişli, 1–3 mm sac için; T 101 B ahşap için",
    giris="Sacı ahşap bıçağıyla mı kesiyorsun? ❌ Sık yapılan hata.\n\nİri dişli ahşap bıçağı ince saca takılır; bıçak körelir, sac titrer, kesim bozulur. Sac için ince dişli metal bıçağı tak (örnek: Bosch T 118 A, 1–3 mm sac)."
          "\n\nBosch GST 8000 E dekupaj testere: 710 W motor, 4 kademeli pandül, aletsiz bıçak değiştirme; ahşapta 80 mm'ye, çelikte 10 mm'ye kadar kesim. 🪚"),
 "2026-12-21-bosch-panc-67": dict(template="reel_bil", tag="BİL BAKALIM", question_kicker="ELEKTRİK PANOSU",
    question=["Panç metalde", "hangi devirde?"],
    options=[{"big": "YÜKSEK", "label": "devir"}, {"big": "DÜŞÜK", "label": "devir"}],
    answer=1, answer_text="Cevap: Düşük devir",
    why=["Yüksek devir dişi yakar, panç çabuk körelir", "Paslanmazda düşük devir ve kesme yağı kullan"],
    urun={"marka": "BOSCH", "ad": "Panç delik testeresi 67 mm", "ozellik": "Bimetal kobalt · sac ve paslanmaz"},
    kaynak="Pro Tool Reviews delik testeresi devir tablosu: 67 mm bimetal, paslanmazda yaklaşık 65 dev/dk",
    giris="Bil bakalım: panç metalde yüksek devirde mi, düşük devirde mi kullanılır? 🤔 " + BIL
          + "\n\nBosch PRO Sheet Metal 67 mm panç: kobalt alaşımlı bimetal, Power Change Plus bağlantı. Panoya, saca, paslanmaz panele buat deliğini temiz aç. ⚡"),
 "2026-12-25-grangos-caraskal": dict(template="reel_yd", tag="USTA HATASI", hook_kicker="SIK YAPILAN HATA",
    hook=["Caraskalla", "yandan mı", "çekiyorsun?"],
    yanlis={"ne": "Yükü yandan, çapraz çekmek", "alt": "Zincir ve gövde zorlanır, yük savrulur"},
    dogru={"ne": "Kancayı yükün tam üstüne alıp dik kaldırmak", "alt": "Grangos GRCK15, 1 ton", "product_dir": "work/grangos-caraskal"},
    why_kicker="Neden?", why="Caraskal dik kaldırmak için yapılır. Yandan çekiş zinciri ve gövdeyi zorlar; yük savrulabilir.",
    urun={"marka": "GRANGOS", "ad": "Zincirli caraskal GRCK15", "ozellik": "1 ton · 5 m kaldırma"},
    bg_video={"file": "work/stok/pexels-6160043.mp4", "url": STOK["pexels-6160043"], "start": 10.0, "x": 0.52, "pan": 0.02},
    kaynak_video="https://www.pexels.com/video/6160043/ (Pexels lisansı)",
    kaynak="ASME B30.16, Harrington ve Kito kullanım kılavuzları: caraskalla yandan çekiş yapılmaz, yük dik kaldırılır",
    giris="Caraskalla yükü yandan mı çekiyorsun? ❌ Sık yapılan hata.\n\nCaraskal dik kaldırmak için yapılır. Yandan çekiş zinciri ve gövdeyi zorlar, yük savrulabilir. Kancayı yükün tam üstüne al, dik kaldır."
          "\n\nGrangos GRCK15 zincirli caraskal: 1 ton kapasite, 5 m kaldırma; elektrik gerekmez. ⛓️"),
 "2026-12-28-varta-f30r": dict(template="reel_bil", tag="BİL BAKALIM", question_kicker="AYDINLATMA",
    question=["IPX4 fener", "suya girer mi?"],
    options=[{"big": "EVET", "label": "Suya daldırılır"}, {"big": "HAYIR", "label": "Yalnız su sıçraması"}],
    answer=1, answer_text="Cevap: Hayır",
    why=["IPX4: her yönden su sıçramasına dayanır", "Suya daldırmak için IPX7 ya da IPX8 gerekir"],
    urun={"marka": "VARTA", "ad": "Şarjlı el feneri F30R", "ozellik": "700 lümen · powerbank · IPX4"},
    kaynak="IEC 60529 (DigiKey özeti): IPX4 her yönden su sıçraması; IPX7 ve IPX8 suya daldırma",
    giris="Bil bakalım: IPX4 fener suya girer mi? 🤔 " + BIL
          + "\n\nVARTA Night Cutter F30R: 700 lümen ışık ve telefonu şarj eden 2600 mAh powerbank bir arada. Alüminyum gövde, 2 metreden düşme testli; IPX4 ile yağmurda ve su sıçramasında çalışır. 🔦"),
 "2027-01-01-klpro-lazer-metre": dict(template="reel_yd", tag="USTA HATASI", hook_kicker="SIK YAPILAN HATA",
    hook=["Uzun mesafeyi", "şeritle mi", "ölçüyorsun?"],
    yanlis={"ne": "Uzun mesafeyi şerit metreyle tek başına ölçmek", "alt": "Şerit sarkar, ölçü şaşar", "product_dir": D + "serit"},
    dogru={"ne": "Lazer metreyle tek tuşla ölçmek", "alt": "KL Pro KLLZM80, 80 m", "product_dir": "work/klpro-lazer-metre"},
    why_kicker="Neden?", why="Uzun şerit sarkar, ucunu tutacak ikinci kişi ister. Lazer metre tek kişiyle, saniyede ölçer.",
    urun={"marka": "KL PRO", "ad": "Lazer metre KLLZM80", "ozellik": "80 m ölçüm · dijital ekran"},
    bg_video={"file": "work/stok/pexels-7033925.mp4", "url": STOK["pexels-7033925"], "start": 1.0, "x": 0.5, "pan": 0.0},
    kaynak_video="https://www.pexels.com/video/7033925/ (Pexels lisansı)",
    kaynak="Genel ölçüm bilgisi: uzun şerit sarkar; lazer metre tek kişiyle ölçer",
    giris="Uzun mesafeyi şerit metreyle mi ölçüyorsun? ❌\n\nUzun şerit sarkar, ucunu tutacak ikinci kişi ister. Lazer metre tek kişiyle, tek tuşla ölçer."
          "\n\nKL Pro KLLZM80 lazer metre: 80 metreye kadar ölçüm, dijital ekran. 📏"),
}
if "--indir" in sys.argv:
    indir()
    for f in sorted(glob.glob(os.path.join(ROOT, "weeks", "*.json"))):
        for p in json.load(open(f, encoding="utf-8")).get("posts", []):
            if p["id"] in YENI and not os.path.exists(os.path.join(ROOT, p["product_dir"], "product.json")):
                subprocess.run([sys.executable, "-I", os.path.join(ROOT, "fetch_product.py"), p["url"], os.path.join(ROOT, p["product_dir"])], check=True)
    sys.exit(0)
SIL = ("hook", "hook_kicker", "brand", "sku", "title", "chips", "ses", "template", "tag")
posts, i = [], 0
for f in sorted(glob.glob(os.path.join(ROOT, "weeks", "*.json"))):
    for p in json.load(open(f, encoding="utf-8")).get("posts", []):
        y = YENI.get(p["id"])
        if not y:
            continue
        y = dict(y)
        q = {k: v for k, v in p.items() if k not in SIL}
        satir = p["caption"].split("\n")
        k = next(n for n, s in enumerate(satir) if s[:1] in "💾📤")       # çağrı satırından sona kadar aynı kalır
        q["caption"] = y.pop("giris") + "\n\n" + "\n".join(satir[k:])
        q.update(y, stil="sinematik", muzik="abc"[i % 3])
        i += 1
        etiket = [w for w in q["caption"].split() if w.startswith("#")]
        assert len(etiket) <= 5, (p["id"], etiket)
        posts.append(q)
assert len(posts) == 10, len(posts)
json.dump({"hafta": "aralik-yeni", "taslak": "23 Kasım 2026, onay bekliyor", "posts": posts}, open(os.path.join(ROOT, "taslak/aralik-yeni/aralik-yeni.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for p in posts:
    print(p["id"], p["template"], p["muzik"], "video" if p.get("bg_video") else "kod")
