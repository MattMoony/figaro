"""Several utility functions"""

import colorama as cr
cr.init()

def colorz(txt: str, col: int) -> str:
    return '{}{}{}'.format(col, txt, cr.Fore.RESET)

def printcolor(txt: str, col: int) -> None:
    print(colorz(txt, col))

def printerr(msg: str) -> None:
    printcolor(msg, cr.Fore.LIGHTRED_EX)

def printwrn(msg: str) -> None:
    printcolor(msg, cr.Fore.LIGHTYELLOW_EX)