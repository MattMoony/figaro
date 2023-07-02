"""
Show the current status.
"""

from typing import Any, Callable, Dict, List, Tuple

from hans.cmd import Command

from figaro.cli._helper.state import FigaroSessionState
from figaro.utils import io


class ShowStatus(Command):
    """
    The show status command
    """

    def __init__(self):
        """
        Initializes the command
        """
        super().__init__('show status', description='Shows the current status')

    def execute(self, raw_args: List[str], argv: List[str], state: FigaroSessionState, *args, **kwargs) -> None:
        """
        Executes the command
        """
        io.l(str(state.channel))
