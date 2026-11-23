# Senaryo Rehberi

Bu dosya Reels ve İpucu konularının nasıl bulunacağını ve nasıl yazılacağını anlatır. Alan yapıları ve teknik kurallar `ROBOT.md` dosyasındadır; burada içerik ve kurgu vardır.

**Amaç (kullanıcının sözü, 23 Kasım 2026):** Yayılmak, izlenmek, ürünü tanıtmak, yeri geldiğinde bilgi vermek ve sayfayı popüler hale getirmek.

**Kullanıcının isteği (23 Kasım 2026):** Robot gelecek paylaşımlar için fikir dağarcığını ve senaryo yazma becerisini geliştirsin. Bu dosya, `dagarcik.json` ve `fikir.py` bunun için kuruldu.

## 1. Bir senaryonun dört parçası

Her Reels 9 saniyedir ve tek bir fikir taşır.

| Parça | Süre | Görevi |
|---|---|---|
| Kanca | 0–1,5 sn | İzleyeni durdurur. Bir soru ya da "bunu sen de yapıyorsun" iması. |
| Gerilim | 1,5–4 sn | Cevabı bekletir: geri sayım ya da ilk panel. |
| Çözüm | 4–6,75 sn | Cevap ve tek cümlelik nedeni. |
| Ürün | 6,75–9 sn | Kapanış kartı: aranacak kod, ürünün fotoğrafı ve adı. |

- **Tek fikir:** Bir videoda bir soru ya da bir hata olur. İkinci bilgi açıklamaya ya da başka videoya gider.
- **Ürün bağı:** Soru ya da hata, tanıtılan ürünün işiyle ilgili olur. Bağ kurulamıyorsa o videoda ürün gösterme.

## 2. Kanca kalıpları

Her öğeye `kanca_kalibi` alanı yazılır. Karne bu alana göre hangi kalıbın tuttuğunu ölçer (bölüm 9).

| Kalıp | Biçim | Örnek | Ne zaman |
|---|---|---|---|
| `dert` | "…oluyor mu?" | "Elektrot yapışıp duruyor mu?" | Ustanın yaşadığı bir dert varsa ve ürün onu çözüyorsa |
| `ima` | "…mı yapıyorsun?" | "Paslanmazı darbeliyle mi sıkıyorsun?" | Sık yapılan gerçek bir hata varsa |
| `hangisi` | "Hangisi…?" | "Çiviye basınca hangisi korur?" | İki ürün ya da iki sınıf kıyaslanacaksa |
| `kac` | "Kaç…?" | "M8 imbusa kaç alyan?" | Cevap bir sayıysa ve usta bunu her gün kullanıyorsa |
| `evet-hayir` | "…olur mu?" | "Kesme taşının tarihi geçer mi?" | Cevap şaşırtıcıysa |
| `ne-demek` | "…ne demek?" | "A2-70'teki 70 ne demek?" | Etiketteki bir işaret açıklanacaksa |
| `neden` | "…neden?" | "Metrenin ucu neden oynar?" | Herkesin gördüğü ama nedenini bilmediği bir şey varsa |
| `nasil` / `nereye` | "…nasıl / nereye?" | "Tork anahtarı nasıl saklanır?" | Doğru kullanım iki seçeneğe indirgenebiliyorsa |
| `renk-kod` | "Şu renk ne?" | "Gri sapan kaç ton taşır?" | Renk ya da işaret kodu varsa |
| `efsane` | "…değil mi?" | "Mıknatıs tuttu, paslanmaz değil mi?" | Yaygın bir yanlış inanış varsa |
| `zor-yol` | "…mı uğraşıyorsun?" | "Sacı önce delip sonra mı vidalıyorsun?" | Yanlış yok ama daha kolay bir yol varsa |

Kanca yazarken:

- **Somut ol:** Ürün ya da iş adını söyle. "Doğru alet önemli" kanca değildir; "Fayansı darbeli mi deliyorsun?" kancadır.
- **Ustaya sor:** "Sen" diye hitap et. Soru, ustanın kendi yaptığı işle ilgili olsun.
- **İlk karede oku:** İlk satır tek başına anlam taşısın; video sessiz izlenirken de anlaşılsın.
- **Uzunluk:** Soru 2 satır, kanca 3 satır. Satır başına en çok 16–20 karakter; uzarsa şablon yazıyı küçültür.
- **Abartma:** "Şok", "inanamayacaksın", "kimse bilmiyor" yazma.

