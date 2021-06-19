"""Sets the most important constants for figaro"""
import os
from typing import List

BPATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ALLOWED_EXTS: List[str] = ['mp3', 'wav', 'ogg']

BUF: int = 4096
SMPRATE: int = 44100
CHNNLS: int = 1

HOST: str = '127.0.0.1'
PORT: int = 0xCAFE
DB_PATH: str = os.path.join(BPATH, 'res', 'server.db')