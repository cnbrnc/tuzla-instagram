# Tuzla Hırdavat Instagram Robotu: Haftalık Talimat

Bu dosya, her Pazar 18:55'te (Türkiye saati) çalışan zamanlanmış görevin izlediği adımlardır.
16 Kasım 2026 haftasından itibaren geçerli düzen budur: Reels ve kaydırmalı gönderiler.
4 Ocak 2027 haftasından itibaren Reels türleri değişir: Pazartesi "Bil bakalım", Cuma "Yanlış / doğru" (kullanıcı 23 Kasım 2026'da onayladı).
Depo herkese açıktır; buraya şifre, anahtar veya kişisel bilgi yazılmaz.

## Sabit kurallar

- **Amaç:** tuzlahirdavat.com.tr'yi yaymak. Kullanıcının 23 Kasım 2026'daki sözüyle: yayılmak, izlenmek, ürünü tanıtmak, yeri geldiğinde bilgi vermek ve sayfayı popüler yapmak.
  - İçerik seçerken bu sırayı gözet: önce izlenir ve paylaşılır olsun, sonra ürünü göstersin. Bilgi doğru ve işe yarar olsun.
  - Reels, takip etmeyenlere ulaşır.
  - Kaydırmalı gönderiler kaydedilir ve paylaşılır.
  - Her gönderi, sitede aranacak bir kodla siteye yönlendirir.
- **Hesap:** Instagram @tuzla_civata_hirdavat, Metricool üzerinden yayınlanır. Metricool marka kimliği görev mesajında verilir.
- **Takvim:** Haftada 4 gönderi, hepsi saat **10:00** (Europe/Istanbul).

  | Gün | Biçim | Kuyruk listesi |
  |---|---|---|
  | Pazartesi | Reels: "Bil bakalım" (9 sn video) | `reels_bil` |
  | Çarşamba | Ürün kaydırmalısı (3 slayt) | `urun_carousel` |
  | Perşembe | Usta İpucu kaydırmalısı (5–8 slayt) | `ipucu_carousel` |
  | Cuma | Reels: "Yanlış / doğru" (9 sn video) | `reels_yd` |

  - 4 Ocak 2027'den önceki haftalarda iki Reels de ürün Reels'idir (`reels` listesi). Hangi listenin kullanılacağını `queue.json` içindeki `reels_slotlari` ayarı belirler; `hafta.py` ona bakar.
  - Ürün Reels'i (`reels`) yedek tür olarak durur. Kullanıcı isterse ya da iki yeni listede de öğe yazılamıyorsa kullanılır.

- **Tekli kart haftası:** HAFTA, `state.json` içindeki `last_tekli_week` tarihinden en az 42 gün sonraysa Perşembe günü İpucu yerine `tekli` listesindeki ilk kart kullanılır (`hafta.py --tekli`). Kampanya kartını kullanmadan önce eşiklerin sitede hâlâ aynı yazdığını kontrol et; değiştiyse görseli ve açıklamayı güncelle, kampanya kalktıysa kartı atla.
- **Fiyat yok:** Ne görselde ne açıklamada ürün fiyatı yazılır. Tek istisna, kampanya kartında sitede yazan kargo ve taksit eşikleridir.
- **İletişim:** Sipariş için satis5@tuzlacivata.com.tr, telefon 0542 189 02 69, site tuzlahirdavat.com.tr.
- **Onay şart:** Kullanıcı onay vermeden hiçbir gönderi Metricool'a planlanmaz ve hiçbir görsel ya da video depoya yüklenmez.
  - Tek istisna: Önceden planlanmış haftalar (aşağıda ayrı bölüm). Onları kullanıcı 6 Kasım 2026'da onayladı. Stokta olmayan ürünün gönderisini onaylı yedekle değiştirmeyi de o gün onayladı.
- **Metricool sınırı:** Ücretsiz planda ayda en fazla 20 planlı gönderi var. `state.json` içinde o aya düşen gönderiler ile yeni gönderilerin toplamı 20'yi geçecekse kullanıcıya söyle. Hikayeler de bu sınıra sayılır (`posted` kayıtlarındaki `hikaye` alanı).
- **Doğruluk:**
  - Ürün bilgisi yalnız ürün sayfasından alınır.
  - İpucu içeriklerinde her teknik bilgiyi (ölçü, standart numarası, değer) en az bir güvenilir kaynakla doğrula: standart kuruluşu, üretici kataloğu ya da teknik başvuru kaynağı. Emin olmadığın bilgiyi yazma.
- **Düzen değişikliği:** Haftalık düzeni, saati ya da biçimleri kendi başına değiştirme. Karneye göre ayda en fazla bir kez öneri yapabilirsin; karar kullanıcınındır.

## Biçimler ve alanlar

`queue.json` içindeki öğeler bu alanlarla yazılır. Yeni öğe eklerken oradaki örnekleri kopyala.

### Neden yeni Reels türleri (23 Kasım 2026)

İlk iki ürün Reels'inin sonucu:

- Açanların %73'ü ve %90'ı ilk 3 saniyede geçti. Ortalama izlenme 4,3 ve 1,9 saniye, erişim 182 ve 145 kişi oldu.
- Düz zemin üstünde yazıyla açılan video reklam gibi görünüyor.
- Tutan şey, "yanlış mı yapıyorsun?" diye dürten somut soruydu: "Kabloyu hâlâ maketle mi soyuyorsun?" 3 yorum aldı.

Yeni türlerin kuralları bundan çıkar. Yeni öğe yazarken hepsine uy:

- **İlk kare:** Soru ve görsel ilk karede ekranda olur. Boş zeminle açılmaz.
- **Bekleme nedeni:** İzleyen cevabı görmek için bekler. Cevap 4. saniyede gelir.
- **Soru:** Ustanın gerçekten yaptığı ya da merak ettiği somut bir şeyi sorar. Genel söz yazılmaz ("Kaliteli ürün arıyorsan" gibi).
- **Hedef:** İlk 3 saniyede geçenlerin oranını (karnede `gecme_orani`) düşürmek.

### Reels: "Bil bakalım" (`reel.py`, şablon `templates/reel_bil.html`, liste `reels_bil`)

1080×1920, 9 saniye. Akış:

- **0–1 sn:** Soru ve iki seçenek (A, B) ekranda.
- **1–4 sn:** 3-2-1 geri sayım ve "Tahminin ne? Yoruma yaz" çağrısı.
- **4 sn:** Doğru seçenek sarıya döner, yanlış solar. Cevap ve nedeni gelir.
- **6,75–9 sn:** "Sitede arat" kapanış kartı; video başa sarar.
- **Kapak:** 1,2. saniyedeki kare (soru, seçenekler ve "3").

Alanlar (`"template": "reel_bil"`):

- `tag`: `BİL BAKALIM`.
- `question_kicker`: en fazla 18 karakter, örnek `CIVATA BİLGİSİ`.
- `question`: 2 satır, her biri en fazla 14 karakter. Örnek: "Hangisi daha / sağlam?"
- `options`: tam 2 seçenek. Her biri şu üçünden biriyle gösterilir:
  - `head`: cıvata başına basılı yazı (en fazla 4 karakter, örnek "8.8", "A4"),
  - `big`: büyük yazı (en fazla 6 karakter, örnek "M8", "260°C", "DÜŞÜK"),
  - `lines`: iki satırlı büyük yazı (her satır en fazla 8 karakter, örnek `["HELİKOİL", "DİŞ"]`),
  - `product_url`: sitedeki ürünün fotoğrafı (yuvarlak ürünse `"image_shape": "daire"`).
  - İsteğe bağlı `label`: en fazla 14 karakter.
- `answer`: doğru seçeneğin sırası (0 = A, 1 = B). `answer_text`: "Cevap: …", en fazla 16 karakter.
- `why`: 2 satır, her biri en fazla 40 karakter. Kısa ve sayıyla söyle.
- `search_code`, `key`, `group`, `caption`; isteğe bağlı `url` (stok denetimi için ürün sayfası).
- `urun`: `{marka, ad, ozellik}`. `url` ile birlikte yazılırsa kapanış kartında ürünün fotoğrafı ve adı durur (aşağıda "Kapanışta ürün").
- `kaynak`: Cevabı doğruladığın kaynak, tek cümle. Videoda görünmez.

İçerik kuralları:

- **Tek doğru cevap:** Cevap tartışmasız olmalı ve bir standarda ya da üretici verisine dayanmalı. "Duruma göre değişir" denebilecek soruyu sorma.
- **Doğrula:** Her cevabı ve sayıyı en az bir güvenilir kaynakla doğrula; kaynağı `kaynak` alanına yaz.
- **Açıklamada cevabı verme:** İlk satır soruyu sorar. Gövdede "Tahminini yorumlara yaz. Cevap videonun sonunda." yazar.
- **Konu:** Bağlantı elemanı ve atölye bilgisi: kalite sınıfı, paslanmaz türü, ölçü, diş, matkap, aşındırıcı, anahtar.
- **Doğru cevabın yeri:** A ve B arasında değiştir; hep aynı tarafta olmasın.

### Reels: "Yanlış / doğru" (`reel.py`, şablon `templates/reel_yd.html`, liste `reels_yd`)

1080×1920, 9 saniye. Akış:

- **0–1,5 sn:** Kanca sorusu ve yanlış kullanılan ürünün görseli. Yuvarlak ürün (disk, taş) döner.
- **1,5 sn:** YANLIŞ paneli gelir; 2. saniyede kırmızı damga ve çarpı.
- **3,5 sn:** DOĞRU paneli gelir; 4. saniyede yeşil damga.
- **5 sn:** Tek cümlelik neden.
- **6,75–9 sn:** "Sitede arat" kapanış kartı.

Alanlar (`"template": "reel_yd"`):

- `tag`: `USTA HATASI`. `hook_kicker`: `SIK YAPILAN HATA`.
- `cift`: damga çifti (kurgu). Yazılmazsa `yanlis-dogru`. Öbürleri: `efsane-gercek` (EFSANE / GERÇEK) ve `zor-kolay` (ZOR YOL / KOLAY YOL; kırmızı çarpı ve hata sesi yok). Hangisinin ne zaman kullanılacağı ve etiketleri `SENARYO.md` dosyasında (bölüm 3).
- `kanca_kalibi` ve `fikir`: kancanın kalıbı ve dağarcıktaki kimliği (`SENARYO.md`, bölüm 2 ve 5). "Bil bakalım" öğelerine de yazılır.
- `hook`: 3 satırlık soru, her satır en fazla 13 karakter. Örnek: "Kesme taşıyla / taşlama mı / yapıyorsun?"
- `yanlis` ve `dogru`: her biri `{ne, alt, product_url, image_shape}`.
  - `ne`: ne yapıldığı, en fazla 36 karakter.
  - `alt`: ürünün adı, en fazla 28 karakter.
  - `product_url`: sitedeki ürün sayfası; fotoğrafı gösterilir. Yazılmazsa panelin sağında yalnız büyük çarpı ya da onay işareti durur (sitede ürünü olmayan şeyler için: çakmak, yandan çekiş).
  - `image`: ürün sayfası yerine hazır bir görsel dosyası (depoya göre yol). Örnek: bıçağın diş kısmının yakın kırpması.
- `hook_image`: kancada yanlış ürünün yerine gösterilecek görsel (isteğe bağlı; `bg_video` yoksa görünür).
- `urun`: `{marka, ad, ozellik}`; kapanış kartına ürünün fotoğrafını ve adını koyar (aşağıda "Kapanışta ürün").
- `why_kicker`: `Neden?`. `why`: en fazla 110 karakter.
- `url`: önerilen (doğru) ürünün sayfası. `search_code`, `key`, `group`, `caption`, `kaynak`.
- `bg_video`, `kaynak_video`: zemindeki stok görüntü ve kaynağı (aşağıda "Stok video zemini").

İçerik kuralları:

- **Yanlış olan kullanımdır, ürün değil:** YANLIŞ panelindeki ürünü de satıyoruz. Metin ürünü kötülemez; yanlış işte kullanıldığını söyler.
- **Güvenlik bilgisi:** Üretici kullanım talimatına ya da standarda dayanmalı. Kaynağı `kaynak` alanına yaz.
- **Stok:** Önerilen ürün stokta olmalı; `hafta.py` denetler.
- **Görsel:** İki ürünün de fotoğrafı net ve sade zeminli olsun.

### Reels: "Ürün tanıtımı" (`reel.py`, şablon `templates/reel_tanitim.html`)

Kullanıcı 23 Kasım 2026'da istedi: "Direkt ürünü tanıt, doğru yanlış yapma." Soru, geri sayım ya da YANLIŞ / DOĞRU paneli yoktur; video baştan sona ürünü gösterir.

- **Ne zaman:** Kullanıcı bir ürün bağlantısı verip tanıtım videosu istediğinde bu tür kullanılır. Böyle bir istekte "Bil bakalım" ya da "Yanlış / doğru" kurma.
- **Haftalık düzen:** Pazartesi ve Cuma türleri aynı kalır. Bu tür, kullanıcının istediği ek videolar içindir; kullanıcı düzenli olmasını isterse `reels_slotlari` ayarı değiştirilir.
- **Akış (9 sn):** Ürünün adı gerçek görüntünün üstünde (0–1,5 sn) · ürün fotoğrafı (1,5) · başlık (1,75) · özellikler tek tek (2,0 / 2,5 / 3,0 / 3,5) · rozet (4,0) · slogan (5,0) · kapanış kartı (6,75).
- **Alanlar (`"template": "reel_tanitim"`):**
  - `tag`: ürün türü, örnek `KAYNAK MAKİNESİ`. `hook_kicker` ve `marka`: marka adı.
  - `hook`: 3 satır, ürünün ne olduğu. İlk satır sarı çıkar; en güçlü özelliği oraya yaz. Örnek: "200 AMPER / çanta tipi / kaynak makinesi".
  - `baslik`: marka ve model, en fazla 22 karakter.
  - `ozellikler`: 3–4 madde, her biri en fazla 28 karakter.
  - `rozet` (isteğe bağlı): 2 kısa satır, örnek `["2 YIL", "GARANTİ"]`. `slogan` (isteğe bağlı): tek satır, en fazla 34 karakter.
  - `url`, `product_dir`, `search_code`, `urun`, `caption`, `kaynak`; `bg_video` ve `kaynak_video` (ürünün işini gösteren stok görüntü).
- **İçerik kuralı:** Her özellik ürün sayfasında yazıyor olmalı. Fiyat, "en ucuz", "yarı fiyatına" gibi kıyaslar ve rakip adı yazılmaz. Ürün stokta olmalı.
- **Ses:** `muzik` alanıyla profesyonel ses; `ses_pro.py urun` zaman çizelgesini kullanır.
- **Açıklama:** İlk satır ürünün adı ve en güçlü özelliği. Ardından sayfadaki özellikler, çağrı, sabit satırlar ve 5 hashtag.

### Reels: "Fragman" (`reel.py`, şablon `templates/reel_fragman.html`)

Kullanıcı 23 Kasım 2026'da "Ürün tanıtımı" videosunu görünce istedi: "Daha sinematik, daha senaryolu bir şey." Film fragmanı gibi kurulmuş ürün tanıtımıdır.

- **Akış (9 sn):** Dört gerçek sahne, her biri 1 saniye, kesimler müziğin vuruşunda; her sahnede kısa bir cümle (0–4 sn) · 4. saniyede müziğin düşüşüyle ürün ortaya çıkar · ad (4,25) · tür (4,5) · üç özellik (4,75 / 5,0 / 5,25) · slogan (5,5) · kapanış kartı (6,75). Üstte ve altta siyah sinema bantları durur.
- **Alanlar (`"template": "reel_fragman"`, `"stil": "sinematik"` şart):**
  - `sahneler`: 4 stok görüntü, her biri `{file ya da url, start, x, pan, hiz}`. `hiz` 1'den küçükse ağır çekim olur (50 kare/sn kaynakta 0,6 iyi durur). Son sahne ürünün arkasında bulanık olarak sürer.
  - `replikler`: 4 cümle, her biri 1–2 satır, satır başına en fazla 11 karakter, büyük harf. İkinci satır sarı çıkar.
  - `baslik` (marka ve model, en fazla 12 karakter), `tur_yazi` (ürünün türü, büyük harf), `ozellikler` (3 kısa madde, toplamı 36 karakteri geçmesin), `slogan` (tek satır).
  - `kapak_ms`: kapak karesi; `4900` yaz (ürünün ve adının göründüğü an). `planla.py` bunu Metricool'a iletir.
  - `url`, `product_dir`, `search_code`, `urun`, `tag`, `caption`, `kaynak`, `kaynak_video`.
- **Senaryo:** Cümleler ustanın derdinden ürüne gider; nasıl yazılacağı `SENARYO.md` dosyasında (bölüm 3, "Fragman").
- **Görüntü kuralları:** "Stok video zemini" bölümündeki kurallar aynen geçerli. Sahneler birbirinden farklı olsun (yakın, orta, geniş çekim) ve hepsi ürünün işini göstersin. Yüzü görünen kesiti kullanma.
- **Ses:** `ses_pro.py fragman`: her kesimde vuuş ve darbe, 4. saniyeye yükseliş, üründe büyük vuruş.
- **Uzun sürüm (`uzat`; 25 Kasım 2026):** Kullanıcı site filmi için "biraz daha uzun yap" dedi. Öğeye `"uzat": 6` yazınca film 15 saniye olur: sahneler 0–10 sn, ürün ya da site 10. saniyede (müziğin düşüşü), kapanış kartı 12,75'te. `uzat` çift sayı olmalı (2 sn = 1 ölçü).
  - `"replik_sure": 2`: her cümle 2 saniye ekranda kalır; cümle sayısı (4 + `uzat`) / `replik_sure` olur (15 saniyede 5 cümle). Her cümlenin altına 2–4 kesit koy (`"sure": 0.5` ya da `1.0`); son kesit hariç sürelerin toplamı düşüş anından küçük olsun.
  - `kapak_ms`: (4 + `uzat`) × 1000 + 900 (15 saniyelik filmde `10900`).
  - Ses: `reel.py` `ses_pro.py`'ye `--uzat` verir; müzik düşüşten o kadar önce başlar. Düşüşten önce yeterli süresi olmayan parçada hata verir; başka parça seç. Yapıyı en iyi taşıyan parça `e` (düşüşe doğru yükseliyor).
  - Yalnız fragman türünde çalışır. Örnek: `taslak/site-tanitim/site-tanitim-uzun.json`.
- **Fotoğraftan sahne (`foto_sahne.py`; 25 Kasım 2026):** Videosu bulunmayan konu (belirli bir gemi, araç) serbest lisanslı fotoğrafla gösterilir. `python3 foto_sahne.py <foto> work/foto/s-<ad>.mp4 --hf <pencere yüksekliği> --ust <üst kenar> --sol <başlangıç> <bitiş> --sure 2` fotoğrafı yavaş kayan bir kesite çevirir; sonra `sahneler` içinde sıradan video gibi kullanılır. Öğeye fotoğrafın sayfa adresini (`foto`) ve ayarı (`foto_ayar`) yaz.
  - Pexels fotoğrafı: `https://images.pexels.com/photos/<no>/pexels-photo-<no>.jpeg?auto=compress&cs=tinysrgb&w=2600`. Arama sayfasını WebFetch ile açıp fotoğraf numaralarını al.
  - **Kullanıcının gönderdiği başkasına ait video (YouTube indirmesi, ajans ya da televizyon görüntüsü) kullanılmaz; logo kırpılmaz.** Kullanıcı ısrar etse de kural aynı; sahibinin yazılı izni gelirse kullanılır. Aynı konuyu serbest lisanslı görüntüyle göster.
  - Kullanıcı tercihi: askerî gemi gösterilecekse yalnız Türk Donanması; ABD Donanması görüntüsü kullanma.
- **Pixabay dosya adresi:** Video sayfaları bu ortamdan açılmıyor (403). Arama sayfasını (`pixabay.com/videos/search/<kelime>/`) WebFetch ile aç ve her sonucun "Edit video" (Canva) bağlantısındaki `file-url` değerini iste; çözülmüş hali `https://cdn.pixabay.com/video/…_large.mp4` olur ve `curl` ile iner. "Ai Generated" etiketli klibi alma.
- **Sektör bilgisi (kullanıcı, 25 Kasım 2026):** A4-316 paslanmaz en çok tersaneye, ayrıca savunma sanayine satılıyor; sitede M1,6'dan M48'e var. Örnek film: `taslak/a4-tersane/a4-tersane.json`.
- **GFB (25 Kasım 2026):** Kullanıcı GFB kataloglarını gönderdi (XPRO darbeli bits kataloğu ve fiyat listesi). Kataloglar fiyat listesidir: **fiyat kullanılmaz**; katalog kendi görsellerinin izinsiz kullanılamayacağını yazar: **ürün fotoğrafı siteden alınır** (sitede 1.080 GFB ürünü; `work/products.xml` içinde `gfb` ara). Ürün grupları: matkap uçları (HSS, kobaltlı, kademeli, SDS-Plus), kılavuz ve pafta, panç, parmak freze, XPRO bits uçları, ölçü aletleri. Film taslağı: `taslak/gfb-tanitim/gfb-tanitim.json` (onay bekliyor). GFB filminde başka markanın kutusu görünen raf çekimi (3595) kullanılmaz; depo rafları (3601, 3602) kullanılır. **Marka filmi (kullanıcı "daha GFB özel" istedi):** her cümlede marka adı geçer ve `replik_urun` ile o cümlenin gerçek ürünü üstte kartta durur (`[{"product_dir", "marka", "kod", "ad"} | null]`, cümle başına bir öğe). Cümle yalnız stokta olan ürünle kurulur; stok görüntüdeki alet temsilîdir, bunu kullanıcıya söyle. Soluk kesitte sahneye `"kontrast": 1.2–1.4` ver.
- **Markanın kendi hesabı için film (istisna, 25 Kasım 2026):** GFB, kendi hesabında paylaşmak üzere Tuzla Hırdavat tanıtımı olmayan bir video rica etti; kullanıcı istedi. Bunun için `"marka_filmi": {"ad", "ust", "web"}` alanı var: üstte Tuzla logosu yerine marka adı, kapanışta yalnız marka adı ve markanın kendi web adresi çıkar; Tuzla'nın sitesi, e-postası, telefonu, deposu ve "sitede arat" olmaz. `replik_urun` öğesi liste olabilir (cümle içinde kart değişir), `"mozaik_satir": 3` dokuz karo verir. `"mozaik_sutun": 4` ile birlikte 12 karo olur. `uzat: 8` ile film 17 sn ve 6 cümle olur (kapak 12900 ms). Çeşit vurgusu için cümle başına 4 kart (0,5 sn'de bir değişir) kullanıldı: `taslak/gfb-tanitim/gfb-marka-cesit.json`. Marka kendi ürününü tanıttığı için stok şartı aranmaz; fiyat yine yazılmaz. Örnek: `taslak/gfb-tanitim/gfb-marka.json`. **Bu filmler bizim hesapta yayınlanmaz, planlanmaz, depoya konmaz;** dosya kullanıcıya verilir. Başka bir marka için ancak kullanıcı isterse yapılır.
- **Site tanıtımı (`mozaik`; 25 Kasım 2026):** Kullanıcı site için de "tanıtım filmi" istedi. Aynı tür kullanılır; tek ürün yerine 6 ürün karosu çıkar. Öğeye `mozaik` yaz: 6 adet `{"product_dir": "work/<ürün>"}`. `product_dir`, `url` ve `urun` yazılmaz; `baslik` "TUZLA HIRDAVAT", `tur_yazi` "20.000+ ÜRÜN · TEK ADRES", `kapanis_k` "HEMEN GİR", `search_code` site adresi olur. Karolara stokta olan ürünleri koy; ürün sayısını `work/products.xml` ile doğrula. Örnek: `taslak/site-tanitim/site-tanitim-filmi.json`.
- **Ne zaman:** Kullanıcı bir ürün için tanıtım istediğinde önce bu türü hazırla; uygun görüntü bulunamazsa "Ürün tanıtımı" türüne dön ve nedenini kullanıcıya yaz.

