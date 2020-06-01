"""The main entry point"""

import pash.misc, pash.cmds
from lib import cmd

def main():
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
    cmd.start()

if __name__ == '__main__':
    main()