"""Her HTML sayfasında ortak site.js ve GoatCounter sayaç satırı olduğundan emin olur.

Eksikse </body>'den hemen önce ekler. Değişiklik olursa 1 döner (iş akışı commit eder).
"""
import glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = '<script src="site.js" defer></script>'
GC = '<script data-goatcounter="https://thezngn.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
changed = []
for f in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
    s = open(f, encoding="utf-8").read()
    t = s
    if "site.js" not in t and "</body>" in t:
        t = t.replace("</body>", TAG + "\n</body>", 1)
    # okunma ve beğeni sayımı (GoatCounter) her sayfada olmalı
    if "gc.zgo.at/count.js" not in t and "</head>" in t:
        t = t.replace("</head>", GC + "\n</head>", 1)
    if t != s:
        open(f, "w", encoding="utf-8").write(t)
        changed.append(os.path.basename(f))
print("eklendi: " + ", ".join(changed) if changed else "tüm sayfalarda var")