### Reels: "Oyun" (`reel.py`, şablon `templates/reel_oyun.html`)

Kullanıcı 23 Kasım 2026'da "GTA 6 temalı site tanıtımı" istedi. Gerçek bir oyunun adı, logosu, yazı tipi ya da görünümü kullanılamaz (tescilli marka; hak ihlali ve Instagram'da kaldırılma riski). Bunun yerine özgün, oyun arayüzü temalı bir site tanıtımı kuruldu: kendi renklerimiz ve yazı tipimizle "görev" kurgusu.

- **Akış (9 sn):** Açılış ekranı (0–1,5 sn) · görev kartı (1,5) · dört madde tek tek tamamlanır ve puan çubuğu dolar (2,0 / 2,5 / 3,0 / 3,5) · "GÖREV TAMAM!" (4,0) · site adresi ve üç kısa bilgi (5,0) · kapanış kartı (6,75).
- **Alanlar (`"template": "reel_oyun"`, `"stil": "sinematik"`):** `hook_kicker`, `hook` (2 satır), `gorev` `{no, seviye, ad}`, `maddeler` (4 adet: `ad`, `product_url` ya da `product_dir`, isteğe bağlı `xp`), `tamam`, `odul`, `cagri_ust`, `cagri`, `cipler` (3), `kapanis_k` (kapanış kartının küçük başlığı; site tanıtımında "HEMEN GİR"), `search_code` (site tanıtımında site adresi), `caption`, `kaynak`.
- **Kural:** Başka bir markanın ya da eserin (oyun, film, dizi, karakter) adı, logosu, kapağı ve tanınan görünümü hiçbir gönderide kullanılmaz. Kullanıcı böyle bir tema isterse nedenini bir cümleyle söyle ve aynı fikri özgün bir tasarımla yap.
- **Sayılar:** "20.000+ ürün" gibi bir sayı yazılacaksa `work/products.xml` içindeki ürün adresi sayısından doğrula.

