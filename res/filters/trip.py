"""
Filter to add a trippy sound effect.
"""

import re
from typing import Any, Dict, List

import numpy as np

import figaro.filters.filter
from figaro.utils import parse_perc


class Trip(figaro.filters.filter.Filter):
    """
    Filter plugin to add a trippy sound effect.
    """

    class Filter(figaro.filters.filter.Filter.Filter):
        """
        Adds a trippy effect to audio.
        """

        scale: float
        """How much the echo gets damped on each iteration."""

        def __init__(self, scale: float) -> None:
            self.scale: float = scale
            self._prev: np.ndarray = None

        @classmethod
        def parse_args(cls, args: List[str]) -> List[Any]:
            args = [a.strip() for a in args if a.strip()]
            if not args:
                raise Exception('Missing parameter <scale> ... ')
            return [parse_perc(args[0].strip()),]

        def update(self, *args: List[Any]) -> None:
            self.scale = args[0]

        def apply(self, data: np.ndarray) -> np.ndarray:
            if self._prev is None:
                self._prev = np.zeros(data.shape)
            data, self._prev = data + self._prev, self._prev * self.scale + data
            return data

        def toJSON(self) -> Dict[str, Any]:
            return dict(name='Trip', scale=self.scale)

        def __call__(self, data: np.ndarray) -> np.ndarray:
            return self.apply(data)

        def __str__(self) -> str:
            return f'Trip({self.scale*100:.2f}% damping)'

    desc: str = 'Makes you sound rather trippy!'

    @classmethod
    def start(cls, args: List[str]) -> "Trip.Filter":
        return Trip.Filter(*Trip.Filter.parse_args(args))

    @classmethod
    def props(cls) -> List[Dict[str, Any]]:
        return [dict(name='scale', min=0, max=1, step=.01, value=.4),]
