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
