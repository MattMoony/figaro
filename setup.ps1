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

log "info" "Checking requirements ... "
log "info" "Checking python/pip installation ... "
$PyVersion = "$(python --version)"
if (-Not $PyVersion.StartsWith("Python 3")) {
    log "error" "No python3 installation could be found!"
    exit 1
}
log "success" "Functioning python3 setup detected!"
python -m pip --version >$null
if (-Not $?) {
    log "error" "No python3 installation could be found!"
    exit 1
}
log "success" "Functioning pip3 setup detected!"
log "info" "Checking node/npm installation ... "
node --version >$null
if (-Not $?) {
    log "error" "No node setup could be found!"
    exit 1
}
log "success" "Functional node installation found!"
npm --version >$null
if (-Not $?) {
    log "error" "No npm installation found!"
    exit 1
}
log "success" "Functioning npm setup found!"

log "info" "Installing python requirements ... "
python -m pip install -r .\requirements-windows.txt

log "info" "Installing node requirements ... "
Set-Location figaro/gui/web/
npm i

log "success" 'Finished setting up "Figaro"'
