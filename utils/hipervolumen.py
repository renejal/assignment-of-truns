import numpy as np
from typing import List
from dominio.Solution import Solution
from pymoo.visualization.scatter import Scatter
from pymoo.factory import get_performance_indicator
from pymoo.factory import get_problem


class Hipervolumen:
    @staticmethod
    def calculate_hipervolumen(frente: List[Solution]):
        pf = Hipervolumen.generate_matriz_fitness(frente)
        # pf = get_problem("zdt1").pareto_front()
        # pf = np.empty([20,2])
        # pf = np.array(
        #     [[1,2]])
        # A = pf * 1.1
        print(pf)
        pf = np.array(pf)
        # print("pf",pf)
        A = pf * 1
        Scatter(legend=True).add(pf, label="Pareto-front").add(A, label="Result").show()
        hv = get_performance_indicator("hv", ref_point=np.array([1, 1]))
        print("hv", hv.do(A))

    @staticmethod  
    def generate_matriz_fitness(frente: List[Solution]):
        # Todo : solo hay una iteracion, valdiar el motivo si es neceasrio gnar mas itearcions para genear
        # un frente de pareto mas grandes.
        weights=[]
        for indx, soluction in enumerate(frente):
            weights.append(soluction.fitness)
        return weights



# Hipervolumen.calculate_hipervolumen(None) 