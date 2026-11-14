# Claude ile Erken Okumalar: ortak çalışma notu

Bu depo tek gerçek kaynaktır. Hangi oturum (sohbet sekmesi, bulut görevi) çalışırsa çalışsın önce bu dosyayı, sonra yayin/hafta-plani.md dosyasını oku.

## Roller
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

## Açık konular
- GitHub'ın cron (schedule) tetikleyicisinin bu depoda çalışıp çalışmadığı doğrulanmadı. Bulut görevi asıl tetikleyici, cron yedek.
