#!/bin/bash

log() {
    case "$1" in
        "error")
            c=1
            s="-"
            ;;
        "warning")
            c=3
            s="!"
            ;;
        "success")
            c=2
            s="+"
            ;;
        *)
            c=6
            s="*"
            ;;
    esac
    echo -e "\033[3${c}m[$(date +'%Y-%m-%d~%H:%M')|$s]\033[0m $2"
}

log "success" "Setting up \"Figaro\""

log "info" "Checking requirements ... "
log "info" "Checking python/pip installation ... "
/usr/bin/env python3 --version >/dev/null
if [[ $? -ne 0 ]]; then
    log "error" "No python3 installation could be found!"
    exit 1
fi
log "success" "Functioning python3 setup detected!"
/usr/bin/env python3 -m pip --version >/dev/null
if [[ $? -ne 0 ]]; then
    log "error" "No pip3 installation could be found!"
    exit 1
fi
log "success" "Functioning pip3 setup detected!"
log "info" "Checking node/npm installation ... "
node --version >/dev/null
if [[ $? -ne 0 ]]; then
    log "error" "No node setup could be found!"
    exit 1
fi
log "success" "Functional node installation found!"
npm --version >/dev/null
if [[ $? -ne 0 ]]; then
    log "error" "No npm installation found!"
    exit 1
fi
log "success" "Functioning npm setup found!"

log "info" "Installing python requirements ... "
/usr/bin/env python3 -m pip install -r ./requirements-unix.txt

log "info" "Installing node requirements ... "
cd figaro/gui/web/
npm i
cd ../../../

log "info" "Building the GUI (web/gatsby part)"
cd figaro/gui/web/
npm run build
cd ../../../

log "success" "Finished setting up \"Figaro\""

log "info" "If you want to use the GUI, you should now run"
log "info" "python3 .\figaro.py -s"
log "info" "enter some user credentials when prompted to do so (this is so in future versions you can also use Figaro accross the network), then quit and run"
log "info" "./gui.sh"
