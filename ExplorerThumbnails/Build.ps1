param([string]$CompilerRoot)
$ErrorActionPreference='Stop'
if(-not $CompilerRoot){$locator=Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe';if(-not(Test-Path -LiteralPath $locator)){throw 'Install Visual Studio C++ build tools and Windows SDK.'};$CompilerRoot=& $locator -latest -products '*' -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath}
$environment=Join-Path $CompilerRoot 'VC\Auxiliary\Build\vcvars64.bat'
Push-Location $PSScriptRoot
try{& $env:COMSPEC /d /c ('call "'+$environment+'" >nul && cl /nologo /std:c++17 /EHsc /W4 /O2 /MT /DUNICODE /D_UNICODE /LD ThumbnailProvider.cpp /link /DEF:ThumbnailProvider.def /OUT:Jago.ProjectThumbnails.dll ole32.lib shlwapi.lib windowscodecs.lib crypt32.lib gdi32.lib uuid.lib');if($LASTEXITCODE -ne 0){throw 'Native provider build failed.'}}finally{Pop-Location}
