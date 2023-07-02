"""
Add an input device.
"""

import pyaudio
from typing import Any, Callable, Dict, List, Tuple

from hans.cmd import Command

from figaro import params
from figaro.cli._helper.state import FigaroSessionState
from figaro.device import Device
from figaro.utils import io


class AddInput(Command):
    """
    The add input command
    """

    def __init__(self):
        """
        Initializes the command
        """
        super().__init__('add input', description='Adds an input device')
        super().add_argument('indi', type=int, help='The input device index')

    def execute(self, indi: int, raw_args: List[str], argv: List[str], state: FigaroSessionState, *args, **kwargs) -> None:
        """
        Executes the command
        """
        state.channel.inputs.append(Device(state.audio, format=pyaudio.paFloat32, channels=1, rate=params.SMPRATE, input=True, input_device_index=indi))
