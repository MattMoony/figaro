"""
Figaro's CLI module.
"""

from hans.session import CmdSession

from figaro.cli._helper import CMDS
from figaro.cli._helper.state import FigaroSessionState


def start() -> None:
    """
    Start handling commands.
    """
    session: CmdSession = CmdSession(CMDS, prompt='figaro> ')
    session.state = FigaroSessionState(session)
    session.handle_forever()
