#from dominio.Metaheuristics.GRASP import Grasp
#from data.SiteDataFile import SiteDataFile
#from data.VigilantsDataFile import VigilantsDataFile
from dominio.vigilant_assigment import VigilantAssigment
from dominio.Solution import Solution
#from utils.print_sites_xls import generateResultBySite
#from utils.print_vigilants_xls import generateResultByVigilant
#from utils.print_xls import generate_results
from dominio.problem import DataSites
from dominio.problem import DataVigilantes
import time
import json
class GenerateShiftView:

    def __init__(self, path_site: str, path_vigilantes: str):
        self.__data_sites = self.create_sites(path_site)
        self.__data_vigilantes = self.create_vigilantes(path_vigilantes)
        self.__algoritmNSGA = None
        self.__myProblem: VigilantAssigment = VigilantAssigment(self.__data_vigilantes, self.__data_sites, 4)
        # self.___myProble.get_workig_day()

    def create_sites(self, path) -> json:
        json_problem = None
        with open(path) as json_file:
            json_problem = json.load(json_file)
        json_file.close()
        __data_Sites = DataSites.from_dict(json_problem)

    def create_vigilantes(self, path):
        json_vigilantes = None
        with open(path) as json_file:
            json_vigilantes = json.load(json_file)
            json_file.close()
            __dataVigilantes = DataVigilantes.from_dict(json_vigilantes)

    def getShiftViglants(self):
        print("Start")
        tic = time.perf_counter()
        response: Solution = self.__algoritmGrasp.Execute(self.__vigilantes, 0, 1)
        toc = time.perf_counter()
        self.__generateResults(0, 10, response)
        print(f"Time {toc - tic:0.4f} seconds")

"""
    def __generateResults(self, CurrentEFOs, MaxEFOs, response: Solution):
        if CurrentEFOs == 0:
            self.__generateResults_xls('./views/FirstResult', response)
        elif CurrentEFOs == MaxEFOs / 2:
            self.__generateResults_xls('./views/FResults/HalfResult', response)
        elif CurrentEFOs == MaxEFOs - 1:
            self.__generateResults_xls('./views/Results/FinalResult', response)

    def __generateResults_xls(self, path, solution):
        generate_results(solution)
        generateResultBySite(self.__vigilantes.cantVigilantsByPeriod, path, solution)
        generateResultByVigilant(path, solution)
"""