### Ek fragmanlar: onaylı, bitmiş videolar (`ek.py`, liste `ek_fragman`)

Kullanıcı 23 Kasım 2026'da 5 fragmanı izledi ve "kalanı hangisi iyi olacaksa onu yap" dedi. Paslanmaz DIN 933 fragmanı 1 Aralık'a planlandı. Kalan dördü Aralık'ın sınırına (ayda 19) sığmadığı için sıraya alındı: İzeltaş 35 parça lokma, Karbosan Thinline kesme taşı, Tyrolit flap disk, Egesan inox kesme taşı.

- **Videolar hazır:** `posts/ek/fragman-<anahtar>.mp4` ve `-kapak.jpg`. Yeniden üretme; `reel.py` `"hazir": true` yazan gönderiyi atlar.
- **Taslaktan üretilen öğe (`taslak`):** Listede `medya` yerine `taslak` yazan öğenin videosu depoda yoktur (kullanıcı "Ocak'a sakla" dedi ama yayın onayı Pazar mesajında alınacak). `ek.py ekle` onu taslak tanımından kendisi üretir; eksik stok kesitlerini `url` alanından indirir. Sıranın başındaki öğe: Rayno 200A ikinci reklam filmi.
- **Aynı Salı dolu ise:** `state.json` içinde o Salı için kayıtlı gönderi varsa `ek.py` eklemez (5 Ocak 2027: site tanıtım filmi).
- **Ne zaman:** 4 Ocak 2027 haftasından itibaren, liste bitene kadar, haftada en fazla bir tane; **Salı 10:00**. Haftanın 4 gönderisine ektir, onların yerine geçmez.
- **Nasıl:** `python3 hafta.py <HAFTA>` çalıştıktan sonra `python3 ek.py ekle <HAFTA>` çalıştır.
  - Ayın toplamı (gönderi + hikaye) 19'u geçecekse eklemez ve bunu söyler; o hafta ek video çıkmaz.
  - Ürünün stokta olduğuna bakar; stokta değilse sıradakine geçer.
  - Videoyu `out/<HAFTA>/` klasörüne kopyalar ve gönderiyi `weeks/<HAFTA>.json` dosyasına `"ek": true` ile ekler.
  - `hafta.py` yeniden çalışırsa `ek.py ekle` komutunu da yinele.
- **Onay:** Pazar günkü onay mesajında 5. gönderi olarak göster ("Ek: Salı 10:00, fragman") ve videoyu gönder. Kullanıcı istemezse `weeks/<HAFTA>.json` dosyasından çıkar; öğe listede kalır.
- **Sonrası aynı:** `planla.py kopyala`, `json` ve `durum` ek gönderiyi öbürleriyle birlikte işler; `durum` öğeyi listeden düşer. Kapak karesi 4900 ms'dir (`kapak_ms`).
- `python3 ek.py liste`: sıradaki videoları ve önümüzdeki ayların sayımını gösterir.
- **Yeni fragman:** Liste bitince kendi başına yenisini ekleme. Kullanıcı bir ürün için tanıtım isterse "Fragman" türünde hazırla, onaya sun.

**Kapanışta ürün (`urun`):** Amaç bilgi verirken ürünü de tanıtmak. Öğede `url` (ürün sayfası) ve `urun` varsa kapanış kartında "Sitede arat" kodunun altında ürünün fotoğrafı, markası ve adı durur.
- `kicker` (isteğe bağlı): fotoğrafın yanındaki küçük başlık. Yazılmazsa "BU İŞİN ALETİ". Alet olmayan ürünlerde (cıvata, eldiven) "SİTEMİZDE" yaz.
- `marka`: en fazla 10 karakter, büyük harf. `ad`: en fazla 30 karakter. `ozellik`: en fazla 36 karakter, " · " ile ayrılmış 2–3 özellik.
- Fiyat yazılmaz. Soru ya da hata o ürünün işiyle ilgili olsun (somun sıkma → hangi lokma; ısıtıcı → hangi priz).
- Ürünle ilgisi olmayan genel bilgi sorusunda `urun` yazma.

**Koyu sahnede ürün fotoğrafı:** Sinematik stilde beyaz zeminli ürün fotoğrafı beyaz, köşesi yuvarlak bir karo içinde durur (şablon kendisi yapar). Yuvarlak ürün (`"image_shape": "daire"`) daire olarak kalır.

**Yeni türlerde ses:** Her türün kendi sesi vardır: `assets/reel-ses-bil.wav` ve `assets/reel-ses-yd.wav`; kaynağı `ses_tur.py`. Kapanıştaki "tınn" ve melodi ürün Reels'iyle aynıdır. `ses` alanı yazılmaz; `reel.py` türe göre seçer. Şablonlardaki zamanlar değişirse `ses_tur.py` içindeki zamanları da güncelle ve iki dosyayı yeniden üret.

