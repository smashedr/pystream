$ErrorActionPreference = "Stop"

if (!(Get-Command "7z.exe" -ErrorAction SilentlyContinue)) {Throw "Unable to locate 7z.exe."}

if(!(Test-Path -Path ".\pystream.py" )) {Throw "You are in the wrong directory..."}
if(!(Test-Path -Path ".\icon.ico" )) {Throw "Unable to locate icon.ico..."}
if(!(Test-Path -Path ".\readme.txt" )) {Throw "Unable to locate readme.txt..."}

if((Test-Path -Path ".\pystream" )) {Remove-Item ".\pystream" -Recurse -Force}
if((Test-Path -Path ".\build" )) {Remove-Item ".\build" -Recurse -Force}
if((Test-Path -Path ".\dist" )) {Remove-Item ".\dist" -Recurse -Force}
if((Test-Path -Path ".\__pycache__" )) {Remove-Item ".\__pycache__" -Recurse -Force}
if((Test-Path -Path ".\pystream.zip" )) {Remove-Item ".\pystream.zip"  -Force}

pyinstaller.exe --clean --console --onefile ".\pystream.spec"
if ( ! $lastExitCode -eq 0 ) { Throw "Error running pyinstaller.exe" }

Rename-Item -Path ".\dist" -NewName ".\pystream"
Copy-Item ".\readme.txt" -Destination ".\pystream\readme.txt"
7z.exe a ".\pystream.zip" ".\pystream"
if ( ! $lastExitCode -eq 0 ) { Throw "Error running 7z.exe" }