## 3. Kurgular

| Kurgu | Şablon ve alan | Damgalar | Ne zaman |
|---|---|---|---|
| Bil bakalım | `reel_bil` | A / B, geri sayım, "Cevap: …" | Tek doğru cevabı olan soru |
| Yanlış / doğru | `reel_yd`, `cift` yok ya da `yanlis-dogru` | YANLIŞ (kırmızı çarpı) / DOĞRU | Gerçek hata: güvenlik riski ya da alete, parçaya zarar |
| Efsane / gerçek | `reel_yd`, `"cift": "efsane-gercek"` | EFSANE (kırmızı çarpı) / GERÇEK | Yaygın yanlış inanış. Kimse suçlanmaz. |
| Zor yol / kolay yol | `reel_yd`, `"cift": "zor-kolay"` | ZOR YOL (turuncu saat, çarpı yok) / KOLAY YOL | Yanlış yok; bir ürün işi kolaylaştırıyor. Hata sesi çalmaz. |
| Ürün tanıtımı | `reel_tanitim` | Ürün fotoğrafı, özellikler, rozet | Kullanıcı bir ürünü doğrudan tanıtmak istediğinde. Soru ve yanlış/doğru yok. |
| Fragman | `reel_fragman` | Dört sahne ve dört cümle, sonra ürün | Kullanıcı sinematik ve senaryolu ürün tanıtımı istediğinde (ürün tanıtımında ilk tercih). |

- **Kullanıcı "tanıtım videosu" derse:** Doğrudan ürünü tanıtan videoyu kasteder (23 Kasım 2026: "direkt ürünü tanıt, doğru yanlış yapma"). "Ürün tanıtımı" türünü kullan.
- **Fragman senaryosu nasıl yazılır:** Dört kısa cümle bir yay çizer: üç dert ya da istek, dördüncüsü çözüme çağrı. Ardından ürün gelir.
  - Örnek (Rayno kaynak makinesi): "ARK KOPMASIN." · "ELEKTROT YAPIŞMASIN." · "İŞ YARIM KALMASIN." · "GÜCÜ OMZUNA AL." → RAYNO 200A.
  - Her cümle ustanın ağzından çıkabilecek bir istek olsun; her biri ürün sayfasındaki bir özelliğe dayansın (ark kararlılığı, elektrodu yakması, taşınabilirlik).
  - Cümleler aynı kalıpta olsun (hepsi "-masın" ya da hepsi tek kelime); son cümle kalıbı bozar ve ürüne bağlar.
  - Sahne ile cümle uyuşsun: "ark" cümlesinde ark görüntüsü. Görüntüde olmayan şeyi (çatı, iskele) cümleye yazma.
  - Fiyat, kıyas ve abartı yine yok.
- **Sattığımız ürüne çarpı:** İlk panelde bizim sattığımız bir ürün gösterilecekse önce "Zor yol / kolay yol" kurgusunu düşün. Kırmızı çarpı ürünü kötü gösterir. Kullanıcı Karbosan, İzeltaş, GFB, Tyrolit ve Egesan'ın ana bayisidir; bu markaların ürününe çarpı koymadan önce iki kez düşün.
- **Etiketler:**
  - Yanlış / doğru: `tag` "USTA HATASI", `hook_kicker` "SIK YAPILAN HATA".
  - Efsane / gerçek: `tag` "EFSANE Mİ?", `hook_kicker` "DOĞRU BİLİNEN YANLIŞ".
  - Zor yol / kolay yol: `tag` "USTA İPUCU", `hook_kicker` "ZOR YOLDAN MI?".
- **Dönüşüm:** Cuma Reels'inde aynı kurgu iki hafta üst üste gelmesin. Dört haftada en az bir kez "Efsane / gerçek" ya da "Zor yol / kolay yol" kullan.
- **Yeni kurgu:** Yeni bir damga çifti ya da yeni bir Reels türü gerekiyorsa kullanıcıya örnek videoyla öner. Onay gelmeden kuyruğa koyma.

## 4. Konu nereden gelir

