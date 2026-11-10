"""feed.xml'deki yeni yazıları Telegram kanalına gönderir.

TELEGRAM_BOT_TOKEN ve TELEGRAM_CHAT_ID tanımlı değilse hiçbir şey yapmadan çıkar.
Gönderilenler notified.json'a yazılır; aynı yazı iki kez gitmez.
Sayfa henüz yayında değilse (HTTP 200 dönmüyorsa) en fazla ~6 dk bekler.
"""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = "".join(os.environ.get("TELEGRAM_BOT_TOKEN", "").split())
CHAT = "".join(os.environ.get("TELEGRAM_CHAT_ID", "").split())


def live(url):
    for _ in range(12):
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(30)
    return False


def send(text):
    chat = CHAT if CHAT.startswith(("@", "-")) or CHAT.isdigit() else "@" + CHAT
    data = urllib.parse.urlencode({"chat_id": chat, "text": text}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=data)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r).get("ok")
    except urllib.error.HTTPError as e:
        # Telegram hatanın nedenini gövdede yazar (ör. "chat not found", "Unauthorized")
        print(f"TELEGRAM HATASI {e.code}: {e.read().decode('utf-8', 'replace')}", file=sys.stderr)
        return False


def main():
    if not TOKEN or not CHAT:
        print("Telegram anahtarları tanımlı değil, atlandı.")
        return
    path = os.path.join(ROOT, "notified.json")
    done = json.load(open(path, encoding="utf-8"))
    items = ET.parse(os.path.join(ROOT, "feed.xml")).getroot().findall("./channel/item")
    failed = False
    for it in reversed(items):
        link = it.findtext("link")
        if link in done:
            continue
        if not live(link):
            print(f"yayında değil, sonra denenecek: {link}", file=sys.stderr)
            failed = True
            continue
        if send(f"☀️ Yeni okuma\n\n{it.findtext('title')}\n13 dk\n\n{link}"):
            done.append(link)
            print(f"gönderildi: {link}")
        else:
            failed = True
    json.dump(done, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
