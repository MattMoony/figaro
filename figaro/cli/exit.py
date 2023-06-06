"""
Module for the exit command
"""

from typing import List

from hans.cmd import Command
from hans.state import CLISessionState


class Exit(Command):
    """
    The exit command
    """

    def __init__(self):
        """
        Initializes the exit command
        """
        super().__init__('exit', aliases=['quit',], description='Exits the program')

    def execute(self, raw_args: List[str], argv: List[str], state: CLISessionState, *args, **kwargs) -> None:
        """
        Executes the exit command
        """
        state.session.exit(code=0)