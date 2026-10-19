"""Exercise a full installer using only the isolated setup AppId and a fresh work directory."""
from pathlib import Path
import argparse,subprocess,os,json,time,hashlib,winreg
parser=argparse.ArgumentParser();parser.add_argument('--setup',required=True);parser.add_argument('--snapshot',required=True);parser.add_argument('--output',required=True);parser.add_argument('--payload');args=parser.parse_args()
base=Path(r'C:\Jago Studio Dev');setup=Path(args.setup).resolve();snapshot=Path(args.snapshot).resolve();out=Path(args.output).resolve()
assert 'Isolated-Test' in setup.name and setup.is_file(),'Use the isolated installer only'
assert out.is_relative_to(base/'work') and not out.exists(),'Choose a fresh isolated work directory'
try:
 with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Uninstall\JagoSuiteSavepointTest_is1'):raise RuntimeError('An earlier isolated test is registered; inspect it before continuing.')
except FileNotFoundError:pass
out.mkdir(parents=True);target=out/'Installed';payload=Path(args.payload).resolve() if args.payload else snapshot/'Installer-payload';manifest=json.loads((snapshot/'Snapshot-manifest.json').read_text(encoding='utf-8'));checks=[];native=[]
si=subprocess.STARTUPINFO();si.dwFlags=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def public_state():
 result={}
 for channel in ['Preview','Stable','Installed']:
  for key in ['workspace','wobble','dither','repeat','worldbuilding','material','music','library','companion','pulse']:
   try:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Software\\Jago Suite\\'+channel+'\\Components\\'+key) as h:result[channel+'/'+key]=winreg.QueryValueEx(h,'Executable')[0]
   except FileNotFoundError:pass
 prefs=Path(os.environ['LOCALAPPDATA'])/'Jago Companion Preview/preferences.json'
 result['companionPreferences']=sha(prefs) if prefs.exists() else None
 return result
before=public_state()
def check(ok,name):
 assert ok,name
 checks.append(name);print(name,flush=True)
def run(*options,success=True):
 log=out/('setup-'+str(len(checks))+'.log')
 result=subprocess.run([str(setup),'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/SP-','/DIR='+str(target),'/LOG='+str(log),*options],startupinfo=si,timeout=300)
 assert (result.returncode==0)==success,(result.returncode,options,str(log))
def verify_apps(names):
 for component in manifest['components']:
  if component['name'] not in names:continue
  for name,digest in component['appHashes'].items():assert sha(target/component['folder']/name)==digest,(component['name'],name)
def env(folder):return {**os.environ,'JAGO_SUITE_ROOT':str(folder/'Suite'),'JAGO_PREVIEW_CACHE':str(folder/'PreviewCache')}
def json_result(path):
 data=json.loads(path.read_text(encoding='utf-8-sig'))
 return json.loads(data) if isinstance(data,str) else data
