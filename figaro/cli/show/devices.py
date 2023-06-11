"""
Show all audio devices.
"""

from typing import Any, Callable, Dict, List, Tuple

from hans.cmd import Command

from figaro.cli._helper.state import FigaroSessionState
from figaro.utils import io


class ShowDevices(Command):
    """
    The show devices command
    """

    def __init__(self):
        """
        Initializes the command
        """
        super().__init__('show devices', description='Shows all audio devices')

    def execute(self, raw_args: List[str], argv: List[str], state: FigaroSessionState, *args, **kwargs) -> None:
        """
        Executes the command
        """
        devs: Dict[str, Any] = [ state.audio.get_device_info_by_host_api_device_index(0, i) 
                                 for i in range(state.audio.get_host_api_info_by_index(0)['deviceCount']) ]
        filterd: Callable[[str], List[Tuple[int, str]]] = lambda s: [ (i, d['name'],) for i, d in enumerate(devs) if d[s] > 0 ]
        io.l('Input devices:')
        for i, n in filterd('maxInputChannels'):
            io.n(f'{i:02d}: {n}')
        io.l('Output devices:')
        for i, n in filterd('maxOutputChannels'):
            io.n(f'{i:02d}: {n}')
