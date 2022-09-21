from copy import deepcopy
from datetime import datetime
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
from utils.graph import Graph

class GenerateShiftView:

    def __init__(self, data: object):
        self.__data_sites = self.create_sites(data)
        self.__data_vigilantes = self.create_vigilantes(data)
        self.__myProblem: VigilantAssigment = VigilantAssigment(
            self.__data_vigilantes, self.__data_sites)
        self.algoritmGrasp = Grasp()
        self.algoritmNSGAII = NsgaII()
        self.__reference_points_IGD = Reference_point().get_reference_points_from_IGD()

    def create_sites(self, data) -> json:
        return DataSites.from_dict(data).data_sites
    
    def create_vigilantes(self, data):
        return DataVigilantes.from_dict(data).data_vigilantes

    def executeGrasp(self):
        print("Start Grasp")
        ticGrasp = time.perf_counter()
        data_grasp = self.algoritmGrasp.Execute(deepcopy(self.__myProblem))
        tocGrasp = time.perf_counter()
        fig = Graph(data_grasp).get_fig()
        return self.getMetrics(data_grasp,fig,ticGrasp,tocGrasp)
    
    def executeGraspToOptimize(self):
        print("Start Grasp")
        data_grasp = self.algoritmGrasp.Execute(deepcopy(self.__myProblem))
        #TODO unir todas las soluciones o solo retornar la final?
        return data_grasp[len(data_grasp)-1]

    def executeNsga(self):
        print("Start Nsga")
        ticNsga = time.perf_counter()
        data_nsgaii = self.algoritmNSGAII.Execute(deepcopy(self.__myProblem))
        tocNsga = time.perf_counter()
        fig = Graph(data_nsgaii).get_fig()
        return self.getMetrics(data_nsgaii,fig ,ticNsga,tocNsga)

    def executeNsgaIIToOptimize(self):
        print("Start Nsga II")
        data_nsgaII = self.algoritmNSGAII.Execute(deepcopy(self.__myProblem))
        return data_nsgaII[len(data_nsgaII)-1]
       
    def getMetrics(self, evolutions:List[List[Solution]], fig, tic:int, toc:int):
        metrics = {}
        fitnesses = []
        hv = []
        igd = []
        for pupulation in evolutions:
            solutionsNormalized = Normalize().normalizeFitness(pupulation)
            fitnesses.append(solutionsNormalized)
            pf = np.array(solutionsNormalized)
            hv.append(Hipervolumen.calculate_hipervolumen(pf))
            igdPerformance = get_performance_indicator("igd", np.array(self.__reference_points_IGD))
            igd.append(igdPerformance.do(np.array(pf)))
        metrics["evolutions"] = evolutions
        metrics["fitnesses"] = fitnesses
        metrics["hv"] = hv
        metrics["igd"] = igd
        metrics["time"] = self.calculate_time(tic,toc)
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
    
    def calculate_time(self, tic, toc):
        d = datetime.utcfromtimestamp(toc - tic)
        decimal_places = 3
        ndigits = decimal_places - 6
        r = round(d.microsecond, ndigits)
        if r > 999999:
            r = 999999
        d = d.replace(microsecond=r)
        return d.strftime("%H:%M:%S.%f")[:ndigits]

