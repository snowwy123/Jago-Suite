from pathlib import Path
import sys
p=Path(sys.argv[1]).resolve()
rows=[]
for f in p.rglob('*'):
 if not f.is_file() or f.name=='Removal.iss':continue
 rel=str(f.relative_to(p))
 if rel.startswith('Library-Production\\Tools\\Documents\\LibreOffice\\'):comp='library\\documents'
 elif rel.startswith('Library-Production\\'):comp='library'
 elif rel=='Jago-Workscape.exe' or rel=='Workscape-LICENSE.txt' or rel.startswith('Documentation\\'):comp='workscape'
 else:continue
 if any(c in rel for c in ['"',"'",'..',';']):raise ValueError(rel)
 rows.append(f"Type: files; Name: \"{{app}}\\{rel}\"; Check: RemoveComponentFile('{comp}', '{rel}')")
(p/'Removal.iss').write_text('[InstallDelete]\n'+'\n'.join(rows)+'\n',encoding='utf-8')
print('Prepared file-specific component removal:',len(rows))
