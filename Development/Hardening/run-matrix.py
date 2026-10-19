from pathlib import Path
import subprocess,json,sys,os,time
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True);rows=[]
for repo in sorted(root.iterdir()):
 if not repo.is_dir() or not repo.name.startswith('Jago-'):continue
 build=repo/'Build.ps1'
 if build.exists():
  t=time.monotonic();p=subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(build)],cwd=repo,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=240);(out/(repo.name+'-build.log')).write_text(p.stdout+p.stderr,encoding='utf-8');rows.append({'repository':repo.name,'task':'build','ok':p.returncode==0,'seconds':round(time.monotonic()-t,3)})
  if p.returncode:print(p.stdout+p.stderr)
 tests=[str(repo/n)for n in subprocess.check_output(['git','-C',str(repo),'ls-files'],text=True).splitlines()if n.endswith('.test.cjs')]
 if tests:
  p=subprocess.run(['node','--test',*tests],cwd=repo,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180);(out/(repo.name+'-models.log')).write_text(p.stdout+p.stderr,encoding='utf-8');rows.append({'repository':repo.name,'task':'model tests','ok':p.returncode==0});print(p.stdout+p.stderr)
for row in rows:print(json.dumps(row))
(out/'matrix-results.json').write_text(json.dumps({'os':os.environ.get('RUNNER_OS',os.name),'arch':os.environ.get('RUNNER_ARCH','local'),'results':rows},indent=2),encoding='utf-8')
assert all(row['ok']for row in rows),'One or more build/model checks failed'
