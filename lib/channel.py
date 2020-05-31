"""Channels the altered input data to the output devices"""

from lib.transformer import Transformer

class Channel(object):
    """
    The channel between input and output.

    ...

    Attributes
    ----------
    transf : Transformer
        The transformer applied to the input.
    """

    def __init__(self, transf: Transformer):
        self.transf: Transformer = transf

    