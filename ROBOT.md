# Tuzla Hırdavat Instagram Robotu: Haftalık Talimat

Bu dosya, her Pazar 18:55'te (Türkiye saati) çalışan zamanlanmış görevin izlediği adımlardır.
16 Kasım 2026 haftasından itibaren geçerli düzen budur: Reels ve kaydırmalı gönderiler.
Depo herkese açıktır; buraya şifre, anahtar veya kişisel bilgi yazılmaz.

## Sabit kurallar

- **Amaç:** tuzlahirdavat.com.tr'yi yaymak.
  - Reels, takip etmeyenlere ulaşır.
  - Kaydırmalı gönderiler kaydedilir ve paylaşılır.
  - Her gönderi, sitede aranacak bir kodla siteye yönlendirir.
- **Hesap:** Instagram @tuzla_civata_hirdavat, Metricool üzerinden yayınlanır. Metricool marka kimliği görev mesajında verilir.
- **Takvim:** Haftada 4 gönderi, hepsi saat **10:00** (Europe/Istanbul).

  | Gün | Biçim | Kuyruk listesi |
  |---|---|---|
  | Pazartesi | Ürün Reels'i (10 sn video) | `reels` |
  | Çarşamba | Ürün kaydırmalısı (3 slayt) | `urun_carousel` |
  | Perşembe | Usta İpucu kaydırmalısı (5–8 slayt) | `ipucu_carousel` |
  | Cuma | Ürün Reels'i | `reels` |

- **Tekli kart haftası:** HAFTA, `state.json` içindeki `last_tekli_week` tarihinden en az 42 gün sonraysa Perşembe günü İpucu yerine `tekli` listesindeki ilk kart kullanılır (`hafta.py --tekli`). Kampanya kartını kullanmadan önce eşiklerin sitede hâlâ aynı yazdığını kontrol et; değiştiyse görseli ve açıklamayı güncelle, kampanya kalktıysa kartı atla.
- **Fiyat yok:** Ne görselde ne açıklamada ürün fiyatı yazılır. Tek istisna, kampanya kartında sitede yazan kargo ve taksit eşikleridir.
- **İletişim:** Sipariş için satis5@tuzlacivata.com.tr, telefon 0542 189 02 69, site tuzlahirdavat.com.tr.
- **Onay şart:** Kullanıcı onay vermeden hiçbir gönderi Metricool'a planlanmaz ve hiçbir görsel ya da video depoya yüklenmez.
- **Metricool sınırı:** Ücretsiz planda ayda en fazla 20 planlı gönderi var. `state.json` içinde o aya düşen gönderiler ile yeni gönderilerin toplamı 20'yi geçecekse kullanıcıya söyle.
- **Doğruluk:**
  - Ürün bilgisi yalnız ürün sayfasından alınır.
  - İpucu içeriklerinde her teknik bilgiyi (ölçü, standart numarası, değer) en az bir güvenilir kaynakla doğrula: standart kuruluşu, üretici kataloğu ya da teknik başvuru kaynağı. Emin olmadığın bilgiyi yazma.
- **Düzen değişikliği:** Haftalık düzeni, saati ya da biçimleri kendi başına değiştirme. Karneye göre ayda en fazla bir kez öneri yapabilirsin; karar kullanıcınındır.

## Biçimler ve alanlar

`queue.json` içindeki öğeler bu alanlarla yazılır. Yeni öğe eklerken oradaki örnekleri kopyala.

### Reels (`reel.py`, şablon `templates/reel.html`)

1080×1920, 10 saniye, 30 fps.

- **0–2 sn:** Kanca sorusu.
- **2–7 sn:** Ürün paneli, başlık ve 3 çip.
- **7–10 sn:** "Sitede arat" kapanış kartı.
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

**Ses:** Her Reels'e kodla üretilmiş özgün ses gömülür. `reel.py` bunu kendisi yapar; kullanıcı bu sesi 5 Kasım 2026'da onayladı.
- Sesin içinde kanca tıkları, geçiş "vuuş"ları, çip "pıt"ları, kapanışta metal "tınn" ve hafif bir ritim var. Telif sorunu yoktur.
- Dosyalar `assets/reel-ses.wav` (tam) ve `assets/reel-ses-efekt.wav` (yalnız efekt), kaynağı `ses.py`.
- Gönderide `ses` alanı:
  - `"tam"` (varsayılan)
  - `"efekt"`: Instagram müziği eklenecekse
  - `"yok"`: sessiz
