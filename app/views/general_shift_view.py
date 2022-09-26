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
from utils.igd import IGD
from dominio.model.problem import DataSites, DataVigilantes
import time
import json
import numpy as np
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
    
    def executeGraspToOptimize(self, amountPopulation):
        print("Start Grasp")
        data_grasp = self.algoritmGrasp.Execute(deepcopy(self.__myProblem))
        amountEvolutions = len(data_grasp)
        lastEvolution = data_grasp[amountEvolutions-1]
        if amountEvolutions == 1:
            return lastEvolution
        if(len(lastEvolution) >= amountPopulation):
            return lastEvolution
        else:
            return data_grasp[amountEvolutions-2]

    def executeNsga(self):
        print("Start Nsga")
        ticNsga = time.perf_counter()
        data_nsgaii = self.algoritmNSGAII.Execute(deepcopy(self.__myProblem))
        tocNsga = time.perf_counter()
        fig = Graph(data_nsgaii).get_fig()
        return self.getMetrics(data_nsgaii,fig ,ticNsga,tocNsga)

    def executeNsgaIIToOptimize(self, amountPopulation):
        print("Start Nsga II")
        data_nsgaII = self.algoritmNSGAII.Execute(deepcopy(self.__myProblem))
        amountEvolutions = len(data_nsgaII)
        lastEvolution = data_nsgaII[amountEvolutions-1]
        if amountEvolutions == 1:
            return lastEvolution
        if(len(lastEvolution) >= amountPopulation):
            return lastEvolution
        else:
            return data_nsgaII[amountEvolutions-2]
       
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
            igd.append(IGD.calculate_igd(pf, self.__reference_points_IGD))
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

