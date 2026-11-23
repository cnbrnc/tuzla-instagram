#!/usr/bin/env python3
"""dagarcik.json dosyasını yazar: Reels ve İpucu için fikir dağarcığı.

Kullanım: python3 dagarcik_yaz.py
Yeni fikir eklemek için aşağıdaki listelere satır ekle ve betiği çalıştır. Kurallar SENARYO.md dosyasındadır.
dogrulandi = kaynağın okunduğu tarih (YYYY-MM-DD). None ise fikir kullanılmadan önce doğrulanır.
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
D = "2026-11-23"


def bil(id, grup, meslek, kalip, kicker, soru, a, b, cevap, cevap_yazi, neden, urun_ara, kaynak, dogrulandi=D, **ek):
    """a ve b: ("big", "YAZI", "etiket") ya da ("lines", ["ÜST", "ALT"], "etiket")."""
    sec = []
    for tur, deger, etiket in (a, b):
        o = {tur: deger}
        if etiket:
            o["label"] = etiket
        sec.append(o)
    return dict(id=id, tur="bil", grup=grup, meslek=meslek, kanca_kalibi=kalip, question_kicker=kicker, question=soru,
                options=sec, answer=cevap, answer_text=cevap_yazi, why=neden, urun_ara=urun_ara, kaynak=kaynak,
                dogrulandi=dogrulandi, **ek)


def yd(id, grup, meslek, kalip, cift, kanca, yanlis, dogru, neden, urun_ara, kaynak, dogrulandi=D, **ek):
    """yanlis ve dogru: (ne, alt). cift: yanlis-dogru | efsane-gercek | zor-kolay."""
    return dict(id=id, tur="yd", cift=cift, grup=grup, meslek=meslek, kanca_kalibi=kalip, hook=kanca,
                yanlis={"ne": yanlis[0], "alt": yanlis[1]}, dogru={"ne": dogru[0], "alt": dogru[1]}, why=neden,
                urun_ara=urun_ara, kaynak=kaynak, dogrulandi=dogrulandi, **ek)


BSSA = "British Stainless Steel Association (bssa.org.uk)"
FIKIRLER = [
    # ---------- Bil bakalım ----------
    bil("bil-sapan-renk", "kaldirma", "depo, vinç, nakliye", "renk-kod", "YÜK KALDIRMA", ["Gri sapan", "kaç ton taşır?"],
        ("big", "2 TON", None), ("big", "4 TON", None), 1, "Cevap: 4 ton",
        ["Sapanın rengi kapasitesini gösterir", "Mor 1, yeşil 2, sarı 3, gri 4, kırmızı 5 ton"],
        "polyester sapan", "EN 1492-1 renk kodu: Certex, Mennens ve LiftKing güvenlik belgeleri",
        not_="Sitedeki sapanın tonajı ile soruyu eşle (4 ton gri, 5 ton kırmızı). Etiketteki değer esastır, bunu açıklamaya yaz."),
    bil("bil-imbus-alyan", "baglanti", "makine bakım, kalıpçı", "kac", "CIVATA BİLGİSİ", ["M8 imbusa", "kaç alyan?"],
        ("big", "5 mm", None), ("big", "6 mm", None), 1, "Cevap: 6 mm",
        ["DIN 912: M6'ya 5, M8'e 6, M10'a 8 mm", "Yanlış ölçü, anahtar yuvasını bozar"],
        "alyan anahtar takımı, imbus cıvata din912", "DIN 912 / ISO 4762 ölçü tablosu (Brighton-Best ürün föyü)"),
    bil("bil-tas-tarih", "asindirici", "kaynakçı, demirci", "evet-hayir", "KESME TAŞI", ["Kesme taşının", "tarihi geçer mi?"],
        ("big", "EVET", "Son kullanma var"), ("big", "HAYIR", "Sonsuza dek dayanır"), 0, "Cevap: Evet",
        ["Reçine bağlı taşın ömrü en çok 3 yıldır", "Tarih, ortadaki metal halkada yazar"],
        "kesme taşı karbosan, inox kesme taşı", "EN 12413; FEPA ve oSa (osa-abrasives.org) açıklamaları"),
    bil("bil-miknatis", "paslanmaz", "paslanmaz imalat, denizci", "efsane", "PASLANMAZ", ["Mıknatıs tutan", "cıvata paslanmaz mı?"],
        ("big", "OLAMAZ", None), ("big", "OLABİLİR", None), 1, "Cevap: Olabilir",
        ["A2 (304) soğuk şekillenince hafif mıknatıslanır", "Mıknatıs tek başına kesin sonuç vermez"],
        "inox cıvata a2", BSSA + ": soğuk işlemenin manyetik geçirgenliğe etkisi"),
    bil("bil-a2-70", "paslanmaz", "paslanmaz imalat", "ne-demek", "PASLANMAZ", ["A2-70'teki", "70 ne demek?"],
        ("lines", ["NİKEL", "ORANI"], None), ("lines", ["ÇEKME", "DAYANIMI"], None), 1, "Cevap: Dayanım",
        ["70: en az 700 MPa çekme dayanımı", "A2 çeliğin türünü gösterir (304)"],
        "inox cıvata a2-70", "ISO 3506-1: özellik sınıfı = çekme dayanımının onda biri"),
    bil("bil-s1-s3", "isg", "şantiye, depo", "hangisi", "İŞ GÜVENLİĞİ", ["Çiviye basınca", "hangisi korur?"],
        ("big", "S1", "iş ayakkabısı"), ("big", "S3", "iş ayakkabısı"), 1, "Cevap: S3",
        ["S3'te delinmez ara taban vardır", "S1'de yok; S1P'de var (EN ISO 20345)"],
        "s3 ayakkabı, s1 ayakkabı", "EN ISO 20345 sınıf tablosu (Strauss, Cromwell rehberleri)"),
    bil("bil-eldiven-kesilme", "isg", "sac işleri, cam", "hangisi", "İŞ GÜVENLİĞİ", ["Hangi eldiven", "kesilmeye dayanır?"],
        ("big", "A", "EN 388 seviyesi"), ("big", "F", "EN 388 seviyesi"), 1, "Cevap: F",
        ["Kesilme seviyesi A'dan F'ye doğru artar", "F en yüksek: en az 30 newton"],
        "kesilmez eldiven, atg maxicut", "EN 388:2016 (ISO 13997) seviye tablosu",
        not_="Tanıtılan eldivenin kendi seviyesini ürün sayfasından oku; yazmıyorsa seviye yazma."),
    bil("bil-serit-ucu", "olcu", "marangoz, inşaat", "neden", "ÖLÇÜ ALETİ", ["Metrenin ucu", "neden oynar?"],
        ("lines", ["BOZUK", "DEMEK"], None), ("lines", ["BİLEREK", "YAPILIR"], None), 1, "Cevap: Bilerek",
        ["Uç, kendi kalınlığı kadar oynar", "İçten de dıştan da doğru ölçmek için"],
        "şerit metre", "Stanley Tools destek sayfası: uç kancası neden oynar"),
    bil("bil-tork-saklama", "el-aleti", "oto servis, makine bakım", "nasil", "TORK ANAHTARI", ["Tork anahtarı", "nasıl saklanır?"],
        ("lines", ["AYARINDA", "BIRAK"], None), ("lines", ["EN DÜŞÜĞE", "AL"], None), 1, "Cevap: En düşüğe",
        ["Yay sıkışık kalırsa ayar zamanla kayar", "Skalanın en düşük değerine al, altına inme"],
        "tork anahtarı", "Snap-on ve Park Tool kullanım kılavuzları"),
    bil("bil-uc-acisi", "matkap", "paslanmaz imalat, tesisat", "hangisi", "MATKAP UCU", ["Paslanmaza", "hangi uç açısı?"],
        ("big", "118°", None), ("big", "135°", None), 1, "Cevap: 135°",
        ["135° uç kaymaz, daha az baskı ister", "Kobaltlı uç, düşük devir, kesme yağı"],
        "kobalt matkap ucu", BSSA + " delme önerileri; Thürmer matkap SSS"),
    bil("bil-testere-disi", "el-aleti", "tesisat, demirci", "nereye", "EL ALETİ", ["Demir testeresi", "dişi nereye bakar?"],
        ("big", "İLERİ", None), ("big", "GERİ", None), 0, "Cevap: İleri",
        ["Demir testeresi iterken keser", "Dişler saptan uzağa, ileri bakmalı"],
        "testere kolu izeltaş", "CCOHS el testeresi güvenlik föyü; RS demir testeresi rehberi"),
    bil("bil-flap-kum", "asindirici", "kaynakçı, demirci", "hangisi", "FLAP DİSK", ["Hangi flap disk", "daha kaba?"],
        ("big", "40", "kum"), ("big", "80", "kum"), 0, "Cevap: 40 kum",
        ["Kum numarası küçüldükçe tane irileşir", "40 kum kaba talaş, 80 kum ince yüzey"],
        "flap disk", "FEPA P tane numarası", dogrulandi=None),
    bil("bil-anahtar-m8", "baglanti", "makine bakım", "kac", "CIVATA BİLGİSİ", ["M8 somuna", "kaç anahtar?"],
        ("big", "13", "mm"), ("big", "14", "mm"), 0, "Cevap: 13 mm",
        ["DIN 934: M6'ya 10, M8'e 13, M10'a 17 mm", "ISO'da M10 için 16 mm de görülür"],
        "somun din934", "DIN 934 / ISO 4032 anahtar ağzı tablosu", dogrulandi=None),
    bil("bil-somun-sinif", "baglanti", "çelik konstrüksiyon", "hangisi", "CIVATA BİLGİSİ", ["8.8 cıvataya", "hangi somun?"],
        ("big", "6", "kalite"), ("big", "8", "kalite"), 1, "Cevap: 8 kalite",
        ["Somun sınıfı cıvatanın ilk sayısına uyar", "8.8 cıvataya 8, 10.9 cıvataya 10 kalite"],
        "somun 8 kalite", "ISO 898-2", dogrulandi=None),
    bil("bil-dubel-uc", "insaat", "inşaat, montaj", "kac", "DÜBEL", ["8'lik dübele", "kaç mm uç?"],
        ("big", "6 mm", None), ("big", "8 mm", None), 1, "Cevap: 8 mm",
        ["Dübelin numarası delik çapıdır", "Vida ise genelde 2–3 mm daha incedir"],
        "plastik dübel 8mm", "Dübel üreticisi teknik föyü", dogrulandi=None),
    bil("bil-tas-devir", "asindirici", "kaynakçı", "kac", "KESME TAŞI", ["115'lik taş en", "çok kaç devir?"],
        ("big", "6.600", "devir/dk"), ("big", "13.300", "devir/dk"), 1, "Cevap: 13.300",
        ["Sınır 80 m/sn çevre hızıdır", "Değer taşın üstünde yazar; makineyle karşılaştır"],
        "kesme taşı 115", "EN 12413 işaretleme: 80 m/sn; 115 mm için hesap 13.286 dev/dk", dogrulandi=None),

    # ---------- Yanlış / doğru ----------
    yd("yd-paslanmaz-sarma", "paslanmaz", "paslanmaz imalat, denizci", "ima", "yanlis-dogru",
       ["Paslanmazı", "darbeliyle mi", "sıkıyorsun?"],
       ("Paslanmaz somunu kuru ve hızlı sıkmak", "Diş ısınır, sarar, kilitlenir"),
       ("Dişi yağlayıp yavaş sıkmak", "Elle ya da düşük devirde"),
       "Paslanmaz diş sürtünmeyle ısınır ve birbirine kaynar. Buna sarma denir; sonu kopan cıvatadır.",
       "inox cıvata a2, inox somun", "TWI (twi-global.com) ve Essentra: galling nedir, nasıl önlenir"),
    yd("yd-paslanmaz-firca", "paslanmaz-bulasma", "paslanmaz imalat, kaynakçı", "ima", "yanlis-dogru",
       ["Paslanmazı", "demir fırçayla", "mı siliyorsun?"],
       ("Paslanmazı demir tel fırçayla temizlemek", "Demir tozu bulaşır, pas lekesi yapar"),
       ("Paslanmaz (inox) tel fırça kullanmak", "Yalnız paslanmazda kullan"),
       "Demir parçacığı yüzeye gömülür, nem alınca paslanır. Fırça ve disk paslanmaza ayrı olsun.",
       "inox fırça", BSSA + ": demir bulaşması ve pas lekesi"),
    yd("yd-inox-tas", "paslanmaz-bulasma", "paslanmaz imalat", "ima", "yanlis-dogru",
       ["Demir kestiğin", "taşla inox mu", "kesiyorsun?"],
       ("Demir kesilmiş taşla paslanmaz kesmek", "Kesim yeri sonradan pas tutar"),
       ("Paslanmaza ayrı inox kesme taşı", "Demirsiz (Fe içermeyen) taş"),
       "Taştaki demir tozu kesim yüzeyine bulaşır. İnox taşı yalnız paslanmazda kullan.",
       "inox kesme taşı", BSSA + ": demirsiz kesme ve taşlama diskleri kullanılmalı"),
    yd("yd-paslanmaz-devir", "matkap", "paslanmaz imalat, tesisat", "ima", "yanlis-dogru",
       ["Paslanmazı", "yüksek devirde", "mi deliyorsun?"],
       ("Yüksek devir, hafif baskıyla delmek", "Yüzey sertleşir, uç yanar"),
       ("Düşük devir, sabit baskı, kesme yağı", "Kobaltlı uç, 135° açı"),
       "Uç kesmeden sürtünürse paslanmaz sertleşir ve delinmez olur. Baskıyı hiç bırakma.",
       "kobalt matkap ucu", BSSA + " delme hız ve ilerleme önerileri; Thürmer"),
    yd("yd-eldiven-matkap", "isg", "torna, freze, atölye", "ima", "yanlis-dogru",
       ["Matkapta", "eldivenle mi", "çalışıyorsun?"],
       ("Dönen makinede eldiven takmak", "Eldiven uca dolanır, eli içeri çeker"),
       ("Eldivensiz çalış, parçayı mengeneye bağla", "Kol sıvalı, saç toplu"),
       "Sütunlu matkap ve tornada eldiven koruma değil tehlikedir. Parçayı elle tutma.",
       "matkap mengenesi", "CCOHS sütunlu matkap föyü; OSHA torna rehberi (Harvard EHS)"),
    yd("yd-fayans-darbe", "matkap", "tesisat, montaj, tadilat", "ima", "yanlis-dogru",
       ["Fayansı", "darbeli mi", "deliyorsun?"],
       ("Fayansı darbe açıkken delmek", "Titreşim fayansı çatlatır"),
       ("Darbeyi kapat, düşük devirde del", "Fayans ucu, hafif baskı"),
       "Önce fayansı darbesiz geç; duvara gelince beton ucu tak ve darbeyi aç.",
       "seramik matkap ucu, darbeli matkap", "Bosch: fayans nasıl delinir"),
    yd("yd-kilavuz-kirma", "kilavuz", "torna, makine bakım", "ima", "yanlis-dogru",
       ["Kılavuzu", "tek seferde mi", "çekiyorsun?"],
       ("Kılavuzu durmadan ileri çevirmek", "Talaş sıkışır, kılavuz kırılır"),
       ("Yarım tur ileri, çeyrek tur geri", "Kesme yağıyla"),
       "Geri çevirmek talaşı kırar. Kırılan kılavuzu delikten çıkarmak çok zordur.",
       "kılavuz pafta seti", "Sheldon Brown kılavuz yazısı; ToolGuyd elle kılavuz çekme"),
    yd("yd-teflon-yon", "tesisat", "tesisatçı", "ima", "yanlis-dogru",
       ["Teflonu", "ters yöne mi", "sarıyorsun?"],
       ("Teflonu sıkma yönünün tersine sarmak", "Sıkarken açılır, sızdırır"),
       ("Sıkma yönünde, gergin sarmak", "Dişin ucundan bakınca saat yönü"),
       "Doğru yönde sarılan bant sıkarken dişe yatar. 3–5 tur yeter.",
       "teflon bant", "Toolstation PTFE bant rehberi",
       not_="Sitede teflon bant yoksa urun yazma; boru anahtarıyla eşle."),
    yd("yd-kurbagacik", "el-aleti", "tesisat, bakım", "ima", "yanlis-dogru",
       ["Kurbağacığı", "ters mi", "tutuyorsun?"],
       ("Yükü oynak çeneye bindirmek", "Çene açılır, somunu sıyırır"),
       ("Yük sabit çenede olacak şekilde çevirmek", "Çeneyi somuna tam sıkıştır"),
       "Sabit çene daha sağlamdır. Anahtarı kendine doğru çek, itme.",
       "kurbağacık anahtar", "CCOHS anahtarlar güvenlik föyü"),
    yd("yd-tork-sokme", "el-aleti", "oto servis", "ima", "yanlis-dogru",
       ["Tork anahtarıyla", "somun mu", "söküyorsun?"],
       ("Tork anahtarını sökme kolu yapmak", "Ayarı bozulur"),
       ("Sökmeye cırcır ya da kol kullanmak", "Tork anahtarı yalnız son sıkmada"),
       "Tork anahtarı ölçü aletidir. Sökerken sınırını aşarsın, bir daha doğru sıkmaz.",
       "tork anahtarı, cırcır kol", "Park Tool tork anahtarı kullanım ve bakım"),
    yd("yd-siperlik", "asindirici", "kaynakçı, demirci", "ima", "yanlis-dogru",
       ["Taşlamanın", "siperini mi", "söktün?"],
       ("Siperliksiz taşlama yapmak", "Taş kırılırsa parça sana gelir"),
       ("Siper takılı, tarihi geçmemiş taşla çalışmak", "Gözlük ve yüz siperi de tak"),
       "Siperlik kırılan taşın önündeki tek engeldir. Rahat kesmek için sökülmez.",
       "kesme taşı, koruyucu gözlük", "FEPA taşlama ve kesme taşı güvenlik föyü", sfx_kanca="taslama"),
    yd("ef-miknatis", "paslanmaz", "paslanmaz imalat", "efsane", "efsane-gercek",
       ["Mıknatıs tuttu,", "paslanmaz", "değil mi?"],
       ("Mıknatıs tutuyorsa paslanmaz değildir", "Çok duyulan bir söz"),
       ("A2 cıvata hafif mıknatıs tutabilir", "Soğuk şekillenirken olur"),
       "Baş ve diş soğuk dövülürken çelik biraz mıknatıslanır. Paslanmazlığı bundan etkilenmez.",
       "inox cıvata a2", BSSA + ": soğuk işlemenin manyetik geçirgenliğe etkisi",
       not_="bil-miknatis ile aynı konu; yalnız biri kullanılır."),
    yd("ef-paslanmaz-paslanir", "paslanmaz-bulasma", "paslanmaz imalat, denizci", "efsane", "efsane-gercek",
       ["Paslanmaz", "hiç paslanmaz", "mı?"],
       ("Paslanmaz hiçbir koşulda paslanmaz", "Adından öyle sanılır"),
       ("Demir bulaşırsa pas lekesi yapar", "Temiz tut, demirle temas ettirme"),
       "Lekenin çoğu paslanmazın kendisi değil, üstüne bulaşan demir tozudur.",
       "inox cıvata, inox fırça", BSSA + ": demir bulaşması ve pas lekesi"),
    yd("ef-serit-ucu", "olcu", "marangoz, inşaat", "efsane", "efsane-gercek",
       ["Metrenin ucu", "oynuyor,", "bozuk mu?"],
       ("Ucu oynayan metre bozuktur", "Perçini gevşemiş sanılır"),
       ("Uç bilerek oynar", "Kendi kalınlığı kadar"),
       "İçten ölçerken uç içeri, dıştan ölçerken dışarı kayar. Ölçü iki durumda da doğru çıkar.",
       "şerit metre", "Stanley Tools destek sayfası",
       not_="bil-serit-ucu ile aynı konu; yalnız biri kullanılır."),
    yd("zk-matkap-uclu-vida", "baglanti", "çatı, sac, çelik", "zor-yol", "zor-kolay",
       ["Sacı önce", "delip sonra", "mı vidalıyorsun?"],
       ("Önce delmek, sonra sac vidası takmak", "İki uç, iki iş"),
       ("Matkap uçlu vida: deler ve bağlar", "DIN 7504, tek seferde"),
       "Ucundaki matkap sacı deler, diş arkasından tutar. Sac kalınlığı sınırına bak.",
       "matkap uçlu vida din7504", "DIN 7504; üreticinin delme kapasitesi tablosu", dogrulandi=None),
    yd("zk-kademeli-uc", "matkap", "elektrikçi, sac işleri", "zor-yol", "zor-kolay",
       ["Deliği uç", "değiştirerek", "mi büyütüyorsun?"],
       ("Sacda deliği uç değiştirerek büyütmek", "Her çap için ayrı uç"),
       ("Kademeli (konik) uçla tek seferde", "Çapak da alır"),
       "İnce sacda kademeli uç istediğin çapa kadar iner; delik yuvarlak ve temiz çıkar.",
       "kademeli matkap ucu, konik matkap ucu", "Üretici ürün föyü", dogrulandi=None),
]

IPUCU = [
    dict(konu="Polyester sapan renkleri", ozet="EN 1492: mor 1 t, yeşil 2 t, sarı 3 t, gri 4 t, kırmızı 5 t, kahverengi 6 t, mavi 8 t, turuncu 10 t ve üstü. Esas olan mavi etiketteki değerdir; bağlama biçimi kapasiteyi değiştirir.",
         urun_ara="polyester sapan", kaynak="Certex, Mennens, LiftKing", dogrulandi=D),
    dict(konu="İmbus cıvata ve alyan ölçüleri", ozet="DIN 912: M3 2,5 · M4 3 · M5 4 · M6 5 · M8 6 · M10 8 · M12 10 mm alyan.",
         urun_ara="alyan anahtar takımı, imbus cıvata", kaynak="Brighton-Best DIN 912 / ISO 4762 föyü", dogrulandi=D),
    dict(konu="Paslanmazla çalışmanın 5 kuralı", ozet="Dişi yağla ve yavaş sık (sarma). Fırça ve taş paslanmaza ayrı olsun (demir bulaşması). Düşük devir, sabit baskı, kesme yağıyla del. 135° kobaltlı uç kullan. Mıknatıs testi yanıltır.",
         urun_ara="inox fırça, inox kesme taşı, kobalt matkap ucu", kaynak="BSSA, TWI", dogrulandi=D),
    dict(konu="Kesme taşının etiketi nasıl okunur", ozet="En yüksek devir ve çevre hızı (80 m/sn), son kullanma tarihi (metal halkada, üretimden en çok 3 yıl), ölçüler, kullanım kısıtı, EN 12413 işareti.",
         urun_ara="kesme taşı", kaynak="FEPA güvenlik föyü, oSa", dogrulandi=D),
    dict(konu="Eldiven etiketi: EN 388", ozet="Dört rakam ve bir harf: aşınma, kesilme (eski test), yırtılma, delinme, kesilme A–F (ISO 13997). F en yüksek.",
         urun_ara="iş eldiveni", kaynak="EN 388:2016 açıklamaları", dogrulandi=D),
    dict(konu="Tork anahtarı bakımı", ozet="İş bitince en düşük ayara al. Sökmede kullanma. Düşürme. Yılda bir ayar kontrolü. Klik sesinden sonra çekmeyi bırak.",
         urun_ara="tork anahtarı", kaynak="Snap-on ve Park Tool kılavuzları", dogrulandi=D),
    dict(konu="Elle kılavuz çekmenin 5 adımı", ozet="Doğru ön delik, dik başlangıç, kesme yağı, yarım tur ileri çeyrek tur geri, talaşı temizle. (Ön delik çapları 3 Aralık 2026'da işlendi; tekrar etme, yalnız anımsat.)",
         urun_ara="kılavuz pafta seti", kaynak="Sheldon Brown, ToolGuyd", dogrulandi=D),
    dict(konu="Fayans nasıl delinir", ozet="Darbe kapalı, fayans ya da elmas uç, düşük devir (1.000 dev/dk altı), hafif baskı; fayansı geçince beton ucuna geç.",
         urun_ara="seramik matkap ucu", kaynak="Bosch", dogrulandi=D),
]

# Yazı sığmazsa şablon küçültür (en az 60 px); bu sınırlar okunaklı kalması içindir.
SINIR = {"question": 20, "big": 8, "lines": 9, "label": 20, "answer_text": 18, "why_bil": 48, "hook": 16, "ne": 44, "alt": 38, "why_yd": 115}


def denetle():
    hata, ids = [], set()
    for f in FIKIRLER:
        assert f["id"] not in ids, f["id"]
        ids.add(f["id"])
        u = lambda alan, s, n: hata.append("%s: %s uzun (%d > %d): %s" % (f["id"], alan, len(s), n, s)) if len(s) > n else None
        if f["tur"] == "bil":
            assert len(f["question"]) == 2 and len(f["options"]) == 2 and f["answer"] in (0, 1) and len(f["why"]) == 2
            for s in f["question"]:
                u("question", s, SINIR["question"])
            for o in f["options"]:
                for s in ([o["big"]] if "big" in o else o["lines"]):
                    u("seçenek", s, SINIR["big" if "big" in o else "lines"])
                u("label", o.get("label", ""), SINIR["label"])
            u("answer_text", f["answer_text"], SINIR["answer_text"])
            for s in f["why"]:
                u("why", s, SINIR["why_bil"])
        else:
            assert len(f["hook"]) == 3 and f["cift"] in ("yanlis-dogru", "efsane-gercek", "zor-kolay")
            for s in f["hook"]:
                u("hook", s, SINIR["hook"])
            for k in ("yanlis", "dogru"):
                u(k + ".ne", f[k]["ne"], SINIR["ne"])
                u(k + ".alt", f[k]["alt"], SINIR["alt"])
            u("why", f["why"], SINIR["why_yd"])
    return hata


if __name__ == "__main__":
    h = denetle()
    for s in h:
        print("UYARI:", s)
    for f in FIKIRLER:
        if "not_" in f:
            f["not"] = f.pop("not_")
    veri = {
        "aciklama": "Reels ve İpucu için fikir dağarcığı. Kaynağı dagarcik_yaz.py; elle düzenleme. Kullanım ve kurallar: SENARYO.md. "
                    "dogrulandi boşsa fikir kullanılmadan önce bir kaynakla doğrulanır. Kullanılan fikirler state.json içindeki kullanilan_fikirler listesine yazılır.",
        "fikirler": FIKIRLER,
        "ipucu": IPUCU,
    }
    with open(os.path.join(ROOT, "dagarcik.json"), "w", encoding="utf-8") as fh:
        json.dump(veri, fh, ensure_ascii=False, indent=1)
    n = lambda t: sum(1 for f in FIKIRLER if f["tur"] == t)
    print("yazıldı: dagarcik.json  bil=%d  yd=%d  ipucu=%d  doğrulanmış=%d  doğrulanacak=%d"
          % (n("bil"), n("yd"), len(IPUCU), sum(1 for f in FIKIRLER if f["dogrulandi"]), sum(1 for f in FIKIRLER if not f["dogrulandi"])))
