from pathlib import Path
import os,subprocess,json,time
r=Path(r'C:\Jago Studio Dev');base=r/'work/Suite-Hardening-2026-10-19/Workscape';base.mkdir(exist_ok=True);keys={'wobble':'Wobble','dither':'Dither','repeat':'Repeat','worldbuilding':'World','material':'Material','music':'Sound','library':'Library','pulse':'Pulse','companion':'Companion'}
for mode in ['all','pulse']:
 out=base/mode;out.mkdir(exist_ok=False);(out/'studio-locations.json').write_text(json.dumps({key:str(r/('GitHub/Jago-Companion/Jago-Companion.exe' if name=='Companion' else f'GitHub/Jago-{name}-Studio/Jago-{name}.exe'))for key,name in keys.items()}),encoding='utf-8')
 if mode=='pulse':(out/'pulse-only.txt').write_text('1')
 env=os.environ.copy();env['JAGO_SUITE_ROOT']=str(out/'Suite');si=subprocess.STARTUPINFO();si.dwFlags=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
 child=subprocess.Popen([str(r/'GitHub/Jago-Workscape/Jago-Workscape.exe'),'--test',str(out)],env=env,startupinfo=si)
 try:
  if mode=='all':
   for _ in range(100):
    sessions=list((out/'Sessions').glob('*'))if(out/'Sessions').exists()else[]
    if sessions:
     bad=sessions[0]/'action-invalid.json';bad.write_text('{invalid',encoding='utf-8');break
    time.sleep(.05)
  child.wait(timeout=240);data=json.loads((out/'result.json').read_text(encoding='utf-8-sig'));assert data.get('ok'),data
  if mode=='all':assert list(bad.parent.glob(bad.name+'.invalid-*')),'bad action was not quarantined'
  print(json.dumps({'mode':mode,'ok':True,'checks':len(data.get('checks',[]))}),flush=True)
 finally:
  if child.poll() is None:child.terminate();child.wait(timeout=10)
