"""The main entry point"""

import pash.misc, pash.cmds, os, sys
from argparse import ArgumentParser

from lib import cmd

def main():
    parser = ArgumentParser()
    parser.add_argument('-g', '--gui', action='store_true', help='Use GUI?')
    parser.add_argument('-f', '--file', type=str, help='A .fig file to be interpreted ... ')
    parser.add_argument('-i', '--ist', type=int, help='Index of the Input Stream ... ')
    parser.add_argument('-o', '--ost', type=int, help='Index of the Output Stream ... ')
    args = parser.parse_args()
    sys.argv = sys.argv[:1]

    if args.gui:
        from lib import gui
        gui.start()
        os._exit(0)

    pash.cmds.clear(None, [])
    pash.misc.fancy_print("""   ,d8888b  d8,                                     
   88P'    `8P                                      
d888888P                                            
  ?88'      88b d888b8b   d888b8b    88bd88b d8888b 
  88P       88Pd8P' ?88  d8P' ?88    88P'  `d8P' ?-by
 d88       d88 88b  ,88b 88b  ,88b  d88     88b  d-MattMoony
d88'      d88' `?88P'`88b`?88P'`88bd88'     `?8888P'
                      )88                           
                     ,88P                           
                 `?8888P                             
""")

    if args.file:
        cmd.on_start_interpreter(None, [], args.file)
    if args.ist:
        cmd.on_start_input(None, [], args.ist)
    if args.ost:
        cmd.on_start_output(None, [], args.ost)
    if args.ist and args.ost:
        cmd.on_start(None, [])
        
    cmd.start()
    pash.cmds.clear(None, [])

if __name__ == '__main__':
    main()