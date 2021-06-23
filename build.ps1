function log {
    param (
        $Type,
        $Msg
    )
    switch ($Type) {
        "error"     { $c = "Red"; $s = "-"; }
        "warning"   { $c = "Yellow"; $s = "!"; }
        "success"   { $c = "Green"; $s = "+"; }
        default     { $c = "Cyan"; $s = "*"; }
    }
    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd~HH:mm')|$s] " -ForegroundColor $c -NoNewline
    Write-Host "$Msg"
}

log "success" 'Building "Figaro"'

$OriginalPath = Get-Location
Set-Location $PSScriptRoot

log "info" "Checking for ffmpeg ... "

if (Test-Path -Path ".\static\ffmpeg.exe") {
    log "success" "An ffmpeg build is in the static directory"
} else {
    log "info" "Downloading the latest version of ffmpeg"
    Invoke-WebRequest "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile "${env:Temp}\ffmpeg.zip"
    Expand-Archive -Force "${env:Temp}\ffmpeg.zip" ".\static\"
    Move-Item ".\static\*\bin\ffmpeg.exe" ".\static\tmp.exe"
    Move-Item ".\static\*\bin\*" ".\static\"
    Remove-Item -Path ".\static\ffmpeg*" -Recurse
    Move-Item ".\static\tmp.exe" ".\static\ffmpeg.exe"
    log "success" "Successfully downloaded ffmpeg!"
}

log "info" "Checking for pyinstaller"

python -m pip install pyinstaller

log "success" "Pyinstaller found/installed!"

log "info" 'Building "figaro-cli" w. pyinstaller'

pyinstaller --noupx -ci ".\media\figaro.ico" .\figaro.py

log "success" 'Finished building "figaro-cli"'

log "info" "Building the GUI"

Set-Location lib/gui/
npm run dist

log "success" "Finished building the GUI"

Set-Location $OriginalPath
