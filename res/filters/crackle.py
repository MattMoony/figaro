"""A crackling filter for audio"""

import numpy as np
from typing import List, Dict, Any

import figaro.filters.filter
from figaro.utils import parse_perc

class Crackle(figaro.filters.filter.Filter):
    class Filter(figaro.filters.filter.Filter.Filter):
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

        def apply(self, data: np.ndarray) -> np.ndarray:
            ifac = 1 - .9 * self.fac
            return data.clip(data.min() * ifac, data.max() * ifac) * (.5 / ifac)

        def toJSON(self) -> Dict[str, Any]:
            return dict(name='crackle', fac=self.fac)

        def __call__(self, data: np.ndarray) -> np.ndarray:
            return self.apply(data)

        def __str__(self) -> str:
            return f'Crackle({self.fac*100:.2f}%)'

    @classmethod
    def start(cls, args: List[str]) -> "Crackle.Filter":
        args = [a.strip() for a in args if a.strip()]
        if not args:
            raise Exception('Missing parameter <factor> ... ')
        return Crackle.Filter(parse_perc(args[0]))

    @classmethod
    def html(cls) -> str:
        return '''
            <input type="range" min="0" max="1" step="0.01" name="fac" />
        '''