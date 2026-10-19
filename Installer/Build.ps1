param(
 [Parameter(Mandatory=$true)][string]$LibraryPackage,
 [Parameter(Mandatory=$true)][string]$WorkscapeExe,
 [Parameter(Mandatory=$true)][string]$Compiler,
 [Parameter(Mandatory=$true)][string]$OutputDirectory,
 [string]$StageDirectory=(Join-Path ([IO.Path]::GetTempPath()) ('Jago-Installer-'+[guid]::NewGuid()))
)
$ErrorActionPreference='Stop'
foreach($file in @((Join-Path $LibraryPackage 'Jago-Library.exe'),(Join-Path $LibraryPackage 'Jago-Library.html'),$WorkscapeExe,$Compiler)){
 if(-not(Test-Path -LiteralPath $file -PathType Leaf)){throw "Required file missing: $file"}
}
if(Test-Path -LiteralPath $StageDirectory){throw 'Choose a new staging directory to avoid carrying stale release files.'}
New-Item -ItemType Directory -Path $StageDirectory | Out-Null
Copy-Item -LiteralPath $LibraryPackage -Destination (Join-Path $StageDirectory 'Library-Production') -Recurse
Copy-Item -LiteralPath $WorkscapeExe -Destination (Join-Path $StageDirectory 'Jago-Workscape.exe')
$workscapeRoot=Split-Path $WorkscapeExe
Copy-Item -LiteralPath (Join-Path $workscapeRoot 'LICENSE.txt') -Destination (Join-Path $StageDirectory 'Workscape-LICENSE.txt')
Copy-Item -LiteralPath (Join-Path $workscapeRoot 'Documentation') -Destination (Join-Path $StageDirectory 'Documentation') -Recurse
Set-Content -LiteralPath (Join-Path $StageDirectory 'installer-preview.txt') -Value 'Jago installation pilot'
Set-Content -LiteralPath (Join-Path $StageDirectory 'Library-Production\installer-preview.txt') -Value 'Jago installation pilot'
& python (Join-Path $PSScriptRoot 'prepare-removal.py') $StageDirectory
if($LASTEXITCODE -ne 0){throw 'Component removal list generation failed'}
& $Compiler /Q ("/DPayload="+[IO.Path]::GetFullPath($StageDirectory)) ("/DOutput="+[IO.Path]::GetFullPath($OutputDirectory)) (Join-Path $PSScriptRoot 'pilot.iss')
if($LASTEXITCODE -ne 0){throw 'Installer compilation failed'}
Write-Output (Join-Path $OutputDirectory 'Jago-Library-Workscape-Setup-Preview.exe')