try:
 run('/TYPE=custom','/COMPONENTS=workscape,music,companion,pulse,library','/TASKS=boardshortcut')
 verify_apps(['Workscape','Sound','Companion','Pulse','Library']);check(not (target/'Wobble/Jago-Wobble.exe').exists(),'Selected installation contains exact current apps and all Companion preview DLLs')
 group=Path(os.environ['APPDATA'])/'Microsoft/Windows/Start Menu/Programs/Jago Suite Isolated Test'
 check((group/'Jago Capture.lnk').exists() and (group/'Jago Board.lnk').exists() and not (group/'Jago Preview.lnk').exists(),'Capture and optional Board shortcuts exist; Preview has no separate launcher')
 sentinel=target/'Companion/My retained note.txt';sentinel.write_text('Keep my personal addition',encoding='utf-8')
 run();verify_apps(['Workscape','Sound','Companion','Pulse','Library']);check(not (target/'Wobble/Jago-Wobble.exe').exists() and sentinel.read_text()=='Keep my personal addition','Update remembers selection and retains personal additions')
 wrong=out/'WrongLocation';run('/DIR='+str(wrong),'/TYPE=custom','/COMPONENTS=music','/TASKS=',success=False);check(not (wrong/'Music-SFX/Jago-Sound.exe').exists(),'Wrong-location update is refused')
 run('/TYPE=full','/TASKS=boardshortcut');verify_apps([x['name'] for x in manifest['components']])
 check((target/'Library-Production/Tools/Documents/LibreOffice/program/soffice.exe').exists() and (target/'Pulse/Transcription/whisper-cli.exe').exists(),'Full installs all ten apps, Office rendering and the offline lyric engine/model')
 for rel,item in manifest['files'].items():assert sha(target/rel)==item['sha256'],rel
 check(True,'Every full-install payload file matches its staged SHA-256')
 sound=out/'Native-Sound';sound.mkdir();repo=base/'GitHub/Jago-Sound-Studio';code='window.soundOriginalFixture='+(repo/'Source/Tests/0.9/original-bank-fixture.json').read_text(encoding='utf-8')+';\n'+(repo/'Source/Native-probes/sound-refresher.js').read_text(encoding='utf-8')
 (sound/'probe.js').write_text(code,encoding='utf-8');subprocess.run([str(target/'Music-SFX/Jago-Sound.exe'),'--test',str(sound)],env=env(sound),startupinfo=si,timeout=120,check=True);data=json_result(sound/'result.json');check(data.get('ok'),'Installed Sound passes generation coordination, editing, Undo and save/reopen checks');native.append({'app':'Sound','checks':len(data.get('checks',[]))})
 pulse=out/'Native-Pulse';pulse.mkdir();subprocess.run([str(target/'Pulse/Jago-Pulse.exe'),'--check',str(pulse)],env=env(pulse),startupinfo=si,timeout=90,check=True);data=json_result(pulse/'native-result.json');check(data.get('ok'),'Installed Pulse starts with current visual/text/export systems');native.append({'app':'Pulse','result':data})
 phrase=base/'work/Pulse/Speech-verification/phrase.wav'
 if phrase.exists():
  speech=out/'Native-Lyrics';speech.mkdir();(speech/'speech-check.json').write_text(json.dumps({'audio':str(phrase)}),encoding='utf-8');subprocess.run([str(target/'Pulse/Jago-Pulse.exe'),'--speech-check',str(speech)],env=env(speech),startupinfo=si,timeout=120,check=True);data=json_result(speech/'native-speech.json');check(data.get('ok') and Path(data['executable']).parent==target/'Pulse/Transcription' and 'music' in data.get('srt','').lower(),'Installed optional lyric engine produces timed text from synthetic local speech')
 workspace=out/'Native-Workscape';workspace.mkdir();subprocess.run([str(target/'Jago-Workscape.exe'),'--test',str(workspace)],env=env(workspace),startupinfo=si,timeout=240,check=True);data=json_result(workspace/'result.json');check(data.get('ok'),'Installed Workscape passes native tab, recovery, theme and detach/reattach checks');native.append({'app':'Workscape','checks':len(data.get('checks',[]))})
 run('/TYPE=compact','/TASKS=boardshortcut');verify_apps([x['name'] for x in manifest['components']]);check(not (target/'Library-Production/Tools/Documents/LibreOffice/program/soffice.exe').exists() and not (target/'Pulse/Transcription/whisper-cli.exe').exists() and (target/'Library-Production/Tools/PDF/Jago-PDF-Engine.exe').exists(),'Compact removes optional Office/lyric tools while keeping every app and PDF/OCR')
 run('/TYPE=custom','/COMPONENTS=music','/TASKS=');check(not (target/'Companion/Jago-Companion.exe').exists() and not (target/'Companion/Microsoft.Web.WebView2.Core.dll').exists() and sentinel.read_text()=='Keep my personal addition' and (target/'Music-SFX/Jago-Sound.exe').exists(),'Deselecting Companion removes owned helper/runtime files and retains personal files and Sound')
 subprocess.run([str(target/'unins000.exe'),'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/LOG='+str(out/'uninstall.log')],startupinfo=si,timeout=240,check=True)
 for i in range(100):
  if not (target/'Music-SFX/Jago-Sound.exe').exists():break
  time.sleep(.1)
 check(not (target/'Music-SFX/Jago-Sound.exe').exists() and sentinel.read_text()=='Keep my personal addition','Uninstall removes owned app files and preserves the personal sentinel')
 check(public_state()==before,'The real installation registrations and Companion preferences remain unchanged')
 result={'ok':True,'checks':checks,'native':native,'installerVersion':manifest.get('suiteVersion','0.3.8'),'isolatedAppId':'JagoSuiteSavepointTest'}
except Exception as error:
 result={'ok':False,'error':repr(error),'checks':checks,'native':native};(out/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8');raise
(out/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True)
