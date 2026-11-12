"""feed.xml'deki yeni okumaları Brevo üzerinden abone listesine e-postayla gönderir.

Gerekli gizli ayarlar (GitHub > Settings > Secrets and variables > Actions):
  BREVO_API_KEY       Brevo > SMTP & API > API Keys
  BREVO_LIST_ID       Brevo > Contacts > Lists'teki listenin numarası (#)
  BREVO_SENDER_EMAIL  Brevo'da doğrulanmış gönderici adresi
İsteğe bağlı: BREVO_SENDER_NAME (varsayılan "Claude ile Erken Okumalar")

Anahtarlar yoksa hiçbir şey yapmadan çıkar. Gönderilenler email-notified.json'a yazılır;
aynı okuma iki kez gitmez. Sayfa henüz yayında değilse ~6 dk bekler.
Deneme: python scripts/notify_email.py --preview  -> email-preview.html üretir, göndermez.
"""
import html, json, os, re, sys, time, urllib.error, urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get("BREVO_API_KEY", "").strip()
LIST = os.environ.get("BREVO_LIST_ID", "").strip()
SENDER = os.environ.get("BREVO_SENDER_EMAIL", "").strip()
SENDER_NAME = os.environ.get("BREVO_SENDER_NAME", "").strip() or "Claude ile Erken Okumalar"
MON = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
DAY = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
STATE = os.path.join(ROOT, "email-notified.json")


def api(path, body=None, method="POST"):
    req = urllib.request.Request("https://api.brevo.com/v3" + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"api-key": KEY, "content-type": "application/json", "accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            t = r.read().decode() or "{}"
            return r.status, json.loads(t)
    except urllib.error.HTTPError as e:
        print(f"BREVO HATASI {e.code} {path}: {e.read().decode('utf-8', 'replace')}", file=sys.stderr)
        return e.code, None


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


def tags_for(link):
    """Okumanın etiketlerini index.html'deki kartından okur."""
    try:
        s = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
        f = link.rsplit("/", 1)[-1]
        m = re.search(r'<li><a href="' + re.escape(f) + r'">.*?</li>', s, re.S)
        return re.findall(r'chip c[124]">([^<]+)<', m.group(0)) if m else []
    except Exception:
        return []


def build(item):
    title = item.findtext("title") or ""
    link = item.findtext("link") or ""
    desc = re.sub(r"\s*13 dakikalık okuma\.?\s*$", "", item.findtext("description") or "")
    try:
        d = parsedate_to_datetime(item.findtext("pubDate"))
        d = d.astimezone(__import__("zoneinfo").ZoneInfo("Europe/Istanbul"))
        date = f"{d.day} {MON[d.month-1]} {DAY[d.weekday()]}"
    except Exception:
        date = ""
    tags = "".join(html.escape(t) + " · " for t in tags_for(link))
    tpl = open(os.path.join(ROOT, "templates", "email.html"), encoding="utf-8").read()
    body = (tpl.replace("{{TITLE}}", html.escape(title)).replace("{{DESC}}", html.escape(desc))
               .replace("{{DATE}}", date).replace("{{TAGS}}", tags).replace("{{URL}}", html.escape(link)))
    return title, link, body


def main():
    items = ET.parse(os.path.join(ROOT, "feed.xml")).getroot().findall("./channel/item")
    if "--preview" in sys.argv:
        newest = max(items, key=lambda it: parsedate_to_datetime(it.findtext("pubDate")))
        open(os.path.join(ROOT, "email-preview.html"), "w", encoding="utf-8").write(build(newest)[2])
        print("email-preview.html yazıldı")
        return
    if not (KEY and LIST and SENDER):
        print("Brevo anahtarları tanımlı değil, e-posta atlandı.")
        return
    done = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else []
    failed = False
    for it in sorted(items, key=lambda it: parsedate_to_datetime(it.findtext("pubDate"))):
        link = it.findtext("link")
        if link in done:
            continue
        if not live(link):
            print(f"yayında değil, sonra denenecek: {link}", file=sys.stderr)
            failed = True
            continue
        title, link, body = build(it)
        code, res = api("/emailCampaigns", {
            "name": f"Erken Okumalar: {title}"[:120],
            "subject": f"☀️ {title}",
            "previewText": re.sub(r"\s*13 dakikalık okuma\.?\s*$", "", it.findtext("description") or "")[:140],
            "sender": {"name": SENDER_NAME, "email": SENDER},
            "htmlContent": body,
            "recipients": {"listIds": [int(LIST)]},
        })
        if code not in (200, 201) or not res or "id" not in res:
            failed = True
            continue
        code, _ = api(f"/emailCampaigns/{res['id']}/sendNow")
        if code in (200, 204):
            done.append(link)
            print(f"gönderildi: {link}")
        else:
            failed = True
    json.dump(done, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
