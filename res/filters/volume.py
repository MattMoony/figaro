"""Filter to change the voice's volume"""

import numpy as np, re
from typing import List, Dict, Any

import lib.filters.filter
from lib.utils import parse_perc

class Volume(lib.filters.filter.Filter):
    class Filter(lib.filters.filter.Filter.Filter):
        """
        Changes the volume of raw voice data.

        ...

        Attributes
        ----------
        fac : float
            The factor by which to change the volume.

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
            return data*self.fac

        def toJSON(self) -> Dict[str, Any]:
            return dict(name='Volume', fac=self.fac)

        def __call__(self, data: np.ndarray) -> np.ndarray:
            return self.apply(data)

        def __str__(self) -> str:
            return f'Volume({self.fac*100:.2f}%)'

    desc: str = 'Changes your voice\'s volume!'

    @classmethod
    def start(cls, args: List[str]) -> "Volume.Filter":
        return Volume.Filter(*Volume.Filter.parse_args(args))

    @classmethod
    def props(cls) -> List[Dict[str, Any]]:
        return [dict(name='fac', min=0, max=20, value=2, step=.2)]