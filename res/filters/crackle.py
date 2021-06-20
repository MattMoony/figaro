"""A crackling filter for audio"""

import numpy as np
from typing import List, Dict, Any

import lib.filters.filter
from lib.utils import parse_perc

class Crackle(lib.filters.filter.Filter):
    class Filter(lib.filters.filter.Filter.Filter):
        """
        Adds a crackling effect to audio.

        Attributes
        ----------
        fac : float
            How much crackling should be applied.

        Methods
        -------
        apply(data: np.ndarray)
            Applies the filter and returns the result.
        """

        def __init__(self, fac: float):
            self.fac: float = fac

        @classmethod
        def parse_args(cls, args: List[str]) -> List[Any]:
            args = [a.strip() for a in args if a.strip()]
            if not args:
                raise Exception('Missing parameter <factor> ... ')
            return [parse_perc(args[0].strip()),]

        def update(self, *args: List[Any]) -> None:
            self.fac = args[0]

        def apply(self, data: np.ndarray) -> np.ndarray:
            ifac = 1 - .9 * self.fac
            return data.clip(data.min() * ifac, data.max() * ifac) * (.5 / ifac)

        def toJSON(self) -> Dict[str, Any]:
            return dict(name='Crackle', fac=self.fac)

        def __call__(self, data: np.ndarray) -> np.ndarray:
            return self.apply(data)

        def __str__(self) -> str:
            return f'Crackle({self.fac*100:.2f}%)'

    desc: str = 'Adds a crackling effect to your audio!'

    @classmethod
    def start(cls, args: List[str]) -> "Crackle.Filter":
        return Crackle.Filter(*Crackle.Filter.parse_args(args))

    @classmethod
    def props(cls) -> List[Dict[str, Any]]:
        return [dict(name='fac', min=0, max=1, step=.01),]