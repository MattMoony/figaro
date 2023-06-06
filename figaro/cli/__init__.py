"""
Figaro's CLI module.
"""

from hans.session import CmdSession

from figaro.cli._helper import CMDS


def start() -> None:
    """
    Start handling commands.
    """
    session: CmdSession = CmdSession(CMDS, prompt='figaro> ')
    session.handle_forever()
