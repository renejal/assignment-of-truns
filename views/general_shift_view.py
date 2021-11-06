from dominio.Metaheuristics.GRASP import Grasp
from data.SiteDataFile import SiteDataFile
from data.VigilantsDataFile import VigilantsDataFile
from dominio.vigilant_assigment import VigilantAssigment
from dominio.Solution import Solution
from utils.print_sites_xls import generateResultBySite
from utils.print_vigilants_xls import generateResultByVigilant
from utils.print_xls import generate_results
import time
class GenerateShiftView:

    __algoritmGrasp = Grasp()
    __algoritmNSGA = None
    __myProblem: VigilantAssigment = VigilantAssigment("dataset/userInterface.csv", "dataset/vigilants.csv", 4)
    __myProblem.get_workig_day()

    def getShiftViglants(self):
        print("Start")
        tic = time.perf_counter()
        response: Solution = self.__algoritmGrasp.Execute(self.__myProblem, 0, 1)
        toc = time.perf_counter()
        self.__generateResults(0, 10, response)
        print(f"Time {toc - tic:0.4f} seconds")

    def __generateResults(self, CurrentEFOs, MaxEFOs, response: Solution):
        if CurrentEFOs == 0:
            self.__generateResults_xls('./views/FirstResult', response)
        elif CurrentEFOs == MaxEFOs / 2:
            self.__generateResults_xls('./views/FResults/HalfResult', response)
        elif CurrentEFOs == MaxEFOs - 1:
            self.__generateResults_xls('./views/Results/FinalResult', response)

    def __generateResults_xls(self, path, solution):
        generate_results(solution)
        generateResultBySite(self.__myProblem.cantVigilantsByPeriod, path, solution)
        generateResultByVigilant(path, solution)


