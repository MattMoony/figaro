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

log "success" 'Setting up "Figaro"'

$OriginalPath = Get-Location
Set-Location $PSScriptRoot

log "info" "Checking requirements ... "
log "info" "Checking python/pip installation ... "
$PyVersion = (python --version).Replace('.', '').Split(' ')[1].SubString(0,2)
if (-Not $PyVersion.StartsWith("3")) {
    log "error" "No python3 installation could be found!"
    exit 1
}
log "success" "Functioning python3 setup detected!"

python -m pip --version >$null 2>$null
if (-Not $?) {
    log "error" "No python3 installation could be found!"
    exit 1
}
log "success" "Functioning pip3 setup detected!"

log "info" "Checking node/npm installation ... "
node --version >$null 2>$null
if (-Not $?) {
    log "error" "No node setup could be found!"
    exit 1
}
log "success" "Functional node installation found!"

npm --version >$null 2>$null
if (-Not $?) {
    log "error" "No npm installation found!"
    exit 1
}
log "success" "Functioning npm setup found!"

log "info" "Installing python requirements ... "
$ExtPyVersion = $PyVersion;
if ($PyVersion -lt 38) {
    $ExtPyVersion = $PyVersion + "m"
}
$Arch = (Get-WmiObject -Class Win32_operatingsystem).OsArchitecture.SubString(0,2)
if ($Arch -eq 64) {
    $Arch = "win_amd64"
} else {
    $Arch = "win32"
}
log "warning" "The Windows PyAudio build has to be downloaded manually!"
$yN = (Read-Host -Prompt "Do you want to download it now? (If you don't now and installing the requirements fails, simply run this setup script again)").ToLower()
if ($yN.StartsWith("y")) {
    $WheelName = "PyAudio-0.2.11-cp${PyVersion}-cp${ExtPyVersion}-${Arch}.whl"
    log "warning" "Download the `"$WheelName`" wheel"
    start "https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio"
    log "warning" "After downloading it, run `"pip install .\$WheelName`" in the download directory"
    $PyAudioInstalled = $False
    Do {
        Read-Host -Prompt "Once the setup has finished, press <ENTER> here to continue"
        python -c "import pyaudio" >$null 2>$null
        $PyAudioInstalled = $?
        if (-Not $PyAudioInstalled) {
            log "error" "Python failed to import `"pyaudio`". Has the installation finished?"
            log "error" "If you have installed the wheel already and think this is an error, please submit an Issue on https://github.com/MattMoony/figaro/issues!"
        }
    } While (-Not $PyAudioInstalled)
    log "success" "You have successfully installed `"PyAudio`"! Congratulations!"
}

log "info" "Installing requirements via pip ... "
python -m pip install -r .\requirements-windows.txt

log "info" "Installing node requirements (electron part) ... "
Set-Location lib/gui/
npm i

log "info" "Installing node requirements (web/gatsby part) ... "
Set-Location web/
npm i

log "info" "Building the GUI (web/gatsby part)"
npm run build
Set-Location ..\..\..\

log "warning" "If you want to use `"Figaro`" with programs such as Discord, you will have to install a loopback adapter."
$yn = (Read-Host -Prompt "Do you want this setup script to download and install the https://vb-audio.com/Cable/ loopback device now?")
if ($yN.StartsWith("y")) {
    Invoke-WebRequest "https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack43.zip" -OutFile "${env:Temp}\VBCABLE_Driver_Pack.zip"
    Expand-Archive -Force "${env:Temp}\VBCABLE_Driver_Pack.zip" "${env:Temp}\VBCABLE_Driver_Pack"
    Start-Process powershell -Verb runAs -ArgumentList "start ${env:Temp}\VBCABLE_Driver_Pack\VBCABLE_Setup$(If ($Arch -eq 'win_amd64') {'_x64'} Else {''}).exe"
    log "Warning" "It is recommended you restart your PC after this setup script has finished!" 
}

log "success" 'Finished setting up "Figaro"'

log "info" "If you want to use the GUI, just run"
log "info" ".\gui.ps1"

Set-Location $OriginalPath