1. **Dağarcık:** `python3 fikir.py sec <HAFTA>` o hafta için 3'er aday önerir ve nedenini yazar. Çoğu hafta buradan seç.
2. **Üründen soruya:** Tanıtılacak ürün belliyse şu beş soruyu sor; ilk iyi cevap senaryodur.
   - Bu ürün en çok hangi yanlış aletin yerine kullanılır? → Yanlış / doğru ya da Zor yol / kolay yol.
   - Bu ürünle en sık yapılan hata ne? (Kullanım kılavuzundaki "yapmayın" maddeleri.) → Yanlış / doğru.
   - Etiketinde ya da adında ustanın anlamını bilmediği bir sayı ya da harf var mı? → Bil bakalım (`ne-demek`, `kac`).
   - En çok hangi benzer ürünle karıştırılır? → Bil bakalım (`hangisi`).
   - Hakkında yaygın bir yanlış inanış var mı? → Efsane / gerçek.
3. **Mevsim:**

   | Aylar | Öne çıkan işler |
   |---|---|
   | Aralık – Şubat | Isıtma, akü ve takviye, aydınlatma, kış lastiği, don ve nem, kapalı atölye işleri |
   | Mart – Mayıs | Tadilat, boya, montaj, bahçe, çatı onarımı |
   | Haziran – Ağustos | Tesisat ve klima montajı, şantiye, tekne ve deniz kenarı (A4 paslanmaz) |
   | Eylül – Kasım | Kışa hazırlık, çatı ve oluk, ısıtıcı bakımı, iş güvenliği |

4. **Meslek dönüşümü:** Oto servis, elektrikçi, tesisatçı, marangoz, kaynakçı ve demirci, tornacı ve makine bakımcı, inşaat ve montaj, paslanmaz imalatçı. Aynı mesleğe iki hafta üst üste seslenme.
5. **Paslanmaz ağırlığı:** Kullanıcı paslanmaz bağlantı elemanı ithalatçısıdır. Ayda en az bir Reels paslanmazla ilgili olsun (sarma, demir bulaşması, A2 ve A4, mıknatıs, delme).
6. **Kullanıcının verdiği konu:** Kullanıcı bir konu söylerse dağarcığa ekle ve öne al. Yine de kaynakla doğrula; doğrulanamıyorsa kullanıcıya söyle.

## 5. Dağarcık

- **Dosyalar:** İçerik `dagarcik_yaz.py` içinde yazılır; `python3 dagarcik_yaz.py` komutu `dagarcik.json` dosyasını üretir ve yazı uzunluklarını denetler. `dagarcik.json` elle düzenlenmez.
- **Komutlar:**
  - `python3 fikir.py sec <HAFTA>`: adayları önerir.
  - `python3 fikir.py kuyruk <id>`: kuyruk öğesinin iskeletini yazdırır. "YAZ" yazan alanları doldur (`url`, `search_code`, `urun`, `caption`) ve öğeyi `queue.json` içindeki `reels_bil` ya da `reels_yd` listesine ekle.
  - `python3 fikir.py liste`: tüm fikirleri ve kullanılanları gösterir.
- **Kullanım kaydı:** Öğedeki `fikir` alanı fikrin kimliğidir. `planla.py durum` kullanılan fikri `state.json` içindeki `kullanilan_fikirler` listesine yazar; `fikir.py` onu bir daha önermez.
- **Doğrulama:**
  - `dogrulandi` alanında tarih varsa fikir o gün kaynaktan okunarak doğrulanmıştır.
  - Boşsa kullanmadan önce güvenilir bir kaynakla doğrula; `kaynak` alanına kaynağı ve tarihi yaz.
  - Doğrulanamayan fikri kullanma ve dağarcıktan çıkar.
- **Aynı konunun iki hâli:** Bazı konular hem "Bil bakalım" hem "Efsane / gerçek" olarak yazılıdır (`not` alanında belirtilir). Yalnız biri kullanılır; kullanınca ötekini dağarcıktan çıkar.
- **Dağarcığı büyüt:** Her Pazar çalışmasında, kullandığın her fikrin yerine en az bir yenisini ekle. Kaynaklar:
  - Tanıtılan ürünün kullanım kılavuzu ve üreticinin "yapmayın" listesi,
  - Standartlar (DIN, ISO, EN) ve üretici teknik föyleri,
  - İş güvenliği kurumlarının föyleri (CCOHS, HSE, OSHA),
  - Karnede iyi tutan videonun kalıbına benzeyen yeni bir soru.
