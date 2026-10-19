#ifndef Payload
  #error Define Payload to the prepared pilot files
#endif
#ifndef Output
  #define Output "Output"
#endif
[Setup]
AppId=JagoSuiteInstallerPreview
AppName=Jago Suite Preview
AppVersion=0.2.0
AppPublisher=Cameron Jago Lis Illustrates
AppPublisherURL=https://jagosuite.co.uk/
DefaultDirName={localappdata}\Programs\Jago Suite Preview
DefaultGroupName=Jago Suite Preview
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
DisableWelcomePage=no
UsePreviousAppDir=yes
UsePreviousTasks=yes
UsePreviousSetupType=yes
WizardStyle=modern light
WizardSizePercent=120
WizardImageFile=Brand\wizard.bmp
WizardSmallImageFile=Brand\small.bmp
WizardImageStretch=yes
WizardImageBackColor=$E7F2F6
WizardBackColor=$E7F2F6
SetupIconFile=Brand\setup.ico
UninstallDisplayIcon={app}\Brand\setup.ico
OutputDir={#Output}
OutputBaseFilename=Jago-Library-Workscape-Setup-Preview
Compression=zip
SolidCompression=no
CloseApplications=yes
RestartApplications=no
UninstallDisplayName=Jago Suite Preview
ChangesAssociations=yes
[Types]
Name: "full"; Description: "Library and Workscape, with offline document tools"
Name: "compact"; Description: "Library and Workscape, without the larger document renderer"
Name: "custom"; Description: "Choose your tools"; Flags: iscustom
[Components]
Name: "workscape"; Description: "Workscape - use your studios in tabs or side by side"; Types: full compact
Name: "library"; Description: "Library - organise assets, preview fonts and build creative projects"; Types: full compact
Name: "library\documents"; Description: "Office previews - render Word, Excel and PowerPoint pages offline"; Types: full
[Tasks]
Name: "desktop"; Description: "Desktop shortcuts - open your tools straight from the desktop"; Flags: unchecked
Name: "libraryfiles"; Description: "Library project files - open saved collections from Explorer"; Components: library; Flags: unchecked
Name: "workspacefiles"; Description: "Workscape project files - reopen your saved set of studio tabs"; Components: workscape; Flags: unchecked
Name: "pdf"; Description: "PDF Open with - read PDFs in Library; keeps your current default"; Components: library; Flags: unchecked
[Files]
Source: "{#Payload}\Jago-Workscape.exe"; DestDir: "{app}"; Components: workscape; Flags: ignoreversion
Source: "{#Payload}\Workscape-LICENSE.txt"; DestDir: "{app}"; Components: workscape
Source: "{#Payload}\Documentation\*"; DestDir: "{app}\Documentation"; Components: workscape; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "{#Payload}\installer-preview.txt"; DestDir: "{app}"
Source: "Brand\setup.ico"; DestDir: "{app}\Brand"
Source: "{#Payload}\Library-Production\*"; DestDir: "{app}\Library-Production"; Excludes: "Tools\Documents\LibreOffice\*"; Components: library; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "{#Payload}\Library-Production\Tools\Documents\LibreOffice\*"; DestDir: "{app}\Library-Production\Tools\Documents\LibreOffice"; Components: library\documents; Flags: recursesubdirs createallsubdirs ignoreversion
[Icons]
Name: "{group}\Jago Workscape Preview"; Filename: "{app}\Jago-Workscape.exe"; Components: workscape
Name: "{group}\Jago Library Preview"; Filename: "{app}\Library-Production\Jago-Library.exe"; Components: library
Name: "{group}\Uninstall Jago Suite Preview"; Filename: "{uninstallexe}"
Name: "{userdesktop}\Jago Workscape Preview"; Filename: "{app}\Jago-Workscape.exe"; Components: workscape; Tasks: desktop
Name: "{userdesktop}\Jago Library Preview"; Filename: "{app}\Library-Production\Jago-Library.exe"; Components: library; Tasks: desktop
[Registry]
Root: HKCU; Subkey: "Software\Jago Suite\Preview\Components\library"; ValueType: string; ValueName: "Executable"; ValueData: "{app}\Library-Production\Jago-Library.exe"; Components: library; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Jago Suite\Preview\Components\workspace"; ValueType: string; ValueName: "Executable"; ValueData: "{app}\Jago-Workscape.exe"; Components: workscape; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\JagoPreview.Library"; ValueType: string; ValueData: "Jago Library project"; Tasks: libraryfiles; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\JagoPreview.Library\shell\open\command"; ValueType: string; ValueData: """{app}\Library-Production\Jago-Library.exe"" ""%1"""; Tasks: libraryfiles
Root: HKCU; Subkey: "Software\Classes\.jagolibrary\OpenWithProgids"; ValueType: string; ValueName: "JagoPreview.Library"; Tasks: libraryfiles; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\JagoPreview.Workscape"; ValueType: string; ValueData: "Jago Workscape project"; Tasks: workspacefiles; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\JagoPreview.Workscape\shell\open\command"; ValueType: string; ValueData: """{app}\Jago-Workscape.exe"" ""%1"""; Tasks: workspacefiles
Root: HKCU; Subkey: "Software\Classes\.jagoworkspace\OpenWithProgids"; ValueType: string; ValueName: "JagoPreview.Workscape"; Tasks: workspacefiles; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\JagoPreview.PDF"; ValueType: string; ValueData: "Jago Library PDF"; Tasks: pdf; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\JagoPreview.PDF\shell\open\command"; ValueType: string; ValueData: """{app}\Library-Production\Jago-Library.exe"" ""%1"""; Tasks: pdf
Root: HKCU; Subkey: "Software\Classes\.pdf\OpenWithProgids"; ValueType: string; ValueName: "JagoPreview.PDF"; Tasks: pdf; Flags: uninsdeletevalue
[Run]
Filename: "{app}\Jago-Workscape.exe"; Parameters: "{code:SelectedStudioArguments}"; Description: "Open selected studios together in Workscape"; Components: workscape; Check: WantTabs; Flags: postinstall nowait skipifsilent
Filename: "{app}\Jago-Workscape.exe"; Description: "Open Workscape separately"; Components: workscape; Check: WantSeparate; Flags: postinstall nowait skipifsilent
Filename: "{app}\Library-Production\Jago-Library.exe"; Description: "Open Library separately"; Components: library; Check: WantSeparate; Flags: postinstall nowait skipifsilent
#include Payload + "\Removal.iss"
[Code]
var LaunchPage: TInputOptionWizardPage;
function WantTabs(): Boolean;
begin Result := WizardIsComponentSelected('workscape') and LaunchPage.Values[0]; end;
function WantSeparate(): Boolean;
begin Result := not WantTabs(); end;
function SelectedStudioArguments(Param: String): String;
begin if WizardIsComponentSelected('library') then Result := '--open-studios library' else Result := ''; end;
function PathAttributes(Name: String): LongWord; external 'GetFileAttributesW@kernel32.dll stdcall';
function RemoveComponentFile(Component, Relative: String): Boolean;
var Folder, Base: String;
begin
  Result := not WizardIsComponentSelected(Component);
  if not Result then exit;
  Base := RemoveBackslashUnlessRoot(ExpandConstant('{app}'));
  Folder := ExtractFileDir(Base+'\'+Relative);
  while Length(Folder) >= Length(Base) do begin
    if (PathAttributes(Folder) <> $FFFFFFFF) and ((PathAttributes(Folder) and $400) <> 0) then RaiseException('An installed folder is a junction. Restore a regular program folder before modifying this installation.');
    if CompareText(Folder,Base) = 0 then break;
    Folder := ExtractFileDir(Folder);
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  if (CurPageID = wpSelectComponents) and not WizardIsComponentSelected('library') and not WizardIsComponentSelected('workscape') then begin
    MsgBox('Choose Library, Workscape, or both to continue.', mbInformation, MB_OK);
    Result := False;
  end;
end;
function PrepareToInstall(var NeedsRestart: Boolean): String;
var Version, Existing: String;
begin
  Result := '';
  if RegQueryStringValue(HKCU, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\JagoSuiteInstallerPreview_is1', 'InstallLocation', Existing) then begin
    if DirExists(Existing) and (CompareText(RemoveBackslashUnlessRoot(Existing),RemoveBackslashUnlessRoot(ExpandConstant('{app}'))) <> 0) then begin
      Result := 'This preview is already installed at '+Existing+'. Update it there, or uninstall the preview before choosing another location. Personal projects and settings are kept.';
      exit;
    end;
  end;
  if not WizardIsComponentSelected('library') and not WizardIsComponentSelected('workscape') then begin
    Result := 'Choose Library, Workscape, or both. Use Windows Apps to uninstall everything.';
    exit;
  end;
  if not ((RegQueryStringValue(HKLM32, 'Software\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', Version) and (Version <> '') and (Version <> '0.0.0.0')) or
    (RegQueryStringValue(HKCU, 'Software\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', Version) and (Version <> '') and (Version <> '0.0.0.0'))) then
    Result := 'Microsoft Edge WebView2 Runtime is needed to open the Windows apps. Install the Evergreen Runtime from https://developer.microsoft.com/microsoft-edge/webview2/ and run this setup again. Library also includes an offline HTML edition.';
end;
procedure InitializeWizard();
begin
  LaunchPage := CreateInputOptionPage(wpSelectTasks, 'How would you like to start?', 'Open together or use separate windows', 'Workscape opens your selected studios as tabs. Separate windows keep each studio independent. The finish page lets you choose whether to open them now.', True, False);
  LaunchPage.Add('Open all selected studios in Workscape');
  LaunchPage.Add('Open selected tools as separate windows');
  LaunchPage.Values[0] := True;
  WizardForm.WelcomeLabel1.Caption := 'Make room for your creative work.';
  WizardForm.WelcomeLabel2.Caption := 'Install Library, Workscape, or both. You can open Library independently or inside Workscape.' + #13#10#13#10 + 'This preview stays separate from your existing studios. Projects and personal settings are kept when you uninstall.';
end;

procedure ClearAssociation(Extension, ProgID: String);
begin
  RegDeleteValue(HKCU, 'Software\Classes\'+Extension+'\OpenWithProgids', ProgID);
  RegDeleteKeyIncludingSubkeys(HKCU, 'Software\Classes\'+ProgID);
end;
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep <> ssPostInstall then exit;
  if not WizardIsComponentSelected('library') then begin
    RegDeleteKeyIncludingSubkeys(HKCU, 'Software\Jago Suite\Preview\Components\library');
    DeleteFile(ExpandConstant('{group}\Jago Library Preview.lnk'));
  end;
  if not WizardIsComponentSelected('workscape') then begin
    RegDeleteKeyIncludingSubkeys(HKCU, 'Software\Jago Suite\Preview\Components\workspace');
    DeleteFile(ExpandConstant('{group}\Jago Workscape Preview.lnk'));
  end;
  if not WizardIsComponentSelected('library') or not WizardIsTaskSelected('libraryfiles') then ClearAssociation('.jagolibrary','JagoPreview.Library');
  if not WizardIsComponentSelected('workscape') or not WizardIsTaskSelected('workspacefiles') then ClearAssociation('.jagoworkspace','JagoPreview.Workscape');
  if not WizardIsComponentSelected('library') or not WizardIsTaskSelected('pdf') then ClearAssociation('.pdf','JagoPreview.PDF');
  if not WizardIsComponentSelected('library') or not WizardIsTaskSelected('desktop') then DeleteFile(ExpandConstant('{userdesktop}\Jago Library Preview.lnk'));
  if not WizardIsComponentSelected('workscape') or not WizardIsTaskSelected('desktop') then DeleteFile(ExpandConstant('{userdesktop}\Jago Workscape Preview.lnk'));
end;
procedure RegisterExtraCloseApplicationsResources();
begin
  RegisterExtraCloseApplicationsResource(ExpandConstant('{app}\Jago-Workscape.exe'));
  RegisterExtraCloseApplicationsResource(ExpandConstant('{app}\Library-Production\Jago-Library.exe'));
  RegisterExtraCloseApplicationsResource(ExpandConstant('{app}\Library-Production\Tools\Documents\LibreOffice\program\soffice.bin'));
end;
function UpdateReadyMemo(Space, NewLine, MemoUserInfoInfo, MemoDirInfo, MemoTypeInfo, MemoComponentsInfo, MemoGroupInfo, MemoTasksInfo: String): String;
var Changes: String;
begin
  Changes := '';
  if FileExists(ExpandConstant('{app}\Jago-Workscape.exe')) and not WizardIsComponentSelected('workscape') then Changes := Changes + Space + 'Remove Workscape program files' + NewLine;
  if FileExists(ExpandConstant('{app}\Library-Production\Jago-Library.exe')) and not WizardIsComponentSelected('library') then Changes := Changes + Space + 'Remove Library program files' + NewLine;
  if FileExists(ExpandConstant('{app}\Library-Production\Tools\Documents\LibreOffice\program\soffice.exe')) and not WizardIsComponentSelected('library\documents') then Changes := Changes + Space + 'Remove the optional Office renderer' + NewLine;
  Result := MemoDirInfo + NewLine + NewLine + MemoComponentsInfo + NewLine + NewLine + MemoTasksInfo;
  if Changes <> '' then Result := Result + NewLine + NewLine + 'Components being removed:' + NewLine + Changes;
  Result := Result + NewLine + NewLine + 'Projects, collections, linked folders and personal settings are kept. Save work and close your studios before continuing.';
end;
procedure CurPageChanged(CurPageID: Integer);
var Existing: String;
begin
  if CurPageID <> wpWelcome then exit;
  if RegQueryStringValue(HKCU, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\JagoSuiteInstallerPreview_is1', 'InstallLocation', Existing) and FileExists(AddBackslash(Existing)+'unins000.exe') then begin
    WizardForm.WelcomeLabel1.Caption := 'Update or modify your Jago tools.';
    WizardForm.WelcomeLabel2.Caption := 'Keep the tools you want checked. Untick a tool to remove its program files, or tick another to add it.' + #13#10#13#10 + 'Your projects and personal settings stay where they are. The final page shows what will be installed or removed.';
  end;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin Result := (PageID = LaunchPage.ID) and not WizardIsComponentSelected('workscape'); end;
