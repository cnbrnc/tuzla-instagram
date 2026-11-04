# Tuzla Hırdavat Instagram Robotu: Haftalık Talimat

Bu dosya, her Pazar akşamı çalışan zamanlanmış görevin izlediği adımlardır.
Depo herkese açıktır; buraya şifre, anahtar veya kişisel bilgi yazılmaz.

## Sabit kurallar

- **Hesap:** Instagram @tuzla_civata_hirdavat, Metricool üzerinden yayınlanır. Metricool marka kimliği görev mesajında verilir.
- **Takvim:** Haftada 4 gönderi, hepsi saat **10:00** (Europe/Istanbul).
  - Pazartesi: ürün
  - Çarşamba: ürün
  - Perşembe: ürün dışı kart
  - Cuma: ürün
- **Fiyat yok:** Ne görselde ne açıklamada ürün fiyatı yazılır. Tek istisna, kampanya kartında sitede yazan kargo ve taksit eşikleridir.
- **İletişim:** Sipariş için satis5@tuzlacivata.com.tr, telefon 0542 189 02 69, site tuzlahirdavat.com.tr.
- **Onay şart:** Kullanıcı onay vermeden hiçbir gönderi Metricool'a planlanmaz.
- **Metricool sınırı:** Ücretsiz planda ayda en fazla 20 planlı gönderi var. Planlamadan önce `getScheduledPosts` ile o ayın toplamına bak; aşılacaksa kullanıcıya söyle.

## Haftalık akış

### 1. Hazırlık
1. `add_repo` ile bu depoyu push erişimiyle ekle, klonla, klasöre gir.
2. `npm ci` ile fontları kur. Python'da jinja2, playwright ve PIL; Chrome `/usr/bin/google-chrome` olmalı.
3. `state.json` ve `queue.json` dosyalarını oku.

### 2. Hafta ve slotlar
`HAFTA` = gelecek Pazartesi'nin tarihi (YYYY-MM-DD). Slotlar: Pzt ürün, Çar ürün, Per ürün dışı, Cum ürün; hepsi 10:00.

- **Hafta zaten planlıysa:** `state.json` içindeki `planned_weeks` listesinde `HAFTA` varsa yeniden planlama yapma. Kullanıcıya "bu hafta zaten planlı" diye kısa bilgi ver ve bitir.
- **Geçen haftayı kontrol et:** `getScheduledPosts` ile son 7 günü sorgula. Tarihi geçmiş ama hâlâ planlı görünen gönderi varsa yayınlanmamış demektir; kullanıcıya bildir.

### 3. İçerik seçimi
- **Ürün slotları:** Önce `queue.json` içindeki `products` listesini sırayla kullan. Liste bittiyse `python3 pick_products.py 8` çalıştır ve adaylardan 3 ürün seç:
  - Aynı hafta içinde farklı gruplardan olsun.
  - İki haftada en az bir bağlantı elemanı (cıvata, somun, pul; grup `baglanti`) olsun.
  - Görseli net olanları seç; benzer ürünü art arda koyma.
- **Ürün dışı slot:** Önce `queue.json` içindeki `extras` listesini sırayla kullan. Bittiyse `state.json` içindeki `extras_cycle` sırasıyla yeni içerik üret:
  - `bilgi`: Teknik bilgi kartı (cıvata, kılavuz, kaynak, iş güvenliği konuları). Doğruluğundan emin olmadığın bilgiyi yazma.
  - `karsilastirma`: İki seçenek, 4 satır.
  - `kampanya`: Sadece sitede o an yazan kampanyalar. Siteyi kontrol et; kampanya yoksa bu türü atla.
  - `toplu`: Toplu alım ve ithalatçı kartı, en fazla 8 haftada bir.

### 4. Ürün verisi
Her ürün için `python3 fetch_product.py <ürün_url> work/<anahtar>` çalıştır. `product.json` içinde ad, marka, açıklama, stok durumu ve görsel olur. Ürün stokta değilse başka ürün seç.

### 5. Metinler
Tümü Türkçe olur. Sadece ürün sayfasındaki bilgilere dayan; özellik, sertifika, garanti, stok adedi uydurma.

