"""announce/ klasöründeki duyuruları (*.html) Telegram kanalına bir kez gönderir.

Gönderilenler announce/sent.json'a yazılır; aynı duyuru iki kez gitmez.
Metin Telegram'ın HTML biçimiyle gönderilir (<b>, <i>, <a> kullanılabilir).
"""
import glob, json, os, sys, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = "".join(os.environ.get("TELEGRAM_BOT_TOKEN", "").split())
CHAT = "".join(os.environ.get("TELEGRAM_CHAT_ID", "").split())


def send(text):
    chat = CHAT if CHAT.startswith(("@", "-")) or CHAT.isdigit() else "@" + CHAT
    data = urllib.parse.urlencode({"chat_id": chat, "text": text, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=data)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r).get("ok")
    except urllib.error.HTTPError as e:
        print(f"TELEGRAM HATASI {e.code}: {e.read().decode('utf-8', 'replace')}", file=sys.stderr)
        return False


def main():
    if not TOKEN or not CHAT:
        print("Telegram anahtarları tanımlı değil, atlandı.")
        return
    path = os.path.join(ROOT, "announce", "sent.json")
    done = json.load(open(path, encoding="utf-8"))
    failed = False
    for f in sorted(glob.glob(os.path.join(ROOT, "announce", "*.html"))):
        name = os.path.basename(f)
        if name in done:
            continue
        if send(open(f, encoding="utf-8").read().strip()):
            done.append(name)
            print(f"gönderildi: {name}")
        else:
            failed = True
    json.dump(done, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
