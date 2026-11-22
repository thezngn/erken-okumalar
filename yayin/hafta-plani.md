# Haftalık yayın planı (Claude ile Erken Okumalar)

Her gün 07:45 İstanbul (feed pubDate 04:45 UTC), 13 dakikalık Türkçe okuma (~2.800 kelime).

| Gün | Tema |
|---|---|
| Pazartesi | Kişisel gelişim |
| Salı | Tarih, devlet tarihleri |
| Çarşamba | AB ülke ekonomisi, sıra: Almanya (18 Kas), Fransa (25 Kas), İspanya, Hollanda, Polonya, Yunanistan |
| Perşembe | Kelime ve eşya kökeni |
| Cuma | Uzay |
| Cumartesi | Saatler ve spor otomobiller |
| Pazar | Serbest / güncel |

## Konu seçimi
- Emrah'a konular haftada bir kez, Pazar günü sorulur (sonraki Salı ve Perşembe-Pazar için; Çarşamba ülke sırasına göre sabit).
- Cevap gelmezse plan kendiliğinden sürer: her tema için listenin ilk önerisi alınır.
- 16 Kas Pzt: Uyku ve öğrenme (yayın kuyruğunda). 18 Kas Çar: Almanya.

## Yayın düzeni
- Yazı yayin/<slug>.html olarak yazılır, yayin/kuyruk.json'a eklenir (pub, rfc, tags, date_card). scripts/yayin_kuyrugu.py zamanı gelince sayfayı, kartı ve feed öğesini ekler.
- Her sabah 07:45'te bulut görevi yayin-kuyrugu.yml iş akışını başlatır; GitHub zamanlayıcısı yedek.
- Notify (Telegram) ve email iş akışları feed.xml push'uyla tetiklenir.

## Yazı kuralları
- Her şey Türkçe. Bildiğim ama doğrulamadığım bilgiler yazıda işaretlenir. "O Gün" etiketi yok, tarihe bağlı konular az.
- Orijinal satır içi SVG infografikler (en az 2-3), Pexels/Unsplash lisanslı, insan (ünlü) içermeyen fotoğraf (images.json + fetch-images iş akışı).
- Bölümler: veri notu, "Kaynaklar çelişiyor", "Bu yazının sınırları", kaynak listesi.
- turkish-anti-ai-skill taraması: "Yani", "X değil, Y", em-dash, "aslında" vb. temizlenir.

## Bu haftanın konuları (Emrah, 15 Kasım Pazar günü seçti)
- Sal 17 Kas: Boltzmann Beyni Paradoksu (kuyrukta)
- Çar 18 Kas: Almanya ekonomisi (kuyrukta)
- Per 19 Kas: Maaş ve tuz (kuyrukta)
- Cum 20 Kas: Porsche 911'in tarihi (Emrah'ın seçimi, tema uzaydı)
- Cmt 21 Kas: Boylam sorunu ve deniz kronometresi
- Paz 22 Kas: Veri merkezleri ve elektrik tüketimi

## Gelecek haftanın konuları (22 Kasım Pazar sorusu, cevap gelmedi, varsayılanlar alındı)
- Pzt 23 Kas: kişisel gelişim (konu sorulmadı, kuyrukta kayıt yok; içerik oturumu bakmalı)
- Sal 24 Kas: Venedik Cumhuriyeti (kuyrukta)
- Çar 25 Kas: Fransa ekonomisi (kuyrukta)
- Per 26 Kas: Kahve, kelime yolculuğu (kuyrukta)
- Cum 27 Kas: Voyager 1 ve 2 (kuyrukta)
- Cmt 28 Kas: McLaren F1 (varsayılan Kuvars krizi quartz-krizi.html olarak zaten yayında olduğundan 2. öneri alındı)
- Paz 29 Kas: Kuzey Deniz Yolu (kuyrukta)
- Not: Kuzey Deniz Yolu fotoğrafının fotoğrafçı adı ve sayfa URL'si doğrulanamadı (images.json "DOĞRULANAMADI"); fotoğraflar fetch-images iş akışıyla inecek.
