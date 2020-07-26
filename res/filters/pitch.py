"""Filter to change the voice's pitch"""

import numpy as np
from typing import List, Dict, Any

from figaro.utils import parse_perc
import figaro.filters.filter

class Pitch(figaro.filters.filter.Filter):
    class Filter(figaro.filters.filter.Filter.Filter):
        """
        Changes the pitch of raw voice data.
        
        ...
    
        Attributes
        ----------
        fac : float
            The factor by which to change the pitch.
    
        Methods
        -------
        apply(data: np.ndarray)
            Applies the filter and returns the result.
        """
    
        def __init__(self, fac: float):
            self.fac: float = fac
    
        def apply(self, data: np.ndarray) -> np.ndarray:
            freq = np.fft.rfft(data)
            N = len(freq)
            sh_freq = np.zeros(N, freq.dtype)
            S = int(np.round(self.fac if self.fac > 0 else N + self.fac, 0))
            s = int(N-S)
            sh_freq[:S] = freq[s:]
            sh_freq[S:] = freq[:s]
            sh_chunk = np.fft.irfft(sh_freq)
            return sh_chunk.astype(data.dtype)
    
        def toJSON(self) -> Dict[str, Any]:
            return dict(name='pitch', fac=self.fac)
    
        def __call__(self, data: np.ndarray) -> np.ndarray:
            return self.apply(data)
    
        def __str__(self) -> str:
            return f'Pitch({self.fac*100:.2f}%)'

    @classmethod
    def start(cls, args: List[str]) -> "Pitch.Filter":
        args = [a.strip() for a in args if a.strip()]
        if not args:
            raise Exception('Missing parameter <factor> ... ')
        n = args[0].strip()
        return Pitch.Filter(parse_perc(n))

    @classmethod
    def html(cls) -> str:
        return '''
            <input type="range" min="-30" max="30" value="0" name="fac" />
        '''