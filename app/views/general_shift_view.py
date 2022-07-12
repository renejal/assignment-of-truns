from copy import deepcopy
from typing import List
from services.reference_point import Reference_point
from dominio.Solution import Solution
from utils.normalize import Normalize
from dominio.Metaheuristics.GRASP import Grasp
from dominio.Metaheuristics.NSGA_II import NsgaII
from dominio.vigilant_assigment import VigilantAssigment
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
        self.__reference_points_IGD = Reference_point().get_reference_points_from_IGD()

    def create_sites(self, data) -> json:
        return DataSites.from_dict(data).data_sites
    
    def create_vigilantes(self, data):
        return DataVigilantes.from_dict(data).data_vigilantes

    def executeGrasp(self):
        print("Start Grasp")
        ticGrasp = time.perf_counter()
        data_grasp = self.__algoritmGrasp.Execute(deepcopy(self.__myProblem))
        tocGrasp = time.perf_counter()
        return self.getMetrics(data_grasp[0],data_grasp[1],ticGrasp,tocGrasp)

    def executeNsga(self):
        print("Start Nsga")
        ticNsga = time.perf_counter()
        data_nsgaii= self.__algoritmNSGA.Execute(deepcopy(self.__myProblem))
        tocNsga = time.perf_counter()
        return self.getMetrics(data_nsgaii[0],data_nsgaii[1],ticNsga,tocNsga)
       
    def getMetrics(self,solutions:List[Solution],fig, tic:int,toc:int):
        metrics = {}
        solutionsNormalized = Normalize().normalizeFitness(solutions)
        pf = np.array(solutionsNormalized)
        hv = Hipervolumen.calculate_hipervolumen(pf)
        igd = get_performance_indicator("igd", np.array(self.__reference_points_IGD))
        igd = igd.do(np.array(pf))
        # igd = get_performance_indicator("igd", pf)
        # igd = igd.do(np.array(self.__reference_points_IGD))
        print(igd)
        metrics["solutions"] = solutions
        metrics["fitnesses"] = solutionsNormalized
        metrics["hv"] = hv
        metrics["igd"] = igd
        metrics["time"] = toc - tic
        metrics["fig"] = fig
        return metrics

    def create_sites_test(self, data) -> json:
        json_problem = None
        with open("app/dataset/sites.json") as json_file:
            json_problem = json.load(json_file)
        json_file.close()
        return DataSites.from_dict(json_problem).data_sites

    def create_vigilantes_test(self, data):
        json_vigilantes = None
        with open("app/dataset/vigilantes.json") as json_file:
            json_vigilantes = json.load(json_file)
            json_file.close()
        return DataVigilantes.from_dict(json_vigilantes).data_vigilantes

