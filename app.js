(function(){
  var list=document.getElementById('post-list');
  var disc=document.getElementById('disclosure');
  function el(tag,cls,text){var e=document.createElement(tag);if(cls)e.className=cls;if(text!=null)e.textContent=text;return e;}
  function safeUrl(u){if(!u)return null;try{var x=new URL(u,location.href);return (x.protocol==='https:'||x.protocol==='http:')?x.href:null;}catch(e){return null;}}
  fetch('data/posts.json',{cache:'no-cache'}).then(function(r){return r.json();}).then(function(posts){
    list.textContent='';
    if(!Array.isArray(posts)||!posts.length){list.appendChild(el('p','muted','곧 추천템이 올라와요!'));return;}
    var anyProducts=false;
    posts.forEach(function(p){
      var card=el('article','post');card.id='post-'+p.id;
      var head=el('div','post-head');
      if(p.thumbnail){var img=el('img','thumb');img.src=p.thumbnail;img.alt='';img.loading='lazy';head.appendChild(img);}
      var meta=el('div');
      if(p.date)meta.appendChild(el('div','post-date',p.date));
      meta.appendChild(el('div','post-title',p.title||''));
      var yu=safeUrl(p.youtube_url);
      if(yu){var a=el('a','yt-link','▶ 유튜브 영상 보기');a.href=yu;a.target='_blank';a.rel='noopener';meta.appendChild(a);}
      head.appendChild(meta);card.appendChild(head);
      var prods=(p.products||[]).filter(function(x){return x&&x.name&&safeUrl(x.url);});
      if(prods.length){
        anyProducts=true;
        var box=el('div','products');
        prods.forEach(function(x){
          var a=el('a','product');a.href=safeUrl(x.url);a.target='_blank';a.rel='sponsored nofollow noopener';
          a.appendChild(el('div','product-name',x.name));
          if(x.note)a.appendChild(el('div','product-note',x.note));
          a.appendChild(el('div','product-cta','쿠팡에서 보기 →'));
          box.appendChild(a);
        });
        card.appendChild(box);
      }
      list.appendChild(card);
    });
    disc.hidden=!anyProducts;
  }).catch(function(){list.textContent='';list.appendChild(el('p','muted','게시물을 불러오지 못했어요. 잠시 후 다시 시도해 주세요.'));});
})();
