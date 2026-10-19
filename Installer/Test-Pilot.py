from pathlib import Path
import subprocess,winreg,json,os,hashlib,time,argparse
parser=argparse.ArgumentParser();parser.add_argument('--work',required=True);parser.add_argument('--setup',required=True);args=parser.parse_args();w=Path(args.work).resolve();w.mkdir(parents=True,exist_ok=True);app=w/'TestInstall';test=w/'WorkscapeTest';test.mkdir(exist_ok=True)
setup=Path(args.setup).resolve()
si=subprocess.STARTUPINFO();si.dwFlags=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
checks=[]
for component in ['library','workspace']:
 try:
  with winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Software\\Jago Suite\\Preview\\Components\\'+component):pass
  raise RuntimeError('An installer preview is already registered. Use a clean test account to avoid replacing it.')
 except FileNotFoundError:pass
def run(args):
 p=subprocess.Popen(list(map(str,args)),startupinfo=si);code=p.wait(timeout=180);assert code==0,(args,code)
def reg(component):
 with winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Software\\Jago Suite\\Preview\\Components\\'+component) as k:return winreg.QueryValueEx(k,'Executable')[0]
run([setup,'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/TYPE=full','/DIR='+str(app),'/LOG='+str(w/'install.log')])
assert Path(reg('library'))==app/'Library-Production/Jago-Library.exe';assert Path(reg('workspace'))==app/'Jago-Workscape.exe';checks.append('per-user installed components registered')
assert (app/'Library-Production/Tools/Documents/LibreOffice/program/soffice.exe').exists();checks.append('offline renderer included in full install')
assert (app/'Jago-Workscape.exe').is_file() and (app/'Library-Production/Jago-Library.exe').is_file()
checks.append('installed executables present')
(test/'installer-only.txt').write_text('test')
run([app/'Jago-Workscape.exe','--test',test]);result=json.loads((test/'result.json').read_text(encoding='utf-8-sig'));assert result.get('ok'),result;checks+=result['checks']
sentinel=app/'my-project.txt';sentinel.write_text('preserve user-created files')
run([setup,'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/TYPE=full','/LOG='+str(w/'upgrade.log')]);assert sentinel.read_text()=='preserve user-created files';checks.append('reinstall preserves unknown user file')
run([app/'unins000.exe','/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/LOG='+str(w/'uninstall.log')]);assert sentinel.exists();assert not (app/'Jago-Workscape.exe').exists()
for c in ['library','workspace']:
 try:reg(c);raise AssertionError('registry component remained')
 except FileNotFoundError:pass
checks.append('uninstall removes app registration and preserves unknown files')
run([setup,'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/TYPE=custom','/COMPONENTS=workscape','/DIR='+str(app),'/LOG='+str(w/'workscape-only.log')]);assert (app/'Jago-Workscape.exe').exists();assert not (app/'Library-Production/Jago-Library.exe').exists();checks.append('Workscape-only selection does not install Library')
run([app/'unins000.exe','/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART'])
(w/'verification.json').write_text(json.dumps({'ok':True,'checks':checks,'installerSHA256':hashlib.sha256(setup.read_bytes()).hexdigest()},indent=2));print(json.dumps({'ok':True,'checks':checks}),flush=True)