**Görsel üzerindeki metinler:**
- **Başlık:** 2 satır, her satır en fazla 18 karakter. Kısa ve somut bir fayda söyle, ünlem kullanma.
- **Alt satır:** Ürün adının kısaltılmışı, en fazla 48 karakter.
- **Çipler:** 3 adet, her biri en fazla 22 karakter, teknik bilgi.
- **Sağ üst etiket:** Sitede "Yeni Ürün" ise `YENİ ÜRÜN`, değilse kategori adı büyük harfle.
- **Marka ve kod:** Marka büyük harfle yazılır; marka "DİĞER" ise ürün tipini yaz (örn. `PASLANMAZ CIVATA`). Sağa model kodunu yaz.

**Açıklama sırası:**
1. Kanca cümlesi ve bir emoji
2. 1–2 cümle fayda
3. 3–4 adet "✅" madde
4. `🔎 Sitede “<model kodu>” yazıp aratın` (kod yoksa ürün adından 2–3 kelime)
5. `🛒 tuzlahirdavat.com.tr`
6. `✉️ Sipariş: satis5@tuzlacivata.com.tr`
7. `📞 0542 189 02 69`
8. 10–12 hashtag: #hırdavat #tuzlahırdavat #tuzla #istanbul ve ürüne özel olanlar

### 6. Tema
Ürün gönderilerinde açık (`light`) ve koyu (`dark`) sırayla gider. `state.json` içindeki `last_product_theme` değerinin tersiyle başla. Ürün dışı kartların kendi teması vardır (`queue.json` içinde yazar).

### 7. Görselleri üret
1. `weeks/<HAFTA>.json` dosyasını yaz; örnek için `weeks/2026-11-09.json` dosyasına bak.
2. `python3 render.py weeks/<HAFTA>.json out/<HAFTA>` çalıştır.
3. Her PNG'yi açıp bak: yazı taşması, boş görsel, bozuk Türkçe karakter olmasın.

### 8. Onaya sun
1. 4 PNG'yi SendUserFile ile gönder.
2. Mesajda her gönderinin gününü, saatini ve açıklamasını yaz.
3. "Onaylıyor musun? Değiştirmek istediğin varsa numarasını yaz." diye sor ve bildirim gönder.
4. Onay gelene kadar bekle.

### 9. Onay gelince planla
1. PNG'leri `posts/<HAFTA>/` klasörüne kopyala, commit et (`<HAFTA> haftası gönderileri`) ve push et.
2. Her görselin adresi `https://raw.githubusercontent.com/<sahip>/tuzla-instagram/main/posts/<HAFTA>/<id>.png` olur. `curl` ile 200 döndüğünü kontrol et.
3. Her gönderi için Metricool `createScheduledPost` çağır:
   - `blogId`: marka kimliği
   - `date`: `YYYY-MM-DDT10:00:00+03:00`
   - `info` (JSON metni):
     ```json
     {"autoPublish": true, "draft": false, "text": "<açıklama>", "media": ["<görsel adresi>"],
      "mediaAltText": ["<kısa görsel açıklaması>"], "providers": [{"network": "instagram"}],
      "publicationDate": {"dateTime": "YYYY-MM-DDT10:00:00", "timezone": "Europe/Istanbul"},
      "instagramData": {"type": "POST"}, "firstCommentText": "", "shortener": false,
      "smartLinkData": {"ids": []}, "descendants": [], "hasNotReadNotes": false}
     ```
4. Hata gelirse aynı isteği tekrar deneme; hatayı kullanıcıya olduğu gibi bildir.

### 10. Durumu kaydet
1. `state.json`'a şunları işle: 4 kayıt (tarih, id, tür, url, grup, Metricool bağlantısı), `planned_weeks` listesine `HAFTA`, `recent_groups`, `last_product_theme`, `extras_used`.
2. Kullanılan öğeleri `queue.json`'dan çıkar.
3. Commit et ve push et.

### 11. Özet
Kullanıcıya kısa bir özet yaz: hangi gün hangi gönderi yayınlanacak.

## Düzeltme istekleri
- **Bir gönderi değişecekse:** Sadece onu yeniden üret ve tekrar göster.
- **"Bu haftayı atla" denirse:** Hiçbir şey planlama; `state.json`'a not düş.
