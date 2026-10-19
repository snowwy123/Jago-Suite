from pathlib import Path
import argparse,json,subprocess,shutil
a=argparse.ArgumentParser();a.add_argument('--payload',required=True);a.add_argument('--output',required=True);a.add_argument('--version',default='0.3.8');a.add_argument('--test',action='store_true');a.add_argument('--release-branding',action='store_true');args=a.parse_args()
repo=Path(r'C:\Jago Studio Dev\GitHub\Jago-Suite'); payload=Path(args.payload).resolve();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
specs=[('workscape','Workscape','','Bring studios together in tabs and side-by-side views'),('wobble','Wobble','Wobble','Draw and animate illustrations'),('dither','Dither','Dither','Dithering, palettes and print effects'),('repeat','Repeat','Repeat','Build seamless repeating patterns'),('worldbuilding','World','Worldbuilding','Maps, characters and worldbuilding'),('material','Material','Material','Procedural textures and surface materials'),('music','Sound','Music-SFX','Compose music and create sound effects'),('library','Library','Library-Production','Assets, fonts, boards, layouts and document tools'),('companion','Companion','Companion','Quick notes, sticky tasks and screen captures'),('pulse','Pulse','Pulse','Music-driven films and procedural visuals')]
def quote(s):return s.replace('"','""')
def relapp(name,folder):return (folder+'\\' if folder else '')+'Jago-'+name+'.exe'
appid='JagoSuiteSavepointTest' if args.test else 'JagoSuiteInstallerPreview'; channel='SavepointTest' if args.test else 'Preview'
group='Jago Suite Isolated Test' if args.test else 'Jago Suite Preview'
iss=['[Setup]',f'AppId={appid}',f'AppName={group}',f'AppVersion={args.version}','AppPublisher=Cameron Jago Lis Illustrates','AppPublisherURL=https://jagosuite.co.uk/',f'DefaultDirName={{localappdata}}\\Programs\\{group}',f'DefaultGroupName={group}','PrivilegesRequired=lowest','ArchitecturesAllowed=x64compatible','ArchitecturesInstallIn64BitMode=x64compatible','DisableProgramGroupPage=yes','DisableWelcomePage=no','UsePreviousAppDir=yes','UsePreviousTasks=yes','UsePreviousSetupType=yes','WizardStyle=modern light','WizardSizePercent=120',f'WizardImageFile={repo}/Installer/Brand/wizard.bmp',f'WizardSmallImageFile={repo}/Installer/Brand/small.bmp','WizardImageStretch=yes','WizardImageBackColor=$E7F2F6','WizardBackColor=$E7F2F6',f'SetupIconFile={repo}/Installer/Brand/setup.ico','UninstallDisplayIcon={app}\\Branding\\setup.ico',f'OutputDir={out}',f'OutputBaseFilename=Jago-Suite-Setup-{"Isolated-Test" if args.test else "Preview"}','Compression=zip','SolidCompression=no','CloseApplications=yes','RestartApplications=no','[Types]','Name: full; Description: "All studios, Companion and optional offline tools"','Name: compact; Description: "All studios and Companion; without Office renderer or lyric model"','Name: custom; Description: "Choose individual apps and tools"; Flags: iscustom','[Components]']
for key,name,folder,benefit in specs:
 iss.append(f'Name: "{key}"; Description: "{name} - {benefit}"; Types: full compact')
 if key=='library':
  for child,title,types in [('documents','Office previews - view Word, Excel and PowerPoint offline (larger disk footprint)','full'),('pdf','PDF engine - reconstruct and export PDFs offline','full compact'),('ocr','OCR - recognise text in scanned documents offline','full compact')]:iss.append(f'Name: "library\\{child}"; Description: "{title}"; Types: {types}')
 if key=='pulse' and (payload/'Pulse/Transcription').exists():
  for required in ['whisper-cli.exe','whisper.dll','ggml.dll','ggml-base.dll','ggml-tiny.en.bin','whisper.cpp-LICENSE.txt','Whisper-model-LICENSE.txt']:
   if not (payload/'Pulse/Transcription'/required).is_file():raise ValueError('Incomplete transcription pack: '+required)
  iss.append('Name: "pulse\\transcription"; Description: "Offline lyric transcription - English starter engine and model; drafts words from your music, no uploads"; Types: full')
