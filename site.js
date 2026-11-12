/* Okuma sayfası üst bandı: ortada doğan güneş (ana sayfadaki şafakla aynı). */
(function(){
  var h=document.querySelector('.hero');
  if(!h||document.body.classList.contains('home')||h.querySelector('.sunbox'))return;
  h.classList.add('dawn');
  var s=document.createElement('div');s.className='sunbox';s.setAttribute('aria-hidden','true');
  s.innerHTML='<div class="sun"></div>';h.appendChild(s);
})();
/* Başa dön düğmesi (sağ alt). Okuma sayfalarında etrafında okuma ilerlemesi halkası. */
(function(){
  if(document.querySelector('.totop')) return;
  var home=document.body.classList.contains('home');
  var R=23,C=2*Math.PI*R;
  var b=document.createElement('button');
  b.type='button';b.className='totop'+(home?'':' ring');
  b.setAttribute('aria-label','Sayfanın başına dön');b.title='Başa dön';
  b.innerHTML=(home?'':'<svg class="pr" viewBox="0 0 52 52" aria-hidden="true"><circle class="tr" cx="26" cy="26" r="'+R+'"/><circle class="fg" cx="26" cy="26" r="'+R+'" stroke-dasharray="'+C+'" stroke-dashoffset="'+C+'"/></svg>')+
    '<svg class="ar" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V6M6 11.5 12 5.5l6 6"/></svg>';
  document.body.appendChild(b);
  var fg=b.querySelector('.fg');
  function upd(){
    var y=window.scrollY||document.documentElement.scrollTop,max=document.documentElement.scrollHeight-innerHeight;
    b.classList.toggle('on',y>160);
    if(fg){var p=max>0?Math.min(1,y/max):0;fg.setAttribute('stroke-dashoffset',String(C*(1-p)))}
  }
  addEventListener('scroll',upd,{passive:true});
  addEventListener('resize',upd);
  b.addEventListener('click',function(){
    var still=matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({top:0,behavior:still?'auto':'smooth'});
    b.blur();
  });
  upd();addEventListener('load',upd);
})();

/* Okuma sayfalarının sonunda ana sayfa bağlantısı. */
(function(){
  if(document.body.classList.contains('home')||document.querySelector('.backhome'))return;
  var m=document.querySelector('main');if(!m)return;
  var a=document.createElement('a');a.className='backhome';a.href='index.html';
  a.innerHTML='<span class="bh-ar" aria-hidden="true">←</span><span><b>Ana sayfaya dön</b><small>Tüm okumalar, Claude ile Erken Okumalar</small></span>';
  m.appendChild(a);
})();

/* İmza satırı: ana sayfada alt notun altında, okuma sayfalarında ana sayfa kartının altında. */
(function(){
  if(document.querySelector('.sig'))return;
  var y=new Date().getFullYear(),yr=y>2026?'2026–'+y:'2026';
  var p=document.createElement('p');p.className='sig';
  p.innerHTML='<span class="sig-sun" aria-hidden="true"></span><a href="https://claude.ai" target="_blank" rel="noopener">Claude</a> (Anthropic) ile yapıldı · <span class="sig-name">Emrah Zengin</span> · '+yr;
  var home=document.body.classList.contains('home');
  var after=home?document.querySelector('.site-foot'):document.querySelector('.backhome');
  if(after&&after.parentNode)after.parentNode.insertBefore(p,after.nextSibling);
  else{var m=document.querySelector('main');if(m)m.appendChild(p)}
  var side=document.querySelector('.side');
  if(side){var q=p.cloneNode(true);q.classList.add('sig-side');q.innerHTML=q.innerHTML.replace(' ile yapıldı · ',' ile yapıldı<br>');side.appendChild(q);p.classList.add('sig-main')}
})();

