"""Her HTML sayfasında ortak site.js (başa dön düğmesi) olduğundan emin olur.

Eksikse </body>'den hemen önce ekler. Değişiklik olursa 1 döner (iş akışı commit eder).
"""
import glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = '<script src="site.js" defer></script>'
changed = []
for f in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
    s = open(f, encoding="utf-8").read()
    if "site.js" in s or "</body>" not in s:
        continue
    open(f, "w", encoding="utf-8").write(s.replace("</body>", TAG + "\n</body>", 1))
    changed.append(os.path.basename(f))
print("eklendi: " + ", ".join(changed) if changed else "tüm sayfalarda var")
