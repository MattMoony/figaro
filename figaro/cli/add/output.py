"""
Add an output device.
"""

import pyaudio
from typing import Any, Callable, Dict, List, Tuple

from hans.cmd import Command

from figaro import params
from figaro.cli._helper.state import FigaroSessionState
from figaro.device import Device
from figaro.utils import io


class AddOutput(Command):
    """
    The add output command
    """

    def __init__(self):
        """
        Initializes the command
        """
        super().__init__('add output', description='Adds an output device')
        super().add_argument('indo', type=int, help='The output device index')

    def execute(self, indo: int, raw_args: List[str], argv: List[str], state: FigaroSessionState, *args, **kwargs) -> None:
        """
        Executes the command
        """
        state.channel.inputs.append(Device(state.audio, format=pyaudio.paFloat32, channels=1, rate=params.SMPRATE, output=True, output_device_index=indo))