iss+=['[Tasks]','Name: desktop; Description: "Desktop shortcuts for your selected apps"; Flags: unchecked']
if not args.test:
 pilotText=(repo/'Installer/pilot.iss').read_text(encoding='utf-8-sig')
 iss += [line for line in pilotText.split('[Tasks]\n')[1].split('[Files]')[0].splitlines() if 'Name: "desktop"' not in line]
iss+=['Name: boardshortcut; Description: "Jago Board shortcut - open Library reference boards directly from Start"; Components: library; Flags: unchecked']
iss+=['[Files]']
owned=[]
for f in sorted(payload.rglob('*')):
 if not f.is_file():continue
 rel=str(f.relative_to(payload));top=rel.split('\\')[0];comp=next((k for k,n,folder,b in specs if folder and top==folder),None)
 if rel.startswith('Library-Production\\Tools\\Documents\\'):comp='library\\documents'
 if rel.startswith('Library-Production\\Tools\\PDF\\'):comp='library\\pdf'
 if rel.startswith('Library-Production\\Tools\\OCR\\'):comp='library\\ocr'
 if rel.startswith('Pulse\\Transcription\\'):comp='pulse\\transcription'
 if rel in ['Jago-Workscape.exe','Workscape-LICENSE.txt'] or rel.startswith('Documentation\\Workscape\\'):comp='workscape'
 dest=str(Path(rel).parent); dest='' if dest=='.' else '\\'+dest
 iss.append(f'Source: "{quote(str(f))}"; DestDir: "{{app}}{dest}"; Flags: ignoreversion'+(f'; Components: "{comp}"' if comp else ''))
 if comp:owned.append((comp,rel))
iss+=['[InstallDelete]']
for comp,rel in owned:
 if "'" in rel or '"' in rel:raise ValueError(rel)
 iss.append(f'Type: files; Name: "{{app}}\\{rel}"; Check: RemoveComponentFile(\'{comp}\', \'{rel}\')')
iss+=['[Icons]']
for key,name,folder,benefit in specs:
 exe=relapp(name,folder);iss.append(f'Name: "{{group}}\\Jago {name}"; Filename: "{{app}}\\{exe}"; Components: {key}')
 iss.append(f'Name: "{{userdesktop}}\\Jago {name} Preview"; Filename: "{{app}}\\{exe}"; Components: {key}; Tasks: desktop')
iss+=['Name: "{group}\\Jago Capture"; Filename: "{app}\\Companion\\Jago-Capture.exe"; Components: companion; AppUserModelID: "Jago.Capture"','Name: "{userdesktop}\\Jago Capture Preview"; Filename: "{app}\\Companion\\Jago-Capture.exe"; Components: companion; Tasks: desktop; AppUserModelID: "Jago.Capture"']
iss+=['Name: "{group}\\Jago Board"; Filename: "{app}\\Library-Production\\Jago-Board.exe"; Components: library; Tasks: boardshortcut; AppUserModelID: "Jago.Board"']
iss+=['Name: "{group}\\Uninstall Jago Suite Preview"; Filename: "{uninstallexe}"','[Registry]']
for key,name,folder,benefit in specs:
 registry='workspace' if key=='workscape' else key
 iss.append(f'Root: HKCU; Subkey: "Software\\Jago Suite\\{channel}\\Components\\{registry}"; ValueType: string; ValueName: Executable; ValueData: "{{app}}\\{relapp(name,folder)}"; Components: {key}; Flags: uninsdeletekey')
iss+=['[Run]','Filename: "{app}\\Companion\\Jago-Capture.exe"; Parameters: "--register'+(' --test-shell' if args.test else '')+'"; Components: companion; Flags: runhidden','Filename: "{app}\\Library-Production\\Jago-Board.exe"; Parameters: "--register'+(' --test-shell' if args.test else '')+'"; Components: library; Flags: runhidden','Filename: "{app}\\Jago-Preview-Launcher.exe"; Parameters: "{code:LaunchArguments}"; Description: "Open Jago Workscape"; Check: HasWorkscape; Flags: postinstall nowait skipifsilent','Filename: "{app}\\Jago-Preview-Launcher.exe"; Parameters: "{code:LaunchArguments}"; Description: "Open selected apps in separate windows"; Check: NoWorkscape; Flags: postinstall nowait skipifsilent unchecked','[Code]','var LyricsInfoPage: TOutputMsgWizardPage;','function PathAttributes(Name: String): LongWord; external \'GetFileAttributesW@kernel32.dll stdcall\';']
if not args.test:
 associations=[line for line in pilotText.split('[Registry]\n')[1].split('[Run]')[0].splitlines() if 'Software\\Classes' in line]
 at=iss.index('[Run]');iss[at:at]=associations
