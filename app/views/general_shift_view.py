from django.conf import settings
from dominio.Metaheuristics.GRASP import Grasp
from dominio.Metaheuristics.NSGA_II import NsgaII
from dominio.vigilant_assigment import VigilantAssigment
from dominio.Solution import Solution
from utils.graph import Graph
from utils.hipervolumen import Hipervolumen
from utils.print_xls import generate_results
from dominio.model.problem import DataSites, DataVigilantes
import pprint
import time
import json
class GenerateShiftView:

    def __init__(self, data: object):
        # self.__data_sites = self.create_sites(data)
        # self.__data_vigilantes = self.create_vigilantes(data)
        self.__data_sites = self.create_sites_test(data)
        self.__data_vigilantes = self.create_vigilantes_test(data)

        self.__myProblem: VigilantAssigment = VigilantAssigment(self.__data_vigilantes, self.__data_sites)
        self.__algoritmGrasp = Grasp()
        self.__algoritmNSGA = NsgaII()

    def create_sites(self, data) -> json:
        return DataSites.from_dict(data).data_sites
    
    def create_vigilantes(self, data):
        return DataVigilantes.from_dict(data).data_vigilantes

    def create_sites_test(self, data) -> json:
        json_problem = None
        with open("dataset/sites.json") as json_file:
            json_problem = json.load(json_file)
        json_file.close()
        return DataSites.from_dict(json_problem).data_sites

    def create_vigilantes_test(self, data):
        json_vigilantes = None
        with open("dataset/vigilantes.json") as json_file:
            json_vigilantes = json.load(json_file)
            json_file.close()
        return DataVigilantes.from_dict(json_vigilantes).data_vigilantes

    def execute(self):
        print("Start")
        tic = time.perf_counter()
        best_solutions= self.__algoritmNSGA.Execute(self.__myProblem)
        Hipervolumen.calculate_hipervolumen(best_solutions)
        best_solutions = self.__algoritmGrasp.Execute(self.__myProblem)
        Hipervolumen.calculate_hipervolumen(best_solutions)
        toc = time.perf_counter()
        # generate_results(solution)
        print(f"Time {toc - tic:0.4f} seconds")