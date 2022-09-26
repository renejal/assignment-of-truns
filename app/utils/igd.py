import numpy as np
from typing import List
from pymoo.factory import get_performance_indicator

class IGD:
    @staticmethod
    def calculate_igd(pf: List[List[int]], reference_points: List[List[int]]):
        igdPerformance = get_performance_indicator("igd", np.array(reference_points))
        return igdPerformance.do(pf)