pilot=(repo/'Installer/pilot.iss').read_text(encoding='utf-8-sig');start=pilot.index('function RemoveComponentFile');end=pilot.index('function NextButtonClick',start);iss.append(pilot[start:end])
selected=' or '.join(f"WizardIsComponentSelected('{k}')" for k,n,f,b in specs)
iss.append('function PrepareToInstall(var NeedsRestart: Boolean): String;\nvar Existing, Version: String;\nbegin\n Result := \'\';')
iss.append(f" if not ({selected}) then begin Result := 'Choose at least one app. Use Windows Apps to uninstall everything.'; exit; end;")
iss.append(f" if RegQueryStringValue(HKCU, 'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{appid}_is1', 'InstallLocation', Existing) and DirExists(Existing) and (CompareText(RemoveBackslashUnlessRoot(Existing),RemoveBackslashUnlessRoot(ExpandConstant('{{app}}'))) <> 0) then begin Result := 'Update this preview at '+Existing+', or uninstall it before choosing another location. Personal files are kept.'; exit; end;")
if not args.test:
 iss.append(" if WizardIsComponentSelected('companion') and RegQueryStringValue(HKCU, 'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\JagoCompanionPreview_is1', 'InstallLocation', Existing) and DirExists(Existing) then begin Result := 'Companion has a separate preview installation at '+Existing+'. Untick Companion to keep using it, or uninstall that preview first to let this suite installer manage Companion. Notes and captures are kept.'; exit; end;")
iss.append(" if not ((RegQueryStringValue(HKLM32, 'Software\\Microsoft\\EdgeUpdate\\Clients\\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', Version) and (Version<>'') and (Version<>'0.0.0.0')) or (RegQueryStringValue(HKCU, 'Software\\Microsoft\\EdgeUpdate\\Clients\\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', Version) and (Version<>'') and (Version<>'0.0.0.0'))) then Result := 'Install Microsoft Edge WebView2 Evergreen Runtime, then run setup again.';\nend;")
iss.append("procedure InitializeWizard();\nbegin\n WizardForm.WelcomeLabel1.Caption := 'Your creative tools, your selection.';\n WizardForm.WelcomeLabel2.Caption := 'Install any single app or the complete suite. Tick apps to add them; untick installed apps to remove their program files.'+#13#10+#13#10+'Personal projects, notes, captures and linked folders are kept. Setup can open Workscape at the end; it will not preload all your studios. Save work and close your apps before continuing.';\n LyricsInfoPage := CreateOutputMsgPage(wpSelectComponents, 'Offline lyric transcription', 'What the optional Pulse component adds', 'Draft English words and timings from imported music.'+#13#10+''+#13#10+'Includes the whisper.cpp engine, compact English model and required Microsoft runtime files (about 86 MiB). Support files stay beside the engine; no system files are replaced.'+#13#10+''+#13#10+'Works offline with no account or uploads. Runs only when requested, and stops when finished or cancelled. No background service is installed.'+#13#10+''+#13#10+'Singing, names and busy recordings can be inaccurate. Review the draft words and timing. This does not separate a vocal track.'+#13#10+''+#13#10+'After setup, restart Pulse. Add music, open Words & lyrics and choose Transcribe this music locally.'+#13#10+''+#13#10+'Untick this component under Pulse to leave it out, or add/remove it later through setup. Manual words and timed-text import work without it.');\nend;")
iss.append("function HasWorkscape(): Boolean;\nvar Path: String;\nbegin Result := WizardIsComponentSelected('workscape') or FileExists(ExpandConstant('{app}\\Jago-Workscape.exe'));")
if not args.test:
 for ch in ['Preview','Stable']:iss.append("if not Result then if RegQueryStringValue(HKCU, 'Software\\Jago Suite\\"+ch+"\\Components\\workspace', 'Executable', Path) then Result := FileExists(Path);")
