import numpy as np
from typing import List
from dominio.Solution import Solution
from pymoo.visualization.scatter import Scatter
from pymoo.factory import get_performance_indicator

class Hipervolumen:
    @staticmethod
    def calculate_hipervolumen(pf: List[List[int]]):
        # pf = Hipervolumen.generate_matriz_fitness(frente)
        # pf = np.array(frente)
        # A = pf *1
        # Scatter(legend=True).add(pf, label="Pareto-front").add(A, label="Result").show()
        # Scatter(legend=True).add(pf, label="Pareto-front").show()
        hv = get_performance_indicator("hv", ref_point=np.array([1, 1, 1,1]))
        return hv.do(pf)

    @staticmethod  
    def generate_matriz_fitness(frente: List[Solution]):
        weights=[]
        for soluction in frente:
            weights.append(soluction.fitness)
        return weights


