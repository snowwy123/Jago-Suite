[Setup]
AppId=JagoExplorerThumbnails
AppName=Jago Explorer Thumbnails
AppVersion=0.1.0
AppPublisher=Cameron Jago Lis Illustrates
DefaultDirName={commonpf}\Jago Suite\ExplorerThumbnails
DisableDirPage=yes
DisableProgramGroupPage=yes
PrivilegesRequired=admin
ArchitecturesAllowed=x64os
ArchitecturesInstallIn64BitMode=x64os
UninstallDisplayName=Jago Explorer Thumbnails
WizardStyle=modern light
WizardBackColor=$E7F2F6
WizardImageBackColor=$E7F2F6
OutputDir=Output
OutputBaseFilename=Jago-Explorer-Thumbnails-Setup
Compression=lzma2
SolidCompression=yes
[Files]
Source: "Jago.ProjectThumbnails.dll"; DestDir: "{app}"; Flags: ignoreversion restartreplace uninsrestartdelete
Source: "README.txt"; DestDir: "{app}"; Flags: ignoreversion
[Registry]
Root: HKLM; Subkey: "Software\Classes\CLSID\{{97139026-28D9-4DD5-941B-29D97C0AA832}"; ValueType: string; ValueData: "Jago project thumbnails"
Root: HKLM; Subkey: "Software\Classes\CLSID\{{97139026-28D9-4DD5-941B-29D97C0AA832}\InprocServer32"; ValueType: string; ValueData: "{app}\Jago.ProjectThumbnails.dll"
Root: HKLM; Subkey: "Software\Classes\CLSID\{{97139026-28D9-4DD5-941B-29D97C0AA832}\InprocServer32"; ValueType: string; ValueName: "ThreadingModel"; ValueData: "Apartment"
[Code]
const ProviderId = '{97139026-28D9-4DD5-941B-29D97C0AA832}';
const CategoryId = '{E357FCCD-A995-4576-B01F-234630154E96}';
procedure SHChangeNotify(EventId, Flags: Integer; Item1, Item2: Integer); external 'SHChangeNotify@shell32.dll stdcall';
function ExtensionAt(I: Integer): String;
begin
 case I of 0: Result := '.jago'; 1: Result := '.jagodither'; 2: Result := '.jagorepeat'; 3: Result := '.jagoworld'; 4: Result := '.jagomaterial'; 5: Result := '.jagomusic'; 6: Result := '.jagolibrary'; 7: Result := '.jagopulse'; 8: Result := '.jago3d'; 9: Result := '.jagoworkspace'; end;
end;
procedure CurStepChanged(CurStep: TSetupStep);
var I: Integer; Key, Existing: String;
begin
 if CurStep <> ssPostInstall then exit;
 for I := 0 to 9 do begin
  Key := 'Software\Classes\' + ExtensionAt(I) + '\ShellEx\' + CategoryId;
  if not RegQueryStringValue(HKLM, Key, '', Existing) or (Existing = '') or (CompareText(Existing, ProviderId) = 0) then RegWriteStringValue(HKLM, Key, '', ProviderId);
 end;
 SHChangeNotify($08000000, 0, 0, 0);
end;
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var I: Integer; Key, Existing: String;
begin
 if CurUninstallStep <> usUninstall then exit;
 Key := 'Software\Classes\CLSID\' + ProviderId + '\InprocServer32';
 if not RegQueryStringValue(HKLM, Key, '', Existing) or (CompareText(Existing, ExpandConstant('{app}\Jago.ProjectThumbnails.dll')) <> 0) then exit;
 for I := 0 to 9 do begin
  Key := 'Software\Classes\' + ExtensionAt(I) + '\ShellEx\' + CategoryId;
  if RegQueryStringValue(HKLM, Key, '', Existing) and (CompareText(Existing, ProviderId) = 0) then RegDeleteKeyIncludingSubkeys(HKLM, Key);
 end;
 RegDeleteKeyIncludingSubkeys(HKLM, 'Software\Classes\CLSID\' + ProviderId);
 SHChangeNotify($08000000, 0, 0, 0);
end;

