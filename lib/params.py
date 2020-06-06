"""Sets the most important constants for figaro"""
import os

BPATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

BUF: int = 4096
SMPRATE: int = 44100
CHNNLS: int = 1