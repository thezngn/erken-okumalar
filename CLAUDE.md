# Claude ile Erken Okumalar: ortak çalışma notu

Bu depo tek gerçek kaynaktır. Hangi oturum (sohbet sekmesi, bulut görevi) çalışırsa çalışsın önce bu dosyayı, sonra yayin/hafta-plani.md dosyasını oku.

## Roller
Kural: okuma yazıları yalnızca içerik oturumunda yazılır. Altyapı oturumu yazı yazmaz, konu seçmez, kuyruğa yazı eklemez; yazı sorunu görürse içerik oturumuna iletilmesi için Emrah'a söyler.

- İçerik oturumu: yazıları araştırır, yazar, yayin/ altına koyar, yayin/kuyruk.json'a ekler.
- Altyapı oturumu ("Erken okumalar sayfası tasarımı" sohbeti, gh erişimi var): tasarım, style.css, iş akışları (notify, email, fetch-images, yayin-kuyrugu), GitHub Actions kontrolü.
- Bulut görevleri: her sabah 07:45'te yayin-kuyrugu.yml iş akışını başlatır; Pazar 10:17'de haftalık konu sorusu gelir.

## Yayın akışı
1. Yazı gövdesi yazılır, araclar/build.py ile sayfa derlenir (OKUMA_CIKTI ortam değişkeni çıktı klasörü).
2. Derlenen sayfa yayin/<slug>.html olarak konur, fotoğraf images.json'a eklenir.
3. yayin/kuyruk.json'a kayıt eklenir (slug, file, title, desc, tags, date_card, pub, rfc).
4. scripts/yayin_kuyrugu.py zamanı gelen yazıyı kök dizine kopyalar, ana sayfa kartını ve feed.xml öğesini ekler. feed.xml değişince notify.yml ve email.yml tetiklenir.

## Çakışmayı önleme
- Push'tan önce git pull --rebase origin main.
- Bir oturum başka oturumun dosyasını (özellikle iş akışlarını) değiştirecekse önce commit geçmişine bak.
- Kuyruk betiği idempotent: akışta olan slug'a dokunmaz.

## Okuma süresi
- 1 Aralık 2026'dan itibaren okumalar 7 dakikalık (~1.500-1.600 kelime). Öncesi 13 dakika (~2.800 kelime), eski sayfalar olduğu gibi kalır.
- Süre kod tarafında otomatik: kuyruk kaydında "dk" alanı yoksa pub tarihi 1 Aralık 2026 İstanbul gününden sonraysa 7, değilse 13 sayılır. Kayıtta "dk" varsa o geçerlidir.
- Etkilenen yerler: sayfa etiketi (araclar/build.py `dk=` parametresi), ana sayfa kartı ve feed açıklaması (scripts/yayin_kuyrugu.py), Telegram ve e-posta (süreyi feed açıklamasından okur), site sloganı (kuyruk betiği index, arşiv, abone ve feed kanal açıklamasını son yayımlanan okumanın süresine göre günceller; ensure_og.py bağlantı önizlemesini aynı şekilde).
- Yeni yazı derlerken Aralık'tan itibaren `build(..., dk=7)` verilir.

## Açık konular
- GitHub'ın zamanlayıcısı (schedule) denendi, güvenilir değil: 13 Kasım işi 8 saat geç geldi, 14 Kasım'daki zamanlı çalıştırmalar atlandı. Asıl tetikleyici 07:45 bulut görevi. Zamanlayıcı bir gün geç çalışsa da kuyruk betiği idempotent olduğu için zarar vermez.