/* Arşiv sayacı boşsa (abone gibi sayfalarda) ana sayfadaki listeden say. */
(function(){
  var c=document.querySelector('.archcount');if(!c||c.textContent.trim())return;
  fetch('index.html',{cache:'no-cache'}).then(function(r){return r.text()}).then(function(t){
    var n=new DOMParser().parseFromString(t,'text/html').querySelectorAll('ol.list > li').length;
    if(n&&!c.textContent.trim())c.textContent=n;
  }).catch(function(){});
})();

/* Okuma sonunda paylaş düğmesi: WhatsApp, X, LinkedIn, Telegram, bağlantıyı kopyala, (telefonda) diğer. */
(function(){
  if(document.body.classList.contains('home')||document.querySelector('.share'))return;
  var h1=document.querySelector('h1'),m=document.querySelector('main');if(!h1||!m)return;
  var url=location.origin+location.pathname,title=h1.textContent.trim(),e=encodeURIComponent;
  var I={
    chat:'<path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3Z"/>',
    post:'<path d="M9 4 7 20M17 4l-2 16M4 9h16M3 15h16"/>',
    work:'<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
    plane:'<path d="m21 4-18 7 6 2 2 6 3-4 5 4 2-15Z"/>',
    link:'<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    more:'<circle cx="5" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="19" cy="12" r="1.6"/>',
    share:'<path d="M12 15V3M7 8l5-5 5 5M5 13v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/>'
  };
  function ic(k){return '<svg viewBox="0 0 24 24" aria-hidden="true">'+I[k]+'</svg>'}
  var opts=[
    ['WhatsApp','chat','https://wa.me/?text='+e(title+' '+url)],
    ['X','post','https://x.com/intent/post?text='+e(title)+'&url='+e(url)],
    ['LinkedIn','work','https://www.linkedin.com/sharing/share-offsite/?url='+e(url)],
    ['Telegram','plane','https://t.me/share/url?url='+e(url)+'&text='+e(title)]
  ];
  var w=document.createElement('section');w.className='share';w.setAttribute('aria-label','Bu okumayı paylaş');
  var h='<button type="button" class="sharebtn" aria-expanded="false" aria-controls="sharepop">'+ic('share')+'Paylaş</button>'+
    '<div class="sharepop" id="sharepop" hidden>';
  opts.forEach(function(o){h+='<a class="so" href="'+o[2]+'" target="_blank" rel="noopener">'+ic(o[1])+'<span>'+o[0]+'</span></a>'});
  h+='<button type="button" class="so copy">'+ic('link')+'<span>Bağlantıyı kopyala</span></button>';
  if(navigator.share)h+='<button type="button" class="so native">'+ic('more')+'<span>Diğer</span></button>';
  h+='</div><p class="sharemsg" role="status" aria-live="polite"></p>';
  w.innerHTML=h;
  var like=document.querySelector('.like'),home=document.querySelector('.backhome');
  if(like&&like.parentNode)like.parentNode.insertBefore(w,like.nextSibling);
  else if(home)home.parentNode.insertBefore(w,home);else m.appendChild(w);
  var btn=w.querySelector('.sharebtn'),pop=w.querySelector('.sharepop'),msg=w.querySelector('.sharemsg');
  if(like){like.classList.add('withshare');like.appendChild(btn)}
  if(!w.querySelector('.native'))w.querySelector('.copy').classList.add('wide');
  function set(open){pop.hidden=!open;btn.setAttribute('aria-expanded',String(open));w.classList.toggle('open',open)}
  btn.onclick=function(){set(pop.hidden)};
  document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&!pop.hidden){set(false);btn.focus()}});
  w.querySelector('.copy').onclick=function(){
    function ok(){msg.textContent='Bağlantı kopyalandı.';setTimeout(function(){msg.textContent=''},2500)}
    if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(url).then(ok,function(){prompt('Bağlantıyı kopyala:',url)});
    else{var t=document.createElement('textarea');t.value=url;document.body.appendChild(t);t.select();try{document.execCommand('copy');ok()}catch(x){}t.remove()}
  };
  var nat=w.querySelector('.native');
  if(nat)nat.onclick=function(){navigator.share({title:title,url:url}).catch(function(){})};
})();
