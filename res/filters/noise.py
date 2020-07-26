"""A noise filter for audio"""

import numpy as np
from typing import List, Dict, Any

from figaro.utils import parse_perc
import figaro.filters.filter

class Noise(figaro.filters.filter.Filter):
    class Filter(figaro.filters.filter.Filter.Filter):
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

        def apply(self, data: np.ndarray) -> np.ndarray:
            return data + (np.random.rand(*data.shape) - .5) * .05 * self.amp

        def toJSON(self) -> Dict[str, Any]:
            return dict(name='noise', amp=self.amp)

        def __call__(self, data: np.ndarray) -> np.ndarray:
            return self.apply(data)

        def __str__(self) -> str:
            return f'Noise({self.amp*100:.2f}%)'

    @classmethod
    def start(cls, args: List[str]) -> "Noise.Filter":
        args = [a.strip() for a in args if a.strip()]
        if not args:
            raise Exception('Missing parameter <amplitude> ... ')
        return Noise.Filter(parse_perc(args[0]))

    @classmethod
    def html(cls) -> str:
        return '''
            <input type="range" min="0" max="1" step="0.01" value="0.3" name="amplitude" />
        '''