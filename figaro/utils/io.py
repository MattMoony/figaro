"""
Some I/O related utility functions
"""

from rich import print  # pylint: disable=redefined-builtin


def e(msg: str) -> None:
    """
    Prints an error message
    """
    print(fe(msg))

def fe(msg: str) -> None:
    """
    Marks up an error message as if outputting it.
    """
    return f'[bold red]Error:[/bold red] {msg}'

def w(msg: str) -> None:
    """
    Prints a warning message
    """
    print(fw(msg))

def fw(msg: str) -> None:
    """
    Marks up a warning message as if outputting it.
    """
    return f'[bold yellow]Warning:[/bold yellow] {msg}'

def i(msg: str) -> None:
    """
    Prints an info message
    """
    print(fi(msg))

def fi(msg: str) -> None:
    """
    Marks up an info message as if outputting it.
    """
    return f'[bold blue]Info:[/bold blue] {msg}'

def l(msg: str) -> None:
    """
    Outputs a single line to the user. 
    """
    print(fl(msg))

def fl(msg: str) -> None:
    """
    Marks up a single line as if outputting it.
    """
    return f'[bold grey53][*][/bold grey53] {msg}'

def n(msg: str) -> None:
    """
    Output an *indented* line.
    """
    print(fn(msg))

def fn(msg: str) -> None:
    """
    Marks up an *indented* line as if outputting it.
    """
    return f'    └── {msg}'