"""The main entry point"""

import pash.misc, pash.cmds, sys
from argparse import ArgumentParser

from lib import cmd, params, gui

def main():
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help='A .fig file to be interpreted ... ')
    parser.add_argument('-i', '--ist', type=str, help='Index of the Input Stream ... ')
    parser.add_argument('-o', '--ost', type=str, help='Index of the Output Stream ... ')
    parser.add_argument('-s', '--server', action='store_true', help='Start listening to websocket commands?')
    parser.add_argument('-g', '--gui', action='store_true', help='Start the GUI?')
    args = parser.parse_args()
    sys.argv = sys.argv[:1]

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
        for ind in args.ist.split(','):
            cmd.on_start_input(None, [], int(ind), json=False)
    if args.ost:
        for ind in args.ost.split(','):
            cmd.on_start_output(None, [], int(ind), json=False)
    if args.ist and args.ost:
        cmd.on_start(None, [], json=False)
    if args.server:
        cmd.on_start_server(None, [])
    if args.gui:
        gui.start()

    cmd.start()
    pash.cmds.clear(None, [])

if __name__ == '__main__':
    main()