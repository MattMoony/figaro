"""
Module for the exit command
"""

from typing import List

from hans.cmd import Command

from figaro.cli._helper.state import FigaroSessionState


class Exit(Command):
    """
    The exit command
    """

    def __init__(self):
        """
        Initializes the exit command
        """
        super().__init__('exit', aliases=['quit',], description='Exits the program')

    def execute(self, raw_args: List[str], argv: List[str], state: FigaroSessionState, *args, **kwargs) -> None:
        """
        Executes the exit command
        """
        try:
            state.channel.stop()
        except:
            pass
        state.audio.terminate()
        state.session.exit(code=0)
