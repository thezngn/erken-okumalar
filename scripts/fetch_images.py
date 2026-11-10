"""images.json içindeki fotoğrafları images/ klasörüne indirir.

Zaten inmiş dosyaları atlar. Bir indirme başarısız olursa, görsel olmayan bir
içerik gelirse ya da dosya 8 MB'ı aşarsa en sonda hata koduyla çıkar.
"""
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_BYTES = 8 * 1024 * 1024
HEADERS = {"User-Agent": "erken-okumalar-bot/1.0 (+https://github.com/thezngn/erken-okumalar)"}


def main():
    with open(os.path.join(ROOT, "images.json"), encoding="utf-8") as f:
        items = json.load(f)

    out_dir = os.path.join(ROOT, "images")
    os.makedirs(out_dir, exist_ok=True)
    failures = []

    for item in items:
        dest = os.path.join(out_dir, item["file"])
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            print(f"atlandı (zaten var): {item['file']}")
            continue
        try:
            req = urllib.request.Request(item["url"], headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as resp:
                ctype = resp.headers.get_content_type()
                if not ctype.startswith("image/"):
                    raise ValueError(f"görsel değil: {ctype}")
                data = resp.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError("dosya 8 MB'dan büyük")
            if not data:
                raise ValueError("boş yanıt")
            with open(dest, "wb") as out:
                out.write(data)
            print(f"indirildi: {item['file']} ({len(data) // 1024} KB)")
        except Exception as exc:
            failures.append(item["file"])
            print(f"HATA: {item['file']}: {exc}", file=sys.stderr)

    if failures:
        print("İndirilemeyenler: " + ", ".join(failures), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