**Sinematik stil (kullanıcı 23 Kasım 2026'da seçti; 4 Ocak 2027'den itibaren varsayılan):** İki yeni tür sinematik stilde üretilir: koyu sahne, kenarlarda kararma, film greni, yavaş kamera yaklaşması ve fragman havasında ses (`assets/reel-ses-bil-sin.wav`, `reel-ses-yd-sin.wav`; `ses_tur.py --stil sinematik`).
- `hafta.py`, `queue.json` içindeki `reels_slotlari.stil` ayarına bakar ve gönderiye `"stil": "sinematik"` yazar. Öğeye ayrıca yazmana gerek yok.
- **"Bil bakalım":** Çoğunlukla kodla üretilmiş sahneyle çıkar; soru ve kartlar ekranı doldurur. Konuyu doğrudan gösteren, sade bir kesit varsa `bg_video` yazılabilir.
- **"Yanlış / doğru":** Zeminde gerçek stok görüntü olur (`bg_video`, aşağıda). Uygun kesit bulunamazsa `bg_video` yazma; şablon yuvarlak ürünü (disk, taş) ağır çekimde döndürür ve kodla kıvılcım çizer.

**Profesyonel ses (`muzik`; kullanıcı 23 Kasım 2026'da istedi):** Sinematik Reels'in sesi stok müzik, stok efekt ve kendi imza seslerimizin karışımıdır. `ses_pro.py` üretir; kaynaklar `assets/ses-kaynak.json` dosyasındadır.
- **Müzik çeşitliliği (kullanıcı 23 Kasım 2026: "Hep aynı melodi, izleyeni sıkar"):** Kütüphanede 6 ayrı parça var; kimlikleri `a`–`j` (`a`, `b`, `c` ilk parçanın bölümleri; `d` savaş davulları, `e` sert rock, `f` ve `i` tekno, `g` ve `j` sinematik hip-hop, `h` hareketli vurmalı).
  - `hafta.py` yeni türlere `muzik` alanını `assets/ses-kaynak.json` içindeki `sira` listesinden sırayla yazar. Art arda iki Reels aynı parçayla çıkmaz.
  - Müzik öndedir; ortak efektler (vuruş, vuuş, yükseliş) ve imza sesler geride kalır. "Fragman" ve "Ürün tanıtımı" türlerinde melodik "ding" çalmaz.
  - Yalnız sesi değiştirmek için: `python3 ses_degistir.py <video> <tür> <kimlik> <çıktı>` (görüntü aynen kalır).
  - **Kütüphaneyi büyüt:** Ayda en az bir yeni parça ekle. Parça sayfasındaki veride "Content ID Registered" olmamalı (arama listesinde kalkan simgesi olan parçalar kayıtlıdır; onları alma). `python3 muzik_olc.py --bas <mp3>` tempoyu ve başlangıç anını ölçer; sonucu `muzikler` altına yaz ve kimliği `sira` listesine ekle. Tempo 100–145 arasında olsun.
  - Kullanıcı bir parçayı beğenmezse `sira` listesinden çıkar.
- Müzik 120 BPM'e getirilir; düşüşü 4. saniyeye, yani cevabın ya da DOĞRU damgasının geldiği ana oturur.
- `"sfx_kanca": "taslama"`: Kancaya gerçek taşlama sesi ekler. Yalnız taş, disk ve spiral konularında yaz.
- Müzik ya da efekt indirilemezse `reel.py` uyarı verir ve kodla üretilmiş sinematik sesi kullanır. Gönderi yine çıkar.
- **Yeni müzik ya da efekt seçerken:**
  - Yalnız ticari kullanımı serbest kaynak: Pixabay (müzik ve efekt). Başkasının videosundan ses alınmaz.
  - YouTube Content ID'ye kayıtlı parçayı seçme; Instagram'da telif uyarısına yol açabilir. Pixabay arama sayfasındaki veride `hasYoutubeContentId` alanı `false` olmalı.
  - Seçtiğin parçayı `assets/ses-kaynak.json` dosyasına adı, yapanı ve adresiyle yaz. Dosyayı depoya koyma.
  - Müziği değiştirirsen `bpm`, `faz` ve `varyantlar` değerlerini yeniden ölç; vuruşlar 0. ve 4. saniyeye oturmalı.

**Stok video zemini (`bg_video`):** `{"url": "<mp4 adresi>", "start": <sn>, "x": <0–1>, "pan": <0–0,08>}`. `hafta.py` dosyayı `work/stok/` klasörüne indirir; indiremezse uyarı verir ve gönderi kodla üretilmiş sahneyle hazırlanır.
- **Kaynak:** Yalnız ticari kullanımı serbest stok siteleri: Pexels ve Pixabay. Başkasının YouTube, Instagram ya da TikTok videosundan kesit alınmaz.
  - **Mixkit (25 Kasım 2026'da eklendi):** Her klibin lisansı ayrıdır. Klip sayfasında "Mixkit Stock Video Free License" yazıyorsa kullan; **"Mixkit Restricted License" (yalnız kişisel kullanım) yazıyorsa kullanma.** Sayfayı `curl` ile aç ve `data-license="videoFree"` ara. Sayfanın gizli verisindeki (`ld+json`) `license` alanına güvenme; kısıtlı kliplerde de "videoFree" yazıyor. Yalnız indirme düğmesinin yanındaki `data-license` etiketine bak. 25 Kasım'da bakılan 92 klibin 42'si kısıtlıydı; kaynak yakın çekimlerinin hepsi kısıtlı. Dosya adresi: `https://assets.mixkit.co/videos/<no>/<no>-1080.mp4`. İşe yarayanlar: kıvılcım ve kor görüntüleri (3460, 3463, 3465, 684), şantiyede kaynakçı (4125).
  - **Coverr (25 Kasım 2026'da eklendi):** Lisans ticari kullanıma açık, kaynak gösterme yok. Arşivi küçük; hırdavat konularında az şey var (kaynak aramasında işe yarar klip çıkmadı). Adı `user-ai-generation` ile başlayan klipler yapay zekâ üretimidir, alma. Shutterstock'a giden bağlantılar ücretlidir. Dosya adresi: `https://cdn.coverr.co/videos/<ad>/1080p.mp4`.
  - **Kullanma:** Vecteezy, Videezy, Dareful, Vidsplay (ücretsizde kaynak gösterme şart); Videvo ve Mazwai (adresleri başka siteye yönleniyor).
  - **Kullanıcıya soruldu, cevap bekliyor (25 Kasım 2026):** ISO Republic (CC0, yaklaşık 130 klip; alan adı izni gerekir), Unsplash fotoğrafları (ticari kullanım serbest, kaynak gösterme yok; fotoğraf yavaş kamera hareketiyle sahne olur), Adobe Stock ücretsiz koleksiyonu (ticari lisans; Adobe hesabı ister, robot indiremez, kullanıcı indirip gönderebilir).
- **Nasıl bulunur:**
  1. WebSearch ile ara; `allowed_domains` olarak `pexels.com` ya da `pixabay.com` ver. Örnek sorgu: "angle grinder sparks video".
  2. Video sayfasını WebFetch ile aç ve doğrudan dosya adresini iste (`videos.pexels.com/video-files/…mp4` ya da `cdn.pixabay.com/video/…mp4`). Lisans etiketini de oku.
  3. Dosyayı `curl -A "Mozilla/5.0"` ile `work/stok/` klasörüne indir. Site sayfaları `curl` ile açılmaz; yalnız dosya adresleri açılır.
  4. `ffmpeg` ile saniyede bir kare çıkarıp Read ile bak. 9 saniye boyunca hareketin sürdüğü bir başlangıç anı (`start`) seç.
- **Seçim kuralları:**
  - Kesit, kancadaki hatayı ya da işi doğrudan göstersin (taşlama sorusunda taşlama görüntüsü).
  - Yüzü tanınan kişi ve okunur marka olmasın.
  - Koyu zeminli, yakın çekim, hareketli kesit en iyi sonucu verir. En az 1280 piksel genişlik olsun.
- **Kırpma:** Görüntü yataysa dikeye kırpılır. `x`, kırpmanın yatay merkezidir (0 sol, 1 sağ); hareketin olduğu yeri ortala. `pan`, 9 saniyede sağa kayma oranıdır.
- **Kontrol:** Üretimden sonra karelere bak: kanca yazısı görüntünün üstünde okunuyor mu, kesit konuyla ilgili mi?
- **Kayıt:** Öğeye `kaynak_video` alanında sayfa adresini, yükleyeni ve lisansı yaz.
- **Depoya yükleme:** Stok dosyasını depoya koyma; lisans tek başına dağıtıma izin vermez. `work/` zaten yok sayılır. Yalnız bitmiş Reels videosu `posts/` klasörüne girer.
- **Erişim:** Kullanıcı `www.pexels.com`, `videos.pexels.com`, `pixabay.com`, `cdn.pixabay.com`, `mixkit.co`, `assets.mixkit.co`, `coverr.co` ve `cdn.coverr.co` adreslerine izin verdi. Mixkit ve Coverr sayfaları `curl` ile açılır. Erişim kapalıysa tekrar deneme; gönderiyi kodla üretilmiş sahneyle hazırla ve kullanıcıya yaz.

**Gerçek çekim (25 Kasım 2026'da başladı):** Kullanıcı dükkânında telefonla çektiği 11 kısa videoyu sohbete ekledi (IMG_3592–3602; dik, 4K, 3–8 sn). Site tanıtım filmi bu görüntülerle kuruldu (`taslak/site-tanitim/site-tanitim-dukkan.json`).
- **Hazırlık:** Her dosyayı `ffmpeg -i <mov> -vf "scale=1080:1920,fps=30" -c:v libx264 -crf 15 -an work/dukkan/d-<no>.mp4` ile çalışma boyutuna getir; telefonun döndürme bilgisini ffmpeg kendisi uygular.
- **İçerik (25 Kasım çekimleri):** 3592 mağaza içi ve el aletleri duvarı · 3593 el aletleri · 3594 elektrikli aletler · 3595 kutulu raflar · 3596 çekiçler · 3597 kesme taşı duvarı · 3598 ve 3599 dış cephe (tabelalar) · 3600 "tuzla CIVATA HIRDAVAT" tabelası · 3601 cıvata deposu rafları · 3602 raf arasında yürüyüş.
- **Kurgu:** Fragman türünde bir cümleye iki yarım saniyelik kesit konabilir (`"sure": 0.5`); kesimler yine vuruşa oturur.
- **Gizlilik:** Araç plakası, başka firmanın araç yazısı ve tanınan yüz görünmesin. Gerekirse kesiti önceden kırp (3600 için `crop=750:1334:180:270`). Kullanıcının kendi tabelası ve bayisi olduğu markaların tabelaları kalabilir.
- **Saklama:** Çekimler yalnız o sohbetin çalışma klasöründedir (`work/dukkan/`); depoya konmadı. Kullanıcı izin verirse kalıcı bir yere (depo ya da Drive) alınır; izin yoksa her kullanımda yeniden istenir.
- Kullanıcının şirket sitesindeki galeri (`tuzlacivata.com.tr/galeri`, "Depomuzdan Kareler", 31 fotoğraf) da kullanılabilir; bağlantı bu ortamdan yavaş ve kesintili.
- Cuma Reels'i "Yanlış / doğru" olarak kalır; gerçek çekim, uygun kesit olduğunda stok görüntünün yerine kullanılır.

### Ürün Reels'i (`reel.py`, şablon `templates/reel.html`, liste `reels`)

1080×1920, 9 saniye, 30 fps. İzleyiciyi tutmak için kuruldu (kullanıcı 6 Kasım 2026'da istedi):

- **0–2 sn:** Kanca sorusu. Satırlar vuruşla çarparak gelir (0 / 0,25 / 0,5 sn); ilk karede ses var.
- **2 sn:** Ürün paneli müziğin "düşüş" anında gelir.
- **2,5–6,5 sn:** Başlık 2,5'te gelir. Ürün 3 ve 3,5'ta vuruşla yakınlaşır, çipler 4 / 4,5 / 5'te gelir. 6'da ürünün üstünden bir parlama geçer. Her 0,5–1 saniyede ekranda bir şey değişir.
- **7–9 sn:** "Sitede arat" kapanış kartı. Ses sonda yükselir ve video başa kesintisiz sarar; tekrar izlenmesi süreyi artırır.
- **Kapak:** 1,2. saniyedeki kare (kanca).

Alanlar:

- `hook_kicker`: Üstteki küçük etiket, en fazla 18 karakter. Örnek: `USTA SORUSU`, `ATÖLYE SORUSU`.
- `hook`: 3 satırlık soru, her satır en fazla 12 karakter.
  - Ustanın derdinden başla: "Kabloyu hâlâ / maketle mi / soyuyorsun?"
  - Ürün adını kancaya yazma.
- `title`: Ürün sahnesindeki tek satır, en fazla 16 karakter. Fayda söyler: "Tek hamlede soy."
- `chips`: 3 teknik bilgi, her biri en fazla 22 karakter.
- `tag`: Sağ üst etiket. Sitede "Yeni Ürün" ise `YENİ ÜRÜN`, değilse kategori adı.
- `brand`, `sku`: Panelin üstünde durur; marka büyük harfle yazılır.
- `search_code`: Kapanış kartındaki arama kodu, en fazla 12 karakter. Sitede aratınca ürünü bulduran model kodu; kod yoksa ürün adından 2 kelime.
- `key`, `url`, `group`, `caption`.

Şablon taşan satırı kendisi küçültür, ama karakter sınırlarına yine de uy.

**Ses:** Her Reels'e kodla üretilmiş özgün ses gömülür; telif sorunu yoktur. `reel.py` bunu kendisi yapar.
- **İmza sesler her Reels'te aynıdır:** başta "tak-tak-TAK", ürün gelirken düşüş, çiplerde "pıt", parlamada "şing", kapanışta metal "tınn". Bunlar markanın sesi olur.
- **Ritim üç türlü:** `enerjik`, `atolye` (cırcır, çekiç), `derin` (yarım tempo). Akılda kalan kısa melodi hepsinde vardır.
- **Sıra:** `hafta.py` ritimleri sırayla dağıtır (`state.json` içinde `ses_sirasi`), böylece aynı hafta iki Reels'te aynı ritim olmaz. `planla.py durum` sırayı ilerletir.
- **Dosyalar:** `assets/reel-ses-<ritim>.wav` ve `assets/reel-ses-efekt.wav` (yalnız efekt); kaynağı `ses.py`.
- **Gönderideki `ses` alanı:** ritim adı, `"efekt"` (Instagram müziği eklenecekse) ya da `"yok"`.
- **Zamanlama:** `reel.html` içindeki animasyon zamanları değişirse `ses.py` içindeki zamanları da güncelle ve dört dosyayı yeniden üret.
- **Karne:** Karnede ritimlere göre izlenme ve paylaşımı da not et. Birkaç hafta sonra hangi ritim daha iyi gidiyorsa kullanıcıya öner.

### Ürün kaydırmalısı (3 slayt)

1. **`urun` (kapak):**
   - `tag`, `brand`, `sku`
   - `headline`: 2 satır, her biri en fazla 18 karakter
   - `product_line`: en fazla 48 karakter
   - `chips`: 3 adet, her biri en fazla 22 karakter
2. **`slide_liste`:**
   - `kicker`: örnek `NEREDE İŞİNE YARAR?`
   - `headline`: 2 satır, her biri en fazla 16 karakter
   - `items`: 4 madde; `title` en fazla 24, `text` en fazla 60 karakter
   - Konu şunlardan biri olur: kimin işine yarar, nerede kullanılır, seçerken neye bakılır, doğru kullanım kuralları. Yalnız ürün sayfasındaki ya da genel kabul görmüş teknik bilgiye dayan.
3. **`slide_cta` (sarı zemin):**
   - `headline: ["Sitede arat:", "<arama kodu>"]`
   - `lead`
   - `actions: ["Kaydet", "Ustana gönder"]`
   - `card`: queue.json'daki sipariş kartını aynen kopyala

Gönderi düzeyinde şu alanlar bulunur:

- `key`, `url`, `group`, `caption`
- `theme`: Yoksa `hafta.py` açık ve koyu temayı sırayla verir.
- `alt`: Her slayt için kısa görsel açıklaması, slayt sayısı kadar.

### Usta İpucu kaydırmalısı (5–8 slayt, lacivert)

1. **`slide_kapak`:**
   - `kicker`: `USTA İPUCU · <KONU>`
   - `headline`: 2–3 satır
   - `lead`: tek cümle
   - `illustration_file`: isteğe bağlı, `assets/` içindeki SVG
2. **`slide_madde` (her madde bir slayt):**
   - `code`: en fazla 8 karakter, örnek "M8", "DIN 933"
   - `headline`: 1–2 satır
   - `text`: en fazla 120 karakter
   - `tip`: "USTA NOTU" kutusu, en fazla 110 karakter
   - Görsel olarak ya `product_url` (sitedeki ürün sayfası; ürün fotoğrafı gösterilir) ya da `illustration_file` ver.
3. **`slide_cta` (son slayt, sarı):**
   - `kicker: "KAYDET · PAYLAŞ"`
   - `headline`, `lead`, `actions`, `card`

Gönderi düzeyinde şu alanlar bulunur:

- `key`, `caption`
- `group`: bağlantı elemanı konularında `baglanti`
- `theme: "dark"`
- `alt`

Konuyu `queue.json` içindeki `ipucu_konulari` listesinden sırayla al. Aynı konuyu 8 hafta içinde tekrarlama; `state.json` içindeki `posted` listesine bak.

### Tekli kart

`kampanya` ve `toplu` şablonlarını kullanır; öğeler `queue.json` içindeki `tekli` listesindedir. `bilgi` ve `karsilastirma` şablonları da duruyor, ama yeni düzende bilgi içeriği kaydırmalı olarak hazırlanır.

### Hikaye denemesi (16 ve 23 Kasım 2026 haftaları)
Kullanıcı 9 Kasım 2026'da onayladı. `state.json` içindeki `hikaye_denemesi` ayarı hangi haftalarda yapılacağını söyler.

- **Ne yapılır:** Bu haftalarda iki Reels, aynı gün 18:00'de Instagram hikayesi olarak da yayınlanır.
  - Video aynıdır. Hikayeye metin, bağlantı ya da çıkartma eklenmez; otomatik yayında Instagram bunlara izin vermez.
- **Ek iş yok:** `hafta.py` bu haftaların Reels'lerine `"hikaye": "18:00"` yazar. `planla.py json` her biri için `<id>-hikaye` girişini kendisi ekler.
- **Sınır:** Hikayeler Metricool'un aylık 20 sınırına sayılır. Kasım: 13 gönderi + 4 hikaye = 17.
- **Ölçüm:** 3. adımdaki hikaye isteğiyle her hikayenin erişimini karneye yaz.
- **Sonuç (3 Ocak 2027 çalışması):** Onay mesajının başına 2–3 satır yaz:
  - 4 hikayenin erişimi, yanıtı ve çıkışı,
  - aynı günün Reels erişimiyle kıyas.
  - Sonra kullanıcıya hikayeye devam edilip edilmeyeceğini sor.
  - Ona şunu hatırlat: her gönderiye hikaye için ücretsiz planın sınırı yetmez, Metricool Starter gerekir (9 Kasım 2026'da aylık 20 € + KDV).
  - Kullanıcı karar vermeden yeni bir hafta için hikaye planlama.

## Açıklama (caption) kuralları

Açıklama bu sırayla yazılır:

1. **İlk satır:** Aranacak kelime ve fayda, en fazla 125 karakter. Instagram bu kısmı "devamı" demeden gösterir, aramada da bu kelimeler işe yarar. Örnek: "Kablo soyma pensesi ile 0,2–6,0 mm² kabloyu tek hamlede, iletkeni çizmeden soy. ⚡"
2. **Gövde:** 1–2 kısa cümle, ürün sayfasındaki bilgilerle.
3. **Kaydırmalıda:** `👉 Kaydır: <2. slaytın konusu>`
4. **Kaydet ve paylaş çağrısı:** `💾 Kaydet, lazım olur.` ve/veya `📤 <meslek> arkadaşına gönder.`
5. `🔎 Sitede “<arama kodu>” arat` (İpucu ve tekli kartta isteğe bağlı)
6. `🛒 tuzlahirdavat.com.tr`
7. `✉️ Sipariş: satis5@tuzlacivata.com.tr`
8. `📞 0542 189 02 69`
9. **Hashtag:** Boş satırdan sonra **tam 5 hashtag**. Instagram en fazla 5 hashtag'e izin veriyor.

Metnin tamamı Türkçe olur. Bağırma (ünlem yağmuru, büyük harfle yazı) yok. Özellik, sertifika, garanti ya da stok adedi uydurma.

### Hashtag kuralı (5 adet, bu sırayla)

1. **Ürün tipi:** `#kablosoyma`, `#elfeneri`, `#kaynakmakinesi`, `#cıvata`, `#kılavuz`…
2. **Marka:** Biliniyorsa en yaygın yazılışıyla: `#gedore`, `#izeltaş`, `#kolege`. Marka yoksa ikinci bir ürün ya da konu etiketi: `#din912`, `#inox`.
3. **Kitle ya da meslek:** `#elektrikçi`, `#otoservis`, `#kaynakçı`, `#usta`, `#imalat`, `#atölye`, `#şantiye`, `#talaşlıimalat`.
4. **Kategori:** `#hırdavat`, `#elaletleri`; bağlantı elemanında `#bağlantıelemanları`.
5. **Her zaman** `#tuzlahırdavat`.

`#tuzla`, `#istanbul` gibi genel etiketleri kullanma; site Türkiye'nin her yerine gönderiyor. Her hafta aynı 5'li seti kopyalama.

## Haftalık akış

### 1. Hazırlık
1. `add_repo` ile depoyu push erişimiyle ekle, klonla ve klasöre gir.
2. Ortamı hazırla:
   - `npm ci` ile fontları kur.
   - Python'da jinja2, playwright ve PIL olmalı; eksikse `pip install --break-system-packages` ile kur.
   - `ffmpeg -version` çalışmalı.
   - Chrome `/usr/bin/google-chrome` yolunda olmalı.
3. `state.json` ve `queue.json` dosyalarını oku.

### 2. Hafta ve slotlar
`HAFTA` = gelecek Pazartesi'nin tarihi (YYYY-MM-DD).

- **Önce kaçan kayıtları tamamla:** `python3 planla.py yakala <HAFTA>` çalıştır. Önceden planlanmış bir haftanın Pazar çalışması kaçtıysa, o haftanın durumunu sırayla `state.json` dosyasına işler. Kaydedilecek bir şey yoksa bunu söyler. Bir şey kaydettiyse 8. adımdaki gibi commit et ve push et.
- **Hafta zaten planlıysa:** `planned_weeks` listesinde `HAFTA` varsa yeniden planlama yapma. Kullanıcıya kısa bilgi ver (3. adımdaki karneyi ekleyebilirsin) ve bitir.
- **Hafta önceden planlandıysa:** `weeks/<HAFTA>.json` dosyasında `"on_planli": true` varsa bu bölümdeki diğer adımları uygulama. Aşağıdaki "Önceden planlanmış haftalar" bölümünü uygula ve bitir.
- **Geçen haftayı kontrol et:** `getScheduledPosts` ile son 7 günü sorgula (brandId, Europe/Istanbul). Tarihi geçmiş ama hâlâ planlı görünen gönderi yayınlanmamış demektir; kullanıcıya bildir.
- **Tekli kart haftası mı?** Sabit kurallardaki 42 gün kuralına bak.

### 3. Geçen haftanın karnesi
`getAnalyticsDataByMetrics` ile son 7 günü çek: geçen Pazartesi 00:00'dan bu Pazar 23:59'a, saat dilimi +03:00. Bağlantı türlerini aynı istekte karıştırma; her tür için ayrı istek gönder. Hikaye isteğini yalnız geçen hafta hikaye yayınlandıysa gönder.

| İstek | Ölçümler | Anlamı |
|---|---|---|
| Hesap | `["IGEV01","IGEV43","IGEV44","IGEV06","IGEV42"]` | takipçi, kazanılan, kaybedilen, erişim, etkileşen hesap |
| Gönderiler | `["IGPO02","IGPO06","IGPO07","IGPO14","IGPO15","IGPO27","IGPO29"]` | tarih, bağlantı, tür, erişim, kaydetme, paylaşım, yeni takip |
| Reels | `["IGRE02","IGRE06","IGRE11","IGRE23","IGRE12","IGRE21","IGRE28","IGRE30","IGRE24","IGRE07"]` | tarih, bağlantı, erişim, izlenme, kaydetme, paylaşım, 3 sn üstü izlenme oranı, ilk 3 sn'de geçme oranı, ortalama izlenme süresi (sn), yorum |
| Hikayeler (connector `stories`) | `["IGST02","IGST04","IGST10","IGST09","IGST11","IGST13","IGST08"]` | tarih ve saat, hikaye kimliği, erişim, gösterim, yanıt, ileri dokunma, çıkış |

Sonuçları okurken:

- Satırlar gün gün ve karışık sırada gelir; son sütun tarihtir (YYYYMMDD).
- Takipçi için en son dolu `IGEV01` değerini al; diğer hesap ölçümlerini topla.
- Veri boş gelebilir; Instagram girişiyle bağlıyken bazı ölçümler gelmez. Olanı yaz, olmayanı uydurma.

Ne yapılacak:

- `state.json` içindeki `karne` listesine bir kayıt ekle: `{"hafta": "<geçen Pazartesi>", "takipci": N, "yeni_takipci": N, "erisim": N, "en_iyi": {"id": "...", "erisim": N, "kaydetme": N, "paylasim": N}}`. İlk kayıt başlangıç noktasıdır.
- Geçen hafta hikaye yayınlandıysa kayda `hikayeler` listesini de ekle: `[{"tarih": "...", "erisim": N, "gosterim": N, "yanit": N, "ileri": N, "cikis": N, "reels_erisim": N}]`. `reels_erisim` aynı günün Reels erişimidir.
  - Bu kayıt şart: Ücretsiz plan yalnız son 30 günün verisini gösterir. Deneme sonucu Ocak'ta buradan okunur.
  - Veri boş gelirse boş yaz, uydurma.
- Onay mesajının başına 2–4 satır yaz: takipçi sayısı ve değişimi, erişim, en iyi gönderi ve neden iyi olduğu (kaydetme, paylaşım).
- Bir şey öğrendiysen (örnek: "soru kancalı Reels daha çok izlendi") yeni haftanın metinlerinde uygula.
- Karne kaydındaki her Reels'e türünü (`tur`: `urun`, `bil`, `yd`, `tanitim`), `gecme_orani`, `ort_izlenme` ve `yorum` değerlerini de yaz.
  - Yeni türlerde `kanca_kalibi` ve (Cuma Reels'inde) `cift` değerini de yaz. `python3 fikir.py karne` bunlardan hangi kalıbın tuttuğunu çıkarır (`SENARYO.md`, bölüm 9).
  - Kıyas noktası, Kasım 2026'nın ürün Reels'leri: geçme oranı %73 ve %90, ortalama izlenme 4,3 ve 1,9 saniye.
  - Yeni türlerin ilk 4 haftası dolunca onay mesajının başına türlere göre kısa bir kıyas yaz. Hangi tür daha iyi tutuyorsa kullanıcıya söyle; karar onundur.

### 4. İçerik
1. **Kuyruğu kontrol et:** `reels_bil` ve `reels_yd` listelerinde en az 1'er, `urun_carousel` listesinde en az 1, `ipucu_carousel` listesinde (tekli haftasıysa `tekli` listesinde) en az 1 öğe olmalı.
2. **Eksikse yenisini yaz ve kuyruğa ekle.** Alan yapısı yukarıdaki gibi olur.
   - **"Bil bakalım" ve "Yanlış / doğru" Reels'i:** Önce `SENARYO.md` dosyasını oku; konu seçimi, kanca kalıpları, kurgular ve kontrol listesi orada.
     - `python3 fikir.py sec <HAFTA>` ile fikir dağarcığından aday al. Seçtiğin fikrin iskeletini `python3 fikir.py kuyruk <id>` ile yazdır, "YAZ" alanlarını doldur ve kuyruğa ekle.
     - Alanlar ve teknik sınırlar için "Biçimler ve alanlar" bölümüne bak.
     - Dağarcıkta `dogrulandi` tarihi olan fikir doğrulanmıştır. Olmayanı ve kendi yazdığın her yeni cevabı, güvenlik bilgisini web aramasıyla doğrula.
     - Kullandığın her fikrin yerine dağarcığa en az bir yeni, doğrulanmış fikir ekle (`dagarcik_yaz.py`).
     - Ürün gerekiyorsa `work/products.xml` dosyasında `grep` ile bul ve `fetch_product.py` ile stokta olduğuna bak.
     - Aynı konuyu 8 hafta içinde tekrarlama; İpucu kaydırmalısıyla aynı hafta aynı konuyu işleme.
   - **Ürün kaydırmalısı (ve ürün Reels'i):** `python3 pick_products.py 10` ile aday al, sonra seç:
     - Görseli net, tek ürün, sade zemin olsun. Reels'te ürünün çözdüğü dert soruya dönüşebilmeli.
     - Aynı hafta farklı gruplardan olsun. `recent_groups` içinde son 2 haftada geçen grubu tekrarlama.
     - Haftada en az bir bağlantı elemanı içeriği olsun. İpucu genelde bunu karşılar; karşılamıyorsa ürünlerden biri `baglanti` grubundan olsun.
     - Ürün sayfasını `fetch_product.py` ile oku ve açıklamadaki bilgiler dışında özellik yazma.
     - `weeks/` altındaki herhangi bir haftada (önceden planlananlar ve yedekler dahil) geçen ürünü yeniden seçme. `pick_products.py` bunları zaten atlar.
   - **İpucu:**
     - `ipucu_konulari` listesindeki ilk konuyu al ve 4–6 maddelik kaydırmalı yaz.
     - Her teknik bilgiyi web aramasıyla doğrula.
     - Ürün görseli için sitede uygun ürünü `work/products.xml` dosyasında `grep` ile bul. Dosya yoksa önce `pick_products.py` çalıştır; dosyayı o indirir.
     - Kullandığın konuyu listeden çıkar.
3. **Haftayı kur:** `python3 hafta.py <HAFTA>` (tekli haftasıysa `python3 hafta.py <HAFTA> --tekli`). Betik ürünleri indirir, stok durumunu kontrol eder ve `weeks/<HAFTA>.json` dosyasını yazar.
   - "stokta yok" derse o öğeyi kuyruktan çıkar ya da sona taşı, gerekirse yenisini ekle ve betiği yeniden çalıştır.
   - UYARI satırlarını oku ve gereğini yap.
4. **Ek fragman:** `queue.json` içinde `ek_fragman` listesi boş değilse `python3 ek.py ekle <HAFTA>` çalıştır (Biçimler → Ek fragmanlar). "EKLENMEDİ" derse devam et; o hafta ek video yok.

### 5. Üret ve kontrol et
```
python3 render.py weeks/<HAFTA>.json out/<HAFTA>
python3 reel.py weeks/<HAFTA>.json out/<HAFTA>
python3 onizleme.py weeks/<HAFTA>.json out/<HAFTA>
```
Her önizlemeyi Read ile açıp bak:

- Yazı taşmış ya da kesilmiş mi?
- Görsel boş ya da bozuk mu?
- Türkçe karakterler doğru mu?
- Ürün görseli okunuyor mu?

Sorun varsa metni kısalt ya da görseli değiştir ve yeniden üret.

### 6. Onaya sun
1. **Dosyaları gönder (SendUserFile):**
   - Her Reels için `<id>.mp4`
   - Her kaydırmalı için `<id>-onizleme.png`
   - Tekli kart için `<id>.png`
2. **Tek mesaj gönder (SendUserMessage):**
   - En üstte karne satırları.
   - Sonra her gönderi için gün, saat, biçim ve açıklamanın tamamı. Müzik varsa şarkının adı.
   - Hikaye denemesi haftasındaysa her Reels'in altına şu satırı yaz: "Aynı gün 18:00: bu video hikaye olarak da yayınlanır."
3. **Onay iste:**
   - "Onaylıyor musun? Değiştirmek istediğin varsa numarasını yaz." diye sor.
   - Telefona tek bildirim gönder: «Bu haftanın 4 Instagram gönderisi onayını bekliyor.» (Ek fragman varsa 5 yaz.)
4. **Bekle:** Onay gelene kadar bekle. Kısmi onayda ("1, 2, 4 tamam; 3'ü değiştir") yalnız istenen gönderiyi yeniden üret ve tekrar göster.

### 7. Onay gelince planla
1. **Onay geç geldiyse:** Saati geçmiş bir slotu atlama.
   - O gönderiyi aynı gün 18:00'e al: `--saat <id>=18:00`
   - O saat de geçtiyse haftanın ilk boş gününe, saat 10:00'a kaydır: `--tarih <id>=YYYY-MM-DD`
   - Değişikliği kullanıcıya yaz.
2. **Dosyaları yükle:**
   - `python3 planla.py kopyala <HAFTA>` onaylanan dosyaları `posts/<HAFTA>/` klasörüne kopyalar.
   - `weeks/<HAFTA>.json` ile birlikte commit et (`<HAFTA> haftası gönderileri (onaylandı)`) ve push et.
   - Commit kimliğini al: `SHA=$(git rev-parse HEAD)`
3. **Görsel adreslerini kontrol et:** `curl -sI https://raw.githubusercontent.com/cnbrnc/tuzla-instagram/$SHA/posts/<HAFTA>/<dosya>.png` komutu 200 döndürmeli. jsDelivr bu ortamdan açılmaz; video adreslerini curl ile deneme.
4. **İstekleri hazırla:** `python3 planla.py json <HAFTA> $SHA [--saat …] [--tarih …] [--muzik …] > plan.json`
   - Her gönderi için `id`, `date` ve `info` üretir.
   - Görseller raw.githubusercontent.com'dan, videolar jsDelivr'dan verilir. GitHub videoyu yanlış dosya türüyle sunduğu için videoda jsDelivr kullanılır.
5. **Planla:** `plan.json` içindeki her giriş için `createScheduledPost` çağır: `blogId`, `date` ve `info` (metni olduğu gibi). Yanıttaki `plannerUrl` adreslerini `links.json` dosyasına `{"<id>": "<plannerUrl>"}` biçiminde yaz.
   - Hikaye denemesi haftasında `-hikaye` ile biten 2 giriş daha vardır. Onları da planla; bağlantıları da `links.json` dosyasına aynı biçimde yaz.
6. **Kontrol et:** `getScheduledPosts` ile haftayı listele.
   - 4 gönderi doğru gün ve saatte olmalı (ek fragman varsa 5; o Salı 10:00'da, kapak karesi 4900 ms).
   - Medya sayısı doğru olmalı: Reels'te 1 video, kaydırmalıda slayt sayısı kadar görsel.
   - Deneme haftasında ayrıca 2 hikaye olmalı: tür STORY, saat 18:00, 1 video.
7. **Hata olursa:**
   - Aynı isteği tekrar gönderme.
   - Tek istisna: Bir Reels isteği video adresi yüzünden reddedildiyse ve gönderi oluşmadıysa, `planla.py json … --ham` ile üretilen raw adresiyle bir kez dene.
   - Hikaye isteği reddedilirse gönderiler etkilenmez. Hikayeyi atla ve hatayı kullanıcıya olduğu gibi yaz.
   - Diğer hataları kullanıcıya olduğu gibi yaz.

### 8. Durumu kaydet
1. `python3 planla.py durum <HAFTA> --linkler links.json` çalıştır.
   - `state.json` güncellenir: `posted`, `planned_weeks`, `recent_groups`, `last_product_theme`, `last_tekli_week`.
   - Kullanılan öğeler `queue.json` dosyasından düşülür.
2. 3. adımdaki karne kaydını ekle ve kullandığın `ipucu_konulari` öğesini çıkar.
3. Commit et (`<HAFTA> haftası planlandı`) ve push et. `links.json`, `plan.json` gibi geçici dosyaları depoya ekleme.

### 9. Özet
Kullanıcıya kısa bir özet yaz: hangi gün hangi gönderi (ve varsa hikaye) yayınlanacak ve her birinin Metricool bağlantısı.

## Önceden planlanmış haftalar (30 Kasım 2026 – 1 Ocak 2027)

Kullanıcı Aralık 2026'da askerde. Bu yüzden 5 haftanın 20 gönderisi önceden hazırlandı. Kullanıcı hepsini 6 Kasım 2026'da onayladı ve hepsi aynı gün Metricool'a planlandı (her biri 10:00'da).

- **Dosyalar:**
  - `weeks/2026-11-30.json` … `weeks/2026-12-28.json`: Her dosyada `"on_planli": true` var. Her gönderinin `metricool` alanında `uuid` ve Metricool bağlantısı durur.
  - Görseller ve videolar `posts/<HAFTA>/` klasöründe.
  - Onaylı 2 yedek: `weeks/yedek.json`, görselleri `posts/yedek/`. Sıra: önce `yedek-metrik-inc`, sonra `yedek-matkap-ucu`. Kullanılanlar `state.json` içindeki `kullanilan_yedekler` listesine yazılır.
- **Bu haftalarda yapma:**
  - Onay isteme.
  - Telefon bildirimi gönderme.
  - Yeni gönderi üretme.
  - `hafta.py`, `render.py` ve `reel.py` çalıştırma. `hafta.py` bu haftalarda zaten durur.

| Pazar çalışması | HAFTA | Not |
|---|---|---|
| 29 Kasım | 2026-11-30 | |
| 6 Aralık | 2026-12-07 | |
| 13 Aralık | 2026-12-14 | |
| 20 Aralık | 2026-12-21 | 24 Aralık kampanya kartı: eşikler de denetlenir |
| 27 Aralık | 2026-12-28 | |
| 3 Ocak 2027 | 2027-01-04 | Normal düzen geri döner ve onay yine şarttır. Reels'ler yeni türlerdedir: Pazartesi "Bil bakalım", Cuma "Yanlış / doğru"; ilk öğeler kuyrukta hazır. Kaydırmalı listeleri boşalmış olur; 4. adımdaki kurallarla yeni öğe yaz. **Ocak'ta onaylı ve planlı iki ek gönderi zaten var (25 Kasım 2026'da planlandı; `state.json` `posted` içinde; `getScheduledPosts` çıktısında görünür, dokunma): 5 Ocak Salı 10:00 site tanıtım filmi (15 sn) ve 19 Ocak Salı 10:00 A4-316 tanıtım filmi (L400 ve SİHA'lı, 15 sn).** Bunlarla Ocak 19 gönderiye ulaşır; `ek.py` Ocak'ta başka ek video eklemez. Sıradaki ekler (Rayno'nun ikinci reklam filmi, sonra dört fragman) Şubat'tan itibaren çıkar. Reels türü Aralık'ta zaten değişti; onay mesajında Aralık Reels'lerinin karne özetini (geçme oranı, ortalama izlenme) yaz. Mesajın başına hikaye denemesinin sonucunu da yaz (Biçimler → Hikaye denemesi). |

### Aralık Reels'leri yeni biçimde (23 Kasım 2026'da onaylandı ve uygulandı)

Kullanıcı 23 Kasım 2026'da Aralık'ın 10 ürün Reels'inin yeni türlere çevrilmesini istedi, videoları sohbette izledi ve onayladı. Aynı gün 10 gönderi Metricool'da güncellendi.

- **Düzen:** Pazartesi Reels'i "Bil bakalım", Cuma Reels'i "Yanlış / doğru". Hepsi sinematik stilde, profesyonel sesle; kapanış kartında ürünün fotoğrafı ve adı var. Tarih, saat, `uuid`, ürün ve aranacak kod aynı kaldı.
- **Dosyalar:** `weeks/2026-11-30.json` … `weeks/2026-12-28.json` içindeki Reels öğeleri yeni türde; `metricool.guncellendi` ve `metricool.son_id` alanları eklendi. Videolar `posts/<HAFTA>/` klasöründe eski adlarıyla duruyor.
- **İçerik kaynağı:** `taslak/aralik-yeni/yap.py`. Yeniden üretmek gerekirse: `python3 taslak/aralik-yeni/yap.py --indir`, `python3 taslak/aralik-yeni/yap.py`, `python3 reel.py taslak/aralik-yeni/aralik-yeni.json out/aralik-yeni`.
- **Pazar çalışması:** Aşağıdaki adımlar aynen geçerli. Stok denetimi her Reels'in `url` alanındaki ürüne bakar. Yedekle değiştirme kuralı da aynıdır.
- **Karne:** Bu haftaların Reels'lerinde `tur` alanına `bil` ya da `yd` yaz; 4 Ocak'tan sonraki haftalarla karşılaştırılabilsin.

### 23 Kasım 2026 akşamı yapılan ekler (kullanıcı: "Oyun temalı onaylı, kalanı hangisi iyi olacaksa onu yap")

- **Sesler değişti:** Kullanıcı "hep aynı melodi" dedi. 10 Reels'in sesi farklı parçalarla değiştirildi ve Metricool'da güncellendi; görüntü, açıklama, tarih ve `uuid` aynı. Her öğenin `muzik` alanı yeni parçayı, `metricool.son_id` yeni Metricool kimliğini gösterir. Sıra: helikoil `a`, ısıtıcı `e`, somun sıkma `f`, sıcak hava `g`, boru kaynak `d`, dekupaj `h`, panç `b`, caraskal `i`, fener `j`, lazer metre `c`.
- **1 Aralık Salı 10:00, ek gönderi:** Paslanmaz DIN 933 A2 cıvata fragmanı (`weeks/2026-11-30.json` içinde `"ek": true`). Bu yüzden 30 Kasım haftasında 5 gönderi var ve Aralık'ın toplamı 19. Stok denetimi ve yedekle değiştirme kuralı bu gönderi için de geçerli.
- **24 Kasım Salı 10:00:** Oyun temalı "Usta Modu" site tanıtımı. **28 Kasım Cumartesi 10:00:** Rayno 200A kaynak makinesi, fragman sürümü. İkisi de `weeks/2026-11-23.json` içinde `"ek": true`; Kasım'ın toplamı 19.
- **Aralık'ta başka gönderi ekleme.** İki ay da sınırda.

### Adımlar
1. **Karne:** 3. adımdaki karneyi çıkar ve `state.json` dosyasına ekle.
2. **Geçen hafta:** Geçen haftayı 2. adımdaki gibi kontrol et.
   - Yayınlanmamış gönderi varsa `state.json` içindeki `notes` listesine yaz ve özette belirt.
   - O gönderiyi yeniden planlama.
3. **Denetle:** `python3 planla.py stok <HAFTA>` çalıştır.
   - Ürünlü her gönderinin sayfası stokta mı diye bakılır.
   - Kampanya kartı varsa sitede şu eşikler hâlâ aynı mı diye bakılır: 3.000 TL üstü ücretsiz kargo, 5.000 TL üstü 3 taksit, 20.000 TL üstü 6 taksit. Bunlar 6 Kasım 2026'da doğrulandı.
   - Çıkış kodu 0 ise sorun yoktur; 5. adıma geç.
   - **DENETLENEMEDİ** satırı çıkarsa komutu bir kez daha çalıştır. Yine çıkarsa o ürünün sayfasını WebFetch ile aç:
     - Ürün kaldırılmışsa ya da tükendiyse SORUNLU say.
     - Sayfa hiç açılmıyorsa gönderiye dokunma ve özette yaz.
4. **Yedekle değiştir:** **SORUNLU** her gönderi için sırayla şunları yap:
   1. `SHA=$(git rev-parse HEAD)`, sonra `python3 planla.py yedek <HAFTA> <id> $SHA > yedek-istek.json`.
      - Çıktıda şunlar olur: `yedek` (anahtar), `date`, `uuid` (değişecek gönderinin) ve `info`.
      - "kullanılmamış yedek kalmadı" derse gönderiye dokunma. `notes` listesine yaz ve özette belirt.
   2. Yedeğin ilk görselini kontrol et: `curl -sI <info içindeki ilk media adresi>` 200 döndürmeli.
   3. Gönderinin güncel `id` değerini bul. `getScheduledPosts` ile o günü listele (brandId, 00:00–23:59, Europe/Istanbul). `uuid` değeri eşleşen gönderinin `id`'sini al.
      - Güncellemede `id` değişir, `uuid` değişmez.
      - Gönderi bulunamazsa ya da artık PENDING değilse dokunma ve yaz.
   4. `updateScheduledPost` çağır: blogId, `id`, `uuid` ve `info` (metni olduğu gibi).
   5. `getScheduledPosts` ile doğrula: aynı gün 10:00, tür POST, 6 görsel ve yedeğin metni.
   6. Başarılıysa `python3 planla.py yedek <HAFTA> <id> --uygula <yedek> --neden "<kısa neden>"` çalıştır.
   7. Hata olursa aynı isteği tekrarlama. Gönderiyi olduğu gibi bırak ve `notes` listesine yaz.
   - Kampanya kartını yeniden çizme ve eşikleri kendin değiştirme. Eşik bilgisi kullanıcı onayı ister. Eşikler değiştiyse kart da yedekle değiştirilir.
5. **Kaydet:** `python3 planla.py durum <HAFTA>` çalıştır. Metricool bağlantıları haftanın dosyasından okunur.
6. **Commit et ve push et:** Mesaj `<HAFTA> önceden planlı hafta: denetlendi` olsun. `yedek-istek.json` gibi geçici dosyaları ekleme.
7. **Özet:** Kısa yaz:
   - haftanın gönderileri (gün ve konu; 30 Kasım haftasında 5 tane),
   - denetimin sonucu,
   - yapılan değişiklik varsa o,
   - karne satırları.
   - Bildirim gönderme.

## Facebook bağlantısı varsa (`state.json` içinde `facebook_bagli: true`)

- **Reels müziği:** Haftanın iki Reels'inden birine Instagram müziği ekle, diğeri kendi sesimizle kalsın. Karnede hangisinin daha çok izlendiğini ve paylaşıldığını takip et; birkaç hafta sonra sonucu kullanıcıya öner.
  - Müzik eklenecek Reels'e `weeks/<HAFTA>.json` dosyasında üretimden önce `"ses": "efekt"` yaz. Böylece ritim müzikle çakışmaz.
  - Müziği `planla.py json … --muzik <id>=<audioId>` ile ekle. Videonun efektleri müziğin altında kalır (`videoVolume` 50).
  - Müzik yalnız Reels'te olur ve her zaman videonun başından başlar.
  - "Bil bakalım" ve "Yanlış / doğru" Reels'ine müzik ekleme: geri sayım ve damga sesleri kurgunun parçasıdır. Müzik denemesi yalnız ürün Reels'inde yapılır.
  - `audioId` bir arama terimi (şarkı ya da sanatçı adı) veya bir numaradır.
  - Arama tek sonuca denk gelmezse Metricool isteği aday listesiyle reddeder. O zaman listeden **sözsüz (enstrümantal)** bir parça seç ve numarasıyla bir kez daha dene.
  - Sözlü, argo içeren ya da marka adı geçen parça seçme.
  - Onay mesajında şarkının adını yaz.
  - İstek bağlantı türü yüzünden reddedilirse müziksiz planla, `facebook_bagli` değerini `false` yap ve kullanıcıya bildir.
- **En iyi saat:** Ayda bir `getBestTimeToPostByNetwork` (instagram) çağır. 10:00'dan belirgin biçimde daha iyi bir saat çıkarsa kullanıcıya öner; kendin değiştirme.

## Düzeltme istekleri
- **Bir gönderi değişecekse:** Sadece onu yeniden üret ve tekrar göster.
- **"Bu haftayı atla" denirse:** Hiçbir şey planlama; `state.json` içindeki `notes` listesine not düş.
- **Kullanıcı bir ürünü ya da konuyu istemezse:** Kuyruktan çıkar.

## Dosyalar
- `hafta.py`: Kuyruktan haftayı kurar, ürünleri indirir, stok kontrol eder.
- `render.py`: Kaydırmalı ve tekli gönderilerin PNG'lerini üretir (1080×1350).
- `reel.py`: Reels videosunu ve kapağını üretir (altı tür: `reel`, `reel_bil`, `reel_yd`, `reel_tanitim`, `reel_fragman`, `reel_oyun`); sesi `assets/reel-ses-*.wav` dosyalarından ekler.
- `ses.py`: Ürün Reels'inin özgün ses izini üretir. `ses_tur.py`: "Bil bakalım" ve "Yanlış / doğru" seslerini üretir. Yalnız animasyon zamanları değişirse çalıştırılırlar.
- `SENARYO.md`: Senaryo rehberi (konu bulma, kanca kalıpları, kurgular, yazım kuralları, kontrol listesi).
- `dagarcik.json`: Fikir dağarcığı; kaynağı `dagarcik_yaz.py`. `fikir.py`: dağarcıktan aday seçer, kuyruk iskeleti yazar, karneden kalıp kıyası çıkarır.
- `ses_pro.py`: Sinematik Reels'in profesyonel sesini üretir (stok müzik ve efekt); kaynak listesi `assets/ses-kaynak.json`. `reel.py` kendisi çağırır.
- `muzik_olc.py`: Yeni müziğin temposunu ve başlangıç anını ölçer. `ses_degistir.py`: Üretilmiş videonun yalnız sesini değiştirir.
- `ek.py`: Onaylı, bitmiş ek videoları (`ek_fragman`) haftaya ekler; ayın sayımını gösterir.
- `taslak/`: Onay bekleyen taslakların içeriği (yalnız metin ve betik; video konmaz).
- `onizleme.py`: Onay için önizlemeleri üretir; bunlar depoya yüklenmez.
- `planla.py`: Dosyaları kopyalar, Metricool isteklerini hazırlar, durumu kaydeder.
  - Önceden planlanmış haftalar için `stok`, `yedek` ve `yakala` komutları da onda.
- `fetch_product.py`, `pick_products.py`, `tools_svg.py`: Ürün verisi, ürün adayları, cıvata çizimleri.
- `templates/`: `urun`, `slide_liste`, `slide_kapak`, `slide_madde`, `slide_cta`, `reel`, `reel_taban`, `reel_bil`, `reel_yd`, `reel_tanitim`, `reel_fragman`, `reel_oyun`, `kampanya`, `toplu`, `bilgi`, `karsilastirma`.
- `queue.json`: İçerik kuyruğu. `state.json`: Geçmiş, karne ve ayarlar.
- `weeks/`: Haftalık gönderi tanımları. `weeks/yedek.json`: Önceden planlanmış haftaların onaylı yedekleri.
- `posts/`: Onaylanmış dosyalar. `posts/ek/`: sırasını bekleyen onaylı ek fragmanlar.
