from pathlib import Path
import json,urllib.request,datetime
import sys
r=Path(sys.argv[1]);repo=r/'GitHub/Jago-Library-Studio';out=r/'work/Suite-Hardening-2026-10-19';out.mkdir(parents=True,exist_ok=True)
packages=[('npm','pdfjs-dist',(repo/'Source/Vendor/pdfjs-version.txt').read_text().strip()),('npm','pdf-lib','1.17.1'),('npm','docx-preview','0.4.1'),('npm','jszip','3.10.2'),('npm','mediabunny','1.61.4'),('npm','tesseract.js','6.0.1'),('npm','tesseract.js-core','6.1.2')]
for line in (repo/'Source/PDF-Engine/requirements.txt').read_text().splitlines():
 if '==' in line:
  n,v=line.split('==');packages.append(('PyPI',n,v))
queries=[{'package':{'ecosystem':e,'name':n},'version':v} for e,n,v in packages]
request=urllib.request.Request('https://api.osv.dev/v1/querybatch',data=json.dumps({'queries':queries}).encode(),headers={'Content-Type':'application/json'},method='POST')
try:
 data=json.load(urllib.request.urlopen(request,timeout=60));result={'date':'2026-10-19','service':'https://api.osv.dev/v1/querybatch','scope':'Exact declared package versions only; not all native/transitive components or exploitability. Empty results are not a security guarantee.','packages':[dict(ecosystem=e,name=n,version=v,advisories=entry.get('vulns',[]))for (e,n,v),entry in zip(packages,data['results'])]}
except Exception as ex:result={'date':'2026-10-19','error':str(ex),'queries':queries}
(out/'dependency-advisories.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
