from typing import List
from dominio.Solution import Solution
from utils.normalize import Normalize
from dominio.Metaheuristics.GRASP import Grasp
from dominio.Metaheuristics.NSGA_II import NsgaII
from dominio.vigilant_assigment import VigilantAssigment
from utils.graph import Graph
from utils.hipervolumen import Hipervolumen
from dominio.model.problem import DataSites, DataVigilantes
import time
import json
import numpy as np
from pymoo.factory import get_performance_indicator

class GenerateShiftView:

    def __init__(self, data: object):
        self.__data_sites = self.create_sites(data)
        self.__data_vigilantes = self.create_vigilantes(data)
        self.__myProblem: VigilantAssigment = VigilantAssigment(
            self.__data_vigilantes, self.__data_sites)
        self.__algoritmGrasp = Grasp()
        self.__algoritmNSGA = NsgaII()

    def create_sites(self, data) -> json:
        # json_problem = None
        # with open(path) as json_file:
        #     json_problem = json.load(json_file)
        # json_file.close()
        return DataSites.from_dict(data).data_sites

    def create_vigilantes(self, data):
        # json_vigilantes = None
        # with open(path) as json_file:
        #     json_vigilantes = json.load(json_file)
        #     json_file.close()
        return DataVigilantes.from_dict(data).data_vigilantes

    def executeGrasp(self):
        print("Start Grasp")
        ticGrasp = time.perf_counter()
        best_solutionsGrasp = self.__algoritmGrasp.Execute(self.__myProblem)
        tocGrasp = time.perf_counter()
        return self.getMetrics(best_solutionsGrasp,ticGrasp,tocGrasp)


    
    def executeNsga(self):
        print("Start Nsga")
        ticNsga = time.perf_counter()
        best_solutionsNsga= self.__algoritmNSGA.Execute(self.__myProblem)
        tocNsga = time.perf_counter()
        return self.getMetrics(best_solutionsNsga,ticNsga,tocNsga)
       
    def getMetrics(solutions:List[Solution],tic:int,toc:int):
        metrics = {}
        solutionsNormalized = Normalize(solutions)
        hv = Hipervolumen.calculate_hipervolumen(solutionsNormalized)
        igd = get_performance_indicator("igd", np.array(solutionsNormalized))
        metrics["solutions"] = solutions
        metrics["fitnesses"] = solutionsNormalized
        metrics["hv"] = hv
        metrics["igd"] = igd
        metrics["time"] = toc - tic
        return metrics