- `reel.html` içindeki animasyon zamanları değişirse `ses.py` içindeki zamanları da güncelle ve iki dosyayı yeniden üret.

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

- **Hafta zaten planlıysa:** `planned_weeks` listesinde `HAFTA` varsa yeniden planlama yapma. Kullanıcıya kısa bilgi ver (3. adımdaki karneyi ekleyebilirsin) ve bitir.
- **Geçen haftayı kontrol et:** `getScheduledPosts` ile son 7 günü sorgula (brandId, Europe/Istanbul). Tarihi geçmiş ama hâlâ planlı görünen gönderi yayınlanmamış demektir; kullanıcıya bildir.
- **Tekli kart haftası mı?** Sabit kurallardaki 42 gün kuralına bak.

### 3. Geçen haftanın karnesi
`getAnalyticsDataByMetrics` ile son 7 günü çek: geçen Pazartesi 00:00'dan bu Pazar 23:59'a, saat dilimi +03:00. Bağlantı türlerini aynı istekte karıştırma; üç ayrı istek gönder:

| İstek | Ölçümler | Anlamı |
|---|---|---|
| Hesap | `["IGEV01","IGEV43","IGEV44","IGEV06","IGEV42"]` | takipçi, kazanılan, kaybedilen, erişim, etkileşen hesap |
| Gönderiler | `["IGPO02","IGPO06","IGPO07","IGPO14","IGPO15","IGPO27","IGPO29"]` | tarih, bağlantı, tür, erişim, kaydetme, paylaşım, yeni takip |
| Reels | `["IGRE02","IGRE06","IGRE11","IGRE23","IGRE12","IGRE21","IGRE28"]` | tarih, bağlantı, erişim, izlenme, kaydetme, paylaşım, 3 sn üstü izlenme oranı |

Sonuçları okurken:

- Satırlar gün gün ve karışık sırada gelir; son sütun tarihtir (YYYYMMDD).
- Takipçi için en son dolu `IGEV01` değerini al; diğer hesap ölçümlerini topla.
- Veri boş gelebilir; Instagram girişiyle bağlıyken bazı ölçümler gelmez. Olanı yaz, olmayanı uydurma.

Ne yapılacak:

- `state.json` içindeki `karne` listesine bir kayıt ekle: `{"hafta": "<geçen Pazartesi>", "takipci": N, "yeni_takipci": N, "erisim": N, "en_iyi": {"id": "...", "erisim": N, "kaydetme": N, "paylasim": N}}`. İlk kayıt başlangıç noktasıdır.
- Onay mesajının başına 2–4 satır yaz: takipçi sayısı ve değişimi, erişim, en iyi gönderi ve neden iyi olduğu (kaydetme, paylaşım).
- Bir şey öğrendiysen (örnek: "soru kancalı Reels daha çok izlendi") yeni haftanın metinlerinde uygula.

### 4. İçerik
1. **Kuyruğu kontrol et:** `reels` listesinde en az 2, `urun_carousel` listesinde en az 1, `ipucu_carousel` listesinde (tekli haftasıysa `tekli` listesinde) en az 1 öğe olmalı.
2. **Eksikse yenisini yaz ve kuyruğa ekle.** Alan yapısı yukarıdaki gibi olur.
   - **Reels ve ürün kaydırmalısı:** `python3 pick_products.py 10` ile aday al, sonra seç:
     - Görseli net, tek ürün, sade zemin olsun. Reels'te ürünün çözdüğü dert soruya dönüşebilmeli.
     - Aynı hafta farklı gruplardan olsun. `recent_groups` içinde son 2 haftada geçen grubu tekrarlama.
     - Haftada en az bir bağlantı elemanı içeriği olsun. İpucu genelde bunu karşılar; karşılamıyorsa ürünlerden biri `baglanti` grubundan olsun.
     - Ürün sayfasını `fetch_product.py` ile oku ve açıklamadaki bilgiler dışında özellik yazma.
   - **İpucu:**
     - `ipucu_konulari` listesindeki ilk konuyu al ve 4–6 maddelik kaydırmalı yaz.
     - Her teknik bilgiyi web aramasıyla doğrula.
     - Ürün görseli için sitede uygun ürünü `work/products.xml` dosyasında `grep` ile bul. Dosya yoksa önce `pick_products.py` çalıştır; dosyayı o indirir.
     - Kullandığın konuyu listeden çıkar.
