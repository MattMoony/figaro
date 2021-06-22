"""Several utility functions"""

import re
import os
import sys
import colorama as cr
cr.init()

def colorz(txt: str, col: int) -> str:
    """Colorize the given text in the given color"""
    return '{}{}{}'.format(col, txt, cr.Fore.RESET)

def printcolor(txt: str, col: int) -> None:
    """Print the given text in the given color"""
    print(colorz(txt, col))

def printerr(msg: str) -> None:
    """Print an error message in an appropriate color"""
    printcolor(msg, cr.Fore.LIGHTRED_EX)

def printwrn(msg: str) -> None:
    """Print a warning message in an appropriate color"""
    printcolor(msg, cr.Fore.LIGHTYELLOW_EX)

def parse_perc(s: str) -> float:
    """Parse a percentage; e.g. either '150%' or '1.5'"""
    return float(s[:-1])/100. if re.match(r'^\d+(?:\.\d+)?%$', s) else float(s)

def dir_exists(path: str) -> None:
    """Make sure that the given directory exists (create it, if need be)"""
    if not os.path.isdir(path):
        os.makedirs(path)

def touch(path: str) -> None:
    """Create an empty file"""
    with open(path, 'w') as f:
        f.write('')

def platform_ext(path: str) -> None:
    """Appends the correct binary file extension, depending on the current platform"""
    return f'{path}.exe' if sys.platform == 'win32' else path
