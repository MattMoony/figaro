"""Sets the most important constants for figaro"""

from lib.channel import Channel
from lib.transformer import Transformer

"""The buffer size"""
BUF: int = 4096
"""The global transformer"""
transf: Transformer = Transformer()
"""The global audio channel"""
channl: Channel = Channel()