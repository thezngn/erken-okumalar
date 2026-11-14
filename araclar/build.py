import re,sys,json,base64,os
import pathlib
R=str(pathlib.Path(__file__).resolve().parent.parent)+'/'
OUT=os.environ.get('OKUMA_CIKTI','/tmp/okuma-taslak/')
os.makedirs(OUT,exist_ok=True)
def build(slug,title,desc,date,tags,body,src,note,photo=None):
    s=open(R+'ataturk-10-kasim-ortadogu.html',encoding='utf-8').read()
    head=s[:s.index('<div class="hero"')]
    head=re.sub(r'<title>.*?</title>','<title>'+title+' · Claude ile Erken Okumalar</title>',head,flags=re.S)
    head=re.sub(r'<meta name="description" content=".*?">','<meta name="description" content="'+desc+'">',head,flags=re.S)
    hero=s[s.index('<div class="hero"'):s.index('<p class="meta">')]
    chips=''.join('<span class="chip c%d">%s</span>'%(i+1,t) for i,t in enumerate(tags))
    n=len(tags)+1
    meta='<p class="meta"><a href="index.html">← Claude ile Erken Okumalar</a><span>%s</span>%s<span class="chip c%d">13 dk okuma</span><span id="reads" class="reads"></span></p>\n<h1>%s</h1>\n'%(date,chips,min(n,3),title)
    tail=s[s.index('<div class="like">'):]
    tail=re.sub(r'<p class="src">.*?</p>\n<p class="note">.*?</p>','@@S@@',tail,flags=re.S)
    tail=tail.replace('@@S@@','<p class="src"><b>Başlıca kaynaklar:</b> '+src+'</p>\n<p class="note">'+note+'</p>')
    html=head+hero+meta+body+'\n'+tail
    open(OUT+'%s.html'%slug,'w',encoding='utf-8').write(html)
    css=open(R+'style.css',encoding='utf-8').read()
    p=re.sub(r'<script data-goatcounter.*?</script>','',html)
    p=re.sub(r'<link rel="stylesheet" href="style\.css[^"]*">',lambda m:'<style>'+css+'</style>',p)
    for m in re.findall(r'src="(images/[^"]+)"',p):
        fp=R+m
        if os.path.exists(fp):
            p=p.replace('src="%s"'%m,'src="data:image/jpeg;base64,'+base64.b64encode(open(fp,'rb').read()).decode()+'"')
    open(OUT+'%s-onizleme.html'%slug,'w',encoding='utf-8').write(p)
    t=re.sub(r'<svg.*?</svg>|<[^>]+>',' ',html,flags=re.S)
    return len(t.split())
