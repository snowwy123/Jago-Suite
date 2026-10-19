from pathlib import Path
import subprocess,json,re,sys
suite=Path(__file__).resolve().parents[2];root=Path(sys.argv[1]).resolve();root.mkdir(parents=True,exist_ok=True)
for name,sha in json.loads(Path(__file__).with_name('matrix-revisions.json').read_text()).items():
 if not re.fullmatch(r'Jago-(?:Wobble-Studio|Dither-Studio|Repeat-Studio|World-Studio|Material-Studio|Sound-Studio|Library-Studio|Pulse-Studio|Workscape|Companion)',name) or not re.fullmatch(r'(?:[0-9a-f]{40}|v[0-9]+\.[0-9]+\.[0-9]+)',sha):raise ValueError('Invalid revision manifest')
 dest=root/name
 if dest.exists():raise ValueError('Use a fresh checkout directory: '+str(dest))
 subprocess.run(['git','init',str(dest)],check=True)
 subprocess.run(['git','-C',str(dest),'remote','add','origin','https://github.com/snowwy123/'+name+'.git'],check=True)
 subprocess.run(['git','-C',str(dest),'fetch','--depth=1','origin',sha],check=True)
 subprocess.run(['git','-C',str(dest),'checkout','--detach','FETCH_HEAD'],check=True)
