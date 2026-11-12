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
  var R=21,C=2*Math.PI*R;
  var b=document.createElement('button');
  b.type='button';b.className='totop'+(home?'':' ring');
  b.setAttribute('aria-label','Sayfanın başına dön');b.title='Başa dön';
  b.innerHTML=(home?'':'<svg class="pr" viewBox="0 0 48 48" aria-hidden="true"><circle class="tr" cx="24" cy="24" r="'+R+'"/><circle class="fg" cx="24" cy="24" r="'+R+'" stroke-dasharray="'+C+'" stroke-dashoffset="'+C+'"/></svg>')+
    '<svg class="ar" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V6M6 11.5 12 5.5l6 6"/></svg>';
  document.body.appendChild(b);
  var fg=b.querySelector('.fg'),tick=false;
  function upd(){
    tick=false;
    var y=window.scrollY||document.documentElement.scrollTop,max=document.documentElement.scrollHeight-innerHeight;
    b.classList.toggle('on',y>Math.min(innerHeight*0.6,420));
    if(fg){var p=max>0?Math.min(1,y/max):0;fg.setAttribute('stroke-dashoffset',String(C*(1-p)))}
  }
  addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(upd)}},{passive:true});
  addEventListener('resize',upd);
  b.addEventListener('click',function(){
    var still=matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({top:0,behavior:still?'auto':'smooth'});
    b.blur();
  });
  upd();
})();
