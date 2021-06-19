"""Home of the sounds manager"""

import os
import copy
import json
import collections
from typing import List, Dict, Any

from lib import params, utils

"""The path to the default sound-file directory"""
SPATH: str = os.path.join(params.BPATH, 'res', 'sounds')
"""The default volume"""
DEFAULT_VOLUME: int = 1
"""The default background"""
DEFAULT_COLOR: str = '#0B3954'

def __home_exists() -> None:
    """Make sure that SPATH exists"""
    utils.dir_exists(SPATH)
    utils.touch(os.path.join(SPATH, '.gitkeep'))

def __get_legal(spath: str = SPATH) -> List[str]:
    """Get a list of all audio files with an appropriate extension in the given directory"""
    return [s for s in os.listdir(spath) if os.path.isfile(os.path.join(spath, s)) and s.split('.')[-1] in params.ALLOWED_EXTS]

def __update_missing(sounds: List[str], conf: Dict[str, Dict[str, Any]], bpath: str = SPATH) -> bool:
    """Adds any new sounds to the configuration; returns `True`, if new sounds were added"""
    missing = list(filter(lambda s: s not in conf.keys(), sounds))
    for s in missing:
        conf[s] = { 'vol': DEFAULT_VOLUME, 'color': DEFAULT_COLOR, 'path': os.path.join(bpath, s), }
    return bool(missing)

def __update_deleted(conf: Dict[str, Dict[str, Any]]) -> bool:
    """Checks if all sound files in the config still exist, if not, it deletes the entry"""
    deleted = []
    for k, v in conf.items():
        if 'path' not in v.keys() or not os.path.isfile(v['path']):
            deleted.append(k)
    for k in deleted:
        del conf[k]
    return bool(deleted)

def get(sname: str) -> Dict[str, Any]:
    """Returns config for the given sound file"""
    return get_conf()[sname]

def add(sname: str, path: str) -> None:
    """Adds a new sound to the config"""
    conf = get_conf()
    if not os.path.isfile(path):
        raise FileNotFoundError()
    conf[sname] = { 'vol': DEFAULT_VOLUME, 'color': DEFAULT_COLOR, 'path': path, }
    with open(os.path.join(SPATH, 'conf.json'), 'w') as f:
        json.dump(conf, f)

def update(sname: str, upd: Dict[str, Any]) -> None:
    """Update all or parts of a sound's config"""
    conf = get_conf()
    conf[sname] = { **conf[sname], **upd, }
    with open(os.path.join(SPATH, 'conf.json'), 'w') as f:
        json.dump(conf, f)

def get_all() -> List[str]:
    """Returns a list of all playable sound files (in known locations)"""
    return get_conf().keys()

def get_conf() -> Dict[str, Dict[str, Any]]:
    """Returns the entire config; for all soundfiles"""
    __home_exists()
    conf = {}
    cpath = os.path.join(SPATH, 'conf.json')
    if os.path.isfile(cpath):
        with open(cpath, 'r') as f:
            conf = json.load(f)
    deleted = __update_deleted(conf)
    sounds = __get_legal()
    missing = __update_missing(sounds, conf)
    if deleted or missing:
        with open(cpath, 'w') as f:
            json.dump(conf, f)
    return dict(sorted(conf.items(), key=lambda x: x[0].lower()))
