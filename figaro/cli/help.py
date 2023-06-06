"""
Module for the help command
"""

from typing import Any, Dict, List, Optional, Union

from hans.cmd import Command
from hans.state import CLISessionState
from prompt_toolkit.completion.nested import NestedDict
from rich import print  # pylint: disable=redefined-builtin
from rich.tree import Tree

from figaro.utils import io


class Help(Command):
    """
    The help command
    """

    def __init__(self):
        """
        Initializes the help command
        """
        super().__init__('help', aliases=['?',], description='Shows this help message')

    def __build_tree(self, cmds: Dict[str, Any], tree: Tree, state: CLISessionState) -> None:
        """
        Builds a tree of commands from the specified dictionary

        Args:
            cmds (Dict[str, Any]): The dictionary of commands
            tree (Tree): The tree to build
            state (CLISessionState): The current cli session state
        """
        done: List[Command] = []
        for k, v in cmds.items():
            if k.startswith('.'):
                continue
            if isinstance(v, Command) and v.available(state) and v not in done:
                tree.add(f'[bold]{v.name}[/bold]: {v.description}')
                done.append(v)
            elif isinstance(v, dict):
                t: Tree = Tree(k)
                self.__build_tree(v, t, state)
                if t.children:
                    tree.add(t)

    def completer(self, state: CLISessionState) -> Optional[NestedDict]:
        """
        Custom completer behaviour.
        """
        return state.session.compl_dict

    def execute(self, raw_args: List[str], argv: List[str], state: CLISessionState, *args, **kwargs) -> None:
        """
        Executes the help command
        """
        cmds: Dict[str, Union[Command, Dict[str, Any]]] = {}
        for v in state.session.cmds.values():
            state.session.deep_merge(cmds, v)

        if len(raw_args) == 0:
            # seems a little redunant, but keeps aliases
            # out of the top-level overview, at least ...
            cmd_tree: Tree = Tree(io.fl('Available commands:'))
            self.__build_tree(cmds, cmd_tree, state)
            print(cmd_tree)
        else:
            try:
                c, _ = state.session.parse(raw_args)
                if isinstance(c, Command):
                    io.l(f'[bold]{c.name}[/bold]: {c.description}')
                    if len(c.aliases) > 0:
                        io.n(f'Aliases: [bold]{", ".join(c.aliases)}[/bold]')
                else:
                    cmd_tree: Tree = Tree(io.fl('Available sub-commands:'))
                    self.__build_tree(c, cmd_tree, state)
                    print(cmd_tree)
            except KeyError:
                io.e(f'Unknown command: [italic]{" ".join(raw_args)}[/italic]. Enter [bold]help[/bold] to see all available commands ...')