3. **Haftayı kur:** `python3 hafta.py <HAFTA>` (tekli haftasıysa `python3 hafta.py <HAFTA> --tekli`). Betik ürünleri indirir, stok durumunu kontrol eder ve `weeks/<HAFTA>.json` dosyasını yazar.
   - "stokta yok" derse o öğeyi kuyruktan çıkar ya da sona taşı, gerekirse yenisini ekle ve betiği yeniden çalıştır.
   - UYARI satırlarını oku ve gereğini yap.

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
3. **Onay iste:**
   - "Onaylıyor musun? Değiştirmek istediğin varsa numarasını yaz." diye sor.
   - Telefona tek bildirim gönder: «Bu haftanın 4 Instagram gönderisi onayını bekliyor.»
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
5. **Planla:** Her gönderi için `createScheduledPost` çağır: `blogId`, `date` ve `info` (metni olduğu gibi). Yanıttaki `plannerUrl` adreslerini `links.json` dosyasına `{"<id>": "<plannerUrl>"}` biçiminde yaz.
6. **Kontrol et:** `getScheduledPosts` ile haftayı listele. 4 gönderi doğru gün ve saatte olmalı, medya sayısı doğru olmalı: Reels'te 1 video, kaydırmalıda slayt sayısı kadar görsel.
7. **Hata olursa:**
   - Aynı isteği tekrar gönderme.
   - Tek istisna: Bir Reels isteği video adresi yüzünden reddedildiyse ve gönderi oluşmadıysa, `planla.py json … --ham` ile üretilen raw adresiyle bir kez dene.
   - Diğer hataları kullanıcıya olduğu gibi yaz.

### 8. Durumu kaydet
1. `python3 planla.py durum <HAFTA> --linkler links.json` çalıştır.
   - `state.json` güncellenir: `posted`, `planned_weeks`, `recent_groups`, `last_product_theme`, `last_tekli_week`.
   - Kullanılan öğeler `queue.json` dosyasından düşülür.
2. 3. adımdaki karne kaydını ekle ve kullandığın `ipucu_konulari` öğesini çıkar.
3. Commit et (`<HAFTA> haftası planlandı`) ve push et. `links.json`, `plan.json` gibi geçici dosyaları depoya ekleme.

### 9. Özet
Kullanıcıya kısa bir özet yaz: hangi gün hangi gönderi yayınlanacak ve her birinin Metricool bağlantısı.

## Facebook bağlantısı varsa (`state.json` içinde `facebook_bagli: true`)

- **Reels müziği:** Haftanın iki Reels'inden birine Instagram müziği ekle, diğeri kendi sesimizle kalsın. Karnede hangisinin daha çok izlendiğini ve paylaşıldığını takip et; birkaç hafta sonra sonucu kullanıcıya öner.
  - Müzik eklenecek Reels'e `weeks/<HAFTA>.json` dosyasında üretimden önce `"ses": "efekt"` yaz. Böylece ritim müzikle çakışmaz.
  - Müziği `planla.py json … --muzik <id>=<audioId>` ile ekle. Videonun efektleri müziğin altında kalır (`videoVolume` 50).
  - Müzik yalnız Reels'te olur ve her zaman videonun başından başlar.
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
- `reel.py`: Reels videosunu ve kapağını üretir; sesi `assets/reel-ses*.wav` dosyalarından ekler.
- `ses.py`: Reels'in özgün ses izini üretir. Yalnız animasyon zamanları değişirse çalıştırılır.
- `onizleme.py`: Onay için önizlemeleri üretir; bunlar depoya yüklenmez.
- `planla.py`: Dosyaları kopyalar, Metricool isteklerini hazırlar, durumu kaydeder.
- `fetch_product.py`, `pick_products.py`, `tools_svg.py`: Ürün verisi, ürün adayları, cıvata çizimleri.
- `templates/`: `urun`, `slide_liste`, `slide_kapak`, `slide_madde`, `slide_cta`, `reel`, `kampanya`, `toplu`, `bilgi`, `karsilastirma`.
- `queue.json`: İçerik kuyruğu. `state.json`: Geçmiş, karne ve ayarlar.
- `weeks/`: Haftalık gönderi tanımları. `posts/`: Onaylanmış dosyalar.