- **Kaynak olmaz:** Forum yazısı, kaynağı belirsiz sosyal medya paylaşımı, tek bir satıcının reklam metni.

## 6. Yazım kuralları

- **Dil:** Usta dili, kısa cümle, "sen" hitabı. Yabancı terim yerine atölyede kullanılan söz: "galling" değil "sarma", "PTFE bant" değil "teflon".
- **Sayı ver:** "Düşük devir" yerine mümkünse sayı. Sayıyı kaynakta gördüğün gibi yaz; yuvarlayarak yeni sayı üretme.
- **Neden cümlesi:** Tek cümle, sonucu söyler: "Diş ısınır, sarar, cıvata kopar."
- **Seçenekler:** İki seçenek de akla yatkın olsun. Doğru cevap hep B'de kalmasın; iki videoda bir A'ya koy.
- **Güvenlik:** Net yaz ama korkutma. Kan, yaralanma görüntüsü ve "ölürsün" gibi sözler olmaz.
- **Yasaklar:** Fiyat, "en iyi", "garanti", rakip markayı kötüleme, doğrulanmamış sayı, ürün sayfasında yazmayan özellik.
- **Marka:** Videoda marka adı yalnız kapanış kartında ve panelin alt satırında geçer.

## 7. Açıklama (caption)

Sıra hep aynıdır; hashtag kuralı `ROBOT.md` dosyasındadır (5 adet).

1. **İlk satır:** Videodaki soru ya da hata, aranacak kelimeyle.
   - Bil bakalım: "Bil bakalım: … 🤔 Tahminini yoruma yaz: A mı, B mi? Cevap videoda." Cevabı ve ipucunu yazma.
   - Yanlış / doğru: "… mı yapıyorsun? ❌ Sık yapılan hata." Ardından iki cümleyle doğrusu.
   - Efsane / gerçek: "… sanılır. Gerçek öyle değil." Ardından iki cümleyle açıklama.
   - Zor yol / kolay yol: "… mı uğraşıyorsun? Kolayı var." Ardından iki cümle.
2. **Ürün:** Bir ya da iki cümle; marka, model ve ürün sayfasındaki 2–3 özellik.
3. **Çağrı:** "💾 Kaydet, lazım olur." ya da "📤 … arkadaşına gönder." (mesleğe göre).
4. **Sabit satırlar:** "🔎 Sitede “…” arat", site, sipariş e-postası, telefon.
5. **Hashtag:** 5 adet.

## 8. Kontrol listesi

Öğeyi kuyruğa koymadan önce:

1. Tek fikir var mı?
2. Kanca ilk satırda somut bir iş ya da ürün söylüyor mu?
3. Cevap tartışmasız mı ve kaynağı `kaynak` alanında tarihle yazılı mı?
4. Ürün stokta mı ve soru o ürünün işiyle ilgili mi?
5. Sattığımız bir ürüne kırmızı çarpı geliyor mu? Geliyorsa kurgu doğru mu?
6. "Bil bakalım"da cevap açıklamada gizli mi? Doğru cevabın yeri (A ya da B) geçen haftadan farklı mı?
7. Grup, meslek, kanca kalıbı ve kurgu geçen haftadan farklı mı?
8. Fiyat, abartı, ürün sayfasında olmayan özellik var mı?
9. `fikir`, `kanca_kalibi`, `group` ve (Cuma için) `cift` alanları yazılı mı?
10. Üretimden sonra karelere bak: yazı sığıyor mu, görsel doğru mu, kapanışta ürün görünüyor mu?

## 9. Öğrenme

- **Kayıt:** Karne kaydındaki her Reels'e `kanca_kalibi` ve Cuma Reels'inde `cift` değerini de yaz (`ROBOT.md`, 3. adım).
- **Kıyas:** `python3 fikir.py karne` kalıp ve kurgu başına ortalama geçme oranını yazar. Bir kalıpta en az 2 Reels birikince `fikir.py sec` o veriyi kullanır: geçme oranı düşük olan kalıbı öne alır.
- **Rapor:** Dört haftada bir onay mesajına bir satır yaz: hangi kalıp ve kurgu daha iyi tuttu, hangisi tutmadı. Karar kullanıcınındır.
- **Not:** Bir senaryo beklenenden iyi ya da kötü çıktıysa nedenini `state.json` karne kaydının `not` alanına bir cümleyle yaz. Sonraki senaryoda uygula.
