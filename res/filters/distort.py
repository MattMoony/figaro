"""Filter to change the voice's pitch"""

import secrets
import numpy as np
from typing import List, Dict, Any

import figaro.filters.filter

class Distort(figaro.filters.filter.Filter):
    class Filter(figaro.filters.filter.Filter.Filter):
        """
        Distorts audio.
        
        ...
    
        Methods
        -------
        apply(data: np.ndarray)
            Applies the filter and returns the result.
        """
    
        def __init__(self):
            self.gen = secrets.SystemRandom()
    
        def apply(self, data: np.ndarray) -> np.ndarray:
            freq = np.fft.rfft(data)
            N = len(freq)
            sh_freq = np.zeros(N, freq.dtype)
            fac = self.gen.random() * 35 + 10
            S = int(np.round(fac if self.gen.randint(0,1) else N - fac, 0))
            s = int(N-S)
            sh_freq[:S] = freq[s:]
            sh_freq[S:] = freq[:s]
            sh_chunk = np.fft.irfft(sh_freq)
            return sh_chunk.astype(data.dtype)
    
        def toJSON(self) -> Dict[str, Any]:
            return dict(name='distort')
    
        def __call__(self, data: np.ndarray) -> np.ndarray:
            return self.apply(data)
    
        def __str__(self) -> str:
            return f'Distort()'

    @classmethod
    def start(cls, args: List[str]) -> "Distort.Filter":
        return Distort.Filter()

    @classmethod
    def html(cls) -> str:
        return ''''''