iss.append("end;\nfunction NoWorkscape(): Boolean;\nbegin Result := not HasWorkscape(); end;")
iss.append("function LaunchArguments(Param: String): String;\nbegin Result := '"+('--isolated-no-registry' if args.test else '')+"';")
for key,name,folder,benefit in specs:iss.append(f"if WizardIsComponentSelected('{key}') then Result := Result+' {key}';")
iss.append("end;")
iss.append('procedure CurStepChanged(CurStep: TSetupStep);\nvar Existing: String;\nbegin\n if CurStep<>ssPostInstall then exit;')
if not args.test:
 for comp,task,ext,progid in [('library','libraryfiles','.jagolibrary','JagoPreview.Library'),('workscape','workspacefiles','.jagoworkspace','JagoPreview.Workscape'),('library','pdf','.pdf','JagoPreview.PDF')]:
  iss.append(f"if not WizardIsComponentSelected('{comp}') or not WizardIsTaskSelected('{task}') then begin RegDeleteValue(HKCU,'Software\\Classes\\{ext}\\OpenWithProgids','{progid}'); RegDeleteKeyIncludingSubkeys(HKCU,'Software\\Classes\\{progid}'); end;")
for key,name,folder,benefit in specs:
 registry='workspace' if key=='workscape' else key; path=relapp(name,folder)
 iss.append(f"if not WizardIsComponentSelected('{key}') then begin\n if RegQueryStringValue(HKCU, 'Software\\Jago Suite\\{channel}\\Components\\{registry}', 'Executable', Existing) and (CompareText(Existing, ExpandConstant('{{app}}\\{path}'))=0) then RegDeleteKeyIncludingSubkeys(HKCU, 'Software\\Jago Suite\\{channel}\\Components\\{registry}');\n DeleteFile(ExpandConstant('{{group}}\\Jago {name}.lnk')); end;")
 iss.append(f"if not WizardIsComponentSelected('{key}') or not WizardIsTaskSelected('desktop') then DeleteFile(ExpandConstant('{{userdesktop}}\\Jago {name} Preview.lnk'));")
iss.append("if not WizardIsComponentSelected('companion') then DeleteFile(ExpandConstant('{group}\\Jago Capture.lnk'));")
iss.append("if not WizardIsComponentSelected('companion') or not WizardIsTaskSelected('desktop') then DeleteFile(ExpandConstant('{userdesktop}\\Jago Capture Preview.lnk'));")
iss.append("if not WizardIsComponentSelected('library') or not WizardIsTaskSelected('boardshortcut') then DeleteFile(ExpandConstant('{group}\\Jago Board.lnk'));")
iss+=['end;','procedure RegisterExtraCloseApplicationsResources();','begin']
for key,name,folder,benefit in specs:iss.append(f"RegisterExtraCloseApplicationsResource(ExpandConstant('{{app}}\\{relapp(name,folder)}'));")
for extra in ['Companion/Jago-Capture.exe','Companion/Jago-Recorder.exe','Companion/Jago-Preview.exe','Companion/Jago-Update.exe','Library-Production/Jago-Board.exe']:iss.append("RegisterExtraCloseApplicationsResource(ExpandConstant('{app}\\"+extra.replace('/','\\')+"'));")
iss+=['end;',"function UpdateReadyMemo(Space, NewLine, U, D, T, C, G, Tasks: String): String;\nbegin Result := D+NewLine+NewLine+C+NewLine+NewLine+Tasks+NewLine+NewLine+'Unchecked installed components will have their known program files removed. Projects, linked folders, notes and personal settings are kept.'; end;"]
iss.append("function ShouldSkipPage(PageID: Integer): Boolean;\nbegin Result := False; if LyricsInfoPage <> nil then if PageID = LyricsInfoPage.ID then Result := not WizardIsComponentSelected('pulse\\transcription'); end;")
if args.test:iss=[line.replace('AppUserModelID: "Jago.Capture"','AppUserModelID: "Jago.Test.Installer.Capture"').replace('AppUserModelID: "Jago.Board"','AppUserModelID: "Jago.Test.Installer.Board"') for line in iss]
if args.release_branding:
 iss=[line.replace('Jago Suite Preview','Jago Suite').replace('Jago-Preview-Launcher.exe','Jago-Suite-Launcher.exe').replace(' Preview\"','\"').replace(' Preview.lnk','.lnk').replace('Update this preview at ','Update this installation at ') for line in iss]
 if not args.test:iss=[line.replace('OutputBaseFilename=Jago-Suite-Setup-Preview','OutputBaseFilename=Jago-Suite-Setup-v'+args.version) for line in iss]
script=out/'full-suite.iss';script.write_text('\n'.join(iss),encoding='utf-8-sig')
subprocess.run([r'C:\Jago Studio Dev\work\Installer-Pilot\Compiler\ISCC.exe',str(script)],check=True,stdout=(out/'compiler.log').open('w',encoding='utf-8'),stderr=subprocess.STDOUT)
print('Built '+str(out))

