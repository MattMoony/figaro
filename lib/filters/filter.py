import numpy as np

class Filter(object):
    def __init__(self):
        pass

    def apply(self, data: np.array) -> np.array:
        pass

    def __call__(self, data: np.array) -> np.array:
        return self.apply(data)