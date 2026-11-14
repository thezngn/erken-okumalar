"""yayin/kuyruk.json içindeki zamanı gelmiş yazıları yayınlar (sayfa, ana sayfa kartı, akış öğesi).
Tekrar çalıştırılabilir: akışta olan yazıya dokunmaz. Yayınlanan slug'ları stdout'a yazar."""
import json, shutil, datetime, html, re
now = datetime.datetime.now(datetime.timezone.utc)
q = json.load(open('yayin/kuyruk.json', encoding='utf-8'))
feed = open('feed.xml', encoding='utf-8').read()
index = open('index.html', encoding='utf-8').read()
done = []
for it in q:
    slug = it['slug']
    due = datetime.datetime.fromisoformat(it['pub'].replace('Z', '+00:00'))
    if due > now or (slug + '.html') in feed:
        continue
    shutil.copy(it['file'], slug + '.html')
    if (slug + '.html') not in index:
        chips = ' '.join('<span class="chip c%d">%s</span>' % (k + 1, t) for k, t in enumerate(it['tags'])) + ' <span class="chip c3">13 dk</span>'
        card = '<li><a href="%s.html">%s</a><div class="m">%s &nbsp;%s</div></li>\n' % (slug, it['title'], it['date_card'], chips)
        index = index.replace('</ol>', card + '</ol>', 1)
    item = ('<item>\n<title>%s</title>\n<link>https://thezngn.github.io/erken-okumalar/%s.html</link>\n'
            '<guid>https://thezngn.github.io/erken-okumalar/%s.html</guid>\n<pubDate>%s</pubDate>\n'
            '<description>%s 13 dakikalık okuma.</description>\n</item>\n') % (it['title'], slug, slug, it['rfc'], it['desc'])
    feed = feed.replace('</channel>', item + '</channel>', 1)
    done.append(slug)
if done:
    open('feed.xml', 'w', encoding='utf-8').write(feed)
    open('index.html', 'w', encoding='utf-8').write(index)
print(' '.join(done))
