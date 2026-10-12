async function importWobbleTransfer(p,o){
  const count=Math.max(...p.layers.map(l=>l.frames.length)),animated=count>1;
  if(count>48||p.width<16||p.height<16||p.width>2048||p.height>2048||p.width*p.height>2097152)throw Error('Wobble receives up to 48 frames and 2 million canvas pixels. Lower the transfer rate or size.');
  const fps=animated?Math.round(p.frameRate):project.fps;
  if(animated&&(fps<1||fps>24||Math.abs(fps-p.frameRate)>.0001||p.layers.some(l=>l.frames.length!==count||l.frames.some(f=>Math.abs(f.duration-1/fps)>.0001))))throw Error('Send this loop at a whole frame rate from 1–24 fps for Wobble.');
  const matches=p.layers.map(l=>o.mode==='update'?project.layers.find(x=>x.suiteKey===JagoSuite.key(p,l)):null);
  if(o.mode!=='new'&&project.layers.length+matches.filter(x=>!x).length>12)throw Error('There is room for 12 layers. Send combined artwork or start a new project.');
  const timelineMatches=project.loop==='loop'&&project.frames.length===count&&project.fps===fps&&project.frames.every(f=>f.hold===1);
  if(animated&&o.mode!=='new'&&project.frames.length>1&&!timelineMatches)throw Error('This project has a different drawing timeline. Start a new project to preserve the incoming loop, or send a still to add without changing your frame holds.');
  const decoded=[];for(const l of p.layers)for(const f of l.frames){const image=await JagoSuite.decode(f.src);if(image.width!==p.width||image.height!==p.height)throw Error('Transfer frames have inconsistent dimensions.');decoded.push([f.src,image])}
  const old=JSON.parse(snapshot());pause();clearSelection();
  try{
    if(o.mode==='new'){project=fresh(p.width,p.height);project.layers=[];project.frames=[];project.name=p.name.slice(0,100);project.transparent=true;project.wiggleEnabled=false;project.suiteProjectId=crypto.randomUUID()}
    const before=project.frames.slice(),frameCount=animated?count:Math.max(1,before.length),generated=[];
    for(let i=0;i<frameCount;i++){const source=animated?(timelineMatches?before[i]:before[0]):before[i];generated.push({id:source?.id||uid(),hold:animated?1:(source?.hold||1),contents:source?copy(source.contents):{}})}
    for(const l of p.layers){const key=JagoSuite.key(p,l);let layer=o.mode==='update'?project.layers.find(x=>x.suiteKey===key):null;const wasLinked=!!layer;if(!layer){layer={id:uid(),name:l.name.slice(0,60),visible:true,locked:false,opacity:1,blend:['source-over','multiply','screen','overlay','darken','lighten','difference'].includes(l.blend)?l.blend:'source-over',suiteKey:key};project.layers.push(layer)}
      for(let i=0;i<generated.length;i++){const f=JagoSuite.frameAt(l,animated?i/fps:0,p.seconds),scale=Math.min(1,project.width/p.width,project.height/p.height),previous=before[Math.min(i,before.length-1)]?.contents[layer.id]?.find(op=>op.kind==='image');const op=wasLinked&&previous?{...previous,src:f.src}:{kind:'image',src:f.src,x:(project.width-p.width*scale)/2,y:(project.height-p.height*scale)/2,w:p.width*scale,h:p.height*scale,opacity:1,wiggle:false};generated[i].contents[layer.id]=[op]}
      project.activeLayer=layer.id;
    }
    project.frames=generated;if(animated){project.fps=fps;project.loop='loop'}for(const [src,image]of decoded)imageCache.set(src,image);project.current=0;resizeBuffers();invalidate();commit('Artwork received from '+p.sourceStudio);fit();scheduleSave();adapter.lastSource=p.sourceStudio;adapter.lastPackage=p;
  }catch(e){project=old;resizeBuffers();invalidate();updateUI();throw e}
}
