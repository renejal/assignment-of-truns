import numpy as np
from typing import List
from pymoo.factory import get_performance_indicator

class Hipervolumen:
    @staticmethod
    def calculate_hipervolumen(pf: List[List[int]]):
        hv = get_performance_indicator("hv", ref_point=np.array([1, 1, 1,1]))
        return hv.do(pf)