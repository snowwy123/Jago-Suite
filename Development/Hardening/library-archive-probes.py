from pathlib import Path
import zipfile,json,subprocess,os,warnings
r=Path(r'C:\Jago Studio Dev');out=r/'work/Suite-Hardening-2026-10-19/Library-archives';out.mkdir(exist_ok=True);paths=[]
for name,entry in [('parent','../escape.txt'),('absolute','/escape.txt'),('drive','C:/escape.txt'),('backslash','..\\escape.txt'),('duplicate','assets/repeated.txt'),('symlink','assets/link')]:
 p=out/(name+'.jagokit')
 with zipfile.ZipFile(p,'w') as z:
  z.writestr('project.json','{}')
  if name=='symlink':
   info=zipfile.ZipInfo(entry);info.create_system=3;info.external_attr=0xa1ff<<16;z.writestr(info,'../../escape.txt')
  else:
   z.writestr(entry,'harmless test content')
   if name=='duplicate':
    with warnings.catch_warnings():warnings.simplefilter('ignore');z.writestr(entry,'duplicate')
 paths.append(str(p))
script='''(async()=>{let checks=[];try{for(let path of __PATHS__){let message='';try{let result=await projectKitRequest('project-kit-import',{path});message=result.error||'';}catch(e){message=e.message;}if(!/Invalid or duplicate package path/.test(message))throw Error('Expected unsafe archive path rejection: '+path+' '+message);checks.push(path.split('\\\\').pop()+' rejected');}window.testResult={ok:true,checks};}catch(e){window.testResult={ok:false,error:e.stack,checks};}})();'''.replace('__PATHS__',json.dumps(paths))
(out/'probe.js').write_text(script,encoding='utf-8');env=os.environ.copy();env['JAGO_SUITE_ROOT']=str(out/'Suite');si=subprocess.STARTUPINFO();si.dwFlags=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
p=subprocess.run([str(r/'GitHub/Jago-Library-Studio/Jago-Library.exe'),'--test',str(out)],env=env,startupinfo=si,timeout=100);data=json.loads((out/'result.json').read_text(encoding='utf-8-sig'));data=json.loads(data)if isinstance(data,str)else data;assert data['ok'],data;assert not(out/'escape.txt').exists();assert not list((out/'Project-packages').glob('*'));print(json.dumps(data))
