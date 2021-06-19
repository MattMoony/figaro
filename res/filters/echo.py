"""Filter to add an echo"""

import numpy as np, re
from datetime import datetime
from typing import List, Tuple, Dict, Any

from lib.utils import parse_perc
import lib.filters.filter

class Echo(lib.filters.filter.Filter):
    class Filter(lib.filters.filter.Filter.Filter):
        """
        Adds an echo to audio.

        ...

        Attributes
        ----------
        scale : float
            How much the echo gets damped on each iteration.
        pause : float
            How large the pause between the actual sound and the echo should be.

        Methods
        -------
        apply(data: np.ndarray)
            Applies the filter and returns the result.
        """

        def __init__(self, scale: float, pause: float):
            self.scale: float = scale
            self.pause: float = pause
            self._q: List[Tuple[float, np.ndarray]] = []

        @classmethod
        def parse_args(cls, args: List[str]) -> List[Any]:
            args = [a.strip() for a in args if a.strip()]
            if len(args) < 2:
                raise Exception('Missing parameters <scale> <pause> ... ')
            scale = parse_perc(args[0])
            pause = float(args[1])
            return [scale, pause,]

        def update(self, *args: List[Any]) -> None:
            self.scale = args[0]
            self.pause = args[1]

        def apply(self, data: np.ndarray) -> np.ndarray:
            c = np.zeros(data.shape)
            now = datetime.now().timestamp()
            if self._q:
                if self._q[0][0] + self.pause <= now + .1:
                    c = self._q[0][1]
                    self._q = self._q[1:]
            data += c
            self._q.append((now, data * self.scale))
            return data

        def toJSON(self) -> Dict[str, Any]:
            return dict(name='Echo', scale=self.scale, pause=self.pause)

        def __call__(self, data: np.ndarray) -> np.ndarray:
            return self.apply(data)

        def __str__(self) -> str:
            return f'Echo({self.pause}s delay, {self.scale*100:.2f}% damping)'

    desc: str = 'Adds an echo to your voice!'

    @classmethod
    def start(cls, args: List[str]) -> "Echo.Filter":
        return Echo.Filter(*Echo.Filter.parse_args(args))

    @classmethod
    def props(cls) -> List[Dict[str, Any]]:
        return [
            dict(name='scale', min=0, max=1, step=.01, value=.5),
            dict(name='pause', min=0, max=10, step=.1, value=.5),
        ]