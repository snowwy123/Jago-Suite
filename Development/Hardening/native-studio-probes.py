from pathlib import Path
import os,subprocess,time,json,uuid
r=Path(r'C:\Jago Studio Dev');out=r/'work/Suite-Hardening-2026-10-19/Native';out.mkdir(exist_ok=True);rows=[]
script=r'''(async()=>{let checks=[],check=(v,n)=>{if(!v)throw Error(n);checks.push(n);};try{let snapshot=await JagoSession.capture();check(!!snapshot.document,'editable capture');await JagoSession.restore(snapshot.document);check(!!(await JagoSession.capture()).document,'editable restore');let before=location.href;location.href=before.replace(/[^/]+$/,'untrusted-preview.html');await new Promise(r=>setTimeout(r,150));check(location.href===before,'sibling document navigation blocked');if(snapshot.studio!=='pulse'){let got=false;let on=e=>{if(e.data.type==='jago-suite-fonts')got=true;};chrome.webview.addEventListener('message',on);chrome.webview.postMessage({type:'jago-suite-fonts'});for(let i=0;i<20&&!got;i++)await new Promise(r=>setTimeout(r,50));chrome.webview.removeEventListener('message',on);check(got,'trusted app retains native font bridge');}window.__workspaceTestResult={ok:true,checks};}catch(e){window.__workspaceTestResult={ok:false,error:e.stack,checks};}})();'''
def waitfile(p,child,seconds=45):
 end=time.monotonic()+seconds
 while not p.exists():
  if child.poll() is not None:raise RuntimeError('App exited before '+str(p))
  if time.monotonic()>end:raise TimeoutError(str(p))
  time.sleep(.1)
 return p.read_text(encoding='utf-8-sig')
for name in ['Wobble','Dither','Repeat','World','Material','Sound','Library','Pulse']:
 folder=out/name;folder.mkdir(exist_ok=False);env=os.environ.copy();env.update(JAGO_SUITE_ROOT=str(out/'Suite'),JAGO_WORKSPACE_ROOT=str(out/'Session'),JAGO_WORKSPACE_TAB_ROOT=str(folder),JAGO_WORKSPACE_TAB_ID=uuid.uuid4().hex,JAGO_WORKSPACE_TEST_ROOT=str(out));(out/'Session').mkdir(exist_ok=True)
 si=subprocess.STARTUPINFO();si.dwFlags=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
 child=subprocess.Popen([str(r/f'GitHub/Jago-{name}-Studio/Jago-{name}.exe')],env=env,startupinfo=si)
 try:
  waitfile(folder/'ready.json',child);(folder/'command-000.json').write_text('{broken command',encoding='utf-8');(folder/'command-001.json').write_text(json.dumps({'type':'test','script':script}),encoding='utf-8')
  data=json.loads(waitfile(folder/'test-result.json',child));data['studio']=name;data['invalidCommandQuarantined']=len(list(folder.glob('command-000.json.invalid-*')))==1;assert data['ok'] and data['invalidCommandQuarantined'],data;rows.append(data);print(json.dumps(data),flush=True)
 finally:
  if child.poll() is None:
   (folder/'command-999.json').write_text('{"type":"close"}',encoding='utf-8')
   try:child.wait(timeout=10)
   except subprocess.TimeoutExpired:child.terminate();child.wait(timeout=10)
(out/'result.json').write_text(json.dumps({'ok':True,'results':rows},indent=2),encoding='utf-8')
