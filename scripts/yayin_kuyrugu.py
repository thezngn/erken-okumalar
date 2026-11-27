"""yayin/kuyruk.json içindeki zamanı gelmiş yazıları yayınlar (sayfa, ana sayfa kartı, akış öğesi).
Tekrar çalıştırılabilir: akışta olan yazıya dokunmaz. Yayınlanan slug'ları stdout'a yazar."""
import json, shutil, datetime, html, re
now = datetime.datetime.now(datetime.timezone.utc)
q = json.load(open('yayin/kuyruk.json', encoding='utf-8'))
feed = open('feed.xml', encoding='utf-8').read()
index = open('index.html', encoding='utf-8').read()
done = []
last_dk = None
# 1 Aralık 2026'dan itibaren okumalar 7 dakikalık. Kayıtta "dk" alanı varsa o geçerli.
SWITCH = datetime.datetime(2026, 11, 30, 21, 0, tzinfo=datetime.timezone.utc)


def minutes(it):
    if 'dk' in it:
        return int(it['dk'])
    due = datetime.datetime.fromisoformat(it['pub'].replace('Z', '+00:00'))
    return 7 if due >= SWITCH else 13


def retag(path, dk):
    """Site genelindeki 'N dakika' ifadelerini son yayımlanan okumanın süresine uydurur."""
    s = open(path, encoding='utf-8').read()
    t = re.sub(r'\d+ dakikada okunacak', '%d dakikada okunacak' % dk, s)
    t = re.sub(r'\d+ dakikalık yazılar', '%d dakikalık yazılar' % dk, t)
    t = re.sub(r'(Emrah’a )\d+( dakikalık araştırmalı okuma)', r'\g<1>%d\g<2>' % dk, t)
    if t != s:
        open(path, 'w', encoding='utf-8').write(t)

for it in q:
    slug = it['slug']
    due = datetime.datetime.fromisoformat(it['pub'].replace('Z', '+00:00'))
    if due > now or (slug + '.html') in feed:
        continue
    shutil.copy(it['file'], slug + '.html')
    if (slug + '.html') not in index:
        chips = ' '.join('<span class="chip c%d">%s</span>' % (k + 1, t) for k, t in enumerate(it['tags'])) + ' <span class="chip c3">%d dk</span>' % minutes(it)
        card = '<li><a href="%s.html">%s</a><div class="m">%s &nbsp;%s</div></li>\n' % (slug, it['title'], it['date_card'], chips)
        index = index.replace('</ol>', card + '</ol>', 1)
    item = ('<item>\n<title>%s</title>\n<link>https://thezngn.github.io/erken-okumalar/%s.html</link>\n'
            '<guid>https://thezngn.github.io/erken-okumalar/%s.html</guid>\n<pubDate>%s</pubDate>\n'
            '<description>%s %d dakikalık okuma.</description>\n</item>\n') % (it['title'], slug, slug, it['rfc'], it['desc'], minutes(it))
    feed = feed.replace('</channel>', item + '</channel>', 1)
    done.append(slug)
    last_dk = minutes(it)
if done:
    open('feed.xml', 'w', encoding='utf-8').write(feed)
    open('index.html', 'w', encoding='utf-8').write(index)
    for p in ('index.html', 'arsiv.html', 'abone.html', 'feed.xml'):
        retag(p, last_dk)
print(' '.join(done))
