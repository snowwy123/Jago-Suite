from pathlib import Path
import os,subprocess,winreg,json,hashlib,time,argparse
parser=argparse.ArgumentParser();parser.add_argument('--setup',required=True);parser.add_argument('--work',required=True);parser.add_argument('--home-report',required=True);args=parser.parse_args();w=Path(args.work).resolve();w.mkdir(parents=True,exist_ok=True);setup=Path(args.setup).resolve();app=w/'FinalInstall';si=subprocess.STARTUPINFO();si.dwFlags=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0;checks=[]
def run(args,expected=0,env=None):
 p=subprocess.Popen(list(map(str,args)),startupinfo=si,env=env);code=p.wait(timeout=180);assert code==expected,(code,args)
for key in ['library','workspace']:
 try:
  with winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Software\\Jago Suite\\Preview\\Components\\'+key):pass
  raise RuntimeError('An installer preview is already registered. Use a clean test account.')
 except FileNotFoundError:pass
run([setup,'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/TYPE=compact','/DIR='+str(app)])
assert (app/'Jago-Workscape.exe').is_file() and (app/'Library-Production/Jago-Library.exe').is_file()
checks.append('installed executables present')
home=json.loads(Path(args.home_report).read_text())['home'];catalog=Path(home['path'])/'.jago-library/catalog.jagolibrary';saved=catalog.read_text();before=hashlib.sha256(catalog.read_bytes()).hexdigest();test=w/('RetainTest-'+time.strftime('%H%M%S'));test.mkdir()
(test/'probe.js').write_text('(async()=>{try{await loadProject(new File(['+json.dumps(saved)+'],"retained.jagolibrary"));if(state.libraryHome.path!=='+json.dumps(home['path'])+'||state.collections.length!==2||state.collections[1].parent!=="parent")throw Error("Home or collections lost");window.testResult={ok:true,checks:["saved home and nested collections load in installed app"]};}catch(e){window.testResult={ok:false,error:e.message}}})();')
run([app/'Library-Production/Jago-Library.exe','--test',test],env={**os.environ,'JAGO_SUITE_ROOT':str(test/'Suite')});assert (test/'result.txt').read_text().startswith('PASS');checks.append('installed app reopens saved home and nested collections')
work=w/('FinalWorkscape-'+time.strftime('%H%M%S'));work.mkdir();(work/'installer-only.txt').write_text('test');run([app/'Jago-Workscape.exe','--test',work],env={**os.environ,'JAGO_SUITE_ROOT':str(work/'Suite')});result=json.loads((work/'result.json').read_text());assert result['ok'],result;checks+=result['checks']
run([setup,'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/DIR='+str(w/'WrongSecondCopy'),'/LOG='+str(w/'location-guard.log')],expected=7);assert not (w/'WrongSecondCopy/Jago-Workscape.exe').exists();checks.append('update refuses a second installation location')
run([setup,'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART']);assert not (app/'Library-Production/Tools/Documents/LibreOffice/program/soffice.exe').exists();checks.append('update remembers compact selection and location')
run([setup,'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/TYPE=custom','/COMPONENTS=workscape']);assert not (app/'Library-Production/Jago-Library.exe').exists();checks.append('final installer removes deselected Library')
assert before==hashlib.sha256(catalog.read_bytes()).hexdigest();checks.append('linked home catalog unchanged by update and component removal');run([app/'unins000.exe','/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART'])
(w/'final-install-verification.json').write_text(json.dumps({'ok':True,'checks':checks,'installerSHA256':hashlib.sha256(setup.read_bytes()).hexdigest()},indent=2));print(json.dumps({'ok':True,'checks':checks}))
