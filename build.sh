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


log "success" 'Building "Figaro"'

ORIGINAL_PATH=`pwd`
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd $SCRIPT_DIR

log "info" "Checking for ffmpeg ... "

if [[ -f static/ffmpeg ]]; then
    log "success" "An ffmpeg build is in the static directory"
else
    log "info" "Downloading the latest version of ffmpeg"
    wget -O /tmp/ffmpeg-release-amd64-static.tar.xz "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
    wget -O /tmp/ffmpeg.tar.xz.md5 "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz.md5"
    cd /tmp && md5sum -c ./ffmpeg.tar.xz.md5
    if [[ $? -ne 0 ]]; then
        log "error" "MD5 Checksum doesn't match!"
        exit 1
    fi
    rm /tmp/ffmpeg.tar.xz.md5
    cd $SCRIPT_DIR
    tar -C /tmp -xf /tmp/ffmpeg-release-amd64-static.tar.xz
    rm /tmp/ffmpeg-release-amd64-static.tar.xz
    mv /tmp/ffmpeg*/ffmpeg static/
    mv /tmp/ffmpeg*/ffprobe static/
    log "success" "Successfully downloaded ffmpeg!"
fi

log "info" "Checking for pyinstaller"

python3 -m pip install pyinstaller

log "success" "Pyinstaller found/insatlled!"

log "info" 'Building "figaro-cli" w. pyinstaller'

pyinstaller -ci media/figaro.icns ./figaro.py

log "success" 'Finished building "figaro-cli"'

log "info" "Building the GUI"

cd lib/gui/
npm run dist

log "success" "Finished building the GUI"

cd $ORIGINAL_PATH
