"""
Custom cmd session state for figaro.
"""

from dataclasses import dataclass, field
from typing import List

import pyaudio
from hans.state import CLISessionState

from figaro.channel import Channel
from figaro.interpreter import Interpreter


@dataclass
class FigaroSessionState(CLISessionState):
    audio: pyaudio.PyAudio = pyaudio.PyAudio()
    """The pyaudio object."""
    channel: Channel = Channel()
    """The main audio channel."""
    interpreters: List[Interpreter] = field(default_factory=list)
    """A list of all running interpreters."""
