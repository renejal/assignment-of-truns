from dominio.Metaheuristics.GRASP import Grasp
from dominio.Metaheuristics.NSGA_II import NsgaII
from dominio.vigilant_assigment import VigilantAssigment
from dominio.Solution import Solution
from utils.print_xls import generate_results
from dominio.model.problem import DataSites, DataVigilantes
import time
import json
class GenerateShiftView:

    def __init__(self, path_site: str, path_vigilantes: str):
        self.__data_sites = self.create_sites(path_site)
        self.__data_vigilantes = self.create_vigilantes(path_vigilantes)
        self.__myProblem: VigilantAssigment = VigilantAssigment(self.__data_vigilantes, self.__data_sites)
        self.__algoritmGrasp = Grasp()
        self.__algoritmNSGA = NsgaII()

    def create_sites(self, path) -> json:
        json_problem = None
        with open(path) as json_file:
            json_problem = json.load(json_file)
        json_file.close()
        return DataSites.from_dict(json_problem).data_sites

    def create_vigilantes(self, path):
        json_vigilantes = None
        with open(path) as json_file:
            json_vigilantes = json.load(json_file)
            json_file.close()
            return DataVigilantes.from_dict(json_vigilantes).data_vigilantes

    def execute(self):
        print("Start")
        tic = time.perf_counter()
        solution: Solution = self.__algoritmNSGA.Execute(self.__myProblem)
        # generate_results(solution)
        # solution: Solution = self.__algoritmGrasp.Execute(self.__myProblem)
        toc = time.perf_counter()
        generate_results(solution)
        print(f"Time {toc - tic:0.4f} seconds")