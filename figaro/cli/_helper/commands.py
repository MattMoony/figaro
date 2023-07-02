"""
Defines all commands of the figaro module.
"""

from typing import Dict

from hans.cmd import Command

from figaro.cli.exit import Exit
from figaro.cli.help import Help
from figaro.cli.show.devices import ShowDevices
from figaro.cli.show.status import ShowStatus

CMDS: Dict[str, Command] = {
    'exit': Exit(),
    'help': Help(),
    'show': {
        'devices': ShowDevices(),
        'status': ShowStatus(),
    }
}
