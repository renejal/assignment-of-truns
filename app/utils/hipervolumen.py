import numpy as np
from typing import List
from dominio.Solution import Solution
from pymoo.factory import get_performance_indicator

class Hipervolumen:
    @staticmethod
    def calculate_hipervolumen(pf: List[List[int]]):
        hv = get_performance_indicator("hv", ref_point=np.array([1, 1, 1,1]))
        return hv.do(pf)
    
    @staticmethod
    def calculate_hipervolumen_for_optimization(pf: List[List[int]]):
        hv = get_performance_indicator("hv", ref_point=np.array([2, 2, 2, 2]))
        return (hv.do(pf))/2

    @staticmethod  
    def generate_matriz_fitness(frente: List[Solution]):
        weights=[]
        for soluction in frente:
            weights.append(soluction.fitness)
        return weights


