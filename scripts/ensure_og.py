"""Her sayfaya bağlantı önizleme etiketlerini (Open Graph / Twitter) ekler.

Okuma sayfaları: başlık <h1>'den, özet meta description'dan, görsel yazının ilk
fotoğrafından (yoksa images/og.png). Ana sayfa, arşiv ve abone: site kartı.
Etiketler <!-- og --> ... <!-- /og --> arasında durur; her çalıştırmada yenilenir.
"""
import glob, html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://thezngn.github.io/erken-okumalar/"
SITE = "Claude ile Erken Okumalar"
SITE_DESC = ("Her sabah 07.45’te yeni bir okuma. Bir yapay zeka ajanının araştırıp yazdığı "
             "13 dakikalık yazılar: tarihten ekonomiye, merak uyandıran her şey.")
SPECIAL = {"index.html": (SITE, ""), "arsiv.html": ("Arşiv · " + SITE, "arsiv.html"),
           "abone.html": ("E-posta ile abone ol · " + SITE, "abone.html")}


def esc(s):
    return html.escape(html.unescape(s.strip()), quote=True)


def tags(title, desc, url, image, kind):
    return ("<!-- og -->\n"
            f'<meta property="og:site_name" content="{SITE}">\n'
            f'<meta property="og:locale" content="tr_TR">\n'
            f'<meta property="og:type" content="{kind}">\n'
            f'<meta property="og:title" content="{esc(title)}">\n'
            f'<meta property="og:description" content="{esc(desc)}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{image}">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            "<!-- /og -->")


changed = []
for f in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
    name = os.path.basename(f)
    s = open(f, encoding="utf-8").read()
    if "</head>" not in s:
        continue
    t = re.sub(r'\n?<meta property="og:[^>]*>|\n?<meta name="twitter:[^>]*>', "", s)
    t = re.sub(r"\n?<!-- og -->.*?<!-- /og -->", "", t, flags=re.S)
    if name in SPECIAL:
        title, path = SPECIAL[name]
        block = tags(title, SITE_DESC, BASE + path, BASE + "images/og.png", "website")
    else:
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
        title = re.sub(r"<[^>]+>", "", h1.group(1)) if h1 else SITE
        d = re.search(r'<meta name="description" content="([^"]*)"', t)
        desc = d.group(1) if d else SITE_DESC
        img = re.search(r'<figure class="photo">\s*<img[^>]*src="(images/[^"]+)"', t)
        image = BASE + (img.group(1) if img and os.path.exists(os.path.join(ROOT, img.group(1))) else "images/og.png")
        block = tags(title, desc, BASE + name, image, "article")
    t = t.replace("</head>", block + "\n</head>", 1)
    if t != s:
        open(f, "w", encoding="utf-8").write(t)
        changed.append(name)
print("güncellendi: " + ", ".join(changed) if changed else "değişiklik yok")
