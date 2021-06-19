"""A noise filter for audio"""

import numpy as np
from typing import List, Dict, Any

from lib.utils import parse_perc
import lib.filters.filter

class Noise(lib.filters.filter.Filter):
    class Filter(lib.filters.filter.Filter.Filter):
        """
        Adds noise to audio.

        Attributes
        ----------
        amp : float 
            The amplitude.

        Methods
        -------
        apply(data: np.ndarray)
            Applies the filter and returns the result.
        """

        def __init__(self, amp: float):
            self.amp: float = amp

        @classmethod
        def parse_args(cls, args: List[str]) -> List[Any]:
            args = [a.strip() for a in args if a.strip()]
            if not args:
                raise Exception('Missing parameter <amplitude> ... ')
            return [parse_perc(args[0].strip()),]

        def update(self, *args: List[Any]) -> None:
            self.amp = args[0]

        def apply(self, data: np.ndarray) -> np.ndarray:
            return data + (np.random.rand(*data.shape) - .5) * .05 * self.amp

        def toJSON(self) -> Dict[str, Any]:
            return dict(name='Noise', amp=self.amp)

        def __call__(self, data: np.ndarray) -> np.ndarray:
            return self.apply(data)

        def __str__(self) -> str:
            return f'Noise({self.amp*100:.2f}%)'

    desc: str = 'Adds some random noise to your audio!'

    @classmethod
    def start(cls, args: List[str]) -> "Noise.Filter":
        return Noise.Filter(*Noise.Filter.parse_args(args))

    @classmethod
    def props(cls) -> List[Dict[str, Any]]:
        return [dict(name='amplitude', min=0, max=1, step=.01, value=.3),]
        return '''
            <input type="range" min="0" max="1" step="0.01" value="0.3" name="amplitude" />
        '''