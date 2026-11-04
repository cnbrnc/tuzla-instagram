# Tuzla Hırdavat Instagram Robotu

Bu depo, tuzlahirdavat.com.tr Instagram sayfasının (@tuzla_civata_hirdavat) haftalık gönderi robotunun dosyalarını tutar.

Haftalık düzen (16 Kasım 2026'dan itibaren, hepsi 10:00):

| Gün | Gönderi |
|---|---|
| Pazartesi | Ürün Reels'i |
| Çarşamba | Ürün kaydırmalısı |
| Perşembe | Usta İpucu kaydırmalısı |
| Cuma | Ürün Reels'i |

- `ROBOT.md`: Robotun her Pazar izlediği adımlar.
- `posts/`: Onaylanmış gönderi görselleri ve videoları. Metricool dosyaları buradan çeker.
- `weeks/`: Her haftanın gönderi tanımları.
- `templates/`, `render.py`, `reel.py`, `onizleme.py`: Görsel, video ve önizleme üretimi.
- `hafta.py`, `planla.py`: Haftayı kuyruktan kurma ve onaydan sonra Metricool'a planlama.
- `fetch_product.py`, `pick_products.py`: Siteden ürün bilgisi ve yeni ürün adayları.
- `queue.json`: Sırada bekleyen içerikler.
- `state.json`: Paylaşılanlar, haftalık karne ve ayarlar.

Fiyat bilgisi hiçbir gönderide yer almaz. Sipariş: satis5@tuzlacivata.com.tr
